---
description: "Develop features in parallel with multiple agents using file ownership boundaries, automated test verification, and doc tracking"
argument-hint: "<feature-description> [--team-size N] [--branch feature/name] [--plan-first]"
---

# team-feature

Develop a feature using parallel implementation streams, automated test verification after each stream, and continuous documentation tracking.

## Phase 1: Analysis

Explore the codebase to understand:
- Existing file structure and conventions
- Related modules, APIs, and integration points
- Test framework and build commands in use
- Current documentation locations

Identify all files that will need to be created or modified.

## Phase 2: Decomposition

Split the feature into independent implementation streams. Each stream must have:
- Exclusive file ownership (no two streams own the same file)
- Clear acceptance criteria
- Explicit integration points with other streams

Default team size is 2 implementer streams. Use `--team-size N` to override.

If `--plan-first` is set: present the full decomposition plan (streams, owned files, acceptance criteria, dependency order) and wait for explicit user approval before proceeding. Do not spawn any agents until approved.

If `--branch` is set: note the target branch for all implementation work.

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 3: Team Spawn

Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY: `TeamCreate` with `displayMode: "tmux"`; IMPLICIT: skip creation). Spawn recipe for EVERY Agent call: `name` (session-unique), `team_name` (team label), `subagent_type`, explicit `model`; the prompt includes the `ROLE: WORKER` no-spawn line and "Report via SendMessage to `team-lead`; if unreachable, send to `main`." Always include `team_name` (legacy gates require it; harmless in IMPLICIT). Derive the team name from the feature description or `--branch` value.

Spawn the following agents (all using subagent_type prefix `podium:`):
- ONE `podium:team-lead` — coordinates streams, owns integration files
- N `podium:team-implementer` agents — one per stream
- ONE `podium:team-test-runner` — runs test/build commands after each stream completes, reports PASS/FAIL
- ONE `podium:team-doc-updater` — updates docs at leader checkpoints with change summaries

## Phase 4: Task Creation

Use TaskCreate for each implementation stream with:
- Owned file list (exclusive boundaries)
- Acceptance criteria
- Integration contracts with adjacent streams
- `blockedBy` relationships to enforce dependency order (streams that depend on another stream's output are blocked until that stream passes tests)

Create a task for team-test-runner: stand by to receive test/build commands per stream.
Create a task for team-doc-updater: stand by to receive change summaries at leader checkpoints.

## Phase 5: Monitor and Coordinate

As each implementation stream completes:

1. Signal `team-test-runner` with the specific test/build commands for that stream's owned files.
2. Wait for team-test-runner to report PASS or FAIL.

**If FAIL:**
- Create a fix task and assign it back to the stream's `team-implementer`.
- Do NOT unblock any dependent streams.
- Re-signal `team-test-runner` once the implementer reports the fix is ready.
- Repeat until PASS.

**If PASS:**
- Unblock dependent streams that were waiting on this stream.
- Continue monitoring remaining streams.

At each leader checkpoint (defined as: after each PASS, before unblocking dependents), broadcast to `team-doc-updater` with:
- Which stream completed
- Files modified
- New functions/APIs introduced
- Interface changes

## Phase 6: Integration Verification

After all implementation streams have individually passed their tests:

1. Signal `team-test-runner` to run the full integration test suite.
2. Wait for PASS or FAIL.

**If FAIL:**
- Identify which integration boundary failed from the test output.
- Assign targeted fix tasks to the relevant `team-implementer`(s).
- Re-run integration suite after fixes.
- Repeat until PASS.

After PASS: Spawn ONE `podium:team-reviewer` per `${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md`
(review cadence and the 2-cycle bound; dimensions `techdebt, architecture` plus any the diff needs) scoped to the combined diff.
Route findings back to the responsible implementer, then re-review.

## Phase 7: Doc Update

After all tests pass (per-stream and integration):

Broadcast to `team-doc-updater` with the complete change summary:
- Full list of modified files
- All new public APIs and their signatures
- Interface changes and migration notes
- Any configuration changes

Wait for `team-doc-updater` to confirm completion before proceeding.

## Phase 8: Cleanup

Present the feature summary:

```
Feature: {feature-description}
Branch: {branch if specified}

Implementation Streams: {N}
Files Changed: {list}
Test Results: All streams PASS | Integration PASS

Docs Updated:
  {list from team-doc-updater}

Agents: {count} spawned
```

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
