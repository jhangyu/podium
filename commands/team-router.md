---
description: "Run a consolidated command from disabled plugins: /team-router <name> [args] — scaffolds, security scans, migrations."
argument-hint: "<command-name> [arguments...]"
---

# /team-router — Consolidated Command Dispatcher

Parse `$ARGUMENTS`: the **first token** is the command name; everything after it is the **payload**.

Look up the command name in the index below. If found, Read the referenced file (path is relative to this plugin's root directory — go up one level from this `commands/` folder) and execute its full instructions, treating the payload as that command's `$ARGUMENTS`.

If the name is missing or not in the index, print the available commands table below and stop. Do not guess or suggest alternatives.

## Command Index

| Name | Reference path | Source plugin | Summary |
|---|---|---|---|
| python-scaffold | ${CLAUDE_PLUGIN_ROOT}/references/routed/python-scaffold.md | python-development | Scaffold a new Python project with best-practice layout |
| typescript-scaffold | ${CLAUDE_PLUGIN_ROOT}/references/routed/typescript-scaffold.md | javascript-typescript | Scaffold a new TypeScript/Node.js project |
| component-scaffold | ${CLAUDE_PLUGIN_ROOT}/references/routed/component-scaffold.md | frontend-mobile-development | Scaffold frontend UI component with tests and styles |
| feature-development | ${CLAUDE_PLUGIN_ROOT}/references/routed/feature-development.md | backend-development | End-to-end feature development workflow |
| full-stack-feature | ${CLAUDE_PLUGIN_ROOT}/references/routed/full-stack-feature.md | full-stack-orchestration | Multi-agent full-stack feature orchestrator (db to deploy) |
| multi-platform | ${CLAUDE_PLUGIN_ROOT}/references/routed/multi-platform.md | multi-platform-apps | Orchestrate feature build across web/iOS/Android/desktop |
| data-driven-feature | ${CLAUDE_PLUGIN_ROOT}/references/routed/data-driven-feature.md | data-engineering | 16-step orchestrator: data-driven feature dev with A/B testing |
| tdd-red | ${CLAUDE_PLUGIN_ROOT}/references/routed/tdd-red.md | tdd-workflows | Write failing tests for TDD red phase |
| tdd-green | ${CLAUDE_PLUGIN_ROOT}/references/routed/tdd-green.md | tdd-workflows | Write minimal code to pass failing tests |
| tdd-refactor | ${CLAUDE_PLUGIN_ROOT}/references/routed/tdd-refactor.md | tdd-workflows | Refactor code safely while keeping tests green |
| test-generate | ${CLAUDE_PLUGIN_ROOT}/references/routed/test-generate.md | unit-testing | Generate comprehensive test suites for code |
| api-mock | ${CLAUDE_PLUGIN_ROOT}/references/routed/api-mock.md | api-testing-observability | Generate mock API servers/responses for testing |
| error-analysis | ${CLAUDE_PLUGIN_ROOT}/references/routed/error-analysis.md | error-diagnostics | Analyze error messages and stack traces |
| error-trace | ${CLAUDE_PLUGIN_ROOT}/references/routed/error-trace.md | error-diagnostics | Trace error origins through call stack |
| smart-debug | ${CLAUDE_PLUGIN_ROOT}/references/routed/smart-debug.md | error-diagnostics | AI-assisted debugging from error to root cause |
| debug-trace | ${CLAUDE_PLUGIN_ROOT}/references/routed/debug-trace.md | distributed-debugging | Trace distributed system requests to find bugs |
| smart-fix | ${CLAUDE_PLUGIN_ROOT}/references/routed/smart-fix.md | incident-response | Multi-agent issue resolution: diagnose, fix, verify |
| full-review | ${CLAUDE_PLUGIN_ROOT}/references/routed/full-review.md | comprehensive-review | Multi-phase orchestrated comprehensive code review |
| tech-debt | ${CLAUDE_PLUGIN_ROOT}/references/routed/tech-debt.md | codebase-cleanup | Inventory and prioritize technical debt |
| deps-audit | ${CLAUDE_PLUGIN_ROOT}/references/routed/deps-audit.md | codebase-cleanup | Audit dependencies for vulnerabilities/staleness |
| performance-optimization | ${CLAUDE_PLUGIN_ROOT}/references/routed/performance-optimization.md | application-performance | End-to-end app performance profiling and optimization |
| doc-generate | ${CLAUDE_PLUGIN_ROOT}/references/routed/doc-generate.md | code-documentation | Auto-generate API/architecture/code/user docs from codebase |
| code-explain | ${CLAUDE_PLUGIN_ROOT}/references/routed/code-explain.md | code-documentation | Explain complex code via diagrams, step-by-step breakdowns |
| monitor-setup | ${CLAUDE_PLUGIN_ROOT}/references/routed/monitor-setup.md | observability-monitoring | Set up observability monitoring stack and dashboards |
| sql-migrations | ${CLAUDE_PLUGIN_ROOT}/references/routed/sql-migrations.md | database-migrations | Plan and generate safe SQL schema migrations |
| migration-observability | ${CLAUDE_PLUGIN_ROOT}/references/routed/migration-observability.md | database-migrations | Instrument and monitor database migrations in flight |
| config-validate | ${CLAUDE_PLUGIN_ROOT}/references/routed/config-validate.md | deployment-validation | Validate deployment configs before rollout |
| workflow-automate | ${CLAUDE_PLUGIN_ROOT}/references/routed/workflow-automate.md | cicd-automation | Automate CI/CD workflow pipelines |
| data-pipeline | ${CLAUDE_PLUGIN_ROOT}/references/routed/data-pipeline.md | data-engineering | Design and build data engineering pipelines |
| security-sast | ${CLAUDE_PLUGIN_ROOT}/references/routed/security-sast.md | security-scanning | Static application security testing |
| security-hardening | ${CLAUDE_PLUGIN_ROOT}/references/routed/security-hardening.md | security-scanning | Defense-in-depth security hardening |
| security-dependencies | ${CLAUDE_PLUGIN_ROOT}/references/routed/security-dependencies.md | security-scanning | Dependency vulnerability scanning |
| xss-scan | ${CLAUDE_PLUGIN_ROOT}/references/routed/xss-scan.md | frontend-mobile-security | Scan frontend/mobile code for XSS vulnerabilities |
| compliance-check | ${CLAUDE_PLUGIN_ROOT}/references/routed/compliance-check.md | security-compliance | Check codebase against compliance frameworks (GDPR/SOC2 etc) |
| code-migrate | ${CLAUDE_PLUGIN_ROOT}/references/routed/code-migrate.md | framework-migration | Framework/language migration plans and scripts |
| deps-upgrade | ${CLAUDE_PLUGIN_ROOT}/references/routed/deps-upgrade.md | framework-migration | Safe incremental dependency upgrades |
| legacy-modernize | ${CLAUDE_PLUGIN_ROOT}/references/routed/legacy-modernize.md | framework-migration | Strangler-fig legacy system modernization |

## Argument Mapping

The payload (all tokens after the command name) becomes the target command's `$ARGUMENTS` verbatim. Examples:

- `/team-router python-scaffold my-api --framework fastapi` reads `python-scaffold.md` and executes with `$ARGUMENTS = "my-api --framework fastapi"`
- `/team-router security-sast ./src` reads `security-sast.md` and executes with `$ARGUMENTS = "./src"`
- `/team-router` (empty) prints the command index above
