"""Delayed consequence / eligibility for yrotisopeRweN Gate 8.

Gate 7 established that earlier context can survive as a transient receiver state.
Gate 8 asks whether a later scalar consequence can assign credit back to the
nonlinear conjunctions that were active earlier.

There is no mass, geometry, structural growth, or source-separation objective.
The only slow variables are readout efficacies over fixed conjunction subunits.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from receiver_composition import conjunction_basis
from receiver_context import ScalarContextReceiver, make_distractors

Array = np.ndarray
TRUE_UTILITY_WEIGHTS = np.array([1.0, 0.0, 1.0, 0.0], dtype=float)


def contextual_conjunction_features(
    A: Array,
    B: Array,
    state: Array,
    temperature: float = 0.20,
) -> Array:
    """Gate Gate-6 conjunctions using receiver state, not a current context label."""
    q = conjunction_basis(A, B)
    signed = np.tanh(np.asarray(state, dtype=float) / float(temperature))
    same = 0.5 * (1.0 + signed)
    crossed = 0.5 * (1.0 - signed)
    gates = np.column_stack([same, crossed, crossed, same])
    return q * gates


def ideal_context_features(A: Array, B: Array, context: Array) -> Array:
    """Digital oracle features using the old context bit explicitly."""
    q = conjunction_basis(A, B)
    mode = np.asarray(context, dtype=float)
    same = 1.0 - mode
    crossed = mode
    return q * np.column_stack([same, crossed, crossed, same])


def make_consequence_world(
    n_trials: int = 12_000,
    context_gap: int = 4,
    seed: int = 0,
) -> dict[str, Array]:
    """Earlier context -> transient state -> later candidate conjunctions -> target."""
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n_trials, 2))
    B = rng.normal(size=(n_trials, 2))
    context = rng.integers(0, 2, size=n_trials).astype(float)

    receiver = ScalarContextReceiver()
    real, _ = make_distractors(n_trials, context_gap, seed=1000 + seed)
    state = receiver.state_after(context, real)
    features = contextual_conjunction_features(A, B, state, receiver.temperature)

    ideal = ideal_context_features(A, B, context)
    target = ideal @ TRUE_UTILITY_WEIGHTS
    return {
        "A": A,
        "B": B,
        "context": context,
        "state": state,
        "features": features,
        "ideal_features": ideal,
        "target": target,
        "true_weights": TRUE_UTILITY_WEIGHTS.copy(),
    }


def fit_ridge(features: Array, target: Array, ridge: float = 1e-8) -> Array:
    X = np.asarray(features, dtype=float)
    y = np.asarray(target, dtype=float)
    design = np.column_stack([np.ones(len(X)), X])
    reg = ridge * np.eye(design.shape[1])
    reg[0, 0] = 0.0
    return np.linalg.solve(design.T @ design + reg, design.T @ y)


def predict_ridge(features: Array, weights: Array) -> Array:
    X = np.asarray(features, dtype=float)
    return np.column_stack([np.ones(len(X)), X]) @ np.asarray(weights, dtype=float)


def nmse(prediction: Array, target: Array) -> float:
    pred = np.asarray(prediction, dtype=float)
    truth = np.asarray(target, dtype=float)
    return float(np.mean((pred - truth) ** 2) / (np.var(truth) + 1e-12))


def cosine_alignment(a: Array, b: Array) -> float:
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    return float((x @ y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))


@dataclass
class DelayedConsequenceLearner:
    """Slow efficacy learner; delayed error can update only through eligibility."""

    n_features: int = 4
    learning_rate: float = 0.01
    trace_decay: float = 0.85
    seed: int = 0

    def __post_init__(self) -> None:
        self.weights = np.zeros(self.n_features, dtype=float)
        self.rng = np.random.default_rng(self.seed)

    def fit(
        self,
        features: Array,
        target: Array,
        consequence_delay: int = 8,
        epochs: int = 1,
        use_eligibility: bool = True,
        shuffle_consequence: bool = False,
        shuffle_eligibility: bool = False,
    ) -> "DelayedConsequenceLearner":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.n_features or len(X) != len(y):
            raise ValueError("features and target have incompatible shapes")

        delay = int(consequence_delay)
        if delay < 0:
            raise ValueError("consequence_delay must be nonnegative")
        trace_scale = self.trace_decay**delay

        for _ in range(int(epochs)):
            order = self.rng.permutation(len(X))
            consequence_perm = (
                self.rng.permutation(len(X)) if shuffle_consequence else None
            )
            eligibility_perm = (
                self.rng.permutation(len(X)) if shuffle_eligibility else None
            )

            for step, index in enumerate(order):
                feature = X[index]
                prediction = float(self.weights @ feature)
                truth_index = consequence_perm[step] if shuffle_consequence else index
                error = float(y[truth_index] - prediction)

                if use_eligibility:
                    eligibility_index = (
                        eligibility_perm[step] if shuffle_eligibility else index
                    )
                    eligibility = trace_scale * X[eligibility_index]
                else:
                    eligibility = np.zeros(self.n_features, dtype=float)

                # At consequence time the original feature is conceptually gone.
                # The slow update gets only the delayed scalar error and the trace.
                self.weights += self.learning_rate * error * eligibility
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.weights
