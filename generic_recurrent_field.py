"""Generic mixed-coordinate recurrent field for yrotisopeRweN Gate 15.

Gate 14 still mapped every anonymous incoming channel to a dedicated matrix
coordinate. Gate 15 removes that convenience. Each point receives the same six
raw streams, but its internal candidate cells are dense random mixtures of all
six channels. No feature is a channel axis.

The question is whether delayed consequence plus finite positive-only growth can
select a stable recurrent computational subspace in this generic field.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import numpy as np

Array = np.ndarray


def project_global_budget(values: Array, reserve: float = 0.0002) -> Array:
    v = np.asarray(values, dtype=float)
    free = 1.0 - len(v) * float(reserve)
    if reserve < 0.0 or free < -1e-12:
        raise ValueError("reserve incompatible with unit budget")
    free = max(free, 0.0)
    excess = np.maximum(v - reserve, 0.0)
    share = np.full(len(v), 1.0 / len(v)) if excess.sum() < 1e-12 else excess / excess.sum()
    return reserve + free * share


def cue_state(t: int, period: int = 180, width: int = 10) -> tuple[float, float, bool]:
    block = int(t) // int(period)
    sign = 1.0 if block % 2 == 0 else -1.0
    active = (int(t) % int(period)) < int(width)
    return (2.0 * sign if active else 0.0), sign, active


@dataclass
class GenericFeatureCell:
    n_channels: int = 6
    n_features: int = 24
    reserve: float = 0.0002
    output_gain: float = 3.0
    feature_gain: float = 2.0
    growth_rate: float = 0.10
    eligibility_decay: float = 0.93
    score_decay: float = 0.995
    nonlinear: bool = True
    seed: int = 0

    def __post_init__(self) -> None:
        if self.n_features < 2:
            raise ValueError("n_features must be at least 2")
        rng = np.random.default_rng(self.seed)

        # Dense random local coordinates. Every feature mixes every raw channel:
        # magnitudes are bounded away from zero, then each row is normalized.
        signs = rng.choice(np.array([-1.0, 1.0]), size=(self.n_features, self.n_channels))
        magnitudes = rng.uniform(0.5, 1.0, size=(self.n_features, self.n_channels))
        projection = signs * magnitudes
        projection /= np.linalg.norm(projection, axis=1, keepdims=True)
        self.projection = projection

        self.mass = np.full(self.n_features, 1.0 / self.n_features, dtype=float)
        self.state = np.zeros(self.n_features, dtype=float)
        self.eligibility = np.zeros(self.n_features, dtype=float)
        self.growth_score = np.zeros(self.n_features, dtype=float)

        decays = np.linspace(0.74, 0.82, self.n_features)
        rng.shuffle(decays)
        self.feature_decays = decays

    @property
    def max_axis_loading(self) -> float:
        """Largest absolute raw-channel coefficient in any internal feature."""
        return float(np.max(np.abs(self.projection)))

    @property
    def effective_feature_count(self) -> float:
        """exp(entropy): approximate number of structurally occupied features."""
        p = self.mass / self.mass.sum()
        return float(np.exp(-np.sum(p * np.log(p + 1e-15))))

    def forward(
        self,
        channel_values: Array,
        *,
        scramble_feature_addresses: bool = False,
        rng: np.random.Generator | None = None,
    ) -> float:
        x = np.asarray(channel_values, dtype=float)
        if x.shape != (self.n_channels,):
            raise ValueError("channel_values has wrong shape")

        mixed = self.projection @ x
        feature_drive = np.tanh(self.feature_gain * mixed) if self.nonlinear else mixed

        # Kill condition: the same computed features still exist, but which
        # physical/internal coordinate receives each one changes every step.
        if scramble_feature_addresses:
            if rng is None:
                raise ValueError("rng required when scrambling feature addresses")
            feature_drive = feature_drive[rng.permutation(self.n_features)]

        a = self.feature_decays
        self.state = a * self.state + (1.0 - a) * feature_drive
        self.eligibility = self.eligibility_decay * self.eligibility + self.state * self.mass
        return float(np.tanh(self.output_gain * (self.mass @ self.state)))

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
            trace = trace[rng.permutation(self.n_features)]
        impulse = np.maximum(float(delayed_error) * trace, 0.0)
        self.growth_score = self.score_decay * self.growth_score + (1.0 - self.score_decay) * impulse
        self.mass = project_global_budget(self.mass + self.growth_rate * self.growth_score, self.reserve)


def run_generic_basis_world(
    seed: int = 0,
    n_steps: int = 12_000,
    *,
    n_features: int = 24,
    learn: bool = True,
    memory_required: bool = True,
    scramble_feature_addresses: bool = False,
    shuffle_eligibility: bool = False,
    nonlinear: bool = True,
    cut_returns_after: int | None = None,
    freeze_after_cut: bool = True,
    nuisance_scale: float = 0.05,
    consequence_delay: int = 4,
) -> dict[str, float | Array | int]:
    """Continuous two-point recurrent task in a generic internal coordinate basis."""
    rng = np.random.default_rng(seed)
    a = GenericFeatureCell(n_features=n_features, nonlinear=nonlinear, seed=seed)
    b = GenericFeatureCell(n_features=n_features, nonlinear=nonlinear, seed=seed + 100)

    # Gate 14 already established stable anonymous input addresses. Gate 15
    # attacks the internal feature coordinates, not both scaffolds at once.
    perm_a = rng.permutation(4)
    perm_b = rng.permutation(4)

    a_prev = 0.0
    b_prev = 0.0
    error_queue: deque[float] = deque()
    late_correct: list[bool] = []

    nuisance = np.zeros(6, dtype=float)
    rho = np.array([0.90, 0.60, 0.20, 0.85, 0.50, 0.10])
    score_start = n_steps - min(3_000, n_steps // 3)

    for t in range(n_steps):
        cue, sign, active = cue_state(t)
        target = 0.90 * sign if memory_required else (0.90 * sign if active else 0.0)

        nuisance = rho * nuisance + np.sqrt(1.0 - rho * rho) * rng.normal(
            scale=nuisance_scale, size=6
        )

        cut = cut_returns_after is not None and t >= int(cut_returns_after)
        current_b = 0.0 if cut else b_prev
        current_a = 0.0 if cut else a_prev

        returns_a = np.array([current_b, nuisance[0], nuisance[1], nuisance[2]], dtype=float)[perm_a]
        returns_b = np.array([current_a, nuisance[3], nuisance[4], nuisance[5]], dtype=float)[perm_b]

        channels_a = np.zeros(6, dtype=float)
        channels_b = np.zeros(6, dtype=float)
        channels_a[0] = cue
        channels_a[1:5] = returns_a
        channels_b[1:5] = returns_b
        channels_a[5] = rng.normal(scale=0.02)
        channels_b[5] = rng.normal(scale=0.02)

        a_now = a.forward(
            channels_a,
            scramble_feature_addresses=scramble_feature_addresses,
            rng=rng,
        )
        b_now = b.forward(
            channels_b,
            scramble_feature_addresses=scramble_feature_addresses,
            rng=rng,
        )

        error_queue.append(float(target - a_now))
        if len(error_queue) > int(consequence_delay):
            delayed_error = error_queue.popleft()
            learning_now = learn and not (freeze_after_cut and cut)
            if learning_now:
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

        if t >= score_start and not active:
            if memory_required:
                late_correct.append((np.sign(a_now) == sign) and (abs(a_now) >= 0.50))
            else:
                late_correct.append(abs(a_now) < 0.20)

    return {
        "late_hold_accuracy": float(np.mean(late_correct)),
        "a_effective_feature_count": a.effective_feature_count,
        "b_effective_feature_count": b.effective_feature_count,
        "a_max_feature_mass": float(a.mass.max()),
        "b_max_feature_mass": float(b.mass.max()),
        "a_max_axis_loading": a.max_axis_loading,
        "b_max_axis_loading": b.max_axis_loading,
        "a_mass": a.mass.copy(),
        "b_mass": b.mass.copy(),
    }
