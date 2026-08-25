import unittest
import numpy as np

from population_oja import (
    IndependentOjaPopulation,
    SangerPopulation,
    distinct_source_claims,
    effective_rank,
    lag1_autocorrelations,
    lag_only_world,
    mean_weight_duplication,
    pca_attacker,
    rank1_world,
    source_recovery,
    variance_world,
)


class PopulationDifferentiationTests(unittest.TestCase):
    def test_independent_oja_points_collapse_to_one_mode(self):
        world = variance_world(seed=0)
        model = IndependentOjaPopulation(seed=1000).fit(world.train_x)
        y = model.transform(world.test_x)
        self.assertGreater(mean_weight_duplication(model.W), 0.99)
        self.assertEqual(distinct_source_claims(y, world.test_sources), 1)

    def test_sanger_between_point_term_differentiates(self):
        world = variance_world(seed=0)
        model = SangerPopulation(epochs=8, seed=2000).fit(world.train_x)
        y = model.transform(world.test_x)
        self.assertLess(mean_weight_duplication(model.W), 0.15)
        self.assertGreater(source_recovery(y, world.test_sources), 0.95)
        self.assertEqual(distinct_source_claims(y, world.test_sources), 4)

    def test_explicit_pca_remains_stronger_attacker(self):
        world = variance_world(seed=0)
        weights = pca_attacker(world.train_x)
        y = world.test_x @ weights.T
        self.assertGreater(source_recovery(y, world.test_sources), 0.99)

    def test_rank1_world_cannot_gain_information_rank(self):
        world = rank1_world(seed=0)
        model = SangerPopulation(seed=3000).fit(world.train_x)
        y = model.transform(world.test_x)
        self.assertAlmostEqual(effective_rank(y), 1.0, places=9)

    def test_lag_only_world_marks_the_zero_lag_boundary(self):
        world = lag_only_world(seed=0)
        model = SangerPopulation(seed=4000).fit(world.train_x)
        y = model.transform(world.test_x)
        self.assertGreater(np.ptp(lag1_autocorrelations(world.train_sources)), 1.0)
        self.assertLess(source_recovery(y, world.test_sources), 0.90)


if __name__ == "__main__":
    unittest.main()
