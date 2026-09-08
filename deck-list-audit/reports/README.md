# Dated collection reports

Reports in this directory are evidence tied to exact deck hashes. They do not
update themselves when Moxfield lists change.

## Current

- [`commander-social-audit-2026-09-08.md`](commander-social-audit-2026-09-08.md)
  — social-power, combo, and disclosure review of the current 11-deck lineup
- [`commander-bracket-power-evaluation-2026-09-08.md`](commander-bracket-power-evaluation-2026-09-08.md)
  — bracket and play-pattern descriptions, including Smaug's B4 combo role

`manifest.json` pins both reports to all 11 exact deck hashes. Structured adjudications in
`../knowledge/combo-adjudications.json` pin the underlying combo findings
separately. Every current list has hash-current full-list Spellbook evidence and
manual prerequisite review. Smaug was scanned and reviewed on 2026-09-08;
all ten existing lists retain their original scan and review dates after fresh
exports confirmed no card changes. The public Smaug primer's three absent-card
references and a corrected Spellbook Fiendlash claim are documented. A
database miss remains evidence rather than proof that no possible interaction
exists.

## Superseded snapshots

- [`commander-social-audit-2026-09-05.md`](commander-social-audit-2026-09-05.md)
- [`commander-bracket-power-evaluation-2026-09-05.md`](commander-bracket-power-evaluation-2026-09-05.md)
- [`commander-social-audit-2026-09-04.md`](commander-social-audit-2026-09-04.md)
- [`commander-bracket-power-evaluation-2026-09-04.md`](commander-bracket-power-evaluation-2026-09-04.md)

These reports describe earlier collections. Use the retained
[September 5 source manifest](../data/moxfield-exports/2026-09-05/manifest.json)
or [September 4 source manifest](../data/moxfield-exports/2026-09-04/manifest.json)
for their exact snapshots, even when historical prose names the mutable current
manifest. Previous report hashes are retained in
[`archive/manifest-2026-09-05.json`](archive/manifest-2026-09-05.json) and
[`archive/manifest-2026-09-04.json`](archive/manifest-2026-09-04.json).
Superseded Spellbook results and combo reviews are stored in
[`../data/spellbook-results/archive/2026-09-05-superseded/`](../data/spellbook-results/archive/2026-09-05-superseded/).
