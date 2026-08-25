"""Global finite-growth relation matrix for yrotisopeRweN.

This is the first attack on Gate 9's hand-written rivalry scaffold.

Gate 9 told q00 which cell it competed with. Here every possible bilinear
relation A_i * B_j is simply one cell in an N x N candidate matrix. All cells
draw from ONE conserved material budget. Delayed consequence can provide only
positive local growth evidence; global conservation supplies the retraction.

The point is architectural, not optimizer performance. A signed projected
gradient attacker is included and should be allowed to win.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray


def relation_basis(A: Array, B: Array) -> Array:
    """Flatten all pairwise local conjunctions A_i * B_j."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 2 or B.ndim != 2 or A.shape != B.shape:
        raise ValueError("A and B must have matching shape (time, channels)")
    return np.einsum("ti,tj->tij", A, B).reshape(len(A), -1)


def sparse_pattern(n_channels: int, cells: tuple[tuple[int, int], ...]) -> Array:
    """Unit-budget sparse target matrix, flattened row-major."""
    n = int(n_channels)
    out = np.zeros(n * n, dtype=float)
    if not cells:
        raise ValueError("cells must be nonempty")
    for i, j in cells:
        if not (0 <= i < n and 0 <= j < n):
            raise ValueError("cell outside matrix")
        out[i * n + j] = 1.0 / len(cells)
    return out


def make_growing_matrix_world(
    n_samples: int = 10_000,
    n_channels: int = 6,
    seed: int = 0,
) -> dict[str, Array]:
    """Dense candidate relation field with two disjoint useful sparse patterns."""
    if n_channels != 6:
        raise ValueError("development world currently fixes n_channels=6")
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n_samples, n_channels))
    B = rng.normal(size=(n_samples, n_channels))
    features = relation_basis(A, B)

    cells1 = ((0, 0), (1, 3), (4, 2), (5, 5))
    cells2 = ((0, 4), (2, 1), (3, 5), (5, 0))
    pattern1 = sparse_pattern(n_channels, cells1)
    pattern2 = sparse_pattern(n_channels, cells2)

    return {
        "A": A,
        "B": B,
        "features": features,
        "target1": features @ pattern1,
        "target2": features @ pattern2,
        "pattern1": pattern1,
        "pattern2": pattern2,
    }


def nmse(prediction: Array, target: Array) -> float:
    pred = np.asarray(prediction, dtype=float)
    truth = np.asarray(target, dtype=float)
    return float(np.mean((pred - truth) ** 2) / (np.var(truth) + 1e-12))


def pattern_mass(mass: Array, pattern: Array) -> float:
    m = np.asarray(mass, dtype=float)
    p = np.asarray(pattern, dtype=float)
    return float(m[p > 0.0].sum())


def _project_global_budget(values: Array, reserve: float) -> Array:
    """Project all cells onto one unit budget with a per-cell exploration floor."""
    v = np.asarray(values, dtype=float)
    d = len(v)
    reserve = float(reserve)
    free = 1.0 - d * reserve
    if reserve < 0.0 or free < -1e-12:
        raise ValueError("reserve is incompatible with global unit budget")
    free = max(free, 0.0)
    excess = np.maximum(v - reserve, 0.0)
    if excess.sum() < 1e-12:
        share = np.full(d, 1.0 / d)
    else:
        share = excess / excess.sum()
    return reserve + free * share


@dataclass
class GrowingRelationMatrix:
    """Positive-only local growth under one conserved matrix-wide budget."""

    n_channels: int = 6
    reserve: float = 0.001
    growth_rate: float = 8.0
    trace_decay: float = 0.95
    consequence_delay: int = 8
    seed: int = 0

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.mass = np.full(d, 1.0 / d, dtype=float)
        self.rng = np.random.default_rng(self.seed)

    @property
    def matrix(self) -> Array:
        return self.mass.reshape(self.n_channels, self.n_channels)

    def develop(
        self,
        features: Array,
        target: Array,
        epochs: int = 160,
        use_consequence: bool = True,
        shuffle_eligibility: bool = False,
    ) -> "GrowingRelationMatrix":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        if X.ndim != 2 or X.shape[1] != len(self.mass) or len(X) != len(y):
            raise ValueError("features and target have incompatible shapes")

        trace_scale = self.trace_decay ** int(self.consequence_delay)

        for _ in range(int(epochs)):
            error = y - X @ self.mass

            if use_consequence:
                # A cell can only claim growth if it was active enough to leave
                # eligibility. A zeroed cell therefore cannot magically regrow.
                eligibility = trace_scale * (X * self.mass[None, :])
                if shuffle_eligibility:
                    eligibility = eligibility[self.rng.permutation(len(X))]
                score = np.mean(error[:, None] * eligibility, axis=0)
                growth = np.maximum(score, 0.0)
            else:
                # Co-activation-only control: no consequence says what mattered.
                growth = np.mean((X * self.mass[None, :]) ** 2, axis=0)

            proposal = self.mass + self.growth_rate * growth
            self.mass = _project_global_budget(proposal, self.reserve)
        return self

    def hard_consolidate(self, threshold: float = 0.01) -> "GrowingRelationMatrix":
        """Prune low-mass cells completely, then renormalize the surviving matrix."""
        keep = self.mass.copy()
        keep[keep < float(threshold)] = 0.0
        if keep.sum() < 1e-12:
            keep[:] = 1.0 / len(keep)
        else:
            keep /= keep.sum()
        self.mass = keep
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass


@dataclass
class UnlimitedMatrixGrowth:
    """Ablation: positive growth with no shared material budget."""

    n_channels: int = 6
    growth_rate: float = 8.0
    trace_decay: float = 0.95
    consequence_delay: int = 8

    def __post_init__(self) -> None:
        self.mass = np.full(self.n_channels * self.n_channels, 0.001, dtype=float)

    def develop(self, features: Array, target: Array, epochs: int = 160) -> "UnlimitedMatrixGrowth":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        trace_scale = self.trace_decay ** int(self.consequence_delay)
        for _ in range(int(epochs)):
            error = y - X @ self.mass
            eligibility = trace_scale * (X * self.mass[None, :])
            growth = np.maximum(np.mean(error[:, None] * eligibility, axis=0), 0.0)
            self.mass = np.clip(self.mass + self.growth_rate * growth, 0.0, 1.0)
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass


@dataclass
class SignedGlobalAttacker:
    """Boring optimizer: signed gradient can grow and retract any cell directly."""

    n_channels: int = 6
    learning_rate: float = 0.5

    def __post_init__(self) -> None:
        d = self.n_channels * self.n_channels
        self.mass = np.full(d, 1.0 / d, dtype=float)

    def develop(self, features: Array, target: Array, epochs: int = 60) -> "SignedGlobalAttacker":
        X = np.asarray(features, dtype=float)
        y = np.asarray(target, dtype=float)
        for _ in range(int(epochs)):
            error = y - X @ self.mass
            gradient = np.mean(error[:, None] * X, axis=0)
            self.mass = _project_global_budget(
                self.mass + self.learning_rate * gradient,
                reserve=0.0,
            )
        return self

    def predict(self, features: Array) -> Array:
        return np.asarray(features, dtype=float) @ self.mass
