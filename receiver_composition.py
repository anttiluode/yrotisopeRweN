"""Receiver-relative composition for yrotisopeRweN.

This module deliberately contains no learning, utility, mass, geometry, or
source-separation objective. It tests one primitive only:

    same broadcasts + same slow structure + different fast receiver state
    -> different nonlinear conjunction.

Two 2-D broadcasts A=(a0,a1) and B=(b0,b1) are available to four fixed local
conjunction subunits. Each subunit uses a square-law identity to expose one
bilinear cross-term:

    conjunction(a,b) = ((a+b)^2 - a^2 - b^2)/2 = a*b

The receiver has one fast circular state theta. At theta=0 it listens to the
"same-index" conjunctions a0*b0 and a1*b1. At theta=pi it listens to the
crossed conjunctions a0*b1 and a1*b0. Slow weights/topology never change.

This is not a biological neuron model. The phase coordinate is intentionally
attacked by an ordinary scalar mode switch; if they tie, phase has earned only
the role of an endogenous fast mode variable, not extra expressive power.
"""
from __future__ import annotations

import numpy as np

Array = np.ndarray
PI = np.pi


def phase_window(theta: Array | float, center: float) -> Array:
    """Cosine window: 1 at center, 0 at center+pi."""
    t = np.asarray(theta, dtype=float)
    return 0.5 * (1.0 + np.cos(t - float(center)))


def square_conjunction(a: Array, b: Array) -> Array:
    """Local square-law interaction with self terms removed; exactly a*b."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return 0.5 * ((a + b) ** 2 - a**2 - b**2)


def conjunction_basis(A: Array, B: Array) -> Array:
    """Four fixed local conjunctions [00, 01, 10, 11]."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 2 or B.ndim != 2 or A.shape != B.shape or A.shape[1] != 2:
        raise ValueError("A and B must have matching shape (n, 2)")
    return np.column_stack(
        [
            square_conjunction(A[:, 0], B[:, 0]),
            square_conjunction(A[:, 0], B[:, 1]),
            square_conjunction(A[:, 1], B[:, 0]),
            square_conjunction(A[:, 1], B[:, 1]),
        ]
    )


def same_relation(A: Array, B: Array) -> Array:
    q = conjunction_basis(A, B)
    return q[:, 0] + q[:, 3]


def crossed_relation(A: Array, B: Array) -> Array:
    q = conjunction_basis(A, B)
    return q[:, 1] + q[:, 2]


def phase_compose(A: Array, B: Array, theta: Array | float) -> Array:
    """Fixed structure; fast state selects which conjunction family is effective."""
    same = same_relation(A, B)
    crossed = crossed_relation(A, B)
    gs = phase_window(theta, 0.0)
    gc = phase_window(theta, PI)
    return gs * same + gc * crossed


def scalar_mode_compose(A: Array, B: Array, mode: Array | float) -> Array:
    """Boring attacker: ordinary scalar switch between the same fixed relations."""
    m = np.asarray(mode, dtype=float)
    return (1.0 - m) * same_relation(A, B) + m * crossed_relation(A, B)


def state_conditioned_linear_features(A: Array, B: Array, theta: Array) -> Array:
    """Same fast gates but no multiplicative A*B conjunctions."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    gs = phase_window(theta, 0.0)
    gc = phase_window(theta, PI)
    raw = np.column_stack([A, B])
    return np.column_stack([raw, gs[:, None] * raw, gc[:, None] * raw])


def make_paired_world(n_pairs: int = 6000, seed: int = 0) -> dict[str, Array]:
    """Each exact broadcast pair is evaluated in both receiver states."""
    rng = np.random.default_rng(seed)
    A0 = rng.normal(size=(n_pairs, 2))
    B0 = rng.normal(size=(n_pairs, 2))

    A = np.repeat(A0, 2, axis=0)
    B = np.repeat(B0, 2, axis=0)
    mode = np.tile(np.array([0.0, 1.0]), n_pairs)
    theta = mode * PI

    y_same = same_relation(A, B)
    y_cross = crossed_relation(A, B)
    target = np.where(mode == 0.0, y_same, y_cross)
    pair_id = np.repeat(np.arange(n_pairs), 2)
    return {
        "A": A,
        "B": B,
        "mode": mode,
        "theta": theta,
        "target": target,
        "pair_id": pair_id,
        "same": y_same,
        "crossed": y_cross,
    }


def fit_ridge(features: Array, target: Array, ridge: float = 1e-8) -> Array:
    X = np.asarray(features, dtype=float)
    y = np.asarray(target, dtype=float)
    D = np.column_stack([np.ones(len(X)), X])
    reg = ridge * np.eye(D.shape[1])
    reg[0, 0] = 0.0
    return np.linalg.solve(D.T @ D + reg, D.T @ y)


def predict_ridge(features: Array, weights: Array) -> Array:
    X = np.asarray(features, dtype=float)
    return np.column_stack([np.ones(len(X)), X]) @ np.asarray(weights, dtype=float)


def nmse(prediction: Array, target: Array) -> float:
    p = np.asarray(prediction, dtype=float)
    y = np.asarray(target, dtype=float)
    return float(np.mean((p - y) ** 2) / (np.var(y) + 1e-12))
