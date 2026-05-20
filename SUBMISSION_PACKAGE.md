# Submission Package — AgentOps Flight Recorder

## Project Title

AgentOps Flight Recorder

## Short Description

A Splunk-oriented black box for AI-agent operations, turning actions, risk, cost, approvals, and handoff points into searchable evidence.

## Repository

https://github.com/daideguchi/agentops-flight-recorder

## Live Demo

https://daideguchi.github.io/agentops-flight-recorder/

## YouTube Demo

https://www.youtube.com/watch?v=KrLB5xI_SCg

## Architecture Diagram

- `architecture_diagram.md`
- `ARCHITECTURE.md`
- `architecture-diagram.svg`

## Devpost Manual Submit Guide

- `splunk-agentic-ops/submission/devpost-submit-manual.md`

## Try It Out

Open the live demo or these local demo files after cloning the repository:

- `splunk-agentic-ops/prototype/flight-recorder-dashboard.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `splunk-agentic-ops/media/flight-recorder-dashboard-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Demo Video

Narrated demo video:

- YouTube: `https://www.youtube.com/watch?v=KrLB5xI_SCg`
- `splunk-agentic-ops/media/agentops-flight-recorder-demo.mp4`

Regenerate:

```bash
cd splunk-agentic-ops
bash scripts/build_demo_video.sh
bash scripts/run_splunk_local_checks.sh
```

## Inspiration

AI agents are becoming operational workers. They run commands, call APIs, browse dashboards, retry failures, and hand work back to humans.

The problem is not only whether the agent gave a good answer. The problem is whether a team can reconstruct what the agent actually did after something goes wrong.

Splunk already gives teams a way to search, monitor, and investigate operational systems. AgentOps Flight Recorder applies that same discipline to AI agents: if agents become part of operations, their actions need to become searchable evidence.

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

The demo turns those events into a Splunk-ready timeline and a local dashboard for incident review. The AI investigation layer is evidence-bound: summaries must cite event IDs and SPL result rows instead of inventing facts.

## How We Built It

- AgentOps JSON event schema
- HEC-shaped event export
- Draft SPL searches
- Local dashboard generator
- Root architecture diagram
- Natural English narrated demo video
- Evidence-bound AI investigation pattern
- Shared evidence stream used across multiple hackathon lanes
- Public sanitized sample data

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- Splunk HEC-shaped events
- SPL search drafts
- Evidence-bound AI investigation workflow

## What Is Working

```text
verify_ok
status: ok
event_count=26
case_count=3
splunk_local_checks_ok
hec_events=26
architecture=root
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
bash scripts/run_splunk_local_checks.sh
```

## Demo Script Summary

1. Show why AI-agent operations need observability.
2. Show structured event capture.
3. Show the Flight Recorder dashboard.
4. Show risk, approval, and cost signals.
5. Explain the evidence-bound AI investigation layer.
6. Explain the honest boundary: Splunk-ready artifacts are verified; live Splunk Cloud ingestion is not claimed yet.

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
- Added a root `architecture_diagram.md` for the Devpost architecture requirement
- Built a narrated demo video under three minutes
- Added a repeatable local verification script

## What We Learned

Agentic operations need the same visibility discipline that infrastructure operations already expect.

## What's Next

Verify live Splunk ingestion and convert the local dashboard into a real Splunk dashboard after the account and terms path is approved.

## Claim Boundary

This is a local verified prototype with Splunk-ready artifacts.

It does not claim live Splunk ingestion yet.
