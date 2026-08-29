#!/usr/bin/env python3
"""Validate the complete Commander audit system and its evidence provenance."""

from __future__ import annotations

import argparse
import gzip
import shutil
import sys
from datetime import date, datetime
from typing import Any

from audit_decks import (
    ROOT,
    build_audit,
    canonical_json_bytes,
    json_bytes,
    json_load,
    normalize_name,
    sha256_bytes,
    sha256_file,
)
from generate_reports import generate_outputs


REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "Justfile",
    "collection.json",
    "policy/current.json",
    "knowledge/combo-adjudications.json",
    "knowledge/role-taxonomy.json",
    "knowledge/card-role-overrides.json",
    "scripts/audit_decks.py",
    "scripts/apply_change.py",
    "scripts/classify_roles.py",
    "scripts/generate_reports.py",
    "scripts/refresh_sources.py",
    "data/commander-spellbook-openapi.yaml",
)


def age_days(value: str, today: date) -> int:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    return (today - parsed).days


def doctor() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if sys.version_info < (3, 11):
        errors.append("Python 3.11 or newer is required")
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            errors.append(f"missing required file: {relative}")
    if shutil.which("just") is None:
        warnings.append("just is not installed; direct Python commands still work")
    if shutil.which("ruff") is None:
        warnings.append("ruff is not installed; lint command is unavailable")
    for path in sorted(ROOT.rglob("*.json")):
        if "cache" in path.parts:
            continue
        try:
            json_load(path)
        except Exception as exc:
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
    oracle = ROOT / "cache/scryfall/oracle-cards.jsonl.gz"
    if not oracle.exists():
        oracle = ROOT / "data/oracle-cards.jsonl.gz"
    try:
        with gzip.open(oracle, "rb") as handle:
            while handle.read(1024 * 1024):
                pass
    except (OSError, EOFError) as exc:
        errors.append(f"invalid Oracle gzip: {exc}")
    return errors, warnings


def validate_internal_artifacts() -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    stored = json_load(ROOT / "data/audit.json")
    stored_date = date.fromisoformat(stored["audit_date"])
    expected, requests = build_audit(audit_date=stored_date)
    if (ROOT / "data/audit.json").read_bytes() != json_bytes(expected):
        errors.append("data/audit.json is stale; run `just audit`")
    for slug, request in requests.items():
        path = ROOT / f"data/spellbook-requests/{slug}.json"
        if not path.exists() or path.read_bytes() != json_bytes(request):
            errors.append(f"stale Spellbook request: {path.relative_to(ROOT)}")
    report_mismatches = generate_outputs(check=True)
    errors.extend(f"stale generated report: {path}" for path in report_mismatches)
    from classify_roles import build_analysis

    role_path = ROOT / "generated/functional-analysis.json"
    if not role_path.exists() or role_path.read_bytes() != json_bytes(build_analysis()):
        errors.append("stale functional role analysis; run `just audit`")
    return errors, warnings, expected


def validate_spellbook(
    audit: dict[str, Any], *, require_current: bool, today: date
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = ROOT / "data/spellbook-results/manifest.json"
    if not manifest_path.exists():
        return ["missing Spellbook evidence manifest"], warnings
    manifest = json_load(manifest_path)
    freshness = json_load(ROOT / "collection.json")["freshness"]["spellbook_max_age_days"]
    for slug, deck in audit["decks"].items():
        record = (manifest.get("decks") or {}).get(slug)
        if record is None:
            errors.append(f"missing Spellbook evidence record: {slug}")
            continue
        status = record.get("status", "exact-list-scan")
        evidence_date = record.get("fetched_on")
        if status == "exact-list-scan":
            if record.get("request_sha256") != deck["spellbook_request_sha256"]:
                errors.append(f"stale Spellbook evidence for changed deck: {slug}")
        elif status == "delta-reviewed":
            if record.get("current_request_sha256") != deck["spellbook_request_sha256"]:
                errors.append(f"stale Spellbook delta review for changed deck: {slug}")
            if record.get("current_deck_sha256") != deck["deck_sha256"]:
                errors.append(f"delta review targets the wrong deck hash: {slug}")
            review = record.get("delta_review") or {}
            applied_path = ROOT / (
                f"changes/applied/{slug}-{deck['deck_sha256'][:12]}.json"
            )
            if not applied_path.exists():
                errors.append(f"delta review has no matching applied change: {slug}")
            else:
                applied = json_load(applied_path)
                application = applied.get("application") or {}
                if application.get("before_sha256") != record.get(
                    "source_deck_sha256"
                ):
                    errors.append(f"delta review source hash is unproven: {slug}")
                if application.get("after_sha256") != deck["deck_sha256"]:
                    errors.append(f"delta review applied hash is stale: {slug}")
                planned_adds = {
                    normalize_name(item["name"]) for item in applied.get("adds") or []
                }
                planned_cuts = {
                    normalize_name(item["name"]) for item in applied.get("cuts") or []
                }
                reviewed_adds = {
                    normalize_name(name) for name in review.get("added") or []
                }
                reviewed_cuts = {
                    normalize_name(name) for name in review.get("removed") or []
                }
                if planned_adds != reviewed_adds or planned_cuts != reviewed_cuts:
                    errors.append(f"delta review does not match applied change: {slug}")
            current_cards = {
                normalize_name(card["canonical_name"]) for card in deck["cards"]
            }
            for name in review.get("added") or []:
                if normalize_name(name) not in current_cards:
                    errors.append(f"delta-reviewed add is absent from {slug}: {name}")
            for name in review.get("removed") or []:
                if normalize_name(name) in current_cards:
                    errors.append(f"delta-reviewed cut is still present in {slug}: {name}")
            evidence_date = record.get("delta_reviewed_on")
            if not evidence_date:
                errors.append(f"delta review has no review date: {slug}")
            warnings.append(
                f"{slug} uses a current manual delta review over a dated prior "
                "exact-list Spellbook scan; no revised full list was uploaded"
            )
        else:
            errors.append(f"unknown Spellbook evidence status for {slug}: {status}")
        for file_key, hash_key in (
            ("estimate_file", "estimate_sha256"),
            ("combos_file", "combos_sha256"),
        ):
            path = ROOT / str(record.get(file_key, ""))
            if not path.exists():
                errors.append(f"missing Spellbook result for {slug}: {path}")
            elif sha256_file(path) != record.get(hash_key):
                errors.append(f"modified Spellbook result without manifest update: {path}")
        if require_current and evidence_date and age_days(evidence_date, today) > int(
            freshness
        ):
            errors.append(
                f"Spellbook evidence for {slug} is older than {freshness} days"
            )
    return errors, warnings


def validate_adjudications(audit: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    knowledge = json_load(ROOT / "knowledge/combo-adjudications.json")
    covered: set[str] = set()
    for record in knowledge.get("decks") or []:
        slug = record.get("deck")
        if slug not in audit["decks"]:
            errors.append(f"combo adjudication references unknown deck: {slug}")
            continue
        covered.add(slug)
        if record.get("deck_sha256") != audit["decks"][slug]["deck_sha256"]:
            errors.append(f"stale combo adjudication for changed deck: {slug}")
    missing = sorted(set(audit["decks"]) - covered)
    if missing:
        errors.append(f"decks without combo adjudication records: {', '.join(missing)}")
    return errors, warnings


def validate_social_report(audit: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    path = ROOT / "reports/manifest.json"
    if not path.exists():
        return ["missing social report manifest"], warnings
    manifest = json_load(path)
    report_path = ROOT / manifest["report_file"]
    if not report_path.exists() or sha256_file(report_path) != manifest["report_sha256"]:
        errors.append("social report changed without manifest update")
    changed = [
        slug
        for slug, deck in audit["decks"].items()
        if manifest.get("deck_sha256", {}).get(slug) != deck["deck_sha256"]
    ]
    if changed:
        warnings.append(
            "social report does not describe current deck hashes: "
            + ", ".join(changed)
        )
    return errors, warnings


def validate_current_sources(today: date) -> list[str]:
    errors: list[str] = []
    collection = json_load(ROOT / "collection.json")
    freshness = collection["freshness"]
    oracle_metadata = json_load(ROOT / "data/oracle-bulk-metadata.json")
    policy = json_load(ROOT / "policy/current.json")
    if age_days(oracle_metadata["updated_at"], today) > int(
        freshness["oracle_max_age_days"]
    ):
        errors.append(
            f"Oracle snapshot is older than {freshness['oracle_max_age_days']} days"
        )
    if age_days(policy["verified_on"], today) > int(freshness["policy_max_age_days"]):
        errors.append(
            f"official policy lock is older than {freshness['policy_max_age_days']} days"
        )
    return errors


def validate_request_hash_formula(audit: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for slug, deck in audit["decks"].items():
        request = json_load(ROOT / f"data/spellbook-requests/{slug}.json")
        actual = sha256_bytes(canonical_json_bytes(request))
        if actual != deck["spellbook_request_sha256"]:
            errors.append(f"Spellbook request provenance mismatch: {slug}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doctor", action="store_true")
    parser.add_argument("--require-current", action="store_true")
    args = parser.parse_args()
    errors, warnings = doctor()
    if not args.doctor and not errors:
        internal_errors, internal_warnings, audit = validate_internal_artifacts()
        errors.extend(internal_errors)
        warnings.extend(internal_warnings)
        if not internal_errors:
            spellbook_errors, spellbook_warnings = validate_spellbook(
                audit,
                require_current=args.require_current,
                today=date.today(),
            )
            errors.extend(spellbook_errors)
            warnings.extend(spellbook_warnings)
            adjudication_errors, adjudication_warnings = validate_adjudications(audit)
            errors.extend(adjudication_errors)
            warnings.extend(adjudication_warnings)
            report_errors, report_warnings = validate_social_report(audit)
            errors.extend(report_errors)
            warnings.extend(report_warnings)
            errors.extend(validate_request_hash_formula(audit))
            if args.require_current:
                errors.extend(validate_current_sources(date.today()))

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("SYSTEM CHECK FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    label = "doctor" if args.doctor else "current system" if args.require_current else "system"
    print(f"{label} check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
