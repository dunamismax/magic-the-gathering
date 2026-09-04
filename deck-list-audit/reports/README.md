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
`data/moxfield-refresh.json`. Structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately. Every current list has hash-current full-list Spellbook evidence and
manual prerequisite review. A database miss remains evidence rather than proof
that no possible interaction exists.
