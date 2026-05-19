#!/usr/bin/env python3
"""Generate deterministic sample events for AgentOps Flight Recorder."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "sample_events"
OUT_FILE = OUT_DIR / "agentops_sample_sessions.jsonl"


@dataclass
class EventBuilder:
    base_time: datetime = datetime(2026, 5, 19, 12, 0, tzinfo=UTC)
    counter: int = 0
    rows: list[dict[str, Any]] = field(default_factory=list)

    def add(
        self,
        *,
        session_id: str,
        task_id: str,
        actor_type: str,
        actor_name: str,
        phase: str,
        event_type: str,
        status: str,
        risk_level: str,
        summary: str,
        human_approval_required: bool = False,
        tool: str | None = None,
        action: str | None = None,
        target: str | None = None,
        duration_ms: int | None = None,
        risk_reason: str | None = None,
        cost_usd_estimate: float | None = None,
        redaction_applied: bool | None = None,
        metadata: dict[str, str | int | float | bool | None] | None = None,
    ) -> None:
        self.counter += 1
        event_id = f"evt-{self.counter:04d}"
        row: dict[str, Any] = {
            "event_id": event_id,
            "timestamp": (self.base_time + timedelta(seconds=self.counter * 37)).isoformat().replace("+00:00", "Z"),
            "session_id": session_id,
            "task_id": task_id,
            "actor_type": actor_type,
            "actor_name": actor_name,
            "phase": phase,
            "event_type": event_type,
            "status": status,
            "risk_level": risk_level,
            "human_approval_required": human_approval_required,
            "summary": summary,
            "evidence_ref": event_id,
        }
        optional = {
            "tool": tool,
            "action": action,
            "target": target,
            "duration_ms": duration_ms,
            "risk_reason": risk_reason,
            "cost_usd_estimate": cost_usd_estimate,
            "redaction_applied": redaction_applied,
            "metadata": metadata,
        }
        for key, value in optional.items():
            if value is not None:
                row[key] = value
        self.rows.append(row)


def build_events() -> list[dict[str, Any]]:
    b = EventBuilder()

    session = "agent-session-prod-latency-001"
    task = "incident-api-latency"
    agent = "codex-sre-agent"

    b.add(
        session_id=session,
        task_id=task,
        actor_type="human",
        actor_name="incident-commander",
        phase="intake",
        event_type="task_start",
        status="info",
        risk_level="none",
        summary="Human opened incident investigation for API latency spike.",
        metadata={"severity": "sev2", "service": "checkout-api"},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="planning",
        event_type="plan_update",
        status="success",
        risk_level="low",
        summary="Agent proposed a read-only investigation plan before making changes.",
        metadata={"plan_steps": 4},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="tool_call",
        tool="shell",
        action="exec_command",
        target="logs/checkout-api",
        status="success",
        duration_ms=1840,
        risk_level="low",
        summary="Queried recent checkout-api error counts.",
        cost_usd_estimate=0.001,
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="tool_call",
        tool="shell",
        action="exec_command",
        target="logs/payment-worker",
        status="failed",
        duration_ms=60200,
        risk_level="medium",
        risk_reason="Query timed out after repeated broad search.",
        summary="Broad payment-worker query timed out.",
        cost_usd_estimate=0.004,
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="risk_signal",
        status="warning",
        risk_level="medium",
        risk_reason="Retry loop detected: same failing query pattern repeated.",
        summary="Detected retry loop around payment-worker log query.",
        metadata={"retry_count": 3},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="browser_action",
        tool="browser",
        action="open_dashboard",
        target="splunk-cloud-latency-dashboard",
        status="warning",
        duration_ms=3230,
        risk_level="medium",
        risk_reason="Browser profile account did not match expected incident account.",
        summary="Opened latency dashboard but found account/profile mismatch.",
        metadata={"expected_account": "incident-team", "observed_account": "personal-profile"},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="execution",
        event_type="tool_call",
        tool="shell",
        action="exec_command",
        target="prod/checkout-api",
        status="blocked",
        duration_ms=110,
        risk_level="critical",
        risk_reason="Destructive command pattern requires human approval.",
        human_approval_required=True,
        summary="Blocked attempted restart command before human approval.",
        metadata={"command_class": "service_restart"},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="risk_signal",
        status="warning",
        risk_level="high",
        risk_reason="Secret-like text detected in tool output and redacted.",
        summary="Redacted secret-like value from log excerpt before storage.",
        redaction_applied=True,
        metadata={"redaction_type": "api_key_like"},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="verification",
        event_type="ai_call",
        tool="llm",
        action="summarize_evidence",
        target="splunk_events",
        status="success",
        duration_ms=2460,
        risk_level="low",
        summary="Generated incident summary from cited event IDs only.",
        cost_usd_estimate=0.018,
        metadata={"cited_events": "evt-0003,evt-0004,evt-0005,evt-0006,evt-0007"},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="human",
        actor_name="incident-commander",
        phase="handoff",
        event_type="approval_gate",
        status="success",
        risk_level="low",
        summary="Human reviewed blocked restart and chose read-only rollback verification instead.",
        human_approval_required=True,
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="system",
        actor_name="agentops-recorder",
        phase="handoff",
        event_type="task_end",
        status="success",
        risk_level="none",
        summary="Incident investigation session closed with evidence trail preserved.",
        metadata={"events_recorded": 10},
    )

    session = "agent-session-docs-release-002"
    task = "release-readme-update"
    agent = "codex-release-agent"

    b.add(
        session_id=session,
        task_id=task,
        actor_type="human",
        actor_name="release-owner",
        phase="intake",
        event_type="task_start",
        status="info",
        risk_level="none",
        summary="Human requested README and release checklist update.",
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="execution",
        event_type="file_change",
        tool="git",
        action="edit_file",
        target="README.md",
        status="success",
        duration_ms=1380,
        risk_level="low",
        summary="Updated README with verified commands and screenshot links.",
        metadata={"files_changed": 1},
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="ai_agent",
        actor_name=agent,
        phase="verification",
        event_type="verification",
        tool="shell",
        action="run_command",
        target="npm run build",
        status="success",
        duration_ms=18200,
        risk_level="low",
        summary="Build passed before release handoff.",
        cost_usd_estimate=0.0,
    )
    b.add(
        session_id=session,
        task_id=task,
        actor_type="system",
        actor_name="agentops-recorder",
        phase="handoff",
        event_type="task_end",
        status="success",
        risk_level="none",
        summary="Release documentation session closed.",
        metadata={"events_recorded": 4},
    )

    return b.rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_events()
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} events to {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
