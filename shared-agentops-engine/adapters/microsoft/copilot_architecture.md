# Human-AI Handoff Copilot Architecture

Target: Microsoft Agent Academy Hackathon

## User

A support manager who wants AI assistance without losing control over cost, escalation, policy accuracy, or final customer communication.

## Components

- Copilot-style conversational intake
- Knowledge retrieval from approved policy sources
- Adaptive-card approval gate for escalations and high-cost model calls
- AgentOps event stream for auditability
- Handoff report with event IDs and source citations

## Data Flow

1. User asks a customer-support question.
2. Agent retrieves policy evidence before drafting an answer.
3. Risk and cost guardrails evaluate the draft.
4. Human approval is required when uncertainty, policy risk, or cost exceeds the threshold.
5. Final answer and handoff report cite event IDs.

## Evidence From Prototype

- `evt-0020` Support manager requested an agent that answers customer questions and escalates uncertain cases.
- `evt-0021` Agent created a workflow plan using retrieval, MCP tools, cost guardrails, and human escalation.
- `evt-0022` MCP retrieval returned the current refund policy and source URL for citation.
- `evt-0023` Agent drafted a customer answer grounded in the retrieved refund policy.
- `evt-0024` Cost guardrail warned that the high-quality model should be reserved for escalations.
- `evt-0025` Human approved the workflow with a rule that expensive model calls are escalation-only.
- `evt-0026` Closed cloud-agent workflow case with source citations, cost guardrail, and human approval captured.
