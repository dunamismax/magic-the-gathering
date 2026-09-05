# Dated collection reports

Reports in this directory are evidence tied to exact deck hashes. They do not
update themselves when Moxfield lists change.

## Current

- [`commander-social-audit-2026-09-05.md`](commander-social-audit-2026-09-05.md)
  — social-power, combo, and disclosure review of the current 10-deck lineup
- [`commander-bracket-power-evaluation-2026-09-05.md`](commander-bracket-power-evaluation-2026-09-05.md)
  — bracket assignments and relative 1-10 power ranges for the same exact
  10-deck snapshot

`manifest.json` pins both reports to all 10 exact deck hashes. Structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately. Every current list has hash-current full-list Spellbook evidence and
manual prerequisite review. The six changed lists were rescanned on 2026-09-05;
the four unchanged lists retain their original scan and review dates. A
database miss remains evidence rather than proof that no possible interaction
exists.

## Superseded snapshots

- [`commander-social-audit-2026-09-04.md`](commander-social-audit-2026-09-04.md)
- [`commander-bracket-power-evaluation-2026-09-04.md`](commander-bracket-power-evaluation-2026-09-04.md)

These reports describe the previous lists. Their source references resolve to
the retained [September 4 source manifest](../data/moxfield-exports/2026-09-04/manifest.json),
not the mutable current manifest. The previous social report hash is retained
in [`archive/manifest-2026-09-04.json`](archive/manifest-2026-09-04.json).
Superseded Spellbook results and combo reviews are stored in
[`../data/spellbook-results/archive/2026-09-05-superseded/`](../data/spellbook-results/archive/2026-09-05-superseded/).
