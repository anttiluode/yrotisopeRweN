import unittest

from recurrent_loop import (
    run_recurrent_loop,
    run_scalar_recurrent_attacker,
)


class Gate12RecurrentLoopTests(unittest.TestCase):
    def test_full_loop_holds_and_overwrites(self):
        r = run_recurrent_loop(seed=0)
        self.assertGreater(r["hold1_a_accuracy"], 0.99)
        self.assertGreater(r["hold2_a_accuracy"], 0.99)
        self.assertGreater(r["hold1_b_accuracy"], 0.99)
        self.assertGreater(r["hold2_b_accuracy"], 0.99)

    def test_cut_return_destroys_persistent_state(self):
        r = run_recurrent_loop(seed=0, cut_return=True)
        self.assertLess(r["hold1_a_accuracy"], 0.05)
        self.assertLess(r["hold2_a_accuracy"], 0.05)

    def test_scrambled_return_timing_blocks_clean_overwrite(self):
        r = run_recurrent_loop(seed=0, scramble_return_timing=True)
        self.assertGreater(r["hold1_a_accuracy"], 0.90)
        self.assertLess(r["hold2_a_accuracy"], 0.20)

    def test_loop_gain_has_a_failure_boundary(self):
        r = run_recurrent_loop(seed=0, recurrent_gain_scale=0.10)
        self.assertLess(r["hold1_a_accuracy"], 0.20)
        self.assertLess(r["hold2_a_accuracy"], 0.20)

    def test_instantaneous_local_compartments_can_still_hold_state(self):
        r = run_recurrent_loop(seed=0, instantaneous_compartments=True)
        self.assertGreater(r["hold1_a_accuracy"], 0.99)
        self.assertGreater(r["hold2_a_accuracy"], 0.99)

    def test_scalar_recurrent_attacker_ties(self):
        r = run_scalar_recurrent_attacker(seed=0)
        self.assertGreater(r["hold1_accuracy"], 0.99)
        self.assertGreater(r["hold2_accuracy"], 0.99)


if __name__ == "__main__":
    unittest.main()
