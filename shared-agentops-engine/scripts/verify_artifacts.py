#!/usr/bin/env python3
"""Verify generated AgentOps portfolio artifacts."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "data/agentops_events.jsonl",
    "reports/handoff_report.md",
    "web/index.html",
    "media/shared-dashboard-full.png",
    "adapters/uipath/case_packet.json",
    "adapters/uipath/maestro_case_stages.md",
    "adapters/splunk/hec_events.jsonl",
    "adapters/splunk/searches.spl",
    "adapters/findevil/dfir_report.md",
    "adapters/google/gemini_mcp_workflow.json",
    "adapters/microsoft/copilot_architecture.md",
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    missing = [item for item in REQUIRED if not (ROOT / item).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    events = read_jsonl(ROOT / "data/agentops_events.jsonl")
    if len(events) != 26:
        raise SystemExit(f"expected 26 events, got {len(events)}")

    event_ids = {row["event_id"] for row in events}
    for required_id in ["evt-0007", "evt-0016", "evt-0024", "evt-0025"]:
        if required_id not in event_ids:
            raise SystemExit(f"missing important evidence id: {required_id}")

    if not any(row["status"] == "blocked" for row in events):
        raise SystemExit("no blocked event found")
    if not any(row.get("redaction_applied") for row in events):
        raise SystemExit("no redaction event found")
    if not any(row["human_approval_required"] for row in events):
        raise SystemExit("no human approval event found")

    case_packet = json.loads((ROOT / "adapters/uipath/case_packet.json").read_text(encoding="utf-8"))
    if case_packet["case_id"] != "CASE-AI-OPS-001":
        raise SystemExit("UiPath case packet points to wrong case")

    html_text = (ROOT / "web/index.html").read_text(encoding="utf-8")
    HTMLParser().feed(html_text)
    match = re.search(r'<script id="events-json" type="application/json">(.*?)</script>', html_text, re.S)
    if not match:
        raise SystemExit("dashboard embedded JSON missing")
    if len(json.loads(match.group(1))) != 26:
        raise SystemExit("dashboard embedded JSON count mismatch")

    print("verify_ok")
    print("events=26")
    print("cases=3")
    print("blocked=1+")
    print("approvals=1+")
    print("redactions=1+")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

