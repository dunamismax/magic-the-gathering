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

    def test_all_combo_adjudications_match_current_decks(self) -> None:
        for deck in self.analysis["decks"].values():
            self.assertTrue(deck["combo_adjudication_current"])

    def test_confirmed_kang_combo_pieces_are_structured(self) -> None:
        kang = self.analysis["decks"]["kang-prime"]
        self.assertGreaterEqual(kang["role_counts"]["combo_piece"], 5)
        top = next(card for card in kang["cards"] if card["name"] == "Sensei's Divining Top")
        self.assertEqual(top["roles"]["combo_piece"], "confirmed-combo")

    def test_normal_lands_are_not_counted_as_ramp(self) -> None:
        for deck in self.analysis["decks"].values():
            for card in deck["cards"]:
                if "land" in card["roles"] and "ramp" in card["roles"]:
                    self.assertEqual(card["name"], "Ancient Tomb")

    def test_context_overrides_can_remove_false_positive_roles(self) -> None:
        minn = self.analysis["decks"]["minn-wily-illusionist"]
        oneirophage = next(
            card for card in minn["cards"] if card["name"] == "Oneirophage"
        )
        read_the_runes = next(
            card for card in minn["cards"] if card["name"] == "Read the Runes"
        )
        self.assertNotIn("card_advantage", oneirophage["roles"])
        self.assertNotIn("card_advantage", read_the_runes["roles"])
        self.assertEqual(read_the_runes["roles"]["selection"], "override")


if __name__ == "__main__":
    unittest.main()
