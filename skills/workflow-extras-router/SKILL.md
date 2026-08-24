---
name: workflow-extras-router
description: Use when the task matches one of these disabled-plugin workflows. Extras index for disabled plugins — AngularJS/Angular, database/ORM migration, major dependency upgrades, React hooks modernization, strangler-fig legacy modernization, multi-reviewer/parallel-debugging/parallel-feature/task-coordination/team-communication/team-composition patterns for agent teams, TDD red/green/refactor/cycle, code explanation, doc generation, AI-assisted debugging, dependency/tech-debt audits, full multi-dimensional code review, git workflow with quality gates, PR enhancement, team onboarding.
---

# Workflow Extras Router

This skill is an index. Identify the matching topic below, then Read the referenced file (path is relative to this SKILL.md's directory) and follow it. Read at most 2 references per task — if none match, say so rather than guessing.

| Topic | Reference | Use when |
|---|---|---|
| AngularJS to Angular migration | references/angular-migration/SKILL.md | Upgrading AngularJS apps, hybrid mode, component conversion |
| database/ORM schema migration | references/database-migration/SKILL.md | Zero-downtime schema/data migrations across ORMs |
| major dependency version upgrades | references/dependency-upgrade.md | Compatibility analysis, staged rollout, breaking changes |
| React class-to-hooks modernization | references/react-modernization/SKILL.md | Upgrading React versions, hooks migration, concurrent features |
| migration plan/script generation | references/code-migrate.md | Transitioning codebases between frameworks/languages/platforms |
| dependency upgrade execution strategy | references/deps-upgrade.md | Planning safe incremental dependency upgrades |
| strangler-fig legacy modernization | references/legacy-modernize.md | Gradual legacy component replacement |
| multi-reviewer coordination, finding dedup | references/multi-reviewer-patterns/SKILL.md | Organizing parallel multi-dimension code reviews |
| competing-hypothesis parallel debugging | references/parallel-debugging/SKILL.md | Debugging with multiple potential root causes |
| parallel feature dev, file ownership | references/parallel-feature-development/SKILL.md | Decomposing a feature into parallel agent work streams |
| task decomposition, dependency graphs | references/task-coordination-strategies/SKILL.md | Breaking down work, balancing multi-agent workload |
| team messaging protocols, shutdown | references/team-communication-protocols/SKILL.md | Establishing comms norms, plan approval, graceful shutdown |
| team sizing, preset composition | references/team-composition-patterns/SKILL.md | Choosing team size/type and subagent_type per role |
| TDD full cycle orchestration | references/tdd-cycle.md | Running strict red-green-refactor discipline end to end |
| TDD green phase (minimal passing code) | references/tdd-green.md | Making failing tests pass with minimal implementation |
| TDD red phase (failing tests) | references/tdd-red.md | Writing comprehensive failing tests first |
| TDD-safe refactoring | references/tdd-refactor.md | Refactoring with a green test suite as safety net |
| code explanation for onboarding | references/code-explain.md | Explaining complex code/algorithms/architecture to devs |
| automated documentation generation | references/doc-generate.md | Generating API docs, architecture diagrams, user guides |
| AI-assisted root cause debugging | references/smart-debug.md | Modern debugging tools, observability, root cause analysis |
| dependency vulnerability/license audit | references/deps-audit.md | Scanning for vulnerable/outdated/license-conflicting deps |
| technical debt inventory and scoring | references/tech-debt.md | Inventorying debt, scoring impact, remediation planning |
| multi-dimensional review orchestration | references/full-review.md | Architecture/security/performance/testing review in one pass |
| PR description and review-facilitation | references/pr-enhance.md | Improving PR descriptions, test coverage notes, reviewability |
| git workflow with quality gates | references/git-workflow.md | Code review through PR creation with gated checks |
| new-hire onboarding planning | references/onboard.md | 90-day onboarding plans, technical/cultural integration |
| test suite generation | references/test-generate.md | Generating comprehensive test suites for existing code |
| mock API server/response generation | references/api-mock.md | Testing against mocked APIs without live dependencies |
| error message/stack trace analysis | references/error-analysis.md | Diagnosing errors from messages and stack traces |
| error origin tracing through call stack | references/error-trace.md | Tracing where an error originated through the call chain |
| distributed request tracing for bugs | references/debug-trace.md | Tracing requests across services to find distributed bugs |
| multi-agent issue resolution | references/smart-fix.md | Diagnosing, fixing, and verifying an issue end to end |
| end-to-end performance optimization | references/performance-optimization.md | Profiling and optimizing full application performance |
| observability stack setup | references/monitor-setup.md | Setting up monitoring stack and dashboards |
| SQL schema migration planning | references/sql-migrations.md | Planning and generating safe SQL schema migrations |
| database migration observability | references/migration-observability.md | Instrumenting and monitoring in-flight DB migrations |
| deployment config validation | references/config-validate.md | Validating deployment configs before rollout |
| CI/CD workflow automation | references/workflow-automate.md | Automating CI/CD pipelines |
| data engineering pipeline design | references/data-pipeline.md | Designing and building data pipelines |
| data-driven feature with A/B testing | references/data-driven-feature.md | 16-step orchestrator for data-driven feature development |
| full-stack feature orchestration | references/full-stack-feature.md | Multi-agent orchestrator from database to deployment |
| cross-platform feature build | references/multi-platform.md | Orchestrating a feature build across web/iOS/Android/desktop |

Skipped as duplicate: git-pr-workflows/commands/pr-enhance.md (byte-identical to comprehensive-review's, kept once above).
