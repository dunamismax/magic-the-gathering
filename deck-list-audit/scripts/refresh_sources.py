#!/usr/bin/env python3
"""Refresh Oracle/Spellbook evidence or import a local Moxfield text export."""

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from audit_decks import (
    ROOT,
    build_audit,
    canonical_json_bytes,
    json_bytes,
    json_load,
    read_deck,
    sha256_bytes,
    sha256_file,
    write_or_check,
)


USER_AGENT = "dunamismax-commander-audit/2.0 (local personal collection tool)"


def request_json(
    url: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout: int = 90,
) -> dict[str, Any]:
    data = canonical_json_bytes(payload) if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl.create_default_context(),
        ) as response:
            value = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"request failed for {url}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"expected a JSON object from {url}")
    return value


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def refresh_oracle() -> None:
    collection = json_load(ROOT / "collection.json")
    index = request_json(collection["sources"]["scryfall_bulk_index"])
    records = index.get("data") or []
    metadata = next((item for item in records if item.get("type") == "oracle_cards"), None)
    if not metadata or not metadata.get("jsonl_download_uri"):
        raise RuntimeError("Scryfall bulk index did not contain Oracle JSONL metadata")
    cache_path = ROOT / "cache/scryfall/oracle-cards.jsonl.gz"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        metadata["jsonl_download_uri"],
        headers={"User-Agent": USER_AGENT, "Accept": "application/gzip"},
    )
    with tempfile.NamedTemporaryFile(dir=cache_path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                shutil.copyfileobj(response, handle)
        except (urllib.error.URLError, TimeoutError) as exc:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(f"Oracle download failed: {exc}") from exc
    try:
        with gzip.open(temporary, "rb") as handle:
            while handle.read(1024 * 1024):
                pass
    except (OSError, EOFError) as exc:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"downloaded Oracle corpus is invalid: {exc}") from exc
    os.replace(temporary, cache_path)
    metadata = dict(metadata)
    metadata["local_sha256"] = sha256_file(cache_path)
    metadata["cached_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write(ROOT / "data/bulk-index.json", json_bytes(index))
    atomic_write(ROOT / "data/oracle-bulk-metadata.json", json_bytes(metadata))
    print(f"refreshed Oracle corpus: {metadata['updated_at']} ({metadata['local_sha256']})")


def normalize_export(path: Path) -> bytes:
    entries = read_deck(path)
    return ("\n".join(f"{entry['quantity']} {entry['name']}" for entry in entries) + "\n").encode(
        "utf-8"
    )


def import_moxfield(slug: str, source: Path, expected_sha: str) -> None:
    collection = json_load(ROOT / "collection.json")
    if slug not in collection["decks"]:
        raise RuntimeError(f"unknown deck: {slug}")
    target = ROOT / f"decks/{slug}.txt"
    actual_sha = sha256_file(target)
    if actual_sha != expected_sha:
        raise RuntimeError(
            f"baseline SHA mismatch for {slug}: expected {expected_sha}, found {actual_sha}"
        )
    normalized = normalize_export(source)
    with tempfile.TemporaryDirectory(prefix="deck-import-") as temporary_directory:
        temp_decks = Path(temporary_directory)
        for deck_file in (ROOT / "decks").glob("*.txt"):
            shutil.copy2(deck_file, temp_decks / deck_file.name)
        (temp_decks / target.name).write_bytes(normalized)
        result, _ = build_audit(decks_dir=temp_decks, audit_date=date.today())
        imported = result["decks"][slug]
        if not imported["valid"]:
            messages = "; ".join(error["message"] for error in imported["errors"])
            raise RuntimeError(f"imported deck is invalid: {messages}")
    atomic_write(target, normalized)
    print(f"imported {slug}: {actual_sha} -> {sha256_file(target)}")
    regenerate_local_artifacts()


def spellbook_spec_version() -> str | None:
    spec = ROOT / "data/commander-spellbook-openapi.yaml"
    for line in spec.read_text(encoding="utf-8").splitlines()[:10]:
        if line.strip().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return None


def load_spellbook_manifest() -> dict[str, Any]:
    path = ROOT / "data/spellbook-results/manifest.json"
    if path.exists():
        return json_load(path)
    return {"schema_version": 1, "api_version": spellbook_spec_version(), "decks": {}}


def spellbook_record(slug: str, fetched_on: str) -> dict[str, Any]:
    request_path = ROOT / f"data/spellbook-requests/{slug}.json"
    estimate_path = ROOT / f"data/spellbook-results/{slug}-estimate.json"
    combos_path = ROOT / f"data/spellbook-results/{slug}-combos.json"
    return {
        "fetched_on": fetched_on,
        "request_sha256": sha256_bytes(canonical_json_bytes(json_load(request_path))),
        "estimate_file": str(estimate_path.relative_to(ROOT)),
        "estimate_sha256": sha256_file(estimate_path),
        "combos_file": str(combos_path.relative_to(ROOT)),
        "combos_sha256": sha256_file(combos_path),
    }


def index_existing_spellbook(fetched_on: str) -> None:
    audit = json_load(ROOT / "data/audit.json")
    manifest = {
        "schema_version": 1,
        "api_base": json_load(ROOT / "collection.json")["sources"][
            "commander_spellbook_base"
        ],
        "api_version": spellbook_spec_version(),
        "decks": {},
    }
    for slug in audit["decks"]:
        manifest["decks"][slug] = spellbook_record(slug, fetched_on)
    atomic_write(ROOT / "data/spellbook-results/manifest.json", json_bytes(manifest))
    print(f"indexed existing Spellbook evidence for {len(manifest['decks'])} decks")


def refresh_spellbook(slug: str, allow_deck_upload: bool) -> None:
    if not allow_deck_upload:
        raise RuntimeError("refusing deck upload without --allow-deck-upload")
    collection = json_load(ROOT / "collection.json")
    metadata = collection["decks"].get(slug)
    if metadata is None:
        raise RuntimeError(f"unknown deck: {slug}")
    if metadata.get("visibility") != "public":
        raise RuntimeError(f"refusing to upload non-public deck: {slug}")
    request_path = ROOT / f"data/spellbook-requests/{slug}.json"
    payload = json_load(request_path)
    base = collection["sources"]["commander_spellbook_base"].rstrip("/")
    estimate = request_json(f"{base}/estimate-bracket", payload=payload)
    combos = request_json(f"{base}/find-my-combos", payload=payload)
    estimate_path = ROOT / f"data/spellbook-results/{slug}-estimate.json"
    combos_path = ROOT / f"data/spellbook-results/{slug}-combos.json"
    atomic_write(estimate_path, json_bytes(estimate))
    atomic_write(combos_path, json_bytes(combos))
    manifest = load_spellbook_manifest()
    manifest["api_base"] = base
    manifest["api_version"] = spellbook_spec_version()
    manifest.setdefault("decks", {})[slug] = spellbook_record(slug, date.today().isoformat())
    atomic_write(ROOT / "data/spellbook-results/manifest.json", json_bytes(manifest))
    print(f"refreshed Commander Spellbook evidence for public deck {slug}")


def regenerate_local_artifacts() -> None:
    result, requests = build_audit(audit_date=date.today())
    write_or_check(
        result,
        requests,
        output=ROOT / "data/audit.json",
        requests_dir=ROOT / "data/spellbook-requests",
        check=False,
    )
    from classify_roles import build_analysis
    from generate_reports import generate_outputs

    (ROOT / "generated/functional-analysis.json").write_bytes(json_bytes(build_analysis()))
    generate_outputs(check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("oracle")
    import_parser = subparsers.add_parser("import-moxfield")
    import_parser.add_argument("--deck", required=True)
    import_parser.add_argument("--file", type=Path, required=True)
    import_parser.add_argument("--expected-sha", required=True)
    spellbook_parser = subparsers.add_parser("spellbook")
    spellbook_parser.add_argument("--deck", required=True)
    spellbook_parser.add_argument("--allow-deck-upload", action="store_true")
    index_parser = subparsers.add_parser("index-existing-spellbook")
    index_parser.add_argument("--fetched-on", required=True)
    args = parser.parse_args()

    try:
        if args.command == "oracle":
            refresh_oracle()
            regenerate_local_artifacts()
        elif args.command == "import-moxfield":
            import_moxfield(args.deck, args.file.resolve(), args.expected_sha)
        elif args.command == "spellbook":
            refresh_spellbook(args.deck, args.allow_deck_upload)
        elif args.command == "index-existing-spellbook":
            index_existing_spellbook(args.fetched_on)
    except RuntimeError as exc:
        print(f"REFRESH ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
