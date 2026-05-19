# Architecture Diagram

```text
AI Agent / Human-AI Workflow
        |
        | emits structured events
        v
AgentOps Event Recorder
        |
        | JSONL / HEC
        v
Splunk Event Index
        |
        +--> SPL Searches
        |       - session timeline
        |       - risky actions
        |       - retry loops
        |       - approval handoffs
        |       - cost signals
        |
        +--> Dashboard
        |       - active sessions
        |       - risk queue
        |       - incident timeline
        |       - cost summary
        |
        +--> AI-Assisted Investigation
                - evidence-grounded summary
                - cited event IDs
                - suggested next human action
```

Submission note:

The final public repository should include a polished image version of this architecture diagram at root, not only this text draft.

