"""Transient receiver context for yrotisopeRweN Gate 7.

A context event happens, disappears, and leaves a temporary internal state.
Later identical broadcasts are composed according to that leftover state.
There is no mode input at composition time and no weight update anywhere.

The circular receiver is intentionally attacked by a one-scalar recurrent
state. If the scalar state ties or wins, the surviving primitive is receiver-
carried context rather than a special status for phase.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from receiver_composition import (
    conjunction_basis,
    phase_compose,
    scalar_mode_compose,
)

Array = np.ndarray


def make_context_world(n_pairs: int = 4000, seed: int = 0) -> dict[str, Array]:
    """Present each exact broadcast pair once after each possible old context."""
    rng = np.random.default_rng(seed)
    A0 = rng.normal(size=(n_pairs, 2))
    B0 = rng.normal(size=(n_pairs, 2))

    A = np.repeat(A0, 2, axis=0)
    B = np.repeat(B0, 2, axis=0)
    context = np.tile(np.array([0.0, 1.0]), n_pairs)
    target = scalar_mode_compose(A, B, context)
    pair_id = np.repeat(np.arange(n_pairs), 2)
    return {
        "A": A,
        "B": B,
        "context": context,
        "target": target,
        "pair_id": pair_id,
    }


def make_distractors(n: int, gap: int, seed: int) -> tuple[Array, Array]:
    """Unrelated events that perturb receiver state during the context gap."""
    rng = np.random.default_rng(seed)
    if gap <= 0:
        return np.zeros((0, n)), np.zeros((0, n))
    real = rng.normal(size=(gap, n)) / np.sqrt(2.0)
    imag = rng.normal(size=(gap, n)) / np.sqrt(2.0)
    return real, imag


@dataclass
class CircularContextReceiver:
    """A tiny two-component transient state whose direction stores context."""

    persistence: float = 0.93
    distractor_gain: float = 0.12

    def state_after(
        self,
        context: Array,
        distractor_real: Array,
        distractor_imag: Array,
    ) -> Array:
        mode = np.asarray(context, dtype=float)
        z = np.where(mode == 0.0, 1.0 + 0.0j, -1.0 + 0.0j)
        if (
            distractor_real.shape != distractor_imag.shape
            or distractor_real.ndim != 2
            or distractor_real.shape[1] != len(mode)
        ):
            raise ValueError("distractors must have shape (gap, n)")

        for real, imag in zip(distractor_real, distractor_imag):
            z = self.persistence * z + self.distractor_gain * (real + 1j * imag)
        return z

    def compose(self, A: Array, B: Array, state: Array) -> Array:
        """Compose from leftover state only; there is no current context input."""
        z = np.asarray(state, dtype=complex)
        mag = np.abs(z)
        signed = np.divide(
            z.real,
            mag,
            out=np.zeros_like(mag),
            where=mag > 1e-12,
        )
        theta = np.arccos(np.clip(signed, -1.0, 1.0))
        return phase_compose(A, B, theta)


@dataclass
class ScalarContextReceiver:
    """Boring one-number recurrent-state attacker."""

    persistence: float = 0.93
    distractor_gain: float = 0.12
    temperature: float = 0.20

    def state_after(self, context: Array, distractor_real: Array) -> Array:
        mode = np.asarray(context, dtype=float)
        h = np.where(mode == 0.0, 1.0, -1.0)
        if distractor_real.ndim != 2 or distractor_real.shape[1] != len(mode):
            raise ValueError("distractors must have shape (gap, n)")

        for real in distractor_real:
            h = self.persistence * h + self.distractor_gain * real
        return h

    def compose(self, A: Array, B: Array, state: Array) -> Array:
        signed = np.tanh(np.asarray(state, dtype=float) / self.temperature)
        mode = 0.5 * (1.0 - signed)
        return scalar_mode_compose(A, B, mode)


def stateless_bilinear_features(A: Array, B: Array) -> Array:
    """All Gate-6 conjunctions, but no memory of which relation is wanted."""
    return conjunction_basis(A, B)


def explicit_context_features(
    A: Array,
    B: Array,
    remembered_context: Array,
) -> Array:
    """Digital attacker: conjunctions plus an explicitly buffered old context bit."""
    q = conjunction_basis(A, B)
    mode = np.asarray(remembered_context, dtype=float)[:, None]
    return np.column_stack([q, mode * q])


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


def paired_contrast_nmse(
    prediction: Array,
    target: Array,
    pair_id: Array,
) -> float:
    """Error in the context-dependent difference for identical broadcast pairs."""
    pred = np.asarray(prediction, dtype=float)
    truth = np.asarray(target, dtype=float)
    pid = np.asarray(pair_id, dtype=int)
    if len(pred) % 2 or not np.all(pid[0::2] == pid[1::2]):
        raise ValueError("paired rows [context0, context1] are required")

    pred_delta = pred[0::2] - pred[1::2]
    truth_delta = truth[0::2] - truth[1::2]
    return float(
        np.mean((pred_delta - truth_delta) ** 2)
        / (np.var(truth_delta) + 1e-12)
    )
