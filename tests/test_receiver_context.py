import unittest
import numpy as np

from receiver_composition import nmse
from receiver_context import (
    CircularContextReceiver,
    ScalarContextReceiver,
    explicit_context_features,
    fit_ridge,
    make_context_world,
    make_distractors,
    paired_contrast_nmse,
    predict_ridge,
    stateless_bilinear_features,
)


class TestReceiverContext(unittest.TestCase):
    def test_same_broadcast_pair_appears_under_both_contexts(self):
        w = make_context_world(n_pairs=100, seed=0)
        self.assertTrue(np.allclose(w["A"][0::2], w["A"][1::2]))
        self.assertTrue(np.allclose(w["B"][0::2], w["B"][1::2]))
        self.assertTrue(np.all(w["context"][0::2] == 0.0))
        self.assertTrue(np.all(w["context"][1::2] == 1.0))

    def test_context_state_composes_without_current_mode(self):
        w = make_context_world(n_pairs=500, seed=1)
        real, imag = make_distractors(len(w["A"]), 0, seed=10)
        receiver = CircularContextReceiver()
        state = receiver.state_after(w["context"], real, imag)
        pred = receiver.compose(w["A"], w["B"], state)
        self.assertLess(nmse(pred, w["target"]), 1e-12)

    def test_state_reset_destroys_context_contrast(self):
        w = make_context_world(n_pairs=500, seed=2)
        receiver = CircularContextReceiver()
        pred = receiver.compose(
            w["A"], w["B"], np.zeros(len(w["A"]), dtype=complex)
        )
        self.assertGreater(
            paired_contrast_nmse(pred, w["target"], w["pair_id"]), 0.95
        )

    def test_memory_degrades_under_gap_distractors(self):
        w = make_context_world(n_pairs=1500, seed=3)
        receiver = CircularContextReceiver()
        real8, imag8 = make_distractors(len(w["A"]), 8, seed=38)
        real64, imag64 = make_distractors(len(w["A"]), 64, seed=364)
        pred8 = receiver.compose(
            w["A"], w["B"], receiver.state_after(w["context"], real8, imag8)
        )
        pred64 = receiver.compose(
            w["A"], w["B"], receiver.state_after(w["context"], real64, imag64)
        )
        self.assertLess(nmse(pred8, w["target"]), 0.05)
        self.assertGreater(nmse(pred64, w["target"]), 0.55)

    def test_scalar_recurrent_attacker_is_enough(self):
        w = make_context_world(n_pairs=1500, seed=4)
        real, imag = make_distractors(len(w["A"]), 16, seed=416)
        circular = CircularContextReceiver()
        scalar = ScalarContextReceiver()
        circular_pred = circular.compose(
            w["A"], w["B"], circular.state_after(w["context"], real, imag)
        )
        scalar_pred = scalar.compose(
            w["A"], w["B"], scalar.state_after(w["context"], real)
        )
        self.assertLess(nmse(scalar_pred, w["target"]), 0.20)
        self.assertLess(
            abs(nmse(scalar_pred, w["target"]) - nmse(circular_pred, w["target"])),
            0.08,
        )

    def test_explicit_context_buffer_is_perfect_attacker(self):
        w = make_context_world(n_pairs=2000, seed=5)
        train = w["pair_id"] < 1200
        test = ~train
        features = explicit_context_features(w["A"], w["B"], w["context"])
        coef = fit_ridge(features[train], w["target"][train])
        pred = predict_ridge(features[test], coef)
        self.assertLess(nmse(pred, w["target"][test]), 1e-10)

    def test_stateless_bilinear_must_compromise(self):
        w = make_context_world(n_pairs=2000, seed=6)
        train = w["pair_id"] < 1200
        test = ~train
        features = stateless_bilinear_features(w["A"], w["B"])
        coef = fit_ridge(features[train], w["target"][train])
        pred = predict_ridge(features[test], coef)
        self.assertGreater(nmse(pred, w["target"][test]), 0.40)


if __name__ == "__main__":
    unittest.main()
