# Gate 4 — population differentiation

Development receipt, not confirmatory evidence.

## Why this gate

Gate 3 established one narrow thing: a normalized-Hebbian/Oja point can settle onto one stable covariance axis. It did **not** establish that a population of such points divides the world into several different listeners.

The next missing computational verb is therefore deliberately small:

> **differentiate**

Do several finite-growth points learn different information, or do they all become copies of the strongest mode?

No mass growth, geometry, utility, phase learning, ICA contrast, or task objective is allowed into this gate. All four points see the same input.

## World A — four real covariance modes

Four independent latent processes are given distinct variances and mixed by one random orthogonal matrix. Zero-lag covariance is sufficient to identify the axes, so explicit PCA is the correct digital attacker.

Two developmental arms:

```text
INDEPENDENT OJA
four normalized-Hebbian points
same input
no between-point interaction

SANGER / GHA
same local Oja-like skeleton
plus ordered deflation of directions already claimed by earlier points
```

Twelve-seed held-out result:

| arm | weight duplication | source recovery | strong distinct claims |
|---|---:|---:|---:|
| independent Oja points | **1.0000** | 0.2735 | 1.00 / 4 |
| **Sanger / GHA population** | **0.0368** | **0.9782** | **3.92 / 4** |
| explicit PCA attacker | — | **0.9990** | — |

Axis recovery:

| arm | mean axis recovery |
|---|---:|
| Sanger / GHA | `0.9802 ± 0.0599` |
| explicit PCA | `0.9993 ± 0.0005` |

So the first question has a clean answer.

> **Without a between-point term, independently normalized Hebbian points collapse onto the same strongest covariance mode. Sanger-style deflation adds a genuinely new population operation: different points divide the available covariance structure.**

The explicit eigendecomposition remains cleaner. Good.

## Kill world — orthogonality cannot create information

The seductive mistake here is to celebrate four different weight vectors even when the world contains only one informative direction.

So the second world is exactly rank one.

Sanger is free to produce any internal orthogonal directions it likes, but the held-out output covariance has:

```text
effective information rank = 1.0000
```

Different axes therefore do not count as different information. The data rank remains one.

## Boundary world — temporal diversity that this gate cannot use

The most important control is not really a kill. It marks the edge of the mechanism.

Four sources are constructed with:

```text
same mean
same variance
mutually orthogonal zero-lag covariance
```

but very different temporal laws. Their lag-1 autocorrelations have mean spread:

```text
1.1410
```

So there is strong information in history, but none in the zero-lag covariance basis that Oja/Sanger/PCA is designed to exploit.

Result:

| arm | source recovery | weight duplication |
|---|---:|---:|
| Sanger / GHA | 0.7440 | 0.0200 |
| explicit PCA | 0.7643 | — |

This is exactly why low duplication is not itself a result. Sanger produces a beautiful nearly orthogonal basis, but because the covariance is spherical that basis is arbitrary with respect to the true temporal sources.

The gate therefore **does not** get to claim temporal source identification.

That missing operation is now isolated cleanly:

> **When zero-lag covariance cannot distinguish the causes but their histories can, a temporal statistic has to enter.**

That is the point at which AMUSE/SOBI may later earn their way into the machine. They are not installed here.

## What survived

The current ladder is now sharper:

```text
ONE OJA POINT
normalized growth selects one covariance direction

SEVERAL INDEPENDENT OJA POINTS
all select the same strongest direction

BETWEEN-POINT DEFLATION
population differentiates and divides covariance structure

EQUAL-COVARIANCE / DIFFERENT-HISTORY WORLD
differentiation alone is insufficient
```

So Gate 4 adds one sentence to the repo:

> **Normalisation makes one point selective; competition/deflation makes a population diverse.**

## What this does not show

- Sanger/GHA is a novel algorithm;
- cortical populations literally implement ordered Sanger deflation;
- orthogonal responses are automatically meaningful;
- source independence has been learned;
- temporal structure has been exploited;
- phase, mass, geometry, or utility are necessary for this differentiation gate.

In fact those mechanisms were deliberately removed.

## Next

Do **not** recombine the whole architecture yet.

The next scientific fork is now explicit:

1. If the next question is **history-identifiability**, construct a world with matched zero-lag covariance and ask whether one delayed statistic is sufficient. That is where AMUSE belongs.
2. If the next question is **non-Gaussian source identity**, keep covariance ambiguous and add a higher-order/nonlinear learning rule. That is where ICA-like machinery belongs.
3. Only after one of those earns a distinct capability should it be rejoined with phase gating, utility, and structural commitment.

Raw metrics: `results/gate4_population_metrics.json`.
