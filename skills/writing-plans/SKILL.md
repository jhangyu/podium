---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for our codebase. The plan is written in two stages: first a complete skeleton (architecture, interfaces, acceptance criteria for every task), then bite-sized implementation steps with complete code, expanded against the frozen skeleton. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Delegated Authoring

The main conversation (orchestrator) does NOT write the plan itself — plan authoring consumes too much context. Instead:

1. **REQUIRED SUB-SKILL:** Use `podium:team-spawn` to create a team (TeamCreate).
2. Use `podium:team-roster` to pick ONE implementer identity suited to the project's domain (backend, frontend, systems, etc.).
3. Spawn that member with **model: opus**. Its task: read the spec, follow this skill's rules (Two-Stage Writing Process below), write the plan to the plan file section by section — never in a single write (see Incremental Writing below), run the Self-Review, then report `READY_FOR_SIGNOFF` with only: plan file path, task list summary (one line per task), and self-review results. It must NOT paste the plan body back.
4. The authoring member is a worker: it may not spawn subagents, teams, or workflows. Both stages are done serially by this one member.
5. On receipt, the main conversation spot-checks 1–2 tasks in the plan file (interfaces consistent, code steps complete, acceptance criteria mechanically checkable) before sign-off. Sign-off gates execution handoff.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## Two-Stage Writing Process

Write the plan in this order — never interleave the stages:

**Stage 1 — Skeleton (all tasks, no code):** Write the Plan Document Header, then for EVERY task write only the spec block: Files / Interfaces / Behavior / Constraints / Acceptance criteria. Finish the skeleton for all tasks before writing any code. This freezes interface names, signatures, and types across tasks — type consistency is locked here, before any code exists to contradict it.

**Stage 2 — Bite-sized steps (per task, with code):** Go back through the tasks in order and append the implementation steps to each one, expanding strictly against the frozen skeleton. Each step is one action (2-5 minutes):
- "Write the failing test" - step (with the actual test code)
- "Run it to make sure it fails" - step (exact command + expected failure)
- "Implement the minimal code to make the test pass" - step (with the actual code)
- "Run the tests and make sure they pass" - step (exact command + expected output)
- "Commit" - step (exact git commands)

If Stage 2 reveals a skeleton mistake (missing parameter, wrong type), fix the skeleton block first, re-check every other task that consumes that interface, then continue.

**Incremental writing:** Never compose the whole plan in memory and write it in one call — large single writes time out. Write the file in sections: first the header and every task's skeleton block (one write per few tasks), then append each task's Stage 2 steps task-by-task with separate edits.

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use podium:team-spawn (recommended) or podium:team-fable to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## Task Structure

Each task has two parts, written in the two stages above: the spec block (Stage 1), then the steps (Stage 2).

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

**Behavior:**
[What this component does and why — the decisions made during
brainstorming that the implementer cannot derive from the codebase.
Edge cases and error-path behavior spelled out.]

**Constraints:**
- [Hard requirements: algorithms mandated, dependencies allowed/forbidden,
  performance bounds, naming rules — one line each]

**Acceptance criteria:**
- [ ] [Mechanically checkable condition — a named test that must exist and
  pass, a command with expected output, a grep-able content marker]

**Steps:**

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every task must contain the actual content an implementer needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases" — name the specific error paths and the required behavior for each
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the implementer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- Acceptance criteria that can't be checked mechanically ("works correctly", "is robust")
- References to types, functions, or methods not defined in any task's Produces block

## Remember

- Exact file paths always
- Exact interface signatures in every task's spec block — names, parameters, return types
- Complete code in every Stage 2 step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

Run by the authoring member after completing both stages, before reporting `READY_FOR_SIGNOFF`. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names used in Stage 2 code match the skeleton's Interfaces blocks? A function called `clearLayers()` in Task 3's skeleton but `clearFullLayers()` in Task 7's code is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task. Include the results of all three checks in your sign-off report.

## Execution Handoff

After the plan is signed off, the main conversation offers execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Team Spawn (recommended)** - Continue with the existing team via podium:team-spawn, one member per task, review between tasks, fast iteration

**2. Fable Squad** - Execute via podium:team-fable, round-based milestones with handoff docs

**Which approach?"**

**If Team Spawn chosen:**
- **REQUIRED SUB-SKILL:** Use podium:team-spawn
- Fresh team member per task + two-stage review

**If Fable Squad chosen:**
- **REQUIRED SUB-SKILL:** Use podium:team-fable
- Round-based execution with checkpoints for review
