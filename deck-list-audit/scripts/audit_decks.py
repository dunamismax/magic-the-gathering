#!/usr/bin/env python3
"""Audit the locally exported public Moxfield Commander decks.

The script resolves card names against Scryfall's Oracle bulk JSONL, checks
basic Commander construction/legality properties, and emits both a detailed
machine-readable audit and Commander Spellbook request payloads.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


DECKS = {
    "blor-the-impervious": {
        "commander": "Blor the Impervious",
        "title": "Blor the Impervious | Built Frog Tough",
        "moxfield_id": "jfWEvfYBHkGi7P1oqzAQww",
    },
    "ekthi-contaminator-priest": {
        "commander": "Ekthi, Contaminator Priest",
        "title": "Ekthi, Contaminator Priest | Armed and Contagious",
        "moxfield_id": "-7GF8IrCdkWIVS667RgA9w",
    },
    "henzie-toolbox-torre": {
        "commander": "Henzie \u201cToolbox\u201d Torre",
        "title": "Henzie \u201cToolbox\u201d Torre | Jundyard Shift",
        "moxfield_id": "hmDd37TPIEaienBhw05Udw",
    },
    "kang-prime": {
        "commander": "Kang Prime",
        "title": "Kang Prime | All in Due Time",
        "moxfield_id": "Yr7eDw8Ay0-9gX091oXxkA",
    },
    "magda-brazen-outlaw": {
        "commander": "Magda, Brazen Outlaw",
        "title": "Magda, Brazen Outlaw | Dragon Delivery Service",
        "moxfield_id": "sfMB4JriEkaOXwGSCqoZlw",
    },
    "marrow-gnawer": {
        "commander": "Marrow-Gnawer",
        "title": "Marrow-Gnawer | Rats All, Folks!",
        "moxfield_id": "ih0yHz5lR0iEcRJyRNMpQQ",
    },
    "minn-wily-illusionist": {
        "commander": "Minn, Wily Illusionist",
        "title": "Minn, Wily Illusionist | Now You See Minn",
        "moxfield_id": "yRogqEE7oE29tp9aASt9IQ",
    },
    "pantlaza-sun-favored": {
        "commander": "Pantlaza, Sun-Favored",
        "title": "Pantlaza, Sun-Favored | The Land Before Value",
        "moxfield_id": "zqJp4nSGKEqfbE0Jx1iJJA",
    },
    "queen-marchesa": {
        "commander": "Queen Marchesa",
        "title": "Queen Marchesa | Mardu Your Business",
        "moxfield_id": "CXl1HrG9uE21A_07vqY3lA",
    },
}

# Moxfield can export alternate in-universe/Arena names. These are the same
# game objects as their canonical paper names, so resolve them to one Oracle
# record while retaining the listed name in the output.
ALIASES = {
    "Giantcraft Helm": "Doc Ock's Tentacles",
    "Egrix the Bile Bulwark": "Gwenom, Remorseless",
    "Escape Containment": "Incarnation Technique",
    "Vazin, Two-Faced Trickster": "Chameleon, Master of Disguise",
    "The Terminus of Return": "The Soul Stone",
}

TYPE_ORDER = (
    "Creature",
    "Planeswalker",
    "Battle",
    "Instant",
    "Sorcery",
    "Artifact",
    "Enchantment",
    "Land",
)


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"\s+", " ", value).strip()
    return value.casefold()


def read_deck(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        match = re.match(r"^(\d+)\s+(.+)$", line)
        if not match:
            raise ValueError(f"{path}:{line_number}: cannot parse {raw!r}")
        entries.append({"quantity": int(match.group(1)), "name": match.group(2)})
    return entries


def load_oracle(path: Path) -> tuple[dict[str, dict], dict[str, list[str]]]:
    candidates: dict[str, list[dict]] = defaultdict(list)
    nonplayable_layouts = {"art_series", "token", "double_faced_token", "emblem"}
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            card = json.loads(line)
            if card.get("layout") in nonplayable_layouts:
                continue
            names = {card.get("name", "")}
            if " // " in card.get("name", ""):
                names.add(card["name"].split(" // ", 1)[0])
            for face in card.get("card_faces") or []:
                names.add(face.get("name", ""))
            for name in names:
                if name:
                    candidates[normalize_name(name)].append(card)

    resolved: dict[str, dict] = {}
    ambiguous: dict[str, list[str]] = {}
    for key, cards in candidates.items():
        unique = {card.get("oracle_id") or card.get("id"): card for card in cards}
        values = list(unique.values())
        if len(values) == 1:
            resolved[key] = values[0]
            continue
        exact = [card for card in values if normalize_name(card.get("name", "")) == key]
        if len(exact) == 1:
            resolved[key] = exact[0]
        else:
            ambiguous[key] = sorted(card.get("name", "") for card in values)
    return resolved, ambiguous


def card_type_counts(card: dict, quantity: int, counts: Counter) -> None:
    type_line = card.get("type_line", "")
    matched = False
    for card_type in TYPE_ORDER:
        if re.search(rf"\b{re.escape(card_type)}\b", type_line):
            counts[card_type] += quantity
            matched = True
    if not matched:
        counts["Other"] += quantity


def front_is_land(card: dict) -> bool:
    if card.get("card_faces"):
        return "Land" in card["card_faces"][0].get("type_line", "")
    return "Land" in card.get("type_line", "")


def has_land_back(card: dict) -> bool:
    faces = card.get("card_faces") or []
    return bool(
        card.get("layout") == "modal_dfc"
        and faces
        and not front_is_land(card)
        and any("Land" in face.get("type_line", "") for face in faces[1:])
    )


def can_repeat(card: dict) -> bool:
    if "Basic" in card.get("type_line", ""):
        return True
    text = card.get("oracle_text", "")
    return bool(
        re.search(r"A deck can have (?:any number|up to [a-z]+) of cards named", text, re.I)
        or re.search(r"A deck can have up to \w+ cards named", text, re.I)
    )


def compact_card(card: dict) -> dict:
    return {
        key: card.get(key)
        for key in (
            "name",
            "released_at",
            "mana_cost",
            "cmc",
            "type_line",
            "oracle_text",
            "color_identity",
            "keywords",
            "legalities",
            "game_changer",
            "layout",
        )
    } | {
        "card_faces": [
            {
                key: face.get(key)
                for key in ("name", "mana_cost", "type_line", "oracle_text", "colors")
            }
            for face in (card.get("card_faces") or [])
        ]
    }


def audit_deck(
    slug: str,
    metadata: dict,
    path: Path,
    oracle: dict[str, dict],
    ambiguous: dict[str, list[str]],
    today: date,
) -> tuple[dict, dict]:
    entries = read_deck(path)
    unresolved: list[str] = []
    ambiguous_names: dict[str, list[str]] = {}
    resolved_entries: list[tuple[dict, dict]] = []
    for entry in entries:
        lookup_name = ALIASES.get(str(entry["name"]), str(entry["name"]))
        key = normalize_name(lookup_name)
        card = oracle.get(key)
        if card is None:
            unresolved.append(str(entry["name"]))
            if key in ambiguous:
                ambiguous_names[str(entry["name"])] = ambiguous[key]
            continue
        resolved_entries.append((entry, card))

    commander_key = normalize_name(metadata["commander"])
    commander_card = oracle.get(commander_key)
    if commander_card is None:
        commander_matches = [card for entry, card in resolved_entries if normalize_name(str(entry["name"])) == commander_key]
        commander_card = commander_matches[0] if commander_matches else None
    commander_identity = set(commander_card.get("color_identity", [])) if commander_card else set()

    type_counts: Counter = Counter()
    total = 0
    printed_lands = 0
    mdfc_lands = 0
    game_changers: list[str] = []
    not_legal: list[str] = []
    unreleased: list[dict[str, str]] = []
    identity_violations: list[dict[str, object]] = []
    nonbasic_duplicates: list[dict[str, object]] = []
    card_details: list[dict[str, object]] = []

    for entry, card in resolved_entries:
        quantity = int(entry["quantity"])
        name = str(entry["name"])
        total += quantity
        card_type_counts(card, quantity, type_counts)
        if front_is_land(card):
            printed_lands += quantity
        elif has_land_back(card):
            mdfc_lands += quantity
        if card.get("game_changer"):
            game_changers.extend([name] * quantity)
        if (card.get("legalities") or {}).get("commander") != "legal":
            not_legal.extend([name] * quantity)
        released_at = card.get("released_at")
        if released_at and date.fromisoformat(released_at) > today:
            unreleased.append({"name": name, "released_at": released_at})
        identity = set(card.get("color_identity") or [])
        if commander_card and not identity.issubset(commander_identity):
            identity_violations.append({"name": name, "identity": sorted(identity)})
        if quantity > 1 and not can_repeat(card):
            nonbasic_duplicates.append({"name": name, "quantity": quantity})
        card_details.append({
            "listed_name": name,
            "quantity": quantity,
            "is_commander": normalize_name(name) == commander_key,
            "card": compact_card(card),
        })

    commander_quantity = sum(
        int(entry["quantity"])
        for entry, _ in resolved_entries
        if normalize_name(str(entry["name"])) == commander_key
    )

    summary = {
        "slug": slug,
        "title": metadata["title"],
        "commander": metadata["commander"],
        "moxfield_id": metadata["moxfield_id"],
        "moxfield_url": f"https://moxfield.com/decks/{metadata['moxfield_id']}",
        "file": str(path),
        "total_cards": sum(int(entry["quantity"]) for entry in entries),
        "resolved_cards": total,
        "unique_lines": len(entries),
        "commander_quantity": commander_quantity,
        "commander_identity": sorted(commander_identity),
        "type_counts": dict(type_counts),
        "printed_lands": printed_lands,
        "mdfc_lands": mdfc_lands,
        "effective_land_faces": printed_lands + mdfc_lands,
        "game_changer_count": len(game_changers),
        "game_changers": game_changers,
        "not_commander_legal": not_legal,
        "unreleased": unreleased,
        "identity_violations": identity_violations,
        "nonbasic_duplicates": nonbasic_duplicates,
        "unresolved": unresolved,
        "ambiguous": ambiguous_names,
        "cards": card_details,
    }

    main = [
        {
            "card": ALIASES.get(str(entry["name"]), str(entry["name"])),
            "quantity": int(entry["quantity"]),
        }
        for entry in entries
        if normalize_name(str(entry["name"])) != commander_key
    ]
    commanders = [
        {
            "card": ALIASES.get(str(entry["name"]), str(entry["name"])),
            "quantity": int(entry["quantity"]),
        }
        for entry in entries
        if normalize_name(str(entry["name"])) == commander_key
    ]
    request = {"main": main, "commanders": commanders}
    return summary, request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decks-dir", type=Path, default=Path("decks"))
    parser.add_argument("--oracle", type=Path, default=Path("data/oracle-cards.jsonl.gz"))
    parser.add_argument("--output", type=Path, default=Path("data/audit.json"))
    parser.add_argument("--requests-dir", type=Path, default=Path("data/spellbook-requests"))
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    oracle, ambiguous = load_oracle(args.oracle)
    args.requests_dir.mkdir(parents=True, exist_ok=True)
    audits: dict[str, dict] = {}
    for slug, metadata in DECKS.items():
        path = args.decks_dir / f"{slug}.txt"
        audit, request = audit_deck(slug, metadata, path, oracle, ambiguous, args.date)
        audits[slug] = audit
        request_path = args.requests_dir / f"{slug}.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = {
        "audit_date": args.date.isoformat(),
        "oracle_source_updated_at": json.loads(Path("data/oracle-bulk-metadata.json").read_text())["updated_at"],
        "decks": audits,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
