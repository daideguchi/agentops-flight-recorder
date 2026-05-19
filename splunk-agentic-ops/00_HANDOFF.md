# AgentOps Flight Recorder — Handoff

## 2026-05-19 Start

DD clarified that the education folder was not meant to make AI create hackathons. The hackathon development lead owns the actual product build. General lessons from the previous project were recorded under `99_フリーAI教育用`.

After that correction, the next hackathon lane was opened.

## Selected Hackathon

- Hackathon: Splunk Agentic Ops Hackathon
- Devpost: https://splunk.devpost.com/
- Public / online
- Submission period: May 18, 2026 9:00 AM PDT to June 15, 2026 9:00 AM PDT
- Judging: June 26, 2026 to July 10, 2026
- Winners announced: July 17, 2026
- Prize pool: $20,000 cash

## Working Product Name

AgentOps Flight Recorder

## Current Thesis

AI agents are becoming operational workers, but their actions are hard to reconstruct after an incident. AgentOps Flight Recorder captures agent activity as Splunk-searchable operational evidence, then helps humans review timelines, risk signals, cost signals, and safe next actions.

## Why This Follows Coexistence Console

Coexistence Console handled governance for AI-assisted participation in Reddit communities.

AgentOps Flight Recorder handles governance and observability for AI-assisted operations teams.

The shared idea:

```text
Human-AI coexistence needs records, visibility, review, and accountability.
```

## Current Files

- `README.md`
- `docs/official-rules-research.md`
- `docs/product-thesis.md`
- `docs/mvp-plan.md`
- `SUBMISSION_PREP.md`
- `submission/devpost-draft.md`
- `submission/demo-script.md`
- `architecture_diagram.md`

## Open Technical Questions

- Which Splunk runtime should be used first:
  - Splunk Cloud trial
  - local Splunk Enterprise container
  - Splunk Observability Cloud
- Whether Splunk MCP Server can be used directly in this environment.
- Whether hosted models are available through a provided hackathon account.
- Whether demo should focus on Platform & Developer Experience or Observability.

## Immediate Next Steps

1. Confirm Splunk account / free trial / hackathon resources access.
2. Choose local-first Splunk ingestion path.
3. Create event schema and sample agent session generator.
4. Ingest sample events into Splunk.
5. Build dashboard/searches.
6. Add AI-assisted incident summary.

## Safety Notes

- Do not include real API keys, billing information, credentials, or DD private logs in public submissions.
- Use synthetic or sanitized agent traces for the demo.
- If using real Codex/hackathon logs, redact all secrets and private paths before ingestion.

## 2026-05-19 Prototype Seed

Created the first local prototype assets:

- `schemas/agentops_event.schema.json`
- `scripts/generate_sample_events.py`
- `sample_events/agentops_sample_sessions.jsonl`
- `splunk/searches.spl`
- `splunk/README.md`

Validation result:

- generated events: 15
- sessions: 2
- risk events with medium/high/critical level: 5
- human approval required events: 2
- estimated AI cost in sample data: 0.023 USD
- schema JSON parsed successfully with `python3 -m json.tool`
- each generated event contains the required core fields

Docker is installed, but the Docker daemon was not running when checked:

```text
Cannot connect to the Docker daemon at unix:///Users/dd/.docker/run/docker.sock. Is the docker daemon running?
```

Docker Desktop was then started successfully. Pulling `splunk/splunk:latest` required `--platform linux/amd64` on this Apple Silicon Mac, and the image downloaded. The container did not start because the current Splunk Docker image requires explicit acceptance of Splunk General Terms:

```text
License not accepted, please adjust SPLUNK_GENERAL_TERMS and/or SPLUNK_START_ARGS...
include the '--accept-sgt-current-at-splunk-com' and '--accept-license' flags
```

The failed local container was removed:

```text
docker rm agentops-splunk
```

Do not pass `SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com` unless DD explicitly approves accepting the Splunk General Terms. This is a legal/terms boundary, not a technical blocker.

Next practical implementation step:

1. Ask DD whether to accept Splunk General Terms for local Docker Splunk, or use a Splunk Cloud/trial account that DD has already accepted.
2. Import `sample_events/agentops_sample_sessions.jsonl`.
3. Run the searches in `splunk/searches.spl`.
4. Turn the strongest searches into dashboard panels.

## 2026-05-19 Shared Dashboard Package

Built a Splunk-focused local dashboard from the shared HEC-shaped event export without accepting Splunk General Terms.

Created:

- builder: `scripts/build_flight_recorder_dashboard.py`
- HTML output: `prototype/flight-recorder-dashboard.html`
- screenshot: `media/flight-recorder-dashboard-full.png`
- panel notes: `reports/splunk-dashboard-panels.md`

Source data:

- `../shared-agentops-engine/adapters/splunk/hec_events.jsonl`
- `../shared-agentops-engine/adapters/splunk/searches.spl`

Observed builder output:

- `status: ok`
- `event_count: 26`
- `case_count: 3`

Claim boundary:

- This is a local prototype from Splunk-ready HEC events and SPL searches.
- Do not claim live Splunk ingestion until a terms/account path is approved and verified.
