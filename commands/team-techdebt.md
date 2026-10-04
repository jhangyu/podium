---
description: "Multi-agent technical debt inventory, impact scoring, and actionable remediation roadmap"
argument-hint: "<target path or description> [--output roadmap|report|both] [--horizon sprint|quarter|year]"
---

# Team Tech Debt

Orchestrate a comprehensive technical debt analysis.
Parallel agents scan different debt categories, a team-reviewer assesses structural impact, and a legacy-modernizer produces a prioritized remediation roadmap.
A doc-updater captures the findings into persistent documentation.

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Pre-flight Checks

1. Do NOT pre-check the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var;
   if spawning fails with a teams-disabled error, halt and instruct the user to set it to 1.
   Spawn recipe for EVERY Agent call (per `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md`):
   `name` (session-unique), `team_name` (team label, e.g. `techdebt-{timestamp}`), `subagent_type`, explicit `model`;
   the prompt includes the `ROLE: WORKER` no-spawn line and "Report via SendMessage to `team-lead`; if unreachable, send to `main`."
   Always include `team_name` (legacy gates require it; harmless in IMPLICIT).
2. Parse `$ARGUMENTS`:
   - `<target>`: path or description of codebase scope
   - `--output`: `roadmap` (actionable items only) | `report` (full inventory) | `both` — default: `both`
   - `--horizon`: planning horizon — `sprint` (1-2 weeks) | `quarter` (3 months) | `year` — default: `quarter`

## Phase 1: Debt Discovery (Parallel)

Spawn 3 parallel investigators:

1. **`podium:team-reviewer`** (dimension: `techdebt`, whole-tree audit mode) —
   applies `${CLAUDE_PLUGIN_ROOT}/protocols/review.md` §L1 Structural questions, §L2 Policy Gate, §L3 Hygiene, and §Periodic audit A1–A3.
   Every finding has Origin = pre-existing.
2. **`podium:team-reviewer`** (dimension: `architecture`) — per `${CLAUDE_PLUGIN_ROOT}/protocols/review.md` §Dimensions.
3. **`podium:legacy-modernizer`** (dimension: technology-debt) — applies `${CLAUDE_PLUGIN_ROOT}/protocols/review.md` §Periodic audit A4 only.

Track progress: "{completed}/3 investigations complete"

## Phase 2: Impact Scoring

For each debt item collected, score:
- **Impact** (1-5): How much does this slow development / increase bug risk?
- **Effort** (1-5): How much work to fix?
- **Severity**: per `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Severity`.

Compute priority score: `Impact / Effort × multiplier(severity)`; multiplier: Critical=4, High=2, Medium=1.5, Low=1.

## Phase 3: Remediation Planning

Spawn `podium:legacy-modernizer` to create a prioritized remediation plan:
- Group items by horizon (`--horizon`); per item: exact change, files affected, estimated effort
- Flag dependencies between items (fix X before Y); identify quick wins (Impact ≥ 3, Effort ≤ 2)

## Phase 4: Documentation

Broadcast to `team-doc-updater` with:
- Full debt inventory (Phase 1), priority scores (Phase 2), remediation roadmap (Phase 3)
- Request to create/update `TECH_DEBT.md` per `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Debt register`; update CHANGELOG or architecture docs if relevant

`team-doc-updater` works in parallel while Phase 5 proceeds.

## Phase 5: Report

Present consolidated report:

```
## Tech Debt Report: {target}

### Summary
Total items: {N} | Critical: {N} | High: {N} | Medium: {N} | Low: {N}
Estimated total remediation effort: {N} days
Hotspot counts (A2): absolute {N} | delta {+/-N} | size {N}

### Quick Wins (do this sprint)
1. {item} — Impact: {score}, Effort: {score} — {files}
...

### This Quarter
1. {item} — Impact: {score}, Effort: {score} — {files}
...

### Backlog (longer term)
1. {item} — ...
### Docs Updated
{from team-doc-updater}
```

## Phase 6: Cleanup

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
