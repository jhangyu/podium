The four-phase graceful team shutdown — doc flush, ordered member shutdown, cleanup, and the residue checks that prove the team is gone.

Referenced by: `podium:team-shutdown`, `podium:team-fable`, `podium:team-spawn`.

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
2. If yes: call SendMessage to `team-doc-updater` (subagent_type: `podium/team-doc-updater`) with:
   > "Final flush before shutdown. Please complete any pending documentation updates and confirm when done."
3. Wait for team-doc-updater to confirm (or timeout after 60 seconds).
4. Report: "Docs flushed: {list of files updated}".

If `--skip-doc-flush` is set or `team-doc-updater` is not in the team: skip this phase and note it in the summary.

## Phase 3: Graceful Shutdown

Send shutdown messages in the following order:

1. **Implementers, reviewers, debuggers** (in parallel)
2. **team-test-runner**
3. **team-doc-updater**
4. **team-lead / squad leads** (last)

For each member:

1. Call SendMessage with `type: "shutdown_request"`:
   > "Team shutdown requested. Please finish your current work, save any state, and confirm shutdown."
2. If `--force` is not set: wait for shutdown confirmation response before proceeding to the next group.
3. Mark the member as shut down.

## Phase 4: Cleanup

Display the shutdown summary:

```
Team "{team-name}" shutdown complete.

Members shut down: {N}/{total}
Tasks completed: {completed}/{total}
Tasks remaining: {remaining}
Docs updated: {list from doc-updater flush}
```

Unless `--keep-tasks` is set: call `TeamDelete` to remove the team and task directories under `~/.claude/teams/{team-name}/`.

## Residue Checks

After `TeamDelete`, verify no residue remains:

- No residual tmux session for the team (`tmux ls`).
- `git worktree list` shows only the main tree; no leftover squad branches (`git branch --merged main` cleanup with `-d`) — see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`.
- No stray `tmp/verify/` output or detached processes left running.

The same ordered shutdown flow (members → test-runners → leads, then `TeamDelete`) applies when closing out an intermediate round, not just at the end of the task.
