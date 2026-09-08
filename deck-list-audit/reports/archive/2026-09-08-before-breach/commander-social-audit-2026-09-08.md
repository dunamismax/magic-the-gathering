# dunamismax 11-deck social-power audit

Reviewed: 2026-09-08
Profile: <https://moxfield.com/users/dunamismax>
Scope: all 11 public Commander mains in the [September 8 source manifest](../data/moxfield-exports/2026-09-08/manifest.json), plus Gandalf's separately pinned nine-for-nine configuration switch.

Smaug the Impenetrable | Hurts So Gold joins the lineup as the owner's **Bracket 4 / Optimized maximum-power combo deck**. All ten existing main decks and Gandalf's nine-card sideboard were freshly exported and verified byte-identical to the September 5 snapshots. Frodo & Sam and Thorin have September 7 public page dates, with no card changes. No existing Commander deck was removed or renamed.

## Construction and source verification

All 11 mains contain exactly 100 resolved cards and pass commander configuration, singleton, banned-card, color-identity, release-state, and configured exception checks. Passing with a configured exception does not establish ordinary Commander legality for that exception. Counts below separate printed lands from spell/land MDFCs.

| Deck | Printed lands | Spell/land MDFCs | Game Changers | Required exception |
|---|---:|---:|---:|---|
| Aragorn | 36 | 1 | 0 | None |
| Blor | 36 | 2 | 0 | Blor releases 2026-11-09 |
| Frodo & Sam | 36 | 0 | 1 | The One Ring in the posted B2* list |
| Gandalf | 34 | 3 | 0 | Westward Voyager is outside Jeskai identity |
| Henzie | 34 | 4 | 0 | None |
| Thorin | 36 | 1 | 0 | None |
| Minn | 34 | 2 | 0 | The Theorist, Jace Beleren releases 2026-10-02 |
| Pantlaza | 35 | 3 | 0 | Maular releases 2026-11-09 |
| Queen Marchesa | 35 | 2 | 0 | None |
| The Notary Hobbits | 36 | 3 | 0 | Darksteel Angel releases 2026-10-02 |
| Smaug | 35 | 1 | 6 | None |

Smaug has six Game Changers: Ancient Tomb, Demonic Tutor, Jeska's Will, Mana Vault, The One Ring, and Vampiric Tutor. Its configured ceiling is unrestricted, consistent with Bracket 4. Frodo & Sam retains its one Game Changer and explicit B2* exception; all other existing decks have zero. This is seven Game Changer copies across the collection, representing six distinct names.

Fresh exports are retained in `data/moxfield-exports/2026-09-08/`. Their hashes, source dates, IDs, and normalized-list hashes are pinned in the manifest. [changes.json](../data/moxfield-exports/2026-09-08/changes.json) records the addition, zero existing substitutions, and the two metadata-only updates.

The Oracle loader now excludes nonplayable `front_card` records, with a regression test for Heroes for Hire. The playable enchantment and its same-named display card have different Oracle IDs; the display record previously made the name ambiguous. No deck card was replaced to resolve this data issue.

## Smaug's role in the lineup

Smaug supplies the explicit optimized combo seat. Its seven-mana commander converts noncombat damage into Treasures; rituals, fast mana, two unrestricted tutors, Magda, Inventors' Fair, and Urza's Saga support access and acceleration. The seven fetch lands are mana fixing, not seven additional combo tutors. Repeated damage and Treasure events feed redundant damage or life-loss payoffs, with free or discounted interaction protecting the decisive turn.

The main constraint is commander dependence. Indestructible helps against damage and destruction, while exile, bounce, sacrifice, toughness reduction, ability suppression, and artifact disruption can still interrupt the plan. Resolving Smaug and an enabler can lead to a win that turn, but no measured win-turn distribution or competitive results are available. The owner's maximum-power designation describes this deck's intended role; it does not establish a proven cEDH list or an exhaustive optimization claim.

Replayability comes from selecting the engine, managing mana and life, choosing a payoff, and navigating interaction. Opponents need to expect compact repeatable combos and possible abrupt wins. The deck is a poor default choice for the lineup's B2/B3 social games without an explicit agreement to play at its higher power. No extra-turn, broad land-denial, or hard-lock package was identified in Smaug's exact list. Star of Extinction destroys one targeted land; Mana Vault's self-untap restriction is not an opponent lock.

## Smaug combo adjudication

A September 8 full-list Commander Spellbook scan returned nine included candidates. Each was checked against current Oracle text and the exact 100. None requires an unresolved abstract template. The bracket estimator also listed two prepare templates; the deck contains no prepare card and those templates do not establish another line.

| Candidate | Exact-list finding |
|---|---|
| Smaug + Mayhem Devil | One untapped Treasure starts unbounded mana and Treasure entry/sacrifice events; the base loop aims Devil damage at Smaug and needs a payoff to win. |
| Smaug + Havoc Jester | The same replacement-Treasure loop, using Jester's sacrifice trigger. |
| Smaug + Chain Lightning | RRR starts the line: pay the first RR copy cost during resolution before the first Treasure trigger resolves. Later copies create three Treasures and spend two to continue. |
| Smaug + Dizzying Gaze | R starts a mana-neutral self-damage/Treasure loop. A payoff wins directly; an amplifier can create surplus mana. |
| Smaug + Pyrohemia | Repeatable symmetric damage, limited by the pilot's life and support-creature survival unless another effect changes those constraints. |
| Smaug + Pestilence | The same life-limited pattern using black mana. Lifelink on Smaug does not give the enchantment lifelink. |
| Dawnsire + Pain for All | With ten charge counters, an enchanted creature, and a legal attacker, one attack can deal 100 to each opponent. Smaug is the durable host and also creates 100 Treasures. Finite damage burst. |
| Dawnsire + Fiendlash | **Database correction:** Fiendlash deals the equipped creature's power, not Dawnsire's 100 damage. Otherwise unmodified Smaug has 10 power with Fiendlash, so the trigger deals 10 to one target while Smaug makes 100 Treasures. |
| Expedited Inheritance + Blasphemous Act | Finite, optional library access from each damaged creature; opponents can benefit. It is neither an infinite engine nor automatic access to the whole library. |

Manual review additionally confirms **Smaug + Blazing Sunsteel + an initial damage event**. Equip Smaug, damage him, and repeatedly aim Sunsteel's trigger back at him while resolving Treasure triggers. Choose another target to end the loop. This line was absent from the nine included scan results.

Reckless Fireweaver, Weftstalker Ardent, Mirkwood Bats, Marionette Apprentice, Disciple of the Vault, The Sackville-Bagginses, Pain for All, and Fiendlash convert the relevant entry, sacrifice, or damage events into a finish. The payoff must survive: a sweeper can remove support creatures before the resulting Treasures enter. Heroes for Hire, Professional Face-Breaker, and optional Expedited Inheritance can turn repeatable resources into access to the remaining library. Library access remains finite.

The [public primer](https://moxfield.com/decks/PyYsm-js4EG7x4j-RUkTVw/primer), read September 8, still mentions **Agent of the Iron Throne, Torment of Hailfire, and Witch's Clinic**, all absent from the current export. Those cards were not imported or counted as available outlets. The repo refresh does not edit Moxfield.

## Existing-deck pod fit and disclosures

These exact ten lists are unchanged. Their September 5 social judgments and original scan/review dates remain applicable to the same hashes; they were not relabeled as newly rescanned. Relative power and pod fit remain medium-confidence list-based judgments without measured game results.

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

Pantlaza retains three conditional Apex Altisaur/Wrathful Raptors lines with Savage Order, Flawless Maneuver, or Akroma's Will. Damage is normally bounded by opposing fight targets; a suitable indestructible opposing creature can sustain the fight chain. Queen Marchesa retains a finite Fire Covenant/Brash Taunter line and its conditional five-card Arcbond loop. Henzie's Mikaeus/Viscera Seer template remains incomplete because there is no persist creature.

Gandalf's posted Maximum Flavor main contains neither Surge to Victory nor Savage Beating. Its exact nine-for-nine Maximum Power switch restores the conditional unlimited-combat line. No other cards change. Maximum Flavor requires the Westward Voyager color-identity house rule; Maximum Power is Commander-legal and needs its separate combo disclosure.

Minn's Teferi, Master of Time can take two consecutive extra turns through its ultimate. Notary's Rise of the Eldrazi grants its caster an extra turn and exiles itself. Emrakul, the Promised End controls an opponent's next turn and gives that opponent the subsequent extra turn. These remain distinct pregame disclosures.

## Evidence and confidence

Oracle was refreshed on September 8. Official [Commander format and Game Changer guidance](https://magic.wizards.com/en/formats/commander), the [February bracket update](https://magic.wizards.com/en/news/announcements/commander-brackets-beta-update-february-9-2026), and the [banned list](https://magic.wizards.com/en/banned-restricted-list) were rechecked that day. Bracket 4 permits unrestricted Game Changers; play intent and the actual lines also support Smaug's B4 designation.

The ten unchanged decks retain hash-matching Spellbook scans and manual reviews from August 30, September 4, or September 5, as recorded individually. Smaug's scan and review are September 8. [Structured adjudications](../knowledge/combo-adjudications.json) preserve each candidate, prerequisite, correction, and review date. The previous report manifest is retained in [archive/manifest-2026-09-05.json](archive/manifest-2026-09-05.json).

Construction and hash equality are deterministic. Bracket fit, speed, resilience, and relative power remain judgments. Neither a scan nor manual review proves combo completeness. Future representative-printing warnings for already-legal identities are separate from the four unreleased-card exceptions listed above. No stale external layer remains within the repository's configured freshness windows after successful `just verify`.
