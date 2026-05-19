# Submission Prep

## Hackathon

Splunk Agentic Ops Hackathon

## Working Product

AgentOps Flight Recorder

## Submission Window

May 18, 2026 9:00 AM PDT to June 15, 2026 9:00 AM PDT

## Required Assets

- Public GitHub repo
- README
- architecture diagram at repo root
- demo video under 3 minutes
- screenshots
- Devpost story
- clear Splunk usage

## Draft Built With

- Splunk
- Splunk Search Processing Language
- Splunk dashboards
- Splunk HEC or local event import
- Splunk MCP Server, if feasible
- TypeScript or Python for event generation and ingestion
- AI summarization path, grounded in Splunk evidence

## Submission Copy Must Emphasize

- Agentic operations
- operational data as AI context
- human-AI work with records and accountability
- Splunk as the evidence layer
- practical value for platform teams
- safe human review

## Do Not Claim Until Verified

- Splunk MCP works
- Splunk hosted models work
- Splunk Cloud account works
- live ingestion works
- AI summary is using Splunk evidence

## Current Local Proof

- HEC-shaped events: `../shared-agentops-engine/adapters/splunk/hec_events.jsonl`
- SPL searches: `../shared-agentops-engine/adapters/splunk/searches.spl`
- Local dashboard prototype: `prototype/flight-recorder-dashboard.html`
- Screenshot: `media/flight-recorder-dashboard-full.png`
- Panel notes: `reports/splunk-dashboard-panels.md`

Do not confuse the local dashboard prototype with a live Splunk dashboard.

## Cost / Credential Notes

- Avoid paid cloud use until DD confirms.
- Prefer free trial or local Splunk first.
- Do not commit tokens, keys, or real private logs.
