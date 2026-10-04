---
description: "Launch a multi-reviewer parallel code review with specialized review dimensions and automatic documentation of findings"
argument-hint: "<target> [--reviewers security,performance,architecture,testing,accessibility,techdebt] [--base-branch main] [--doc]"
---

# team-review

Run a parallel code review with each reviewer specialized in a distinct dimension, then consolidate findings and optionally document them.

## Phase 1: Target Resolution

Determine the review scope from the `<target>` argument:
- **File or directory path**: read the relevant files directly
- **Git diff**: collect diff against `--base-branch` (default: `main`)
- **PR number or URL**: fetch PR diff content

Gather the full diff or file content. Display a scope summary to the user:
- Files in scope
- Total lines changed (if diff)
- Review dimensions that will be applied

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 2: Team Spawn

Generate a team name: `review-{timestamp}`.

Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY: `TeamCreate` with `displayMode: "tmux"`; IMPLICIT: skip creation). Spawn recipe for EVERY Agent call: `name` (session-unique), `team_name` (team label), `subagent_type`, explicit `model`; the prompt includes the `ROLE: WORKER` no-spawn line and "Report via SendMessage to `team-lead`; if unreachable, send to `main`." Always include `team_name` (legacy gates require it; harmless in IMPLICIT). Then use TaskCreate per reviewer.

Default dimensions and agent mapping:
- `security` → `podium:team-reviewer` with security focus
- `performance` → `podium:team-reviewer` with performance focus
- `architecture` → `podium:team-reviewer` with architecture focus
- `testing` → `podium:team-reviewer` with testing focus
- `accessibility` → `podium:team-reviewer` with accessibility focus
- `techdebt` → `podium:team-reviewer` with structural technical-debt focus

All six dimensions above are the DEFAULT set — `techdebt` runs whenever `--reviewers` is omitted. If `--reviewers` is specified, spawn only the listed dimensions (the only way to exclude techdebt).

Special dimension note: if `refactor` is included in `--reviewers`, spawn `podium:architect-reviewer` instead of `team-reviewer` for that slot.

Always spawn ONE `podium:team-doc-updater`. This agent is active regardless of whether `--doc` is explicitly set. The `--doc` flag only affects whether documentation is written to a persistent file (REVIEW_FINDINGS.md) or surfaced inline in the report only.

Each reviewer prompt MUST embed the verification protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/verification.md and apply it — it owns the adversarial framing, the self-produced-evidence rule, the negative-space question, the verdict format, and reviewer independence.

Each reviewer task must include:
- The full diff or file content
- Their assigned dimension and focus criteria
- Output format: findings list with `file:line`, severity (Critical/High/Medium/Low), description, and suggested fix

## Phase 3: Monitor and Collect

Use TaskList to track progress of all reviewer tasks.
Wait for all reviewers to complete.
Collect all findings reports.

## Phase 4: Consolidation

Deduplicate findings:
- Group by `file:line` reference
- If multiple reviewers flag the same location: merge descriptions, use the **higher** severity of the pair
- Note which dimensions flagged each finding (cross-reference tag)

Organize findings into severity buckets:
1. Critical
2. High
3. Medium
4. Low

Within each bucket, sort by file path then line number.

Identify cross-dimension findings (same issue caught by multiple reviewers) and mark them with a `[multi]` tag.

Cross-layer adjudication: when a structural (L1) techdebt finding exists, mark policy/hygiene (L2/L3) findings in the same scope as `deferred` in the consolidated report — structure first, polish later.

## Phase 5: Documentation

Broadcast to `team-doc-updater` with the consolidated findings:
- Full structured findings list
- Severity summary counts
- Scope metadata (target, base-branch, timestamp)

If `--doc` flag is set (or always by default), request `team-doc-updater` to write or update `REVIEW_FINDINGS.md` in the project root with the full report.

This phase runs in parallel with Phase 6 — do not wait for doc completion before presenting the report.

## Phase 6: Report and Cleanup

Present the consolidated review report:

```
## Code Review: {target}
Base: {base-branch} | Reviewers: {dimensions} | {timestamp}

### Summary
Critical: {N} | High: {N} | Medium: {N} | Low: {N}

### Critical Findings
{file:line} [{dimensions}] — {description}
  Suggested fix: {fix}

### High Findings
...

### Medium Findings
...

### Low Findings
...

### Docs Updated
{REVIEW_FINDINGS.md or "inline only" if --doc not set}
```

Wait for `team-doc-updater` to confirm completion (if writing to file).

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
