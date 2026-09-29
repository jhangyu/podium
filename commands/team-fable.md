---
description: "Fable-led hierarchical squad orchestration: the main agent commands 1-3 squads (opus squad-lead + task-derived implementers + conditional haiku test-runner) through round-based milestones with handoff docs and strict chain-of-command reporting"
argument-hint: "<task description> [--squads N] [--name team-name] [--logs-dir path]"
---

# team-fable — Hierarchical Squad Orchestration

Round-based multi-squad orchestration for large tasks. The **main agent** (the agent invoking
this command — the strongest available model) is the **Orchestrator**: it owns task direction,
round decisions, and user reporting. Never spawn a separate agent to fill the orchestrator
role — only the main agent can reach the user.

## Hierarchy

```
User
 └─ Orchestrator (main agent) — direction, round decisions, reviewer dispatch, user reporting
     ├─ Squad {purpose1}
     │   ├─ {purpose1}-lead-{model}        team-lead         model: opus
     │   ├─ {purpose1}-impl-1..N-{model}   task-derived specialist (see Phase 1 step 4)
     │   └─ {purpose1}-test-{model}        team-test-runner  model: haiku (only if a runnable test command exists)
     └─ Squad {purpose2} (same shape)   [Squad B/C only if task width truly requires them]
```

Teams are **flat** — squads are a logical grouping enforced by the communication protocol
embedded in every member's task prompt, not by the harness. Name members with a purpose-based
squad prefix AND a model suffix so routing rules are unambiguous and the model of every pane
is visible at a glance; the naming rule is owned by the reporting protocol
(${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md).

## Pre-flight

1. Do NOT pre-check the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var; if spawning fails with a teams-disabled error, halt and instruct the user to set it to 1.
2. Parse arguments:
   - Positional: the overall task description
   - `--squads N`: squad count (default **2**, hard max **3**)
   - `--name <team-name>`: override default team name (`fable-team`)
   - `--logs-dir <path>`: handoff docs root (default `./docs/logs`)
3. Confirm the working directory is a git repository (worktree isolation requires it).

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Round Lifecycle

A **round** = one milestone. Follow the rounds and review protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md and apply it — it owns the round definition, the round-end condition, the review cadence, and the orchestrator's duties during a round (spot-checks, stall watchdog, escalation).

### Phase 1 — Decompose (orchestrator, before any spawn)

1. Define this round's milestone with mechanically checkable acceptance criteria, per the rounds and review protocol.
2. Split into squad-scoped work packages with exclusive file ownership per squad. Follow the file ownership protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/file-ownership.md and apply it.
3. Create one git worktree per squad. Follow the worktree lifecycle protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md and apply it.
4. Derive each squad's composition (squad count, implementer count and identity, conditional test-runner, model assignment) from its work package, not from a fixed roster. Follow the member selection protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/member-selection.md and apply it.
5. Output the allocation plan (squads, members with their source tier, models, file
   ownership, worktree paths) before spawning.

### Phase 2 — Spawn

1. Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY: `TeamCreate` with `displayMode: "tmux"`; IMPLICIT: skip).
2. Spawn **all** members from the orchestrator (squad leads never spawn agents). Every
   spawn call's `name` MUST follow the member naming rule in the reporting protocol
   (${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md).
3. `TaskCreate` per squad member. Every squad member prompt MUST embed the protocol blocks
   listed below, the member's file ownership list, worktree path, acceptance criteria, and
   paths to prior-round handoff docs (if any).

#### Protocol blocks to embed in member prompts

- **Communication, reporting, and baton rotation**: follow the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.
- **Git red lines and file ownership**: follow the file ownership protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/file-ownership.md and apply it.
- **Verification (embed in reviewer prompts)**: follow the verification protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/verification.md and apply it.

### Phase 3 — Execute & Review

The orchestrator runs the round: it receives squad-lead summaries only, dispatches the round reviewer over the round's combined diff once every squad has reported complete, routes reviewer issues back to the originating squad lead, spot-checks key claims against evidence, and watches for members that end a turn without delivering. Follow the rounds and review protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md and apply it; the reviewer prompt embeds the verification protocol (${CLAUDE_PLUGIN_ROOT}/protocols/verification.md) and the git red lines (${CLAUDE_PLUGIN_ROOT}/protocols/file-ownership.md).

### Phase 4 — Close the Round

Close the round in this order: verify the round-end condition, have each squad lead write its handoff doc, merge and re-verify, clean up the round's worktrees in the same round, report the round's results to the user (stopping for any decision the user must make), then shut down all round members and verify no residue. Follow the rounds and review protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md and apply it, together with the worktree lifecycle protocol (${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md) for merge/cleanup and the shutdown protocol (${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md) for member teardown.

### Phase 5 — Close the Task (after the final round)

Merge back to `main`, re-verify on `main`, prove zero residue, and report the final state to the user. Follow the worktree lifecycle protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md and apply it.

## Round Report Format (to the user)

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

## Hard Rules

- Default 2 squads; open a third only when the task genuinely has three independent streams.
- Squad leads and members NEVER spawn subagents, teams, or workflows. Needing delegation
  means: stop and report up the chain.
- Task closure, signoff, and baton rotation are governed by the reporting protocol
  (${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md); review loops, retries, and round bounds by
  the rounds and review protocol (${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md).
