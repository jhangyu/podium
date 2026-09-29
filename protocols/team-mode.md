Team mode detection — behavior on legacy Claude Code (explicit teams) vs >= 2.1.178 (implicit team).

Referenced by: every command that creates or shuts down a team, `protocols/shutdown.md`, `protocols/reporting.md`.

## Detect the mode (once, before any team creation)

ToolSearch query `select:TeamCreate`.

- Schema returned → **LEGACY** (< 2.1.178): `TeamCreate` → `Agent(team_name + name)` → `TeamDelete`.
- Not found → **IMPLICIT** (>= 2.1.178): `TeamCreate`/`TeamDelete` do not exist; the session itself is the one and only team.

Both modes require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, but do not pre-check it — a teams-disabled spawn error is the signal to halt and ask the user to set it. A command step "create the team": LEGACY → call `TeamCreate` as written; IMPLICIT → skip.

## IMPLICIT mode rules

1. **No TeamCreate / TeamDelete.** One team per session; no second named team. Team names in commands (`debug-{timestamp}` etc.) are labels only (output, worktree/branch names, docs).
2. **Spawn** with `Agent(name=<unique role name>, team_name=<team label>, subagent_type, model, prompt)`. The harness ignores `team_name`, but delegation-gate hooks reject Agent calls without it — always include it.
3. **Unique names are mandatory.** A duplicate `name` silently creates a second agent. Check each name against members already spawned this session; suffix (`-2`) if taken. Address members by exact name.
4. **Tasks**: `TaskCreate`/`TaskUpdate`/`TaskList` still work (may be deferred — load via ToolSearch `select:TaskCreate,TaskUpdate,TaskList`). `TaskUpdate owner=<name>` auto-delivers a task_assignment message.
5. **Reply address**: members report via `SendMessage`; the lead's address is `team-lead` or `main` depending on harness (headless `-p` uses `main`; interactive unverified). Every member prompt must say: "Report via SendMessage to `team-lead`; if unreachable ('No agent named ... is reachable'), send to `main`." Members with a squad lead/owner report to that member.
6. **Cleanup (no TeamDelete)**: find the session team dir via `ls ~/.claude/teams/`, picking the one whose config.json lists your members. No config.json → skip the snapshot/drain script; verify shutdown via `pgrep` of member processes (and `tmux ls`). Shut members down via `shutdown_request` (order in `protocols/shutdown.md`); in headless (`-p`) sessions it reports send-success and lands in the member's inbox file but background agents never consume it (verified on 2.1.284), so treat it as best-effort and treat `pgrep` as the authoritative shutdown check. Verify none alive, then optionally remove `~/.claude/teams/<session-uuid>/` and `~/.claude/tasks/<session-uuid>/` (the session UUID dir, not a made-up label). Remove only after shutdown verification passed.

## LEGACY mode

Follow the command text as written (`TeamCreate` with `displayMode: "tmux"`, `Agent` with `team_name`, `TeamDelete` at shutdown). Members report to `team-lead`.
