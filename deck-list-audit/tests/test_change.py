from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_change import apply_items, render_deck  # noqa: E402
from audit_decks import build_audit  # noqa: E402
from check_system import validate_spellbook  # noqa: E402


class ChangeTests(unittest.TestCase):
    def test_adds_and_cuts_preserve_quantities(self) -> None:
        entries = [
            {"quantity": 2, "name": "Swamp", "line_number": 1},
            {"quantity": 1, "name": "Old Card", "line_number": 2},
            {"quantity": 1, "name": "Commander", "line_number": 4},
        ]
        changed = apply_items(
            entries,
            [{"name": "New Card", "quantity": 1}],
            [{"name": "Old Card", "quantity": 1}],
        )
        rendered = render_deck(changed, ["Commander"]).decode("utf-8")
        self.assertIn("1 New Card\n", rendered)
        self.assertNotIn("Old Card", rendered)
        self.assertTrue(rendered.endswith("\n\n1 Commander\n"))

    def test_cut_must_exist_in_sufficient_quantity(self) -> None:
        entries = [{"quantity": 1, "name": "Only Copy", "line_number": 1}]
        with self.assertRaisesRegex(RuntimeError, "sufficient quantity"):
            apply_items(entries, [], [{"name": "Only Copy", "quantity": 2}])

    def test_spellbook_manifest_is_current_for_all_decks(self) -> None:
        audit, _ = build_audit(audit_date=date(2026, 9, 1))
        errors, warnings = validate_spellbook(
            audit, require_current=False, today=date(2026, 9, 1)
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

        current_errors, current_warnings = validate_spellbook(
            audit, require_current=True, today=date(2026, 9, 1)
        )
        self.assertEqual(current_errors, [])
        self.assertEqual(current_warnings, [])


if __name__ == "__main__":
    unittest.main()
