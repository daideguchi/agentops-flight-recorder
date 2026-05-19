# Devpost Draft

## Project Title

AgentOps Flight Recorder

## Elevator Pitch

AgentOps Flight Recorder is a Splunk-native black box for AI-agent operations, turning tool calls, browser actions, retries, approvals, cost signals, and risk events into searchable evidence and human-readable incident timelines.

## Inspiration

AI agents are starting to do real operational work. They run commands, call APIs, browse dashboards, edit files, retry failures, and hand work back to humans.

That is powerful, but it creates a new operational problem: after something happens, teams need to reconstruct what the agent actually did.

I built this from the same human-AI collaboration reality that produced my previous hackathon project. The hard problem is not just making AI act. The hard problem is making AI-assisted work observable, reviewable, and accountable.

## What It Does

- captures AI-agent activity as structured events
- sends those events into Splunk
- reconstructs session timelines
- highlights risky actions, retry loops, approval handoffs, and cost signals
- generates an evidence-grounded investigation summary
- gives humans a clear next action

## What It Does Not Do

- does not hide agent actions
- does not expose secrets in public demo data
- does not allow unreviewed production changes
- does not let AI summaries override the event trail

## How We Built It

Draft. Fill after implementation.

## Impact

Agentic operations need observability.

Splunk already helps teams understand infrastructure and applications. AgentOps Flight Recorder extends that idea to AI workers: if agents become part of operations, their actions need to be searchable, explainable, and governed too.

