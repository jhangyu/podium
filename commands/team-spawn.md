---
description: "Spawn an agent team using presets (review, debug, feature, fullstack, refactor, techdebt, performance, systems, research, security, migration) or custom composition"
argument-hint: "<preset|custom> [--name team-name] [--members N] [--delegate] [--lang c|cpp|go|rust]"
---

# team-spawn

Spawn a coordinated agent team. A preset fixes the team **shape**; members and counts are derived from the task. `P` = `${CLAUDE_PLUGIN_ROOT}/protocols/`.

## Arguments
- 1st positional: preset or `custom`. `--name`: team label (default `<preset>-team`). `--members N`: overrides derived specialist count (scaffolding conditions still apply). `--delegate`: add owned files, blockedBy, and acceptance-criteria placeholders to each task prompt. `--lang c|cpp|go|rust`: language-specialist hint.
- Do not pre-check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; on a teams-disabled error, halt and tell the user to set it to `1`.

## Spawn recipe (first call must succeed)
Every `Agent` call carries ALL of: `name` (session-unique, `{role}-{model}`; suffix `-2` if taken), `team_name` (the team label — always include it: legacy gates require it; harmless in IMPLICIT), `subagent_type`, explicit `model`, and a prompt that contains:
- `ROLE: WORKER — you may NOT spawn agents, teams, or workflows. If the task needs delegation, STOP and report back.`
- `Report via SendMessage to team-lead; if unreachable, send to main.`

Spawn all members in ONE message. If a `TeamCreate` tool exists in this build, create the team with it first (`displayMode: "tmux"`). Details: `P/team-mode.md`.

## Presets (slots filled via `P/member-selection.md`; scaffolding per its conditions)
| Preset | Slots |
|---|---|
| `review` | one `podium:team-reviewer` per dimension (default six: security, performance, architecture, testing, accessibility, techdebt) |
| `debug` | one `podium:team-debugger` per competing hypothesis (typically 2–4); doc-updater writes the runbook |
| `feature` | one slot per parallel feature stream |
| `fullstack` | one slot per layer actually touched (frontend/backend/data/tests) |
| `research` | one `general-purpose` (roster-adopted where a role matches, e.g. search-specialist) per independent area |
| `security` | one reviewer per attack-surface dimension present (OWASP, authn/authz, deps, secrets/config); prefer roster security roles over generic team-reviewer |
| `migration` | one slot per independent migration stream |
| `refactor` | `podium:legacy-modernizer` when legacy patterns are in scope + one slot per refactor stream |
| `techdebt` | `architect-reviewer` + `code-reviewer`; `legacy-modernizer` when modernization is applied |
| `performance` | `performance-engineer`; `architect-reviewer` if architectural concerns surface; language specialist per `--lang`/repo; `team-test-runner` runs benchmarks |
| `systems` | `c-pro`/`cpp-pro`/`golang-pro`/`rust-pro` per `--lang`, else detect from manifests, else AskUserQuestion |

`custom`: run member selection, present each slot (role, source tier agent/roster/fallback, model, one-line reason) via AskUserQuestion to confirm/adjust, ask for a name if `--name` is absent, then spawn the confirmed list.

## Steps
1. Select members per `P/member-selection.md`.
2. Spawn per the recipe above.
3. `TaskCreate` one task per member (English). Each prompt embeds the reporting-discipline block (`P/reporting.md`); roster-adopted members also get the Team Protocol Preamble (`P/member-selection.md`).
4. Run the team under `P/reporting.md` (naming, baton rotation, signoff, language), `P/rounds-and-review.md` (one round reviewer per round, stall watchdog; review-deliverable presets skip the round reviewer), `P/file-ownership.md`, `P/verification.md`; finish with `P/shutdown.md`.

## Output
```
Team: {team-name}
Preset: {preset or "custom"}
Members:
  [1] {name} — {role/focus} — source: {agent|roster:<role>|fallback} — model: {model}
Status: All agents spawned. Tasks assigned.
```
