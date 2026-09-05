# Commander bracket and power evaluation

Reviewed: 2026-09-05
Profile: <https://moxfield.com/users/dunamismax>
Scope: the 10 exact public Commander lists in `data/moxfield-refresh.json`.

All 10 lists were re-downloaded; six changed by 31 equal-count substitutions.
The changes improve specific engines, interaction, recovery, or mana access.
They do not justify a wholesale revision of the collection's relative power
estimates. The following ranges are medium-confidence list-based judgments;
no game logs or measured goldfish results were supplied.

| Deck | Appropriate conversation | Power estimate | Primary reason |
|---|---|---:|---|
| Pantlaza, Sun-Favored | B3 ceiling; B4 when combo-forward | 8.0-8.5/10 | Discover, tutors, protected conditional fight-chain kills |
| The Notary Hobbits | High B3 | 7.5-8.0/10 | Halfling mana into Eldrazi cast triggers and annihilator |
| Thorin, King of Durin's Folk | Upper B3 | 7.5-8.0/10 | Dwarf/Treasure scaling, tutors, card flow and recovery |
| Henzie “Toolbox” Torre | Mid-to-upper B3 | 7.0-7.5/10 | Blitz, creature ETBs, Birthing Pod and reanimation |
| Aragorn, the Uniter | Mid-to-upper B3 | 7.0-7.5/10 | Multicolor-spell value, trigger multiplication, combat conversion |
| Blor the Impervious | Mid-to-upper B3; Rule Zero until release | 7.0-7.5/10 | Resilient Voltron with improved protection and land access |
| Queen Marchesa | Middle B3 with loop disclosure | 6.5-7.0/10 | Political control, better Sunforger access and interaction |
| Minn, Wily Illusionist | Middle B3 play pattern; discuss Teferi ultimate | 6.5-7.0/10 | Draw/Illusion engines with more instant-speed interaction |
| Gandalf, Party Guest | Maximum Flavor B2-style Rule Zero; Maximum Power B3 by agreement | 6.0-6.5/10 Maximum Flavor | Two exact modes, with the conditional combat loop only in Maximum Power |
| Frodo & Sam | B2* by agreement; otherwise B3 | 5.5-6.5/10 | Hobbit/Food value and the disclosed One Ring exception |

The tables describe play patterns rather than certifying bracket compliance.
Minn's Teferi, Master of Time can take two consecutive extra turns; a table
that excludes that pattern needs an explicit agreement. Gandalf's Maximum
Power configuration similarly requires discussion of its intentional
conditional unlimited-combat finish. No commander, card, or constraint was
changed locally to resolve a table-dependent judgment.

## Effects of the six updates

- Aragorn adds Balmor, Tocasia's Welcome, Cosmic Rebirth, and Winds of Abandon.
  Combat conversion and recovery improve within the same multicolor identity.
- Blor adds two spell/land MDFCs, Hammer of Nazahn, and Krosan Grip. Its 36
  printed lands now have two additional MDFC options; Devoted Druid is absent.
- Thorin adds Chronicle of Victory, Priest of Ancient Lore, two recovery
  spells, and a Mountain. It retains 31 Dwarf creatures and now has 36 printed
  lands plus one MDFC. Molten Echoes is absent.
- Minn adds four counters and three draw spells while cutting seven slots,
  including Minamo. It now has 34 printed lands plus two MDFCs. Flare of Denial
  cannot use a token for its alternative sacrifice cost.
- Queen Marchesa adds three shock lands, Kor Haven, Fighter Class, and four
  political/interaction spells or creatures. Its printed lands fall to 35,
  plus two MDFCs; its existing five-card loop remains present.
- Notary adds Sylvan Library and Tamiyo's Safekeeping over Strionic Resonator
  and The Shire. It now has 36 printed lands plus three MDFCs.

## Construction and evidence boundaries

All 10 mains contain exactly 100 resolved cards and pass the configured audit.
The One Ring in Frodo & Sam remains the only Game Changer. No mass-land-denial
package was identified. Single-land interaction and Eldrazi annihilator still
deserve their own gameplay discussion.

Rule Zero remains necessary for Blor, Minn's The Theorist, Jace Beleren,
Pantlaza's Maular, Notary's Darksteel Angel, and Gandalf's Westward Voyager
color-identity exception. Frodo & Sam's B2* label needs its separate Game
Changer exception. Gandalf's sideboard switch is unchanged.

See the [social audit](commander-social-audit-2026-09-05.md) for exact combo
conditions, source changes, policy citations, and release dates. It uses the
2026-09-05 Oracle and policy checks, fresh Spellbook scans for all six changed
lists, and retained hash-matching evidence for the four unchanged lists.
`reports/manifest.json` pins both reports and all 10 deck hashes. Combo
completeness and actual game speed remain uncertain beyond those checks.
