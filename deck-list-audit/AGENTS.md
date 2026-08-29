# Commander collection operating contract

This folder is the source-controlled operating system for Sawyer's Commander
collection. Treat deck advice and deck edits as stateful, audited work.

## Start every task here

1. Read `collection.json` and the relevant deck file in `decks/`.
2. Run `just check` before relying on generated evidence. If it fails, explain
   the stale or invalid layer before making a current claim.
3. Use the rubric matching the request in `rubrics/`:
   - full evaluation: `evaluate.md`
   - minimal, high-confidence tuning: `tune-conservative.md`
   - coordinated structural tuning: `tune-structural.md`
   - collection comparison: `collection-review.md`
4. Treat `decks/*.txt` and `collection.json` as human-owned source files.
   Treat `data/audit.json`, `data/spellbook-requests/`, and `generated/` as
   generated artifacts.

## Non-negotiable audit rules

- Evaluate the exact current list, never a remembered or earlier version.
- Machine-count quantities. Report printed lands separately from spell/land
  modal double-faced cards.
- Verify all 100 cards resolve before asserting legality, category totals, or
  Game Changer counts.
- Verify count, commander configuration, singleton exceptions, color identity,
  Commander legality, release timing, banned status, Game Changers, and known
  combo-policy constraints after every adopted change.
- Game Changer count does not determine bracket by itself. Also evaluate speed,
  tutors, fast mana, deterministic lines, extra turns, locks, land denial,
  resilience, interaction, replayability, and opponent agency.
- Distinguish objective validation from judgment. Use explicit confidence and
  evidence dates for bracket, speed, salt, and combo-completeness conclusions.
- A Commander Spellbook miss is not proof that no combo exists. Consult
  `knowledge/combo-adjudications.json` and manually inspect commander-specific
  interactions and newly released cards.
- Respect `constraints` in `collection.json` as hard requirements. Preview or
  Rule Zero cards listed there are not automatic cuts.

## Advice and change-state rules

- Clearly label a package `proposed`, `applied`, or `user-confirmed`.
- Do not edit a deck for a review-only request.
- For an authorized edit, create a change plan from
  `changes/change-plan.example.json` and use `just apply-change PLAN=...`.
- Never bypass the baseline SHA-256 guard or hand-edit generated artifacts.
- Adds and cuts must have equal total quantities. Present actionable card
  packages in one Moxfield-ready fenced block with one `1 Card Name` per line.
- Preserve the commander-specific identity and stated play experience; stop at
  sidegrades when the user asks for conservative or high-impact-only work.
- Never sync changes back to Moxfield or another external service without a
  separate explicit request.

## Freshness and privacy

- `just check-current` is required before calling an audit current. If current
  verification is unavailable, state the exact locked snapshot dates.
- Oracle bulk data may be refreshed locally with `just refresh-oracle`.
- Moxfield refresh is local-import only: use a user-provided MTGO text export.
- Do not upload a complete private decklist to any third party. Commander
  Spellbook refresh requires both `visibility: public` in `collection.json` and
  the explicit `--allow-deck-upload` command flag.

## Completion gate

Before finalizing deck work, run `just check`. Report any remaining warning,
stale external analysis, Rule Zero dependency, or subjective uncertainty.
