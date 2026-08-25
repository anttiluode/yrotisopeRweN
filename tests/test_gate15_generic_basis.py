import unittest

from generic_recurrent_field import run_generic_basis_world


class Gate15GenericBasisTests(unittest.TestCase):
    def test_stable_dense_random_basis_supports_grown_recurrence(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000)
        self.assertGreater(r["late_hold_accuracy"], 0.99)
        self.assertLess(r["a_max_axis_loading"], 0.70)
        self.assertLess(r["b_max_axis_loading"], 0.70)

    def test_scrambling_internal_feature_addresses_kills_memory(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000, scramble_feature_addresses=True)
        self.assertLess(r["late_hold_accuracy"], 0.10)

    def test_shuffled_eligibility_still_kills_credit(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000, shuffle_eligibility=True)
        self.assertLess(r["late_hold_accuracy"], 0.10)

    def test_no_learning_still_fails(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000, learn=False)
        self.assertLess(r["late_hold_accuracy"], 0.10)

    def test_cut_return_after_growth_breaks_persistence(self):
        r = run_generic_basis_world(
            seed=0,
            n_steps=10_000,
            cut_returns_after=7000,
            freeze_after_cut=True,
        )
        self.assertLess(r["late_hold_accuracy"], 0.10)

    def test_linear_random_basis_is_already_sufficient(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000, nonlinear=False)
        self.assertGreater(r["late_hold_accuracy"], 0.99)

    def test_square_six_feature_basis_is_already_sufficient(self):
        r = run_generic_basis_world(seed=0, n_steps=10_000, n_features=6)
        self.assertGreater(r["late_hold_accuracy"], 0.99)


if __name__ == "__main__":
    unittest.main()
