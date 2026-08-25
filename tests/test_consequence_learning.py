import unittest

from consequence_learning import (
    DelayedConsequenceLearner,
    TRUE_UTILITY_WEIGHTS,
    cosine_alignment,
    fit_ridge,
    make_consequence_world,
    nmse,
    predict_ridge,
)


class TestConsequenceLearning(unittest.TestCase):
    def test_world_uses_transient_state_not_current_context_for_features(self):
        w = make_consequence_world(n_trials=1000, context_gap=4, seed=0)
        self.assertEqual(w["features"].shape, (1000, 4))
        self.assertEqual(w["state"].shape, (1000,))

    def test_delayed_eligibility_learns_useful_conjunctions(self):
        w = make_consequence_world(n_trials=6000, context_gap=4, seed=1)
        learner = DelayedConsequenceLearner(seed=1).fit(
            w["features"][:4000],
            w["target"][:4000],
            consequence_delay=8,
        )
        pred = learner.predict(w["features"][4000:])
        self.assertLess(nmse(pred, w["target"][4000:]), 0.01)
        self.assertGreater(
            cosine_alignment(learner.weights, TRUE_UTILITY_WEIGHTS), 0.99
        )

    def test_no_eligibility_cannot_assign_delayed_credit(self):
        w = make_consequence_world(n_trials=5000, context_gap=4, seed=2)
        learner = DelayedConsequenceLearner(seed=2).fit(
            w["features"][:3500],
            w["target"][:3500],
            consequence_delay=8,
            use_eligibility=False,
        )
        pred = learner.predict(w["features"][3500:])
        self.assertGreater(nmse(pred, w["target"][3500:]), 0.90)

    def test_shuffled_consequence_kills_learning(self):
        w = make_consequence_world(n_trials=5000, context_gap=4, seed=3)
        learner = DelayedConsequenceLearner(seed=3).fit(
            w["features"][:3500],
            w["target"][:3500],
            consequence_delay=8,
            shuffle_consequence=True,
        )
        pred = learner.predict(w["features"][3500:])
        self.assertGreater(nmse(pred, w["target"][3500:]), 0.80)

    def test_shuffled_eligibility_kills_credit_assignment(self):
        w = make_consequence_world(n_trials=5000, context_gap=4, seed=4)
        learner = DelayedConsequenceLearner(seed=4).fit(
            w["features"][:3500],
            w["target"][:3500],
            consequence_delay=8,
            shuffle_eligibility=True,
        )
        pred = learner.predict(w["features"][3500:])
        self.assertGreater(nmse(pred, w["target"][3500:]), 0.80)

    def test_explicit_context_buffer_is_digital_upper_bound(self):
        w = make_consequence_world(n_trials=5000, context_gap=4, seed=5)
        coef = fit_ridge(w["ideal_features"][:3500], w["target"][:3500])
        pred = predict_ridge(w["ideal_features"][3500:], coef)
        self.assertLess(nmse(pred, w["target"][3500:]), 1e-10)


if __name__ == "__main__":
    unittest.main()
