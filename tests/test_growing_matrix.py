import unittest
import numpy as np

from growing_matrix import (
    GrowingRelationMatrix,
    SignedGlobalAttacker,
    make_growing_matrix_world,
    nmse,
    pattern_mass,
    relation_basis,
)


class TestGrowingMatrix(unittest.TestCase):
    def test_relation_basis_is_full_pairwise_matrix(self):
        A = np.array([[2.0, 3.0]])
        B = np.array([[5.0, 7.0]])
        q = relation_basis(A, B)
        np.testing.assert_allclose(q, [[10.0, 14.0, 15.0, 21.0]])

    def test_global_budget_has_no_pairwise_families(self):
        w = make_growing_matrix_world(n_samples=1000, seed=0)
        g = GrowingRelationMatrix().develop(w["features"], w["target1"], epochs=5)
        self.assertAlmostEqual(float(g.mass.sum()), 1.0, places=12)
        self.assertEqual(g.matrix.shape, (6, 6))

    def test_global_growth_finds_sparse_useful_matrix(self):
        w = make_growing_matrix_world(seed=1)
        cut = 6000
        g = GrowingRelationMatrix(seed=1).develop(
            w["features"][:cut], w["target1"][:cut]
        )
        self.assertGreater(pattern_mass(g.mass, w["pattern1"]), 0.94)
        self.assertLess(
            nmse(g.predict(w["features"][cut:]), w["target1"][cut:]),
            0.005,
        )

    def test_reserve_allows_disjoint_matrix_to_regrow(self):
        w = make_growing_matrix_world(seed=2)
        cut = 6000
        X = w["features"][:cut]
        g = GrowingRelationMatrix(seed=2).develop(X, w["target1"][:cut])
        g.develop(X, w["target2"][:cut], epochs=40)
        self.assertGreater(pattern_mass(g.mass, w["pattern2"]), 0.90)
        self.assertLess(
            nmse(g.predict(w["features"][cut:]), w["target2"][cut:]),
            0.005,
        )

    def test_hard_pruned_zero_reserve_freezes_new_structure(self):
        w = make_growing_matrix_world(seed=3)
        cut = 6000
        X = w["features"][:cut]
        g = GrowingRelationMatrix(reserve=0.0, seed=3).develop(
            X, w["target1"][:cut]
        )
        g.hard_consolidate(threshold=0.01)
        g.develop(X, w["target2"][:cut], epochs=120)
        self.assertLess(pattern_mass(g.mass, w["pattern2"]), 1e-12)
        self.assertGreater(
            nmse(g.predict(w["features"][cut:]), w["target2"][cut:]),
            1.5,
        )

    def test_consequence_is_load_bearing(self):
        w = make_growing_matrix_world(seed=4)
        cut = 6000
        g = GrowingRelationMatrix(seed=4).develop(
            w["features"][:cut],
            w["target1"][:cut],
            use_consequence=False,
        )
        self.assertGreater(
            nmse(g.predict(w["features"][cut:]), w["target1"][cut:]),
            1.0,
        )

    def test_signed_attacker_is_allowed_to_win(self):
        w = make_growing_matrix_world(seed=5)
        cut = 6000
        attacker = SignedGlobalAttacker().develop(
            w["features"][:cut], w["target1"][:cut]
        )
        self.assertLess(
            nmse(attacker.predict(w["features"][cut:]), w["target1"][cut:]),
            1e-8,
        )


if __name__ == "__main__":
    unittest.main()
