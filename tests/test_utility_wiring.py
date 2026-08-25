import unittest
import numpy as np

from utility_wiring import UtilityGuidedGraph, utility_wiring_world, task_metrics


class UtilityWiringTests(unittest.TestCase):
    def test_twin_receivers_are_phase_identical(self):
        w = utility_wiring_world(n=2000, seed=1)
        G = w['receiver_gates']
        self.assertTrue(np.allclose(G[:, 0], G[:, 1]))
        self.assertTrue(np.allclose(G[:, 2], G[:, 3]))
        self.assertTrue(np.allclose(G[:, 4], G[:, 5]))

    def test_phase_only_cannot_choose_actuator_sign(self):
        w = utility_wiring_world(n=9000, seed=2)
        g = UtilityGuidedGraph(seed=2).fit(
            w['sender_events'], w['receiver_gates'], w['actuator_matrix'], w['target'],
            epochs=100, use_phase=True, use_utility=False,
        )
        useful = w['useful_receivers']
        useful_mass = np.mean([g.mass[i, useful[i]] for i in range(3)])
        self.assertLess(useful_mass, 0.60)

    def test_utility_selects_useful_coherent_twin(self):
        w = utility_wiring_world(n=9000, seed=3)
        g = UtilityGuidedGraph(seed=3).fit(
            w['sender_events'], w['receiver_gates'], w['actuator_matrix'], w['target'],
            epochs=140, use_phase=True, use_utility=True,
        )
        pred = g.predict(w['sender_events'], w['receiver_gates'], w['actuator_matrix'])
        m = task_metrics(g.mass, w['useful_receivers'], pred, w['target'])
        self.assertEqual(m['top1_useful'], 1.0)
        self.assertGreater(m['useful_mass'], 0.90)
        self.assertGreater(m['mean_target_correlation'], 0.75)

    def test_unrelated_utility_does_not_harden_correct_twin(self):
        w = utility_wiring_world(n=9000, seed=4)
        g = UtilityGuidedGraph(seed=4).fit(
            w['sender_events'], w['receiver_gates'], w['actuator_matrix'], w['target'],
            epochs=140, use_phase=True, use_utility=True, independent_utility=True,
        )
        useful = w['useful_receivers']
        useful_mass = np.mean([g.mass[i, useful[i]] for i in range(3)])
        self.assertLess(useful_mass, 0.65)


if __name__ == '__main__':
    unittest.main()
