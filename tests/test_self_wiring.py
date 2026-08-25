import unittest
import numpy as np

from self_wiring import (
    SelfWiringPhaseGraph,
    delayed_compatibility,
    periodic_event_train,
    periodic_receiver_gate,
    self_wiring_world,
    wiring_metrics,
)


class SelfWiringTests(unittest.TestCase):
    def test_matching_clock_beats_wrong_clock_after_delay_search(self):
        n = 5000
        s = periodic_event_train(n, 17.0, seed=1)
        good = periodic_receiver_gate(n, 17.0, phase_offset=1.0)
        bad = periodic_receiver_gate(n, 23.0, phase_offset=1.0)
        good_best = max(delayed_compatibility(s, good, d) for d in range(35))
        bad_best = max(delayed_compatibility(s, bad, d) for d in range(35))
        self.assertGreater(good_best, 0.85)
        self.assertLess(bad_best, 0.05)

    def test_nonoscillating_receiver_has_no_phase_compatibility(self):
        s = periodic_event_train(2000, 17.0, seed=2)
        dead = periodic_receiver_gate(2000, None)
        self.assertAlmostEqual(delayed_compatibility(s, dead, 5), 0.0)

    def test_mass_budget_is_conserved(self):
        w = self_wiring_world(n=5000, seed=3)
        g = SelfWiringPhaseGraph(3, 6, seed=4)
        g.fit(
            w["sender_events"][:4000],
            w["receiver_gates"][:4000],
            epochs=10,
            window=1000,
        )
        np.testing.assert_allclose(g.mass.sum(axis=1), 1.0, atol=1e-9)

    def test_full_self_wiring_finds_matching_receivers(self):
        w = self_wiring_world(seed=0)
        split = 9000
        g = SelfWiringPhaseGraph(3, 6, seed=0)
        g.fit(w["sender_events"][:split], w["receiver_gates"][:split])
        score = g.scores(
            w["sender_events"][split:], w["receiver_gates"][split:]
        )
        metrics = wiring_metrics(g.mass, score, w["matching_receivers"])
        self.assertEqual(metrics["top1_accuracy"], 1.0)
        self.assertGreater(metrics["correct_mass"], 0.95)
        self.assertLess(metrics["dead_receiver_mass"], 0.01)


if __name__ == "__main__":
    unittest.main()
