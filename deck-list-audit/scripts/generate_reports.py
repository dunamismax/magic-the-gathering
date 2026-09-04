#!/usr/bin/env python3
"""Generate compact collection documentation from the deterministic audit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from audit_decks import ROOT, json_bytes, json_load, sha256_bytes, sha256_file


def deck_readme(collection: dict[str, Any], audit: dict[str, Any]) -> str:
    audit_date = audit["audit_date"]
    lines = [
        "# dunamismax local Commander deck snapshots",
        "",
        f"Current local source files were audited on {audit_date}. Every listed deck",
        "is linked to its exact SHA-256 and public Moxfield reference.",
        "",
        "| Deck | Target | Moxfield updated | Refreshed locally | Local list | Options | SHA-256 |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    for slug, metadata in collection["decks"].items():
        deck = audit["decks"][slug]
        title = str(metadata["title"]).replace("|", "\\|")
        moxfield = f"https://moxfield.com/decks/{metadata['moxfield_id']}"
        sideboard = metadata.get("sideboard") or {}
        options = (
            f"[sideboard]({str(sideboard['file']).removeprefix('decks/')})"
            if sideboard.get("file")
            else "None"
        )
        lines.append(
            f"| [{title}]({moxfield}) | B{metadata['constraints']['target_bracket']} | "
            f"{metadata['source_updated_on']} | {metadata['source_refreshed_on']} | "
            f"[list]({slug}.txt) | {options} | `{deck['deck_sha256']}` |"
        )
    documented_switches = [
        (slug, metadata)
        for slug, metadata in collection["decks"].items()
        if metadata.get("sideboard")
    ]
    if documented_switches:
        lines.extend(["", "## Documented configuration switches"])
        for slug, metadata in documented_switches:
            sideboard = metadata["sideboard"]
            lines.extend(
                [
                    "",
                    f"### {metadata['title']}",
                    "",
                    metadata["constraints"]["experience"],
                    "",
                    sideboard["purpose"],
                    "",
                    "**Remove:** " + "; ".join(sideboard["swap_out"]) + ".",
                    "",
                    f"**Add:** the complete [{slug} sideboard]"
                    f"({str(sideboard['file']).removeprefix('decks/')}).",
                    "",
                    "Enable Tags on Moxfield to see every card's role, and read the",
                    "Primer for the complete play guide and combo explanation.",
                ]
            )
    aliases = collection.get("aliases") or {}
    lines.extend(
        [
            "",
            "`Moxfield updated` is the public page date. `Refreshed locally` records",
            "when the export was last downloaded and verified. The local text files",
            "are the source of truth. Alternate/flavor names are",
            "resolved to shared Oracle objects before validation:",
            "",
        ]
    )
    for listed, canonical in aliases.items():
        lines.append(f"- `{listed}` -> `{canonical}`")
    lines.extend(
        [
            "",
            "Regenerate this file with `just report`; do not edit its hashes manually.",
            "",
        ]
    )
    return "\n".join(lines)


def collection_summary(collection: dict[str, Any], audit: dict[str, Any]) -> str:
    lines = [
        "# Generated Commander collection summary",
        "",
        f"Audit date: {audit['audit_date']}",
        f"Oracle snapshot: {audit['inputs']['oracle_source_updated_at']}",
        f"Policy lock: {json_load(ROOT / 'policy/current.json')['verified_on']}",
        "",
        "This file contains deterministic construction results. Bracket and social",
        "conclusions require the relevant rubric and dated human/AI judgment.",
        "",
        "| Deck | Valid | Cards | Printed lands | MDFC lands | Game Changers | Rule Zero | Bracket exceptions | SHA-256 |",
        "|---|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for slug in collection["decks"]:
        deck = audit["decks"][slug]
        rule_zero = ", ".join(deck["rule_zero_cards"]) or "None"
        bracket_exceptions = ", ".join(deck["bracket_exception_cards"]) or "None"
        lines.append(
            f"| {deck['title'].replace('|', '/')} | {'yes' if deck['valid'] else 'no'} | "
            f"{deck['total_cards']} | {deck['printed_lands']} | {deck['mdfc_lands']} | "
            f"{deck['game_changer_count']} | {rule_zero} | {bracket_exceptions} | "
            f"`{deck['deck_sha256'][:12]}` |"
        )
    lines.extend(
        [
            "",
            "## Validation notes",
            "",
            "- Type counts overlap for multi-type and double-faced cards.",
            "- `selected_printing_future` warnings identify future reprints of card",
            "  identities that are already legal; they are not Rule Zero cards.",
            "- A valid deterministic audit does not prove combo completeness.",
            "- Use `just check-current` before describing these results as current.",
            "",
        ]
    )
    return "\n".join(lines)


def expected_outputs() -> dict[Path, bytes]:
    collection = json_load(ROOT / "collection.json")
    audit = json_load(ROOT / "data/audit.json")
    readme_bytes = deck_readme(collection, audit).encode("utf-8")
    summary_bytes = collection_summary(collection, audit).encode("utf-8")
    manifest = {
        "schema_version": 1,
        "audit_date": audit["audit_date"],
        "audit_sha256": sha256_file(ROOT / "data/audit.json"),
        "collection_sha256": sha256_file(ROOT / "collection.json"),
        "moxfield_refresh_sha256": sha256_file(ROOT / "data/moxfield-refresh.json"),
        "decks_readme_sha256": sha256_bytes(readme_bytes),
        "collection_summary_sha256": sha256_bytes(summary_bytes),
        "functional_analysis_sha256": sha256_file(
            ROOT / "generated/functional-analysis.json"
        ),
        "deck_sha256": {
            slug: deck["deck_sha256"] for slug, deck in audit["decks"].items()
        },
    }
    return {
        ROOT / "decks/README.md": readme_bytes,
        ROOT / "generated/collection-summary.md": summary_bytes,
        ROOT / "generated/manifest.json": json_bytes(manifest),
    }


def generate_outputs(*, check: bool = False) -> list[str]:
    mismatches: list[str] = []
    for path, expected in expected_outputs().items():
        if check:
            if not path.exists() or path.read_bytes() != expected:
                mismatches.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    mismatches = generate_outputs(check=args.check)
    if mismatches:
        print("STALE GENERATED REPORTS:", file=sys.stderr)
        for path in mismatches:
            print(f"- {path}", file=sys.stderr)
        return 1
    print("verified generated reports" if args.check else "generated collection reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
