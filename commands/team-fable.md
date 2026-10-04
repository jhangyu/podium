---
description: "Fable-led hierarchical squad orchestration: the main agent commands 1-3 squads (opus squad-lead + task-derived implementers + conditional haiku test-runner) through round-based milestones with handoff docs and strict chain-of-command reporting"
argument-hint: "<task description> [--squads N] [--name team-name] [--logs-dir path]"
---

# team-fable — Hierarchical Squad Orchestration

The **main agent** is the Orchestrator: task direction, round decisions, reviewer dispatch, user reporting. Never spawn an agent to fill this role — only the main agent reaches the user. `P` = `${CLAUDE_PLUGIN_ROOT}/protocols/`.

```
User
 └─ Orchestrator (main agent)
     ├─ Squad {purpose}: {purpose}-lead-opus (team-lead) · {purpose}-impl-1..N-{model} (task-derived) · {purpose}-test-haiku (team-test-runner, only if a runnable test command exists)
     └─ Squad B/C — same shape, only if the task has truly independent streams
```
The team is flat; squads exist only through the routing rules embedded in member prompts. Naming rule: `P/reporting.md`.

## Pre-flight
- Args: task description; `--squads N` (default 2, max 3); `--name` (default `fable-team`); `--logs-dir` (handoff root, default `./docs/logs`).
- Must be in a git repo (worktrees). Do not pre-check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; on a teams-disabled error, halt and tell the user to set it to `1`.

## Rounds (one round = one milestone; `P/rounds-and-review.md` owns definition, end condition, review cadence, orchestrator duties)

**1 — Decompose (before any spawn).** Milestone with mechanically checkable acceptance criteria → squad work packages with exclusive file ownership (`P/file-ownership.md`) → one worktree per squad (`P/worktree-lifecycle.md`) → squad composition and models from each package (`P/member-selection.md`) → print allocation plan (squads, members + source tier, models, ownership, worktree paths).

**2 — Spawn (orchestrator only; squad leads never spawn).** Every `Agent` call carries ALL of: `name` (`{purpose}-{role}-{model}`, session-unique), `team_name` (the team label — always include it: legacy gates require it; harmless in IMPLICIT), `subagent_type`, explicit `model`. Every prompt contains `ROLE: WORKER — you may NOT spawn agents, teams, or workflows. If the task needs delegation, STOP and report back.` and its report route (squad members → their squad lead; leads → `team-lead`, falling back to `main` if unreachable). Spawn all members in one message. If a `TeamCreate` tool exists in this build, create the team with it first (`displayMode: "tmux"`). Then `TaskCreate` per member embedding: reporting/baton block (`P/reporting.md`), git red lines (`P/file-ownership.md`), owned files, worktree path, acceptance criteria, prior-round handoff paths.

**3 — Execute and review.** Orchestrator receives squad-lead summaries only; once all squads report complete, dispatches one round reviewer over the combined diff (prompt embeds `P/verification.md` + `P/file-ownership.md`), routes issues to the originating squad lead, spot-checks claims, runs the stall watchdog.

**4 — Close the round, in order:** verify end condition → each squad lead writes its handoff doc → merge + re-verify → remove the round's worktrees (`P/worktree-lifecycle.md`) → report to user, stopping for any user decision → shut down all round members and verify zero residue (`P/shutdown.md`).

**5 — Close the task (after final round).** Merge to `main`, re-verify on `main`, prove zero residue, report final state (`P/worktree-lifecycle.md`).

## Round report (to user)
```
Round {N} — {milestone}
  Squad A: {shipped} | tests: {PASS/FAIL}
  Squad B: ...
  Review: {clean / N issues fixed / escalated}
  Merged: {branch @ hash}
  Handoffs: {paths}
  Open questions: {none | list — awaiting your decision}
Next round plan: {milestone or "task complete"}
```

## Hard rules
- Default 2 squads; a third only for a genuinely third independent stream.
- Leads and members never spawn agents, teams, or workflows; needing delegation = stop and report up.
- Signoff, task closure, baton rotation, language: `P/reporting.md`. Review loops, retries, round bounds: `P/rounds-and-review.md`.
