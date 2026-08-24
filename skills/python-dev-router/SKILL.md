---
name: python-dev-router
description: Use when the task involves Python development. Python knowledge index — asyncio, async/await, concurrency, background jobs/task queues, code style/linting/docstrings, pydantic-settings/config, design patterns/SRP/KISS, error handling/exceptions, structured logging/metrics/tracing, packaging/PyPI, cProfile/performance, project structure, retries/backoff/timeouts, context managers/resource cleanup, pytest/fixtures/mocking, type hints/mypy/generics, uv package manager, python-scaffold project scaffolding FastAPI Django CLI library.
---

# Python Development Router

This skill is an index. Identify the matching topic below, then Read the referenced file (path is relative to this SKILL.md's directory) and follow it. Read at most 2 references per task — if none match, say so rather than guessing.

| Topic | Reference | Use when |
|---|---|---|
| asyncio, async/await, concurrency | references/async-python-patterns/SKILL.md | Building async APIs, concurrent systems, I/O-bound apps |
| anti-patterns checklist | references/python-anti-patterns.md | Reviewing code for known bad practices before finalizing |
| task queues, workers, background jobs | references/python-background-jobs/SKILL.md | Async task processing, job queues, decoupling work from requests |
| style, linting, naming, docstrings | references/python-code-style.md | Writing new code, configuring linters, project standards |
| env vars, pydantic-settings, secrets | references/python-configuration/SKILL.md | Externalizing config, environment-specific behavior |
| KISS, SRP, composition, layering | references/python-design-patterns/SKILL.md | Designing a new service, refactoring a God class, choosing abstractions |
| validation, exception hierarchies | references/python-error-handling/SKILL.md | Validation logic, exception strategy, batch failure handling |
| structured logging, metrics, tracing | references/python-observability/SKILL.md | Adding logging, metrics collection, distributed tracing |
| packaging, pyproject.toml, PyPI | references/python-packaging/SKILL.md | Packaging libraries, CLI tools, distributing code |
| cProfile, memory profiling, optimization | references/python-performance-optimization/SKILL.md | Debugging slow code, optimizing bottlenecks |
| module layout, __all__, public API | references/python-project-structure.md | Setting up new projects, organizing modules |
| retries, exponential backoff, timeouts | references/python-resilience/SKILL.md | Retry logic, fault-tolerant services, transient failures |
| context managers, cleanup, streaming | references/python-resource-management/SKILL.md | Managing connections/file handles, streaming responses |
| pytest, fixtures, mocking, TDD | references/python-testing-patterns/SKILL.md | Writing Python tests, setting up test suites |
| type hints, generics, protocols, mypy | references/python-type-safety/SKILL.md | Type annotations, generic classes, mypy/pyright config |
| uv package manager, venvs | references/uv-package-manager/SKILL.md | Setting up projects, dependency management with uv |
| Python project scaffolding (FastAPI, Django, CLI, library) | references/python-scaffold.md | Creating a new Python application with modern tooling |
