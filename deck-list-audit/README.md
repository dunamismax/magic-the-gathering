# Commander deck audit system

This directory is a reproducible, fail-closed workflow for validating,
evaluating, comparing, and safely changing a Commander collection with an AI
agent. It separates hard construction facts from external evidence and social
judgment.

## Trust model

| Layer | Purpose | Authority |
|---|---|---|
| Source | Decklists and collection constraints | `decks/*.txt`, `collection.json` |
| Deterministic | Count, names, commanders, identity, legality, release state, lands, Game Changers | `scripts/audit_decks.py` |
| External evidence | Oracle corpus, official policy snapshot, Commander Spellbook | `data/`, `policy/` |
| Adjudication | Confirmed/rejected/incomplete combo findings and role overrides | `knowledge/` |
| Judgment | Strategy, speed, bracket, replayability, salt, recommendations | `rubrics/`, dated reports |
| Change control | Baseline-locked Adds/Cuts and post-change validation | `changes/`, `scripts/apply_change.py` |

The system can be deterministic about construction. It cannot make subjective
social judgments or combo-database completeness mathematically perfect, so
those conclusions must carry evidence dates and confidence.

## Commands

Run commands from this directory or the repository root:

```text
just doctor
just audit
just check
just check-current
just report
just test
```

Source refresh and imports:

```text
just refresh-oracle
python3 scripts/refresh_sources.py import-moxfield --deck kang-prime --file /path/to/export.txt
python3 scripts/refresh_sources.py spellbook --deck kang-prime --allow-deck-upload
```

The Spellbook command sends a complete decklist to a third party. It refuses
private decks and requires the explicit upload flag. Moxfield imports are local
because Moxfield does not provide a stable anonymous export API for this
workflow.

Apply a deck change:

```text
cp changes/change-plan.example.json changes/my-change.json
# Fill in deck, baseline hash, Adds/Cuts, and rationale.
just apply-change PLAN=changes/my-change.json
```

The change tool verifies the baseline hash, applies the plan to a temporary
copy, runs the deterministic audit, preserves the commander block, writes the
deck atomically, and regenerates local artifacts. External combo results and
human reports become explicitly stale until refreshed or reviewed.

## Source and generated files

Human-owned:

- `collection.json`
- `decks/*.txt`
- `policy/current.json`
- `knowledge/*.json`
- `rubrics/*.md`
- `changes/*.json`

Generated:

- `data/audit.json`
- `data/spellbook-requests/*.json`
- `data/spellbook-results/manifest.json`
- `decks/README.md`
- `generated/collection-summary.md`
- `generated/functional-analysis.json`
- `generated/manifest.json`

Raw refreshed Oracle data is cached under `cache/` and excluded from Git. The
original 2026-08-29 Oracle corpus remains in `data/` as the locked bootstrap
fixture and offline fallback.

GitHub Actions runs the dependency-free test suite and full internal evidence
check on every relevant push and pull request. Current-source age remains a
local/operator gate because a historical commit must stay reproducible after
its freshness window expires.

## Deck format

Deck files use Moxfield/MTGO plain text:

```text
1 Card Name
2 A Card Allowed in Multiple Copies

1 Commander Name
```

Commander identity comes from `collection.json`, not position alone. Blank
lines are cosmetic. Names are normalized to Oracle IDs before duplicate and
identity checks, so aliases cannot evade singleton validation.

## Freshness

`just check` validates internal consistency against locked evidence.
`just check-current` additionally enforces the source-age thresholds in
`collection.json`. A current claim must pass the latter or disclose the locked
snapshot dates.

## Historical report

`commander-social-audit.md` is the human collection analysis made against the
2026-08-29 snapshot. Its input hashes are tracked in `reports/manifest.json`.
It is historical evidence, not a self-updating statement about later deck
versions.
