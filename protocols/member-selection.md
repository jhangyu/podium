How every team member slot is chosen (capability tiers) and how many slots exist (task-derived count).

Referenced by: `podium:team-spawn`, `podium:team-fable`.

## Selection Tiers

Every specialist slot is filled by walking three tiers in order — take the first tier with a capability match:

1. **Registered agents** (`${CLAUDE_PLUGIN_ROOT}/agents/`, subagent_type prefix `podium:`): team-lead, team-reviewer, team-debugger, team-implementer, team-test-runner, team-doc-updater, architect-reviewer, code-reviewer, legacy-modernizer, performance-engineer, c-pro, cpp-pro, golang-pro, rust-pro.
2. **Roster specialists** (115 roles): Read `${CLAUDE_PLUGIN_ROOT}/skills/team-roster/references/details.md` and match roles against the task. Spawn as `general-purpose`; the task prompt MUST begin: `Read <absolute path to the roster file> and fully adopt that agent definition (role, approach, constraints). Then execute the following task: ...`. Use the model from the roster file's frontmatter.
3. **`podium:team-implementer`** — generic builder, last resort only when tiers 1–2 have no match.

Capability signals come from the task description (`$ARGUMENTS` + conversation context) corroborated by repo facts: manifest files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), migrations directories, `Dockerfile`, test commands. Do not assign a specialist the repo facts contradict.

## Member Count Derivation

- **One independently verifiable deliverable = one member.** Parallel is the default: enumerate deliverables first; that count is the number of specialist slots.
- **Serial is a claim that requires evidence** — name the shared data, state, or ordering between steps; if you can't, they are independent deliverables. A proven serial chain gets exactly one worker **at a time** (see the baton rotation rules in `${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md`) — never concurrent capture/implement/verify members.
- **Implementer count per squad**: one implementer per independently verifiable deliverable, cap 3 per squad. A proven chain gets one implementer at a time, rotated per baton rotation.
- **Milestone sizing gate**: after decomposing, divide the round's task count by the member count. If any member would carry more than 4 tasks (or more than 2 judgment-dense tasks), the milestone is too large — split it into more rounds instead of loading one member.
- **Squad count**: derived from truly independent work streams (default 2, hard max 3); a task with a single stream runs one squad — do not pad squads to fill the shape.
- `--members N` overrides the derived specialist-slot count; scaffolding conditions still apply.

## Conditional Scaffolding

Scaffolding roles are conditional, not automatic:

- `team-lead` — only when specialist slots ≥ 3 (below that, the main agent coordinates directly). In squad orchestration, each squad has a lead at model `opus`.
- `team-test-runner` — only when the repo (or the squad's worktree) has a runnable test/build command; otherwise omit it and the lead verifies by executing the changed path directly.
- `team-doc-updater` — only when the change touches user-facing docs.

## Model Assignment

Squad lead = `opus`; implementers = `sonnet` by default, `fable` or `opus` for judgment-dense subtasks (architecture, tricky algorithms, security-sensitive paths); test-runner = `haiku`. Work packages touching authn/authz, secrets, crypto, or input validation get `opus` implementers, and the round review runs a maximum-thoroughness security pass over that squad's diff (probe abuse cases and trust-boundary bypasses, not just functional edges).

## Team Protocol Preamble (mandatory for every roster-adopted member)

Roster definitions are written for solo work and contain no team protocol. Every roster-adopted member's task prompt MUST prepend, after the adopt instruction:

- `ROLE: WORKER — you may NOT spawn agents, teams, or workflows. If the task needs delegation, STOP and report back.`
- Explicit owned-files list; never modify files outside it; message the team lead before touching any shared file.
- The full reporting-discipline block from `${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md`.

Registered team-* agents already carry the protocol; they only need the reporting-discipline block embedded.
