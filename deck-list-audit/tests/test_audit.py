from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_decks import audit_deck, build_audit, normalize_name, read_deck  # noqa: E402


def card(
    name: str,
    *,
    oracle_id: str,
    type_line: str,
    identity: list[str] | None = None,
    oracle_text: str = "",
    legality: str = "legal",
    released_at: str = "2020-01-01",
    game_changer: bool = False,
    layout: str = "normal",
    keywords: list[str] | None = None,
    faces: list[dict] | None = None,
) -> dict:
    return {
        "id": f"printing-{oracle_id}",
        "oracle_id": oracle_id,
        "name": name,
        "type_line": type_line,
        "color_identity": identity or [],
        "oracle_text": oracle_text,
        "legalities": {"commander": legality},
        "released_at": released_at,
        "game_changer": game_changer,
        "layout": layout,
        "keywords": keywords or [],
        "card_faces": faces or [],
        "mana_cost": "",
        "cmc": 0,
    }


COMMANDER = card(
    "Test Commander",
    oracle_id="commander",
    type_line="Legendary Creature — Human",
    identity=["B"],
)
SWAMP = card(
    "Swamp",
    oracle_id="swamp",
    type_line="Basic Land — Swamp",
    identity=["B"],
)


class AuditTests(unittest.TestCase):
    def audit_text(
        self,
        text: str,
        *,
        extra_cards: list[dict] | None = None,
        metadata: dict | None = None,
        aliases: dict[str, str] | None = None,
    ) -> dict:
        all_cards = [COMMANDER, SWAMP, *(extra_cards or [])]
        oracle = {normalize_name(value["name"]): value for value in all_cards}
        normalized_aliases = {
            normalize_name(key): value for key, value in (aliases or {}).items()
        }
        default_metadata = {
            "title": "Test",
            "commanders": ["Test Commander"],
            "constraints": {
                "game_changer_max": 3,
                "rule_zero_cards": [],
                "locked_cards": [],
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.txt"
            path.write_text(text, encoding="utf-8")
            result, _ = audit_deck(
                "test",
                metadata or default_metadata,
                path,
                oracle,
                {},
                normalized_aliases,
                date(2026, 8, 29),
            )
        return result

    def test_split_lines_and_aliases_cannot_evade_singleton(self) -> None:
        unique = card(
            "Canonical Card",
            oracle_id="unique",
            type_line="Artifact",
            identity=["B"],
        )
        result = self.audit_text(
            "97 Swamp\n1 Canonical Card\n1 Flavor Alias\n1 Test Commander\n",
            extra_cards=[unique],
            aliases={"Flavor Alias": "Canonical Card"},
        )
        self.assertFalse(result["valid"])
        self.assertIn("singleton_violation", {error["code"] for error in result["errors"]})
        self.assertEqual(result["nonbasic_duplicates"][0]["quantity"], 2)

    def test_any_number_copy_exception_is_quantity_aware(self) -> None:
        rat = card(
            "Rat Colony",
            oracle_id="rat-colony",
            type_line="Creature — Rat",
            identity=["B"],
            oracle_text="A deck can have any number of cards named Rat Colony.",
        )
        result = self.audit_text(
            "73 Swamp\n26 Rat Colony\n1 Test Commander\n",
            extra_cards=[rat],
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["nonbasic_duplicates"], [])

    def test_future_reprint_is_not_an_unreleased_card_identity(self) -> None:
        reprint = card(
            "Already Legal Card",
            oracle_id="reprint",
            type_line="Artifact",
            identity=["B"],
            legality="legal",
            released_at="2026-11-01",
        )
        result = self.audit_text(
            "98 Swamp\n1 Already Legal Card\n1 Test Commander\n",
            extra_cards=[reprint],
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["unreleased"], [])
        self.assertEqual(result["selected_printing_future"][0]["name"], "Already Legal Card")

    def test_approved_preview_is_valid_but_explicit_rule_zero(self) -> None:
        preview = card(
            "Preview Card",
            oracle_id="preview",
            type_line="Artifact",
            identity=["B"],
            legality="not_legal",
            released_at="2026-11-01",
        )
        metadata = {
            "title": "Test",
            "commanders": ["Test Commander"],
            "constraints": {
                "game_changer_max": 3,
                "rule_zero_cards": ["Preview Card"],
                "locked_cards": [],
            },
        }
        result = self.audit_text(
            "98 Swamp\n1 Preview Card\n1 Test Commander\n",
            extra_cards=[preview],
            metadata=metadata,
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["rule_zero_cards"], ["Preview Card"])
        self.assertEqual(result["unreleased"][0]["name"], "Preview Card")

    def test_unapproved_illegal_card_fails(self) -> None:
        illegal = card(
            "Illegal Card",
            oracle_id="illegal",
            type_line="Artifact",
            identity=["B"],
            legality="banned",
        )
        result = self.audit_text(
            "98 Swamp\n1 Illegal Card\n1 Test Commander\n",
            extra_cards=[illegal],
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["banned_cards"], ["Illegal Card"])

    def test_off_identity_card_fails(self) -> None:
        blue = card(
            "Blue Card",
            oracle_id="blue",
            type_line="Instant",
            identity=["U"],
        )
        result = self.audit_text(
            "98 Swamp\n1 Blue Card\n1 Test Commander\n",
            extra_cards=[blue],
        )
        self.assertFalse(result["valid"])
        self.assertIn("color_identity_violation", {error["code"] for error in result["errors"]})

    def test_rule_zero_off_identity_card_is_explicit_and_valid(self) -> None:
        blue = card(
            "Blue Card",
            oracle_id="blue",
            type_line="Instant",
            identity=["U"],
        )
        metadata = {
            "title": "Test",
            "commanders": ["Test Commander"],
            "constraints": {
                "game_changer_max": 3,
                "rule_zero_cards": ["Blue Card"],
                "locked_cards": [],
            },
        }
        result = self.audit_text(
            "98 Swamp\n1 Blue Card\n1 Test Commander\n",
            extra_cards=[blue],
            metadata=metadata,
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["rule_zero_cards"], ["Blue Card"])
        self.assertEqual(result["identity_violations"][0]["name"], "Blue Card")

    def test_configured_game_changer_bracket_exception_is_explicit_and_valid(self) -> None:
        ring = card(
            "Bracket Exception",
            oracle_id="bracket-exception",
            type_line="Artifact",
            identity=["B"],
            game_changer=True,
        )
        metadata = {
            "title": "Test",
            "commanders": ["Test Commander"],
            "constraints": {
                "game_changer_max": 0,
                "bracket_exception_cards": ["Bracket Exception"],
                "rule_zero_cards": [],
                "locked_cards": [],
            },
        }
        result = self.audit_text(
            "98 Swamp\n1 Bracket Exception\n1 Test Commander\n",
            extra_cards=[ring],
            metadata=metadata,
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["game_changer_count"], 1)
        self.assertEqual(result["bracket_exception_cards"], ["Bracket Exception"])

    def test_background_pair_is_supported(self) -> None:
        leader = card(
            "Background Leader",
            oracle_id="leader",
            type_line="Legendary Creature — Human",
            identity=["B"],
            oracle_text="Choose a Background",
        )
        background = card(
            "Useful Background",
            oracle_id="background",
            type_line="Legendary Enchantment — Background",
            identity=["B"],
        )
        metadata = {
            "title": "Pair",
            "commanders": ["Background Leader", "Useful Background"],
            "constraints": {
                "game_changer_max": 3,
                "rule_zero_cards": [],
                "locked_cards": [],
            },
        }
        result = self.audit_text(
            "98 Swamp\n1 Background Leader\n1 Useful Background\n",
            extra_cards=[leader, background],
            metadata=metadata,
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["commander_quantity"], 2)

    def test_background_cannot_be_the_only_commander(self) -> None:
        background = card(
            "Useful Background",
            oracle_id="background",
            type_line="Legendary Enchantment — Background",
            identity=["B"],
        )
        metadata = {
            "title": "Invalid Background",
            "commanders": ["Useful Background"],
            "constraints": {
                "game_changer_max": 3,
                "rule_zero_cards": [],
                "locked_cards": [],
            },
        }
        result = self.audit_text(
            "99 Swamp\n1 Useful Background\n",
            extra_cards=[background],
            metadata=metadata,
        )
        self.assertFalse(result["valid"])
        self.assertIn(
            "invalid_commander_configuration",
            {error["code"] for error in result["errors"]},
        )

    def test_zero_quantity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text("0 Swamp\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "positive"):
                read_deck(path)

    def test_game_changer_limit_fails_closed(self) -> None:
        cards = [
            card(
                f"Game Changer {index}",
                oracle_id=f"gc-{index}",
                type_line="Artifact",
                identity=["B"],
                game_changer=True,
            )
            for index in range(4)
        ]
        result = self.audit_text(
            "95 Swamp\n"
            + "\n".join(f"1 Game Changer {index}" for index in range(4))
            + "\n1 Test Commander\n",
            extra_cards=cards,
        )
        self.assertFalse(result["valid"])
        self.assertIn("game_changer_limit_exceeded", {error["code"] for error in result["errors"]})


class CollectionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit, _ = build_audit(audit_date=date(2026, 8, 29))

    def test_all_current_decks_are_valid_and_resolved(self) -> None:
        self.assertTrue(self.audit["summary"]["valid"])
        for deck in self.audit["decks"].values():
            self.assertEqual(deck["total_cards"], 100)
            self.assertEqual(deck["resolved_cards"], 100)
            self.assertTrue(deck["valid"], deck["errors"])

    def test_only_four_card_identities_are_genuinely_unreleased(self) -> None:
        actual = {
            record["name"]
            for deck in self.audit["decks"].values()
            for record in deck["unreleased"]
        }
        self.assertEqual(
            actual,
            {
                "Blor the Impervious",
                "Darksteel Angel",
                "Maular, the Next Evolution",
                "The Theorist, Jace Beleren",
            },
        )


if __name__ == "__main__":
    unittest.main()
