# Dated collection reports

Reports in this directory are evidence tied to exact deck hashes. They do not
update themselves when Moxfield lists change.

## Current

- [`commander-social-audit-2026-09-04.md`](commander-social-audit-2026-09-04.md)
  — social-power, combo, and disclosure review of the current 10-deck lineup
- [`commander-bracket-power-evaluation-2026-09-04.md`](commander-bracket-power-evaluation-2026-09-04.md)
  — bracket assignments and relative 1-10 power ranges for the same exact
  10-deck snapshot

`manifest.json` pins the social-power report to all 10 exact deck hashes. The
bracket/power companion records the same snapshot through
`data/moxfield-refresh.json`. The structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately. All 10 lists have hash-current full-list Spellbook evidence and
manual prerequisite review. The current reports still treat a database miss as
evidence rather than proof that no possible interaction exists.

## Superseded

- [`commander-social-audit-2026-09-01.md`](commander-social-audit-2026-09-01.md)
  and [`commander-bracket-power-evaluation-2026-09-01.md`](commander-bracket-power-evaluation-2026-09-01.md)
  — previous 10-deck lineup before Ekthi retired, Notary joined, and three
  retained decks changed

- [`commander-social-audit-2026-08-30.md`](commander-social-audit-2026-08-30.md)
  — exact seven-deck social review before the three Middle-earth additions
- [`commander-bracket-power-evaluation-2026-08-30.md`](commander-bracket-power-evaluation-2026-08-30.md)
  — exact seven-deck bracket and power companion

## Archive

- [`archive/commander-social-audit-2026-08-29.md`](archive/commander-social-audit-2026-08-29.md)
  — retained seven-deck subset of the previous social-power review
- [`archive/combo-adjudications-2026-08-29.json`](archive/combo-adjudications-2026-08-29.json)
  — structured combo findings for the previous exact hashes

The archived files retain seven decks from the previous snapshot for comparison;
they are no longer the full original lineup and must not be applied to the
current hashes.
