#!/usr/bin/env python3
"""Inspect and drain tmux-backed Claude agent teams safely.

Usage:
  python team_shutdown.py snapshot TEAM
  python team_shutdown.py status TEAM
  python team_shutdown.py drain TEAM --timeout 15
  python team_shutdown.py verify TEAM

Run snapshot before sending shutdown requests and before TeamDelete. The script
never deletes team/task metadata; the caller must use TeamDelete after drain.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

CLAUDE_HOME = Path.home() / ".claude"
SNAPSHOT_DIR = Path("/tmp/claude-team-shutdown")
SOCKET_DIR = Path(f"/tmp/tmux-{os.getuid()}")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def config_path(team: str) -> Path:
    return CLAUDE_HOME / "teams" / team / "config.json"


def snapshot_path(team: str) -> Path:
    return SNAPSHOT_DIR / f"{team}.json"


def read_config(team: str) -> dict:
    path = config_path(team)
    if not path.exists():
        raise RuntimeError(f"team config missing: {path}; run snapshot before TeamDelete")
    return json.loads(path.read_text())


def tmux_sockets() -> list[Path]:
    if not SOCKET_DIR.exists():
        return []
    return sorted(SOCKET_DIR.glob("claude-swarm-*"))


def list_panes(socket: Path) -> list[dict[str, str]]:
    fmt = "#{pane_id}\t#{pane_pid}\t#{pane_dead}\t#{pane_current_command}\t#{pane_title}\t#{pane_start_command}\t#{pane_current_path}"
    result = run("tmux", "-S", str(socket), "list-panes", "-a", "-F", fmt)
    if result.returncode != 0:
        return []

    panes = []
    for line in result.stdout.splitlines():
        fields = line.split("\t", 6)
        if len(fields) == 7:
            panes.append(
                dict(
                    zip(
                        ("id", "pid", "dead", "command", "title", "start", "cwd"),
                        fields,
                    )
                )
            )
    return panes


def inspect() -> dict[str, list[dict[str, str]]]:
    return {str(socket): list_panes(socket) for socket in tmux_sockets()}


def member_records(config: dict) -> list[dict[str, str]]:
    lead = config.get("leadAgentId")
    return [
        {
            "name": member["name"],
            "pane_id": member.get("tmuxPaneId", ""),
            "backend": member.get("backendType", ""),
            "agent_type": member.get("agentType", ""),
            "cwd": member.get("cwd", ""),
        }
        for member in config.get("members", [])
        if member.get("agentId") != lead and member.get("tmuxPaneId")
    ]


def _pane_matches_record(pane: dict[str, str], record: dict[str, str]) -> bool:
    """Require pane ID, agent-type title, and cwd to match the team record."""
    if pane["id"] != record["pane_id"]:
        return False
    agent_type = record.get("agent_type", "")
    title = pane.get("title", "")
    if not agent_type or agent_type not in title:
        return False
    expected_cwd = record.get("cwd", "")
    return not expected_cwd or pane.get("cwd") == expected_cwd


def classify_socket(
    records: list[dict[str, str]], state: dict[str, list[dict[str, str]]]
) -> dict:
    """Classify the team's socket as exclusive or mixed.

    Candidate panes must match the recorded pane ID, agent type in the pane title,
    and cwd. This disambiguates independent tmux servers that reuse pane IDs while
    remaining fail-closed when the stronger identity evidence is incomplete.
    """
    candidates = []
    for socket, panes in state.items():
        live = [pane for pane in panes if pane["dead"] != "1"]
        matched = sorted(
            pane["id"]
            for record in records
            for pane in live
            if _pane_matches_record(pane, record)
        )
        if matched:
            live_ids = sorted(pane["id"] for pane in live)
            candidates.append(
                (len(matched), set(live_ids) <= set(matched), socket, matched, live_ids)
            )

    if not candidates:
        return {
            "socket": None,
            "cleanup_mode": None,
            "target_panes": [],
            "outside_panes": [],
        }

    candidates.sort(reverse=True)
    best = candidates[0]
    tied = [item for item in candidates if item[0] == best[0]]
    if len(tied) != 1:
        details = [f"{item[2]} matched={item[3]} live={item[4]}" for item in tied]
        raise RuntimeError(
            "ambiguous tmux sockets after pane identity checks; refuse to kill:\n"
            + "\n".join(details)
        )

    socket = best[2]
    target_panes = best[3]
    all_live = best[4]
    outside_panes = sorted(set(all_live) - set(target_panes))
    cleanup_mode = "server" if not outside_panes else "pane"

    return {
        "socket": socket,
        "cleanup_mode": cleanup_mode,
        "target_panes": target_panes,
        "outside_panes": outside_panes,
    }


def save_snapshot(team: str) -> dict:
    config = read_config(team)
    records = member_records(config)
    state = inspect()
    classification = classify_socket(records, state)
    payload = {
        "team": team,
        "members": records,
        "socket": classification["socket"],
        "cleanup_mode": classification["cleanup_mode"],
        "target_panes": classification["target_panes"],
        "outside_panes": classification["outside_panes"],
        # backward-compatible alias for pre-mixed-socket consumers
        "matched_panes": classification["target_panes"],
    }
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path(team).write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def load_snapshot(team: str) -> dict:
    path = snapshot_path(team)
    if not path.exists():
        raise RuntimeError(f"shutdown snapshot missing: {path}; run snapshot first")
    return json.loads(path.read_text())


def live_team_panes(snapshot: dict) -> list[dict[str, str]]:
    socket_value = snapshot.get("socket")
    if not socket_value:
        return []
    # target_panes from mixed-socket snapshots; fall back to matched_panes for old snapshots
    target = set(
        snapshot.get("target_panes")
        or snapshot.get("matched_panes", [])
    )
    return [
        pane
        for pane in list_panes(Path(socket_value))
        if pane["id"] in target and pane["dead"] != "1"
    ]


def report(team: str, phase: str, snapshot: dict, live: list[dict[str, str]], ok: bool) -> int:
    output: dict = {
        "team": team,
        "phase": phase,
        "ok": ok,
        "socket": snapshot.get("socket"),
        "cleanup_mode": snapshot.get("cleanup_mode"),
        "target_panes": snapshot.get("target_panes", []),
        "outside_panes": snapshot.get("outside_panes", []),
        "live_panes": [
            {key: pane[key] for key in ("id", "pid", "command", "title")} for pane in live
        ],
    }
    print(json.dumps(output, indent=2))
    return 0 if ok else 1


def command_snapshot(team: str) -> int:
    snapshot = save_snapshot(team)
    live = live_team_panes(snapshot)
    return report(team, "snapshot", snapshot, live, True)


def command_status(team: str) -> int:
    snapshot = load_snapshot(team)
    live = live_team_panes(snapshot)
    return report(team, "status", snapshot, live, not live)


def _kill_target_panes(socket_value: str, target_panes: list[str]) -> list[str]:
    """Kill each target pane individually. Returns list of pane IDs that failed."""
    failures: list[str] = []
    for pane_id in target_panes:
        current_panes = list_panes(Path(socket_value))
        current_ids = {p["id"] for p in current_panes if p["dead"] != "1"}
        if pane_id not in current_ids:
            continue  # already exited naturally
        result = run("tmux", "-S", socket_value, "kill-pane", "-t", pane_id)
        if result.returncode != 0:
            failures.append(pane_id)
    return failures


# Keep any single invocation under the global 30s Bash timeout cap
# (see hooks/global-bash-safety); rerun drain if more waiting is needed.
MAX_DRAIN_TIMEOUT = 25


def command_drain(team: str, timeout: int) -> int:
    if timeout > MAX_DRAIN_TIMEOUT:
        print(
            json.dumps({"warning": f"--timeout clamped to {MAX_DRAIN_TIMEOUT}s "
                        "(30s Bash cap); rerun drain to keep waiting"}),
            file=sys.stderr,
        )
        timeout = MAX_DRAIN_TIMEOUT
    snapshot = load_snapshot(team)
    # normalize cleanup_mode for old snapshots that lack the field
    cleanup_mode = snapshot.get("cleanup_mode") or (
        "server" if snapshot.get("socket") else None
    )
    deadline = time.monotonic() + timeout
    live = live_team_panes(snapshot)
    while live and time.monotonic() < deadline:
        time.sleep(1)
        live = live_team_panes(snapshot)

    if live:
        socket_value = snapshot.get("socket")
        if not socket_value:
            raise RuntimeError("live panes found without a recorded socket")

        if cleanup_mode == "server":
            result = run("tmux", "-S", socket_value, "kill-server")
            if result.returncode != 0 and "no server running" not in result.stderr:
                raise RuntimeError(result.stderr.strip() or "tmux kill-server failed")
        elif cleanup_mode == "pane":
            target_panes = snapshot.get("target_panes") or snapshot.get("matched_panes", [])
            failures = _kill_target_panes(socket_value, target_panes)
            if failures:
                # report failure detail but continue; some panes may have been killed
                print(
                    json.dumps({"warning": "pane kill failures", "failed_panes": failures}),
                    file=sys.stderr,
                )
        else:
            raise RuntimeError(f"unknown cleanup_mode: {cleanup_mode}")

        live = live_team_panes(snapshot)

    return report(team, "drain", snapshot, live, not live)


def command_verify(team: str) -> int:
    snapshot = load_snapshot(team)
    live = live_team_panes(snapshot)
    metadata_exists = config_path(team).exists() or (CLAUDE_HOME / "tasks" / team).exists()
    ok = not live and not metadata_exists
    result = report(team, "verify", snapshot, live, ok)
    if metadata_exists:
        print("team/task metadata still exists", file=sys.stderr)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("snapshot", "status", "verify"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("team")
    drain = subparsers.add_parser("drain")
    drain.add_argument("team")
    drain.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()

    try:
        if args.command == "snapshot":
            return command_snapshot(args.team)
        if args.command == "status":
            return command_status(args.team)
        if args.command == "drain":
            return command_drain(args.team, args.timeout)
        return command_verify(args.team)
    except RuntimeError as error:
        print(
            json.dumps(
                {"team": args.team, "phase": args.command, "ok": False, "error": str(error)},
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
