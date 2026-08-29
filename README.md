# Magic: The Gathering Commander tools

This repository contains reusable Commander evaluation/tuning rubrics and the
audited `dunamismax` deck collection.

## Collection audit system

The operational system lives in
[`deck-list-audit/`](deck-list-audit/README.md). Start an AI coding agent in
that directory; its [`AGENTS.md`](deck-list-audit/AGENTS.md) defines the
required exact-list, freshness, privacy, change-control, and verification
workflow.

Quick start:

```text
cd deck-list-audit
just doctor
just check-current
```

## Reusable prompt references

- [`commander-deck-evaluation-prompt.md`](commander-deck-evaluation-prompt.md)
- [`commander-deck-upgrade-prompt.md`](commander-deck-upgrade-prompt.md)
- [`commander-deck-upgrade-advanced.md`](commander-deck-upgrade-advanced.md)

The audit system contains shorter routed rubrics derived from these references,
so an agent can choose full evaluation, conservative tuning, structural tuning,
or collection review without mixing incompatible scopes.
