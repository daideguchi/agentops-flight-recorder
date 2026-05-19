# Human-AI Operations Control Plane

This is the shared prototype engine for DD's parallel hackathon portfolio.

It exists so we can build one real artifact and package it for multiple contests:

- UiPath AgentHack: case orchestration and human approval workflow
- Splunk Agentic Ops: agent event observability and incident timeline
- FIND EVIL!: evidence-locked DFIR investigation trail
- Google Cloud Rapid Agent: Gemini/MCP workflow with human-control checkpoints
- Microsoft Agent Academy: Copilot-style architecture and submission story

## Product Thesis

Human-AI work is becoming operational work.

The core problem is not just whether an AI agent can complete a task. The core problem is whether humans can understand, govern, approve, audit, and hand off that work when humans, AI agents, robots, APIs, and cloud tools all participate in the same case.

This engine records agent events, detects operational risk, preserves evidence IDs, summarizes only from recorded facts, and exports the same run into contest-specific formats.

## Current MVP

Run:

```bash
python3 scripts/generate_portfolio_artifacts.py
```

Verify:

```bash
python3 scripts/verify_artifacts.py
```

Outputs:

- `data/agentops_events.jsonl` — canonical event stream
- `reports/handoff_report.md` — evidence-grounded summary
- `web/index.html` — local static dashboard
- `adapters/uipath/case_packet.json` — UiPath case data packet
- `adapters/uipath/maestro_case_stages.md` — Maestro case workflow outline
- `adapters/splunk/hec_events.jsonl` — Splunk-ready JSONL events
- `adapters/splunk/searches.spl` — SPL searches for dashboard panels
- `adapters/findevil/dfir_report.md` — evidence-locked investigation report
- `adapters/google/gemini_mcp_workflow.json` — Gemini/MCP agent workflow plan
- `adapters/microsoft/copilot_architecture.md` — Copilot submission architecture

Screenshot:

- `media/shared-dashboard-full.png`

## Finish Criteria

This folder is considered useful only when:

- the generator runs without external dependencies
- all adapter outputs are regenerated from the same canonical event stream
- the dashboard can be opened locally without a build step
- the handoff report cites concrete event IDs
- no final hackathon submission is performed from here
