# dunamismax 8-deck social-power audit

Reviewed: 2026-08-30  
Profile: <https://moxfield.com/users/dunamismax>  
Scope: the exact 8 public lists and hashes recorded in `data/moxfield-refresh.json`

This report combines the deterministic Oracle audit, the 2026-08-29 official
policy lock, full-list Commander Spellbook scans refreshed on 2026-08-30, and
manual review of returned prerequisites and newer cards. Commander Spellbook's
estimate is evidence rather than the final social judgment.

## Lineup view

The lineup remains strongly themed and varied. Pantlaza is the clear outlier:
Commander Spellbook tags it `R` (Ruthless) because the exact list contains
three Apex Altisaur and Wrathful Raptors lines. The other seven estimates are
`E` (Exhibition), although several still play above a relaxed table through
command-zone tutoring, repeated free spells, or explosive combat scaling.

| Side-eye rank | Deck | Target | Current pod judgment | Main pressure | Exact-list combo result |
|---:|---|---:|---|---|---|
| 1 | Pantlaza | B3 | Ruthless estimate; disclose before B3 games | Discover, creature tutors, protected Apex fight chain | Three conditional near-infinite lines |
| 2 | Magda | B3 | Upper B3 | Repeatable command-zone artifact/Dragon tutor | No complete combo |
| 3 | Queen Marchesa | B3 | Upper B3 with loop disclosure | Political control, redirection, Sunforger/Wishclaw access | One finite kill and one five-card unbounded loop |
| 4 | Minn | B3 | Upper B3 | Draw-trigger multiplication, free permanents, sacrifice outlets | No complete combo |
| 5 | Henzie | B3 | Mid-to-upper B3 | Blitz value, Birthing Pod, reanimation, large ETBs | Returned persist template is incomplete |
| 6 | Blor | B3 | Upper B3, Rule Zero today | Resilient Voltron and sudden commander-damage multipliers | No complete combo |
| 7 | Ekthi | B3 | Mid-to-upper B3, Rule Zero today | Equipment tutoring and low-cost equip turns | No complete combo |
| 8 | The Fifth Doctor + Susan Foreman | B2 | Good B2/Exhibition fit | Tap/untap value, counters, Vehicles, and combat | No complete combo |

The ranking measures likely blind-pod concern, not deck quality. A familiar pod
can place Magda, Queen, Minn, Henzie, Blor, and Ekthi in a different order
depending on its tolerance for tutors, commander damage, and snowballing value.

## Construction and policy facts

All 8 lists resolve 100 of 100 cards, pass singleton and color-identity checks,
and contain zero cards marked as Game Changers in the current Oracle snapshot.
That zero does not settle bracket fit; Pantlaza's complete lines and Magda's
command-zone tutor are examples of pressure that the count does not express.

| Deck | Printed lands | Spell/land MDFCs | Game Changers | Current release note |
|---|---:|---:|---:|---|
| Blor | 36 | 0 | 0 | `Blor the Impervious` releases 2026-11-09; Rule Zero today |
| Ekthi | 34 | 1 | 0 | `Ekthi, Contaminator Priest` releases 2026-11-09; Rule Zero today |
| Henzie | 34 | 4 | 0 | Legal |
| Magda | 35 | 0 | 0 | Legal |
| Minn | 35 | 2 | 0 | `The Theorist, Jace Beleren` releases 2026-10-02; Rule Zero today |
| Pantlaza | 35 | 3 | 0 | `Maular, the Next Evolution` releases 2026-11-09; Rule Zero today |
| Queen Marchesa | 36 | 2 | 0 | Legal |
| The Fifth Doctor + Susan Foreman | 37 | 0 | 0 | Legal |

## Combo and high-pressure findings

### Pantlaza

The current 100 contains all three Commander Spellbook results:

- `Apex Altisaur` + `Wrathful Raptors` + `Savage Order`
- `Apex Altisaur` + `Wrathful Raptors` + `Flawless Maneuver`
- `Apex Altisaur` + `Wrathful Raptors` + `Akroma's Will`

These lines make Apex indestructible, repeatedly fight opposing creatures, and
route the resulting damage through Wrathful Raptors. They always threaten a
one-sided creature clear and can produce near-infinite player damage when the
opposing battlefield supplies a durable positive-power creature. `Savage
Order` is the most concerning version because one spell both finds Apex and
grants indestructible. This is enough to make a no-disclosure blind B3 game a
poor fit even though the deck remains Dinosaur-centered.

### Queen Marchesa

`Fire Covenant` + `Brash Taunter` is a finite, life-limited kill: paying life
equal to an opponent's life total sends that much damage through the Taunter.

The manual pass also found a five-card unbounded line:

1. Resolve `Selfless Squire` so damage to you is prevented for the turn.
2. Give your permanents indestructible with `Boros Charm`.
3. Cast `Arcbond` targeting `Brash Taunter`; copy it with `Return the Favor`
   and target the Squire with the copy.
4. Activate Brash Taunter so it fights the Squire.
5. Each creature's Arcbond trigger damages the other and creates the next
   trigger. Opponents take damage on every iteration while the Squire's effect
   protects you.

This is a costly five-card assembly rather than a compact plan, but it is a
deterministic loop and should be disclosed under the collection's `disclose`
combo policy.

### Henzie

Commander Spellbook returned `Mikaeus, the Unhallowed` + `Viscera Seer` with a
generic persist-creature requirement. The exact 100 has no creature with
persist, so the returned template cannot run. The other death and reanimation
cards recur creatures a bounded number of times.

### Remaining five decks

Blor, Ekthi, Magda, Minn, and The Fifth Doctor returned no
included combo. Manual review did not find a replacement among the likely
engines:

- Magda has many ways to tap Dwarves, but no repeatable untap engine; its
  Treasure and tutor chains stop.
- Minn's Altars and Blasting Station consume a finite supply of Illusions.
  Krang and Homunculus Horde multiply a second-draw event without recreating it.
- The Fifth Doctor's two Helix effects lack a free recast/untap engine, and
  Basking Broodscale lacks a counter-removal loop.
- Blor's mana creatures and Equipment package and Ekthi's free equip turns
  scale sharply but remain bounded.

## Pregame disclosures

Use the shortest statement that covers the actual risk:

- **Pantlaza:** “This is upgraded Dinosaur discover. Savage Order can fetch an
  indestructible Apex Altisaur beside Wrathful Raptors for a one-sided clear and
  conditional near-infinite damage.”
- **Queen Marchesa:** “This is political Mardu control. It has a clunky
  five-card Arcbond damage loop and a finite Fire Covenant/Brash Taunter kill.”
- **Magda:** “There is no infinite combo in the current list, but Magda can
  repeatedly turn five Treasures into the best Dragon or artifact for the
  position.”
- **Blor, Ekthi, Minn, and Pantlaza before release:** identify the Rule Zero card
  listed in the construction table.
- **The Fifth Doctor + Susan Foreman:** “This is the lower-powered list: Bant
  tap/untap, +1/+1 counters, Vehicles, and no known combo.”

## Evidence boundaries

The exact structured findings live in
`knowledge/combo-adjudications.json`. Raw API responses and their hashes live in
`data/spellbook-results/`. Commander Spellbook does not prove absence, so the
no-combo conclusions are limited to its current database plus the manual Oracle
screen documented here. Re-run `just check-current` before presenting this
report as current after any deck edit.
