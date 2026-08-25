# Gate 15 — GENERIC BASIS: structure does not need semantic coordinates

Development receipt, not confirmatory evidence.

## Why this gate

Gate 14 removed the label `peer return`, but each anonymous incoming stream still landed on its own simple matrix coordinate.

That was a large remaining scaffold:

```text
incoming channel i
    -> dedicated structural coordinate i
```

Gate 15 removes that mapping while keeping the two-point recurrent world fixed.

The question is:

> **Can finite consequence-driven growth select useful recurrent computation when every internal structural cell is a generic mixture of all incoming streams rather than a named relation coordinate?**

## Generic internal field

Each point still receives six stable raw streams:

```text
A:
  brief external cue
  four anonymous return/nuisance streams
  one extra nuisance stream

B:
  four anonymous return/nuisance streams
  other nuisance streams
```

As established in Gate 14, one anonymous return stream carries the current peer broadcast and the others are unrelated. Their external channel identities stay stable in this gate so we attack only the **internal coordinate scaffold**.

Instead of giving every raw channel a structural cell, each point receives a fixed random dense projection:

```text
r_k in R^6

u_k(t) = r_k · x(t)
phi_k(t) = tanh(2 u_k(t))
```

Every row is deliberately dense: before normalization every coefficient magnitude is drawn in `[0.5, 1.0]`, with random sign. No internal feature is a raw channel axis.

The default field has 24 features. Their local states are leaky exactly so the rest of the continuous architecture remains unchanged:

```text
Z_k(t+1) = alpha_k Z_k(t) + (1-alpha_k) phi_k(t)
```

All 24 feature cells share one conserved structural budget. Delayed consequence supplies only positive local growth evidence through eligibility; conservation supplies retraction.

So the learned object is now:

```text
raw traffic
   ↓
fixed generic mixed coordinates
   ↓
finite structural mass over those coordinates
   ↓
continuous recurrent output
```

## Main result — stable generic coordinates work

Three development seeds, 10,000 uninterrupted steps.

```text
late cue-free memory accuracy      1.0000 +/- 0.0000
```

The learned mass becomes sparse-ish in the generic feature field:

```text
A effective occupied features      4.83 +/- 0.59
B effective occupied features      3.05 +/- 1.16

A largest feature mass             0.403 +/- 0.084
B largest feature mass             0.599 +/- 0.210
```

Yet no feature is close to a raw channel axis:

```text
A largest |single channel loading| 0.563 +/- 0.024
B largest |single channel loading| 0.562 +/- 0.028
```

The useful recurrent computation therefore does not require an internal coordinate named `cue`, `return`, or `peer`.

## Kill 1 — scramble internal feature addresses every timestep

Keep the same incoming processes and the same fixed random feature functions, but randomly permute which persistent structural cell receives each feature value on every timestep.

Nothing about the instantaneous feature set is removed. Only its persistent internal address is destroyed.

```text
late memory accuracy               0.00283 +/- 0.00284
```

This is the central Gate-15 kill.

It sharpens Gate 14:

```text
Gate 14:
returning traffic needs a stable external address

Gate 15:
useful computation also needs a stable internal address
```

A structural cell can acquire meaning from utility without having a semantic name, but it cannot be relabeled continuously while slow mass and eligibility are trying to accumulate on it.

## Kill 2 — shuffle eligibility

Preserve the stable generic basis but give delayed consequence the wrong earlier feature traces.

```text
late memory accuracy               0.0000
```

The structural distribution remains almost diffuse:

```text
A effective feature count          23.92 / 24
B effective feature count          23.94 / 24
```

So stable coordinates alone are not enough; causal credit still matters.

## Kill 3 — no learning

Leave the random field at uniform structural mass.

```text
late memory accuracy               0.0000
```

A generic basis is potential structure, not a solution by itself.

## Causal lesion — cut the returns after growth

Let the generic feature masses develop, then at step 7,000 remove both current-peer return streams and freeze structural learning.

```text
late memory accuracy               0.0352 +/- 0.0028
```

So the selected generic feature subspace is not merely correlating with the task. Its dependence on recurrent traffic is load-bearing.

## Ablation — local nonlinearity is not required here

Replace

```text
phi_k = tanh(2 r_k·x)
```

with the plain linear random coordinate

```text
phi_k = r_k·x
```

Result:

```text
late memory accuracy               1.0000 +/- 0.0000
```

Therefore Gate 15 does **not** earn nonlinear random features as a requirement.

This is an important negative result. The task itself is essentially a low-dimensional recurrent-state problem, and a stable dense linear change of coordinates is already sufficient.

The nonlinear field remains relevant to the broader COMPOSE branch, but not to this particular recurrence gate.

## Ablation — overcompleteness is not required either

Reduce the field from 24 features to only six dense random features for six raw channels.

```text
late memory accuracy               1.0000 +/- 0.0000
```

So this gate also does **not** earn a large random reservoir.

A square dense random coordinate system is enough in this toy.

## What actually survived

The surviving result is much smaller than the original plan, and stronger for being smaller:

> **A growing recurrent structure does not need hand-designed semantic coordinates. Finite positive-growth allocation can operate in a fixed generic mixed basis. What it needs is persistent addressability: the same internal coordinate must continue to mean the same local computation long enough for eligibility and structural investment to accumulate there.**

Or:

```text
semantic coordinate     unnecessary
large feature bank      unnecessary
nonlinearity here       unnecessary

stable coordinate       necessary
correct eligibility     necessary
recurrent traffic       causally necessary
structural adaptation   necessary
```

## Why this is not a new optimizer result

For the linear ablation,

```text
output preactivation = sum_k M_k (r_k · x)
                     = (sum_k M_k r_k) · x
```

so the system is simply learning an effective direction expressed as finite positive mass over fixed random directions.

A conventional recurrent network with signed trainable weights can parameterize this much more directly and remains the obvious engineering attacker.

Gate 15 is therefore about the **structural interpretation of persistent coordinates**, not expressive power or optimization efficiency.

## What is still scaffolded

- the generic projection basis is fixed at initialization rather than grown;
- external incoming channel identities are stable;
- only two points exist;
- consequence is a supplied global scalar;
- eligibility is explicit;
- recurrent delays are fixed;
- the task has one binary persistent state;
- no topology or physical geometry is grown;
- this is not a biological memory model.

## Next

The coordinate scaffold has now survived a serious removal.

The earlier roadmap said not to expand the network until this happened. It has happened.

The clean next attack is therefore **population growth**, not another internal mechanism:

```text
several continuously running points
        ↓
many stable anonymous broadcasts
        ↓
generic local coordinate fields
        ↓
finite structural capacity at every point
        ↓
which recurrent routes actually acquire mass?
```

The first population world should contain both useful and useless possible loops. A task that needs one temporary state should not cause every point to become recurrent with every other point.

Keep the boring small-RNN attacker in the room.

Raw metrics: `results/gate15_generic_basis_metrics.json`.
