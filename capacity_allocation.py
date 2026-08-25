"""Finite positive-growth allocation for yrotisopeRweN Gate 9.

Gate 8 supplied delayed utility/eligibility. Gate 9 asks whether a finite
capacity budget can turn positive evidence into reallocation, and whether a
small exploratory reserve prevents hard consolidation from freezing forever.

This is not presented as a superior optimizer. A signed projected-gradient
attacker is included and should be allowed to win.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from consequence_learning import make_consequence_world

Array = np.ndarray
PAIR_FAMILIES = ((0, 3), (1, 2))
PHASE1_PATTERN = np.array([1.0, 0.0, 1.0, 0.0])
PHASE2_PATTERN = np.array([0.0, 1.0, 0.0, 1.0])


def make_allocation_world(
    n_trials: int = 10_000,
    seed: int = 0,
) -> dict[str, Array]:
    w = make_consequence_world(n_trials=n_trials, context_gap=4, seed=seed)
    target1 = w["ideal_features"] @ PHASE1_PATTERN
    target2 = w["ideal_features"] @ PHASE2_PATTERN
    return {
        "features": w["features"],
        "target1": target1,
        "target2": target2,
        "phase1_pattern": PHASE1_PATTERN.copy(),
        "phase2_pattern": PHASE2_PATTERN.copy(),
    }


def nmse(prediction: Array, target: Array) -> float:
    pred = np.asarray(prediction, dtype=float)
    truth = np.asarray(target, dtype=float)
    return float(np.mean((pred - truth) ** 2) / (np.var(truth) + 1e-12))


def useful_mass(mass: Array, pattern: Array) -> float:
    m = np.asarray(mass, dtype=float)
    p = np.asarray(pattern, dtype=float)
    return float(np.mean(m[p > 0.5]))


def _project_pair_budgets(values: Array, reserve: float) -> Array:
    """Each context family owns one unit of capacity split between two rivals."""
    if reserve < 0.0 or reserve >= 0.5:
        raise ValueError("reserve must satisfy 0 <= reserve < 0.5")
    out = np.asarray(values, dtype=float).copy()
    for a, b in PAIR_FAMILIES:
        pair = np.maximum(out[[a, b]] - reserve, 0.0)
        if pair.sum() < 1e-12:
            share = np.array([0.5, 0.5])
        else:
            share = pair / pair.sum()
        out[[a, b]] = reserve + (1.0 - 2.0 * reserve) * share
    return out


@dataclass
class ConservedGrowthAllocator:
    """Positive-only local growth plus conserved pairwise capacity."""

    reserve: float = 0.02
    growth_rate: float = 3.0
    seed: int = 0

    def __post_init__(self) -> None:
        self.mass = np.full(4, 0.5, dtype=float)
        self.rng = np.random.default_rng(self.seed)

    def develop(
        self,
        features: Array,
        target: Array,
        epochs: int = 120,
        use_consequence: bool = True,
        shuffle_eligibility: bool = False,
    ) -> "ConservedGrowthAllocator":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        for _ in range(int(epochs)):
            prediction = X @ self.mass
            error = y - prediction

            if use_consequence:
                eligibility = X * self.mass[None, :]
                if shuffle_eligibility:
                    eligibility = eligibility[self.rng.permutation(len(X))]
                score = np.mean(error[:, None] * eligibility, axis=0)
                growth = np.maximum(score, 0.0)
            else:
                # Co-activation-only control: no task consequence says what matters.
                growth = np.mean((X * self.mass[None, :]) ** 2, axis=0)

            proposal = self.mass + self.growth_rate * growth
            self.mass = _project_pair_budgets(proposal, self.reserve)
        return self

    def hard_consolidate(
        self,
        threshold: float = 0.01,
    ) -> "ConservedGrowthAllocator":
        """Prune tiny unreserved alternatives, then restore each pair budget."""
        for a, b in PAIR_FAMILIES:
            pair = self.mass[[a, b]].copy()
            pair[pair < float(threshold)] = 0.0
            if pair.sum() < 1e-12:
                pair[:] = 0.5
            else:
                pair /= pair.sum()
            self.mass[[a, b]] = pair
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass


@dataclass
class UnlimitedPositiveGrowth:
    """Ablation: positive growth without conservation can only accumulate."""

    growth_rate: float = 3.0

    def __post_init__(self) -> None:
        self.mass = np.full(4, 0.02, dtype=float)

    def develop(
        self,
        features: Array,
        target: Array,
        epochs: int = 120,
    ) -> "UnlimitedPositiveGrowth":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        for _ in range(int(epochs)):
            error = y - X @ self.mass
            eligibility = X * self.mass[None, :]
            growth = np.maximum(
                np.mean(error[:, None] * eligibility, axis=0),
                0.0,
            )
            self.mass = np.clip(
                self.mass + self.growth_rate * growth,
                0.0,
                1.0,
            )
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass


@dataclass
class SignedProjectedAttacker:
    """Boring optimizer: signed gradient can grow and retract directly."""

    learning_rate: float = 1.0

    def __post_init__(self) -> None:
        self.mass = np.full(4, 0.5, dtype=float)

    def develop(
        self,
        features: Array,
        target: Array,
        epochs: int = 40,
    ) -> "SignedProjectedAttacker":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        for _ in range(int(epochs)):
            error = y - X @ self.mass
            gradient = np.mean(error[:, None] * X, axis=0)
            self.mass = _project_pair_budgets(
                self.mass + self.learning_rate * gradient,
                reserve=0.0,
            )
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass
