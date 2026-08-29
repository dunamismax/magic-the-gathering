#!/usr/bin/env python3
"""Apply a baseline-locked Commander Adds/Cuts plan transactionally."""

from __future__ import annotations

import argparse
import difflib
import os
import shutil
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from audit_decks import (
    ROOT,
    build_audit,
    json_bytes,
    json_load,
    normalize_name,
    read_deck,
    sha256_file,
    write_or_check,
)
from generate_reports import generate_outputs


def quantities(items: list[dict[str, Any]], label: str) -> int:
    total = 0
    for item in items:
        if not isinstance(item, dict) or not item.get("name"):
            raise RuntimeError(f"every {label} entry needs a card name")
        quantity = int(item.get("quantity", 1))
        if quantity <= 0:
            raise RuntimeError(f"{label} quantity must be positive: {item}")
        total += quantity
    return total


def apply_items(
    entries: list[dict[str, Any]],
    adds: list[dict[str, Any]],
    cuts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remaining = [dict(entry) for entry in entries]
    for cut in cuts:
        needed = int(cut.get("quantity", 1))
        key = normalize_name(str(cut["name"]))
        for entry in remaining:
            if normalize_name(str(entry["name"])) != key:
                continue
            take = min(needed, int(entry["quantity"]))
            entry["quantity"] -= take
            needed -= take
            if needed == 0:
                break
        if needed:
            raise RuntimeError(f"cut is not present in sufficient quantity: {cut['name']}")
    remaining = [entry for entry in remaining if int(entry["quantity"]) > 0]
    by_name = {normalize_name(str(entry["name"])): entry for entry in remaining}
    for addition in adds:
        name = str(addition["name"])
        quantity = int(addition.get("quantity", 1))
        key = normalize_name(name)
        if key in by_name:
            by_name[key]["quantity"] += quantity
        else:
            entry = {"name": name, "quantity": quantity, "line_number": 0}
            remaining.append(entry)
            by_name[key] = entry
    return remaining


def render_deck(entries: list[dict[str, Any]], commanders: list[str]) -> bytes:
    commander_keys = {normalize_name(name) for name in commanders}
    commander_entries = [
        entry for entry in entries if normalize_name(str(entry["name"])) in commander_keys
    ]
    main_entries = [
        entry for entry in entries if normalize_name(str(entry["name"])) not in commander_keys
    ]
    main_entries.sort(key=lambda entry: normalize_name(str(entry["name"])))
    commander_entries.sort(key=lambda entry: commanders.index(str(entry["name"])) if str(entry["name"]) in commanders else 99)
    lines = [f"{entry['quantity']} {entry['name']}" for entry in main_entries]
    if commander_entries:
        lines.append("")
        lines.extend(f"{entry['quantity']} {entry['name']}" for entry in commander_entries)
    return ("\n".join(lines) + "\n").encode("utf-8")


def atomic_write(path: Path, content: bytes) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def apply_plan(plan_path: Path, *, apply: bool) -> None:
    plan = json_load(plan_path)
    if plan.get("schema_version") != 1:
        raise RuntimeError("change plan schema_version must be 1")
    slug = str(plan.get("deck") or "")
    collection = json_load(ROOT / "collection.json")
    metadata = collection["decks"].get(slug)
    if metadata is None:
        raise RuntimeError(f"unknown deck: {slug}")
    target = ROOT / f"decks/{slug}.txt"
    baseline_sha = str(plan.get("baseline_sha256") or "")
    actual_sha = sha256_file(target)
    if baseline_sha != actual_sha:
        raise RuntimeError(
            f"baseline SHA mismatch: plan={baseline_sha or '<missing>'}, current={actual_sha}"
        )
    adds = plan.get("adds") or []
    cuts = plan.get("cuts") or []
    if quantities(adds, "add") != quantities(cuts, "cut"):
        raise RuntimeError("Adds and Cuts must have equal total quantities")
    locked = {normalize_name(name) for name in metadata["constraints"].get("locked_cards") or []}
    attempted_locked_cuts = [
        item["name"] for item in cuts if normalize_name(str(item["name"])) in locked
    ]
    if attempted_locked_cuts:
        raise RuntimeError(f"plan cuts locked cards: {', '.join(attempted_locked_cuts)}")

    entries = read_deck(target)
    changed_entries = apply_items(entries, adds, cuts)
    changed_content = render_deck(changed_entries, metadata["commanders"])
    current_content = target.read_bytes()
    if changed_content == current_content:
        raise RuntimeError("change plan produces no deck change")

    with tempfile.TemporaryDirectory(prefix="deck-change-") as temporary_directory:
        temporary_decks = Path(temporary_directory)
        for deck_file in (ROOT / "decks").glob("*.txt"):
            shutil.copy2(deck_file, temporary_decks / deck_file.name)
        (temporary_decks / target.name).write_bytes(changed_content)
        before, _ = build_audit(audit_date=date.today())
        after, _ = build_audit(decks_dir=temporary_decks, audit_date=date.today())
        before_deck = before["decks"][slug]
        after_deck = after["decks"][slug]
        if not after_deck["valid"]:
            details = "; ".join(error["message"] for error in after_deck["errors"])
            raise RuntimeError(f"post-change audit failed: {details}")
        policy = plan.get("game_changer_policy", "no-increase")
        if policy == "no-increase" and after_deck["game_changer_count"] > before_deck[
            "game_changer_count"
        ]:
            raise RuntimeError("post-change Game Changer count increased")

    diff = difflib.unified_diff(
        current_content.decode("utf-8").splitlines(),
        changed_content.decode("utf-8").splitlines(),
        fromfile=f"{slug}.txt (before)",
        tofile=f"{slug}.txt (after)",
        lineterm="",
    )
    print("\n".join(diff))
    print(
        f"validated: cards={after_deck['total_cards']}, "
        f"Game Changers={before_deck['game_changer_count']}->{after_deck['game_changer_count']}, "
        f"printed lands={before_deck['printed_lands']}->{after_deck['printed_lands']}"
    )
    if not apply:
        print("dry run only; pass --apply to write the deck")
        return

    atomic_write(target, changed_content)
    result, requests = build_audit(audit_date=date.today())
    write_or_check(
        result,
        requests,
        output=ROOT / "data/audit.json",
        requests_dir=ROOT / "data/spellbook-requests",
        check=False,
    )
    from classify_roles import build_analysis

    (ROOT / "generated/functional-analysis.json").write_bytes(json_bytes(build_analysis()))
    generate_outputs(check=False)
    applied_record = dict(plan)
    applied_record["application"] = {
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "before_sha256": actual_sha,
        "after_sha256": sha256_file(target),
        "post_change_audit_valid": True,
        "external_combo_evidence_stale": True,
        "human_reports_stale": True,
    }
    applied_path = ROOT / f"changes/applied/{slug}-{sha256_file(target)[:12]}.json"
    applied_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(applied_path, json_bytes(applied_record))
    print(f"applied {slug}; recorded {applied_path.relative_to(ROOT)}")
    print("Spellbook evidence and human reports must be refreshed/reviewed before recertification.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        apply_plan(args.plan.resolve(), apply=args.apply)
    except RuntimeError as exc:
        print(f"CHANGE ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
