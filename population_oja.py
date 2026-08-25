"""Population differentiation gate for yrotisopeRweN.

Gate 3 established that one Oja unit learns one stable covariance axis. This
module asks the deliberately smaller next question: if several otherwise
identical normalized-Hebbian points see the same world, do they divide the
available structure among themselves?

Two arms are kept intentionally plain:

* IndependentOjaPopulation: every unit gets the same input and learns alone.
* SangerPopulation: the same Oja-like update plus the smallest ordered
  between-unit deflation term (Generalized Hebbian Algorithm / Sanger rule).

No phase gate, utility, mass, geometry, or structural growth is trained here.
The gate is only about population differentiation.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
import numpy as np

Array = np.ndarray


def _ar1(n: int, rho: float, rng: np.random.Generator) -> Array:
    x = np.empty(n, dtype=float)
    x[0] = rng.normal()
    scale = np.sqrt(max(1.0 - rho * rho, 1e-12))
    for i in range(1, n):
        x[i] = rho * x[i - 1] + scale * rng.normal()
    return x


def _orthogonal(dim: int, rng: np.random.Generator) -> Array:
    q, r = np.linalg.qr(rng.normal(size=(dim, dim)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q * signs


@dataclass(frozen=True)
class PopulationWorld:
    train_x: Array
    train_sources: Array
    test_x: Array
    test_sources: Array
    source_axes: Array


def variance_world(seed: int, n_train: int = 3500, n_test: int = 1800) -> PopulationWorld:
    """Four orthogonal latent modes with deliberately distinct variances.

    This is the theorem-friendly world for Oja/Sanger: zero-lag covariance is
    sufficient, so PCA is the correct digital attacker.
    """
    rng = np.random.default_rng(seed)
    dim = 4
    axes = _orthogonal(dim, rng)
    rhos = (0.96, 0.55, -0.35, 0.0)
    scales = np.asarray((2.0, 1.45, 1.0, 0.65), dtype=float)

    def sample(n: int) -> tuple[Array, Array]:
        cols = []
        for rho, scale in zip(rhos, scales):
            s = _ar1(n, rho, rng)
            s = (s - s.mean()) / (s.std() + 1e-12)
            cols.append(scale * s)
        sources = np.column_stack(cols)
        x = sources @ axes.T + 0.01 * rng.normal(size=(n, dim))
        return x, sources

    train_x, train_s = sample(n_train)
    test_x, test_s = sample(n_test)
    return PopulationWorld(train_x, train_s, test_x, test_s, axes)


def rank1_world(seed: int, n_train: int = 2500, n_test: int = 1400) -> PopulationWorld:
    """Kill world: only one informative direction exists.

    A learning rule is free to manufacture orthogonal weight vectors, but the
    outputs must still have information rank one. This catches the seductive
    mistake "different axes == different information".
    """
    rng = np.random.default_rng(seed)
    dim = 4
    axes = _orthogonal(dim, rng)

    def sample(n: int) -> tuple[Array, Array]:
        s = _ar1(n, 0.92, rng)
        s = (s - s.mean()) / (s.std() + 1e-12)
        sources = s[:, None]
        x = s[:, None] @ axes[:, :1].T
        return x, sources

    train_x, train_s = sample(n_train)
    test_x, test_s = sample(n_test)
    return PopulationWorld(train_x, train_s, test_x, test_s, axes[:, :1])


def lag_only_world(seed: int, n_train: int = 4096, n_test: int = 2048) -> PopulationWorld:
    """Boundary world: equal zero-lag power, distinct temporal dynamics.

    Four sinusoids have exactly equal sample variance and mutually orthogonal
    zero-lag columns, but very different lag-1 autocorrelations. PCA/Sanger
    has no principled source identity here because the covariance is spherical.
    This gate therefore SHOULD NOT solve the world. A later temporal method
    such as AMUSE/SOBI would have extra information to exploit.
    """
    rng = np.random.default_rng(seed)
    dim = 4
    axes = _orthogonal(dim, rng)
    train_bins = np.asarray((48, 216, 562, 1118), dtype=int)
    test_bins = train_bins // 2
    phases = rng.uniform(-np.pi, np.pi, size=dim)

    def sample(n: int, bins: Array) -> tuple[Array, Array]:
        t = np.arange(n, dtype=float)
        cols = [
            np.sqrt(2.0) * np.cos(2.0 * np.pi * k * t / n + ph)
            for k, ph in zip(bins, phases)
        ]
        sources = np.column_stack(cols)
        x = sources @ axes.T
        return x, sources

    train_x, train_s = sample(n_train, train_bins)
    test_x, test_s = sample(n_test, test_bins)
    return PopulationWorld(train_x, train_s, test_x, test_s, axes)


@dataclass
class IndependentOjaPopulation:
    n_units: int = 4
    learning_rate: float = 5e-4
    epochs: int = 3
    seed: int = 0

    def fit(self, x: Array) -> "IndependentOjaPopulation":
        X = np.asarray(x, dtype=float)
        if X.ndim != 2:
            raise ValueError("x must have shape (time, features)")
        rng = np.random.default_rng(self.seed)
        W = rng.normal(size=(self.n_units, X.shape[1]))
        W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-12
        for _ in range(int(self.epochs)):
            for row in X:
                y = W @ row
                W += self.learning_rate * y[:, None] * (row[None, :] - y[:, None] * W)
            W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-12
        self.W = W
        return self

    def transform(self, x: Array) -> Array:
        return np.asarray(x, dtype=float) @ self.W.T


@dataclass
class SangerPopulation:
    """Generalized Hebbian Algorithm: Oja plus ordered between-unit deflation."""

    n_units: int = 4
    learning_rate: float = 5e-4
    epochs: int = 3
    seed: int = 0

    def fit(self, x: Array) -> "SangerPopulation":
        X = np.asarray(x, dtype=float)
        if X.ndim != 2:
            raise ValueError("x must have shape (time, features)")
        rng = np.random.default_rng(self.seed)
        W = rng.normal(size=(self.n_units, X.shape[1]))
        W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-12

        for _ in range(int(self.epochs)):
            for row in X:
                y = W @ row
                old = W.copy()
                for i in range(self.n_units):
                    explained = np.sum(y[: i + 1, None] * old[: i + 1], axis=0)
                    W[i] += self.learning_rate * y[i] * (row - explained)
            W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-12
        self.W = W
        return self

    def transform(self, x: Array) -> Array:
        return np.asarray(x, dtype=float) @ self.W.T


def pca_attacker(x: Array, n_units: int = 4) -> Array:
    """Explicit eigendecomposition baseline. Rows are principal axes."""
    X = np.asarray(x, dtype=float)
    centered = X - X.mean(axis=0, keepdims=True)
    cov = centered.T @ centered / max(len(centered), 1)
    values, vectors = np.linalg.eigh(cov)
    order = np.argsort(values)[::-1][:n_units]
    return vectors[:, order].T


def mean_weight_duplication(weights: Array) -> float:
    W = np.asarray(weights, dtype=float)
    W = W / (np.linalg.norm(W, axis=1, keepdims=True) + 1e-12)
    c = np.abs(W @ W.T)
    n = len(W)
    if n < 2:
        return 0.0
    return float((c.sum() - n) / (n * (n - 1)))


def _best_assignment(score: Array) -> float:
    S = np.asarray(score, dtype=float)
    n = min(S.shape)
    if S.shape[0] != S.shape[1]:
        raise ValueError("assignment metric expects a square score matrix")
    best = max(sum(S[i, p[i]] for i in range(n)) for p in permutations(range(n)))
    return float(best / n)


def axis_recovery(weights: Array, source_axes: Array) -> float:
    W = np.asarray(weights, dtype=float)
    A = np.asarray(source_axes, dtype=float)
    if W.shape[0] != A.shape[1] or W.shape[1] != A.shape[0]:
        raise ValueError("weights/source_axes shape mismatch")
    score = np.abs(W @ A)
    return _best_assignment(score)


def source_recovery(outputs: Array, sources: Array) -> float:
    Y = np.asarray(outputs, dtype=float)
    S = np.asarray(sources, dtype=float)
    if Y.shape[1] != S.shape[1]:
        raise ValueError("outputs and sources need equal component count")
    score = np.zeros((Y.shape[1], S.shape[1]), dtype=float)
    for i in range(Y.shape[1]):
        for j in range(S.shape[1]):
            sy = Y[:, i].std()
            ss = S[:, j].std()
            if sy > 1e-12 and ss > 1e-12:
                score[i, j] = abs(np.corrcoef(Y[:, i], S[:, j])[0, 1])
    return _best_assignment(score)


def distinct_source_claims(outputs: Array, sources: Array, threshold: float = 0.80) -> int:
    """How many different known sources are strongly claimed by at least one unit?"""
    Y = np.asarray(outputs, dtype=float)
    S = np.asarray(sources, dtype=float)
    claimed: set[int] = set()
    for i in range(Y.shape[1]):
        correlations = []
        for j in range(S.shape[1]):
            if Y[:, i].std() <= 1e-12 or S[:, j].std() <= 1e-12:
                correlations.append(0.0)
            else:
                correlations.append(abs(np.corrcoef(Y[:, i], S[:, j])[0, 1]))
        j = int(np.argmax(correlations))
        if correlations[j] >= threshold:
            claimed.add(j)
    return len(claimed)


def effective_rank(outputs: Array) -> float:
    """Participation-ratio rank of output covariance (1 means one information mode)."""
    Y = np.asarray(outputs, dtype=float)
    Y = Y - Y.mean(axis=0, keepdims=True)
    cov = Y.T @ Y / max(len(Y), 1)
    eig = np.clip(np.linalg.eigvalsh(cov), 0.0, None)
    total = eig.sum()
    if total <= 1e-15:
        return 0.0
    return float(total * total / (np.square(eig).sum() + 1e-15))


def lag1_autocorrelations(sources: Array) -> Array:
    S = np.asarray(sources, dtype=float)
    vals = []
    for j in range(S.shape[1]):
        a = S[:-1, j]
        b = S[1:, j]
        vals.append(float(np.corrcoef(a, b)[0, 1]))
    return np.asarray(vals)
