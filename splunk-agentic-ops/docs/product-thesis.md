# Product Thesis

## Working Name

AgentOps Flight Recorder

Alternative names:

- AgentOps Black Box
- Human-AI Ops Recorder
- Splunk AgentOps Console
- Agentic Runbook Recorder

## One-Sentence Pitch

AgentOps Flight Recorder captures AI-agent activity as Splunk-searchable evidence so teams can reconstruct incidents, spot risk and cost signals, and decide the next safe human action.

## Who

Primary users:

- platform engineering teams
- SRE / DevOps teams
- security operations teams
- AI platform teams
- teams letting AI agents run tools, scripts, browsers, or production workflows

## Problem

AI agents are starting to behave like operational workers.

They can:

- run shell commands
- call APIs
- browse web apps
- update files
- create commits
- investigate incidents
- generate reports

But after something goes wrong, the team often cannot quickly answer:

- What exactly did the agent do?
- Which tool calls succeeded or failed?
- Which system changed?
- Which account or browser profile was used?
- Did the agent retry the same failing action?
- Did cost spike?
- Did it touch risky commands or secret-like values?
- What should a human review next?

## Why Now

Agentic operations are becoming real.

The more AI agents help with operational work, the more teams need observability, governance, auditability, and human handoff.

Traditional logs show service behavior.
AgentOps Flight Recorder shows agent behavior.

## Product Promise

Turn agent uncertainty into Splunk-searchable operational evidence.

## What It Does

1. Captures agent activity events.
2. Normalizes them into an AgentOps event schema.
3. Sends events into Splunk.
4. Builds incident timelines from those events.
5. Highlights risk, cost, retry, and approval signals.
6. Generates human-readable investigation summaries from evidence.
7. Produces safe next-step recommendations without pretending the AI knows facts outside the logs.

## What It Does Not Do

- It does not let AI secretly operate without logging.
- It does not hide failed or risky actions.
- It does not expose real secrets in public demo data.
- It does not make production changes automatically.
- It does not treat AI summaries as ground truth.
- It does not claim to replace human incident commanders.

## MVP Demo Story

Before:

An AI agent tries to investigate a production issue. It runs commands, opens browser pages, retries failed steps, and edits a config. Later, the human team has to ask: what actually happened?

After:

Every action appears in Splunk. The dashboard shows a session timeline, retry loops, risky commands, approval boundaries, cost estimates, and the exact evidence behind a generated incident summary.

## Why It Can Win

This is directly aligned with Agentic Ops:

- it treats agents as operational actors
- it uses operational data as the AI context
- it makes Splunk the source of truth
- it is practical for real teams
- it has a strong human-AI governance story

## Minimum Winning Product

- synthetic but realistic agent session generator
- Splunk ingestion
- dashboard/search timeline
- risk and cost signal extraction
- one AI-assisted summary grounded in query evidence
- polished README with architecture diagram, screenshots, and video

