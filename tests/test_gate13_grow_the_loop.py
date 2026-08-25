import unittest

from growing_recurrent_loop import run_growing_recurrent_world


class Gate13GrowTheLoopTests(unittest.TestCase):
    def test_memory_task_grows_closed_loop(self):
        r = run_growing_recurrent_world(seed=0)
        self.assertGreater(r["late_hold_accuracy"], 0.99)
        self.assertGreater(r["a_return_mass"], 0.35)
        self.assertGreater(r["b_forward_mass"], 0.90)
        self.assertGreater(r["closed_loop_mass"], 0.35)

    def test_no_learning_does_not_hold_state(self):
        r = run_growing_recurrent_world(seed=0, learn=False)
        self.assertLess(r["late_hold_accuracy"], 0.10)
        self.assertLess(r["closed_loop_mass"], 0.05)

    def test_shuffled_eligibility_does_not_grow_loop(self):
        r = run_growing_recurrent_world(seed=0, shuffle_eligibility=True)
        self.assertLess(r["late_hold_accuracy"], 0.10)
        self.assertLess(r["closed_loop_mass"], 0.10)

    def test_no_memory_world_grows_direct_cue_not_return(self):
        r = run_growing_recurrent_world(seed=0, memory_required=False)
        self.assertGreater(r["a_cue_mass"], 0.80)
        self.assertLess(r["a_return_mass"], 0.01)
        self.assertLess(r["closed_loop_mass"], 0.01)


if __name__ == "__main__":
    unittest.main()
