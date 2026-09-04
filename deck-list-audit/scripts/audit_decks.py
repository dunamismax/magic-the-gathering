#!/usr/bin/env python3
"""Fail-closed Commander deck construction audit.

The module is intentionally dependency-free so agents can validate the
collection offline. It resolves deck entries to Oracle IDs, aggregates aliases
before singleton checks, distinguishes a future representative printing from a
genuinely unavailable card, supports common two-commander configurations, and
emits deterministic provenance-linked artifacts.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 2
NONPLAYABLE_LAYOUTS = {
    "art_series",
    "token",
    "double_faced_token",
    "emblem",
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
NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "twenty": 20,
}


class AuditConfigurationError(RuntimeError):
    """Raised when the audit system itself is misconfigured."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def json_load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise AuditConfigurationError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditConfigurationError(f"expected a JSON object in {path}")
    return value


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"\s+", " ", value).strip()
    return value.casefold()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def read_deck(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        match = re.fullmatch(r"(\d+)\s+(.+)", line)
        if not match:
            raise ValueError(f"{path}:{line_number}: cannot parse {raw!r}")
        quantity = int(match.group(1))
        if quantity <= 0:
            raise ValueError(f"{path}:{line_number}: quantity must be positive")
        entries.append(
            {
                "quantity": quantity,
                "name": match.group(2).strip(),
                "line_number": line_number,
            }
        )
    return entries


def choose_oracle_path(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    cached = ROOT / "cache/scryfall/oracle-cards.jsonl.gz"
    if cached.exists():
        return cached
    return ROOT / "data/oracle-cards.jsonl.gz"


def load_oracle(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                card = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AuditConfigurationError(
                    f"invalid Oracle JSONL at {path}:{line_number}: {exc}"
                ) from exc
            if card.get("layout") in NONPLAYABLE_LAYOUTS:
                continue
            names = {card.get("name", ""), card.get("flavor_name", "")}
            full_name = card.get("name", "")
            if " // " in full_name:
                names.add(full_name.split(" // ", 1)[0])
            for face in card.get("card_faces") or []:
                names.add(face.get("name", ""))
                names.add(face.get("flavor_name", ""))
            for name in names:
                if name:
                    candidates[normalize_name(name)].append(card)

    resolved: dict[str, dict[str, Any]] = {}
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
            ambiguous[key] = sorted({card.get("name", "") for card in values})
    return resolved, ambiguous


def resolve_card(
    listed_name: str,
    oracle: dict[str, dict[str, Any]],
    aliases: dict[str, str],
) -> tuple[str, dict[str, Any] | None]:
    canonical_name = aliases.get(normalize_name(listed_name), listed_name)
    return canonical_name, oracle.get(normalize_name(canonical_name))


def front_is_land(card: dict[str, Any]) -> bool:
    faces = card.get("card_faces") or []
    if faces:
        return "Land" in faces[0].get("type_line", "")
    return "Land" in card.get("type_line", "")


def has_modal_land_back(card: dict[str, Any]) -> bool:
    faces = card.get("card_faces") or []
    return bool(
        card.get("layout") == "modal_dfc"
        and faces
        and not front_is_land(card)
        and any("Land" in face.get("type_line", "") for face in faces[1:])
    )


def repeat_limit(card: dict[str, Any]) -> int | None:
    """Return maximum copies, or None when copies are unlimited."""
    if "Basic" in card.get("type_line", ""):
        return None
    text = card.get("oracle_text") or ""
    if re.search(r"A deck can have any number of cards named", text, re.I):
        return None
    match = re.search(r"A deck can have up to ([a-z]+|\d+) cards named", text, re.I)
    if match:
        token = match.group(1).casefold()
        if token.isdigit():
            return int(token)
        return NUMBER_WORDS.get(token, 1)
    return 1


def card_can_be_commander(card: dict[str, Any]) -> bool:
    type_line = card.get("type_line", "")
    text = card.get("oracle_text") or ""
    return bool(
        ("Legendary" in type_line and "Creature" in type_line)
        or re.search(r"can be your commander", text, re.I)
        or ("Legendary Enchantment" in type_line and "Background" in type_line)
    )


def commander_pair_is_valid(cards: list[dict[str, Any]]) -> bool:
    if len(cards) == 1:
        type_line = cards[0].get("type_line") or ""
        return card_can_be_commander(cards[0]) and "Background" not in type_line
    if len(cards) != 2 or not all(card_can_be_commander(card) for card in cards):
        return False
    texts = [card.get("oracle_text") or "" for card in cards]
    types = [card.get("type_line") or "" for card in cards]
    keywords = [set(card.get("keywords") or []) for card in cards]
    if any("Background" in type_line for type_line in types):
        return any("Choose a Background" in text for text in texts)
    if all("Partner" in card_keywords for card_keywords in keywords):
        return True
    if all("Friends forever" in card_keywords for card_keywords in keywords):
        return True
    if any("Doctor's companion" in text for text in texts) and any(
        "Doctor" in type_line for type_line in types
    ):
        return True
    partner_with = [re.search(r"Partner with ([^\n(]+)", text, re.I) for text in texts]
    if all(partner_with):
        names = [normalize_name(card.get("name", "")) for card in cards]
        return normalize_name(partner_with[0].group(1)) == names[1] and normalize_name(
            partner_with[1].group(1)
        ) == names[0]
    return False


def overlapping_type_counts(card: dict[str, Any], quantity: int, counts: Counter) -> None:
    type_line = card.get("type_line", "")
    matched = False
    for card_type in TYPE_ORDER:
        if re.search(rf"\b{re.escape(card_type)}\b", type_line):
            counts[card_type] += quantity
            matched = True
    if not matched:
        counts["Other"] += quantity


def compact_card(card: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "id",
        "oracle_id",
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
        "security_stamp",
        "set_type",
    )
    return {key: card.get(key) for key in keys} | {
        "card_faces": [
            {
                key: face.get(key)
                for key in ("name", "mana_cost", "type_line", "oracle_text", "colors")
            }
            for face in (card.get("card_faces") or [])
        ]
    }


def issue(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **details}


def make_spellbook_request(
    entries: Iterable[dict[str, Any]],
    commander_oracle_ids: set[str],
    aliases: dict[str, str],
    oracle: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    main: list[dict[str, Any]] = []
    commanders: list[dict[str, Any]] = []
    for entry in entries:
        canonical, card = resolve_card(str(entry["name"]), oracle, aliases)
        record = {"card": canonical, "quantity": int(entry["quantity"])}
        oracle_id = str((card or {}).get("oracle_id") or (card or {}).get("id"))
        (commanders if oracle_id in commander_oracle_ids else main).append(record)
    return {"main": main, "commanders": commanders}


def audit_deck(
    slug: str,
    metadata: dict[str, Any],
    path: Path,
    oracle: dict[str, dict[str, Any]],
    ambiguous: dict[str, list[str]],
    aliases: dict[str, str],
    audit_date: date,
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    try:
        entries = read_deck(path)
    except (OSError, ValueError) as exc:
        return (
            {
                "slug": slug,
                "title": metadata.get("title", slug),
                "file": display_path(path),
                "valid": False,
                "errors": [issue("deck_parse_error", str(exc))],
                "warnings": [],
            },
            {"main": [], "commanders": []},
        )

    configured_commanders = metadata.get("commanders") or []
    commander_cards: list[dict[str, Any]] = []
    commander_oracle_ids: set[str] = set()
    for commander_name in configured_commanders:
        _, card = resolve_card(str(commander_name), oracle, aliases)
        if card is None:
            errors.append(
                issue(
                    "configured_commander_unresolved",
                    f"configured commander does not resolve: {commander_name}",
                    card=commander_name,
                )
            )
            continue
        commander_cards.append(card)
        commander_oracle_ids.add(str(card.get("oracle_id") or card.get("id")))

    if not configured_commanders:
        errors.append(issue("commander_missing_from_config", "no commander configured"))
    elif commander_cards and not commander_pair_is_valid(commander_cards):
        errors.append(
            issue(
                "invalid_commander_configuration",
                "configured commander or commander pair is not recognized as legal",
                commanders=configured_commanders,
            )
        )

    commander_identity: set[str] = set()
    for card in commander_cards:
        commander_identity.update(card.get("color_identity") or [])

    unresolved: list[str] = []
    ambiguous_names: dict[str, list[str]] = {}
    resolved_entries: list[tuple[dict[str, Any], str, dict[str, Any]]] = []
    aggregates: dict[str, dict[str, Any]] = {}
    for entry in entries:
        canonical_name, card = resolve_card(str(entry["name"]), oracle, aliases)
        lookup_key = normalize_name(canonical_name)
        if card is None:
            unresolved.append(str(entry["name"]))
            if lookup_key in ambiguous:
                ambiguous_names[str(entry["name"])] = ambiguous[lookup_key]
            continue
        resolved_entries.append((entry, canonical_name, card))
        oracle_id = str(card.get("oracle_id") or card.get("id"))
        aggregate = aggregates.setdefault(
            oracle_id,
            {
                "quantity": 0,
                "listed_names": [],
                "line_numbers": [],
                "card": card,
            },
        )
        aggregate["quantity"] += int(entry["quantity"])
        aggregate["listed_names"].append(str(entry["name"]))
        aggregate["line_numbers"].append(int(entry["line_number"]))

    if unresolved:
        errors.append(
            issue(
                "unresolved_cards",
                "one or more deck entries did not resolve",
                cards=sorted(unresolved),
            )
        )
    if ambiguous_names:
        errors.append(
            issue(
                "ambiguous_cards",
                "one or more deck entries are ambiguous",
                cards=ambiguous_names,
            )
        )

    total_cards = sum(int(entry["quantity"]) for entry in entries)
    resolved_cards = sum(int(entry["quantity"]) for entry, _, _ in resolved_entries)
    if total_cards != 100:
        errors.append(
            issue(
                "incorrect_card_count",
                f"Commander deck contains {total_cards} cards; expected 100",
                actual=total_cards,
                expected=100,
            )
        )

    commander_quantities: dict[str, int] = {}
    for commander_name, commander_card in zip(configured_commanders, commander_cards):
        oracle_id = str(commander_card.get("oracle_id") or commander_card.get("id"))
        commander_quantities[str(commander_name)] = int(
            (aggregates.get(oracle_id) or {}).get("quantity", 0)
        )
    wrong_commander_quantities = {
        name: quantity for name, quantity in commander_quantities.items() if quantity != 1
    }
    if wrong_commander_quantities:
        errors.append(
            issue(
                "incorrect_commander_quantity",
                "every configured commander must appear exactly once",
                commanders=wrong_commander_quantities,
            )
        )

    duplicate_violations: list[dict[str, Any]] = []
    for aggregate in aggregates.values():
        card = aggregate["card"]
        limit = repeat_limit(card)
        quantity = int(aggregate["quantity"])
        if limit is not None and quantity > limit:
            duplicate_violations.append(
                {
                    "name": card.get("name"),
                    "quantity": quantity,
                    "allowed": limit,
                    "listed_names": aggregate["listed_names"],
                    "line_numbers": aggregate["line_numbers"],
                }
            )
    if duplicate_violations:
        errors.append(
            issue(
                "singleton_violation",
                "one or more Oracle objects exceed their allowed copies",
                cards=duplicate_violations,
            )
        )

    constraints = metadata.get("constraints") or {}
    rule_zero_allowed = {
        normalize_name(str(name)) for name in constraints.get("rule_zero_cards") or []
    }
    bracket_exception_allowed = {
        normalize_name(str(name))
        for name in constraints.get("bracket_exception_cards") or []
    }
    present_names = {
        normalize_name(str(card.get("name", ""))) for _, _, card in resolved_entries
    } | {normalize_name(str(entry["name"])) for entry, _, _ in resolved_entries}
    missing_locked = sorted(
        str(name)
        for name in constraints.get("locked_cards") or []
        if normalize_name(str(name)) not in present_names
    )
    if missing_locked:
        errors.append(
            issue(
                "locked_card_missing",
                "one or more locked cards are absent",
                cards=missing_locked,
            )
        )

    type_counts: Counter = Counter()
    printed_lands = 0
    modal_land_backs = 0
    game_changers: list[str] = []
    bracket_exception_cards: list[str] = []
    legality_issues: list[dict[str, Any]] = []
    banned_cards: list[str] = []
    rule_zero_cards: list[str] = []
    unreleased: list[dict[str, str]] = []
    selected_printing_future: list[dict[str, str]] = []
    identity_violations: list[dict[str, Any]] = []
    card_details: list[dict[str, Any]] = []

    for entry, canonical_name, card in resolved_entries:
        quantity = int(entry["quantity"])
        listed_name = str(entry["name"])
        overlapping_type_counts(card, quantity, type_counts)
        if front_is_land(card):
            printed_lands += quantity
        elif has_modal_land_back(card):
            modal_land_backs += quantity
        if card.get("game_changer"):
            game_changers.extend([listed_name] * quantity)
            normalized_card_names = {
                normalize_name(listed_name),
                normalize_name(canonical_name),
                normalize_name(str(card.get("name", ""))),
            }
            if normalized_card_names & bracket_exception_allowed:
                bracket_exception_cards.extend([listed_name] * quantity)

        commander_status = (card.get("legalities") or {}).get("commander", "not_legal")
        normalized_card_names = {
            normalize_name(listed_name),
            normalize_name(canonical_name),
            normalize_name(str(card.get("name", ""))),
        }
        approved_rule_zero = bool(normalized_card_names & rule_zero_allowed)
        if commander_status != "legal":
            legality_record = {
                "name": listed_name,
                "status": commander_status,
                "rule_zero_approved": approved_rule_zero,
            }
            legality_issues.append(legality_record)
            if commander_status == "banned":
                banned_cards.extend([listed_name] * quantity)
            if approved_rule_zero:
                if listed_name not in rule_zero_cards:
                    rule_zero_cards.extend([listed_name] * quantity)
            else:
                errors.append(
                    issue(
                        "commander_legality_violation",
                        f"{listed_name} is {commander_status} in Commander",
                        card=listed_name,
                        status=commander_status,
                    )
                )

        released_at = card.get("released_at")
        if released_at and date.fromisoformat(released_at) > audit_date:
            release_record = {"name": listed_name, "released_at": released_at}
            if commander_status == "legal":
                selected_printing_future.append(release_record)
            else:
                unreleased.append(release_record)

        identity = set(card.get("color_identity") or [])
        if commander_cards and not identity.issubset(commander_identity):
            violation = {"name": listed_name, "identity": sorted(identity)}
            identity_violations.append(violation)
            if approved_rule_zero:
                if listed_name not in rule_zero_cards:
                    rule_zero_cards.extend([listed_name] * quantity)
            else:
                errors.append(
                    issue(
                        "color_identity_violation",
                        f"{listed_name} is outside the commander's color identity",
                        **violation,
                    )
                )

        card_details.append(
            {
                "listed_name": listed_name,
                "canonical_name": canonical_name,
                "quantity": quantity,
                "line_number": entry["line_number"],
                "is_commander": str(card.get("oracle_id") or card.get("id"))
                in commander_oracle_ids,
                "card": compact_card(card),
            }
        )

    game_changer_max = constraints.get("game_changer_max")
    uncovered_game_changers = list(game_changers)
    for exception in bracket_exception_cards:
        uncovered_game_changers.remove(exception)
    if game_changer_max is not None and len(uncovered_game_changers) > int(
        game_changer_max
    ):
        errors.append(
            issue(
                "game_changer_limit_exceeded",
                f"deck has {len(uncovered_game_changers)} unexcepted Game Changers; "
                f"maximum is {game_changer_max}",
                cards=uncovered_game_changers,
                actual=len(uncovered_game_changers),
                maximum=int(game_changer_max),
            )
        )

    present_bracket_exceptions = {
        normalize_name(name) for name in bracket_exception_cards
    }
    missing_bracket_exceptions = sorted(
        str(name)
        for name in constraints.get("bracket_exception_cards") or []
        if normalize_name(str(name)) not in present_bracket_exceptions
    )
    if missing_bracket_exceptions:
        errors.append(
            issue(
                "bracket_exception_card_missing",
                "one or more configured bracket exception cards are absent or are not Game Changers",
                cards=missing_bracket_exceptions,
            )
        )

    if selected_printing_future:
        warnings.append(
            issue(
                "future_representative_printings",
                "Oracle selected future reprints of already-legal cards; these are not unreleased card identities",
                cards=selected_printing_future,
            )
        )
    if rule_zero_cards:
        warnings.append(
            issue(
                "approved_rule_zero_cards",
                "deck relies on explicitly approved Rule Zero cards",
                cards=rule_zero_cards,
            )
        )
    if bracket_exception_cards:
        warnings.append(
            issue(
                "configured_bracket_exceptions",
                "deck exceeds its ordinary Game Changer ceiling only through explicitly configured cards",
                cards=bracket_exception_cards,
            )
        )

    request = make_spellbook_request(entries, commander_oracle_ids, aliases, oracle)
    deck_sha = sha256_file(path)
    request_sha = sha256_bytes(canonical_json_bytes(request))
    commander_quantity_total = sum(commander_quantities.values())
    summary = {
        "slug": slug,
        "title": metadata.get("title", slug),
        "commanders": configured_commanders,
        "commander": configured_commanders[0] if len(configured_commanders) == 1 else None,
        "moxfield_id": metadata.get("moxfield_id"),
        "moxfield_url": (
            f"https://moxfield.com/decks/{metadata['moxfield_id']}"
            if metadata.get("moxfield_id")
            else None
        ),
        "file": display_path(path),
        "deck_sha256": deck_sha,
        "spellbook_request_sha256": request_sha,
        "valid": not errors,
        "analysis_ready": not errors,
        "errors": errors,
        "warnings": warnings,
        "constraints": constraints,
        "total_cards": total_cards,
        "resolved_cards": resolved_cards,
        "unique_lines": len(entries),
        "unique_oracle_objects": len(aggregates),
        "commander_quantity": commander_quantity_total,
        "commander_quantities": commander_quantities,
        "commander_identity": sorted(commander_identity),
        "type_counts": dict(type_counts),
        "overlapping_type_counts": dict(type_counts),
        "printed_lands": printed_lands,
        "mdfc_lands": modal_land_backs,
        "modal_land_backs": modal_land_backs,
        "effective_land_faces": printed_lands + modal_land_backs,
        "game_changer_count": len(game_changers),
        "game_changers": game_changers,
        "bracket_exception_cards": bracket_exception_cards,
        "not_commander_legal": [record["name"] for record in legality_issues],
        "legality_issues": legality_issues,
        "banned_cards": banned_cards,
        "rule_zero_cards": rule_zero_cards,
        "unreleased": unreleased,
        "selected_printing_future": selected_printing_future,
        "identity_violations": identity_violations,
        "nonbasic_duplicates": duplicate_violations,
        "unresolved": unresolved,
        "ambiguous": ambiguous_names,
        "cards": card_details,
    }
    return summary, request


def build_audit(
    *,
    collection_path: Path = ROOT / "collection.json",
    decks_dir: Path = ROOT / "decks",
    oracle_path: Path | None = None,
    audit_date: date | None = None,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    audit_date = audit_date or date.today()
    collection = json_load(collection_path)
    aliases = {
        normalize_name(str(key)): str(value)
        for key, value in (collection.get("aliases") or {}).items()
    }
    oracle_path = choose_oracle_path(oracle_path)
    if not oracle_path.exists():
        raise AuditConfigurationError(f"Oracle corpus not found: {oracle_path}")
    oracle, ambiguous = load_oracle(oracle_path)
    metadata_path = ROOT / "data/oracle-bulk-metadata.json"
    oracle_metadata = json_load(metadata_path) if metadata_path.exists() else {}

    audits: dict[str, dict[str, Any]] = {}
    requests: dict[str, dict[str, Any]] = {}
    configured_decks = collection.get("decks") or {}
    if not configured_decks:
        raise AuditConfigurationError("collection.json contains no decks")
    for slug, metadata in configured_decks.items():
        deck_path = decks_dir / f"{slug}.txt"
        audit, request = audit_deck(
            slug,
            metadata,
            deck_path,
            oracle,
            ambiguous,
            aliases,
            audit_date,
        )
        audits[slug] = audit
        requests[slug] = request

    valid_count = sum(1 for deck in audits.values() if deck.get("valid"))
    script_path = Path(__file__).resolve()
    result = {
        "schema_version": SCHEMA_VERSION,
        "audit_date": audit_date.isoformat(),
        "generator": {
            "name": "scripts/audit_decks.py",
            "sha256": sha256_file(script_path),
            "python_requires": ">=3.11",
        },
        "inputs": {
            "collection_file": display_path(collection_path),
            "collection_sha256": sha256_file(collection_path),
            "oracle_file": display_path(oracle_path),
            "oracle_sha256": sha256_file(oracle_path),
            "oracle_source_updated_at": oracle_metadata.get("updated_at"),
            "policy_file": "policy/current.json",
            "policy_sha256": sha256_file(ROOT / "policy/current.json"),
        },
        "summary": {
            "deck_count": len(audits),
            "valid_deck_count": valid_count,
            "invalid_deck_count": len(audits) - valid_count,
            "valid": valid_count == len(audits),
        },
        "decks": audits,
    }
    return result, requests


def compare_bytes(path: Path, expected: bytes) -> bool:
    return path.exists() and path.read_bytes() == expected


def write_or_check(
    result: dict[str, Any],
    requests: dict[str, dict[str, Any]],
    *,
    output: Path,
    requests_dir: Path,
    check: bool,
) -> list[str]:
    mismatches: list[str] = []
    expected_audit = json_bytes(result)
    if check:
        if not compare_bytes(output, expected_audit):
            mismatches.append(display_path(output))
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(expected_audit)
    for slug, request in requests.items():
        request_path = requests_dir / f"{slug}.json"
        expected_request = json_bytes(request)
        if check:
            if not compare_bytes(request_path, expected_request):
                mismatches.append(display_path(request_path))
        else:
            requests_dir.mkdir(parents=True, exist_ok=True)
            request_path.write_bytes(expected_request)
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", type=Path, default=ROOT / "collection.json")
    parser.add_argument("--decks-dir", type=Path, default=ROOT / "decks")
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "data/audit.json")
    parser.add_argument(
        "--requests-dir",
        type=Path,
        default=ROOT / "data/spellbook-requests",
    )
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--check", action="store_true", help="compare without writing")
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="return success even when one or more decks are invalid",
    )
    args = parser.parse_args()

    try:
        result, requests = build_audit(
            collection_path=args.collection.resolve(),
            decks_dir=args.decks_dir.resolve(),
            oracle_path=args.oracle.resolve() if args.oracle else None,
            audit_date=args.date,
        )
        mismatches = write_or_check(
            result,
            requests,
            output=args.output.resolve(),
            requests_dir=args.requests_dir.resolve(),
            check=args.check,
        )
    except AuditConfigurationError as exc:
        print(f"AUDIT CONFIGURATION ERROR: {exc}", file=sys.stderr)
        return 2

    if mismatches:
        print("STALE GENERATED ARTIFACTS:", file=sys.stderr)
        for mismatch in mismatches:
            print(f"- {mismatch}", file=sys.stderr)
        return 1

    invalid = [slug for slug, deck in result["decks"].items() if not deck.get("valid")]
    if invalid:
        print("INVALID DECKS:", file=sys.stderr)
        for slug in invalid:
            print(f"- {slug}", file=sys.stderr)
            for audit_issue in result["decks"][slug].get("errors", []):
                print(
                    f"  [{audit_issue['code']}] {audit_issue['message']}",
                    file=sys.stderr,
                )
        return 0 if args.no_fail else 1

    action = "verified" if args.check else "wrote"
    print(f"{action} {len(result['decks'])} valid Commander deck audits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
