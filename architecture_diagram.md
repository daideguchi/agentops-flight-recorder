# Architecture Diagram — AgentOps Flight Recorder

AgentOps Flight Recorder turns AI-agent operations into Splunk-searchable evidence.

```text
Human + AI agent workflow
        |
        | emits tool calls, browser actions, approvals, risk, cost, retries
        v
AgentOps Event Recorder
        |
        | normalizes events into JSONL and Splunk HEC-shaped payloads
        v
Splunk evidence layer
        |
        +--> SPL searches
        |       - session timeline
        |       - risky actions
        |       - retry loops
        |       - approval handoffs
        |       - cost signals
        |
        +--> Flight Recorder dashboard
        |       - incident timeline
        |       - evidence cards
        |       - risk queue
        |       - cost summary
        |
        +--> Evidence-bound AI investigation
                - summarizes only from cited event IDs
                - identifies next human action
                - cannot override the event trail
```

## Splunk-Ready Artifacts

- `shared-agentops-engine/adapters/splunk/hec_events.jsonl` contains HEC-shaped events.
- `shared-agentops-engine/adapters/splunk/searches.spl` contains draft SPL searches.
- `splunk-agentic-ops/prototype/flight-recorder-dashboard.html` shows the local review surface.
- `splunk-agentic-ops/media/flight-recorder-dashboard-full.png` is the dashboard screenshot.

## Claim Boundary

This is a verified local prototype with Splunk-ready artifacts. It does not claim live Splunk Cloud ingestion or a live Splunk dashboard yet.
