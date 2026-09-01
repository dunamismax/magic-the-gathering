# Commander bracket and power evaluation

Reviewed: 2026-09-01  
Profile: <https://moxfield.com/users/dunamismax>  
Scope: the exact 10 public lists and hashes recorded in
`data/moxfield-refresh.json`

## Verdict

The collection now contains nine Bracket 3 targets and one Bracket 2 deck. Frodo
and Sam are the intentional lower-power deck. Pantlaza and Gandalf are the two
knife-edge B3/B4 decisions: normal combat-forward intent fits the ceiling of
Bracket 3, while routinely assembling or tutoring their conditional unlimited
finishes should be presented as Bracket 4.

| Raw-power order | Deck | Appropriate bracket | Power estimate | Confidence | Practical label |
|---:|---|---|---:|---|---|
| 1 | Pantlaza, Sun-Favored | **B3 ceiling; B4 when combo-forward** | **8.0-8.5/10** | Medium-high | Upgraded Dinosaurs with a disclosed conditional kill |
| 2 | Gandalf, Party Guest | **B3 ceiling; B4 when combo-forward** | **8.0-8.5/10** | Medium-high | Free-spell Wizards with a disclosed two-card conditional combat loop |
| 3 | Magda, Brazen Outlaw | **B3 upper** | **7.5-8.0/10** | High | Command-zone Dragon/artifact toolbox |
| 4 | Henzie “Toolbox” Torre | **B3 mid-upper** | **7.0-7.5/10** | High | Blitz, ETB, and reanimation value |
| 5 | Aragorn, the Uniter | **B3 mid-upper** | **7.0-7.5/10** | Medium-high | Four-color multicolor-spell go-wide |
| 6 | Blor the Impervious | **B3 mid-upper** | **7.0-7.5/10** | Medium-high | Resilient Voltron; Rule Zero until release |
| 7 | Minn, Wily Illusionist | **B3 middle** | **6.5-7.0/10** | Medium-high | Draw/Illusion engine; Rule Zero until Jace releases |
| 8 | Ekthi, Contaminator Priest | **B3 middle** | **6.5-7.0/10** | Medium-high | Equipment combat; Rule Zero until release |
| 9 | Queen Marchesa | **B3 middle** | **6.5-7.0/10** | High | Political control with a disclosed clunky loop |
| 10 | Frodo & Sam | **B2 upper** | **5.5-6.0/10** | Medium-high | Fair Hobbit/Food/Ring value and combat |

The numerical ranges are conventional relative estimates, not a formula that
converts directly into brackets. No game logs or goldfish results were supplied,
so clock and consistency statements are list-based inferences.

## Why the three new decks fit

### Gandalf, Party Guest — Bracket 3 ceiling; Bracket 4 when combo-forward

Gandalf turns a board of legendary Wizards into a free instant or sorcery at
each combat. Extra-combat spells retrigger the commander, and the list backs
that ceiling with efficient interaction, spell tutors, strong trigger
multipliers, and 37 effective land sources. It can create turns that feel much
larger than an ordinary value deck.

The adopted `Surge to Victory` addition creates a confirmed two-card conditional
unlimited-combat line with `Savage Beating`: put Savage Beating in the graveyard,
exile it with Surge, connect with a creature, and use each free copy for another
untap and combat. Its six-mana setup and combat dependency can remain a disclosed
ceiling-Bracket-3 finish when the deck is not built to race or force it before
turn six. A plan that actively tutors or prioritizes the line belongs in
Bracket 4.

It remains a Bracket 3 target rather than automatically becoming Bracket 4
because the line starts with a six-mana sorcery, needs its other named card in
the graveyard, depends on combat damage, and is not backed by a dense fast-mana
or tutor package. It is nevertheless unbounded once established, interactable
at several points, and mandatory to disclose.

### Aragorn, the Uniter — mid-upper Bracket 3

Aragorn has excellent four-color mana, efficient interaction, strong mana
creatures, and many multicolored spells that trigger several commander modes.
Annie Joins Up, Roaming Throne, token makers, and combat payoffs let a normal
spell sequence become a decisive board.

Jeskai Ascendancy can untap multicolor mana creatures repeatedly, but the exact
list lacks the recast engine required for a deterministic loop. The deck's
normal win remains a visible go-wide or commander-trigger turn rather than a
compact optimized finish.

### Frodo & Sam — upper Bracket 2

Frodo and Sam use 37 lands, fair land-ramp, Food and Hobbit engines, Ring
temptation, and creature combat. The list has useful removal and several
high-quality synergy cards, but little broad tutoring, no fast combo, no lock,
no mass land denial, and no deterministic line.

Its engines accumulate value over several turns and depend on creatures,
tokens, combat, and life gain remaining in play. That incremental pace and
opponent agency are a genuine Bracket 2 profile, albeit near the top of that
bracket.

## Revised Minn

The revised Minn list is more typal and less generically explosive. It removed
several broad value engines and Treachery, added low-cost Illusions and more
draw multipliers, and retained finite sacrifice outlets. It can still produce
large hands and free permanents, but it is light on interaction and has no
complete loop. Middle Bracket 3 is more accurate than the previous mid-upper
placement.

## Existing lineup

- **Pantlaza** remains ceiling B3 because of repeated discover, creature tutors,
  and three conditional Apex Altisaur/Wrathful Raptors lines.
- **Magda** remains upper B3 because five Treasures repeatedly become the best
  Dragon or artifact, even though the compact untap loops are absent.
- **Henzie** remains mid-upper B3 through blitz discounts, premium ETBs,
  Birthing Pod, sacrifice, and reanimation; its returned persist template is
  incomplete.
- **Blor** remains mid-upper B3 through hard-to-answer commander damage and
  combat multipliers, but wins visibly and one player at a time.
- **Ekthi** remains middle B3 through Equipment tutoring and efficient equip
  turns; the wins are finite and board-dependent.
- **Queen Marchesa** remains middle B3 through reactive political control. Its
  five-card Arcbond loop requires disclosure but is too clunky to define the
  normal clock.

## Collection-wide facts and caveats

- All 10 exact lists contain 100 cards and pass the local commander,
  singleton, color-identity, legality-policy, banned-card, release-state, and
  configured Game Changer checks.
- All 10 contain zero current Game Changers. That does not determine bracket.
- No list contains a mass-land-denial package. Minn can eventually ultimate
  Teferi for two extra turns, but no deck has a compact repeatable extra-turn
  loop.
- Gandalf has one confirmed two-card conditional unlimited-combat line.
  Pantlaza has three confirmed conditional near-infinite lines. Queen Marchesa
  has one finite kill and one five-card unbounded loop. Henzie's returned
  persist template is incomplete. No complete current line was found in
  Aragorn, Frodo and Sam, or revised Minn during manual exact-list review.
- Rule Zero is presently required for `Blor the Impervious`, `Ekthi,
  Contaminator Priest`, `The Theorist, Jace Beleren` in Minn, and `Maular,
  the Next Evolution` in Pantlaza because those cards have future release
  dates.

## Evidence and limits

This evaluation uses the hashes in `data/moxfield-refresh.json`, the
2026-08-30 Oracle snapshot, the 2026-08-29 official policy lock, hash-current
Spellbook evidence for all ten lists, and the exact-list manual review in
`knowledge/combo-adjudications.json`. Gandalf's refreshed 2026-09-01 scan
returned one included candidate, which manual review confirmed as conditional;
the scans for Aragorn, Frodo and Sam, and revised Minn returned none.

Power ranges are judgments, not measured win rates, and a database miss does not
prove the absence of every possible interaction. Repeated pre-turn-seven wins
are evidence to move a proposed B3 label upward regardless of whether the win is
combat or combo.

Run `just check-current` before applying these judgments after any deck edit.
