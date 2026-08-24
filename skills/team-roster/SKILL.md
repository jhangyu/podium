---
name: team-roster
description: Expert agent roster for composing teams or delegating specialist work. Use when picking team members, or when a task needs a specialist (backend architecture, API security, deployment/CI-CD, docs, DX, GraphQL, TDD, testing, Django/FastAPI, TypeScript, threat modeling...) not in the registered agent list.
---

# Team Roster

Roster files live at `${CLAUDE_PLUGIN_ROOT}/roster/`. To use a role: Read the roster file, then spawn a team member (Agent tool with your `team_name` set, subagent_type `general-purpose`) whose prompt begins: "Read <absolute path to the roster file> and fully adopt that agent definition (role, approach, constraints). Then execute the following task: ...". This costs no registered-agent context. Pick at most the 2 best-matching roles; if nothing matches, use a plain general-purpose team member instead of forcing a bad match.

Roles are grouped by theme (backend/security/testing first, niche last); each roster file is one self-contained agent definition even when a row lists several.

## When to Use

- Composing a team and picking which specialist roles to include
- Delegating a task that needs domain expertise not covered by the registered agent list

See `${CLAUDE_PLUGIN_ROOT}/skills/team-roster/references/details.md` for the full role table (specialty and roster path per role, covering
backend/API, security, testing/debugging, deployment/cloud, database, docs, frontend/mobile,
language specialists, data/ML, and niche domains).
