"""One-lag temporal identification for yrotisopeRweN Gate 5.

Gate 4 deliberately stopped at zero-lag covariance. AMUSE is introduced only
now, because the remaining world has equal instantaneous covariance but
source-specific lag structure.

The implementation is intentionally tiny:

1. center and whiten at lag 0;
2. form one lagged covariance matrix;
3. symmetrize it for this real stationary toy;
4. diagonalize it once.

No mass, geometry, utility, phase learning, or nonlinear contrast is involved.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from population_oja import PopulationWorld

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


@dataclass
class AmuseModel:
    mean: Array
    demixer: Array
    lag_eigenvalues: Array

    def transform(self, x: Array) -> Array:
        X = np.asarray(x, dtype=float)
        return (X - self.mean) @ self.demixer.T


def fit_amuse(x: Array, lag: int = 1, eps: float = 1e-9) -> AmuseModel:
    """Whiten at lag 0, then diagonalize one symmetrized lagged covariance."""
    X = np.asarray(x, dtype=float)
    if X.ndim != 2:
        raise ValueError("x must have shape (time, features)")
    if lag < 1 or lag >= len(X):
        raise ValueError("lag must be between 1 and len(x)-1")

    mean = X.mean(axis=0, keepdims=True)
    Xc = X - mean
    c0 = Xc.T @ Xc / len(Xc)
    values, vectors = np.linalg.eigh(c0)
    keep = values > eps
    if int(np.sum(keep)) != X.shape[1]:
        raise ValueError("AMUSE gate expects full-rank covariance")

    values = values[keep]
    vectors = vectors[:, keep]
    whitening = vectors @ np.diag(1.0 / np.sqrt(values))
    Z = Xc @ whitening

    ct = Z[lag:].T @ Z[:-lag] / (len(Z) - lag)
    ct = 0.5 * (ct + ct.T)
    lag_values, lag_vectors = np.linalg.eigh(ct)
    order = np.argsort(np.abs(lag_values))[::-1]
    lag_values = lag_values[order]
    lag_vectors = lag_vectors[:, order]

    # y = (x-mean) @ whitening @ lag_vectors
    demixer = (whitening @ lag_vectors).T
    return AmuseModel(mean=mean, demixer=demixer, lag_eigenvalues=lag_values)


def same_memory_world(
    seed: int,
    n_train: int = 5000,
    n_test: int = 2500,
    rho: float = 0.72,
) -> PopulationWorld:
    """Kill world: four independent sources share the same AR(1) memory law."""
    rng = np.random.default_rng(seed)
    dim = 4
    axes = _orthogonal(dim, rng)

    def sample(n: int) -> tuple[Array, Array]:
        cols = []
        for _ in range(dim):
            s = _ar1(n, rho, rng)
            s = (s - s.mean()) / (s.std() + 1e-12)
            cols.append(s)
        sources = np.column_stack(cols)
        x = sources @ axes.T
        return x, sources

    train_x, train_s = sample(n_train)
    test_x, test_s = sample(n_test)
    return PopulationWorld(train_x, train_s, test_x, test_s, axes)


def shuffle_time(x: Array, seed: int) -> Array:
    """Destroy temporal ordering while preserving the zero-lag sample cloud."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(x))
    return np.asarray(x, dtype=float)[order]
