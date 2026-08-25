import unittest
import numpy as np

from continuous_loop import (
    ContinuousGrowingCell,
    PHASE1_CELLS,
    branch_decay_field,
    pattern_mass,
    project_global_budget,
    sparse_pattern,
)


class TestContinuousLoop(unittest.TestCase):
    def test_global_budget_and_reserve(self):
        rng = np.random.default_rng(0)
        m = project_global_budget(rng.normal(size=36), reserve=0.001)
        self.assertAlmostEqual(float(m.sum()), 1.0, places=12)
        self.assertGreaterEqual(float(m.min()), 0.001 - 1e-12)

    def test_local_compartment_persists_without_new_drive(self):
        cell = ContinuousGrowingCell(branch_decays=np.full(36, 0.9))
        p = sparse_pattern(6, PHASE1_CELLS)
        cell.step(np.ones(6), np.ones(6), p, learn=False)
        before = cell.branch_state.copy()
        cell.step(np.zeros(6), np.zeros(6), p, learn=False)
        self.assertGreater(np.linalg.norm(cell.branch_state), 0.0)
        np.testing.assert_allclose(cell.branch_state, 0.9 * before, atol=1e-12)

    def test_output_does_not_reset_internal_state_by_default(self):
        cell = ContinuousGrowingCell(branch_decays=np.full(36, 0.9), spike_threshold=-1.0)
        p = sparse_pattern(6, PHASE1_CELLS)
        out = cell.step(np.ones(6), np.ones(6), p, learn=False)
        self.assertEqual(out["output_spike"], 1.0)
        self.assertGreater(np.linalg.norm(cell.branch_state), 0.0)

    def test_reset_on_output_is_an_explicit_ablation(self):
        cell = ContinuousGrowingCell(branch_decays=np.full(36, 0.9), spike_threshold=-1.0)
        p = sparse_pattern(6, PHASE1_CELLS)
        cell.step(np.ones(6), np.ones(6), p, learn=False, reset_on_output=True)
        self.assertLess(np.linalg.norm(cell.branch_state), 1e-12)

    def test_mass_measure(self):
        p = sparse_pattern(6, PHASE1_CELLS)
        m = np.full(36, 0.001)
        m[p > 0] = 0.2
        self.assertAlmostEqual(pattern_mass(m, p), 0.8, places=12)

    def test_decay_field_is_heterogeneous(self):
        a = branch_decay_field(6)
        self.assertEqual(a.shape, (36,))
        self.assertGreater(float(a.max() - a.min()), 0.25)


if __name__ == "__main__":
    unittest.main()
