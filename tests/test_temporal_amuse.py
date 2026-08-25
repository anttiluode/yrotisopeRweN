import unittest
import numpy as np

from population_oja import lag_only_world, pca_attacker, source_recovery
from temporal_amuse import fit_amuse, same_memory_world, shuffle_time


class TemporalAmuseTests(unittest.TestCase):
    def test_amuse_recovers_equal_variance_temporal_sources(self):
        world = lag_only_world(seed=0)
        cov = np.cov(world.train_x, rowvar=False, bias=True)
        self.assertLess(np.linalg.norm(cov - np.eye(4), ord="fro"), 1e-10)
        model = fit_amuse(world.train_x, lag=1)
        self.assertGreater(source_recovery(model.transform(world.test_x), world.test_sources), 0.999)

    def test_pca_cannot_use_the_lag_information(self):
        world = lag_only_world(seed=0)
        weights = pca_attacker(world.train_x)
        y = world.test_x @ weights.T
        self.assertLess(source_recovery(y, world.test_sources), 0.90)

    def test_time_shuffle_destroys_amuse_advantage(self):
        world = lag_only_world(seed=0)
        model = fit_amuse(shuffle_time(world.train_x, seed=9000), lag=1)
        self.assertLess(source_recovery(model.transform(world.test_x), world.test_sources), 0.90)

    def test_same_memory_law_removes_temporal_identity(self):
        world = same_memory_world(seed=0)
        model = fit_amuse(world.train_x, lag=1)
        self.assertLess(source_recovery(model.transform(world.test_x), world.test_sources), 0.90)


if __name__ == "__main__":
    unittest.main()
