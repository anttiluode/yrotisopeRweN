"""Minimal oscillating-point / relative-phase routing abstraction.

The static graph says which connections exist. A receiver oscillator makes their
instantaneous gain time-dependent:

    w_eff_j(t) = w_j * g(phi_global(t) - theta_j(t))

The incoming signal does not need to carry a phase tag. Arrival time relative to
the receiver oscillator is enough.  `CompetitivePhaseReceivers` is intentionally
simple: receiver phase offsets adapt toward energetic arrival phases while a
soft lateral competition prevents every receiver from chasing the same phase.

This is a computational toy, not a biological neuron model.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray
TAU = 2.0 * np.pi


def wrap_phase(x: Array | float) -> Array:
    return (np.asarray(x) + np.pi) % TAU - np.pi


def phase_gate(relative_phase: Array, sharpness: float = 3.0) -> Array:
    """Smooth nonnegative gate with 1 at alignment and 0 at anti-phase."""
    base = 0.5 * (1.0 + np.cos(relative_phase))
    return np.clip(base, 0.0, 1.0) ** float(sharpness)


def ar1(n: int, rho: float, rng: np.random.Generator) -> Array:
    x = np.empty(n, dtype=float)
    x[0] = rng.normal()
    scale = np.sqrt(max(1.0 - rho * rho, 1e-9))
    for i in range(1, n):
        x[i] = rho * x[i - 1] + scale * rng.normal()
    return x


def phase_locked_world(
    n_cycles: int = 700,
    steps_per_cycle: int = 64,
    preferred_phases: tuple[float, float] = (0.0, np.pi),
    source_kappa: float = 7.0,
    phase_jitter: float = 0.10,
    noise_std: float = 0.04,
    seed: int = 0,
) -> dict[str, Array]:
    """Two hidden processes emitted preferentially at different oscillator phases.

    Each cycle has one slowly varying signed amplitude per hidden process. The
    observer receives only their scalar sum plus noise and the global oscillator
    phase.
    """
    rng = np.random.default_rng(seed)
    n = n_cycles * steps_per_cycle
    t = np.arange(n)
    cycle = t // steps_per_cycle
    base_phase = TAU * (t % steps_per_cycle) / steps_per_cycle

    a0 = ar1(n_cycles, 0.96, rng)
    a1 = ar1(n_cycles, 0.91, rng)
    amps = (a0, a1)

    sources = []
    for amp, center in zip(amps, preferred_phases):
        jitter = rng.normal(scale=phase_jitter, size=n_cycles)
        dphi = wrap_phase(base_phase - (center + jitter[cycle]))
        env = np.exp(source_kappa * (np.cos(dphi) - 1.0))
        sources.append(amp[cycle] * env)

    S = np.column_stack(sources)
    mixture = S.sum(axis=1) + noise_std * rng.normal(size=n)
    return {"phase": base_phase, "sources": S, "mixture": mixture}


@dataclass
class CompetitivePhaseReceivers:
    """Bank of receiver oscillators with slow competitive phase plasticity."""

    n_receivers: int = 2
    assignment_kappa: float = 4.0
    gate_sharpness: float = 3.0
    learning_rate: float = 0.003
    seed: int = 0

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        self.theta = rng.uniform(-np.pi, np.pi, size=self.n_receivers)
        self.trace = np.exp(1j * self.theta)

    def fit(self, mixture: Array, phase: Array, passes: int = 4) -> "CompetitivePhaseReceivers":
        x = np.asarray(mixture, dtype=float)
        p = np.asarray(phase, dtype=float)
        if x.shape != p.shape:
            raise ValueError("mixture and phase must have matching 1-D shape")

        energy = x * x
        energy = np.minimum(energy / (np.quantile(energy, 0.98) + 1e-12), 1.0)
        unit_phase = np.exp(1j * p)

        for _ in range(int(passes)):
            scores = self.assignment_kappa * np.cos(p[:, None] - self.theta[None, :])
            scores -= scores.max(axis=1, keepdims=True)
            r = np.exp(scores)
            r /= r.sum(axis=1, keepdims=True) + 1e-12
            weighted = energy[:, None] * r
            new_trace = (weighted * unit_phase[:, None]).sum(axis=0)
            new_trace /= np.maximum(np.abs(new_trace), 1e-12)

            eta = min(max(self.learning_rate * len(x) / 100.0, 0.05), 0.75)
            self.trace = (1.0 - eta) * self.trace + eta * new_trace
            self.trace /= np.maximum(np.abs(self.trace), 1e-12)
            self.theta = np.angle(self.trace)
        return self

    def gates(self, phase: Array) -> Array:
        p = np.asarray(phase, dtype=float)[:, None]
        return phase_gate(p - self.theta[None, :], self.gate_sharpness)

    def transform(self, mixture: Array, phase: Array) -> Array:
        x = np.asarray(mixture, dtype=float)
        return self.gates(phase) * x[:, None]


def fixed_phase_receivers(
    mixture: Array,
    phase: Array,
    receiver_phases: Array | list[float],
    sharpness: float = 3.0,
) -> Array:
    theta = np.asarray(receiver_phases, dtype=float)
    g = phase_gate(np.asarray(phase)[:, None] - theta[None, :], sharpness)
    return np.asarray(mixture)[:, None] * g


def phase_feature_attacker(mixture: Array, phase: Array) -> Array:
    """Boring digital features that expose the same clock information directly."""
    x = np.asarray(mixture, dtype=float)
    p = np.asarray(phase, dtype=float)
    return np.column_stack([x, x * np.cos(p), x * np.sin(p)])


def fit_linear_multioutput(features: Array, targets: Array, ridge: float = 1e-6) -> Array:
    X = np.asarray(features, dtype=float)
    Y = np.asarray(targets, dtype=float)
    design = np.column_stack([np.ones(len(X)), X])
    reg = ridge * np.eye(design.shape[1])
    reg[0, 0] = 0.0
    return np.linalg.solve(design.T @ design + reg, design.T @ Y)


def predict_linear(features: Array, weights: Array) -> Array:
    X = np.asarray(features, dtype=float)
    return np.column_stack([np.ones(len(X)), X]) @ weights


def permutation_recovery(outputs: Array, sources: Array) -> float:
    """Best unique 2x2 assignment, mean absolute correlation."""
    Y = np.asarray(outputs, dtype=float)
    S = np.asarray(sources, dtype=float)
    if Y.shape[1] != 2 or S.shape[1] != 2:
        raise ValueError("metric currently expects exactly two outputs and two sources")
    corr = np.empty((2, 2), dtype=float)
    for i in range(2):
        for j in range(2):
            corr[i, j] = abs(np.corrcoef(Y[:, i], S[:, j])[0, 1])
    return float(max(corr[0, 0] + corr[1, 1], corr[0, 1] + corr[1, 0]) / 2.0)


def output_duplication(outputs: Array) -> float:
    Y = np.asarray(outputs, dtype=float)
    return float(abs(np.corrcoef(Y[:, 0], Y[:, 1])[0, 1]))
