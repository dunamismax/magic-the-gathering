#!/usr/bin/env python3
"""Generate confidence-labeled functional role candidates for every deck."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from typing import Any

from audit_decks import ROOT, json_bytes, json_load, normalize_name, sha256_file


ROLE_PATTERNS: dict[str, tuple[str, ...]] = {
    "ramp": (
        r"\{T\}: Add ",
        r"create (?:a|one|two|three|X) Treasure token",
        r"search your library for (?:a|up to [^ ]+) (?:basic )?land card",
        r"put (?:it|that card|those cards) onto the battlefield",
    ),
    "cost_reduction": (
        r"costs? \{?[0-9X]+\}? less to cast",
        r"without paying (?:its|their) mana cost",
        r"rather than pay",
    ),
    "selection": (
        r"\bscry\b",
        r"\bsurveil\b",
        r"look at the top [^\n]+ cards? of your library",
        r"rearrange [^\n]+ on top of your library",
    ),
    "card_advantage": (
        r"draw (?:a|two|three|X|that many) cards?",
        r"exile the top card of your library[^\n]+(?:play|cast)",
        r"you may play [^\n]+ from exile",
        r"return [^\n]+ from your graveyard to your hand",
    ),
    "tutor": (r"search your library for",),
    "recursion": (
        r"return [^\n]+ from your graveyard",
        r"cast [^\n]+ from your graveyard",
        r"put [^\n]+ from (?:a|your) graveyard onto the battlefield",
    ),
    "spot_removal": (
        r"destroy target",
        r"exile target",
        r"return target [^\n]+ to (?:its|their) owner's hand",
        r"deals? [^\n]+ damage to target",
        r"target creature gets -[0-9X]*/-[0-9X]*",
    ),
    "countermagic": (r"counter target (?:spell|activated ability|triggered ability|spell or ability)",),
    "board_wipe": (
        r"destroy all",
        r"exile all",
        r"all creatures get -",
        r"each creature gets -",
        r"damage to each creature",
    ),
    "protection": (
        r"gain(?:s)? hexproof",
        r"gain(?:s)? indestructible",
        r"protection from",
        r"phase out",
        r"regenerate target",
    ),
    "graveyard_interaction": (
        r"exile [^\n]+ from (?:a|target|an opponent's) graveyard",
        r"exile all cards from (?:a|target) player's graveyard",
    ),
    "win_condition": (
        r"wins? the game",
        r"loses? the game",
        r"poison counters?",
    ),
    "lock_piece": (
        r"players can't cast spells",
        r"your opponents can't cast spells",
        r"skip their untap steps?",
        r"doesn't untap during",
    ),
    "extra_turn": (r"extra turn",),
    "mass_land_denial": (
        r"destroy all lands",
        r"lands don't untap",
        r"players can't play lands",
        r"exile all lands",
    ),
    "modal": (
        r"choose one",
        r"choose two",
        r"choose three",
        r"choose one or more",
    ),
}


def combined_text(card: dict[str, Any]) -> str:
    values = [card.get("oracle_text") or ""]
    values.extend(face.get("oracle_text") or "" for face in card.get("card_faces") or [])
    return "\n".join(values)


def inferred_roles(detail: dict[str, Any]) -> dict[str, str]:
    card = detail["card"]
    type_line = card.get("type_line") or ""
    layout = card.get("layout")
    text = combined_text(card)
    roles: dict[str, str] = {}
    faces = card.get("card_faces") or []
    is_front_land = "Land" in (faces[0].get("type_line", "") if faces else type_line)
    if is_front_land:
        roles["land"] = "deterministic"
        roles["land_capable"] = "deterministic"
    elif layout == "modal_dfc" and any(
        "Land" in face.get("type_line", "") for face in faces[1:]
    ):
        roles["land_capable"] = "deterministic"
        roles["modal"] = "deterministic"
    for role, patterns in ROLE_PATTERNS.items():
        if any(re.search(pattern, text, re.I) for pattern in patterns):
            roles.setdefault(role, "heuristic")
    if is_front_land:
        roles.pop("ramp", None)
    if re.search(r"search your library for (?:a|up to [^ ]+) (?:basic )?land card", text, re.I):
        roles.pop("tutor", None)
    return roles


def build_analysis() -> dict[str, Any]:
    audit_path = ROOT / "data/audit.json"
    audit = json_load(audit_path)
    taxonomy_path = ROOT / "knowledge/role-taxonomy.json"
    overrides_path = ROOT / "knowledge/card-role-overrides.json"
    combo_path = ROOT / "knowledge/combo-adjudications.json"
    taxonomy = json_load(taxonomy_path)
    overrides = json_load(overrides_path)
    combos = json_load(combo_path)
    valid_roles = set(taxonomy["roles"])
    combo_cards: dict[str, set[str]] = defaultdict(set)
    combo_hashes: dict[str, str] = {}
    for deck_record in combos.get("decks") or []:
        combo_hashes[deck_record["deck"]] = deck_record["deck_sha256"]
        for line in deck_record.get("lines") or []:
            if str(line.get("status", "")).startswith("confirmed"):
                combo_cards[deck_record["deck"]].update(
                    normalize_name(str(name)) for name in line.get("cards") or []
                )

    deck_results: dict[str, Any] = {}
    for slug, deck in audit["decks"].items():
        role_counts: Counter = Counter()
        role_cards: dict[str, list[dict[str, Any]]] = defaultdict(list)
        unclassified_nonlands: list[str] = []
        global_overrides = overrides.get("global", {})
        override_map = {
            normalize_name(name): instruction
            for name, roles in {
                **global_overrides,
                **overrides.get("decks", {}).get(slug, {}),
            }.items()
            for instruction in [
                {"include": roles, "exclude": []}
                if isinstance(roles, list)
                else roles
            ]
        }
        classified_quantity = 0
        nonland_quantity = 0
        card_results: list[dict[str, Any]] = []
        for detail in deck["cards"]:
            quantity = int(detail["quantity"])
            roles = inferred_roles(detail)
            keys = {
                normalize_name(detail["listed_name"]),
                normalize_name(detail["canonical_name"]),
                normalize_name(str(detail["card"].get("name", ""))),
            }
            for key in keys:
                instruction = override_map.get(key, {})
                for role in instruction.get("include", []):
                    if role not in valid_roles:
                        raise RuntimeError(f"unknown role override {role!r} for {slug}")
                    roles[role] = "override"
                for role in instruction.get("exclude", []):
                    if role not in valid_roles:
                        raise RuntimeError(f"unknown role exclusion {role!r} for {slug}")
                    roles.pop(role, None)
            if combo_hashes.get(slug) == deck["deck_sha256"] and keys & combo_cards[slug]:
                roles["combo_piece"] = "confirmed-combo"
            if "land" not in roles:
                nonland_quantity += quantity
                if roles:
                    classified_quantity += quantity
                else:
                    unclassified_nonlands.append(detail["listed_name"])
            for role, confidence in sorted(roles.items()):
                role_counts[role] += quantity
                role_cards[role].append(
                    {
                        "name": detail["listed_name"],
                        "quantity": quantity,
                        "confidence": confidence,
                    }
                )
            card_results.append(
                {
                    "name": detail["listed_name"],
                    "quantity": quantity,
                    "roles": roles,
                }
            )
        deck_results[slug] = {
            "deck_sha256": deck["deck_sha256"],
            "counts_overlap": True,
            "role_counts": dict(sorted(role_counts.items())),
            "role_cards": dict(sorted(role_cards.items())),
            "nonland_role_coverage": (
                round(classified_quantity / nonland_quantity, 4) if nonland_quantity else 1.0
            ),
            "unclassified_nonlands": sorted(unclassified_nonlands),
            "combo_adjudication_current": combo_hashes.get(slug) == deck["deck_sha256"],
            "cards": card_results,
        }
    return {
        "schema_version": 1,
        "audit_date": audit["audit_date"],
        "inputs": {
            "audit_sha256": sha256_file(audit_path),
            "taxonomy_sha256": sha256_file(taxonomy_path),
            "overrides_sha256": sha256_file(overrides_path),
            "combo_adjudications_sha256": sha256_file(combo_path),
        },
        "method": {
            "deterministic": "Land and modal-land facts derived from Oracle structure.",
            "heuristic": "Oracle-text pattern candidates requiring deck-context review.",
            "override": "Human-reviewed deck-specific role annotation.",
            "confirmed-combo": "Card occurs in a confirmed structured combo adjudication.",
        },
        "decks": deck_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = ROOT / "generated/functional-analysis.json"
    try:
        expected = json_bytes(build_analysis())
    except RuntimeError as exc:
        print(f"ROLE ANALYSIS ERROR: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print("stale generated/functional-analysis.json", file=sys.stderr)
            return 1
        print("verified functional role candidates")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(expected)
        print("generated functional role candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
