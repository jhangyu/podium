The single source of every review check.
It defines what blocks, how severe, which dimension runs each check, how findings merge, and where debt is recorded.

Referenced by:
- `agents/team-reviewer.md`, `agents/team-implementer.md`
- `protocols/verification.md`, `protocols/rounds-and-review.md`
- `commands/team-review.md`, `commands/team-techdebt.md`, `commands/team-refactor.md`
- `skills/writing-plans/SKILL.md`, `skills/writing-plans/plan-document-reviewer-prompt.md`, `skills/refactor-clean/SKILL.md`
- `README.md`

Check format:
```
**ID Name**
- Rule: <one sentence>
- <extra condition, one per bullet>
- Evidence: <what the finding cites>
- Sev: <default severity>
```
Policy Gate checks add `- Enforced:`.
IDs are stable: never renumber, never reuse a retired ID.
Retired IDs, never reused: G16, G18, G19, H14, H15.
A sub-check such as Q2a follows its parent.

## Scope and blocking

**S1 New code only blocks**
- Rule: Only `introduced` findings block the diff.
- A `deferred` finding (C2) does not block; it goes to the register.
- A `pre-existing` finding never blocks; it goes to the register.
- This holds for every check, L2 Policy Gate checks such as G17 and G20 included.
- Evidence: the finding's Origin and Tags fields.
- Sev: n/a.

**S2 Finding names an action**
- Rule: A finding without a concrete fix action is dropped before consolidation.
- Evidence: the Recommended Fix field.
- Sev: n/a.

**S3 Origin tag**
- Rule: A finding whose line lies inside a hunk of `git diff -U0 <base>` is `introduced`; else `pre-existing`.
- A target with no diff: every finding is `pre-existing`.
- A finding with no line, such as a missing file or config: `introduced` only when the diff deleted it; else `pre-existing`.
- A finding at an unchanged line that a hunk caused, such as code orphaned by a deleted caller, is `introduced`.
- Evidence: hunk range, or its absence, or the deleting or causing hunk.
- Sev: n/a.

## Severity

| Severity | Impact | Likelihood |
|---|---|---|
| Critical | Data loss, security breach, complete failure | Certain or very likely |
| High | Significant functionality impact; structural finding that blocks the next change | Likely |
| Medium | Partial impact, workaround exists | Possible |
| Low | Minimal impact, cosmetic | Unlikely |

Calibration floors:
- Externally exploitable security ≥ High.
- Hot-path performance, missing critical-path tests, core-function accessibility ≥ Medium.
- Style-only with no functional impact = Low.
- Critical path: code whose failure meets the Critical or High ladder row, or that implements a capability the spec, README, or G13 manifest promises.

Default vs adjusted:
- Each check's `Sev:` is its default.
- When the evidence meets a different ladder row, use that row and quote the evidence in the Severity field.
- Example: a Q2a cycle that makes a module fail to import meets "complete failure, certain" = Critical.
- Severity follows evidence, never the question number.
- An unanswerable L1 question = Medium.

Only these four words name a severity.
The `/team-techdebt` priority score multiplies by severity; it is not a severity.

## Dimensions

Each reviewer applies only its assigned dimensions.
Each check runs in exactly one dimension; the table below is the only assignment.
A finding from a dimension line cites the dimension name as its Rule; a check finding cites the check ID.

| Dimension | Runs |
|---|---|
| Security | its line below |
| Performance | its line below |
| Architecture | its line below; also §L1 when techdebt is not assigned |
| Testing | its line below, H5, H11, H12, and H13 |
| Accessibility | its line below |
| Techdebt | §L0 when a plan or design doc is in scope; §L1; §L2; §L3 except H5, H11, H12, and H13; whole-tree audits add §Periodic audit |

- **Security**: input validation and sanitization; authentication and authorization; injection, XSS, CSRF; secrets exposure.
  Also: known-CVE dependencies; insecure cryptography; access-control bypass; API rate limits and input bounds.
- **Performance**: query efficiency such as N+1, missing indexes, full scans; memory leaks; redundant computation.
  Also: caching and invalidation; async correctness; resource cleanup; algorithmic complexity; bundle size and lazy loading.
- **Architecture**: API contract design and versioning; configuration management; one error-handling convention across modules.
  Not here: dependency direction, cycles, cohesion, coupling, SOLID, abstraction, swallowed errors, hard-coded values; these are L1 and L3 checks.
- **Testing**: critical-path coverage gaps; an assertion that cannot fail when the logic breaks = finding (effect assertions: H12).
  Also: a test changed to fit the implementation is H12; isolation and determinism; mock accuracy.
  Also: edge cases; integration completeness; brittleness.
- **Accessibility**: WCAG 2.1 AA; semantic HTML and ARIA; keyboard navigation; screen readers.
  Also: color contrast; focus order; alternative text; zoom and responsive layout.

## L0 Plan gate

Applies to plans and to diffs that link a plan.
The plan template fields live in `skills/writing-plans/SKILL.md`.

**D1 Decision record**
- Rule: A plan or diff that changes a data model, public API, cross-module contract, runtime technology, or deployable unit links a decision record.
- The record, such as an ADR, RFC, or KEP, has ≥2 alternatives, drivers, and drawbacks.
- Refactors and bug fixes are exempt.
- Evidence: changed surface `file:line` + missing field name.
- Sev: Medium; High for a data model or public API.

**D2 One deployable unit**
- Rule: A new service, process entrypoint, or deployable boundary states an operational reason.
- Operational reasons: load profile, independent scaling, isolation.
- "Cleaner modularity" is not a reason; modules are enforced in-process per G7.
- Evidence: new unit path + quoted reason or its absence.
- Sev: High.

**D3 Module layer declared**
- Rule: Each new module in a plan names its layer and its allowed dependencies.
- A module without a layer is not added.
- Evidence: new module path missing a layer entry.
- Sev: Medium.

## L1 Structural questions

A question protocol, not a checklist.
Answer each question in one sentence with evidence.
An unanswerable question is itself a finding.

**Q1 Right layer**
- Rule: The fix lives where the root cause lives.
- The same fix in 2+ places = wrong layer.
- Evidence: caller list.
- Sev: High.

**Q2 Dependency direction**
- Rule: Core logic imports no UI, framework, or IO; a lower layer imports no upper layer.
- Covers SOLID dependency inversion.
- Layer source, first that exists: the G7 checker config, the D3 plan entry, the import direction between the two modules in base.
- The Evidence names the layer source used; with no source, only the core-logic clause applies.
- Evidence: direction of each new import.
- Sev: High.

**Q2a No new cycle**
- Rule: A module cycle present in head and absent in base = finding.
- A lazy import that hides a cycle counts as the cycle.
- Run the project's G7 checker when configured; else grep imports.
- Evidence: path `A → B → A` + new edge `file:line`.
- Sev: High.

**Q2b Hotspot patterns**
- Rule: A parent references a subclass = finding.
- An interface file changed by consecutive PRs = finding.
- Two modules that co-change with no import between them = finding.
- Use A1 co-change data when available.
- Evidence: edge `file:line` or commit hashes.
- Sev: High.

**Q3 Single home**
- Rule: The diff redefines no domain concept's behavior in a second place.
- Evidence: location of the concept's existing definition.
- Sev: High.

**Q3a No foreign data writes**
- Rule: New code writes no other module's tables, store, or schema.
- Cross-module data access goes through the owner's public entry.
- Evidence: write `file:line` + owning module.
- Sev: High.

**Q3b Decision-record conformance**
- Rule: When the repo has decision records, a diff contradicting a code-visible decision = finding.
- Code-visible decisions: dependency, layering, library, pattern.
- Deployment and intent decisions are reported as "needs human", never judged.
- Evidence: record path + decision line + contradicting `file:line`.
- Sev: High.

**Q4 Necessary state**
- Rule: State derivable from existing data is not stored separately.
- Evidence: the derivation source, or why none exists.
- Sev: Medium.

**Q5 Boundary shape**
- Rule: Cross-module signatures pass what the callee needs, not what the caller happens to have.
- Covers SOLID interface segregation.
- Evidence: parameter shape of each new cross-module call.
- Sev: Medium.

**Q6 Next change**
- Rule: The diff does not block the next obvious roadmap need.
- A blocking trade-off is surfaced to the user, never silently merged.
- Evidence: the roadmap need + the blocking point.
- Sev: High.

**Q7 Deletable as a block**
- Rule: A new path is one pluggable block, not tentacles into multiple existing modules.
- A new deployable unit is checked against D2.
- Evidence: integration-point count.
- Sev: Medium.

**Q8 Single responsibility and substitution**
- Rule: A new or changed class or module has one reason to change; 2+ unrelated reasons = finding.
- A subtype that rejects, narrows, or weakens its parent's contract = finding.
- Covers the SOLID principles not owned by Q2, Q5, H2.
- Evidence: the unrelated responsibilities with `file:line`, or the override `file:line` + broken parent contract.
- Sev: Medium.

## L2 Policy Gate

Project-policy checks, each pass/fail.
Runs once per review, by the techdebt holder only.
Run the project's enforcer when one exists; cite its command and exit code.
L2 findings are never deferred; a `pre-existing` L2 finding goes to the register and does not block (S1).

Enforcement label rule:
- Every L2 check carries `Enforced: <path>` naming the hook, CI step, or test that exits non-zero.
- Without one, it carries `Enforced: reviewer-checked`.
- A `reviewer-checked` check is never described as mechanical.
- H7 applies the same label to prose rules.

**G1 Third-party API fidelity**
- Rule: Every third-party API call matches the version installed per the manifest or lockfile.
- An API written from training memory = violation.
- Evidence: call `file:line` + installed version.
- Sev: Critical.
- Enforced: reviewer-checked.

**G2 Verified dependency versions**
- Rule: Versions in new or edited manifests come from registry verification.
- Dep-freshness hook reports are addressed, never ignored.
- Evidence: manifest line + registry version.
- Sev: Critical.
- Enforced: reviewer-checked.

**G3 No platform forks**
- Rule: No per-platform fork or exception unless unreachable.
- An unreachability claim carries proof and a user decision.
- Removing a fork never removes a platform's capability; that removal is G14.
- Evidence: fork `file:line`.
- Sev: Critical.
- Enforced: reviewer-checked.

**G4 No forward-compatibility residue**
- Rule: A replaced module is deleted with its tests and docs.
- Similar functionality converges into one generic module; no parallel paths.
- The replacement's required cases cover every platform the old module served (G13); deletion with no replacement is G14.
- Evidence: surviving old path or parallel module.
- Sev: Critical.
- Enforced: reviewer-checked.

**G5 File-operation scripts**
- Rule: Test, build, and CI file-operation scripts are cross-platform Python.
- One script per functional goal, runnable with zero arguments.
- No bat, shell, or PowerShell.
- Evidence: script path.
- Sev: Critical.
- Enforced: reviewer-checked.

**G6 Shortcut declared**
- Rule: Every added shortcut carries a ticket, an owner, and an allowed reason.
- Shortcuts: baseline entry; suppression such as `noqa`, `eslint-disable`, `@SuppressWarnings`, `#[allow`; `TODO`/`FIXME`/`HACK`; shim; skipped layer.
- The declaration lives in the PR description, the round report, or the commit message when there is no PR.
- The shortcut also has a register row with `Entry: shortcut`.
- Allowed reasons: hotfix, design-improving move, making an implicit dependency explicit.
- Evidence: marker `file:line` + missing ticket, owner, or reason.
- Sev: High; Critical when the stated reason is schedule.
- Enforced: reviewer-checked.

**G7 Executable architecture contract**
- Rule: Layers, allowed dependencies, public-entry-only access, and no new cycles live in a checker config that CI runs in blocking mode.
- Language-level checkers: import-linter, tach, dependency-cruiser, Nx tags, ArchUnit, go-arch-lint, Packwerk, Deptrac.
- Build-level checkers: Bazel `visibility`, cargo-deny.
- A prose-only boundary rule = finding.
- When no checker config exists, report G7 only; G8–G11 are not reported separately.
- Evidence: config path + CI step `file:line`, or their absence.
- Sev: High.
- Enforced: reviewer-checked.

**G8 Exhaustive classification**
- Rule: Every module is assigned to a layer or tag; an unassigned module fails the contract.
- Runs only when a G7 checker config exists.
- Evidence: config line, or an untagged module that passed.
- Sev: High.
- Enforced: reviewer-checked.

**G9 Rule canary**
- Rule: Each architecture rule has a canary that turns the check red, including one transitive edge.
- A rule never seen red is unproven.
- Runs only when a G7 checker config exists.
- Evidence: canary path + observed exit code, per `protocols/verification.md` §Evidence Discipline.
- Sev: High.
- Enforced: reviewer-checked.

**G10 Frozen baseline**
- Rule: Pre-existing violations live in a committed baseline matched by file and rule, never by line.
- CI cannot create or update the baseline; stale entries fail.
- Runs only when a G7 checker config exists.
- Evidence: baseline path + CI flag line.
- Sev: High.
- Enforced: reviewer-checked.

**G11 Baseline shrinks only**
- Rule: A PR only deletes baseline lines.
- A test pins the entry count; each entry links a ticket.
- Additions only via G6 allowed reasons.
- Applies to violation baselines only; a shrink of the G13 manifest is a removal under G14.
- Runs only when a G7 checker config exists.
- Evidence: count delta, or an entry without a ticket.
- Sev: High.
- Enforced: reviewer-checked.

**G12 Ratchet on new code**
- Rule: Lint, type, and coverage gates run on changed files; per-file counts only decrease.
- New modules start strict.
- Matching is by file and rule, never by line.
- Runs independently of G7.
- Evidence: config path, a file whose count rose, or a new module on the relaxed list.
- Sev: Medium.
- Enforced: reviewer-checked.

**G13 Required-capability manifest**
- Rule: Each capability the product promises is listed in a committed manifest: capability × platform → implementing symbol + required case IDs.
- Applies only when the project declares 2+ platforms in its build config or package manifest, or its spec, README, or docs promise a capability per platform.
- The declaration is enough; no separate build per platform is needed. Otherwise G13 does not fire; G15 applies only when G13 does.
- The manifest is a declaration source; it is written by hand and never generated from the tree it checks.
- The manifest's case column is the required-case list every gate reads; a gate judged only by exit code and executed count = finding.
- An enforcer fails when a listed symbol is undefined, or a listed case is not among the passed results of its platform leg.
- Not-run cases follow G17.
- The enforcer has a canary: deleting one required case in a scratch copy turns it red, per `protocols/verification.md` §Evidence Discipline.
- Runs independently of G7.
- Evidence: manifest path + enforcer step `file:line` + canary exit code, or their absence.
- Sev: High.
- Enforced: reviewer-checked.

**G14 Capability removal is a user decision**
- Rule: A diff that removes a capability from a platform links a user decision; without one = finding.
- Removal: deleting a G13 manifest row, a platform from a row, a required case, or the implementing symbol.
- Without a manifest: deleting the implementation of a capability that the spec, README, or docs promise, with its test, counts as removal.
- Deleting dead code that no spec, README, or doc promises is H9, not removal.
- A tree-mirroring list, such as a parity or test list, is not evidence of intent; a row it drops with its code and test counts as removal.
- Removing a platform fork (G3) or a replaced module (G4) is compliant only when every platform keeps the capability.
- The decision lives in a decision record (D1), the PR description, or the commit message, and names the user who approved it.
- A G14 finding is tagged `needs-user-decision`; the lead asks the user, as for G17.
- Runs independently of G7.
- Evidence: deleting hunk `file:line` for the row, case, or symbol + the missing decision link.
- Sev: Critical.
- Enforced: reviewer-checked.

**G15 Deletion guard outside the author's write scope**
- Rule: The G13 manifest and its required cases are protected by an enforcer the change author cannot edit.
- Accepted enforcers: required review on those paths by a user-owned rule, branch protection, or a user-owned hook.
- An in-repo freeze, such as a digest, pin, or ruling field, is never an accepted enforcer: the same diff can edit it.
- A diff that edits a frozen file and its freeze together is G20.
- Runs independently of G7.
- Evidence: protection config path or hook path, or the in-repo freeze that stands in for one.
- Sev: High.
- Enforced: reviewer-checked.

**G17 Not-run is not passed**
- Rule: A test gate reports green only when no case failed and every not-run case names the host that runs it instead.
- Not-run: skipped, excluded, host-excluded, quarantined, or counted as known-flaky.
- A not-run case named for another host is green only when that host's run artifact for the same commit lists it as passed.
- When neither the reviewer nor the project's gates can run a declared platform, the reviewer judges neither pass nor fail for it.
- It raises a finding tagged `needs-user-decision` naming the platform and what could not run; the lead asks the user.
- A declared platform needs its own run only when the reviewed code branches on platform (G3) or the G13 manifest gives it its own symbol.
- Otherwise a run on any one declared platform covers it.
- A quarantine or known-flaky list holds no G13 required case.
- Evidence: verdict code `file:line` + the not-run counter it does not fail on, the quarantine entry, or the platform and what could not run.
- Sev: High.
- Enforced: reviewer-checked.

**G20 Gate binds the action**
- Rule: Each gate is invoked by the action it guards: a pre-push hook, a required CI check, or a release precondition.
- A gate that runs only by convention = finding.
- A push, merge, or release on a red gate result cites a user decision; the changing agent's own "gate defect" or "flaky" label is not one.
- A diff that changes a frozen artifact and its freeze record together, such as a pinned digest or a frozen list, cites a user decision.
- Evidence: gate entry `file:line` + the unguarded action, the red artifact + release commit, or the refreeze hunk.
- Sev: High; Critical for a release on a red gate.
- Enforced: reviewer-checked.

## L3 Hygiene

Spot-checks after L1 and L2.
Each is a counted check, not prose.

**H1 Single source of truth**
- Rule: No constant, path, or schema is defined in two places.
- A list derivable from a declaration source is not hand-maintained.
- A G13 manifest is itself a declaration source; deriving it from the tree it checks = finding.
- Evidence: both definition sites.
- Sev: Medium.

**H2 Interface evolution**
- Rule: A third optional parameter, or a boolean flag that forks behavior = refactor finding.
- Covers SOLID open-closed.
- Evidence: signature `file:line`.
- Sev: Medium.

**H3 No hardcoding**
- Rule: No absolute path or machine-specific value; magic numbers are named or sourced.
- Evidence: literal `file:line`.
- Sev: Medium.

**H4 Error paths**
- Rule: No empty catch and no error swallowed into a default return.
- A discarded result of an OS, external, or fallible call followed by an unconditional success status = swallowed error.
- Fallible: the call reports failure by result or exception; a call with no failure result, such as one returning a count, is not H4.
- The returned status reflects the call's own result.
- Each error path answers "can data be lost, can the user see fake success".
- Evidence: catch, branch, or discarded-result `file:line`.
- Sev: High.

**H5 Agent-change behavior tests**
- Rule: A diff touching input validation or error handling ships a test that drives the invalid or error path.
- Complexity and duplication metrics do not clear it.
- Run by the Testing holder only (§Dimensions).
- Evidence: branch `file:line` + absent test.
- Sev: High.

**H6 Abstraction matches use count**
- Rule: A new interface, base class, factory, plugin point, or config knob with fewer than 2 real implementers or call sites = finding.
- Under-engineering: a diff that adds the third or later site repeating the same decision with no shared function or type = finding.
- Repeated decisions: the same type or kind switch, the same validation sequence, the same field-by-field mapping.
- Identical copied blocks are H10; one fix applied in many places is Q1.
- Evidence: abstraction `file:line` + implementer and caller count, or every repeating site `file:line`.
- Sev: Medium.

**H7 Failure message teaches**
- Rule: Every gate or hook failure message states the rule, its reason, and the allowed replacement.
- Each MUST rule in CLAUDE.md, AGENTS.md, or skills maps to an enforcer or is labelled `prose`.
- Evidence: rule without reason text, or MUST rule with no enforcer path.
- Sev: Medium.

**H8 Context files resolve**
- Rule: Every path and symbol named in CLAUDE.md, AGENTS.md, skills, or a test matrix exists in the tree.
- A test matrix row that names a deleted test file or case = finding.
- Evidence: dangling reference `file:line`.
- Sev: Medium.

**H9 Residue**
- Rule: No dead code, unused exports, orphan imports, or stale tests of removed behavior.
- No expired flags, shims, or TODOs.
- No obsolete comment: a comment that names a removed symbol or describes behavior the code no longer has.
- A test listed in the G13 manifest is never residue; its removal is G14.
- Evidence: residue `file:line`; for a comment, also the code `file:line` it contradicts.
- Sev: Low.

**H10 No duplicated code blocks**
- Rule: The same code block copy-pasted in 2+ places = finding.
- The minimum block size is project-set.
- Distinct from H1 (definitions) and Q1 (one fix applied in many places).
- Evidence: both block ranges `file:line-line`.
- Sev: Medium.

**H11 Test naming and documentation**
- Rule: Each test name states the behavior and condition under test.
- H11 judges the name's wording only; a name claiming a side effect the body does not assert is H12.
- A test whose setup or intent is not clear from its name and code carries a comment that explains it.
- Run by the Testing holder only (§Dimensions).
- Evidence: test `file:line` + its name.
- Sev: Low.

**H12 Effect, not call**
- Rule: A test of a behavior whose purpose is a side effect asserts the observed effect, not only that a call happened.
- Side effects: state changed, data written, resource released, memory or handle returned, message delivered.
- Call-proof only = finding: a call counter, a spy invocation count, a fake or override that returns success.
- A platform or environment simulated by a flag on another host is call-proof for that platform.
- The expected value or threshold is fixed in the test or a linked spec before the measured run; values are project-set.
- A diff that changes the measured code and loosens its threshold together = finding.
- A diff that loosens a threshold or weakens an assertion without changing the measured code = finding at the default Sev.
- A control case proves the measurement sees the effect: the test was observed red once against a no-op implementation.
- Red-run proof follows `protocols/verification.md` §Evidence Discipline.
- Run by the Testing holder only (§Dimensions).
- Evidence: test `file:line` + the asserted quantity, or the threshold edit and the code edit in the same diff.
- Sev: High; Critical for a threshold loosened together with the code.

**H13 Real path crossed**
- Rule: Each capability whose tests replace a boundary with a fake has ≥1 test that runs the real implementation across that boundary.
- Boundaries: OS or system call, foreign-function or native call, process, network, another repository or package.
- Fakes: mocks, stubs, test-only override hooks in product code, platform flags.
- The real-path test is wired into a gate; a test no gate runs does not count. A platform no one can run is G17.
- A capability tested only through fakes on every layer = finding.
- Run by the Testing holder only (§Dimensions).
- Evidence: the fake or override `file:line` + the capability + the real-path test, or its absence.
- Sev: High.

## Periodic audit

Run by `/team-techdebt` on the whole tree.
Every finding is `pre-existing`.

**A1 Hotspots from history**
- Rule: Rank files by churn from `git log --numstat --since=<horizon>` times complexity; inventory only the project-set top count.
- Files co-changing across module boundaries above a project-set share of commits = High.
- Evidence: rank table, or co-change pair + commit count.
- Sev: High for cross-module co-change; ranking otherwise.

**A2 Absolute counts plus delta**
- Rule: Report debt as absolute count, delta since the previous register, and code size; never density alone.
- Growth proportional to size is not a finding by itself.
- Evidence: the three numbers.
- Sev: n/a.

**A3 Rule curation**
- Rule: A check at ≥10% rejected in the C3 tally is flagged for demotion or removal; the user decides.
- A third-party ruleset adopted wholesale = Low.
- Dependency bots without grouping and an open-PR cap = Medium.
- Evidence: check ID + tally, or bot config line.
- Sev: Low; Medium for bot config.

**A4 Technology lag**
- Rule: Frameworks and libraries behind their supported LTS = finding.
- Also: deprecated API usage, CVE-relevant version lag, outdated build tooling.
- Registry and installed-version mismatches are G1/G2.
- Evidence: dependency + installed vs supported version.
- Sev: Medium; High for CVE exposure.

## Consolidation

**C1 Merge**
- Rule: Same `file:line` and same defect → one finding with the more detailed description, the higher severity, and every flagging dimension.
- Same defect = same check ID, or a parent and its sub-check (such as Q2 and Q2a) on the same `file:line`; the merged finding cites the sub-check ID.
- A dimension-line finding and a check finding on the same `file:line` and defect merge under the check ID.
- Same `file:line`, different defect → separate findings, each tagged `co-located`.
- Same defect, different locations → separate findings, cross-referenced.
- A finding flagged by 2+ dimensions is tagged `multi`.
- Conflicting fixes → keep both with reviewer attribution.
- Evidence: merged finding list.
- Sev: n/a.

**C2 Deferral**
- Rule: When an `introduced` L1 finding exists in a file, `introduced` L3 findings in the same file are tagged `deferred`.
- Same scope = same file path; nothing wider.
- L2 findings are never deferred.
- A deferred finding does not block (S1) and gets a register row with `Entry: deferred`.
- A register row still at `Ticket: TBD` when the report is presented raises no extra finding: the row is the record.
- The report states why the ticket was not created, such as in a read-only run.
- Evidence: deferred finding + ticket ID.
- Sev: Medium.

**C3 Trust tally**
- Rule: The lead counts, per check ID, findings reported vs REFUTED or rejected as not useful with no positive action taken.
- The counts live in the `## Trust tally` table of `TECH_DEBT.md`, carried across runs; A3 reads it.
- Evidence: check ID + reported and rejected counts.
- Sev: n/a.

## Debt register

`TECH_DEBT.md` in the project root holds every pre-existing, deferred, and shortcut finding.
Every review writes it; it is never optional.
One row per finding:

| ID | Location | Rule | Severity | Entry | Ticket | Owner | Added |
|---|---|---|---|---|---|---|---|

Entry values:
- `pre-existing`: the finding's Origin is `pre-existing`.
- `deferred`: Origin `introduced`, tagged `deferred` by C2.
- `shortcut`: a declared G6 shortcut.

Ticket and owner:
- The reviewer writes `Ticket: TBD` and `Owner: TBD`.
- The lead creates the ticket, fills both fields, and asks the user when no owner is known.
- A field the lead cannot fill stays `TBD`, for example with no ticket access or no owner answer yet; never write a guessed value.
- A row still at `Ticket: TBD` is its own record, with no extra finding; the report states why the ticket was not created (C2).
- Row IDs are `TD-<n>`, assigned by the lead in register order.

A fixed entry is deleted, never reworded to hide it.
The file ends with a `## Trust tally` table (C3): `| Check | Reported | Rejected |`.
`/team-techdebt` reports its totals per A2.

## Finding template

```
### [SEVERITY] Finding Title

Location: `path/to/file.ts:42`; deleted lines: base-side `file:line (base)`; no line: the missing or deleted path, or `<repo root>`
Dimension: Security | Performance | Architecture | Testing | Accessibility | Techdebt (all flagging dimensions after C1)
Rule: <check ID such as Q2a or G6, or the dimension name>
Severity: Critical | High | Medium | Low (+ evidence when not the default)
Origin: introduced | pre-existing
Tags: none | any of deferred, co-located, multi, needs-user-decision
Register: none | TD-TBD, Ticket: TBD, Owner: TBD (the lead fills all three)

Evidence:
What was found, as the check's Evidence bullet names it, with a code snippet if relevant.

Impact:
What goes wrong if this is not addressed.

Recommended Fix:
Specific, actionable remediation (S2), with a code example if applicable.
```
