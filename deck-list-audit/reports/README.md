# Dated collection reports

Reports in this directory are evidence tied to exact deck hashes. They do not
update themselves when Moxfield lists change.

## Current

- [`commander-social-audit-2026-09-01.md`](commander-social-audit-2026-09-01.md)
  — social-power, combo, and disclosure review of the current 10-deck lineup
- [`commander-bracket-power-evaluation-2026-09-01.md`](commander-bracket-power-evaluation-2026-09-01.md)
  — bracket assignments and relative 1-10 power ranges for the same exact
  10-deck snapshot

`manifest.json` pins the social-power report to all 10 exact deck hashes. The
bracket/power companion records the same snapshot through
`data/moxfield-refresh.json`. The structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately. Full-list Spellbook refreshes remain explicitly pending for the
three new decks and revised Minn; the current reports identify that evidence
boundary rather than treating a missing scan as proof of absence.

## Superseded

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
