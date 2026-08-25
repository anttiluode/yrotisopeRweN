import unittest
import numpy as np

from oscillating_point import phase_locked_world, permutation_recovery
from oja_phase import (
    OjaPhaseAxis,
    PlainHebbPhaseAxis,
    nonlinear_phase_pair,
    phase_energy_features,
    signed_phase_pair,
)


class OjaPhaseTests(unittest.TestCase):
    def test_oja_stabilizes_norm_where_plain_hebb_explodes(self):
        w = phase_locked_world(n_cycles=250, seed=0)
        U = phase_energy_features(w["mixture"], w["phase"])
        hebb = PlainHebbPhaseAxis(seed=1).fit(U)
        oja = OjaPhaseAxis(seed=1).fit(U)
        self.assertGreater(hebb.max_norm, 1000.0)
        self.assertLess(abs(np.linalg.norm(oja.w) - 1.0), 0.02)

    def test_linear_opposite_phase_outputs_are_duplicates(self):
        w = phase_locked_world(n_cycles=200, seed=2)
        U = phase_energy_features(w["mixture"], w["phase"])
        oja = OjaPhaseAxis(seed=3).fit(U)
        y = signed_phase_pair(w["mixture"], w["phase"], oja.theta)
        self.assertGreater(abs(np.corrcoef(y[:, 0], y[:, 1])[0, 1]), 0.999)

    def test_nonlinearity_splits_opposite_phase_sources(self):
        w = phase_locked_world(n_cycles=300, seed=4)
        cut = int(0.6 * len(w["mixture"]))
        U = phase_energy_features(w["mixture"][:cut], w["phase"][:cut])
        oja = OjaPhaseAxis(seed=5).fit(U)
        y = nonlinear_phase_pair(w["mixture"][cut:], w["phase"][cut:], oja.theta)
        self.assertGreater(permutation_recovery(y, w["sources"][cut:]), 0.95)


if __name__ == "__main__":
    unittest.main()
