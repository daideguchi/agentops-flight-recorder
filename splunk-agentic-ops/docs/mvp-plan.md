# MVP Plan

## Product Goal

Build a working Splunk-backed console for observing AI-agent operations.

## Technical Slice 1: Event Schema

Create an event format like:

```json
{
  "timestamp": "2026-05-19T12:00:00Z",
  "session_id": "agent-session-001",
  "task_id": "incident-db-latency",
  "actor_type": "ai_agent",
  "actor_name": "codex-worker",
  "phase": "investigation",
  "event_type": "tool_call",
  "tool": "shell",
  "action": "exec_command",
  "target": "api-service",
  "status": "success",
  "duration_ms": 1820,
  "risk_level": "low",
  "cost_usd_estimate": 0.002,
  "human_approval_required": false,
  "summary": "Checked recent service errors",
  "evidence_ref": "event-0001"
}
```

## Technical Slice 2: Demo Event Generator

Generate realistic sessions:

- successful investigation
- retry loop
- browser account mismatch
- risky destructive command blocked
- secret-like text detected and redacted
- high-cost model call
- human approval handoff

## Technical Slice 3: Splunk Ingestion

Preferred order:

1. local JSONL import into Splunk
2. HEC ingestion if local/Cloud token is available
3. fallback: saved CSV/JSON + documented import steps

Do not block the first prototype on account setup.

## Technical Slice 4: Searches and Dashboard

Searches:

- all events by session
- failed events
- retry loops
- high-risk events
- approval-required events
- estimated cost by session
- timeline by task

Dashboard panels:

- active sessions
- risk queue
- timeline
- failure/retry heatmap
- cost summary
- approval queue
- incident summary

## Technical Slice 5: AI-Assisted Investigation

Use Splunk AI / MCP if feasible.

If not initially available, keep the architecture ready and implement a local evidence-grounded summary path for prototype, then replace with Splunk AI path when credentials/resources are confirmed.

The summary must cite event IDs and must not invent facts.

## Technical Slice 6: Submission Assets

Need:

- architecture diagram at repo root
- README screenshots
- 3-minute-or-less demo video
- public GitHub
- Devpost copy
- install/test commands

## First Implementation Milestones

1. Build `sample_events/agent_session_001.jsonl`.
2. Build a generator script.
3. Confirm local Splunk path.
4. Import events.
5. Create SPL queries.
6. Capture dashboard screenshots.
7. Add AI summary.

