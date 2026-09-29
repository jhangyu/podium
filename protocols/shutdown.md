The authoritative team shutdown sequence — pane snapshot, doc flush, ordered shutdown requests, drain, gated TeamDelete, and final verification.

Referenced by: `podium:team-shutdown`, `podium:team-fable`, `podium:team-spawn`, `podium:team-review`, `podium:team-debug`, `podium:team-feature`, `podium:team-performance`, `podium:team-refactor`, `podium:team-techdebt`.

Shutting a team down is not just "send shutdown_request and call TeamDelete". A member accepting a shutdown request does not mean its process exited, and once the team config is deleted the pane-to-team mapping is gone — leaving orphan tmux panes that cannot be safely identified afterwards. The helper script `${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py` provides the mechanical steps; every phase below is mandatory and ordered.

## Phase 0: Snapshot the pane mapping (before anything else)

Must run before `TeamDelete`, and must return `ok: true` before any later phase proceeds:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py snapshot <team-name>
```

The script reads the member/pane mapping from the team config, scans every `/tmp/tmux-<uid>/claude-swarm-*` socket, and matches pane ownership. It records:

- `cleanup_mode` — `"server"` when every live pane on the socket belongs to this team, or `"pane"` when the socket also carries panes from elsewhere.
- `target_panes` — the pane IDs belonging to this team.
- `outside_panes` — live pane IDs on the same socket that do NOT belong to this team (present only when `cleanup_mode` is `"pane"`).

A **mixed socket is not a failure** — the snapshot succeeds and records both lists. **Ambiguous matching is fail-closed**: if several sockets match equally and cannot be told apart, the script refuses to write a snapshot rather than guess.

Pane matching is strict: a pane counts as a team member's only when the pane ID, the agent type appearing in the pane title, AND the recorded cwd all match the team config. Config or title drift therefore produces a zero-match snapshot, not a wrong match. **A zero-match snapshot is NOT a pass**: `ok: true` with `socket: null` or an empty `target_panes` means the team's panes could not be identified — treat it as a failure, investigate (config drift? panes already gone? title mismatch?), and do not proceed to `TeamDelete` on its strength. Always print the snapshot JSON and check `target_panes` is non-empty before continuing.

Successful output (mixed socket):

```json
{
  "team": "my-team",
  "phase": "snapshot",
  "ok": true,
  "socket": "/tmp/tmux-1000/claude-swarm-abc123",
  "cleanup_mode": "pane",
  "target_panes": ["%1", "%2"],
  "outside_panes": ["%0"],
  "live_panes": [{"id": "%1", "pid": "…", "command": "…", "title": "…"}, {"id": "%2", "…": "…"}]
}
```

If the snapshot returns `ok: false`, STOP — do not proceed, and never call `TeamDelete`.

## Phase 1: Pre-Shutdown

1. Parse args: team name, `--force`, `--keep-tasks`, `--skip-doc-flush`.
2. Read team config from `~/.claude/teams/{team-name}/config.json`.
3. Call TaskList to check for in-progress tasks.
4. If in-progress tasks exist and `--force` is **not** set:
   - Warn the user.
   - List all in-progress tasks with their owners.
   - Ask: "These tasks are still in progress. Proceed with shutdown anyway? (y/n)".
   - Abort if the user declines.

## Phase 2: Documentation Flush

Unless `--skip-doc-flush` is set:

1. Check if `team-doc-updater` is present in the team config.
2. If yes: call SendMessage to the `team-doc-updater` team member with:
   > "Final flush before shutdown. Please complete any pending documentation updates and confirm when done."
3. Wait for team-doc-updater to confirm (or timeout after 60 seconds).
4. Report: "Docs flushed: {list of files updated}".

If `--skip-doc-flush` is set or `team-doc-updater` is not in the team: skip this phase and note it in the summary.

## Phase 3: Ordered Shutdown Requests

Send a `shutdown_request` to every member named in the config, in this order:

1. **Implementers, reviewers, debuggers** (in parallel)
2. **team-test-runner**
3. **team-doc-updater**
4. **team-lead / squad leads** (last)

For each member:

1. Call SendMessage with `type: "shutdown_request"`:
   > "Team shutdown requested. Please finish your current work, save any state, and confirm shutdown."
2. If `--force` is not set: wait for the shutdown confirmation response before proceeding to the next group.
3. Mark the member as shut down.

An `approve: true` response means the request was accepted — it is NOT evidence that the process exited. Neither `shutdown_approved` nor an idle notification proves termination; only Phase 4 does.

## Phase 4: Drain (wait for exit, then clear residual panes)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py drain <team-name> --timeout 15
```

Requires a successful snapshot. `--timeout` is capped at 25 seconds (the script clamps anything higher and says so, keeping a single invocation under the 30s command timeout). Draining is not a one-shot: if panes are still alive and you simply need to keep waiting, **re-run the same drain command** rather than raising the timeout or sleeping.

Behavior:

1. Wait for the target panes recorded in the snapshot to exit on their own.
2. If target panes are still alive after the timeout, terminate according to `cleanup_mode`:
   - **`cleanup_mode: "server"`** (exclusive socket) → `tmux -S <socket> kill-server`.
   - **`cleanup_mode: "pane"`** (mixed socket) → `tmux -S <socket> kill-pane -t <pane-id>` for each target pane **individually**, re-listing panes first to confirm the target pane ID still exists. **NEVER** send any command touching `outside_panes`; never use a wildcard, window, or server target.
3. If socket ownership is ambiguous, refuse to terminate and return `ok: false`.

Required output before continuing:

```json
{"phase": "drain", "ok": true, "live_panes": []}
```

If drain returns `ok: false`, STOP — do not call `TeamDelete`.

## Mode note

Detect the mode per `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md`. Phases 0–4 (snapshot, doc flush, shutdown requests, drain) are identical in both modes; only Phase 5 differs. IMPLICIT: config lives at `~/.claude/teams/<session-uuid>/` — use that as `<team-name>` for the scripts; find it via `ls ~/.claude/teams/` (the one whose config.json lists your members). No config.json → skip the snapshot/drain script and verify shutdown via `pgrep` of member processes (and `tmux ls`); the optional dir removal may then proceed.

## Phase 5: Delete metadata (TeamDelete)

Run only after snapshot **and** drain have both succeeded, and unless `--keep-tasks` is set:

LEGACY mode:

```text
TeamDelete
```

IMPLICIT mode (no TeamDelete tool): skip the call. The session-level team dirs remain; after snapshot and drain both succeeded, they may optionally be removed with `rm -rf ~/.claude/teams/<session-uuid> ~/.claude/tasks/<session-uuid>` (confirm the path is the current session's UUID directory first). If either gate failed, leave them untouched.

This removes the team and task directories under `~/.claude/teams/{team-name}/`.

**If either snapshot or drain failed, calling `TeamDelete` is forbidden.** Deleting the config destroys the pane-ownership evidence and makes residual panes impossible to clean up safely. Keep the config and the snapshot, fix the problem, and re-run drain.

In LEGACY mode never delete team/task directories by hand — metadata cleanup is `TeamDelete`'s job. In IMPLICIT mode the manual removal above is the only cleanup.

## Phase 6: Final verification

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py verify <team-name>
```

Completion criterion — both must hold: no live **target** panes remain AND the team metadata is gone. The lead's own pane is intentionally outside the mechanism: when the invoking session is the lead it has no team pane at all, and a spawned squad-lead pane is excluded from `target_panes` by the script — it is expected to end with its own session, not via drain. `outside_panes` are never waited on or touched.

```json
{"phase": "verify", "ok": true, "live_panes": []}
```

The snapshot survives `TeamDelete` at `/tmp/claude-team-shutdown/<team>.json` so that verify and post-mortem diagnosis still work. If `ok: false`: fix the reported error and re-run the same step until it succeeds. A bare `tmux ls` without `-S` is NOT a valid check.

Then display the shutdown summary:

```
Team "{team-name}" shutdown complete.

Members shut down: {N}/{total}
Tasks completed: {completed}/{total}
Tasks remaining: {remaining}
Docs updated: {list from doc-updater flush}
```

## Command Summary

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py snapshot <team-name>
# SendMessage: shutdown_request to each member, in order
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py drain <team-name> --timeout 15   # re-run to keep waiting; max 25
# TeamDelete (legacy only; implicit mode: optional rm of session dirs; only after snapshot AND drain both succeeded)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py verify <team-name>
```

`status <team-name>` is also available for an inspection-only read of the current pane state.

## Safety Rules

- **Snapshot and drain must BOTH succeed before `TeamDelete`**; if either fails, deleting metadata is forbidden — pane ownership cannot be re-established once the config is gone.
- **A mixed socket is not a failure**: the snapshot records target and outside pane lists, and drain terminates only target panes, never touching outside panes.
- **Exclusive socket** (every live pane belongs to the target team) → `kill-server`; **mixed socket** → per-pane `kill-pane`, never `kill-server`.
- `shutdown_approved` and idle notifications are not evidence of process termination.
- Ambiguous socket matching (several sockets match equally and cannot be distinguished) → fail closed: refuse both snapshot and termination.
- The default tmux socket is never scanned; the script scans every `/tmp/tmux-<uid>/claude-swarm-*` socket.
- LEGACY: never remove team/task directories manually. IMPLICIT: only as described in Phase 5, after the gates passed.

## Residue Checks

After a verified `TeamDelete`, confirm nothing else is left behind:

- `git worktree list` shows only the main tree; no leftover squad branches (`git branch --merged main` cleanup with `-d`) — see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`.
- No stray `tmp/verify/` output or detached processes left running.

The same ordered flow applies when closing out an intermediate round, not just at the end of the task.
