"""Self-wiring phase graph used by Gate 1.

Fast phase-compatible traffic can slowly alter two edge properties:
structural mass (under a fixed outgoing budget) and propagation delay/length.
This is a computational developmental toy, not a biological axon model.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray
TAU = 2.0 * np.pi


def phase_gate(relative_phase: Array | float, sharpness: float = 3.0) -> Array:
    base = 0.5 * (1.0 + np.cos(relative_phase))
    return np.clip(base, 0.0, 1.0) ** float(sharpness)


def _positive_correlation(a: Array, b: Array) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a - a.mean()
    b = b - b.mean()
    den = np.linalg.norm(a) * np.linalg.norm(b)
    if den < 1e-12:
        return 0.0
    return max(float(a @ b / den), 0.0)


def delayed_compatibility(sender: Array, receiver_gate: Array, delay: int) -> float:
    """Positive centered coincidence after a propagation delay.

    Repeated sender events that arrive during high receiver excitability give
    positive support; anti-phase or unrelated timing gives no growth signal.
    A constant/dead receiver has zero score.
    """
    d = int(delay)
    if d < 0:
        raise ValueError("delay must be nonnegative")
    x = np.asarray(sender, dtype=float)
    g = np.asarray(receiver_gate, dtype=float)
    if x.shape != g.shape or x.ndim != 1:
        raise ValueError("sender and receiver_gate must be matching 1-D arrays")
    if d >= len(x) - 2:
        return 0.0
    if d == 0:
        return _positive_correlation(x, g)
    return _positive_correlation(x[:-d], g[d:])


def periodic_event_train(
    n: int,
    period: float,
    phase_offset: float = 0.0,
    sharpness: float = 8.0,
    cycle_jitter: float = 0.08,
    amplitude_jitter: float = 0.25,
    seed: int = 0,
) -> Array:
    """Noisy repeated sender events with a stable underlying period."""
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=float)
    cycle = np.floor(t / period).astype(int)
    n_cycles = int(cycle.max()) + 2
    jitter = rng.normal(scale=cycle_jitter, size=n_cycles)
    amplitude = np.exp(amplitude_jitter * rng.normal(size=n_cycles))
    phase = TAU * t / period + phase_offset - jitter[cycle]
    return amplitude[cycle] * phase_gate(phase, sharpness)


def periodic_receiver_gate(
    n: int,
    period: float | None,
    phase_offset: float = 0.0,
    sharpness: float = 5.0,
    scramble_each_cycle: bool = False,
    seed: int = 0,
) -> Array:
    """Receiver excitability cycle; period=None is a non-oscillating control."""
    if period is None:
        return np.full(n, 0.5, dtype=float)
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=float)
    phase = TAU * t / period + phase_offset
    if scramble_each_cycle:
        cycle = np.floor(t / period).astype(int)
        random_offset = rng.uniform(-np.pi, np.pi, size=int(cycle.max()) + 2)
        phase = phase + random_offset[cycle]
    return phase_gate(phase, sharpness)


def self_wiring_world(n: int = 14_000, seed: int = 0, destroy_coherence: bool = False) -> dict:
    """Three sender clocks, three matching receivers, two distractors, one dead point."""
    sender_periods = np.array([17.0, 23.0, 31.0])
    receiver_periods: tuple[float | None, ...] = (31.0, 17.0, 27.0, 23.0, 41.0, None)
    receiver_offsets = (0.7, -1.2, 0.1, 2.0, -0.4, 0.0)
    match = np.array([1, 3, 0], dtype=int)

    senders = np.column_stack([
        periodic_event_train(n, p, seed=seed * 11 + i)
        for i, p in enumerate(sender_periods)
    ])
    receivers = np.column_stack([
        periodic_receiver_gate(
            n,
            p,
            phase_offset=o,
            scramble_each_cycle=destroy_coherence and p is not None,
            seed=seed * 29 + j,
        )
        for j, (p, o) in enumerate(zip(receiver_periods, receiver_offsets))
    ])
    return {
        "sender_events": senders,
        "receiver_gates": receivers,
        "sender_periods": sender_periods,
        "receiver_periods": receiver_periods,
        "matching_receivers": match,
    }


@dataclass
class SelfWiringPhaseGraph:
    """Candidate edges compete for mass while exploratory delay changes are tested.

    Each sender has a fixed outgoing mass budget of 1. `mass[i,j]` is the slow
    structural commitment to receiver j. `delay[i,j]` is an integer stand-in for
    propagation length. Weak exploratory delay changes are retained only when
    locally measured phase compatibility improves.
    """

    n_senders: int
    n_receivers: int
    max_delay: int = 50
    mass_learning_rate: float = 0.15
    mass_beta: float = 12.0
    explore_probability: float = 0.20
    local_growth_span: int = 6
    vitality_learning_rate: float = 0.10
    seed: int = 0

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.seed)
        self.delay = self.rng.integers(
            0, self.max_delay + 1, size=(self.n_senders, self.n_receivers)
        )
        self.mass = np.full(
            (self.n_senders, self.n_receivers), 1.0 / self.n_receivers
        )
        self.vitality = np.ones(self.n_receivers, dtype=float)

    def _scores(self, sender_events: Array, receiver_gates: Array) -> Array:
        scores = np.zeros((self.n_senders, self.n_receivers), dtype=float)
        for i in range(self.n_senders):
            for j in range(self.n_receivers):
                scores[i, j] = delayed_compatibility(
                    sender_events[:, i], receiver_gates[:, j], int(self.delay[i, j])
                )
        return scores

    def step(
        self,
        sender_events: Array,
        receiver_gates: Array,
        adapt_delay: bool = True,
        adapt_mass: bool = True,
    ) -> Array:
        E = np.asarray(sender_events, dtype=float)
        G = np.asarray(receiver_gates, dtype=float)
        if E.ndim != 2 or G.ndim != 2:
            raise ValueError("sender_events and receiver_gates must be 2-D")
        if (
            E.shape[0] != G.shape[0]
            or E.shape[1] != self.n_senders
            or G.shape[1] != self.n_receivers
        ):
            raise ValueError("window shape does not match graph")

        if adapt_delay:
            for i in range(self.n_senders):
                for j in range(self.n_receivers):
                    current_delay = int(self.delay[i, j])
                    current_score = delayed_compatibility(
                        E[:, i], G[:, j], current_delay
                    )
                    if self.rng.random() < self.explore_probability:
                        proposal = int(self.rng.integers(0, self.max_delay + 1))
                    else:
                        jump = int(
                            self.rng.integers(
                                -self.local_growth_span, self.local_growth_span + 1
                            )
                        )
                        proposal = int(
                            np.clip(current_delay + jump, 0, self.max_delay)
                        )
                    proposal_score = delayed_compatibility(
                        E[:, i], G[:, j], proposal
                    )
                    if proposal_score > current_score + 1e-4:
                        self.delay[i, j] = proposal

        scores = self._scores(E, G)
        if adapt_mass:
            logits = self.mass_beta * scores
            logits -= logits.max(axis=1, keepdims=True)
            target = np.exp(logits)
            target /= target.sum(axis=1, keepdims=True) + 1e-12
            eta = self.mass_learning_rate
            self.mass = (1.0 - eta) * self.mass + eta * target
            self.mass /= self.mass.sum(axis=1, keepdims=True) + 1e-12

        support = (self.mass * scores).sum(axis=0)
        support_target = support / (support.max() + 1e-12)
        eta_v = self.vitality_learning_rate
        self.vitality = (
            (1.0 - eta_v) * self.vitality + eta_v * support_target
        )
        return scores

    def fit(
        self,
        sender_events: Array,
        receiver_gates: Array,
        epochs: int = 120,
        window: int = 2200,
        stride: int = 173,
        adapt_delay: bool = True,
        adapt_mass: bool = True,
    ) -> "SelfWiringPhaseGraph":
        E = np.asarray(sender_events, dtype=float)
        G = np.asarray(receiver_gates, dtype=float)
        if len(E) < window or len(G) < window:
            raise ValueError("training series shorter than window")
        span = len(E) - window
        for epoch in range(int(epochs)):
            start = (epoch * stride) % (span + 1)
            self.step(
                E[start:start + window],
                G[start:start + window],
                adapt_delay,
                adapt_mass,
            )
        return self

    def scores(self, sender_events: Array, receiver_gates: Array) -> Array:
        return self._scores(
            np.asarray(sender_events, dtype=float),
            np.asarray(receiver_gates, dtype=float),
        )

    def top_receivers(self) -> Array:
        return self.mass.argmax(axis=1)


def oracle_delay_matrix(
    sender_events: Array, receiver_gates: Array, max_delay: int = 50
) -> tuple[Array, Array]:
    """Boring digital attacker: exhaustively search every edge delay."""
    E = np.asarray(sender_events, dtype=float)
    G = np.asarray(receiver_gates, dtype=float)
    scores = np.zeros((E.shape[1], G.shape[1]), dtype=float)
    delays = np.zeros_like(scores, dtype=int)
    for i in range(E.shape[1]):
        for j in range(G.shape[1]):
            vals = [
                delayed_compatibility(E[:, i], G[:, j], d)
                for d in range(max_delay + 1)
            ]
            delays[i, j] = int(np.argmax(vals))
            scores[i, j] = float(np.max(vals))
    return scores, delays


def softmax_mass(scores: Array, beta: float = 12.0) -> Array:
    z = beta * np.asarray(scores, dtype=float)
    z -= z.max(axis=1, keepdims=True)
    mass = np.exp(z)
    return mass / (mass.sum(axis=1, keepdims=True) + 1e-12)


def wiring_metrics(
    mass: Array, scores: Array, matching_receivers: Array
) -> dict[str, float]:
    M = np.asarray(mass, dtype=float)
    S = np.asarray(scores, dtype=float)
    match = np.asarray(matching_receivers, dtype=int)
    top = M.argmax(axis=1)
    correct_mass = float(np.mean([M[i, match[i]] for i in range(len(match))]))
    top_score = float(np.mean([S[i, top[i]] for i in range(len(top))]))
    entropy = -np.sum(M * np.log(M + 1e-12), axis=1) / np.log(M.shape[1])
    return {
        "top1_accuracy": float(np.mean(top == match)),
        "correct_mass": correct_mass,
        "top_edge_score": top_score,
        "mass_entropy": float(entropy.mean()),
        "dead_receiver_mass": float(M[:, -1].mean()),
    }
