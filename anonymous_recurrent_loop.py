"""Anonymous return-channel growth for yrotisopeRweN Gate 14.

Gate 13 named one matrix coordinate "peer return". Gate 14 removes that label.
Each cell receives four generic return channels in a seed-specific fixed
permutation: one carries the current peer broadcast and three carry unrelated
traffic. The growth rule sees only local activity and delayed consequence.

If channel identities are reshuffled every timestep, no stable structural
address exists and the recurrent memory should fail.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import deque
import numpy as np

Array = np.ndarray


def project_global_budget(values: Array, reserve: float = 0.001) -> Array:
    v = np.asarray(values, dtype=float)
    free = 1.0 - len(v) * float(reserve)
    if reserve < 0.0 or free < -1e-12:
        raise ValueError("reserve incompatible with unit budget")
    free = max(free, 0.0)
    excess = np.maximum(v - reserve, 0.0)
    share = np.full(len(v), 1.0 / len(v)) if excess.sum() < 1e-12 else excess / excess.sum()
    return reserve + free * share


@dataclass
class AnonymousMatrixCell:
    n_channels: int = 6
    reserve: float = 0.001
    gain: float = 3.0
    growth_rate: float = 0.10
    eligibility_decay: float = 0.93
    score_decay: float = 0.995
    seed: int = 0

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.mass = np.full(d, 1.0 / d, dtype=float)
        self.state = np.zeros(d, dtype=float)
        self.eligibility = np.zeros(d, dtype=float)
        self.growth_score = np.zeros(d, dtype=float)
        rng = np.random.default_rng(self.seed)
        decays = np.linspace(0.74, 0.82, d)
        rng.shuffle(decays)
        self.branch_decays = decays

    def forward(self, channel_values: Array) -> float:
        x = np.asarray(channel_values, dtype=float)
        if x.shape != (self.n_channels,):
            raise ValueError("channel_values has wrong shape")
        drive = np.zeros(self.n_channels * self.n_channels, dtype=float)
        for i, value in enumerate(x):
            drive[i * self.n_channels] = value
        a = self.branch_decays
        self.state = a * self.state + (1.0 - a) * drive
        self.eligibility = self.eligibility_decay * self.eligibility + self.state * self.mass
        return float(np.tanh(self.gain * (self.mass @ self.state)))

    def grow_from_consequence(self, delayed_error: float, *, shuffle_eligibility: bool = False, rng: np.random.Generator | None = None) -> None:
        trace = self.eligibility
        if shuffle_eligibility:
            if rng is None:
                raise ValueError("rng required when shuffling eligibility")
            trace = trace[rng.permutation(len(trace))]
        impulse = np.maximum(float(delayed_error) * trace, 0.0)
        self.growth_score = self.score_decay * self.growth_score + (1.0 - self.score_decay) * impulse
        self.mass = project_global_budget(self.mass + self.growth_rate * self.growth_score, self.reserve)


def cue_state(t: int, period: int = 180, width: int = 10) -> tuple[float, float, bool]:
    block = int(t) // int(period)
    sign = 1.0 if block % 2 == 0 else -1.0
    active = (int(t) % int(period)) < int(width)
    return (2.0 * sign if active else 0.0), sign, active


def run_anonymous_return_world(
    seed: int = 0,
    n_steps: int = 15_000,
    *,
    learn: bool = True,
    memory_required: bool = True,
    dynamic_channel_shuffle: bool = False,
    shuffle_eligibility: bool = False,
    cut_useful_return_after: int | None = None,
    nuisance_scale: float = 0.02,
    consequence_delay: int = 4,
) -> dict[str, float | Array | int]:
    rng = np.random.default_rng(seed)
    a = AnonymousMatrixCell(seed=seed)
    b = AnonymousMatrixCell(seed=seed + 1)

    # Source type 0 is the current peer broadcast; 1..3 are unrelated traffic.
    # Their channel positions are fixed but randomly permuted per seed.
    perm_a = rng.permutation(4)
    perm_b = rng.permutation(4)
    useful_slot_a = int(np.where(perm_a == 0)[0][0])
    useful_slot_b = int(np.where(perm_b == 0)[0][0])
    useful_channel_a = 1 + useful_slot_a
    useful_channel_b = 1 + useful_slot_b

    a_prev = 0.0
    b_prev = 0.0
    errq: deque[float] = deque()
    hold = np.zeros(n_steps, dtype=bool)
    correct = np.zeros(n_steps, dtype=bool)

    nuisance = np.zeros(6, dtype=float)
    rho = np.array([0.90, 0.60, 0.20, 0.85, 0.50, 0.10])

    for t in range(n_steps):
        cue, sign, active = cue_state(t)
        target = 0.90 * sign if memory_required else (0.90 * sign if active else 0.0)

        nuisance = rho * nuisance + np.sqrt(1.0 - rho * rho) * rng.normal(scale=nuisance_scale, size=6)
        current_b = b_prev
        current_a = a_prev
        if cut_useful_return_after is not None and t >= int(cut_useful_return_after):
            current_b = 0.0
            current_a = 0.0

        source_a = np.array([current_b, nuisance[0], nuisance[1], nuisance[2]], dtype=float)
        source_b = np.array([current_a, nuisance[3], nuisance[4], nuisance[5]], dtype=float)

        if dynamic_channel_shuffle:
            returns_a = source_a[rng.permutation(4)]
            returns_b = source_b[rng.permutation(4)]
        else:
            returns_a = source_a[perm_a]
            returns_b = source_b[perm_b]

        channels_a = np.zeros(6, dtype=float)
        channels_b = np.zeros(6, dtype=float)
        channels_a[0] = cue
        channels_a[1:5] = returns_a
        channels_b[1:5] = returns_b
        channels_a[5] = rng.normal(scale=0.02)
        channels_b[5] = rng.normal(scale=0.02)

        a_now = a.forward(channels_a)
        b_now = b.forward(channels_b)
        errq.append(float(target - a_now))
        if len(errq) > int(consequence_delay):
            delayed_error = errq.popleft()
            if learn:
                a.grow_from_consequence(delayed_error, shuffle_eligibility=shuffle_eligibility, rng=rng)
                b.grow_from_consequence(delayed_error, shuffle_eligibility=shuffle_eligibility, rng=rng)

        a_prev = a_now
        b_prev = b_now
        if not active:
            hold[t] = True
            if memory_required:
                correct[t] = (np.sign(a_now) == sign) and (abs(a_now) >= 0.50)
            else:
                correct[t] = abs(a_now) < 0.20

    mask = hold[-3_000:]
    late_accuracy = float(correct[-3_000:][mask].mean())

    def cell_mass(cell: AnonymousMatrixCell, channel: int) -> float:
        return float(cell.mass[int(channel) * cell.n_channels])

    useful_a = cell_mass(a, useful_channel_a)
    useful_b = cell_mass(b, useful_channel_b)
    other_a = max(cell_mass(a, ch) for ch in range(1, 5) if ch != useful_channel_a)
    other_b = max(cell_mass(b, ch) for ch in range(1, 5) if ch != useful_channel_b)

    return {
        "late_hold_accuracy": late_accuracy,
        "a_direct_cue_mass": cell_mass(a, 0),
        "a_useful_return_mass": useful_a,
        "b_useful_return_mass": useful_b,
        "closed_loop_mass": min(useful_a, useful_b),
        "a_best_other_return_mass": other_a,
        "b_best_other_return_mass": other_b,
        "useful_channel_a": useful_channel_a,
        "useful_channel_b": useful_channel_b,
        "a_mass": a.mass.copy(),
        "b_mass": b.mass.copy(),
    }
