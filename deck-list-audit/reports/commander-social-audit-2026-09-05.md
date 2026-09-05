# dunamismax 10-deck social-power audit

Reviewed: 2026-09-05
Profile: <https://moxfield.com/users/dunamismax>
Scope: all 10 public Commander mains in `data/moxfield-refresh.json`, plus
Gandalf's separately pinned nine-for-nine configuration switch.

All 10 lists were freshly downloaded. Six lists changed, with 31 cards replaced
in total. No Commander decks were added, removed, or renamed. The owner has
explicitly kept the repository Commander-only.

## Source changes and construction

Every main resolves to exactly 100 cards and passes commander configuration,
singleton, banned-card, color-identity, release-state, and configured exception
checks. Passing with a configured exception does not establish ordinary
Commander legality for that exception.

| Deck | Cards replaced | Printed lands | Spell/land MDFCs | Game Changers | Required exception |
|---|---:|---:|---:|---:|---|
| Aragorn | 4 | 36 | 1 | 0 | None |
| Blor | 4 | 36 | 2 | 0 | Blor releases 2026-11-09 |
| Frodo & Sam | 0 | 36 | 0 | 1 | The One Ring in the posted B2* list |
| Gandalf | 0 | 34 | 3 | 0 | Westward Voyager is outside Jeskai identity |
| Henzie | 0 | 34 | 4 | 0 | None |
| Minn | 7 | 34 | 2 | 0 | The Theorist, Jace Beleren releases 2026-10-02 |
| Pantlaza | 0 | 35 | 3 | 0 | Maular releases 2026-11-09 |
| Queen Marchesa | 9 | 35 | 2 | 0 | None |
| The Notary Hobbits | 2 | 36 | 3 | 0 | Darksteel Angel releases 2026-10-02 |
| Thorin | 5 | 36 | 1 | 0 | None |

The complete applied adds/cuts and before/after hashes are recorded in
[`changes.json`](../data/moxfield-exports/2026-09-05/changes.json). Four mains
and Gandalf's nine-card sideboard are unchanged. The collection still contains
one Game Changer: The One Ring in Frodo & Sam.

## Gameplay effects of the refresh

Aragorn gains Balmor's team pump and trample, Tocasia's Welcome for the small
creature/token plan, Cosmic Rebirth for recovery, and Winds of Abandon for
asymmetric removal. Bard Class, Gold-Forged Thopteryx, Jhoira, and Time Wipe
leave. These changes support the existing multicolor-spell and combat identity.
No repeatable spell engine completes the Jeskai Ascendancy/mana-creature lines.

Blor replaces Blackblade Reforged, Devoted Druid, Epic Fight, and Sawtusk
Demolisher with Bala Ged Recovery, Bridgeworks Battle, Hammer of Nazahn, and
Krosan Grip. The two MDFCs increase land access while retaining spell functions.
Its pressure remains finite commander damage, with additional Equipment support
and interaction. The closest Hammer of Nazahn line lacks Apex Altisaur.

Thorin replaces Bruenor, Liquimetal Torque, Molten Echoes, Sundering Eruption,
and Warleader's Call with Ascend from Avernus, Chronicle of Victory, one
Mountain, Priest of Ancient Lore, and Sevinne's Reclamation. The deck retains
31 Dwarf creatures, adds recovery and cast-based draw, and exchanges one
spell/land MDFC for a printed land. Magda, Treasure scaling, Bifur, Cadric,
Panharmonicon, and Anointed Procession remain powerful finite engines.

Minn shifts seven slots toward countermagic and instant-speed draw. Abjure can
sacrifice a blue Illusion token; Flare of Denial requires a **nontoken** blue
creature. Flow of Knowledge, Thirst for Discovery, and Thirst for Knowledge
support second-draw and discard decisions. Cutting Minamo reduces the mana base
to 34 printed lands plus two MDFCs. None of these one-shot effects supplies an
unrestricted sacrifice/recursion cycle.

Queen Marchesa improves fixing with three shock lands, adds Kor Haven, and
exchanges several gift/value slots for Fighter Class, Combat Calligrapher,
Nils, Galadriel's Dismissal, and Tibalt's Trickery. Fighter Class improves access
to Sunforger. The deck has one fewer printed land and retains both its finite
Fire Covenant/Brash Taunter kill and its conditional Arcbond loop.

Notary replaces Strionic Resonator and The Shire with Sylvan Library and
Tamiyo's Safekeeping. Selection and protection improve while one printed land
and one trigger-copy effect leave. The Halfling mana engine still funds Eldrazi
cast triggers, annihilator, and combat; no repeatable untap or recast engine was
identified in the revised 100.

## Pod fit and disclosures

The profile still shows nine B3 labels and one B2* label. List-based judgments
remain broadly consistent with the previous review; the six packages change
consistency, interaction, or recovery without establishing a new fast combo.
These are medium-confidence play-pattern judgments, not measured win rates or
goldfish turn estimates.

| Deck | Current pod judgment | Main pregame discussion |
|---|---|---|
| Pantlaza | B3 ceiling; stronger when deliberately tutoring its kill | Protected Apex Altisaur/Wrathful Raptors fight chains |
| The Notary Hobbits | High B3 | Explosive mana, annihilator, Emrakul turn control, Rise of the Eldrazi |
| Thorin | Upper B3 | Treasure scaling, Magda/Dwarven Recruiter access, recovery and combat bursts |
| Aragorn | Mid-to-upper B3 | Trigger multiplication, efficient interaction, wide combat finishes |
| Henzie | Mid-to-upper B3 | Blitz, Birthing Pod, reanimation and large creature triggers |
| Blor | Mid-to-upper B3 by play pattern; Rule Zero until release | Trample/hexproof/indestructible commander and damage multipliers |
| Queen Marchesa | Middle B3 with explicit loop disclosure | Political control, Sunforger/Wishclaw access, five-card loop |
| Minn | Middle B3 by play pattern, with an extra-turn caveat | Draw/Illusion engines, sacrifice outlets, Teferi ultimate, unreleased Jace |
| Gandalf | Maximum Flavor B2-style Rule Zero; Maximum Power B3 by agreement | Exact nine-for-nine switch and alternate-mode unlimited combats |
| Frodo & Sam | Upper B2 play pattern; B3 absent a bracket exception | The One Ring in the posted B2* configuration |

Minn's Teferi, Master of Time can take two consecutive extra turns with its
ultimate. That capability needs explicit discussion for a table that excludes
consecutive extra turns; the posted B3 label is not blanket policy clearance.
Notary's Rise of the Eldrazi grants its caster an extra turn and exiles itself.
Emrakul, the Promised End instead controls an opponent's next turn and gives
that opponent the subsequent extra turn. These effects deserve separate
disclosure from any infinite-combo claim.

## Exact-list combo review

All six changed decks received full-list Commander Spellbook scans on
2026-09-05. Five returned no included candidates; Queen Marchesa returned the
same Fire Covenant/Brash Taunter candidate. Manual review checked the changed
cards, remaining engines, and missing named/template prerequisites.

- Queen Marchesa's Fire Covenant line is finite and limited by life payments.
  Its five-card loop still uses Arcbond, Return the Favor, Boros Charm, Selfless
  Squire, and Brash Taunter. The Squire's enter trigger must have resolved that
  turn, both creatures must survive, and Brash must be able to activate its
  fight ability. The two Arcbond triggers then feed each other while damage to
  the pilot is prevented.
- Pantlaza's unchanged scan contains three Apex Altisaur/Wrathful Raptors
  candidates, with Savage Order, Flawless Maneuver, or Akroma's Will. Damage is
  normally bounded by opposing fight targets; an opposing indestructible
  creature with positive power can sustain the loop. Protection and other
  prevention effects can change whether the fight actually deals damage.
- Henzie's unchanged Mikaeus/Viscera Seer template lacks a persist creature.
- Gandalf's unchanged Maximum Flavor main contains neither Surge to Victory
  nor Savage Beating. The exact nine-for-nine Maximum Power switch restores
  the intentional conditional unlimited-combat line and requires disclosure.

Structured findings and review dates are pinned in
[`combo-adjudications.json`](../knowledge/combo-adjudications.json). No new
complete combo was identified in the six changed lists. A database miss plus a
manual screen remains evidence, not proof of the absence of every possible
interaction.

## Evidence

Oracle was refreshed on 2026-09-05. Official
[Commander format and Game Changer guidance](https://magic.wizards.com/en/formats/commander),
the [February bracket update](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-february-9-2026),
and the [banned list](https://magic.wizards.com/en/banned-restricted-list) were
rechecked the same day. Policy intent and pregame agreement remain controlling.

The four unchanged mains retain their original hash-matching Spellbook scan
and manual review dates. Superseded scans and adjudications are stored under
`data/spellbook-results/archive/2026-09-05-superseded/`. The previous source
manifest is retained under `data/moxfield-exports/2026-09-04/manifest.json`.
This report's manifest pins all 10 current deck hashes.
