# Podium Task 7 Acceptance Log — 2026-08-24

Evidence binds to repo HEAD: `99cf3aa` (branch main). Executed by the main conversation (orchestrator), per plan.
Plan: superpowers repo `docs/plans/2026-08-24-podium-implementation.md`; spec: `docs/specs/2026-08-24-podium-architecture-design.md`.

## Install

- Marketplace `jhangyu` re-registered from GitHub (jhangyu/superpowers) to local `/Users/jhangyu/project/podium` — remove RC=0, add RC=0.
- `claude plugin install podium@jhangyu` → RC=0; `installed_plugins.json` shows `podium@jhangyu` v1.0.0 at cache `…/jhangyu/podium/1.0.0` with all layers (agents, commands, protocols, roster, scripts, skills).
- Note: install cache also copied gitignored `docs/logs/` verify artifacts (local-only, harmless).

## Mechanical acceptance (spec §5, run at HEAD 99cf3aa)

| # | Check | Result |
|---|---|---|
| 1 | Fresh-session visibility | PASS with caveat (below) |
| 2 | Old prefixes repo-wide (README provenance exempt) | 0 hits — PASS |
| 3 | Router dispatch targets resolve | 37/37, `xargs ls` RC=0 — PASS (spec said 34; real source table has 37 rows — plan-stage miscount, corrected) |
| 4 | Mechanism uniqueness outside protocols/ | 0 hits (`first match wins` / `one deliverable = one member` / `CONFIRMED/REFUTED` over commands/, skills/, agents/) — PASS |
| 5 | Live team cycle | PASS with caveat (below) |

## Fresh-session visibility evidence

- Commands: headless fresh session lists all 12 `podium:team-*` commands.
- Skills: named checks return yes for `podium:brainstorming`, `podium:writing-plans`, `podium:team-roster`.
- Agents: structural evidence only — cache agents/ is byte-identical to a source whose registration works; fresh-session listing shows `podium:team-lead`; a real spawn attempt failed at the user's delegation-policy hook layer (not at name resolution), so it is inconclusive. **Final functional agent check deferred to post-cutover** (old plugin currently shadows identical agent names — the README incompatibility statement describes exactly this state).

## Live team cycle (the mechanism liveness proof)

Vehicle: the real 9-member build team `podium-build` (6 implementers + 2 reviewers + 1 livefire worker).

- Spawn→dispatch→report→signoff: `impl-livefire-haiku` spawned into the team, executed, delivered its report via SendMessage, ended `READY_FOR_SIGNOFF`, lead signed off. Flow PASS.
- **Caveat (recorded honestly):** the worker claimed it appended marker `marker-7f3a9c` to `/tmp/podium-livefire.txt` with RC=0, but the file and marker string exist nowhere on disk. Most likely its `/tmp` write was blocked by the session-global tmp-guard hook and the haiku worker misreported success. The artifact leg of this sub-test is therefore VOID; the flow leg stands on message delivery + pane lifecycle. (Consistent with the lessons rule: cheap instruments have systematic bias; haiku gets no second chance.)
- Teardown ran the merged 7-phase shutdown protocol from the INSTALLED plugin (`${CLAUDE_PLUGIN_ROOT}/scripts/team_shutdown.py`, cache path):
  - Phase 0 snapshot: `{"phase":"snapshot","ok":true,"cleanup_mode":"server","target_panes":["%0".."%8"]}` — 9 target panes, **non-empty** (round-3 reviewer's zero-match fail-open caveat did not trigger; all panes identified via pane-ID+title+cwd matching). RC=0.
  - Phase 3: 9 shutdown_requests sent in protocol role order (all members were in the implementers/reviewers group; no test-runner/doc-updater existed; lead is the invoking session, no pane).
  - Phase 4 drain: `{"phase":"drain","ok":true,"live_panes":[]}` RC=0.
  - Phase 5 TeamDelete: success, only after both gates ok.
  - Phase 6 verify: `{"phase":"verify","ok":true,"live_panes":[]}` RC=0 (config + task dirs gone).

## Deviations & incidents (adjudicated during the build)

1. Routed references: spec's "統一放 references/routed/" superseded — round-3 review found all 37 targets already existed as ADAPTED copies under the router skills' references/; single-copy design adopted (`references/routed/` deleted, team-router points at skill copies). ~23k duplicate lines avoided.
2. Row count 34 → 37 (plan-stage miscount; all real rows vendored, none dropped).
3. Shared-index incident: commit `353c4ab` (protocols work) swept a teammate's staged deletion of references/routed/ via a bare `git commit`. No data loss; deletion was ordered work. Rule adopted mid-build: pathspec commits (`git commit -- <own paths>`) on shared trees.
4. This acceptance log lives at `docs/acceptance-2026-08-24.md` instead of the plan's `docs/logs/` (that path is gitignored by design).

## Review trail

- Round 2 (skills+protocols+copy): adversarial review CONFIRMED after 1 fix cycle (6 findings resolved, commit 7e9c21b).
- Round 3 (commands+routers, then Task 9): CONFIRMED after 1 fix cycle (single-copy redesign 99cf3aa; Referenced-by reconciliation 7fa82cd); cycle-2 re-verification CONFIRMED, all invariants independently reproduced by the reviewer.
- Outstanding parking-lot items are tracked in the closure report to the user, not here.

## Task 8 Cutover (executed after this log's first commit)

- Backups: 7 touched files copied to `~/.claude/backups/*.bak-20260824` before any edit.
- Living-rule rewrites: `~/.claude/CLAUDE.md` 任務編排 line → `podium:team-spawn`; `hooks/global-agent-gate` deny-message → `podium:team-spawn`; `reference/team-shutdown-protocol.md` → two-line stub pointing at installed podium `protocols/shutdown.md` + `scripts/team_shutdown.py`; `reference/team_shutdown.py` and `scripts/register_extended_agent_teams.py` removed (backed up). Dated addendums appended to `harness-diagnosis.md` / `hooks-architecture.md`; historical ledgers (change-log, archive/, lessons-learned) intentionally left as history.
- Uninstalls: `superpowers@jhangyu` was already auto-removed with the earlier `jhangyu` marketplace re-registration; `extended-agent-teams@claude-code-workflows` uninstalled RC=0; `claude-code-workflows` marketplace removed RC=0.
- Verification: `installed_plugins.json` old-plugin hits = 0, `podium@jhangyu` present; `known_marketplaces.json` claude-code-workflows = 0, `jhangyu` → directory `/Users/jhangyu/project/podium`; living-rule colon-prefix grep over CLAUDE.md/rules/reference (backups+archive excluded) = 0.
- Post-cutover fresh session (decisive, shadowing gone): `podium:brainstorming` yes / `superpowers:brainstorming` no / `extended-agent-teams:team-spawn` no / agent types `podium:architect-reviewer, podium:c-pro, podium:code-reviewer, podium:cpp-pro, podium:golang-pro…` listed. The Task 7 deferred agent check now PASSES.
