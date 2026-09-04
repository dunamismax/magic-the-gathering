from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from classify_roles import build_analysis  # noqa: E402


class RoleAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.analysis = build_analysis()

    def test_combo_reviews_match_every_current_deck_hash(self) -> None:
        for deck in self.analysis["decks"].values():
            self.assertTrue(deck["combo_adjudication_current"])
            self.assertEqual(deck["combo_adjudication_status"], "reviewed")

    def test_current_confirmed_combo_roles_are_scoped_to_working_lines(self) -> None:
        queen = self.analysis["decks"]["queen-marchesa"]
        queen_cards = {card["name"]: card for card in queen["cards"]}
        self.assertEqual(
            queen_cards["Arcbond"]["roles"].get("combo_piece"),
            "confirmed-combo",
        )
        henzie = self.analysis["decks"]["henzie-toolbox-torre"]
        seer = next(card for card in henzie["cards"] if card["name"] == "Viscera Seer")
        self.assertNotEqual(seer["roles"].get("combo_piece"), "confirmed-combo")

    def test_normal_lands_are_not_counted_as_ramp(self) -> None:
        for deck in self.analysis["decks"].values():
            for card in deck["cards"]:
                if "land" in card["roles"] and "ramp" in card["roles"]:
                    self.assertEqual(card["name"], "Ancient Tomb")

    def test_context_overrides_can_remove_false_positive_roles(self) -> None:
        blor = self.analysis["decks"]["blor-the-impervious"]
        pip_boy = next(
            card for card in blor["cards"] if card["name"] == "Pip-Boy 3000"
        )
        minn = self.analysis["decks"]["minn-wily-illusionist"]
        read_the_runes = next(
            card for card in minn["cards"] if card["name"] == "Read the Runes"
        )
        self.assertNotIn("card_advantage", pip_boy["roles"])
        self.assertNotIn("card_advantage", read_the_runes["roles"])
        self.assertEqual(read_the_runes["roles"]["selection"], "override")

if __name__ == "__main__":
    unittest.main()
