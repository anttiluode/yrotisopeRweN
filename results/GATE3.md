# Gate 3 — Oja under the oscillating point

Development receipt, not confirmatory evidence.

## Why this gate

The oscillating-point line started from a point with hidden internal state. Phase later became one cheap coordinate of that state. Gate 3 asks where Oja's rule belongs in that picture.

The precise connection is narrower than "a mass budget is Oja."

Oja's rule is

```text
y = w^T u
Delta w = eta * y * (u - y w)
```

The second term is not merely numerical hygiene. Plain Hebbian reinforcement has no finite fixed norm. Oja's `-y^2 w` term constrains the weight norm, and that constraint turns growth into selection of a principal direction.

A fixed structural-mass budget is **analogous in spirit** because it forces competition for finite resource, but it is not mathematically the same update.

## Phase as a tiny submatrix

Lift local arrival energy into an in-phase/quadrature pair:

```text
u(t) = sqrt(e(t)) [cos(phi(t)), sin(phi(t))]
```

A unit vector

```text
w = [cos(theta), sin(theta)]
```

is therefore a preferred phase axis. Oja can rotate that axis toward the dominant phase-conditioned energy while keeping its norm finite.

This gives a concrete interpretation of "the matrix beneath the point": even a 2-D hidden subspace can contain a slowly learned orientation, while fast phase determines where the current arrival lies in that subspace.

## World

Gate 0's two hidden sources are reused. They occupy opposite phases (`0` and `pi`) of one supplied oscillator and are summed into one scalar mixture.

First 60% trains Oja; final 40% is held out.

Twelve seeds.

## Result

| quantity | result |
|---|---:|
| plain Hebb norm failure | 12 / 12 runs hit the `1e6` guard |
| plain Hebb max norm | `1,002,307` mean (guarded) |
| Oja final norm | `1.000059 ± 0.000027` |
| Oja phase-axis alignment | `0.999929 ± 0.000078` |

So the normalization term is load-bearing: the same positive-feedback skeleton that explodes under plain Hebb settles onto a stable phase axis under Oja.

## But Oja learns an axis, not two phase identities

Covariance cannot distinguish `theta` from `theta + pi`; they are the same axis with opposite sign.

If the two downstream outputs are kept linear,

```text
y0 = x cos(phi - theta)
y1 = -y0
```

then they are exact duplicates:

| arm | source recovery | output duplication |
|---|---:|---:|
| linear opposite phase axes | `0.7017 ± 0.0124` | `1.0000` |

That is the PCA/Oja limitation in this tiny phase world.

## Local nonlinearity becomes load-bearing

Use the same Oja-learned axis, but let two receivers implement complementary **nonnegative** phase windows at `theta` and `theta + pi`:

```text
g0 = ((1 + cos(phi-theta))/2)^3
g1 = ((1 + cos(phi-theta-pi))/2)^3
```

No new phase learning is added.

Held-out result:

| arm | source recovery | output duplication |
|---|---:|---:|
| Oja axis + nonlinear complementary gates | **`0.9944 ± 0.0006`** | `0.0162` |

Move both hidden sources to the same phase and recovery falls to `0.3979`.

So the win still depends on real phase diversity in the world.

## What this means

The cleanest decomposition is now:

```text
FAST PHASE
where is the current arrival in a local oscillatory coordinate system?

OJA / NORMALISED HEBB
which phase axis has persistently carried structured energy?

LOCAL NONLINEARITY
which end / conjunction of that axis is currently effective?

SLOW STRUCTURE
which repeatedly useful relations deserve mass and wiring?
```

Oja is therefore not "the oscillation rule." It is a candidate slow selector **inside** the hidden state beneath the point.

The important mathematical lesson is:

> **normalisation turns Hebbian growth from amplification into selection.**

And the equally important limitation is:

> **one Oja unit selects one covariance direction. It does not by itself create multiple independent listeners or a null.**

That lines up with the separate Gate-3-growth result supplied by Claude: per-edge local phase alignment naturally grows a matched filter but not a distributed null. Multiple differentiated listeners need an across-unit mechanism such as Sanger-style deflation / lateral decorrelation, or a richer nonlinear objective.

## What this does not show

- biological synapses literally compute the phase lift above;
- a simplex mass budget is literally Oja's rule;
- phase should be added to ordinary AI;
- Oja plus rectification is a new source-separation algorithm;
- local nonlinearity solves Claude's shared-carrier null problem.

The digital phase-feature attacker from Gate 0 remains the simpler computational implementation.

## Next

The next gate should put **several Oja/Sanger-like points** under one finite-resource population and ask whether they differentiate rather than all learning the same coherent mode.

That is the exact place where three threads meet:

```text
Oja          -> one stable direction
Sanger       -> several competing directions
phase        -> fast relational coordinate
mass/growth  -> persistent structural commitment
```

The kill condition is simple: if lateral decorrelation / deflation adds nothing, then the population story is decoration and one matched filter is all the system naturally wants to become.
