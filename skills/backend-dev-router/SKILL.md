---
name: backend-dev-router
description: Use when the task involves backend architecture. Backend architecture knowledge index — REST/GraphQL API design, Clean/Hexagonal Architecture, DDD, bounded contexts, CQRS, event sourcing, event store design, microservices, service boundaries, event-driven communication, read models/projections/materialized views, saga pattern, distributed transactions, compensating actions, Temporal workflows, workflow testing, feature-development end-to-end orchestration.
---

# Backend Development Router

This skill is an index. Identify the matching topic below, then Read the referenced file (path is relative to this SKILL.md's directory) and follow it. Read at most 2 references per task — if none match, say so rather than guessing.

| Topic | Reference | Use when |
|---|---|---|
| REST/GraphQL API design standards | references/api-design-principles/SKILL.md | Designing new APIs, reviewing specs, API standards |
| Clean/Hexagonal Architecture, DDD, bounded contexts | references/architecture-patterns/SKILL.md | Designing microservice architecture, refactoring a monolith |
| CQRS, read/write model separation | references/cqrs-implementation/SKILL.md | Separating read/write models, event-sourced systems |
| event store design and persistence | references/event-store-design/SKILL.md | Building event sourcing infra, choosing event store tech |
| service boundaries, event-driven microservices | references/microservices-patterns/SKILL.md | Building distributed systems, decomposing monoliths |
| read models, materialized views | references/projection-patterns/SKILL.md | Implementing CQRS read sides, optimizing query performance |
| saga pattern, distributed transactions | references/saga-orchestration/SKILL.md | Cross-service transactions, compensating actions, rollback flows |
| Temporal workflow testing | references/temporal-python-testing/SKILL.md | Testing Temporal workflows, replay/time-skip testing |
| durable workflows, workflow vs activity design | references/workflow-orchestration-patterns/SKILL.md | Long-running processes, distributed transactions, orchestration |
| end-to-end feature development orchestration | references/feature-development.md | Orchestrating requirements → architecture → implementation → testing → deployment |
