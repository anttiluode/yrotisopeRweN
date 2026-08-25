import unittest
import numpy as np

from receiver_composition import (
    conjunction_basis,
    fit_ridge,
    make_paired_world,
    nmse,
    phase_compose,
    predict_ridge,
    scalar_mode_compose,
    square_conjunction,
    state_conditioned_linear_features,
)


class TestReceiverComposition(unittest.TestCase):
    def test_square_conjunction_is_product(self):
        rng = np.random.default_rng(0)
        a = rng.normal(size=100)
        b = rng.normal(size=100)
        self.assertLess(np.max(np.abs(square_conjunction(a, b) - a * b)), 1e-12)

    def test_phase_equals_scalar_switch_for_binary_states(self):
        w = make_paired_world(n_pairs=1000, seed=1)
        yp = phase_compose(w["A"], w["B"], w["theta"])
        ys = scalar_mode_compose(w["A"], w["B"], w["mode"])
        self.assertLess(np.max(np.abs(yp - ys)), 1e-12)
        self.assertLess(nmse(yp, w["target"]), 1e-12)

    def test_same_broadcasts_rebind_reversibly(self):
        w = make_paired_world(n_pairs=500, seed=2)
        A = w["A"][::2]
        B = w["B"][::2]
        y0 = phase_compose(A, B, np.zeros(len(A)))
        y1 = phase_compose(A, B, np.full(len(A), np.pi))
        y0_again = phase_compose(A, B, np.zeros(len(A)))
        self.assertGreater(np.mean(np.abs(y1 - y0)), 0.5)
        self.assertLess(np.max(np.abs(y0 - y0_again)), 1e-12)

    def test_static_bilinear_cannot_fit_both_modes(self):
        w = make_paired_world(n_pairs=3000, seed=3)
        q = conjunction_basis(w["A"], w["B"])
        train = w["pair_id"] < 1800
        test = ~train
        coef = fit_ridge(q[train], w["target"][train])
        pred = predict_ridge(q[test], coef)
        self.assertGreater(nmse(pred, w["target"][test]), 0.40)

    def test_state_without_nonlinear_conjunction_is_insufficient(self):
        w = make_paired_world(n_pairs=3000, seed=4)
        X = state_conditioned_linear_features(w["A"], w["B"], w["theta"])
        train = w["pair_id"] < 1800
        test = ~train
        coef = fit_ridge(X[train], w["target"][train])
        pred = predict_ridge(X[test], coef)
        self.assertGreater(nmse(pred, w["target"][test]), 0.90)


if __name__ == "__main__":
    unittest.main()
