import unittest
import numpy as np

from oscillating_point import (
    CompetitivePhaseReceivers,
    phase_gate,
    phase_locked_world,
    permutation_recovery,
)


class OscillatingPointTests(unittest.TestCase):
    def test_phase_gate_alignment(self):
        self.assertAlmostEqual(float(phase_gate(0.0)), 1.0)
        self.assertAlmostEqual(float(phase_gate(np.pi)), 0.0, places=10)

    def test_world_shapes(self):
        w = phase_locked_world(n_cycles=10, steps_per_cycle=16, seed=1)
        self.assertEqual(w["sources"].shape, (160, 2))
        self.assertEqual(w["mixture"].shape, (160,))
        self.assertEqual(w["phase"].shape, (160,))

    def test_competitive_receivers_do_not_duplicate(self):
        w = phase_locked_world(n_cycles=200, seed=2)
        learner = CompetitivePhaseReceivers(seed=3).fit(w["mixture"], w["phase"], passes=4)
        y = learner.transform(w["mixture"], w["phase"])
        self.assertGreater(permutation_recovery(y, w["sources"]), 0.80)
        self.assertGreater(abs(np.angle(np.exp(1j * (learner.theta[0] - learner.theta[1])))), 2.0)


if __name__ == "__main__":
    unittest.main()
