# AgentOps Flight Recorder

AgentOps Flight Recorder is a Splunk-oriented black box for human-AI operations.

AI agents now run scripts, call APIs, browse tools, update files, and make operational suggestions. The hard part after an incident is reconstructing what actually happened. This project turns agent work into searchable events, risk signals, cost signals, approval gates, and evidence-backed timelines.

Submission package: [SUBMISSION_PACKAGE.md](SUBMISSION_PACKAGE.md)

## Demo

![AgentOps Flight Recorder dashboard](splunk-agentic-ops/media/flight-recorder-dashboard-full.png)

Open locally:

- `splunk-agentic-ops/prototype/flight-recorder-dashboard.html`
- `shared-agentops-engine/web/index.html`

## What It Shows

- A normalized AgentOps event schema
- Splunk HEC-shaped sample events
- Draft SPL searches
- A local dashboard for timeline, risk, approval, and cost review
- A reusable evidence trail shared with the other AgentOps hackathon lanes

## Run Locally

```bash
cd shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd ../splunk-agentic-ops
python3 scripts/build_flight_recorder_dashboard.py
```

Expected proof:

```text
verify_ok
status: ok
```

## Hackathon Boundary

Safe claim:

- HEC-shaped events, SPL searches, and a local Flight Recorder dashboard are generated.

Not claimed yet:

- Live Splunk ingestion.
- A live Splunk Cloud dashboard.
- Acceptance of any platform terms on behalf of the user.

## Project Layout

- `splunk-agentic-ops/` - Splunk-focused prototype, docs, screenshots, and submission draft
- `shared-agentops-engine/` - shared event stream, adapters, dashboard, and verifier
