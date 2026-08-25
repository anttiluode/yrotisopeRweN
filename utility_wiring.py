"""Gate 2: phase-compatible edges compete under task utility.

Phase coherence answers "can this route communicate?". A downstream prediction
error answers "is this coherent route useful?". Structural mass is conserved per
sender, so useful coherent routes can consolidate while equally coherent but
behaviorally harmful twins lose mass.

Computational developmental toy; not a biological growth model.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray
TAU = 2.0 * np.pi


def phase_gate(relative_phase: Array | float, sharpness: float = 3.0) -> Array:
    base = 0.5 * (1.0 + np.cos(relative_phase))
    return np.clip(base, 0.0, 1.0) ** float(sharpness)


def ar1(n: int, rho: float, rng: np.random.Generator) -> Array:
    x = np.empty(n, dtype=float)
    x[0] = rng.normal()
    scale = np.sqrt(max(1.0 - rho * rho, 1e-12))
    for i in range(1, n):
        x[i] = rho * x[i - 1] + scale * rng.normal()
    return x


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
    """Compatibility of sender event magnitude with delayed receiver excitability."""
    x = np.asarray(sender, dtype=float)
    g = np.asarray(receiver_gate, dtype=float)
    d = int(delay)
    if x.ndim != 1 or g.ndim != 1 or x.shape != g.shape:
        raise ValueError("sender and receiver_gate must be matching 1-D arrays")
    if d < 0:
        raise ValueError("delay must be nonnegative")
    if d >= len(x) - 2:
        return 0.0
    if d == 0:
        return _positive_correlation(np.abs(x), g)
    return _positive_correlation(np.abs(x[:-d]), g[d:])


def edge_trace(sender: Array, receiver_gate: Array, delay: int) -> Array:
    """Signal arriving through one edge after propagation and receiver gating."""
    x = np.asarray(sender, dtype=float)
    g = np.asarray(receiver_gate, dtype=float)
    d = int(delay)
    out = np.zeros_like(x)
    if d == 0:
        out[:] = x * g
    elif d < len(x):
        out[d:] = x[:-d] * g[d:]
    return out


def receiver_gate(n: int, period: float | None, phase_offset: float, sharpness: float = 5.0) -> Array:
    if period is None:
        return np.full(n, 0.5, dtype=float)
    t = np.arange(n, dtype=float)
    return phase_gate(TAU * t / period + phase_offset, sharpness)


def utility_wiring_world(n: int = 14_000, seed: int = 0) -> dict:
    """Three senders; each has two equally coherent receivers but opposite actuator semantics."""
    rng = np.random.default_rng(seed)
    sender_periods = np.array([17.0, 23.0, 31.0])
    receiver_periods: tuple[float | None, ...] = (17.0, 17.0, 23.0, 23.0, 31.0, 31.0, None)
    pair_offsets = (0.7, 0.7, -1.1, -1.1, 1.5, 1.5, 0.0)

    t = np.arange(n, dtype=float)
    senders = []
    contents = []
    for i, period in enumerate(sender_periods):
        content = ar1(n, 0.999, np.random.default_rng(seed * 101 + i))
        carrier = phase_gate(TAU * t / period, 8.0)
        event = content * carrier + 0.005 * rng.normal(size=n)
        senders.append(event)
        contents.append(content)
    E = np.column_stack(senders)
    C = np.column_stack(contents)

    G = np.column_stack([
        receiver_gate(n, p, o)
        for p, o in zip(receiver_periods, pair_offsets)
    ])

    A = np.zeros((7, 3), dtype=float)
    A[0, 0] = +1.0
    A[1, 0] = -1.0
    A[2, 1] = -1.0
    A[3, 1] = +1.0
    A[4, 2] = +1.0
    A[5, 2] = -1.0
    useful_receivers = np.array([0, 3, 4], dtype=int)

    target = np.column_stack([
        C[:, 0] * G[:, 0],
        C[:, 1] * G[:, 3],
        C[:, 2] * G[:, 4],
    ])
    target = (target - target.mean(axis=0)) / (target.std(axis=0) + 1e-12)

    return {
        "sender_events": E,
        "receiver_gates": G,
        "actuator_matrix": A,
        "target": target,
        "sender_periods": sender_periods,
        "receiver_periods": receiver_periods,
        "useful_receivers": useful_receivers,
    }


def _softmax_rows(z: Array) -> Array:
    z = np.asarray(z, dtype=float)
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / (e.sum(axis=1, keepdims=True) + 1e-12)


@dataclass
class UtilityGuidedGraph:
    n_senders: int = 3
    n_receivers: int = 7
    max_delay: int = 50
    phase_weight: float = 6.0
    utility_weight: float = 8.0
    mass_learning_rate: float = 0.10
    explore_probability: float = 0.20
    local_growth_span: int = 6
    seed: int = 0

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.seed)
        self.delay = self.rng.integers(0, self.max_delay + 1, size=(self.n_senders, self.n_receivers))
        self.mass = np.full((self.n_senders, self.n_receivers), 1.0 / self.n_receivers)

    def _phase_scores(self, E: Array, G: Array) -> Array:
        return np.array([
            [delayed_compatibility(E[:, i], G[:, j], int(self.delay[i, j])) for j in range(self.n_receivers)]
            for i in range(self.n_senders)
        ])

    def _traces(self, E: Array, G: Array) -> Array:
        Q = np.zeros((len(E), self.n_senders, self.n_receivers), dtype=float)
        for i in range(self.n_senders):
            for j in range(self.n_receivers):
                Q[:, i, j] = edge_trace(E[:, i], G[:, j], int(self.delay[i, j]))
        return Q

    def _prediction(self, Q: Array, actuator_matrix: Array) -> Array:
        return np.einsum("tij,ij,jk->tk", Q, self.mass, actuator_matrix)

    def fit(
        self,
        sender_events: Array,
        receiver_gates: Array,
        actuator_matrix: Array,
        target: Array,
        epochs: int = 180,
        window: int = 2200,
        stride: int = 173,
        use_phase: bool = True,
        use_utility: bool = True,
        independent_utility: bool = False,
        adapt_delay: bool = True,
    ) -> "UtilityGuidedGraph":
        E = np.asarray(sender_events, dtype=float)
        G = np.asarray(receiver_gates, dtype=float)
        A = np.asarray(actuator_matrix, dtype=float)
        T = np.asarray(target, dtype=float)
        if E.shape[0] != G.shape[0] or E.shape[0] != T.shape[0]:
            raise ValueError("all time series must have the same length")
        if len(E) < window:
            raise ValueError("training series shorter than window")

        if independent_utility:
            noise_rng = np.random.default_rng(10_000 + self.seed)
            T_used = noise_rng.normal(size=T.shape)
        else:
            T_used = T

        span = len(E) - window
        for epoch in range(int(epochs)):
            start = (epoch * stride) % (span + 1)
            stop = start + window
            Ew, Gw, Tw = E[start:stop], G[start:stop], T_used[start:stop]

            if adapt_delay:
                for i in range(self.n_senders):
                    for j in range(self.n_receivers):
                        current = int(self.delay[i, j])
                        current_score = delayed_compatibility(Ew[:, i], Gw[:, j], current)
                        if self.rng.random() < self.explore_probability:
                            proposal = int(self.rng.integers(0, self.max_delay + 1))
                        else:
                            proposal = int(np.clip(
                                current + self.rng.integers(-self.local_growth_span, self.local_growth_span + 1),
                                0,
                                self.max_delay,
                            ))
                        proposal_score = delayed_compatibility(Ew[:, i], Gw[:, j], proposal)
                        if proposal_score > current_score + 1e-4:
                            self.delay[i, j] = proposal

            phase_score = self._phase_scores(Ew, Gw)
            Q = self._traces(Ew, Gw)
            prediction = self._prediction(Q, A)
            residual = Tw - prediction

            utility = np.zeros_like(self.mass)
            for i in range(self.n_senders):
                for j in range(self.n_receivers):
                    projected_error = residual @ A[j]
                    q = Q[:, i, j]
                    den = np.sqrt(np.mean(q * q)) * np.sqrt(np.mean(projected_error * projected_error))
                    utility[i, j] = 0.0 if den < 1e-12 else float(np.mean(q * projected_error) / den)

            score = np.zeros_like(self.mass)
            if use_phase:
                score += self.phase_weight * phase_score
            if use_utility:
                score += self.utility_weight * utility
            target_mass = _softmax_rows(score)
            eta = self.mass_learning_rate
            self.mass = (1.0 - eta) * self.mass + eta * target_mass
            self.mass /= self.mass.sum(axis=1, keepdims=True) + 1e-12
        return self

    def predict(self, sender_events: Array, receiver_gates: Array, actuator_matrix: Array) -> Array:
        E = np.asarray(sender_events, dtype=float)
        G = np.asarray(receiver_gates, dtype=float)
        return self._prediction(self._traces(E, G), np.asarray(actuator_matrix, dtype=float))

    def phase_scores(self, sender_events: Array, receiver_gates: Array) -> Array:
        return self._phase_scores(np.asarray(sender_events, dtype=float), np.asarray(receiver_gates, dtype=float))


def task_metrics(mass: Array, useful_receivers: Array, prediction: Array, target: Array) -> dict[str, float]:
    M = np.asarray(mass, dtype=float)
    useful = np.asarray(useful_receivers, dtype=int)
    top = M.argmax(axis=1)
    corrs = []
    for k in range(target.shape[1]):
        c = np.corrcoef(prediction[:, k], target[:, k])[0, 1]
        corrs.append(0.0 if not np.isfinite(c) else float(c))
    nmse = float(np.mean((prediction - target) ** 2) / (np.mean(target ** 2) + 1e-12))
    entropy = -np.sum(M * np.log(M + 1e-12), axis=1) / np.log(M.shape[1])
    return {
        "top1_useful": float(np.mean(top == useful)),
        "useful_mass": float(np.mean([M[i, useful[i]] for i in range(len(useful))])),
        "mean_target_correlation": float(np.mean(corrs)),
        "target_nmse": nmse,
        "mass_entropy": float(entropy.mean()),
        "dead_receiver_mass": float(M[:, -1].mean()),
    }


def digital_oracle(
    sender_events: Array,
    receiver_gates: Array,
    actuator_matrix: Array,
    target: Array,
    max_delay: int = 50,
) -> tuple[Array, Array]:
    """Exhaustive attacker: search delay and task utility, then hard-wire one edge per sender."""
    E = np.asarray(sender_events, dtype=float)
    G = np.asarray(receiver_gates, dtype=float)
    A = np.asarray(actuator_matrix, dtype=float)
    T = np.asarray(target, dtype=float)
    ns, nr = E.shape[1], G.shape[1]
    mass = np.zeros((ns, nr), dtype=float)
    delays = np.zeros((ns, nr), dtype=int)
    for i in range(ns):
        best_j, best_d, best_score = 0, 0, -np.inf
        for j in range(nr):
            for d in range(max_delay + 1):
                q = edge_trace(E[:, i], G[:, j], d)
                contribution = q[:, None] * A[j][None, :]
                score = -float(np.mean((T - contribution) ** 2))
                if score > best_score:
                    best_score, best_j, best_d = score, j, d
        mass[i, best_j] = 1.0
        delays[i, best_j] = best_d
    return mass, delays
