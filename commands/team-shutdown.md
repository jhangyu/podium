---
description: "Gracefully shut down an agent team, flush documentation, collect final results, and clean up resources"
argument-hint: "[team-name] [--force] [--keep-tasks] [--skip-doc-flush]"
---

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Shutdown Sequence

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it. The four phases below are that protocol's sequence — the protocol owns every rule, ordering, argument behaviour, and output format they use.

## Phase 1: Pre-Shutdown

Parse args, read the team config, and check for in-progress tasks before doing anything — per the shutdown protocol.

---

## Phase 2: Documentation Flush

Flush pending documentation through `team-doc-updater` before members go down — per the shutdown protocol.

---

## Phase 3: Graceful Shutdown

Send shutdown requests to members in the protocol's order — per the shutdown protocol.

---

## Phase 4: Cleanup

Display the shutdown summary, remove the team, and run the residue checks — per the shutdown protocol.
