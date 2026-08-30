# Archived report: dunamismax nine-deck Bracket 3 and social-power audit

> Historical snapshot only. The 2026-08-30 refresh changed the lineup and every local deck file.
> Reviewed against the nine-deck 2026-08-29 snapshot. Verify deck hashes and source freshness with
> `just check-current` before reusing any conclusion.

Audit date: 2026-08-29  
Source: the nine exact local lists in [`decks/`](../../decks/README.md), including
user-confirmed Blor, Magda, and Minn changes dated 2026-08-29; public Moxfield
links are tracked as source references, not treated as silently synchronized.

## Bottom line

The lineup is much more themed than “good-stuff soup.” The primary risks are
specific play patterns, not a generalized staple problem:

- **Kang Prime is the one list I would not call a clean, ordinary Bracket 3
  deck unchanged.** It has an infinite-draw engine, a separate two-card
  Blightsteel table kill, dense premium interaction, and several
  opponent-agency crushers. It is upper-edge Bracket 3 only for a pod that
  explicitly opts into those lines; otherwise it plays like Bracket 4.
- **Pantlaza is upper-edge Bracket 3 with one serious combo caveat.** `Savage
  Order` plus `Wrathful Raptors` tutors `Apex Altisaur` with indestructible,
  producing a board-clearing, potentially near-infinite damage chain. The
  slower three-card versions with `Akroma's Will` or `Flawless Maneuver` are
  less concerning.
- **Minn, Magda, and Blor are powerful but more comfortably defensible
  Bracket 3 decks after the latest changes.** Each now has only one Game
  Changer. Minn exchanged two free counters and Teferi's extra-turn ceiling for
  on-theme draw/Illusion cards; Magda exchanged generic burst/value cards for
  Dwarf and token synergies; Blor exchanged generic fast mana/value for
  Equipment utility and permanent-type recovery.
- **Queen Marchesa has a concealed loop worth disclosing:** `Orcish Bowmasters`
  plus `Flumph` loops draws and Bowmasters triggers if Flumph is made
  indestructible and the first damage/draw trigger occurs. The surrounding
  deck is otherwise political, interactive, and highly replayable.
- **Henzie, Ekthi, and Marrow are socially comfortable Bracket 3 decks.**
  Henzie is explosive but finite; Ekthi is consistent but strongly
  Equipment-specific; Marrow is now the cleanest list after removing the
  ripple/tutor/life-engine package that made it disproportionately explosive.

No list contains mass land denial. All nine have 100 cards, no banned cards,
no color-identity violations, and no illegal duplicate problem. Game Changer
counts are all within the current Bracket 3 cap of three, but that cap is not a
substitute for evaluating combos, speed, consistency, or opponent agency.

## Ranking: most likely to draw Bracket 3 side-eye

This is a social-fit ranking, not merely a raw-power ranking. A score of 5 is
highest; for “good-stuff drift,” a higher number means more generic power and
less commander-specific identity.

| Rank | Deck | Bracket 3 verdict | Power | Side-eye | Good-stuff drift | Agency pressure | Replayability |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Kang Prime | Borderline B4; opt-in B3 | 5 | 5 | 4 | 5 | 4 |
| 2 | Pantlaza | Upper B3; combo disclosure | 4 | 5 | 2 | 4 | 4 |
| 3 | Queen Marchesa | Upper B3; loop disclosure | 4 | 3 | 3 | 3 | 5 |
| 4 | Magda | Upper B3 | 4 | 4 | 1 | 3 | 4 |
| 5 | Minn | Upper B3 | 4 | 3 | 2 | 3 | 5 |
| 6 | Blor | Upper B3 | 4 | 3 | 3 | 4 | 4 |
| 7 | Henzie | Mid B3 | 3 | 3 | 3 | 3 | 5 |
| 8 | Ekthi | Mid-to-upper B3 | 4 | 2 | 2 | 2 | 4 |
| 9 | Marrow-Gnawer | Low-to-mid B3 | 3 | 2 | 2 | 2 | 3 |

The ordering between Magda, Minn, and Blor will vary by pod. Experienced
players may fear Magda most at commander reveal, while Minn still has a deep
permission suite and Blor remains harder to answer with normal removal. Queen
Marchesa ranks above them here because its conditional unbounded loop is a
more important blind-pod disclosure than any line introduced by the new cards.

## Structural and policy audit

The current official framework says Bracket 3 decks may have strong synergy,
high card quality, effective disruption, and up to three Game Changers, while
the expected game should normally allow at least six turns before a player wins
or loses. The bracket intent matters more than satisfying a mechanical cap.
Tutors no longer have a bracket-wide numeric restriction, but tutor density can
still reduce replayability and make a risky line recur too often.

| Deck | Printed lands | Spell/land MDFCs | Game Changers | Current legality note |
|---|---:|---:|---|---|
| Blor | 36 | 0 | `Ancient Tomb` | Commander releases 2026-11-09; Rule Zero today |
| Ekthi | 34 | 0 | `Ancient Tomb`, `Enlightened Tutor`, `Teferi's Protection` | Commander releases 2026-11-09; Rule Zero today |
| Henzie | 35 | 3 | None | Legal |
| Kang | 35 | 1 | `Ancient Tomb`, `Bolas's Citadel`, `Fierce Guardianship` | Legal |
| Magda | 35 | 0 | `Ancient Tomb` | Legal |
| Marrow | 35 | 0 | None | Legal |
| Minn | 35 | 2 | `Consecrated Sphinx` | `The Theorist, Jace Beleren` releases 2026-10-02; Rule Zero today |
| Pantlaza | 35 | 3 | `Ancient Tomb`, `Worldly Tutor` | `Maular, the Next Evolution` releases 2026-11-09; Rule Zero today |
| Queen Marchesa | 36 | 2 | `Orcish Bowmasters`, `Smothering Tithe`, `Teferi's Protection` | Legal |

The legality notes are temporary release-timing issues, not power judgments.
Blor and Ekthi cannot be played as ordinary Commander decks before their
commander release; the other two affected lists need one Rule Zero card each.

## Individual reviews

### Kang Prime — the real mismatch risk

Kang is not generic Dimir good stuff wearing a commander name, but it has enough
premium generic infrastructure and enough punishing payloads that the
distinction may not matter to an average Bracket 3 opponent.

The decisive lines are:

- `One with the Multiverse` + `Displacer Kitten` + `Sensei's Divining Top` +
  an untapped one-mana rock draws the deck and produces near-infinite storm.
  The list contains multiple qualifying rocks.
- `Blade of Selves` + `Blightsteel Colossus` attacks every opponent with an
  11-infect Blightsteel. It is a two-card table kill if the attackers connect.
- `Kang the Conqueror` is not itself an infinite-turn engine because its extra
  turns disable power-up abilities, but the clone package can bank multiple
  extra turns from one normal turn. That is still a pregame-conversation item.

The social pressure does not stop at combos: `Portal to Phyrexia`, `Archon of
Cruelty`, `Breach the Multiverse`, both Ulamogs, `Galactus`, free protection,
`Mana Drain`, `Lim-Dûl's Vault`, `Rune-Scarred Demon`, Top, Rack, and Citadel
make the deck both disruptive and consistent. Many of those are legitimate
Kang suspend hits; the issue is density, not lack of synergy.

Verdict: **borderline Bracket 4 in practice**. It is the only list where “three
Game Changers” materially understates the table experience.

### Pantlaza — strongly themed, one Ruthless line

This is a real Dinosaur deck, not Naya staples with a Dinosaur commander. The
good-stuff drift is low. `Etali, Primal Conqueror`, `Ghalta, Stampede Tyrant`,
`Zacama`, `Vaultborn Tyrant`, and the blink/protection package all advance the
same discover-and-big-creature plan.

The issue is `Savage Order`. With `Wrathful Raptors` already in play, it is a
four-mana tutor that finds `Apex Altisaur`, gives it indestructible, and starts
the fight/damage chain. Commander Spellbook classifies that version as a
definite two-card, high-pressure line. `Worldly Tutor`, `Finale of Devastation`,
and Pantlaza's own card flow make the shell more consistent than a random
three-card Dinosaur interaction.

`Marauding Raptor` is not a combo problem in the current list because
`Polyraptor` is absent.

Verdict: **upper Bracket 3 with a mandatory combo disclosure**. Without the
`Savage Order`/`Wrathful Raptors` line, it would be a very clean high-power B3.

### Minn — no current infinite, and now less oppressive

The prior exact-list Spellbook scan documented no complete combo after `Meloku
the Clouded Mirror` left. A current card-delta review found no `Read the Runes`
or `Mask of Memory` variants. Spellbook has `Oneirophage` lines, but every one
requires cards absent from this 100; the mono-blue line requires both `O'aka,
Traveling Merchant` and `Mind Over Matter`, and the lines that also use the
present `Sensei's Divining Top` require off-color `Falco Spara, Pactweaver`.

`Read the Runes` is strong Minn infrastructure because it can draw at instant
speed and convert Illusions into sacrificed permanents. `Mask of Memory`
reliably supplies the second draw through evasive bodies, while `Oneirophage`
is an on-theme, visible combat payoff. None is a compact deterministic win here.

The permission suite is still meaningful—`Force of Negation`, `Flare of
Denial`, `Pact of Negation`, `Subtlety`, `Swan Song`, `Arcane Denial`, and
`Abjure` remain—but removing `Fierce Guardianship` and `Force of Will` lowers
both free-answer density and Game Changer count. Removing `Teferi, Master of
Time` also eliminates the finite two-extra-turn ultimate from the pregame
conversation.

Verdict: **defensible upper Bracket 3**, now with materially lower
opponent-agency pressure and no current deterministic win package.

### Magda — scary commander reputation, fair current finishers

Magda is a repeatable artifact/Dragon tutor in the command zone, so experienced
players will assume a combo build until told otherwise. The current list does
not contain `Clock of Omens`, `Aggravated Assault`, or another documented
complete infinite line.

It can still snowball hard. `Dwarven Bloodboiler` taps Dwarves on demand;
`Roaming Throne` doubles Magda triggers; `Xorn` and `Academy Manufactor`
multiply the token economy; and five Treasures can put `Maskwood Nexus` or the
best Dragon directly onto the battlefield. `Ancient Copper Dragon`, `Terror of
the Peaks`, `Scourge of Valkas`, and `Utvara Hellkite` convert that advantage
quickly but through finite, visible combat.

`Fíli and Kíli, Joyous` is a hasty Dwarf that makes restricted mana for the
deck's Dwarves, Equipment, and Sagas. `Idol of Oblivion` turns routine Treasure
or other token production into cards. Spellbook's one Idol line needs
off-color, absent `Mind Over Matter`, and no Fíli/Kíli line was returned. These
adds deepen the actual theme while `Jeska's Will` and `The One Ring` remove two
generic Game Changers.

Verdict: **upper Bracket 3**. Say “Magda toolbox, no Clock combo or infinite” at
commander reveal and most of the social mismatch disappears.

### Blor — resilient Voltron with a smaller generic-power cluster

Blor's plan is coherent Voltron. Removing `Mana Vault` and `The One Ring`
shrinks what had been one of the lineup's most visible off-the-shelf power
packages. `Ancient Tomb`, `Sylvan Library`, `Selvala, Heart of the Wilds`,
`Urza's Saga`, `Strip Mine`, and premium Equipment remain, but only Ancient
Tomb is a Game Changer.

`Pip-Boy 3000` is cheap Equipment with selection, permanent growth, or land
untapping attached to combat. `Creeping Renaissance` lets a permanent-heavy
Voltron deck recover an entire chosen card type and can be flashed back. The
current card-delta search found only two Pip-Boy combo records, both requiring
absent `Bruce Banner` plus a specific land, and no Creeping Renaissance record.

The social issue is interaction geometry. Blor naturally has trample,
hexproof, and indestructible; `Conqueror's Flail` can shut off opponents' spells
on your turn; and damage multipliers such as `Inquisitor's Flail`, `Berserk`,
and `Genji Glove` turn a difficult-to-answer commander into a sudden one-shot.
That is powerful but also telegraphed and combat-based. There is no documented
infinite combo.

Verdict: **upper Bracket 3 once legal**, but it will still draw early table
focus because of Blor's interaction geometry. The latest swaps materially
improve its thematic cohesion and blind-pod presentation.

### Queen Marchesa — excellent social texture, one hidden loop

This is the most socially interactive and replayable deck in the lineup:
monarch politics, goad, gifts, damage redirection, and table-dependent target
selection mean games should vary substantially.

The main disclosure is `Orcish Bowmasters` + `Flumph`. If Flumph is made
indestructible with `Boros Charm`, `Akroma's Will`, or another effect, one
Flumph trigger can feed Bowmasters back into Flumph repeatedly, creating an
unbounded draw/amass loop. The two cards alone do not automatically win and
Flumph must survive, so this is less reliable than Kang's or Pantlaza's lines.

`Fire Covenant` + `Brash Taunter` can also deal a player an enormous amount of
damage when your life total supports the payment. It is finite, costly, and
appropriate for the deck's redirection identity.

The generic pressure cards are `Smothering Tithe`, `Orcish Bowmasters`,
`Teferi's Protection`, `Trouble in Pairs`, and `Deflecting Swat`. With no fast
mana beyond Sol Ring and no mass land denial, they do not overwhelm the deck's
political identity.

Verdict: **upper Bracket 3 with a loop disclosure**, otherwise an excellent
social deck.

### Henzie — “Jund good stuff” appearance, commander-specific reality

Henzie looks like a pile of premium Jund creatures, but most of those creatures
are exactly what blitz wants: expensive ETB/death bodies that replace
themselves or convert a temporary creature into a large swing. `Archon of
Cruelty`, `Etali, Primal Conqueror`, `Apex Devastator`, `Bane of Progress`,
`Massacre Wurm`, `Living Death`, and `Bringer of the Last Gift` are high card
quality, but not random drift.

`Birthing Pod`, `Birthing Ritual`, `Industrial Advancement`, `Greater Good`,
and the recursion suite make the deck consistent and capable of explosive
turns. Repeated `Archon of Cruelty` or a one-sided-looking `Living Death` can be
socially sharp, but opponents can interact with the graveyard, Pod, or creature
board.

Commander Spellbook surfaced `Mikaeus, the Unhallowed` + `Viscera Seer` with an
abstract “Persist Creature” requirement. The current 100 has no persist
creature, so that is **not a complete combo in this list**.

Verdict: **mid Bracket 3**, strong and explosive but finite, with zero Game
Changers and high replayability.

### Ekthi — consistent, synergistic, and fair after the Norn cuts

Ekthi is almost entirely Equipment, living-weapon, Germ, artifact-token, and
support infrastructure. `Enlightened Tutor`, `Steelshaper's Gift`, `Stoneforge
Mystic`, `Inventors' Fair`, `Urza's Saga`, `Fabrication Foundry`, and `Forge
Anew` create consistency, but they are searching for the deck's actual theme.

The ceiling is high: `Kaldra Compleat`, `Colossus Hammer`, free/easy equips,
`Mondrak, Glory Dominus`, and `Skullclamp` can turn every Equipment into both a
body and a card engine. `Umezawa's Jitte` is the card most likely to dominate a
small-creature table. There is no documented combo, no stax package, and the
two Elesh Norns that formerly reduced opponent agency are absent.

Verdict: **clean mid-to-upper Bracket 3 once legal**. High consistency, low
good-stuff drift, and low agency pressure.

### Marrow-Gnawer — cleanest social fit, most linear play pattern

The current Marrow list has no Game Changers and no documented combo.
`Thrumming Stone`, `Demonic Tutor`, `Bolas's Citadel`, `Necropotence`,
`Thornbite Staff`, and `Grave Pact` are all absent. That removes the deck's
former ripple explosion, compact token loop, generic life-based engines, and
repeated sacrifice-board suppression.

The remaining power is visible and interactable: `Cabal Coffers` + `Urborg`,
`Nykthos`, `Three Tree City`, `Diabolic Intent`, `Black Market Connections`,
`Coat of Arms`, `Skullclamp`, and Marrow's activated ability. These can produce
very large turns, but they require board, mana, or a sacrificed creature and do
not remove the pod's ability to play.

The weakness is replayability rather than social power: 26 `Rat Colony` copies
and an unrestricted tutor make the deck more linear than the rest of the
lineup.

Verdict: **low-to-mid Bracket 3 and the safest blind-pod choice**.

## Concise pregame disclosures

- **Kang:** “Upper-edge B3 with three Game Changers; it contains an infinite
  draw engine, Blade/Blightsteel table kill, and possible chained extra turns;
  no mass land denial.”
- **Pantlaza:** “High-power Dinosaurs; Savage Order plus Wrathful Raptors can
  tutor Apex Altisaur for the indestructible fight/damage line.”
- **Minn:** “Upper B3 Illusions with one Game Changer and several free or
  alternate-cost counters; no known infinite after Meloku came out, and no
  extra-turn package.”
- **Magda:** “High-power Dwarf/Dragon toolbox with one Game Changer; Magda
  tutors from the command zone, but there is no Clock combo or infinite.”
- **Blor:** “One-Game-Changer Voltron; the commander is hexproof and
  indestructible and can one-shot, but there is no known combo.”
- **Queen Marchesa:** “Political redirection with three Game Changers; Flumph
  and Bowmasters can loop if Flumph is made indestructible.”
- **Henzie:** “Zero Game Changers and no infinite; explosive Pod, blitz, and
  mass-reanimation turns.”
- **Ekthi:** “Three-Game-Changer living-weapon Equipment deck; no combo or
  stax.”
- **Marrow:** “Zero Game Changers; no Thrumming Stone, Thornbite loop, or Grave
  Pact—just Rat swarm, Coffers, and Diabolic Intent.”

## Evidence and reproducibility

- Exact exports and hashes: [`decks/README.md`](decks/README.md)
- Full Oracle/count/legality audit: [`data/audit.json`](data/audit.json)
- Reproducible audit script: [`scripts/audit_decks.py`](scripts/audit_decks.py)
- Commander Spellbook bracket/combo responses: [`data/spellbook-results/`](data/spellbook-results/)
- Current official policy: [Commander format and Game Changers](https://magic.wizards.com/en/formats/commander), [October 2025 bracket intent update](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-october-21-2025), and [current Commander banned list](https://magic.wizards.com/en/banned-restricted-list)

Combo databases are incomplete, especially for newly released cards. Their
results were treated as leads and manually checked against the lists. Blor,
Magda, and Minn preserve their 2026-08-29 pre-change exact-list responses as
dated evidence and add a current exact-card-name delta review; no revised full
list was uploaded. This limitation is explicit in the Spellbook manifest. It
is also why the Henzie abstract-template result is excluded and the Kang
turn-sequencing risk is discussed separately.
