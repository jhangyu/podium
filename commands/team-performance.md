---
description: "Multi-agent performance profiling, bottleneck identification, and optimization recommendations with language-specific expert analysis"
argument-hint: "<target path or description> [--lang c|cpp|go|rust|auto] [--focus cpu|memory|io|all] [--profile]"
---

# Team Performance

Orchestrate a performance analysis: a performance-engineer profiles the system, language-specific pro agents review idiomatic optimizations, an architect-reviewer evaluates structural bottlenecks, and a test-runner executes benchmarks to measure actual impact.

## Pre-flight Checks

1. Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
2. Parse `$ARGUMENTS`:
   - `<target>`: path or description of code to profile
   - `--lang`: language-specific expert — `c`, `cpp`, `go`, `rust`, `auto` (auto-detect) — default: `auto`
   - `--focus`: `cpu` | `memory` | `io` | `all` — default: `all`
   - `--profile`: if set, signal test-runner to execute benchmarks before analysis

## Phase 1: Benchmark Baseline (if --profile)

If `--profile` flag is set:
1. Spawn `podium:team-test-runner` immediately
2. Signal it to run existing benchmark/profile commands (detect from package.json, Makefile, Cargo.toml, go test -bench, etc.)
3. Capture baseline metrics: throughput, latency p50/p95/p99, memory usage, CPU time
4. Store baseline for comparison after optimizations

## Phase 2: Multi-Angle Analysis (Parallel)

Spawn 2-3 parallel investigators based on `--lang` and `--focus`:

**Always spawn:**
- `podium:performance-engineer` — focuses on:
  - Database query efficiency (N+1, missing indexes)
  - Caching opportunities and cache invalidation
  - Async/concurrent programming correctness
  - Resource cleanup and connection management
  - Algorithm complexity hotspots

**Always spawn:**
- `podium:architect-reviewer` — focuses on:
  - Architectural bottlenecks (synchronous flows that should be async)
  - Service boundary issues causing chattiness
  - Data flow inefficiencies
  - Missing horizontal scaling opportunities

**If `--lang` is specified or auto-detected:**
- `podium:c-pro` — C-specific: memory pools, SIMD, cache locality, compiler hints
- `podium:cpp-pro` — C++-specific: move semantics misuse, virtual dispatch overhead, template instantiation
- `podium:golang-pro` — Go-specific: goroutine leaks, channel sizing, GC pressure, escape analysis
- `podium:rust-pro` — Rust-specific: allocation patterns, Arc/Mutex contention, async executor misuse

Track: "{completed}/{total} analyses complete"

## Phase 3: Prioritized Optimization Plan

Merge findings from all investigators. Score each optimization:
- **Estimated speedup**: ×1.1 / ×1.5 / ×2 / ×5 / ×10+
- **Implementation difficulty**: Low / Medium / High
- **Risk**: Safe (no behavior change) / Low (minor refactor) / High (architectural change)

Group by category:
```
### Quick Wins (Safe, Low difficulty)
### Significant Gains (Medium difficulty, ×2+ speedup)
### Architectural Changes (High impact, higher risk)
```

Present to user and ask: "Proceed with implementation, or just report?"

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 4: Implementation (if user approves)

1. Use the `TeamCreate` tool with `displayMode: "tmux"` and team name `perf-{timestamp}`, enabling real-time inter-agent communication and visibility
2. Spawn `podium:team-lead` to coordinate
3. Spawn `podium:team-implementer` agents for each approved optimization stream
4. Keep `podium:team-test-runner` active to run benchmarks after each change
5. After each implementer completes:
   - Run benchmarks via `team-test-runner`
   - Compare against baseline
   - Report delta: "Optimization X: {baseline} → {after} ({improvement}%)"
6. Broadcast final delta table to `podium:team-doc-updater`:
   - Update PERFORMANCE.md or equivalent
   - Document what was changed and measured impact

## Phase 5: Report

```
## Performance Report: {target}

### Analysis Summary
Investigators: {list}
Focus areas: {cpu/memory/io/all}

### Findings
{merged findings by severity}

### Optimization Results (if implemented)
| Optimization | Before | After | Improvement |
|---|---|---|---|
| {item} | {metric} | {metric} | {%} |

### Recommendations Not Yet Implemented
{list with priority scores}

### Docs Updated
{from team-doc-updater}
```

## Phase 6: Cleanup

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
