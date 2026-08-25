# Gate 5 — one lag gets one chance

Development receipt, not confirmatory evidence.

## Why AMUSE is allowed into the repo now

Gate 4 did **not** add AMUSE merely because delayed covariance sounded related to oscillations or Takens.

It first constructed a boundary world in which:

```text
zero-lag covariance contains no source identity
but
temporal autocorrelation does
```

That is the exact missing operation AMUSE is designed to attack.

So Gate 5 asks only:

> **Can one delayed covariance matrix identify temporal modes that Oja/Sanger/PCA cannot identify at lag zero?**

Nothing else moves. No mass, geometry, utility, phase learning, nonlinear ICA contrast, or prediction loss.

## World

Gate 4's lag-only world is reused.

Four hidden oscillatory sources are constructed to have exactly equal zero-lag sample covariance. They are mixed by a random orthogonal matrix.

Across 12 seeds the observed covariance differs from identity by only:

```text
2.71e-15  Frobenius norm
```

So PCA has no privileged source basis.

But the four sources have strongly different lag-1 autocorrelations. After whitening, the one-lag covariance has mean eigenvalue spread:

```text
1.1411
```

That is the only asymmetry AMUSE receives.

## Algorithm

The implementation is intentionally tiny:

```text
x(t)
  ↓
center + whiten using C(0)
  ↓
z(t)
  ↓
C(1) = E[z(t) z(t-1)^T]
  ↓
symmetrize for this real stationary toy
  ↓
one eigendecomposition
  ↓
recovered temporal axes
```

No higher-order statistics.

No nonlinearity.

No task labels.

## Result

Twelve-seed held-out source recovery:

| arm | recovery |
|---|---:|
| PCA | `0.7643 ± 0.0726` |
| Sanger / GHA | `0.7440 ± 0.0545` |
| **AMUSE, tau=1** | **`0.999995 ± 0.000005`** |

So one delayed matrix is sufficient in this world.

This is the clean interpretation:

> **The causes are not distinguished by what varies most now. They are distinguished by how the present relates to one step of history.**

That is a new operation relative to Gate 4.

## Kill 1 — destroy time, keep the same sample cloud

Shuffle the training rows before fitting AMUSE.

This preserves the zero-lag distribution/covariance but destroys adjacency.

Recovery falls to:

```text
0.7872 ± 0.0616
```

So the gain is not coming from whitening or from an accidental static rotation.

## Kill 2 — give every source the same memory law

Four independent AR(1) sources are given the same autocorrelation coefficient and mixed through a random orthogonal basis.

Now one-lag covariance does not contain a stable identity for which source is which.

AMUSE recovery falls to:

```text
0.7940 ± 0.0437
```

Again, this is the desired failure.

## What survived

The Gate-3/4/5 ladder is now unusually clean:

```text
OJA
one point selects one zero-lag covariance direction

SANGER / GHA
several points divide zero-lag covariance directions

AMUSE
when zero-lag covariance is ambiguous,
one delayed covariance can identify sources
if their one-step temporal fingerprints differ
```

So the word **history** has finally acquired a precise computational meaning in this repo.

Not memory in general.

Not a Takens manifold by itself.

Not an oscillation by itself.

A particular measurable fact:

> **a delayed relation can contain source identity that the instantaneous state does not.**

## What this does not show

- one lag is generally sufficient;
- AMUSE is biologically implemented by neurons;
- Takens delay embedding and AMUSE are the same operation;
- phase is required for temporal identification;
- AMUSE beats modern BSS methods;
- a temporal source is automatically useful to a task;
- this solves Claude's shared-carrier null problem.

The world was deliberately constructed so one lag has distinct eigenvalues. That is why AMUSE wins almost perfectly.

## Next kill before SOBI

Do not add several lags yet.

First construct a world where **lag 1 collides**: at least two sources should have the same lag-1 statistic while differing at later lags.

Then ask:

```text
AMUSE(tau=1)
should fail

AMUSE(best single tau)
may depend precariously on lag choice

multi-lag joint diagonalization
only then gets a chance
```

If several lags actually add robustness/recovery, SOBI earns its place.

If one well-chosen lag still solves everything, keep AMUSE and leave SOBI out.

Raw metrics: `results/gate5_amuse_metrics.json`.
