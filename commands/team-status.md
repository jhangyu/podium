---
description: "Display team members, task status, progress, and reactive agent states for an active agent team"
argument-hint: "[team-name] [--tasks] [--members] [--json]"
---

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 1: Team Discovery

1. Parse args: team name, `--tasks`, `--members`, `--json`
2. If no team name is provided:
   - Check `~/.claude/teams/` for active team directories
   - If exactly one team exists: use it automatically
   - If multiple teams exist: list them and ask the user to choose
3. Read team config from `~/.claude/teams/{team-name}/config.json`
4. Call TaskList to retrieve current task state

---

## Phase 2: Status Display

### Members Table

Distinguish reactive agents (`team-test-runner`, `team-doc-updater`) from task workers. Reactive agents show their last known activity instead of a task count.

```
Team: {team-name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Members:
  Name                Role                   Status
  ──────────────────────────────────────────────────────
  team-lead           orchestrator           coordinating
  implementer-1       team-implementer       working on task #2
  implementer-2       team-implementer       idle
  team-test-runner    [reactive]             waiting / last: PASS #3
  team-doc-updater    [reactive]             idle / last update: README.md
  arch-reviewer       architect-reviewer     working on task #5
```

### Tasks Table

```
Tasks:
  ID   Status        Owner           Subject
  ──────────────────────────────────────────────────────────
  #1   completed     implementer-1   Implement auth module
  #2   in_progress   implementer-1   Add rate limiting
  #3   completed     [test-runner]   Verify auth tests — PASS
  #4   pending       (unassigned)    Update API docs
  #5   in_progress   arch-reviewer   Review service boundaries

Progress: 40% (2/5 completed)
Test runs: 1 PASS, 0 FAIL
Doc updates: 0 pending
```

- If `--members` flag is set: show only the Members table
- If `--tasks` flag is set: show only the Tasks table
- If neither flag is set: show both tables

### JSON Output

If `--json` is set: output raw team config merged with current task list as a single JSON object. Skip all formatted display.
