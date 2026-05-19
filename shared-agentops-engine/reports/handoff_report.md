# Human-AI Operations Control Plane Handoff Report

Generated from the canonical event stream in `data/agentops_events.jsonl`.

## Metrics

- Events recorded: 26
- Cases recorded: 3
- Human approval gates: 5
- Blocked actions: 1
- High or critical risk signals: 3
- Redactions applied: 1
- Estimated model/tool cost: $4.86

## Case Summaries

### CASE-AI-OPS-001: AI Agent Operations Exception Review

- Max risk: critical
- Events: 11
- Approval gates: 3
- Evidence IDs: evt-0001, evt-0002, evt-0003, evt-0004, evt-0005, evt-0006, evt-0007, evt-0008, evt-0009, evt-0010, evt-0011

Key facts:
- `evt-0006` Case risk escalated because the proposed release affects payments and has failing verification.
- `evt-0007` Attempted production deployment was blocked by policy before execution.
- `evt-0008` Human requested more evidence instead of approving the production deployment.
- `evt-0010` Service owner rejected the release until the retry regression is fixed.
- `evt-0011` Generated a case handoff report with cited evidence IDs and final rejection decision.

Risk notes:
- `evt-0005` medium: Regression test failed around duplicate retry suppression.
- `evt-0006` high: Production payment behavior change plus failing regression test.
- `evt-0007` critical: Production deployment is destructive and requires human approval.
- `evt-0008` medium: Human requested more evidence instead of approving the production deployment.

### CASE-DFIR-002: Evidence-Locked Phishing Investigation

- Max risk: high
- Events: 8
- Approval gates: 1
- Evidence IDs: evt-0012, evt-0013, evt-0014, evt-0015, evt-0016, evt-0017, evt-0018, evt-0019

Key facts:
- `evt-0016` System marked the draft finding as provisional because execution evidence was missing.
- `evt-0018` Human approved containment of the reported message and requested no endpoint isolation.
- `evt-0019` Generated DFIR report with evidence IDs, unsupported claims, and human containment decision.

Risk notes:
- `evt-0015` medium: Initial model answer overclaimed malware execution before process evidence was present.
- `evt-0016` high: Unsupported certainty detected in analyst draft.
- `evt-0017` medium: Hash lookup returned low-confidence phishing kit association; raw indicator was redacted in report output.

### CASE-CLOUD-003: Human-Controlled Cloud Agent Workflow

- Max risk: medium
- Events: 7
- Approval gates: 1
- Evidence IDs: evt-0020, evt-0021, evt-0022, evt-0023, evt-0024, evt-0025, evt-0026

Key facts:
- `evt-0025` Human approved the workflow with a rule that expensive model calls are escalation-only.
- `evt-0026` Closed cloud-agent workflow case with source citations, cost guardrail, and human approval captured.

Risk notes:
- `evt-0024` medium: Projected monthly model spend exceeded the manager's prototype budget.

