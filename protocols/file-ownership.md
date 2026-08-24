Exclusive file ownership between members and the git red lines that keep a shared working tree safe.

Referenced by: `podium:team-spawn`, `podium:team-fable`.

## File Ownership Rules (lead)

1. **One owner per file** — Never assign the same file to multiple teammates.
2. **Explicit boundaries** — List owned files/directories in each task description.
3. **Interface contracts** — When teammates share boundaries, define the contract (types, APIs) before work begins.
4. **Shared files** — If a file must be touched by multiple teammates, the lead owns it and applies changes sequentially.

Where squads are used, work is split into squad-scoped work packages with **exclusive file ownership per squad**, and each squad gets its own worktree (see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`).

## File Ownership Protocol (member)

1. **Only modify files assigned to you** — Check your task description for the explicit list of owned files/directories.
2. **Never touch shared files** — If you need changes to a shared file, message the team lead.
3. **Create new files only within your ownership boundary** — New files in your assigned directories are fine.
4. **Interface contracts are immutable** — Do not change agreed-upon interfaces without team lead approval.
5. **If in doubt, ask** — Message the team lead before touching any file not explicitly in your ownership list.

## Git Red Lines (embed verbatim in every member prompt)

- NEVER run `git stash`, `git reset`, `git checkout --`, or `git clean` — teammates' uncommitted work being present in the tree is normal.
- Commit ONLY with explicit `git add <your-own-files>`. Never `git add -A` / `git add .`.
- Never touch files outside your ownership list. Never force-push.

## Conflict Resolution

- Detect overlapping file modifications across teammates; the lead mediates.
- Establish tiebreaking criteria for conflicting recommendations and ensure consistency across parallel workstreams.
