import unittest

from anonymous_recurrent_loop import run_anonymous_return_world


class Gate14AnonymousReturnTests(unittest.TestCase):
    def test_stable_anonymous_channels_select_current_peer(self):
        r = run_anonymous_return_world(seed=0)
        self.assertGreater(r["late_hold_accuracy"], 0.99)
        self.assertGreater(r["a_useful_return_mass"], 0.35)
        self.assertGreater(r["b_useful_return_mass"], 0.90)
        self.assertLess(r["a_best_other_return_mass"], 0.01)

    def test_dynamic_channel_identity_destroys_memory(self):
        r = run_anonymous_return_world(seed=0, dynamic_channel_shuffle=True)
        self.assertLess(r["late_hold_accuracy"], 0.20)
        self.assertLess(r["closed_loop_mass"], 0.05)

    def test_shuffled_eligibility_destroys_selection(self):
        r = run_anonymous_return_world(seed=0, shuffle_eligibility=True)
        self.assertLess(r["late_hold_accuracy"], 0.10)
        self.assertLess(r["closed_loop_mass"], 0.10)

    def test_no_memory_world_does_not_close_loop(self):
        r = run_anonymous_return_world(seed=0, memory_required=False)
        self.assertGreater(r["a_direct_cue_mass"], 0.70)
        self.assertLess(r["closed_loop_mass"], 0.05)

    def test_cut_after_growth_breaks_persistence(self):
        r = run_anonymous_return_world(seed=0, cut_useful_return_after=12_000)
        self.assertLess(r["late_hold_accuracy"], 0.20)


if __name__ == "__main__":
    unittest.main()
