# dunamismax 10-deck social-power audit

Reviewed: 2026-09-01  
Profile: <https://moxfield.com/users/dunamismax>  
Scope: the exact 10 public lists and hashes recorded in `data/moxfield-refresh.json`

This report combines the deterministic Oracle audit, the 2026-08-29 official
policy lock, hash-current exact-list Commander Spellbook evidence for all ten
decks, and manual Oracle/prerequisite review. The 2026-09-01 scans for Aragorn,
Frodo and Sam, Gandalf, and revised Minn returned zero included candidates.

## Lineup view

The current lineup has nine Bracket 3 decks and one Bracket 2 deck. Pantlaza
remains the sharpest blind-pod risk because its exact list contains a tutored
conditional near-infinite damage line. Gandalf is the strongest new addition:
each extra combat retriggers its free-spell commander ability, producing large
but finite turns. Frodo and Sam are the clear lower-power landing point and fit
upper Bracket 2.

| Side-eye rank | Deck | Target | Current pod judgment | Main pressure | Exact-list combo result |
|---:|---|---:|---|---|---|
| 1 | Pantlaza | B3 | Ceiling B3; disclose before blind games | Discover, tutors, protected Apex fight chain | Three conditional near-infinite lines |
| 2 | Gandalf | B3 | Upper B3 | Free spells at every combat, tutors, extra combats | No complete line; finite extra-combat chain |
| 3 | Magda | B3 | Upper B3 | Repeatable command-zone artifact/Dragon tutor | No complete line |
| 4 | Queen Marchesa | B3 | Middle B3 with loop disclosure | Political control, redirection, Sunforger/Wishclaw access | One finite kill and one five-card unbounded loop |
| 5 | Aragorn | B3 | Mid-to-upper B3 | Four-color efficiency, trigger doublers, go-wide pressure | No complete line |
| 6 | Henzie | B3 | Mid-to-upper B3 | Blitz value, Birthing Pod, reanimation, large ETBs | Returned persist template is incomplete |
| 7 | Blor | B3 | Mid-to-upper B3; Rule Zero today | Resilient Voltron and commander-damage multipliers | No complete line |
| 8 | Minn | B3 | Middle B3; Rule Zero today | Draw multiplication, Illusions, sacrifice outlets | No complete line |
| 9 | Ekthi | B3 | Middle B3; Rule Zero today | Equipment tutoring and low-cost equip turns | No complete line |
| 10 | Frodo & Sam | B2 | Upper B2 | Food/Hobbit value, Ring pressure, creature combat | No complete line |

The order measures likely blind-pod concern, not deck quality or pilot fun.
Familiar pods can reorder the middle freely depending on their tolerance for
tutors, political control, hard-to-answer commanders, and explosive combat.

## Construction and policy facts

All 10 lists resolve 100 of 100 cards and pass commander configuration,
singleton, color identity, Commander legality, banned-card, release-state, and
configured Game Changer checks. All 10 currently contain zero cards marked as
Game Changers; that count does not settle bracket fit.

| Deck | Printed lands | Spell/land MDFCs | Game Changers | Current release note |
|---|---:|---:|---:|---|
| Aragorn | 36 | 1 | 0 | Legal |
| Blor | 36 | 0 | 0 | `Blor the Impervious` releases 2026-11-09; Rule Zero today |
| Ekthi | 34 | 1 | 0 | `Ekthi, Contaminator Priest` releases 2026-11-09; Rule Zero today |
| Frodo & Sam | 37 | 0 | 0 | Legal |
| Gandalf | 34 | 3 | 0 | Legal |
| Henzie | 34 | 4 | 0 | Legal |
| Magda | 35 | 0 | 0 | Legal |
| Minn | 35 | 2 | 0 | `The Theorist, Jace Beleren` releases 2026-10-02; Rule Zero today |
| Pantlaza | 35 | 3 | 0 | `Maular, the Next Evolution` releases 2026-11-09; Rule Zero today |
| Queen Marchesa | 36 | 2 | 0 | Legal |

## New and changed deck findings

### Gandalf, Party Guest

At the beginning of every combat on its controller's turn, Gandalf can cast a
qualifying instant or sorcery from hand for free. `World at War` and the
extra-combat mode of `Savage Beating` therefore create another Gandalf trigger
as well as another attack. `Solve the Equation` and `Muddle the Mixture`
increase access, while Harmonic Prodigy, Roaming Throne, Veyran, and Wizard's
Staff multiply other Wizard and spell triggers.

The sequence is finite in this exact 100. The extra-combat spells do not recur
themselves, and the list has no repeatable combat or spell-recursion loop. The
pregame concern is repeated free spells and a high-ceiling combat chain, not a
hidden deterministic combo.

### Aragorn, the Uniter

Aragorn converts multicolored spells into tokens, scry, direct damage, and
combat power. Annie Joins Up and Roaming Throne double relevant triggers, while
Jeskai Ascendancy untaps Bloom Tender, Faeburrow Elder, Birds, and the other
mana creatures during a noncreature-spell chain.

The exact list has no buyback spell, zero-cost recast engine, or creature loop
that converts those untaps into a deterministic cycle. Its strongest turns
remain finite multicolor-spell chains backed by premium four-color mana and
interaction.

### Frodo & Sam

The deck's Hobbit, Food, and Ring engines are synergistic but deliberately
incremental. Peregrin Took, Rosie Cotton, Samwise Gamgee, Mirkwood Bats, and
Tireless Provisioner reward token creation; Sam reduces Food activation costs;
Frodo turns repeated life gain and attacks into Ring progress and cards.

No current line recreates the spent Foods, mana, or historic card at no net
cost. Prize Pig can untap after life gain, but Food activations still consume
mana and tokens. With 37 lands, land-focused ramp, broad but fair interaction,
and no deterministic finish, the list fits upper Bracket 2.

### Revised Minn

Minn shifted away from several broad value cards toward more Illusions and
draw-multiplication pieces. Ashnod's Altar, Phyrexian Altar, and Blasting
Station still convert Illusions into finite value, but the list has no effect
that returns a sacrificed Illusion or recreates a token from the sacrifice
itself. Thought Reflection and Teferi's Ageless Insight multiply draws without
forming a loop. The revision remains a fairer middle-Bracket-3 value deck.

## Existing combo disclosures

Pantlaza retains three `Apex Altisaur` + `Wrathful Raptors` lines using
`Savage Order`, `Flawless Maneuver`, or `Akroma's Will`. They produce a
one-sided creature clear and can deal near-infinite damage when the opposing
battlefield keeps Apex's fight chain going.

Queen Marchesa retains the finite `Fire Covenant` + `Brash Taunter` kill
and the five-card `Arcbond` / `Return the Favor` / `Boros Charm` /
`Selfless Squire` / `Brash Taunter` unbounded damage loop. Henzie's
Mikaeus/Viscera Seer template remains incomplete because the exact list has no
persist creature.

## Pregame disclosures

- **Pantlaza:** disclose the Savage Order/Apex Altisaur/Wrathful Raptors line.
- **Queen Marchesa:** disclose the clunky five-card Arcbond loop and finite
  Fire Covenant/Brash Taunter kill.
- **Gandalf:** disclose that extra combats retrigger the commander's free spell.
- **Magda:** disclose the repeatable command-zone artifact/Dragon tutor despite
  the absence of a current infinite line.
- **Blor, Ekthi, Minn, and Pantlaza before release:** identify the Rule Zero card
  listed in the construction table.

## Evidence boundaries

Structured findings live in `knowledge/combo-adjudications.json`. Six unchanged
lists retain hash-current 2026-08-30 Spellbook evidence; the three new lists and
revised Minn have 2026-09-01 exact-list scans. All ten records also have manual
prerequisite review. Neither a database miss nor a manual screen proves absolute
absence; rerun `just check-current` after any deck edit or evidence expiry.
