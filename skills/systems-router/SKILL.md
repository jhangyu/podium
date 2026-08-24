---
name: systems-router
description: Use when the task involves systems programming. Systems programming knowledge index — Go goroutines/channels/sync primitives/worker pools/race conditions, memory-safe RAII/ownership/smart pointers across Rust/C++/C, Rust async/Tokio/async traits/concurrent patterns. Also routes C++ project scaffolding to the native cpp-project skill.
---

# Systems Programming Router

This skill is an index. Identify the matching topic below, then Read the referenced file (path is relative to this SKILL.md's directory) and follow it. Read at most 2 references per task — if none match, say so rather than guessing.

| Topic | Reference | Use when |
|---|---|---|
| goroutines, channels, sync primitives, worker pools | references/go-concurrency-patterns/SKILL.md | Building concurrent Go apps, debugging race conditions |
| RAII, ownership, smart pointers (Rust/C++/C) | references/memory-safety-patterns/SKILL.md | Writing safe systems code, preventing memory bugs |
| Tokio, async traits, Rust concurrency | references/rust-async-patterns/SKILL.md | Building async Rust apps, debugging async code |
| C++ project scaffolding, CMake, GTest, ASAN/TSAN | cpp-project → native skill, invoke directly | Creating a new C++ application/library/monorepo |
