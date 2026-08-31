# Magic: The Gathering Commander collection

This repository is the source-controlled home for `dunamismax`'s Commander
lineup. It stores exact public Moxfield snapshots, deterministic construction
audits, dated external evidence, safe change tooling, and reusable review
prompts.

The current collection contains **7 decks**. Every public list was downloaded
and verified on **2026-08-30**.

## Start here

| Need | Open |
|---|---|
| Browse the current deck lineup | [`deck-list-audit/decks/README.md`](deck-list-audit/decks/README.md) |
| Understand or operate the audit system | [`deck-list-audit/README.md`](deck-list-audit/README.md) |
| Review deterministic collection totals | [`deck-list-audit/generated/collection-summary.md`](deck-list-audit/generated/collection-summary.md) |
| Choose an evaluation or tuning prompt | [`prompts/README.md`](prompts/README.md) |
| Read dated human reports | [`deck-list-audit/reports/README.md`](deck-list-audit/reports/README.md) |
| See agent rules and privacy boundaries | [`deck-list-audit/AGENTS.md`](deck-list-audit/AGENTS.md) |

## Verify the repository

The root `Justfile` delegates to the audit system:

```text
just doctor
just check
just check-current
just test
just verify
```

`just check` verifies reproducibility and clearly warns when dated external
analysis no longer matches a deck. `just check-current` is stricter: it also
requires current Oracle, policy, Spellbook, and exact-list combo evidence. A
source refresh can therefore pass the internal check while correctly refusing
to call older external conclusions current. `just verify` runs the strict
current check, tests, and lint as the final repository gate.

## Trust boundaries

- `deck-list-audit/decks/*.txt` and `deck-list-audit/collection.json` are the
  current human-owned collection source.
- `data/audit.json` and `generated/` are reproducible outputs; regenerate them
  instead of editing them by hand.
- Public Moxfield exports may be downloaded locally. The workflow never writes
  changes back to Moxfield unless the user separately asks for that action.
- Complete private lists are not sent to third parties. Commander Spellbook
  uploads are opt-in even for public lists.

The project is licensed under [`LICENSE`](LICENSE). Card names and game data
remain subject to their respective owners and data providers.
