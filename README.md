# podium

A single Claude Code plugin merging methodology skills with agent-team orchestration into one pipeline.

## Overview

podium has five layers plus a shared protocols layer:

1. **Methodology skills** (`skills/`) — brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, plus domain routers and the team-roster index skill.
2. **Team commands** (`commands/`) — `/podium:team-spawn`, `/podium:team-fable`, `/podium:team-status`, `/podium:team-shutdown`, `/podium:team-review`, `/podium:team-debug`, `/podium:team-feature`, `/podium:team-delegate`, `/podium:team-refactor`, `/podium:team-techdebt`, `/podium:team-performance`, `/podium:team-router`.
3. **Agent definitions** (`agents/`) — team-lead, team-implementer, team-reviewer, team-debugger, team-test-runner, team-doc-updater, architect-reviewer, code-reviewer, legacy-modernizer, performance-engineer, and language specialists (c-pro, cpp-pro, golang-pro, rust-pro).
4. **Role roster** (`roster/`) — solo role definitions consumed by team-roster and the domain routers.
5. **Domain knowledge** (`references/`) — vendored reference documents routed by `team-router`.

Plus:

- **protocols/** — the seven authoritative mechanism documents (member selection, rounds and review, file ownership, verification, worktree lifecycle, reporting, shutdown). Commands and skills reference these; they never restate the mechanism text themselves.

## Pipeline

```
brainstorming → writing-plans → team-spawn / team-fable → verification-before-completion
```

Ideas are shaped in `brainstorming`, turned into an executable plan in `writing-plans`, executed by a live agent team via `team-spawn` (or `team-fable` for larger squads), and closed out only after `verification-before-completion` gates pass.

## Provenance

podium merges two maintained forks:

- Methodology skills: jhangyu's fork of `obra/superpowers` (now retired; podium is its successor).
- Orchestration layer: the fork-local extended-agent-teams plugin, v1.3.4 (now retired; podium is its successor).

All mechanism text that was duplicated across the two sources has been extracted into `protocols/`; commands are now thin shells that point at the protocol they follow.

## Incompatibility

Do not enable podium together with `agent-teams` or `systems-programming`. This plugin bundles enhanced supersets of their agents under the same names (`team-lead`, `team-implementer`, `team-reviewer`, `team-debugger`, `c-pro`, `cpp-pro`, `golang-pro`, `rust-pro`), which would collide if co-enabled. Use podium as a drop-in replacement for both.

## Maintenance covenant

Mechanism text (member selection, rounds/review cadence, file ownership, verification, worktree lifecycle, reporting, shutdown) lives only under protocols/. Commands reference protocols; they never restate them. Any mechanism revision edits exactly one file under protocols/. One sanctioned exception: the reviewer findings-template's canonical home is `agents/team-reviewer.md` (protocols/verification.md points at it laterally).
