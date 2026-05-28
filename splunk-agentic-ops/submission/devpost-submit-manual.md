# Devpost Submit Manual — AgentOps Flight Recorder

Use this only if the Devpost project must be recreated or edited manually.

## Current State

- Hackathon: Splunk Agentic Ops Hackathon
- Project: AgentOps Flight Recorder
- Repository: https://github.com/daideguchi/agentops-flight-recorder
- Live demo: https://daideguchi.github.io/agentops-flight-recorder/
- YouTube demo: https://www.youtube.com/watch?v=KrLB5xI_SCg
- Devpost project: https://devpost.com/software/agentops-flight-recorder-750zen
- Architecture: https://github.com/daideguchi/agentops-flight-recorder/blob/main/architecture_diagram.md
- Status: submitted. The Splunk Agentic Ops manage page showed `SUBMITTED` for `AgentOps Flight Recorder` on 2026-05-29 JST.

## Manual Start

The project is already submitted. Use this section only if a future edit or recreation is required.

1. Open https://devpost.com/software/new
2. Create project name:

```text
AgentOps Flight Recorder
```

3. Complete the Devpost reCAPTCHA manually.
4. Save and continue.
5. Attach the project to:

```text
https://devpost.com/submit-to/29204-splunk-agentic-ops-hackathon/select/software
```

## Tagline

```text
A Splunk-ready black box for AI-agent operations, turning actions, risk, cost, approvals, and handoff points into searchable evidence.
```

## Built With

```text
Python, HTML, CSS, JSON, JSONL, Splunk HEC-shaped events, SPL searches, AgentOps event schema, evidence-bound AI investigation workflow
```

## Project Links

- Live demo: https://daideguchi.github.io/agentops-flight-recorder/
- GitHub repository: https://github.com/daideguchi/agentops-flight-recorder
- YouTube demo: https://www.youtube.com/watch?v=KrLB5xI_SCg
- Architecture diagram: https://github.com/daideguchi/agentops-flight-recorder/blob/main/architecture_diagram.md
- Submission package: https://raw.githubusercontent.com/daideguchi/agentops-flight-recorder/main/SUBMISSION_PACKAGE.md

## Story

````markdown
## Inspiration

AI agents are starting to do real operational work. They run commands, call APIs, browse dashboards, edit files, retry failures, and hand work back to humans.

That is powerful, but it creates a new operational problem: after something happens, teams need to reconstruct what the agent actually did.

Splunk is the natural place for this story. If infrastructure and applications need searchable telemetry, AI agents need it too.

I built this from a real human-AI collaboration rhythm. The hard problem is not only making AI act. The hard problem is making AI-assisted work observable, reviewable, and accountable.

## What it does

AgentOps Flight Recorder captures human, AI agent, robot, API, and system activity as structured operational events.

The demo turns those events into:

- Splunk HEC-shaped payloads
- SPL searches for timelines, risky actions, retry loops, approval gates, and cost signals
- a local Flight Recorder dashboard
- an evidence-bound AI investigation pattern
- a root architecture diagram

The AI layer is intentionally evidence-bound. It can summarize what happened, but it must cite event IDs and search result rows instead of inventing facts.

## How we built it

- AgentOps JSON event schema
- Splunk HEC-shaped JSONL export
- SPL search drafts
- Local dashboard generator
- Root architecture diagram
- Natural English narrated demo video
- Repeatable local verification script
- Public sanitized sample data

Main verification command:

```bash
cd splunk-agentic-ops
bash scripts/run_splunk_local_checks.sh
```

Observed proof:

```text
splunk_local_checks_ok
hec_events=26
video_seconds=87.4
architecture=root
claim_boundary=verified_local_splunk_ready_no_live_ingestion_claim
```

## Challenges

The main challenge was making the project useful without pretending live Splunk Cloud ingestion was already verified. The current package focuses on HEC-shaped events, SPL searches, a clear review dashboard, and an evidence-bound AI investigation flow that can move into a live Splunk path after the account and terms path is approved.

## Accomplishments

- Built an AgentOps event schema
- Generated Splunk HEC-shaped events
- Drafted SPL searches
- Built a local Flight Recorder dashboard
- Added a root architecture diagram
- Built a narrated demo video under three minutes
- Added a repeatable local verification script
- Published a clean public repository

## What we learned

Agentic operations need the same visibility discipline that infrastructure operations already expect. If AI agents become operational workers, their actions need to become searchable evidence.

## What's next

Verify live Splunk ingestion and convert the local dashboard into a real Splunk dashboard after the account and terms path is approved.

## Claim boundary

This is a verified local prototype with Splunk-ready artifacts. It does not claim live Splunk Cloud ingestion or a live Splunk dashboard yet.
````

## Stopline

Do not claim live Splunk ingestion unless it is actually verified. Do not answer DD-only eligibility fields such as government employment or country of residence, accept Splunk/Devpost terms, or click the final Devpost submit button unless DD approves that exact action.
