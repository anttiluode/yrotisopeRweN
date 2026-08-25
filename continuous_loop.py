"""Continuous growing-matrix cell for yrotisopeRweN Gate 11.

Gate 10 still trained on isolated sample arrays. Gate 11 removes the reset:
relation compartments, eligibility, structural mass, and output all run in one
continuous stream. An output threshold is kept separate from the internal field;
emitting an output does not reset the internal state unless an ablation asks it to.

The heterogeneous leaky compartments are only a computational abstraction of
spatially extended temporal integration. They are not a dendrite simulation.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import deque
import numpy as np

Array = np.ndarray

PHASE1_CELLS = ((0, 0), (1, 3), (4, 2), (5, 5))
PHASE2_CELLS = ((0, 4), (2, 1), (3, 5), (5, 0))


def sparse_pattern(n_channels: int, cells: tuple[tuple[int, int], ...]) -> Array:
    n = int(n_channels)
    out = np.zeros(n * n, dtype=float)
    for i, j in cells:
        out[i * n + j] = 1.0 / len(cells)
    return out


def branch_decay_field(n_channels: int = 6, seed: int = 123) -> Array:
    """Fixed heterogeneous local time constants; no learned geometry yet."""
    d = int(n_channels) ** 2
    values = np.linspace(0.65, 0.96, d)
    rng = np.random.default_rng(seed)
    rng.shuffle(values)
    return values


def project_global_budget(values: Array, reserve: float) -> Array:
    v = np.asarray(values, dtype=float)
    reserve = float(reserve)
    free = 1.0 - len(v) * reserve
    if reserve < 0.0 or free < -1e-12:
        raise ValueError("reserve incompatible with unit matrix budget")
    free = max(free, 0.0)
    excess = np.maximum(v - reserve, 0.0)
    share = np.full(len(v), 1.0 / len(v)) if excess.sum() < 1e-12 else excess / excess.sum()
    return reserve + free * share


def pattern_mass(mass: Array, pattern: Array) -> float:
    return float(np.asarray(mass)[np.asarray(pattern) > 0.0].sum())


def nmse(prediction: Array, target: Array) -> float:
    p = np.asarray(prediction, dtype=float)
    y = np.asarray(target, dtype=float)
    return float(np.mean((p - y) ** 2) / (np.var(y) + 1e-12))


def binary_f1(prediction: Array, target: Array) -> float:
    p = np.asarray(prediction, dtype=bool)
    y = np.asarray(target, dtype=bool)
    tp = np.sum(p & y)
    fp = np.sum(p & ~y)
    fn = np.sum(~p & y)
    return float(2 * tp / (2 * tp + fp + fn + 1e-12))


@dataclass
class ContinuousGrowingCell:
    n_channels: int = 6
    reserve: float = 0.001
    growth_rate: float = 0.06
    eligibility_decay: float = 0.92
    consequence_delay: int = 8
    score_decay: float = 0.99
    spike_threshold: float = 0.12
    branch_decays: Array | None = None
    seed: int = 0

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.mass = np.full(d, 1.0 / d, dtype=float)
        self.branch_state = np.zeros(d, dtype=float)
        self.eligibility = np.zeros(d, dtype=float)
        self.growth_score = np.zeros(d, dtype=float)
        self.rng = np.random.default_rng(self.seed)
        if self.branch_decays is None:
            self.branch_decays = branch_decay_field(self.n_channels)
        else:
            self.branch_decays = np.asarray(self.branch_decays, dtype=float).copy()
        if self.branch_decays.shape != (d,):
            raise ValueError("branch_decays must have one value per matrix cell")
        self._error_queue: deque[float] = deque(maxlen=self.consequence_delay + 1)

    @property
    def matrix(self) -> Array:
        return self.mass.reshape(self.n_channels, self.n_channels)

    def step(
        self,
        A: Array,
        B: Array,
        target_pattern: Array,
        *,
        learn: bool = True,
        use_consequence: bool = True,
        shuffle_eligibility: bool = False,
        use_explicit_eligibility: bool = True,
        reset_on_output: bool = False,
    ) -> dict[str, float]:
        A = np.asarray(A, dtype=float)
        B = np.asarray(B, dtype=float)
        if A.shape != (self.n_channels,) or B.shape != (self.n_channels,):
            raise ValueError("A and B must be channel vectors")

        drive = np.outer(A, B).reshape(-1)
        a = self.branch_decays
        self.branch_state = a * self.branch_state + (1.0 - a) * drive

        pattern = np.asarray(target_pattern, dtype=float)
        target_voltage = float(pattern @ self.branch_state)
        soma_voltage = float(self.mass @ self.branch_state)
        error = target_voltage - soma_voltage

        target_spike = target_voltage > self.spike_threshold
        output_spike = soma_voltage > self.spike_threshold

        self.eligibility = self.eligibility_decay * self.eligibility + self.branch_state * self.mass
        self._error_queue.append(error)

        delayed_error = None
        if len(self._error_queue) > self.consequence_delay:
            delayed_error = self._error_queue.popleft()

        if learn and delayed_error is not None:
            if use_consequence:
                trace = self.eligibility if use_explicit_eligibility else self.branch_state * self.mass
                if shuffle_eligibility:
                    trace = trace[self.rng.permutation(len(trace))]
                impulse = np.maximum(float(delayed_error) * trace, 0.0)
            else:
                impulse = (self.branch_state * self.mass) ** 2

            self.growth_score = self.score_decay * self.growth_score + (1.0 - self.score_decay) * impulse
            proposal = self.mass + self.growth_rate * self.growth_score
            self.mass = project_global_budget(proposal, self.reserve)

        if reset_on_output and output_spike:
            self.branch_state[:] = 0.0
            self.eligibility[:] = 0.0

        return {
            "target_voltage": target_voltage,
            "soma_voltage": soma_voltage,
            "target_spike": float(target_spike),
            "output_spike": float(output_spike),
        }


def run_continuous_stream(
    seed: int = 0,
    n_steps: int = 30_000,
    *,
    use_consequence: bool = True,
    shuffle_eligibility: bool = False,
    use_explicit_eligibility: bool = True,
    reset_on_output: bool = False,
    instantaneous_compartments: bool = False,
) -> dict[str, float | Array | None]:
    """One unbroken stream with a midstream change in useful structure."""
    n = 6
    rng = np.random.default_rng(seed)
    p1 = sparse_pattern(n, PHASE1_CELLS)
    p2 = sparse_pattern(n, PHASE2_CELLS)
    decays = np.zeros(n * n) if instantaneous_compartments else branch_decay_field(n)
    cell = ContinuousGrowingCell(n_channels=n, branch_decays=decays, seed=seed)

    switch = n_steps // 2
    target_v = np.empty(n_steps, dtype=float)
    soma_v = np.empty(n_steps, dtype=float)
    target_s = np.empty(n_steps, dtype=bool)
    output_s = np.empty(n_steps, dtype=bool)
    mass_at_switch = None
    adaptation_steps = None

    for t in range(n_steps):
        if t == switch:
            mass_at_switch = cell.mass.copy()
        A = rng.normal(size=n)
        B = rng.normal(size=n)
        pattern = p1 if t < switch else p2
        out = cell.step(
            A,
            B,
            pattern,
            use_consequence=use_consequence,
            shuffle_eligibility=shuffle_eligibility,
            use_explicit_eligibility=use_explicit_eligibility,
            reset_on_output=reset_on_output,
        )
        target_v[t] = out["target_voltage"]
        soma_v[t] = out["soma_voltage"]
        target_s[t] = bool(out["target_spike"])
        output_s[t] = bool(out["output_spike"])
        if t >= switch and adaptation_steps is None and pattern_mass(cell.mass, p2) > 0.90:
            adaptation_steps = t - switch

    if mass_at_switch is None:
        mass_at_switch = cell.mass.copy()
    tail = min(4_000, switch // 2)
    p1_slice = slice(switch - tail, switch)
    p2_slice = slice(n_steps - tail, n_steps)

    return {
        "phase1_nmse": nmse(soma_v[p1_slice], target_v[p1_slice]),
        "phase2_nmse": nmse(soma_v[p2_slice], target_v[p2_slice]),
        "phase1_spike_f1": binary_f1(output_s[p1_slice], target_s[p1_slice]),
        "phase2_spike_f1": binary_f1(output_s[p2_slice], target_s[p2_slice]),
        "phase1_useful_mass": pattern_mass(mass_at_switch, p1),
        "phase2_useful_mass": pattern_mass(cell.mass, p2),
        "adaptation_steps": adaptation_steps,
        "final_mass": cell.mass.copy(),
    }


@dataclass
class BufferedSignedAttacker:
    """Digital control: exact delayed state buffer plus signed structural update."""
    n_channels: int = 6
    learning_rate: float = 0.01
    consequence_delay: int = 8

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.mass = np.full(d, 1.0 / d, dtype=float)
        self.branch_state = np.zeros(d, dtype=float)
        self.branch_decays = branch_decay_field(self.n_channels)
        self._state_queue: deque[Array] = deque(maxlen=self.consequence_delay + 1)
        self._error_queue: deque[float] = deque(maxlen=self.consequence_delay + 1)

    def step(self, A: Array, B: Array, target_pattern: Array) -> tuple[float, float]:
        drive = np.outer(A, B).reshape(-1)
        a = self.branch_decays
        self.branch_state = a * self.branch_state + (1.0 - a) * drive
        target = float(np.asarray(target_pattern) @ self.branch_state)
        pred = float(self.mass @ self.branch_state)
        self._state_queue.append(self.branch_state.copy())
        self._error_queue.append(target - pred)
        if len(self._error_queue) > self.consequence_delay:
            old_state = self._state_queue.popleft()
            old_error = self._error_queue.popleft()
            self.mass = project_global_budget(
                self.mass + self.learning_rate * old_error * old_state,
                reserve=0.0,
            )
        return pred, target


def run_buffered_attacker(seed: int = 0, n_steps: int = 30_000) -> dict[str, float | None]:
    n = 6
    rng = np.random.default_rng(seed)
    p1 = sparse_pattern(n, PHASE1_CELLS)
    p2 = sparse_pattern(n, PHASE2_CELLS)
    model = BufferedSignedAttacker(n_channels=n)
    switch = n_steps // 2
    pred = np.empty(n_steps)
    target = np.empty(n_steps)
    mass_at_switch = None
    adaptation = None
    for t in range(n_steps):
        if t == switch:
            mass_at_switch = model.mass.copy()
        A = rng.normal(size=n)
        B = rng.normal(size=n)
        pattern = p1 if t < switch else p2
        pred[t], target[t] = model.step(A, B, pattern)
        if t >= switch and adaptation is None and pattern_mass(model.mass, p2) > 0.90:
            adaptation = t - switch
    tail = min(4_000, switch // 2)
    return {
        "phase1_nmse": nmse(pred[switch-tail:switch], target[switch-tail:switch]),
        "phase2_nmse": nmse(pred[-tail:], target[-tail:]),
        "phase1_useful_mass": pattern_mass(mass_at_switch, p1),
        "phase2_useful_mass": pattern_mass(model.mass, p2),
        "adaptation_steps": adaptation,
    }
