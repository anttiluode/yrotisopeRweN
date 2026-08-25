"""Oja/phase bridge for yrotisopeRweN Gate 3.

A fast phase coordinate can be written as a tiny 2-D subspace:

    u(t) = sqrt(e(t)) [cos(phi(t)), sin(phi(t))]

where e(t) is local arrival energy.  A unit vector w=[cos(theta),sin(theta)]
selects a preferred phase axis. Oja's rule rotates w toward the dominant
energy axis while preventing Hebbian norm explosion:

    dw = eta * y * (u - y w),  y = w^T u

Oja learns an AXIS, so theta and theta+pi are identical to the covariance.
A nonlinear/nonnegative receiver gate is therefore load-bearing if the system
must distinguish opposite phases rather than merely represent the axis.

This is a computational bridge, not a biological synapse model.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray
TAU = 2.0 * np.pi


def phase_energy_features(mixture: Array, phase: Array, clip_quantile: float = 0.98) -> Array:
    """Lift scalar arrival energy into in-phase/quadrature coordinates."""
    x = np.asarray(mixture, dtype=float)
    p = np.asarray(phase, dtype=float)
    if x.ndim != 1 or p.ndim != 1 or x.shape != p.shape:
        raise ValueError("mixture and phase must be matching 1-D arrays")
    e = x * x
    scale = np.quantile(e, clip_quantile) + 1e-12
    e = np.minimum(e / scale, 1.0)
    amp = np.sqrt(e)
    return amp[:, None] * np.column_stack([np.cos(p), np.sin(p)])


@dataclass
class OjaPhaseAxis:
    learning_rate: float = 0.01
    epochs: int = 2
    seed: int = 0

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        self.w = rng.normal(size=2)
        self.w /= np.linalg.norm(self.w) + 1e-12
        self.norm_history: list[float] = [float(np.linalg.norm(self.w))]

    def fit(self, features: Array) -> "OjaPhaseAxis":
        U = np.asarray(features, dtype=float)
        if U.ndim != 2 or U.shape[1] != 2:
            raise ValueError("features must have shape (time, 2)")
        for _ in range(int(self.epochs)):
            for u in U:
                y = float(self.w @ u)
                self.w += self.learning_rate * y * (u - y * self.w)
            self.norm_history.append(float(np.linalg.norm(self.w)))
        return self

    @property
    def theta(self) -> float:
        return float(np.arctan2(self.w[1], self.w[0]))


@dataclass
class PlainHebbPhaseAxis:
    """Unnormalised control: same Hebbian positive feedback without Oja decay."""

    learning_rate: float = 0.01
    seed: int = 0
    stop_norm: float = 1e6

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        self.w = rng.normal(size=2)
        self.w /= np.linalg.norm(self.w) + 1e-12
        self.max_norm = float(np.linalg.norm(self.w))
        self.diverged = False

    def fit(self, features: Array, epochs: int = 1) -> "PlainHebbPhaseAxis":
        U = np.asarray(features, dtype=float)
        for _ in range(int(epochs)):
            for u in U:
                y = float(self.w @ u)
                self.w += self.learning_rate * y * u
                n = float(np.linalg.norm(self.w))
                self.max_norm = max(self.max_norm, n)
                if not np.isfinite(n) or n >= self.stop_norm:
                    self.diverged = True
                    return self
        return self


def signed_phase_pair(mixture: Array, phase: Array, theta: float) -> Array:
    """Linear control. Opposite receiver axes are exact negatives (duplicates)."""
    x = np.asarray(mixture, dtype=float)
    p = np.asarray(phase, dtype=float)
    y = x * np.cos(p - float(theta))
    return np.column_stack([y, -y])


def nonlinear_phase_pair(
    mixture: Array,
    phase: Array,
    theta: float,
    sharpness: float = 3.0,
) -> Array:
    """Complementary nonnegative phase windows at theta and theta+pi."""
    x = np.asarray(mixture, dtype=float)
    p = np.asarray(phase, dtype=float)
    rel0 = p - float(theta)
    rel1 = p - (float(theta) + np.pi)
    g0 = np.clip(0.5 * (1.0 + np.cos(rel0)), 0.0, 1.0) ** float(sharpness)
    g1 = np.clip(0.5 * (1.0 + np.cos(rel1)), 0.0, 1.0) ** float(sharpness)
    return x[:, None] * np.column_stack([g0, g1])


def axis_alignment(theta: float, reference: float = 0.0) -> float:
    """Cosine-axis alignment, invariant to theta -> theta+pi."""
    return float(abs(np.cos(float(theta) - float(reference))))
