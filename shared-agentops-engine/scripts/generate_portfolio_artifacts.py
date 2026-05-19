#!/usr/bin/env python3
"""Generate the shared AgentOps prototype artifacts.

This script intentionally uses only the Python standard library so the portfolio
can be rebuilt on a fresh machine without dependency setup.
"""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
WEB_DIR = ROOT / "web"
ADAPTER_DIR = ROOT / "adapters"

EVENT_FILE = DATA_DIR / "agentops_events.jsonl"
DASHBOARD_FILE = WEB_DIR / "index.html"
HANDOFF_FILE = REPORT_DIR / "handoff_report.md"


REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "session_id",
    "task_id",
    "case_id",
    "actor_type",
    "actor_name",
    "phase",
    "event_type",
    "status",
    "risk_level",
    "human_approval_required",
    "summary",
    "evidence_ref",
}

ENUMS = {
    "actor_type": {"human", "ai_agent", "robot", "api", "system"},
    "phase": {
        "intake",
        "planning",
        "investigation",
        "evidence_collection",
        "risk_review",
        "approval",
        "execution",
        "verification",
        "handoff",
        "submission",
    },
    "event_type": {
        "task_start",
        "plan_update",
        "tool_call",
        "browser_action",
        "file_change",
        "robot_task",
        "api_call",
        "approval_gate",
        "ai_call",
        "risk_signal",
        "cost_signal",
        "evidence_captured",
        "verification",
        "handoff_report",
        "task_end",
    },
    "status": {"success", "warning", "blocked", "failed", "info"},
    "risk_level": {"none", "low", "medium", "high", "critical"},
    "decision": {"none", "approved", "rejected", "needs_more_evidence", "blocked_by_policy"},
}

RISK_WEIGHT = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


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
        case_id: str,
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
        decision: str = "none",
        redaction_applied: bool | None = None,
        metadata: dict[str, str | int | float | bool | None] | None = None,
    ) -> None:
        self.counter += 1
        event_id = f"evt-{self.counter:04d}"
        row: dict[str, Any] = {
            "event_id": event_id,
            "timestamp": (self.base_time + timedelta(seconds=self.counter * 41)).isoformat().replace("+00:00", "Z"),
            "session_id": session_id,
            "task_id": task_id,
            "case_id": case_id,
            "actor_type": actor_type,
            "actor_name": actor_name,
            "phase": phase,
            "event_type": event_type,
            "status": status,
            "risk_level": risk_level,
            "human_approval_required": human_approval_required,
            "decision": decision,
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

    case = "CASE-AI-OPS-001"
    session = "session-ai-ops-release-risk"
    task = "release-risk-review"
    agent = "codex-ops-agent"

    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="operations-lead",
        phase="intake",
        event_type="task_start",
        status="info",
        risk_level="none",
        summary="Human opened an AI-agent operations case after a release bot proposed a production change.",
        metadata={"lane": "uipath", "business_process": "release_exception_review"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="planning",
        event_type="plan_update",
        status="success",
        risk_level="low",
        summary="Agent created a read-only investigation plan with explicit approval gates before any production action.",
        metadata={"plan_steps": 5, "approval_gates": 2},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="robot",
        actor_name="uipath-evidence-robot",
        phase="evidence_collection",
        event_type="robot_task",
        tool="UiPath Robot",
        action="collect_release_context",
        target="change-ticket-7841",
        status="success",
        duration_ms=4800,
        risk_level="low",
        summary="Robot gathered the change ticket, linked pull request, deployment window, and service owner.",
        metadata={"records_collected": 4},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="api",
        actor_name="github-api",
        phase="evidence_collection",
        event_type="api_call",
        tool="GitHub API",
        action="read_pull_request",
        target="payments-service/pull/221",
        status="success",
        duration_ms=970,
        risk_level="low",
        cost_usd_estimate=0,
        summary="API confirmed the pull request touches payment retry behavior and has one approving review.",
        metadata={"files_changed": 8, "approvals": 1},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="tool_call",
        tool="shell",
        action="run_tests",
        target="payments-service retry tests",
        status="failed",
        duration_ms=53200,
        risk_level="medium",
        risk_reason="Regression test failed around duplicate retry suppression.",
        cost_usd_estimate=0.006,
        summary="Agent found a failing retry regression test that was not mentioned in the change ticket.",
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="risk_review",
        event_type="risk_signal",
        status="warning",
        risk_level="high",
        risk_reason="Production payment behavior change plus failing regression test.",
        summary="Case risk escalated because the proposed release affects payments and has failing verification.",
        metadata={"risk_rule": "payment_change_failed_test"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="execution",
        event_type="tool_call",
        tool="shell",
        action="deploy",
        target="production/payments-service",
        status="blocked",
        duration_ms=120,
        risk_level="critical",
        risk_reason="Production deployment is destructive and requires human approval.",
        human_approval_required=True,
        decision="blocked_by_policy",
        summary="Attempted production deployment was blocked by policy before execution.",
        metadata={"command_class": "production_deploy"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="operations-lead",
        phase="approval",
        event_type="approval_gate",
        status="success",
        risk_level="medium",
        human_approval_required=True,
        decision="needs_more_evidence",
        summary="Human requested more evidence instead of approving the production deployment.",
        metadata={"requested": "service_owner_signoff"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="robot",
        actor_name="uipath-evidence-robot",
        phase="evidence_collection",
        event_type="robot_task",
        tool="UiPath Robot",
        action="request_owner_signoff",
        target="payments-service owner",
        status="success",
        duration_ms=8200,
        risk_level="low",
        summary="Robot requested service-owner signoff and attached the failed test evidence.",
        metadata={"notification_channel": "case_queue"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="service-owner",
        phase="approval",
        event_type="approval_gate",
        status="success",
        risk_level="low",
        human_approval_required=True,
        decision="rejected",
        summary="Service owner rejected the release until the retry regression is fixed.",
        metadata={"release_decision": "hold"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="system",
        actor_name="agentops-recorder",
        phase="handoff",
        event_type="handoff_report",
        status="success",
        risk_level="none",
        summary="Generated a case handoff report with cited evidence IDs and final rejection decision.",
        metadata={"cited_events": "evt-0003,evt-0004,evt-0005,evt-0006,evt-0007,evt-0010"},
    )

    case = "CASE-DFIR-002"
    session = "session-dfir-phishing-response"
    task = "phishing-triage"
    agent = "dfir-analysis-agent"

    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="security-analyst",
        phase="intake",
        event_type="task_start",
        status="info",
        risk_level="none",
        summary="Security analyst opened a suspicious email investigation with attached endpoint telemetry.",
        metadata={"lane": "findevil", "source": "user_reported_email"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="planning",
        event_type="plan_update",
        status="success",
        risk_level="low",
        summary="Agent proposed an evidence-first DFIR plan: preserve artifacts, list hypotheses, then verify each claim.",
        metadata={"hypotheses": 3},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="robot",
        actor_name="sift-collector",
        phase="evidence_collection",
        event_type="evidence_captured",
        tool="SIFT workstation",
        action="capture_artifacts",
        target="mailbox and endpoint timeline",
        status="success",
        duration_ms=12300,
        risk_level="low",
        summary="Collected email headers, attachment hash, browser download timeline, and endpoint process list.",
        metadata={"artifacts": "headers,hash,timeline,processes"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="investigation",
        event_type="ai_call",
        tool="LLM",
        action="classify_evidence",
        target="artifact packet",
        status="warning",
        duration_ms=2210,
        risk_level="medium",
        risk_reason="Initial model answer overclaimed malware execution before process evidence was present.",
        cost_usd_estimate=0.012,
        summary="Agent generated an initial hypothesis but flagged one claim as unsupported by current evidence.",
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="risk_review",
        event_type="risk_signal",
        status="warning",
        risk_level="high",
        risk_reason="Unsupported certainty detected in analyst draft.",
        summary="System marked the draft finding as provisional because execution evidence was missing.",
        metadata={"self_correction": True},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="api",
        actor_name="threat-intel-api",
        phase="evidence_collection",
        event_type="api_call",
        tool="Threat Intel API",
        action="lookup_hash",
        target="sha256:9f2c-redacted",
        status="success",
        duration_ms=780,
        risk_level="medium",
        redaction_applied=True,
        summary="Hash lookup returned low-confidence phishing kit association; raw indicator was redacted in report output.",
        metadata={"confidence": "low"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="security-analyst",
        phase="approval",
        event_type="approval_gate",
        status="success",
        risk_level="low",
        human_approval_required=True,
        decision="approved",
        summary="Human approved containment of the reported message and requested no endpoint isolation.",
        metadata={"containment": "mailbox_only"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="system",
        actor_name="agentops-recorder",
        phase="handoff",
        event_type="handoff_report",
        status="success",
        risk_level="none",
        summary="Generated DFIR report with evidence IDs, unsupported claims, and human containment decision.",
        metadata={"report_type": "dfir"},
    )

    case = "CASE-CLOUD-003"
    session = "session-cloud-agent-workflow"
    task = "customer-support-knowledge-agent"
    agent = "gemini-ops-navigator"

    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="support-manager",
        phase="intake",
        event_type="task_start",
        status="info",
        risk_level="none",
        summary="Support manager requested an agent that answers customer questions and escalates uncertain cases.",
        metadata={"lane": "google,microsoft", "target_user": "support_manager"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="planning",
        event_type="plan_update",
        status="success",
        risk_level="low",
        summary="Agent created a workflow plan using retrieval, MCP tools, cost guardrails, and human escalation.",
        metadata={"mcp_tools": 3, "guardrails": 4},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="api",
        actor_name="knowledge-base-mcp",
        phase="evidence_collection",
        event_type="api_call",
        tool="MCP server",
        action="retrieve_policy",
        target="refund-policy",
        status="success",
        duration_ms=440,
        risk_level="low",
        cost_usd_estimate=0.001,
        summary="MCP retrieval returned the current refund policy and source URL for citation.",
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="execution",
        event_type="ai_call",
        tool="Gemini",
        action="draft_response",
        target="customer refund question",
        status="success",
        duration_ms=1980,
        risk_level="low",
        cost_usd_estimate=0.021,
        summary="Agent drafted a customer answer grounded in the retrieved refund policy.",
        metadata={"citations": "evt-0022"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="ai_agent",
        actor_name=agent,
        phase="risk_review",
        event_type="cost_signal",
        status="warning",
        risk_level="medium",
        risk_reason="Projected monthly model spend exceeded the manager's prototype budget.",
        cost_usd_estimate=4.82,
        summary="Cost guardrail warned that the high-quality model should be reserved for escalations.",
        metadata={"monthly_projection_usd": 143.6},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="human",
        actor_name="support-manager",
        phase="approval",
        event_type="approval_gate",
        status="success",
        risk_level="low",
        human_approval_required=True,
        decision="approved",
        summary="Human approved the workflow with a rule that expensive model calls are escalation-only.",
        metadata={"approved_budget_mode": "escalation_only"},
    )
    b.add(
        session_id=session,
        task_id=task,
        case_id=case,
        actor_type="system",
        actor_name="agentops-recorder",
        phase="handoff",
        event_type="task_end",
        status="success",
        risk_level="none",
        summary="Closed cloud-agent workflow case with source citations, cost guardrail, and human approval captured.",
        metadata={"submission_lanes": "google,microsoft"},
    )

    return b.rows


def ensure_dirs() -> None:
    for path in [
        DATA_DIR,
        REPORT_DIR,
        WEB_DIR,
        ADAPTER_DIR / "uipath",
        ADAPTER_DIR / "splunk",
        ADAPTER_DIR / "findevil",
        ADAPTER_DIR / "google",
        ADAPTER_DIR / "microsoft",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def validate_events(events: list[dict[str, Any]]) -> None:
    seen = set()
    for row in events:
        missing = REQUIRED_FIELDS - set(row)
        if missing:
            raise ValueError(f"{row.get('event_id', '<no id>')} missing fields: {sorted(missing)}")
        if row["event_id"] in seen:
            raise ValueError(f"duplicate event_id: {row['event_id']}")
        seen.add(row["event_id"])
        for key, allowed in ENUMS.items():
            if key in row and row[key] not in allowed:
                raise ValueError(f"{row['event_id']} invalid {key}: {row[key]}")


def group_cases(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in events:
        grouped[row["case_id"]].append(row)
    return dict(grouped)


def summarize_metrics(events: list[dict[str, Any]]) -> dict[str, Any]:
    cases = group_cases(events)
    risk_counter = Counter(row["risk_level"] for row in events)
    actor_counter = Counter(row["actor_type"] for row in events)
    event_counter = Counter(row["event_type"] for row in events)
    total_cost = round(sum(float(row.get("cost_usd_estimate", 0)) for row in events), 3)
    return {
        "event_count": len(events),
        "case_count": len(cases),
        "approval_count": sum(1 for row in events if row["human_approval_required"]),
        "blocked_count": sum(1 for row in events if row["status"] == "blocked"),
        "redaction_count": sum(1 for row in events if row.get("redaction_applied")),
        "high_or_critical_count": sum(1 for row in events if RISK_WEIGHT[row["risk_level"]] >= 3),
        "total_cost_usd_estimate": total_cost,
        "risk_counter": dict(risk_counter),
        "actor_counter": dict(actor_counter),
        "event_counter": dict(event_counter),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_canonical_events(events: list[dict[str, Any]]) -> None:
    write_jsonl(EVENT_FILE, events)


def case_title(case_id: str) -> str:
    return {
        "CASE-AI-OPS-001": "AI Agent Operations Exception Review",
        "CASE-DFIR-002": "Evidence-Locked Phishing Investigation",
        "CASE-CLOUD-003": "Human-Controlled Cloud Agent Workflow",
    }.get(case_id, case_id)


def max_risk(rows: list[dict[str, Any]]) -> str:
    return max((row["risk_level"] for row in rows), key=lambda r: RISK_WEIGHT[r])


def write_handoff_report(events: list[dict[str, Any]]) -> None:
    metrics = summarize_metrics(events)
    cases = group_cases(events)
    lines = [
        "# Human-AI Operations Control Plane Handoff Report",
        "",
        "Generated from the canonical event stream in `data/agentops_events.jsonl`.",
        "",
        "## Metrics",
        "",
        f"- Events recorded: {metrics['event_count']}",
        f"- Cases recorded: {metrics['case_count']}",
        f"- Human approval gates: {metrics['approval_count']}",
        f"- Blocked actions: {metrics['blocked_count']}",
        f"- High or critical risk signals: {metrics['high_or_critical_count']}",
        f"- Redactions applied: {metrics['redaction_count']}",
        f"- Estimated model/tool cost: ${metrics['total_cost_usd_estimate']}",
        "",
        "## Case Summaries",
        "",
    ]
    for case_id, rows in cases.items():
        approvals = [row for row in rows if row["human_approval_required"]]
        risks = [row for row in rows if RISK_WEIGHT[row["risk_level"]] >= 2]
        lines.extend(
            [
                f"### {case_id}: {case_title(case_id)}",
                "",
                f"- Max risk: {max_risk(rows)}",
                f"- Events: {len(rows)}",
                f"- Approval gates: {len(approvals)}",
                f"- Evidence IDs: {', '.join(row['event_id'] for row in rows)}",
                "",
                "Key facts:",
            ]
        )
        for row in rows:
            if row["event_type"] in {"risk_signal", "approval_gate", "handoff_report", "task_end"} or row["status"] == "blocked":
                lines.append(f"- `{row['event_id']}` {row['summary']}")
        if risks:
            lines.append("")
            lines.append("Risk notes:")
            for row in risks:
                reason = row.get("risk_reason", row["summary"])
                lines.append(f"- `{row['event_id']}` {row['risk_level']}: {reason}")
        lines.append("")
    HANDOFF_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dashboard_case_cards(cases: dict[str, list[dict[str, Any]]]) -> str:
    cards = []
    for case_id, rows in cases.items():
        approvals = sum(1 for row in rows if row["human_approval_required"])
        blocked = sum(1 for row in rows if row["status"] == "blocked")
        cost = sum(float(row.get("cost_usd_estimate", 0)) for row in rows)
        risks = [row for row in rows if RISK_WEIGHT[row["risk_level"]] >= 2]
        risk_items = "".join(
            f"<li><span>{html.escape(row['event_id'])}</span>{html.escape(row.get('risk_reason', row['summary']))}</li>"
            for row in risks[:4]
        )
        cards.append(
            f"""
            <article class="case-card">
              <div class="case-head">
                <div>
                  <p class="eyebrow">{html.escape(case_id)}</p>
                  <h3>{html.escape(case_title(case_id))}</h3>
                </div>
                <span class="risk risk-{html.escape(max_risk(rows))}">{html.escape(max_risk(rows))}</span>
              </div>
              <div class="case-metrics">
                <span>{len(rows)} events</span>
                <span>{approvals} approvals</span>
                <span>{blocked} blocked</span>
                <span>${cost:.3f}</span>
              </div>
              <ol class="risk-list">{risk_items}</ol>
            </article>
            """
        )
    return "\n".join(cards)


def dashboard_timeline(events: list[dict[str, Any]]) -> str:
    rows = []
    for row in events:
        rows.append(
            f"""
            <tr data-case="{html.escape(row['case_id'])}" data-risk="{html.escape(row['risk_level'])}">
              <td><code>{html.escape(row['event_id'])}</code></td>
              <td>{html.escape(row['phase'])}</td>
              <td>{html.escape(row['actor_type'])}<br><small>{html.escape(row['actor_name'])}</small></td>
              <td>{html.escape(row['event_type'])}</td>
              <td><span class="status status-{html.escape(row['status'])}">{html.escape(row['status'])}</span></td>
              <td><span class="risk risk-{html.escape(row['risk_level'])}">{html.escape(row['risk_level'])}</span></td>
              <td>{html.escape(row['summary'])}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def dashboard_stage_board(events: list[dict[str, Any]]) -> str:
    rows = group_cases(events)["CASE-AI-OPS-001"]
    stage_defs = [
        ("Intake", "Human opens the case", ["evt-0001"]),
        ("Agent Investigation", "AI agent plans and tests read-only", ["evt-0002", "evt-0005"]),
        ("Robot Evidence", "UiPath robot and APIs gather records", ["evt-0003", "evt-0004", "evt-0009"]),
        ("Risk Review", "Control plane escalates and blocks risk", ["evt-0006", "evt-0007"]),
        ("Human Approval", "Humans ask for evidence and reject release", ["evt-0008", "evt-0010"]),
        ("Handoff", "Report is generated from evidence IDs", ["evt-0011"]),
    ]
    by_id = {row["event_id"]: row for row in rows}
    cards = []
    for index, (name, description, ids) in enumerate(stage_defs, start=1):
        risk = max((by_id[event_id]["risk_level"] for event_id in ids), key=lambda r: RISK_WEIGHT[r])
        evidence = ", ".join(ids)
        cards.append(
            f"""
            <article class="stage-card">
              <div class="stage-index">{index}</div>
              <div>
                <h3>{html.escape(name)}</h3>
                <p>{html.escape(description)}</p>
                <code>{html.escape(evidence)}</code>
              </div>
              <span class="risk risk-{html.escape(risk)}">{html.escape(risk)}</span>
            </article>
            """
        )
    return "\n".join(cards)


def dashboard_approval_queue(events: list[dict[str, Any]]) -> str:
    approvals = [row for row in events if row["human_approval_required"]]
    items = []
    for row in approvals:
        decision = row.get("decision", "none").replace("_", " ")
        items.append(
            f"""
            <li>
              <div>
                <code>{html.escape(row['event_id'])}</code>
                <strong>{html.escape(row['actor_name'])}</strong>
                <p>{html.escape(row['summary'])}</p>
              </div>
              <span class="decision">{html.escape(decision)}</span>
            </li>
            """
        )
    return "\n".join(items)


def dashboard_adapter_links() -> str:
    adapters = [
        ("UiPath", "case_packet.json", "../adapters/uipath/case_packet.json"),
        ("Splunk", "hec_events.jsonl", "../adapters/splunk/hec_events.jsonl"),
        ("FIND EVIL", "dfir_report.md", "../adapters/findevil/dfir_report.md"),
        ("Google", "gemini_mcp_workflow.json", "../adapters/google/gemini_mcp_workflow.json"),
        ("Microsoft", "copilot_architecture.md", "../adapters/microsoft/copilot_architecture.md"),
    ]
    return "\n".join(
        f"""
        <a class="adapter-card" href="{html.escape(path)}">
          <span>{html.escape(name)}</span>
          <strong>{html.escape(file_name)}</strong>
        </a>
        """
        for name, file_name, path in adapters
    )


def write_dashboard(events: list[dict[str, Any]]) -> None:
    metrics = summarize_metrics(events)
    cases = group_cases(events)
    data_json = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Human-AI Operations Control Plane</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f7f8;
      --surface: #ffffff;
      --muted: #637074;
      --text: #172024;
      --border: #d7dee2;
      --brand: #0b6bcb;
      --ok: #0f7b51;
      --warn: #a05a00;
      --danger: #b42318;
      --critical: #6f1d1b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    header {{
      padding: 28px 32px 18px;
      background: #102027;
      color: white;
      border-bottom: 1px solid #20333b;
    }}
    header p {{ max-width: 920px; color: #c7d2d8; line-height: 1.55; }}
    h1 {{ margin: 0 0 10px; font-size: 34px; letter-spacing: 0; }}
    h2 {{ font-size: 20px; margin: 0 0 14px; }}
    h3 {{ margin: 0; font-size: 18px; }}
    p {{ line-height: 1.45; }}
    main {{ padding: 24px 32px 42px; }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(120px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .metric {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      min-height: 86px;
    }}
    .metric strong {{ display: block; font-size: 28px; margin-top: 8px; }}
    .metric span, .eyebrow, small {{ color: var(--muted); }}
    .case-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(240px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}
    .workbench-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(300px, .8fr);
      gap: 14px;
      margin-bottom: 24px;
    }}
    .stage-board, .approval-board, .adapter-board {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }}
    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(260px, 1fr));
      gap: 10px;
    }}
    .stage-card {{
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr) auto;
      gap: 10px;
      align-items: start;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      background: #fbfcfd;
    }}
    .stage-index {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: #eaf3ff;
      color: var(--brand);
      font-weight: 800;
    }}
    .stage-card p {{
      margin: 6px 0 8px;
      color: var(--muted);
      font-size: 14px;
    }}
    .approval-list {{
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 10px;
    }}
    .approval-list li {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      background: #fbfcfd;
    }}
    .approval-list p {{
      margin: 6px 0 0;
      color: #314046;
      font-size: 14px;
    }}
    .decision {{
      white-space: nowrap;
      color: var(--brand);
      font-weight: 800;
      font-size: 12px;
      text-transform: uppercase;
    }}
    .adapter-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(120px, 1fr));
      gap: 10px;
      margin-bottom: 24px;
    }}
    .adapter-card {{
      display: block;
      text-decoration: none;
      color: var(--text);
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
    }}
    .adapter-card span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 8px;
    }}
    .adapter-card strong {{
      display: block;
      overflow-wrap: anywhere;
    }}
    .case-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }}
    .case-head {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }}
    .eyebrow {{ margin: 0 0 6px; font-size: 12px; text-transform: uppercase; }}
    .case-metrics {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin: 14px 0;
    }}
    .case-metrics span {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 8px;
      background: #fafbfc;
      font-size: 13px;
    }}
    .risk-list {{ margin: 0; padding-left: 18px; }}
    .risk-list li {{ margin: 8px 0; color: #314046; }}
    .risk-list span {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-right: 6px; }}
    .panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .panel-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
    }}
    select {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 8px 10px;
      background: white;
      color: var(--text);
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 11px 12px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
    th {{ font-size: 12px; color: var(--muted); text-transform: uppercase; background: #f8fafb; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .risk, .status {{
      display: inline-block;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid transparent;
    }}
    .risk-none, .risk-low {{ color: var(--ok); background: #e8f5ef; border-color: #bce4d2; }}
    .risk-medium {{ color: var(--warn); background: #fff5df; border-color: #f5d38a; }}
    .risk-high {{ color: var(--danger); background: #fff0ed; border-color: #ffc9c0; }}
    .risk-critical {{ color: white; background: var(--critical); border-color: var(--critical); }}
    .status-success {{ color: var(--ok); background: #e8f5ef; }}
    .status-warning {{ color: var(--warn); background: #fff5df; }}
    .status-blocked, .status-failed {{ color: var(--danger); background: #fff0ed; }}
    .status-info {{ color: var(--brand); background: #eaf3ff; }}
    @media (max-width: 980px) {{
      .metric-grid, .case-grid {{ grid-template-columns: 1fr 1fr; }}
      .workbench-grid {{ grid-template-columns: 1fr; }}
      .adapter-grid {{ grid-template-columns: repeat(2, 1fr); }}
      table {{ font-size: 14px; }}
    }}
    @media (max-width: 680px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .metric-grid, .case-grid, .stage-grid, .adapter-grid {{ grid-template-columns: 1fr; }}
      th:nth-child(3), td:nth-child(3), th:nth-child(4), td:nth-child(4) {{ display: none; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Human-AI Operations Control Plane</h1>
    <p>One event stream for humans, AI agents, robots, APIs, approvals, risks, costs, and evidence. This is the shared prototype behind the UiPath, Splunk, FIND EVIL, Google Cloud, and Microsoft hackathon lanes.</p>
  </header>
  <main>
    <section class="metric-grid" aria-label="Metrics">
      <div class="metric"><span>Events</span><strong>{metrics['event_count']}</strong></div>
      <div class="metric"><span>Cases</span><strong>{metrics['case_count']}</strong></div>
      <div class="metric"><span>Approvals</span><strong>{metrics['approval_count']}</strong></div>
      <div class="metric"><span>Blocked</span><strong>{metrics['blocked_count']}</strong></div>
      <div class="metric"><span>High/Critical</span><strong>{metrics['high_or_critical_count']}</strong></div>
      <div class="metric"><span>Est. Cost</span><strong>${metrics['total_cost_usd_estimate']}</strong></div>
    </section>
    <section class="workbench-grid" aria-label="UiPath case workbench">
      <div class="stage-board">
        <h2>UiPath Case Workbench</h2>
        <div class="stage-grid">
          {dashboard_stage_board(events)}
        </div>
      </div>
      <aside class="approval-board">
        <h2>Human Approval Queue</h2>
        <ul class="approval-list">
          {dashboard_approval_queue(events)}
        </ul>
      </aside>
    </section>
    <section aria-label="Adapter outputs">
      <h2>Contest Adapters</h2>
      <div class="adapter-grid">
        {dashboard_adapter_links()}
      </div>
    </section>
    <section class="case-grid" aria-label="Cases">
      {dashboard_case_cards(cases)}
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>Event Timeline</h2>
        <label>Case
          <select id="caseFilter">
            <option value="all">All cases</option>
            {''.join(f'<option value="{html.escape(case_id)}">{html.escape(case_id)}</option>' for case_id in cases)}
          </select>
        </label>
      </div>
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Phase</th>
            <th>Actor</th>
            <th>Type</th>
            <th>Status</th>
            <th>Risk</th>
            <th>Summary</th>
          </tr>
        </thead>
        <tbody id="timelineBody">
          {dashboard_timeline(events)}
        </tbody>
      </table>
    </section>
  </main>
  <script id="events-json" type="application/json">{data_json}</script>
  <script>
    const filter = document.getElementById('caseFilter');
    const rows = Array.from(document.querySelectorAll('#timelineBody tr'));
    filter.addEventListener('change', () => {{
      const value = filter.value;
      rows.forEach((row) => {{
        row.style.display = value === 'all' || row.dataset.case === value ? '' : 'none';
      }});
    }});
  </script>
</body>
</html>
"""
    DASHBOARD_FILE.write_text(html_text, encoding="utf-8")


def write_uipath_adapter(events: list[dict[str, Any]]) -> None:
    rows = group_cases(events)["CASE-AI-OPS-001"]
    stages = [
        {
            "stage": "Intake",
            "owner": "Human",
            "evidence_events": [row["event_id"] for row in rows if row["phase"] == "intake"],
        },
        {
            "stage": "Agent Investigation",
            "owner": "AI Agent",
            "evidence_events": [row["event_id"] for row in rows if row["actor_type"] == "ai_agent" and row["phase"] in {"planning", "investigation"}],
        },
        {
            "stage": "Robot/API Evidence Collection",
            "owner": "UiPath Robot + APIs",
            "evidence_events": [row["event_id"] for row in rows if row["phase"] == "evidence_collection"],
        },
        {
            "stage": "Risk Review",
            "owner": "Control Plane",
            "evidence_events": [row["event_id"] for row in rows if row["phase"] == "risk_review" or row["status"] == "blocked"],
        },
        {
            "stage": "Human Approval",
            "owner": "Action Center",
            "evidence_events": [row["event_id"] for row in rows if row["human_approval_required"]],
        },
        {
            "stage": "Handoff",
            "owner": "Recorder",
            "evidence_events": [row["event_id"] for row in rows if row["phase"] == "handoff"],
        },
    ]
    packet = {
        "case_id": "CASE-AI-OPS-001",
        "case_name": case_title("CASE-AI-OPS-001"),
        "recommended_uipath_track": "Maestro Case",
        "current_status": "release_rejected_until_evidence_fixed",
        "max_risk": max_risk(rows),
        "stages": stages,
        "events": rows,
    }
    (ADAPTER_DIR / "uipath" / "case_packet.json").write_text(
        json.dumps(packet, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# UiPath Maestro Case Stages",
        "",
        "This is the P0 flagship packaging of the shared event stream.",
        "",
    ]
    for i, stage in enumerate(stages, start=1):
        lines.extend(
            [
                f"## {i}. {stage['stage']}",
                "",
                f"- Owner: {stage['owner']}",
                f"- Evidence events: {', '.join(stage['evidence_events']) or 'none'}",
                "",
            ]
        )
    (ADAPTER_DIR / "uipath" / "maestro_case_stages.md").write_text("\n".join(lines), encoding="utf-8")


def write_splunk_adapter(events: list[dict[str, Any]]) -> None:
    hec_rows = [
        {
            "time": row["timestamp"],
            "sourcetype": "agentops:json",
            "source": "human-ai-operations-control-plane",
            "event": row,
        }
        for row in events
    ]
    write_jsonl(ADAPTER_DIR / "splunk" / "hec_events.jsonl", hec_rows)
    searches = """# AgentOps Flight Recorder SPL Searches

# Timeline by case
index=agentops sourcetype="agentops:json"
| sort 0 _time
| table _time event.case_id event.event_id event.phase event.actor_type event.actor_name event.event_type event.status event.risk_level event.summary

# High-risk or blocked actions
index=agentops sourcetype="agentops:json" (event.risk_level="high" OR event.risk_level="critical" OR event.status="blocked")
| table _time event.case_id event.event_id event.risk_level event.status event.risk_reason event.summary

# Human approval queue
index=agentops sourcetype="agentops:json" event.human_approval_required=true
| table _time event.case_id event.event_id event.actor_name event.decision event.summary

# Estimated model/tool cost by case
index=agentops sourcetype="agentops:json"
| stats sum(event.cost_usd_estimate) as estimated_cost by event.case_id
| sort - estimated_cost
"""
    (ADAPTER_DIR / "splunk" / "searches.spl").write_text(searches, encoding="utf-8")


def write_findevil_adapter(events: list[dict[str, Any]]) -> None:
    rows = group_cases(events)["CASE-DFIR-002"]
    lines = [
        "# Evidence-Locked DFIR Agent Report",
        "",
        "This report is generated only from recorded events. It intentionally distinguishes hypotheses from verified facts.",
        "",
        "## Executive Summary",
        "",
        "- A suspicious email investigation was opened by a human analyst.",
        "- Evidence was collected from email headers, attachment hash, browser timeline, and endpoint process list.",
        "- The AI agent self-corrected an unsupported malware-execution claim.",
        "- Human-approved containment was mailbox-only; endpoint isolation was not approved.",
        "",
        "## Evidence Chain",
        "",
    ]
    for row in rows:
        lines.append(f"- `{row['event_id']}` {row['timestamp']} {row['actor_name']}: {row['summary']}")
    lines.extend(
        [
            "",
            "## Hypotheses And Status",
            "",
            "| Hypothesis | Status | Evidence |",
            "|---|---|---|",
            "| The email is a phishing attempt. | Supported at low-to-medium confidence. | `evt-0014`, `evt-0017` |",
            "| Malware executed on the endpoint. | Not supported by current evidence. | `evt-0015`, `evt-0016` |",
            "| Mailbox-only containment is enough for this case. | Human-approved decision. | `evt-0018` |",
            "",
            "## Analyst Guardrail",
            "",
            "The agent may suggest hypotheses, but the final report must cite event IDs and mark unsupported claims instead of presenting them as fact.",
            "",
        ]
    )
    (ADAPTER_DIR / "findevil" / "dfir_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_google_adapter(events: list[dict[str, Any]]) -> None:
    rows = group_cases(events)["CASE-CLOUD-003"]
    workflow = {
        "name": "Gemini Operations Navigator",
        "hackathon": "Google Cloud Rapid Agent Hackathon",
        "case_id": "CASE-CLOUD-003",
        "goal": "Use Gemini and MCP tools to answer support questions under human-controlled cost and escalation guardrails.",
        "mcp_tools": [
            {"name": "knowledge-base-mcp", "purpose": "retrieve current policy source material", "evidence": ["evt-0022"]},
            {"name": "ticketing-mcp", "purpose": "create escalation task when uncertainty is high", "evidence": []},
            {"name": "cost-guardrail-mcp", "purpose": "choose model tier and stop expensive loops", "evidence": ["evt-0024"]},
        ],
        "human_control_points": [row["event_id"] for row in rows if row["human_approval_required"]],
        "risk_events": [row["event_id"] for row in rows if RISK_WEIGHT[row["risk_level"]] >= 2],
        "events": rows,
    }
    (ADAPTER_DIR / "google" / "gemini_mcp_workflow.json").write_text(
        json.dumps(workflow, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_microsoft_adapter(events: list[dict[str, Any]]) -> None:
    rows = group_cases(events)["CASE-CLOUD-003"]
    lines = [
        "# Human-AI Handoff Copilot Architecture",
        "",
        "Target: Microsoft Agent Academy Hackathon",
        "",
        "## User",
        "",
        "A support manager who wants AI assistance without losing control over cost, escalation, policy accuracy, or final customer communication.",
        "",
        "## Components",
        "",
        "- Copilot-style conversational intake",
        "- Knowledge retrieval from approved policy sources",
        "- Adaptive-card approval gate for escalations and high-cost model calls",
        "- AgentOps event stream for auditability",
        "- Handoff report with event IDs and source citations",
        "",
        "## Data Flow",
        "",
        "1. User asks a customer-support question.",
        "2. Agent retrieves policy evidence before drafting an answer.",
        "3. Risk and cost guardrails evaluate the draft.",
        "4. Human approval is required when uncertainty, policy risk, or cost exceeds the threshold.",
        "5. Final answer and handoff report cite event IDs.",
        "",
        "## Evidence From Prototype",
        "",
    ]
    for row in rows:
        lines.append(f"- `{row['event_id']}` {row['summary']}")
    (ADAPTER_DIR / "microsoft" / "copilot_architecture.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all(events: list[dict[str, Any]]) -> None:
    ensure_dirs()
    validate_events(events)
    write_canonical_events(events)
    write_handoff_report(events)
    write_dashboard(events)
    write_uipath_adapter(events)
    write_splunk_adapter(events)
    write_findevil_adapter(events)
    write_google_adapter(events)
    write_microsoft_adapter(events)


def main() -> int:
    events = build_events()
    write_all(events)
    metrics = summarize_metrics(events)
    print(json.dumps({"status": "ok", **metrics}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
