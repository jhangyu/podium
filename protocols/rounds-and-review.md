What a round is, when it may close, and the once-per-round review cadence with its bounded fix cycles.

Referenced by: `podium:team-spawn`, `podium:team-fable`.

## Round Definition

A **round** = one batch of tasks dispatched together (in squad orchestration, one milestone). Define each round's milestone with **mechanically checkable acceptance criteria** (named tests pass, file exists with section X — never "works well").

## Round-End Condition (all three, mechanically checked)

1. The milestone's acceptance criteria pass.
2. Every task assigned this round is `completed`.
3. The round reviewer's verdict is a confirmation with no open issues (verdict formats are defined in `${CLAUDE_PLUGIN_ROOT}/protocols/verification.md`).

## Review Cadence

Review happens once per round, not per member or per deliverable. When every task in the round is complete (with test-runner PASS evidence where a test-runner exists), spawn a single `podium:team-reviewer` named `round-{N}-reviewer-{model}` scoped to the round's combined diff — across all squad worktrees when squads are in use. Its verdict goes to the main agent (or team-lead / orchestrator) and to no one else.

- In squad orchestration the round reviewer is `opus` (`round-{N}-reviewer-opus`) — the model floor is mandatory, not a default.
- The reviewer works **read-only in the existing worktrees** — no new worktree, no file ownership list.
- The reviewer's task prompt embeds the verification protocol and the git red lines (`${CLAUDE_PLUGIN_ROOT}/protocols/file-ownership.md`) verbatim, not the communication protocol.
- Issues route back to the original worker (or originating squad lead) for fixes, then re-review — **maximum 2 review→fix cycles per round**. Still failing after 2 cycles → stop, report the failure trace to the user, and wait for direction.
- Presets whose deliverable IS review (`review`, `security`, `techdebt`) are exempt from the round reviewer.

## Orchestrator Duties During a Round

1. The orchestrator receives squad-lead summaries only; it does not micro-manage members.
2. **Spot-check**: the orchestrator personally verifies 1–2 key claims per squad against evidence, per the evidence discipline in `${CLAUDE_PLUGIN_ROOT}/protocols/verification.md`.
3. **Stall watchdog**: an idle notification carrying NO outbound `[to <member>]` summary, from a member that was just sent a command, means that member ended its turn without delivering — nudge it once immediately (idle wake-ups are messages, not polling). If the SAME member or relay hop drops its results twice, BYPASS it: the lead or main agent runs the verification commands itself (the lead is independent of the implementers, so verifier-independence holds) and the dropped hop's member is shut down or re-scoped. Bypass is bounded recovery, not the default flow.
4. **Escalation**: if the same subtask fails twice (same root cause), STOP retrying. The squad lead escalates to the orchestrator with the full failure trace (attempts, error output, current state). The orchestrator decides: re-scope, upgrade model, or ask the user.

## Closing a Round

1. Verify the round-end condition (all three items above).
2. Each squad lead confirms next-round direction with the orchestrator, THEN writes a handoff doc: `{logs-dir}/{YYYY-MM-DD}/round-{N}-{squad}-handoff.md` containing:
   - Completed work + evidence (commit hashes, passing test names)
   - Known limitations (explicitly listed — hiding them voids the round)
   - Interface contracts other squads or the next round depend on
   - Next-round notes for the incoming squad lead
3. Merge and re-verify per `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`, then clean up the round's worktrees in the same round.
4. Report the round's results to the user: what each squad shipped, review outcome, open questions. **If any ambiguity requires a user decision, stop here and wait.**
5. Otherwise, shut down ALL round members per `${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md`, and verify no residue remains.
6. Next round: spawn fresh squads (fresh context by design). Their prompts MUST include the handoff doc paths from step 2 — that is how knowledge crosses the round boundary.

## Bounds

Review loops, retries, and rounds are bounded (2 cycles / 2 attempts); when a bound is hit, escalate — never silently keep burning.
