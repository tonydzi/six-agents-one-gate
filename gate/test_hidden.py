"""Held-out spec tests. Agents never see this file; the gate runs it on their fix."""
import unittest

from panel import decide


class TestHiddenSpec(unittest.TestCase):
    def test_order_independent(self):
        self.assertIsNone(decide(["C", None, "I"]))
        self.assertIsNone(decide(["I", None, "C"]))

    def test_two_of_three_wins(self):
        self.assertEqual(decide(["C", None, "C"]), "C")

    def test_failed_judge_stays_in_denominator(self):
        self.assertIsNone(decide(["C", None, None]))

    def test_three_way_split_has_no_verdict(self):
        self.assertIsNone(decide(["C", "I", "P"]))

    def test_plurality_is_not_majority(self):
        self.assertIsNone(decide(["C", "C", "I", "P"]))

    def test_empty_panel(self):
        self.assertIsNone(decide([]))
        self.assertIsNone(decide([None, None]))


if __name__ == "__main__":
    unittest.main()
