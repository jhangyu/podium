How results actually reach their destination: end-of-turn delivery, artifact-first evidence, chain of command, naming, signoff, and baton rotation.

Referenced by: `podium:team-spawn`, `podium:team-fable`, `podium:team-delegate`, `podium:team-status`.

## Reporting Discipline (embed in every member task prompt)

- **End-of-turn delivery**: plain text output is INVISIBLE to teammates — delivery only happens via a SendMessage tool call. Any turn that produced results (test output, completed work, findings, a verdict) MUST end with SendMessage to the team-lead / squad lead (or to the main agent, in presets without a lead) as the LAST action of that turn; results not sent before the turn ends die with the turn and stall the team.
- **Artifact-first verification**: whoever runs verification commands (test-runner or lead) writes the raw output to a file in the working tree or worktree (e.g. `tmp/verify/<timestamp>.txt`) BEFORE reporting; the report message carries the file path + a one-line summary. A dropped message then loses nothing — the lead recovers by reading the file.
- **Long-running processes**: never babysit. Launch detached (nohup + log file), sanity-check once, then report PID + log path to your lead and yield. Repeated polling of a still-running process is the signal to stop and report instead. A detached launch is a handoff, not a completed verification.
- A precise "blocked because X" report is a successful outcome; a guessed implementation is not.
- Audit progress claims against actual tool output before reporting them.

## Chain of Command

- **Implementers / test-runners**: report ONLY to your own squad lead (or the team-lead) via SendMessage. Never message the orchestrator, other squads, or other members directly. If your task is blocked or needs delegation, stop and report to your lead.
- **Squad leads**: you are the only member who messages the orchestrator. Before reporting your squad's conclusion, you MUST wait for your test-runner's PASS/FAIL result — a squad report without test evidence is invalid. Summarize member results; do not forward raw logs.
- **Cross-squad dependency**: if your squad depends on another squad's output, WAIT for that squad lead's explicit SendMessage handing over the interface. Polling is forbidden — do not send repeated status queries; work on non-blocked items or go idle until the handoff arrives.
- Squad leads and members NEVER spawn subagents, teams, or workflows. Needing delegation means: stop and report up the chain.
- Use `message` for direct teammate communication (default); use `broadcast` only for critical team-wide announcements. Never send structured JSON status messages — use TaskUpdate instead. Refer to teammates by NAME, never by UUID.

## Signoff and Task Closure

- Workers never self-complete tasks. When a worker believes its acceptance criteria are met, its report ends with `READY_FOR_SIGNOFF` plus the evidence (artifact path, content markers, commit hashes). The lead verifies and closes the task.
- The final task in the task list is closed only by the user, never by an agent.

> Note: the v1.3.4 `team-implementer` agent variant instructed the implementer to mark its own task completed via TaskUpdate after test-runner confirmation; that self-completion variant is discarded in favour of the `READY_FOR_SIGNOFF` + lead-signoff convention above.

## Member Naming

Every spawned member's `name` MUST carry its role and its model as a suffix: `{role/focus}-{model}` (e.g. `reviewer-security-opus`, `impl-frontend-sonnet`, `test-runner-haiku`; number repeated roles: `impl-1-sonnet`, `impl-2-sonnet`). In squad orchestration, prefix with the squad purpose as well: `{purpose}-{role}-{model}` (e.g. `api-lead-opus`, `api-impl-1-sonnet`, `api-test-haiku`). The suffix is the model actually passed to the spawn call — a name without a model suffix, or with a suffix that differs from the `model` parameter, is an invalid spawn; fix the name before spawning, not after.

## Baton Rotation (mandatory for every worker)

Rotation is mandatory: judgment degrades as a member's context grows.

- **Task cap per member lifetime**: judgment-dense work (debugging, architecture, algorithms, security) = 1–2 tasks; mechanical work (batch edits, applying a known pattern, running commands) = 3–4 tasks. The cap is set by judgment density, not line count. No member carries more than 4 tasks (2 if judgment-dense) in its lifetime.
- On reaching the cap, the member's LAST action is writing a **baton handoff doc** into the working tree (e.g. `{logs-dir}/baton-{k}.md`, or `{logs-dir}/{YYYY-MM-DD}/round-{N}-{squad}-baton-{k}.md` in squad orchestration) containing: the contract's end-state and acceptance criteria **quoted verbatim**, completed tasks + evidence (content markers / hashes / test names), in-progress state with the next concrete action, refuted hypotheses and failure traces (so the successor never retries a dead route), and the red-line list. Then it reports `READY_FOR_HANDOFF` to its lead and stops taking work.
- The lead (or main agent) relays to the orchestrator, which spawns a **fresh** member whose prompt includes the baton doc path and the instruction: "routes listed under failure traces must not be retried."
- **Early-rotation signals** (rotate before the cap): the same error appears a third time, or the member itself reports context pressure. A fresh perspective is the fix — not another retry by the same member. Keeping a degraded member running to save one handoff is how a whole round goes bad.

## Language Policy

All inter-agent communication — task descriptions, SendMessage between agents, TaskUpdate notes, broadcast messages, and all coordination between the main agent, team-lead, and team members — MUST use **English only**. This applies to every phase of team operation.

The main agent (the agent that invoked the command) uses the user's preferred language (as configured in CLAUDE.md) **only** when presenting the final consolidated summary or report directly to the user.
