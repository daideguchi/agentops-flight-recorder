# AgentOps Flight Recorder

AgentOps Flight Recorder is a Splunk-ready black box for human-AI operations.

It is for SRE, platform, security, and operations teams that let AI agents touch tickets, tools, APIs, and release workflows. The hard part after an incident is not reading another chat transcript. The hard part is reconstructing what the agent actually did, what risk appeared, who approved the next step, and what evidence supports the summary.

This project turns agent work into searchable events, risk signals, cost signals, approval gates, and evidence-backed timelines. The AI investigator is evidence-bound: it can summarize the incident only from event IDs and SPL-style result rows.

Submission package: [SUBMISSION_PACKAGE.md](SUBMISSION_PACKAGE.md)

Live demo: https://daideguchi.github.io/agentops-flight-recorder/

YouTube demo: https://youtu.be/Hg1QRVr76Bs

Devpost: https://devpost.com/software/agentops-flight-recorder-750zen

Architecture: [architecture_diagram.md](architecture_diagram.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

Demo video: `splunk-agentic-ops/media/agentops-flight-recorder-demo.mp4`

## Judge Quick Read

- Who: SRE, platform, security, and operations teams responsible for AI-assisted operational work.
- Problem: AI agents are becoming operational actors, but most teams still cannot search, replay, and audit what an agent actually did after an incident.
- Solution: AgentOps Flight Recorder records human, AI agent, robot, API, and system activity as Splunk-ready operational events.
- Demo: a working Flight Recorder dashboard loads events, filters risky actions and approval gates, runs a Splunk-style search, and generates an evidence-bound AI investigation draft.
- Splunk fit: the repo includes HEC-shaped event payloads, draft SPL searches, dashboard panels, and an evidence-bound AI investigation pattern.
- Proof: the prototype generates 26 shared AgentOps events, Splunk-ready HEC JSONL, SPL searches, screenshots, a root `architecture_diagram.md`, and a 53.8 second narrated working-demo video.
- Boundary: this submission claims a verified local prototype and Splunk-ready artifacts. It does not claim live Splunk Cloud ingestion yet.

## Demo

![AgentOps Flight Recorder dashboard](splunk-agentic-ops/media/flight-recorder-dashboard-full.png)

Narrated demo video:

```text
https://youtu.be/Hg1QRVr76Bs
splunk-agentic-ops/media/agentops-flight-recorder-demo.mp4
```

Open locally:

- `splunk-agentic-ops/prototype/flight-recorder-dashboard.html`
- `shared-agentops-engine/web/index.html`

Open in browser:

- https://daideguchi.github.io/agentops-flight-recorder/

## What It Shows

- A normalized AgentOps event schema
- Splunk HEC-shaped sample events
- Draft SPL searches
- A local dashboard for timeline, risk, approval, and cost review
- An evidence-bound AI investigation pattern that cites event IDs
- A reusable evidence trail shared with the other AgentOps hackathon lanes

## Architecture

![AgentOps Flight Recorder architecture](architecture-diagram.svg)

Devpost-required root architecture file: [architecture_diagram.md](architecture_diagram.md)

## Run Locally

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

Expected proof:

```text
verify_ok
status: ok
splunk_local_checks_ok
hec_events=26
architecture=root
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
