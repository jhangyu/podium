Git worktree isolation per squad: creation, merge-and-re-verify, same-round cleanup, and the zero-residue check at task close.

Referenced by: `podium:team-fable`.

## Isolation

- Confirm the working directory is a git repository — worktree isolation requires it.
- Create **one git worktree per squad**. Squads never share a working tree.
- Every member prompt carries its worktree path alongside its file ownership list.

## Merge and Re-verify

- The orchestrator merges squad worktrees into the integration branch (or designates exactly one squad lead to do it), verifying content markers before and after merge.
- After merge verification, **re-run the round's acceptance tests on the integration branch** — in-worktree green does not prove the cross-squad combination works.

## Worktree Cleanup (mandatory, same round)

Once the round's work is merged and verified on the integration branch, the orchestrator removes every squad worktree:

- Before removal, check `git -C <worktree> status --porcelain` is empty. Uncommitted content present → STOP, identify the owner, and have it committed or explicitly discarded by decision — never silently deleted with the worktree.
- `git worktree remove <path>` per squad, then `git worktree prune`, then delete the squad branches already merged (`git branch -d`, never `-D`).
- Worktrees live exactly one round. Next round's squads get **fresh worktrees cut from the updated integration branch** — never a reused or stale worktree.

## Close the Task (after the final round)

1. Merge the integration branch back into `main` (regular merge, never force-push), then re-run the full acceptance suite **on `main`** — post-merge verification on the target branch is an independent gate, not a formality. The merge to `main` is performed only after the user has approved the final round's results.
2. Verify zero residue: `git worktree list` shows only the main tree; no leftover squad branches (`git branch --merged main` cleanup with `-d`); no stray `tmp/verify/` or detached processes.
3. Report the final state to the user: `main @ <hash>`, worktrees removed, branches deleted.
