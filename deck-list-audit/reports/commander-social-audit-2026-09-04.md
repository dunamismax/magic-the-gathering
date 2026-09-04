# dunamismax 10-deck social-power audit

Reviewed: 2026-09-04
Profile: <https://moxfield.com/users/dunamismax>
Scope: the exact 10 public main-deck lists and hashes recorded in
`data/moxfield-refresh.json`, plus Gandalf's separately pinned nine-for-nine switch

This report uses the current Oracle corpus, official Commander policy checked on
2026-09-04, exact-list Commander Spellbook evidence, and manual prerequisite
review. Thorin is the newly added deck in the active lineup.

## Lineup view

The public profile shows nine Bracket 3 decks and one Bracket 2* deck. Gandalf's
posted label is B3, while its Maximum Flavor list still plays as a B2-style Rule
Zero configuration; the exact nine-for-nine sideboard switch is its streamlined
B3 Maximum Power mode. Frodo & Sam contains The One Ring, so its B2* label needs
a bracket-exception discussion and otherwise belongs at B3.

| Side-eye rank | Deck | Posted target | Current pod judgment | Main pressure | Exact-list combo result |
|---:|---|---:|---|---|---|
| 1 | Pantlaza | B3 | Ceiling B3; disclose before blind games | Discover, tutors, protected Apex fight chain | Three conditional near-infinite lines |
| 2 | The Notary Hobbits | B3 | High-end B3 | Sudden 9-25 mana, Eldrazi cast triggers, annihilator | No complete line |
| 3 | Thorin | B3 | Upper B3 | Dwarf ETBs, Treasure scaling, trigger/token multipliers, Magda toolbox | No complete line |
| 4 | Aragorn | B3 | Mid-to-upper B3 | Four-color efficiency, trigger doublers, go-wide pressure | No complete line |
| 5 | Henzie | B3 | Mid-to-upper B3 | Blitz value, Birthing Pod, reanimation, large ETBs | Returned persist template is incomplete |
| 6 | Blor | B3 | Mid-to-upper B3; Rule Zero today | Resilient Voltron and commander-damage multipliers | No complete line |
| 7 | Queen Marchesa | B3 | Middle B3 with loop disclosure | Political control, redirection, Sunforger/Wishclaw access | One finite kill and one five-card unbounded loop |
| 8 | Minn | B3 | Middle B3; Rule Zero today | Draw multiplication, Illusions, sacrifice outlets | No complete line |
| 9 | Gandalf | B3 posted | Maximum Flavor Rule Zero main; sideboard switches to B3 Maximum Power | Eleven Gandalfs and free spells each combat | No Maximum Flavor line; Maximum Power has one conditional loop |
| 10 | Frodo & Sam | B2* | Upper B2 by play pattern; B3 without a bracket exception | Food/Hobbit value, Ring pressure, The One Ring | No complete line |

The order measures likely blind-pod concern. The middle can move with a pod's
tolerance for tutors, political control, explosive combat, and hard-to-answer
commanders.

## Construction and policy facts

All 10 main decks resolve to exactly 100 cards and pass commander configuration,
singleton, banned-card, and configured exception checks. The collection has one
Game Changer, in Frodo & Sam.

| Deck | Printed lands | Spell/land MDFCs | Game Changers | Current exception |
|---|---:|---:|---:|---|
| Aragorn | 36 | 1 | 0 | None |
| Blor | 36 | 0 | 0 | Blor releases 2026-11-09 |
| Frodo & Sam | 36 | 0 | 1 | The One Ring in posted B2* list |
| Gandalf | 34 | 3 | 0 | Westward Voyager is outside Jeskai identity |
| Henzie | 34 | 4 | 0 | None |
| Minn | 35 | 2 | 0 | The Theorist, Jace Beleren releases 2026-10-02 |
| Pantlaza | 35 | 3 | 0 | Maular releases 2026-11-09 |
| Queen Marchesa | 36 | 2 | 0 | None |
| The Notary Hobbits | 37 | 3 | 0 | Darksteel Angel releases 2026-10-02 |
| Thorin | 35 | 2 | 0 | None |

## Thorin finding

Thorin is an all-Dwarf Boros engine. Every Dwarf entering creates a Treasure and
turns the existing artifact-token count into a team-wide power boost. Bifur,
Panharmonicon, Anointed Procession, Cadric, Molten Echoes, and Fíli multiply
those triggers, Treasures, temporary legendary copies, or Dwarf bodies. Magda
adds a repeatable artifact tutor, while Dwarven Recruiter, protection spells,
Cavern of Souls, The Reaver Cleaver, and Akroma's Will make the deck consistent
and difficult to blunt once it develops.

The exact-list Spellbook scan returned no included combo. Manual review agrees:
the token and trigger multipliers are finite, Dwarven Bloodboiler has no
repeatable untap engine, and the list omits Aggravated Assault, Hellkite Charger,
and Clock of Omens. The closest extra-combat and Magda templates are therefore
incomplete. Upper B3 is appropriate because the command-zone scaling, tutors,
free protection, and explosive combat create real pressure without a complete
loop.

## Other refreshed lists

Henzie now uses premium lands and graveyard tools including Metamorphosis Fanatic
and Tortured Existence, plus Kardur for combat control; it removes Sol Ring, two
one-mana Elves, Veil of Summer, and several slower lands. The exact-list scan
still returns only the Mikaeus and Viscera Seer template, which remains
incomplete because the deck has no persist creature. Its mid-to-upper B3
judgment is unchanged.

Frodo & Sam replaces Terramorphic Expanse with Hobbit Hole. Counts, Game
Changer status, combo result, and bracket judgment are unchanged.

## Existing combo disclosures

- Pantlaza retains the three Apex Altisaur and Wrathful Raptors lines using
  Savage Order, Flawless Maneuver, or Akroma's Will.
- Queen Marchesa retains the finite Fire Covenant and Brash Taunter kill and
  the five-card Arcbond, Return the Favor, Boros Charm, Selfless Squire, and
  Brash Taunter loop.
- Henzie's Mikaeus and Viscera Seer template remains incomplete because the
  exact list has no persist creature.
- Gandalf's Surge to Victory and Savage Beating line exists only after applying
  the exact nine-for-nine Maximum Power switch.

## Evidence boundaries

Structured findings live in `knowledge/combo-adjudications.json`. Every current
main deck has hash-current Spellbook evidence and manual prerequisite review.
A database miss and a manual screen are evidence, not proof that no possible
interaction exists.
