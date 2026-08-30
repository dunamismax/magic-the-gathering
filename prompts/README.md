# Commander review prompts

Choose one prompt based on the scope you actually want. Each prompt treats the
submitted 100 as the authority and requires current legality, Game Changer, and
combo checks before making list-specific claims.

| Prompt | Use it for | Change scope |
|---|---|---|
| [`full-evaluation.md`](full-evaluation.md) | Power, speed, bracket, salt, combo, and optional tuning review | Analysis first; up to five swaps only when requested |
| [`conservative-upgrade.md`](conservative-upgrade.md) | “Only the best,” low-disruption tuning | Smallest defensible package, maximum five swaps |
| [`structural-upgrade.md`](structural-upgrade.md) | A coordinated rebuild or correction of structural weaknesses | As many material changes as the evidence supports |
| [`public-collection-refresh.md`](public-collection-refresh.md) | Refresh the repository from the public Moxfield profile | Local source and derived artifacts only |

When working inside this repository, start the agent in `deck-list-audit/` so
[`AGENTS.md`](../deck-list-audit/AGENTS.md) and the current collection metadata
are in scope. Paste a deck only when the agent cannot read the repository.
