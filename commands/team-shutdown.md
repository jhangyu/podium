---
description: "Gracefully shut down an agent team, flush documentation, collect final results, and clean up resources"
argument-hint: "[team-name] [--force] [--keep-tasks] [--skip-doc-flush]"
---

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Shutdown Sequence

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it end-to-end. The protocol owns the full phase sequence (pane-mapping snapshot through final verification), every rule, ordering, gating condition, argument behaviour, output format, and the `${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py` helper it uses.
