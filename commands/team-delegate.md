---
description: "Task delegation dashboard for managing team workload, assignments, rebalancing, and special-role coordination"
argument-hint: "[team-name] [--assign task-id=member-name] [--message member-name 'content'] [--rebalance] [--flush-docs]"
---

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Pre-flight

Parse args for team name and action flags:
- `--assign task-id=member-name`
- `--message member-name 'content'`
- `--rebalance`
- `--flush-docs`: immediately broadcast a doc-update checkpoint to team-doc-updater with current state

---

## Action: Assign Task

If `--assign` is provided:
1. Parse the `task-id=member-name` argument
2. Call TaskUpdate to set the owner field on the specified task
3. Call SendMessage to notify the member of their new assignment
4. Confirm assignment: "Task #{task-id} assigned to {member-name}."

---

## Action: Send Message

If `--message` is provided:
1. Parse member name and message content from args
2. Call SendMessage to that member with the provided content
3. Confirm: "Message sent to {member-name}."

---

## Action: Flush Docs

If `--flush-docs` is provided:
1. Call TaskList to read current task state
2. Compile a summary of: completed tasks, in-progress tasks, and any modified files mentioned in task notes
3. Call SendMessage to `team-doc-updater` (subagent_type: `podium/team-doc-updater`) with the summary and instruction: "Documentation checkpoint triggered manually. Please update docs based on the following state summary and confirm when done."
4. Confirm: "Doc flush sent to team-doc-updater."

---

## Action: Rebalance

If `--rebalance` is provided:
1. Call TaskList to get all tasks
2. For each implementer/reviewer/debugger member, count tasks with status `in_progress` or `pending` assigned to them
3. Identify idle members: 0 tasks assigned
4. Identify overloaded members: 3 or more tasks assigned
5. NOTE: `team-test-runner` and `team-doc-updater` are **exempt from rebalancing** — they are reactive agents, not task workers. Do not include them in workload counts or suggestions.
6. Generate rebalancing suggestions (e.g., move tasks from overloaded to idle implementers)
7. Display suggestions and ask user for confirmation before executing any TaskUpdate calls

---

## Default Dashboard

If no action flag is provided, display the delegation dashboard:

```
## Delegation Dashboard: {team-name}

### Unassigned Tasks
  #{id}  {subject}
  ...

### Member Workloads
  {name}   {role}             {N} tasks ({status breakdown})
  team-test-runner   [reactive: waiting for signals]
  team-doc-updater   [reactive: {N} updates pending / idle]

### Blocked Tasks
  #{id}  Blocked by #{id} (status: {status}, owner: {owner})

### Suggestions
  - Assign #{id} to {member} (idle)
  ...
```

> Tip: Use `/team-delegate --flush-docs` to trigger a documentation checkpoint at any time.
