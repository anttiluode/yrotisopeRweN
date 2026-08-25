"""Consequence-driven growth of recurrent matrix structure for Gate 13.

Gate 12 froze the A<->B loop and established that recurrent traffic can carry
state. Gate 13 starts both cells with diffuse 6x6 structural mass and asks
whether delayed consequence can grow a closed recurrent path only when the task
requires persistence between cues.

The product coordinates and global scalar consequence are still scaffolded.
This is not a biological learning rule or a claim of optimizer superiority.
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
    if excess.sum() < 1e-12:
        share = np.full(len(v), 1.0 / len(v))
    else:
        share = excess / excess.sum()
    return reserve + free * share


@dataclass
class GrowingRecurrentCell:
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

    @property
    def matrix(self) -> Array:
        return self.mass.reshape(self.n_channels, self.n_channels)

    def forward(
        self,
        external_cue: float,
        peer_broadcast: float,
        distractor: float,
        background: Array,
    ) -> float:
        # Constant B[0]=1 keeps Gate 13 focused on growth of recurrent structure,
        # not discovery of the product coordinate system itself.
        drive = np.zeros(self.n_channels * self.n_channels, dtype=float)
        drive[0] = float(external_cue)          # (0,0): direct cue
        drive[self.n_channels] = float(peer_broadcast)  # (1,0): peer return
        drive[2 * self.n_channels] = float(distractor)
        bg = np.asarray(background, dtype=float)
        if bg.shape != (self.n_channels - 3,):
            raise ValueError("background has wrong shape")
        for k, value in enumerate(bg, start=3):
            drive[k * self.n_channels] = value

        a = self.branch_decays
        self.state = a * self.state + (1.0 - a) * drive
        self.eligibility = (
            self.eligibility_decay * self.eligibility
            + self.state * self.mass
        )
        return float(np.tanh(self.gain * (self.mass @ self.state)))

    def grow_from_consequence(
        self,
        delayed_error: float,
        *,
        shuffle_eligibility: bool = False,
        rng: np.random.Generator | None = None,
    ) -> None:
        trace = self.eligibility
        if shuffle_eligibility:
            if rng is None:
                raise ValueError("rng required when shuffling eligibility")
            trace = trace[rng.permutation(len(trace))]
        impulse = np.maximum(float(delayed_error) * trace, 0.0)
        self.growth_score = (
            self.score_decay * self.growth_score
            + (1.0 - self.score_decay) * impulse
        )
        proposal = self.mass + self.growth_rate * self.growth_score
        self.mass = project_global_budget(proposal, self.reserve)


def cue_state(t: int, period: int = 180, width: int = 10) -> tuple[float, float, bool]:
    block = int(t) // int(period)
    sign = 1.0 if block % 2 == 0 else -1.0
    active = (int(t) % int(period)) < int(width)
    cue = 2.0 * sign if active else 0.0
    return cue, sign, active


def run_growing_recurrent_world(
    seed: int = 0,
    n_steps: int = 15_000,
    *,
    learn: bool = True,
    shuffle_eligibility: bool = False,
    memory_required: bool = True,
    consequence_delay: int = 4,
) -> dict[str, float | Array | None]:
    """Continuous alternating cues with or without a persistence requirement."""
    rng = np.random.default_rng(seed)
    a = GrowingRecurrentCell(seed=seed)
    b = GrowingRecurrentCell(seed=seed + 1)
    a_prev = 0.0
    b_prev = 0.0
    error_queue: deque[float] = deque()

    correct = np.zeros(n_steps, dtype=bool)
    hold_mask = np.zeros(n_steps, dtype=bool)
    first_good_step = None

    for t in range(n_steps):
        cue, sign, cue_active = cue_state(t)
        target = 0.90 * sign if memory_required else (0.90 * sign if cue_active else 0.0)

        a_now = a.forward(
            cue,
            b_prev,
            rng.normal(scale=0.03),
            rng.normal(scale=0.006, size=a.n_channels - 3),
        )
        b_now = b.forward(
            0.0,
            a_prev,
            rng.normal(scale=0.03),
            rng.normal(scale=0.006, size=b.n_channels - 3),
        )

        error_queue.append(float(target - a_now))
        if len(error_queue) > int(consequence_delay):
            delayed_error = error_queue.popleft()
            if learn:
                a.grow_from_consequence(
                    delayed_error,
                    shuffle_eligibility=shuffle_eligibility,
                    rng=rng,
                )
                b.grow_from_consequence(
                    delayed_error,
                    shuffle_eligibility=shuffle_eligibility,
                    rng=rng,
                )

        a_prev = a_now
        b_prev = b_now

        if not cue_active:
            hold_mask[t] = True
            if memory_required:
                correct[t] = (np.sign(a_now) == sign) and (abs(a_now) >= 0.50)
            else:
                correct[t] = abs(a_now) < 0.20

        if memory_required and first_good_step is None and t >= 720 and t % 180 == 0:
            m = hold_mask[t - 720:t]
            if m.any() and float(correct[t - 720:t][m].mean()) > 0.90:
                first_good_step = t

    def window_accuracy(start: int, stop: int) -> float:
        mask = hold_mask[start:stop]
        if not mask.any():
            return 0.0
        return float(correct[start:stop][mask].mean())

    peer_idx = a.n_channels
    closed_loop_mass = min(float(a.mass[peer_idx]), float(b.mass[peer_idx]))
    return {
        "early_hold_accuracy": window_accuracy(0, min(3_000, n_steps)),
        "late_hold_accuracy": window_accuracy(max(0, n_steps - 3_000), n_steps),
        "a_cue_mass": float(a.mass[0]),
        "a_return_mass": float(a.mass[peer_idx]),
        "b_forward_mass": float(b.mass[peer_idx]),
        "closed_loop_mass": closed_loop_mass,
        "first_good_step": first_good_step,
        "a_mass": a.mass.copy(),
        "b_mass": b.mass.copy(),
    }
