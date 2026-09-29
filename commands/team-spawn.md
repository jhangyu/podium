---
description: "Spawn an agent team using presets (review, debug, feature, fullstack, refactor, techdebt, performance, systems, research, security, migration) or custom composition"
argument-hint: "<preset|custom> [--name team-name] [--members N] [--delegate] [--lang c|cpp|go|rust]"
---

# team-spawn

Create & spawn a coordinated agent team. Presets define the team **shape**; the actual members and their count are derived from the task content, not fixed lists.

## Pre-flight Checks

1. Verify the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable is set. If not, halt and instruct the user to set it before proceeding.
2. Parse arguments:
   - First positional arg: preset name or `custom`
   - `--name <team-name>`: override default team name
   - `--members N`: explicit member-count override (skips count derivation)
   - `--delegate`: pass task delegation hints to agents
   - `--lang c|cpp|go|rust`: language specialization hint (strong signal for tier-1 language specialists)

## Member Selection

Every specialist slot (which role, how many, and the conditional scaffolding roles) is derived from the task, not from a fixed list. Follow the member selection protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/member-selection.md and apply it. `--members N` overrides the derived specialist-slot count; scaffolding conditions still apply.

### Baton Rotation (mandatory for every worker)

Members rotate on a task cap and hand off via a baton doc. Follow the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Preset Configurations

Each preset defines its shape: which scaffolding applies and how specialist slots are derived. All slots are filled via Member Selection above.

### `review`
Default name: `review-team`. One `podium:team-reviewer` per review dimension relevant to the diff (e.g. security, performance, architecture, correctness — derive from what the diff touches). `team-doc-updater` per scaffolding condition.

### `debug`
Default name: `debug-team`. One `podium:team-debugger` per competing hypothesis derived from the symptom (typically 2–4). `team-doc-updater` documents the runbook.

### `feature`
Default name: `feature-team`. One specialist slot per parallel feature stream. Scaffolding per conditions.

### `fullstack`
Default name: `fullstack-team`. One specialist slot per layer the task actually touches (frontend, backend, data, tests) — omit layers the task doesn't touch. Scaffolding per conditions.

### `research`
Default name: `research-team`. One `general-purpose` (roster-adopted where a role matches, e.g. search-specialist) per independent research area.

### `security`
Default name: `security-team`. One reviewer slot per attack-surface dimension present in the codebase (e.g. OWASP top 10, auth & access control, dependency vulnerabilities, secrets & config exposure) — prefer roster security roles (security-auditor, threat-modeling-expert, backend/frontend/mobile-security-coder) over generic team-reviewer when they match.

### `migration`
Default name: `migration-team`. One specialist slot per independent migration stream; correctness is verified per the round review cadence. Scaffolding per conditions.

### `refactor`
Default name: `refactor-team`. `podium:legacy-modernizer` when legacy patterns are in scope; one specialist slot per refactor stream; correctness is verified per the round review cadence. Scaffolding per conditions.

### `techdebt`
Default name: `techdebt-team`. `architect-reviewer` (structural debt) + `code-reviewer` (code-level debt); `legacy-modernizer` when modernization is applied. Scaffolding per conditions.

### `performance`
Default name: `performance-team`. `performance-engineer` always; `architect-reviewer` when architectural concerns surface; language specialist per `--lang` or detected repo language. `team-test-runner` runs benchmarks.

### `systems`
Default name: `systems-team`. Language specialist per `--lang` (`c-pro`/`cpp-pro`/`golang-pro`/`rust-pro`); if `--lang` absent, detect from repo manifests, and only if still ambiguous use AskUserQuestion. Scaffolding per conditions.

## Custom Composition

If the first argument is `custom`:
1. Run Member Selection to derive a proposed team: for each slot, the chosen role, its source tier (agent / roster / fallback), model, and a one-line reason.
2. Present the proposal via AskUserQuestion for the user to confirm or adjust (swap roles, change counts).
3. Ask for team name if `--name` was not provided.
4. Compose the final member list from the confirmed selections.

## Team Protocol Preamble (mandatory for every roster-adopted member)

Roster definitions are written for solo work and carry no team protocol, so every roster-adopted member's task prompt needs a preamble prepended after the adopt instruction. Follow the member selection protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/member-selection.md and apply it.

## Member Naming and Reporting Discipline

Every spawned member's `name` carries its role and its model as a suffix, and every member task prompt embeds the reporting-discipline block (end-of-turn delivery, artifact-first verification, chain of command, signoff). Follow the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Review Cadence and Round Discipline

Review happens once per round, with a single round reviewer scoped to the round's combined diff; the same protocol defines the orchestrator's duties during a round, including the **stall watchdog** the main agent runs over idle notifications. Follow the rounds and review protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/rounds-and-review.md and apply it. Presets whose deliverable IS review are exempt from the round reviewer, as that protocol states.

## File Ownership

Follow the file ownership protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/file-ownership.md and apply it.

## Verification

Follow the verification protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/verification.md and apply it.

## Shutdown

When the team's work is done, follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Team Creation

1. Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY: `TeamCreate` with `displayMode: "tmux"`; IMPLICIT: skip).
2. Call TaskCreate once per member to assign their initial role context and any relevant instructions. All task prompts MUST be written in English, MUST embed the reporting-discipline block from the reporting protocol, and for roster-adopted members MUST include the full Team Protocol Preamble from the member selection protocol.
3. If `--delegate` is set, include delegation hints in each task prompt: owned files, blockedBy relationships, and acceptance criteria placeholders.

## Output

Present a formatted summary after spawn completes:

```
Team: {team-name}
Preset: {preset or "custom"}

Members:
  [1] {name} — {role/focus} — source: {agent|roster:<role>|fallback} — model: {model}
  [2] ...

Status: All agents spawned. Tasks assigned.
```
