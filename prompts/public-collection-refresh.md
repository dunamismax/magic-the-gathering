# Public Moxfield collection refresh prompt

Refresh this repository from the public Moxfield profile recorded in
`deck-list-audit/collection.json`.

1. Read `deck-list-audit/AGENTS.md`, run `just check`, and preserve any existing
   user changes.
2. Enumerate the public Commander decks on the profile. Record exact titles,
   Moxfield IDs, public update dates, and the refresh date. Detect added,
   removed, or renamed decks explicitly.
3. Download each deck through Moxfield's public plain-text export UI when a
   stable anonymous API is unavailable. Never infer an unchanged list from its
   displayed update date.
4. Machine-count every export before import. Resolve aliases and MDFCs locally,
   then require exactly 100 cards, a valid commander configuration, singleton
   compliance, color identity, legality, release-state handling, and the stated
   Game Changer ceiling.
5. Update `decks/*.txt` and `collection.json`, regenerate deterministic
   artifacts, and update navigation or dated reports that would otherwise make
   a stale claim.
6. Preserve superseded external results as dated evidence. Mark Spellbook,
   combo, and social conclusions stale unless the exact current hashes have
   actually been reviewed. Do not upload a complete list to another service or
   write anything back to Moxfield without a separate explicit request.
7. If the user has explicitly authorized full-list Commander Spellbook uploads,
   refresh all changed public lists, inspect every included result and abstract
   requirement against the exact 100, and update the structured adjudications.
   If authorization is absent, leave an explicit `needs-refresh` marker.
8. Replace or archive dated social reports so the current report manifest pins
   only conclusions reviewed against the current hashes.
9. Run tests, `just check-current` when every evidence layer is current, and
   review the final diff. Report changed decks, validation results, remaining
   stale layers, and every Rule Zero dependency.
