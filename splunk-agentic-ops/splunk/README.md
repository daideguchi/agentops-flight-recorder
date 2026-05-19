# Splunk Setup Notes

## Initial Local Import Path

The first prototype can be validated without paid cloud resources.

1. Generate sample events:

```bash
python3 scripts/generate_sample_events.py
```

2. Import `sample_events/agentops_sample_sessions.jsonl` into Splunk.

Suggested metadata:

```text
index=agentops
sourcetype=agentops:event
source=agentops_sample_sessions.jsonl
```

3. Run searches from `splunk/searches.spl`.

## Future HEC Path

Once a local or cloud Splunk instance is available, add a small ingestion client:

```text
POST /services/collector/event
Authorization: Splunk <HEC_TOKEN>
```

Do not commit HEC tokens.

## Dashboard Direction

Panels:

- session timeline
- high and critical risk events
- failed / blocked events
- retry loop detector
- estimated AI cost by session
- human approval required

