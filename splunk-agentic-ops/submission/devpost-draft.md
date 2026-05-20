# Devpost Draft

## Project Title

AgentOps Flight Recorder

## Elevator Pitch

AgentOps Flight Recorder is a Splunk-ready black box for AI-agent operations, turning tool calls, browser actions, retries, approvals, cost signals, and risk events into searchable evidence and human-readable incident timelines.

## Links

- Live demo: https://daideguchi.github.io/agentops-flight-recorder/
- GitHub: https://github.com/daideguchi/agentops-flight-recorder
- YouTube demo: https://www.youtube.com/watch?v=KrLB5xI_SCg
- Architecture: https://github.com/daideguchi/agentops-flight-recorder/blob/main/ARCHITECTURE.md

## Inspiration

AI agents are starting to do real operational work. They run commands, call APIs, browse dashboards, edit files, retry failures, and hand work back to humans.

That is powerful, but it creates a new operational problem: after something happens, teams need to reconstruct what the agent actually did.

I built this from the same human-AI collaboration reality that produced my previous hackathon project. The hard problem is not just making AI act. The hard problem is making AI-assisted work observable, reviewable, and accountable.

Splunk is the natural place for this story. If infrastructure and applications need searchable telemetry, AI agents need it too.

## What It Does

- captures AI-agent activity as structured events
- exports those events as Splunk HEC-shaped payloads
- reconstructs session timelines
- highlights risky actions, retry loops, approval handoffs, and cost signals
- provides SPL searches for timeline, risk, retry, approval, and cost review
- generates an evidence-grounded investigation summary that cites event IDs
- gives humans a clear next action

## What It Does Not Do

- does not hide agent actions
- does not expose secrets in public demo data
- does not allow unreviewed production changes
- does not let AI summaries override the event trail
- does not claim live Splunk Cloud ingestion yet

## How We Built It

- AgentOps JSON event schema
- Splunk HEC-shaped JSONL export
- SPL search drafts
- Local Flight Recorder dashboard
- Root architecture diagram
- Evidence-bound AI investigation pattern
- Natural English narrated demo video
- Repeatable local verification script

Main verification command:

```bash
cd splunk-agentic-ops
bash scripts/run_splunk_local_checks.sh
```

Observed proof:

```text
splunk_local_checks_ok
hec_events=26
architecture=root
claim_boundary=verified_local_splunk_ready_no_live_ingestion_claim
```

## Impact

Agentic operations need observability.

Splunk already helps teams understand infrastructure and applications. AgentOps Flight Recorder extends that idea to AI workers: if agents become part of operations, their actions need to be searchable, explainable, and governed too.
