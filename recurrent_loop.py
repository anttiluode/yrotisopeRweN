"""Frozen two-cell recurrent broadcast loop for yrotisopeRweN Gate 12.

Gate 11 established that a cell's internal relation state can continue while it
emits. Gate 12 isolates literal recurrence: two continuously running cells
broadcast into each other. Structural mass is deliberately frozen so any success
or failure belongs to recurrence rather than growth.

This is not a hippocampal model. It is the smallest recurrent traffic test the
main hypothesis currently needs.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import deque
import numpy as np

Array = np.ndarray


def frozen_matrix_mass(
    n_channels: int = 6,
    *,
    cue_weight: float = 0.45,
    peer_weight: float = 0.50,
    reserve: float = 0.001,
    peer_only: bool = False,
) -> Array:
    """Sparse unit-budget matrix with cue and peer-broadcast coordinates.

    The active coordinates are products with a constant carrier B[0]=1:

      (0,0) external cue * carrier
      (1,0) peer broadcast * carrier

    Gate 12 freezes this matrix on purpose. It does not claim these coordinates
    emerged biologically or through Gate-10 growth.
    """
    n = int(n_channels)
    d = n * n
    if reserve < 0 or reserve * d >= 1:
        raise ValueError("reserve incompatible with unit budget")
    mass = np.full(d, float(reserve), dtype=float)
    cue_idx = 0
    peer_idx = n
    if peer_only:
        mass[peer_idx] = 1.0 - reserve * (d - 1)
    else:
        free = 1.0 - reserve * (d - 2)
        denom = float(cue_weight + peer_weight)
        if denom <= 0:
            raise ValueError("cue_weight + peer_weight must be positive")
        mass[cue_idx] = free * cue_weight / denom
        mass[peer_idx] = free * peer_weight / denom
    return mass


def branch_decay_field(n_channels: int = 6, seed: int = 17) -> Array:
    d = int(n_channels) ** 2
    values = np.linspace(0.78, 0.86, d)
    rng = np.random.default_rng(seed)
    rng.shuffle(values)
    return values


@dataclass
class FrozenMatrixCell:
    """Continuously running matrix-state cell with fixed structural mass."""

    n_channels: int = 6
    gain: float = 3.0
    mass: Array | None = None
    branch_decays: Array | None = None

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.state = np.zeros(d, dtype=float)
        if self.mass is None:
            self.mass = frozen_matrix_mass(self.n_channels)
        else:
            self.mass = np.asarray(self.mass, dtype=float).copy()
        if self.branch_decays is None:
            self.branch_decays = branch_decay_field(self.n_channels)
        else:
            self.branch_decays = np.asarray(self.branch_decays, dtype=float).copy()
        if self.mass.shape != (d,) or self.branch_decays.shape != (d,):
            raise ValueError("mass and branch_decays need one value per matrix cell")
        if not np.isclose(self.mass.sum(), 1.0):
            raise ValueError("frozen structural mass must sum to one")

    @property
    def matrix(self) -> Array:
        return self.mass.reshape(self.n_channels, self.n_channels)

    def step(
        self,
        external_cue: float,
        peer_broadcast: float,
        distractor: float,
        background: Array | None = None,
        *,
        reset_on_output: bool = False,
        reset_threshold: float = 0.80,
    ) -> float:
        # B[0]=1 is a boring carrier. The matrix therefore still receives a full
        # outer-product field, but only a few frozen cells have substantial mass.
        A = np.zeros(self.n_channels, dtype=float)
        B = np.zeros(self.n_channels, dtype=float)
        A[0] = float(external_cue)
        A[1] = float(peer_broadcast)
        A[2] = float(distractor)
        B[0] = 1.0
        if background is not None:
            bg = np.asarray(background, dtype=float)
            if bg.shape != (self.n_channels - 3,):
                raise ValueError("background has wrong shape")
            A[3:] = bg
        drive = np.outer(A, B).reshape(-1)
        a = self.branch_decays
        self.state = a * self.state + (1.0 - a) * drive
        voltage = float(self.mass @ self.state)
        output = float(np.tanh(self.gain * voltage))
        if reset_on_output and abs(output) > float(reset_threshold):
            self.state[:] = 0.0
        return output


def _cue_at(t: int, first: tuple[int, int, float], second: tuple[int, int, float]) -> float:
    if first[0] <= t < first[1]:
        return float(first[2])
    if second[0] <= t < second[1]:
        return float(second[2])
    return 0.0


def _state_score(signal: Array, desired_sign: float, start: int, stop: int, threshold: float = 0.50) -> float:
    x = np.asarray(signal, dtype=float)[start:stop]
    desired = float(np.sign(desired_sign))
    return float(np.mean((np.sign(x) == desired) & (np.abs(x) >= threshold)))


def run_recurrent_loop(
    seed: int = 0,
    n_steps: int = 400,
    *,
    cut_return: bool = False,
    scramble_return_timing: bool = False,
    reset_on_output: bool = False,
    recurrent_gain_scale: float = 1.0,
    instantaneous_compartments: bool = False,
) -> dict[str, float | Array]:
    """Brief cue -> ongoing A<->B traffic -> opposite cue overwrite.

    The first cue enters only cell A. It disappears after 10 steps. The pair then
    receives distractors only until an opposite cue arrives much later. Neither
    point is reset between these events.
    """
    rng = np.random.default_rng(seed)
    n = 6
    cue1 = (20, 30, +2.0)
    cue2 = (220, 230, -2.0)

    mass_a = frozen_matrix_mass(n, cue_weight=0.45, peer_weight=0.50)
    mass_b = frozen_matrix_mass(n, peer_only=True)

    if instantaneous_compartments:
        decays_a = np.zeros(n * n, dtype=float)
        decays_b = np.zeros(n * n, dtype=float)
    else:
        decays_a = branch_decay_field(n, seed=17)
        decays_b = branch_decay_field(n, seed=29)
    cell_a = FrozenMatrixCell(n_channels=n, mass=mass_a, branch_decays=decays_a)
    cell_b = FrozenMatrixCell(n_channels=n, mass=mass_b, branch_decays=decays_b)

    out_a = np.zeros(n_steps, dtype=float)
    out_b = np.zeros(n_steps, dtype=float)
    cue = np.zeros(n_steps, dtype=float)
    history_b: deque[float] = deque(maxlen=40)
    a_prev = 0.0
    b_prev = 0.0

    for t in range(n_steps):
        cue[t] = _cue_at(t, cue1, cue2)
        returned_b = 0.0 if cut_return else float(recurrent_gain_scale) * b_prev
        if scramble_return_timing and history_b:
            returned_b = float(recurrent_gain_scale) * history_b[int(rng.integers(0, len(history_b)))]

        # External signal enters A only. Both cells continue to receive unrelated
        # distractor/background traffic throughout the memory interval.
        bg_a = rng.normal(scale=0.006, size=n - 3)
        bg_b = rng.normal(scale=0.006, size=n - 3)
        a_now = cell_a.step(
            cue[t],
            returned_b,
            rng.normal(scale=0.03),
            bg_a,
            reset_on_output=reset_on_output,
        )
        b_now = cell_b.step(
            0.0,
            float(recurrent_gain_scale) * a_prev,
            rng.normal(scale=0.03),
            bg_b,
            reset_on_output=reset_on_output,
        )
        out_a[t] = a_now
        out_b[t] = b_now
        a_prev = a_now
        b_prev = b_now
        history_b.append(b_now)

    # Score long cue-free windows, not the cue itself.
    hold1 = (80, 200)
    hold2 = (280, 380)
    return {
        "hold1_a_accuracy": _state_score(out_a, +1, *hold1),
        "hold1_b_accuracy": _state_score(out_b, +1, *hold1),
        "hold2_a_accuracy": _state_score(out_a, -1, *hold2),
        "hold2_b_accuracy": _state_score(out_b, -1, *hold2),
        "hold1_a_mean": float(np.mean(out_a[slice(*hold1)])),
        "hold2_a_mean": float(np.mean(out_a[slice(*hold2)])),
        "hold1_b_mean": float(np.mean(out_b[slice(*hold1)])),
        "hold2_b_mean": float(np.mean(out_b[slice(*hold2)])),
        "out_a": out_a,
        "out_b": out_b,
        "cue": cue,
        "mass_a": cell_a.mass.copy(),
        "mass_b": cell_b.mass.copy(),
    }


def run_scalar_recurrent_attacker(
    seed: int = 0,
    n_steps: int = 400,
    leak: float = 0.25,
    recurrent_gain: float = 2.0,
    cue_gain: float = 2.0,
) -> dict[str, float | Array]:
    """Boring one-state recurrent control.

    It has no matrix, no local compartments and no two-cell loop. It exists to
    remind us that recurrent state, not matrix ornament, is the earned primitive.
    """
    rng = np.random.default_rng(seed)
    h = 0.0
    out = np.zeros(n_steps, dtype=float)
    cue = np.zeros(n_steps, dtype=float)
    for t in range(n_steps):
        cue[t] = _cue_at(t, (20, 30, +2.0), (220, 230, -2.0))
        proposal = np.tanh(recurrent_gain * h + cue_gain * cue[t] + rng.normal(scale=0.01))
        h = (1.0 - leak) * h + leak * proposal
        out[t] = h
    hold1 = (80, 200)
    hold2 = (280, 380)
    return {
        "hold1_accuracy": _state_score(out, +1, *hold1),
        "hold2_accuracy": _state_score(out, -1, *hold2),
        "hold1_mean": float(np.mean(out[slice(*hold1)])),
        "hold2_mean": float(np.mean(out[slice(*hold2)])),
        "out": out,
        "cue": cue,
    }
