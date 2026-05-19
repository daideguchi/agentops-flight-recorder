# Submission Package — AgentOps Flight Recorder

## Project Title

AgentOps Flight Recorder

## Short Description

A Splunk-oriented black box for AI-agent operations, turning actions, risk, cost, approvals, and handoff points into searchable evidence.

## Repository

https://github.com/daideguchi/agentops-flight-recorder

## Try It Out

Open these local demo files after cloning the repository:

- `splunk-agentic-ops/prototype/flight-recorder-dashboard.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `splunk-agentic-ops/media/flight-recorder-dashboard-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Demo Video

Draft silent video:

- `splunk-agentic-ops/media/agentops-flight-recorder-demo-draft.mp4`

Regenerate:

```bash
cd splunk-agentic-ops
bash scripts/build_demo_video.sh
```

## Inspiration

AI agents are becoming operational workers. They run commands, call APIs, browse dashboards, retry failures, and hand work back to humans.

The problem is not only whether the agent gave a good answer. The problem is whether a team can reconstruct what the agent actually did after something goes wrong.

## What It Does

AgentOps Flight Recorder captures AI-agent work as structured operational events:

- tool calls
- shell commands
- browser actions
- risk signals
- cost signals
- retry loops
- approval gates
- handoff points

The demo turns those events into a Splunk-ready timeline and a local dashboard for incident review.

## How We Built It

- AgentOps JSON event schema
- HEC-shaped event export
- Draft SPL searches
- Local dashboard generator
- Shared evidence stream used across multiple hackathon lanes
- Public sanitized sample data

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- Splunk HEC-shaped events
- SPL search drafts

## What Is Working

```text
verify_ok
status: ok
event_count=26
case_count=3
```

## Verification Commands

```bash
cd shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd ../splunk-agentic-ops
python3 scripts/build_flight_recorder_dashboard.py
bash scripts/build_demo_video.sh
```

## Demo Script Summary

1. Show why AI-agent operations need observability.
2. Show structured event capture.
3. Show the Flight Recorder dashboard.
4. Show risk, approval, and cost signals.
5. Explain how this maps to Splunk ingestion and searches.

## What Makes It Different

This is not another chatbot dashboard. It treats AI agents as operational actors whose behavior must be searchable, reviewable, and accountable.

## Challenges

The main challenge was making the demo useful without pretending live Splunk Cloud ingestion was already verified. The current package focuses on HEC-shaped events, SPL searches, and a clear dashboard that can be imported into a live Splunk path later.

## Accomplishments

- Built an AgentOps event schema
- Generated Splunk HEC-shaped events
- Drafted SPL searches
- Built a local Flight Recorder dashboard
- Published a clean public repository

## What We Learned

Agentic operations need the same visibility discipline that infrastructure operations already expect.

## What's Next

Verify live Splunk ingestion and convert the local dashboard into a real Splunk dashboard after the account and terms path is approved.

## Claim Boundary

This is a local verified prototype with Splunk-ready artifacts.

It does not claim live Splunk ingestion yet.
