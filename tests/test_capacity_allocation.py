import unittest

from capacity_allocation import (
    ConservedGrowthAllocator,
    PHASE1_PATTERN,
    PHASE2_PATTERN,
    SignedProjectedAttacker,
    UnlimitedPositiveGrowth,
    make_allocation_world,
    nmse,
    useful_mass,
)


class TestCapacityAllocation(unittest.TestCase):
    def test_finite_growth_allocates_to_useful_relations(self):
        w = make_allocation_world(n_trials=5000, seed=0)
        model = ConservedGrowthAllocator(reserve=0.02, seed=0).develop(
            w["features"], w["target1"]
        )
        self.assertGreater(useful_mass(model.mass, PHASE1_PATTERN), 0.95)
        self.assertLess(
            nmse(model.predict(w["features"]), w["target1"]),
            0.01,
        )

    def test_exploratory_reserve_allows_reversal(self):
        w = make_allocation_world(n_trials=5000, seed=1)
        model = ConservedGrowthAllocator(reserve=0.02, seed=1).develop(
            w["features"], w["target1"]
        ).hard_consolidate()
        model.develop(w["features"], w["target2"], epochs=120)
        self.assertGreater(useful_mass(model.mass, PHASE2_PATTERN), 0.95)
        self.assertLess(
            nmse(model.predict(w["features"]), w["target2"]),
            0.01,
        )

    def test_zero_reserve_hard_consolidation_freezes(self):
        w = make_allocation_world(n_trials=5000, seed=2)
        model = ConservedGrowthAllocator(reserve=0.0, seed=2).develop(
            w["features"], w["target1"]
        ).hard_consolidate()
        model.develop(w["features"], w["target2"], epochs=120)
        self.assertLess(useful_mass(model.mass, PHASE2_PATTERN), 0.05)
        self.assertGreater(
            nmse(model.predict(w["features"]), w["target2"]),
            1.5,
        )

    def test_unlimited_positive_growth_accumulates_old_and_new(self):
        w = make_allocation_world(n_trials=5000, seed=3)
        model = UnlimitedPositiveGrowth().develop(
            w["features"], w["target1"]
        )
        model.develop(w["features"], w["target2"])
        self.assertGreater(
            nmse(model.predict(w["features"]), w["target2"]),
            0.80,
        )

    def test_signed_projected_attacker_reallocates_more_cleanly(self):
        w = make_allocation_world(n_trials=5000, seed=4)
        model = SignedProjectedAttacker().develop(
            w["features"], w["target1"]
        )
        model.develop(w["features"], w["target2"])
        self.assertLess(
            nmse(model.predict(w["features"]), w["target2"]),
            0.01,
        )

    def test_consequence_is_needed_for_allocation(self):
        w = make_allocation_world(n_trials=5000, seed=5)
        model = ConservedGrowthAllocator(reserve=0.02, seed=5).develop(
            w["features"],
            w["target1"],
            use_consequence=False,
        )
        self.assertGreater(
            nmse(model.predict(w["features"]), w["target1"]),
            0.10,
        )


if __name__ == "__main__":
    unittest.main()
