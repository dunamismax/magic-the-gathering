# Commander deck audit system

This directory is the reproducible operating system for `dunamismax`'s public
Commander collection. It separates exact deck sources, deterministic
construction facts, dated external evidence, human judgment, and controlled
deck edits so one layer cannot silently masquerade as another.

## Current snapshot

- **10 public decks**: the full collection was downloaded from Moxfield on
  **2026-08-31**, Gandalf was reconciled to the user's exact six-for-six
  Moxfield change on **2026-09-01**, and all lists were locally audited that day
- **9 Bracket 3 targets** and **1 Bracket 2 target** (Frodo & Sam)
- All 10 currently resolve to exactly 100 cards and pass deterministic count,
  commander, singleton, identity, legality, release-state, banned-card, and
  configured Game Changer checks
- All 10 exact lists have hash-current Commander Spellbook evidence: six scans
  from **2026-08-30** and refreshed scans for Aragorn, Frodo & Sam, Gandalf, and
  revised Minn from **2026-09-01**, each paired with manual prerequisite review
- Gandalf has one confirmed conditional two-card unlimited-combat line;
  Pantlaza has three confirmed conditional near-infinite lines; Queen Marchesa
  has one finite Spellbook line and one manually verified five-card loop; and
  Henzie's returned persist template is incomplete
- The current 10-deck social and bracket reviews are pinned to these exact
  hashes; superseded seven-deck reports remain dated historical evidence

Browse titles, source dates, Moxfield links, and hashes in
[`decks/README.md`](decks/README.md). Deterministic totals are in
[`generated/collection-summary.md`](generated/collection-summary.md).

## Repository map

| Area | Purpose | Editing rule |
|---|---|---|
| `collection.json` | Deck registry, source metadata, and hard constraints | Human-owned |
| `decks/*.txt` | Exact local deck sources | Human-owned; import or guarded change only |
| `policy/` | Dated official Commander policy lock | Human-verified |
| `knowledge/` | Role overrides and current combo-review state | Human-reviewed |
| `rubrics/` | Routed evaluation and tuning instructions | Human-owned |
| `changes/` | Proposed, confirmed, and applied change records | Human-owned audit trail |
| `data/` | Oracle metadata, deterministic audit, Spellbook requests/results | Generated or externally refreshed |
| `generated/` | Collection summary, functional analysis, manifests | Generated |
| `reports/` | Dated human reports and archives | Human-reviewed |
| `scripts/`, `tests/` | Audit engine and verification | Source code |

## Commands

Run these from this directory. The repository-root `Justfile` exposes the same
common commands.

```text
just doctor          # environment and file sanity
just audit           # rebuild deterministic and generated artifacts
just check           # reproducibility plus explicit stale-evidence warnings
just check-current   # also require current external evidence
just report          # rebuild role and Markdown summaries
just test            # dependency-free unit and integration tests
just verify          # strict current check, tests, and lint
```

A source refresh is complete when `just check` passes. `just check-current` may
still fail after a legitimate deck refresh because dated Spellbook, combo, or
social conclusions no longer match the current hashes. That failure protects
future evaluations from reusing obsolete findings.

## Trust model

| Layer | Answers | Authority |
|---|---|---|
| Source | What cards and constraints are current? | `decks/*.txt`, `collection.json` |
| Deterministic | Is the list constructed legally and what does it contain? | `scripts/audit_decks.py` |
| External evidence | What did current Oracle, official policy, or Spellbook report? | `data/`, `policy/` |
| Adjudication | Which candidate lines actually work in this exact 100? | `knowledge/` |
| Judgment | How does the deck play and fit a pod? | `rubrics/`, dated reports |
| Change control | Was a proposed package applied to the intended baseline? | `changes/`, `scripts/apply_change.py` |

The engine can be deterministic about construction. Bracket fit, salt,
replayability, and combo-database completeness remain evidence-backed judgment.

## Refresh the public Moxfield collection

Moxfield does not expose a stable anonymous export API for this workflow. Use
its public deck-page **Download → Copy Plain Text** export, then import locally.
Do not rely on the displayed update date as proof that a list is unchanged.

For each configured deck:

```text
python3 scripts/refresh_sources.py import-moxfield \
  --deck magda-brazen-outlaw \
  --file /path/to/magda-brazen-outlaw.txt \
  --expected-sha CURRENT_LOCAL_SHA256
```

Then update `source_updated_on` and `source_refreshed_on` in `collection.json`,
register any new deck, update `data/moxfield-refresh.json`, and run `just audit`.
The refresh manifest pins the exact public deck set, IDs, dates, and local
SHA-256 values. Every import is baseline-guarded,
normalized, tested against all configured decks, and written atomically.

A deck addition also requires a `collection.json` record with commander names,
Moxfield ID, source dates, visibility, bracket/Game Changer constraints, Rule
Zero cards, locked cards, and intended experience. Alternate export names belong
in `collection.json` under `aliases`.

## External refreshes

Refresh the local Oracle corpus:

```text
just refresh-oracle
```

The repository owner has granted standing authorization for full-list uploads
of decks configured as public when they are needed for collection review or
maintenance. Refresh Commander Spellbook with:

```text
python3 scripts/refresh_sources.py spellbook \
  --deck magda-brazen-outlaw \
  --allow-deck-upload
```

That command sends the complete public list to a third party. It refuses private
decks and requires the explicit flag as a technical safeguard; no additional
per-run confirmation is needed for configured public decks. After a refresh,
manually adjudicate included results and abstract template requirements in
`knowledge/combo-adjudications.json`. A `needs-refresh` manifest entry preserves
old result files as dated evidence without claiming they describe the current
100.

## Apply an intentional deck change

Source synchronization uses the import command above. For a proposed add/cut
package, use guarded change control:

```text
cp changes/change-plan.example.json changes/my-change.json
# Fill in deck, baseline hash, equal Adds/Cuts, and rationale.
just apply-change changes/my-change.json
```

The tool validates the baseline, builds the proposed list in a temporary
location, preserves the commander block, reruns deterministic checks, writes
atomically, and regenerates local artifacts. Recommendations remain `proposed`
until the user confirms or applies them.

## Deck format

Deck files use normalized Moxfield/MTGO text:

```text
1 Card Name
2 A Card Allowed in Multiple Copies
1 Commander Name
```

Blank lines are cosmetic. Commander identity comes from `collection.json`.
Names resolve to Oracle IDs before duplicate and color-identity checks, so flavor
names cannot evade validation. Reports always separate printed lands from
spell/land MDFCs.

## Reports and freshness

[`reports/README.md`](reports/README.md) indexes dated judgment. Report manifests
pin exact deck hashes, and a later refresh produces warnings rather than
silently rewriting old conclusions. Use `just check-current` before describing
external evidence or human conclusions as current.
