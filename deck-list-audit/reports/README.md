# Dated collection reports

Reports in this directory are evidence tied to exact deck hashes. They do not
update themselves when Moxfield lists change.

## Current

- [`commander-social-audit-2026-08-30.md`](commander-social-audit-2026-08-30.md)
  — social-power and combo review of the current 10-deck lineup
- [`commander-bracket-power-evaluation-2026-08-30.md`](commander-bracket-power-evaluation-2026-08-30.md)
  — decisive bracket assignments and relative 1-10 power ranges for the same
  exact 10-deck snapshot

`manifest.json` pins the social-power report to all 10 exact deck hashes. The
bracket/power companion records the same snapshot through
`data/moxfield-refresh.json`. The structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately.

## Archive

- [`archive/commander-social-audit-2026-08-29.md`](archive/commander-social-audit-2026-08-29.md)
  — social-power review of the previous nine-deck lineup
- [`archive/combo-adjudications-2026-08-29.json`](archive/combo-adjudications-2026-08-29.json)
  — structured combo findings for the previous exact hashes

The archived files remain useful for comparing the previous nine-deck snapshot,
but they must not be applied to the current hashes.
