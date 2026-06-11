#!/usr/bin/env python3
"""Build the Splunk-focused AgentOps Flight Recorder demo dashboard."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = ROOT.parent / "shared-agentops-engine"
HEC_FILE = SHARED_ROOT / "adapters" / "splunk" / "hec_events.jsonl"
SPL_FILE = SHARED_ROOT / "adapters" / "splunk" / "searches.spl"
OUT_FILE = ROOT / "prototype" / "flight-recorder-dashboard.html"
PANELS_FILE = ROOT / "reports" / "splunk-dashboard-panels.md"

RISK_WEIGHT = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def read_hec_events() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in HEC_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line)["event"])
    return rows


def risk_class(risk: str) -> str:
    if risk in {"critical", "high"}:
        return "danger"
    if risk == "medium":
        return "warn"
    if risk == "low":
        return "ok"
    return "quiet"


def grouped_cases(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_case[event["case_id"]].append(event)

    cases: list[dict[str, Any]] = []
    for case_id, case_events in by_case.items():
        max_risk = max(case_events, key=lambda row: RISK_WEIGHT[row["risk_level"]])["risk_level"]
        approvals = sum(1 for event in case_events if event.get("human_approval_required"))
        blocked = sum(1 for event in case_events if event["status"] == "blocked")
        cost = sum(float(event.get("cost_usd_estimate", 0) or 0) for event in case_events)
        cases.append(
            {
                "case_id": case_id,
                "events": len(case_events),
                "max_risk": max_risk,
                "approvals": approvals,
                "blocked": blocked,
                "cost": round(cost, 4),
                "summary": case_events[-1]["summary"],
            }
        )
    return sorted(cases, key=lambda row: (RISK_WEIGHT[row["max_risk"]], row["events"]), reverse=True)


def build_case_cards(cases: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"""
        <article class="case-card {risk_class(case["max_risk"])}">
          <div class="case-topline">
            <span class="case-id">{esc(case["case_id"])}</span>
            <span class="risk-pill {risk_class(case["max_risk"])}">{esc(case["max_risk"])}</span>
          </div>
          <p>{esc(case["summary"])}</p>
          <div class="case-stats">
            <span>{case["events"]} events</span>
            <span>{case["approvals"]} approvals</span>
            <span>{case["blocked"]} blocked</span>
            <span>${case["cost"]:.4f}</span>
          </div>
        </article>
        """
        for case in cases
    )


def build_timeline(events: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for event in sorted(events, key=lambda row: row["timestamp"]):
        risk_weight = RISK_WEIGHT[event["risk_level"]]
        approval = "yes" if event.get("human_approval_required") else "no"
        rows.append(
            f"""
            <article class="timeline-row" data-risk-weight="{risk_weight}" data-approval="{approval}" data-case="{esc(event["case_id"])}">
              <div>
                <span class="event-id">{esc(event["event_id"])}</span>
                <span class="subtle">{esc(event["case_id"])}</span>
              </div>
              <div class="timeline-main">
                <strong>{esc(event["event_type"])}</strong>
                <span>{esc(event["actor_type"])} / {esc(event["actor_name"])}</span>
                <p>{esc(event["summary"])}</p>
              </div>
              <span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span>
            </article>
            """
        )
    return "\n".join(rows)


def build_high_risk_rows(events: list[dict[str, Any]]) -> str:
    high_risk = [
        event
        for event in events
        if event["risk_level"] in {"medium", "high", "critical"} or event["status"] == "blocked"
    ]
    return "\n".join(
        f"""
        <tr>
          <td><span class="event-id">{esc(event["event_id"])}</span></td>
          <td>{esc(event["case_id"])}</td>
          <td><span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span></td>
          <td>{esc(event["status"])}</td>
          <td>{esc(event.get("risk_reason", event["summary"]))}</td>
        </tr>
        """
        for event in high_risk
    )


def build_approval_rows(events: list[dict[str, Any]]) -> str:
    approvals = [
        event
        for event in events
        if event.get("human_approval_required") or event.get("decision") not in {None, "none"}
    ]
    return "\n".join(
        f"""
        <tr>
          <td><span class="event-id">{esc(event["event_id"])}</span></td>
          <td>{esc(event["case_id"])}</td>
          <td>{esc(event.get("decision", "none"))}</td>
          <td>{esc(event["summary"])}</td>
        </tr>
        """
        for event in approvals
    )


def build_spl_blocks() -> str:
    raw = SPL_FILE.read_text(encoding="utf-8")
    blocks = [block.strip() for block in raw.split("\n\n") if block.strip()]
    cards: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        title = lines[0].replace("#", "").strip()
        query = "\n".join(lines[1:]).strip()
        if not query:
            continue
        cards.append(
            f"""
            <article class="spl-card">
              <h3>{esc(title)}</h3>
              <pre>{esc(query)}</pre>
            </article>
            """
        )
    return "\n".join(cards)


def build_judge_cards() -> str:
    cards = [
        (
            "Who",
            "SRE, platform, security, and operations teams that let AI agents touch tickets, tools, APIs, and release workflows.",
        ),
        (
            "Pain",
            "After a bad action, a chat transcript is not enough. Teams need to search what the agent did, where risk appeared, and who approved the next step.",
        ),
        (
            "AI Use",
            "The AI investigator is evidence-bound: it summarizes only from event IDs and SPL result rows, then asks a human to approve, reject, or hand off.",
        ),
        (
            "Value",
            "Agent work becomes Splunk-ready operational evidence instead of an unreviewable conversation.",
        ),
    ]
    return "\n".join(
        "\n".join(
            [
                '        <article class="judge-card">',
                f"          <strong>{esc(title)}</strong>",
                f"          <p>{esc(body)}</p>",
                "        </article>",
            ]
        )
        for title, body in cards
    )


def build_demo_events_json(events: list[dict[str, Any]]) -> str:
    compact_events = [
        {
            "event_id": event["event_id"],
            "case_id": event["case_id"],
            "risk_level": event["risk_level"],
            "status": event["status"],
            "summary": event["summary"],
            "decision": event.get("decision", "none"),
            "approval": bool(event.get("human_approval_required")),
            "cost": float(event.get("cost_usd_estimate", 0) or 0),
        }
        for event in events
    ]
    return json.dumps(compact_events, ensure_ascii=False)


def build_html(events: list[dict[str, Any]]) -> str:
    cases = grouped_cases(events)
    actors = Counter(event["actor_type"] for event in events)
    approval_count = sum(1 for event in events if event.get("human_approval_required"))
    blocked_count = sum(1 for event in events if event["status"] == "blocked")
    redaction_count = sum(1 for event in events if event.get("redaction_applied"))
    risk_count = sum(1 for event in events if event["risk_level"] in {"medium", "high", "critical"})
    total_cost = sum(float(event.get("cost_usd_estimate", 0) or 0) for event in events)
    case_cards = build_case_cards(cases)
    high_risk_rows = build_high_risk_rows(events)
    approval_rows = build_approval_rows(events)
    timeline = build_timeline(events)
    spl_blocks = build_spl_blocks()
    judge_cards = build_judge_cards()
    demo_events_json = build_demo_events_json(events)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AgentOps Flight Recorder — Splunk Demo</title>
  <style>
    :root {{
      --bg: #f5f7f8;
      --surface: #ffffff;
      --ink: #14212b;
      --muted: #64717d;
      --line: #d7e0e6;
      --brand: #0b6b4f;
      --brand-soft: #e7f5ef;
      --accent: #2251a4;
      --ok: #087443;
      --ok-soft: #e7f7ee;
      --warn: #b54708;
      --warn-soft: #fff3df;
      --danger: #b42318;
      --danger-soft: #ffebe9;
      --quiet: #edf1f4;
      --shadow: 0 16px 36px rgba(20, 33, 43, 0.08);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}

    .locator {{
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .hero {{
      background: linear-gradient(135deg, #143226, #153247);
      color: #fff;
      border-radius: 8px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(260px, 0.75fr);
      gap: 24px;
    }}

    .judge-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 14px 0 18px;
    }}

    .judge-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      box-shadow: 0 8px 20px rgba(20, 33, 43, 0.05);
      min-height: 150px;
    }}

    .judge-card strong {{
      display: block;
      color: var(--brand);
      font-size: 15px;
      margin-bottom: 8px;
    }}

    .judge-card p {{
      margin: 0;
      color: var(--ink);
      font-size: 14px;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
    }}

    h2 {{
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }}

    h3 {{
      margin: 0 0 8px;
      font-size: 16px;
      letter-spacing: 0;
    }}

    p {{
      margin: 0;
    }}

    .hero-copy {{
      margin-top: 14px;
      color: #d7e9e3;
      font-size: 16px;
      max-width: 740px;
    }}

    .query-card {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      padding: 16px;
    }}

    .query-card code {{
      display: block;
      color: #d9f5e8;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      white-space: pre-wrap;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}

    .metric,
    .section,
    .case-card,
    .spl-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(20, 33, 43, 0.04);
    }}

    .metric {{
      padding: 16px;
      min-height: 108px;
    }}

    .metric strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      margin-bottom: 8px;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 13px;
    }}

    .section {{
      margin-top: 22px;
      padding: 20px;
    }}

    .demo-runner {{
      border: 2px solid rgba(11, 107, 79, 0.32);
      background: #fbfefd;
    }}

    .control-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 10px 0 14px;
    }}

    .control-row button {{
      appearance: none;
      border: 1px solid var(--brand);
      background: var(--brand);
      color: #fff;
      font: inherit;
      font-weight: 700;
      border-radius: 6px;
      padding: 10px 14px;
      cursor: pointer;
    }}

    .control-row button.secondary {{
      color: var(--brand);
      background: #fff;
    }}

    .demo-output {{
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
      padding: 14px;
    }}

    .demo-output pre {{
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      background: #101820;
      color: #e7f5ef;
      border-radius: 6px;
      padding: 12px;
      min-height: 170px;
      max-height: 310px;
      overflow: auto;
      font-size: 13px;
    }}

    .ai-panel {{
      border-left: 4px solid var(--brand);
      padding-left: 14px;
    }}

    .ai-panel h3 {{
      margin: 0 0 8px;
      font-size: 18px;
    }}

    .ai-panel ul {{
      margin: 8px 0 0;
      padding-left: 20px;
    }}

    .case-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .case-card {{
      padding: 16px;
      min-height: 188px;
    }}

    .case-card.danger {{
      border-color: #f2aaa4;
      background: linear-gradient(180deg, #fff, #fff7f6);
    }}

    .case-card.warn {{
      border-color: #ffd49b;
      background: linear-gradient(180deg, #fff, #fffaf2);
    }}

    .case-card.ok {{
      border-color: #a9dec5;
      background: linear-gradient(180deg, #fff, #f8fdf9);
    }}

    .case-topline {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      margin-bottom: 12px;
    }}

    .case-id,
    .event-id {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}

    .case-stats {{
      margin-top: 14px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      color: var(--muted);
      font-size: 12px;
    }}

    .case-stats span {{
      background: var(--quiet);
      border-radius: 999px;
      padding: 4px 8px;
    }}

    .risk-pill {{
      display: inline-flex;
      align-items: center;
      width: fit-content;
      min-height: 24px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .risk-pill.danger {{
      color: var(--danger);
      background: var(--danger-soft);
    }}

    .risk-pill.warn {{
      color: var(--warn);
      background: var(--warn-soft);
    }}

    .risk-pill.ok {{
      color: var(--ok);
      background: var(--ok-soft);
    }}

    .risk-pill.quiet {{
      color: var(--muted);
      background: var(--quiet);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}

    th {{
      color: var(--muted);
      font-size: 12px;
      text-align: left;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
    }}

    td {{
      border-bottom: 1px solid var(--line);
      padding: 12px 8px;
      vertical-align: top;
    }}

    .two-col {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 16px;
    }}

    .spl-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}

    .spl-card {{
      padding: 16px;
      overflow: hidden;
    }}

    pre {{
      margin: 0;
      padding: 12px;
      background: #101820;
      color: #d8f3dc;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 12px;
      line-height: 1.45;
    }}

    .timeline {{
      display: grid;
      gap: 10px;
    }}

    .timeline-row {{
      display: grid;
      grid-template-columns: 190px minmax(0, 1fr) 92px;
      gap: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
      align-items: start;
    }}

    .timeline-main {{
      display: grid;
      gap: 4px;
    }}

    .timeline-main span,
    .timeline-main p,
    .subtle {{
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 940px) {{
      .hero,
      .two-col {{
        grid-template-columns: 1fr;
      }}

      .metrics,
      .case-grid,
      .judge-grid,
      .spl-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .demo-output {{
        grid-template-columns: 1fr;
      }}

      .timeline-row {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 620px) {{
      main {{
        padding: 16px 12px 32px;
      }}

      h1 {{
        font-size: 27px;
      }}

      .metrics,
      .case-grid,
      .judge-grid,
      .spl-grid {{
        grid-template-columns: 1fr;
      }}

      table {{
        display: block;
        overflow-x: auto;
        white-space: nowrap;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="locator">Splunk Agentic Ops · AgentOps Flight Recorder · Demo Artifact</div>

    <section class="hero">
      <div>
        <h1>Help ops teams investigate what AI agents actually did.</h1>
        <p class="hero-copy">
          AgentOps Flight Recorder is for SRE, platform, security, and operations teams that need
          an audit trail when AI agents run tools. It turns agent actions into Splunk-ready evidence
          and uses evidence-bound AI to explain the incident without inventing facts.
        </p>
      </div>
      <aside class="query-card">
        <code>index=agentops sourcetype="agentops:json"
| sort 0 _time
| table _time event.case_id event.event_id event.risk_level event.status event.summary</code>
      </aside>
    </section>

    <section class="judge-grid" aria-label="Judge quick answer">
      {judge_cards}
    </section>

    <section class="metrics">
      <div class="metric"><strong>{len(events)}</strong><span>Splunk-ready AgentOps events</span></div>
      <div class="metric"><strong>{len(cases)}</strong><span>cases reconstructed from event trails</span></div>
      <div class="metric"><strong>{risk_count}</strong><span>medium/high/critical risk events</span></div>
      <div class="metric"><strong>{approval_count}</strong><span>human approval gates</span></div>
      <div class="metric"><strong>${total_cost:.2f}</strong><span>estimated model/tool spend in sample</span></div>
    </section>

    <section class="section demo-runner" id="demo-runner">
      <h2>Run The Review Flow</h2>
      <p>
        This is the working prototype path: load event evidence, narrow to risk or approvals,
        run a Splunk-style search, then generate an evidence-bound AI investigation draft.
      </p>
      <div class="control-row">
        <button type="button" data-demo-filter="all">Load All Events</button>
        <button type="button" data-demo-filter="risk">Show Risky Events</button>
        <button type="button" data-demo-filter="approval">Show Approval Gates</button>
        <button class="secondary" type="button" data-demo-spl>Run SPL Search</button>
        <button class="secondary" type="button" data-demo-ai>Generate AI Summary</button>
      </div>
      <div class="demo-output">
        <pre id="demo-query-output">index=agentops sourcetype="agentops:json"
| sort 0 _time
| table _time event.case_id event.event_id event.risk_level event.status event.summary</pre>
        <div class="ai-panel" id="demo-ai-output">
          <h3>Evidence-Bound AI Investigator</h3>
          <p>Choose a filter or run the AI summary. The assistant is constrained to cite event IDs from the evidence trail.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Case Overview</h2>
      <div class="case-grid">{case_cards}</div>
    </section>

    <section class="section two-col">
      <div>
        <h2>High-Risk And Blocked Actions</h2>
        <table>
          <thead>
            <tr>
              <th>Event</th>
              <th>Case</th>
              <th>Risk</th>
              <th>Status</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>{high_risk_rows}</tbody>
        </table>
      </div>
      <div>
        <h2>Human Approval Queue</h2>
        <table>
          <thead>
            <tr>
              <th>Event</th>
              <th>Case</th>
              <th>Decision</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>{approval_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>Saved SPL Searches</h2>
      <div class="spl-grid">{spl_blocks}</div>
    </section>

    <section class="section">
      <h2>Evidence Timeline</h2>
      <div class="timeline">{timeline}</div>
    </section>
  </main>
  <script>
    const EVENTS = {demo_events_json};
    const output = document.getElementById('demo-query-output');
    const aiOutput = document.getElementById('demo-ai-output');
    const timelineRows = [...document.querySelectorAll('.timeline-row')];

    const visibleEvents = () => timelineRows
      .filter((row) => row.style.display !== 'none')
      .map((row) => row.querySelector('.event-id').textContent.trim());

    function setTimelineFilter(mode) {{
      let count = 0;
      timelineRows.forEach((row) => {{
        const riskWeight = Number(row.dataset.riskWeight || '0');
        const approval = row.dataset.approval === 'yes';
        const show = mode === 'all' || (mode === 'risk' && riskWeight >= 2) || (mode === 'approval' && approval);
        row.style.display = show ? '' : 'none';
        if (show) count += 1;
      }});
      const label = mode === 'all' ? 'all events' : mode === 'risk' ? 'medium/high/critical or blocked events' : 'approval gates';
      output.textContent = `Loaded ${{count}} ${{label}} from the AgentOps event trail.\\n\\nVisible event IDs: ${{visibleEvents().join(', ')}}`;
      aiOutput.innerHTML = `<h3>Evidence Filter Applied</h3><p>The review surface is now limited to <strong>${{label}}</strong>. Every row still carries a case ID and event ID for Splunk lookup.</p>`;
    }}

    function runSplSearch() {{
      const risky = EVENTS.filter((event) => ['medium', 'high', 'critical'].includes(event.risk_level) || event.status === 'blocked');
      output.textContent = `index=agentops sourcetype="agentops:json"\\n| search event.risk_level IN ("medium","high","critical") OR event.status="blocked"\\n| table _time event.case_id event.event_id event.risk_level event.status event.summary\\n\\nMatched rows: ${{risky.length}}\\nEvent IDs: ${{risky.map((event) => event.event_id).join(', ')}}`;
      aiOutput.innerHTML = `<h3>SPL Search Result</h3><p>The same investigation can move into Splunk: the prototype already ships HEC-shaped JSON and saved SPL searches.</p>`;
    }}

    function generateAiSummary() {{
      const risky = EVENTS.filter((event) => ['medium', 'high', 'critical'].includes(event.risk_level) || event.status === 'blocked');
      const approvals = EVENTS.filter((event) => event.approval || event.decision !== 'none');
      const cost = EVENTS.reduce((sum, event) => sum + Number(event.cost || 0), 0);
      const riskIds = risky.map((event) => event.event_id).slice(0, 8);
      const approvalIds = approvals.map((event) => event.event_id).slice(0, 8);
      output.textContent = `AI prompt boundary:\\nUse only the AgentOps events visible in this case. Cite event IDs. Do not infer facts that are not in Splunk-searchable evidence.\\n\\nEvidence set: ${{EVENTS.length}} events, ${{risky.length}} risk/blocked rows, ${{approvals.length}} approval rows.`;
      aiOutput.innerHTML = `
        <h3>AI Investigation Draft</h3>
        <p><strong>What happened:</strong> the agent session contains risky or blocked operational actions that need human review before continuation.</p>
        <ul>
          <li><strong>Risk evidence:</strong> ${{riskIds.join(', ')}}</li>
          <li><strong>Approval evidence:</strong> ${{approvalIds.join(', ')}}</li>
          <li><strong>Cost signal:</strong> estimated model/tool spend is $${{cost.toFixed(2)}} across the sample trail.</li>
          <li><strong>Next safe action:</strong> human reviewer should approve, reject, or hand off using the cited event IDs.</li>
        </ul>
        <p>No unsupported claim is included because every sentence must map back to an event row.</p>
      `;
    }}

    document.querySelectorAll('[data-demo-filter]').forEach((button) => {{
      button.addEventListener('click', () => setTimelineFilter(button.dataset.demoFilter));
    }});
    document.querySelector('[data-demo-spl]').addEventListener('click', runSplSearch);
    document.querySelector('[data-demo-ai]').addEventListener('click', generateAiSummary);
  </script>
</body>
</html>
"""


def write_panels(events: list[dict[str, Any]]) -> None:
    cases = grouped_cases(events)
    lines = [
        "# Splunk Dashboard Panels",
        "",
        "Generated from `../shared-agentops-engine/adapters/splunk/hec_events.jsonl`.",
        "",
        "## Panels",
        "",
        "1. Case overview",
        "2. High-risk and blocked actions",
        "3. Human approval queue",
        "4. Estimated model/tool cost by case",
        "5. Evidence timeline",
        "",
        "## Current Metrics",
        "",
        f"- events: {len(events)}",
        f"- cases: {len(cases)}",
        f"- approval gates: {sum(1 for event in events if event.get('human_approval_required'))}",
        f"- blocked actions: {sum(1 for event in events if event['status'] == 'blocked')}",
        f"- redactions: {sum(1 for event in events if event.get('redaction_applied'))}",
        f"- estimated cost: ${sum(float(event.get('cost_usd_estimate', 0) or 0) for event in events):.2f}",
        "",
        "## Claim Boundary",
        "",
        "This is a local dashboard prototype built from Splunk HEC-shaped events. Do not claim live Splunk ingestion until the Splunk terms/account path is approved and verified.",
    ]
    PANELS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PANELS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    events = read_hec_events()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_html(events), encoding="utf-8")
    write_panels(events)
    print(
        json.dumps(
            {
                "status": "ok",
                "source": str(HEC_FILE.relative_to(ROOT.parent)),
                "output": str(OUT_FILE.relative_to(ROOT)),
                "panels": str(PANELS_FILE.relative_to(ROOT)),
                "event_count": len(events),
                "case_count": len({event["case_id"] for event in events}),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
