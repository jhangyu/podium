---
description: "Parallel code refactoring using code-reviewer analysis + legacy-modernizer planning + implementer execution with test verification"
argument-hint: "<target path or description> [--scope files|module|project] [--strategy safe|aggressive] [--lang c|cpp|go|rust]"
---

# Team Refactor

Orchestrate a parallel refactoring workflow: a code-reviewer identifies issues, a legacy-modernizer creates the remediation plan, implementers execute in parallel with file ownership, and a test-runner verifies nothing broke.

## Pre-flight Checks

1. Do NOT pre-check the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var; if spawning fails with a teams-disabled error, halt and instruct the user to set it to 1.
2. Parse `$ARGUMENTS`:
   - `<target>`: file path, directory, or module description
   - `--scope`: `files` (specific files), `module` (package/module), `project` (entire codebase) — default: `module`
   - `--strategy`: `safe` (rename, extract, dedup only) | `aggressive` (architectural changes, interface redesign) — default: `safe`
   - `--lang`: hint for language-specific pro agent (`c`, `cpp`, `go`, `rust`). If omitted, auto-detect.

## Phase 1: Analysis

Team label: generate `refactor-{timestamp}` now; it is the `team_name` for every Agent call from here on (all phases). LEGACY builds: run TeamCreate with this label now, before the first spawn.

1. Spawn `podium:team-reviewer` with dimension `architecture` to scan the target for:
   - Code smells (long methods, duplication, god classes, magic numbers)
   - SOLID violations
   - Dead code and unused exports
   - Naming inconsistencies
2. Spawn `podium:code-reviewer` in parallel to scan for:
   - Performance anti-patterns
   - Error handling gaps
   - Missing type safety
3. Collect findings. Present summary to user:
   ```
   ## Refactor Analysis: {target}
   Found {N} issues: {critical} critical, {high} high, {medium} medium
   ```

## Phase 2: Modernization Plan

1. Spawn `podium:legacy-modernizer` with:
   - The full findings report from Phase 1
   - The `--strategy` flag
   - A request to produce a prioritized refactoring plan with estimated effort per item
2. If `--lang` is specified (or auto-detected as c/cpp/go/rust), ALSO spawn the corresponding `podium:{lang}-pro` in parallel to review language-specific patterns and add language-idiomatic suggestions.
3. Merge plans. Present to user and wait for approval:
   ```
   ## Refactoring Plan

   ### Immediate (High Impact, Low Effort)
   1. {item} — {files affected} — estimated: {effort}
   ...

   ### Structural (High Impact, Higher Effort)
   1. {item} — {files affected} — estimated: {effort}
   ...
   ```
   Ask user: "Proceed with full plan, or select specific items?"

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 3: Team Spawn

1. Team mode per `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY team already created in Phase 1). Spawn recipe for EVERY Agent call in every phase, including the Phase 1-2 analysts: `name` (session-unique), `team_name` (team label), `subagent_type`, explicit `model`; the prompt includes the `ROLE: WORKER` no-spawn line and "Report via SendMessage to `team-lead`; if unreachable, send to `main`." Always include `team_name` (legacy gates require it; harmless in IMPLICIT); reuse the Phase 1 team label
2. Decompose approved plan into work streams with exclusive file ownership (no overlaps)
3. Spawn `podium:team-lead` to coordinate
4. For each work stream, spawn `podium:team-implementer`:
   - Assign owned files
   - Include the specific refactoring items for that file set
   - Include the interface contracts if streams share boundaries
5. Spawn ONE `podium:team-test-runner` for the team
6. Spawn ONE `podium:team-doc-updater` for the team

## Phase 4: Execute Refactoring

1. Monitor `TaskList` for implementer progress
2. As each implementer completes a work stream:
   - Signal `team-test-runner` with the relevant test/build commands for that stream
   - `team-test-runner` reports PASS/FAIL
   - If FAIL: create a fix task, assign back to the implementer; do NOT move on
   - If PASS: mark stream complete, proceed
3. After ALL streams pass: broadcast checkpoint to `team-doc-updater` with:
   - List of refactored files
   - Summary of structural changes
   - Which public APIs changed (if any)

## Phase 5: Final Verification

1. Signal `team-test-runner` to run the full test suite (not just per-stream tests)
2. If any tests fail: assign targeted fixes to the responsible implementer
3. Wait for all tests to pass

## Phase 6: Report and Cleanup

1. Present refactor summary:
   ```
   ## Refactor Complete: {target}

   Files changed: {count}
   Issues resolved: {count}/{total}
   Tests: {pass}/{total}

   ### Changes Made
   {bullet list of major changes}

   ### Docs Updated
   {list from team-doc-updater}
   ```
2. Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
