# Gate 9 — ALLOCATE / CONSOLIDATE: useful relations compete for finite capacity

Development receipt, not confirmatory evidence.

## Why this gate

Gates 6–8 finally gave the old growth story a specific object to preserve:

```text
earlier context
    -> transient receiver state
    -> later nonlinear conjunction
    -> local eligibility
    -> delayed consequence
    -> evidence that THIS relation mattered
```

Gate 9 asks the next question:

> **Can positive evidence become persistent allocation when useful relations compete for finite capacity, without making the system unable to change later?**

Geometry is still forbidden.

No path lengths move. No dendrites grow. No source separation occurs.

The only new ingredient is a conserved capacity variable called `mass`.

## World

Gate 8's four state-gated conjunctions are reused:

```text
q00, q01, q10, q11
```

They form two rival families because only two are available under each remembered context:

```text
same-index family: q00 vs q11
crossed family:    q01 vs q10
```

Each family owns exactly one unit of capacity.

So:

```text
m00 + m11 = 1
m01 + m10 = 1
```

Growing one claim necessarily shrinks its rival.

This is the actual resource conflict missing from an unlimited-growth model.

## Phase 1 usefulness

Initially the useful pattern is:

```text
[q00, q01, q10, q11]
 [ 1,   0,   1,   0 ]
```

Positive local growth evidence comes from consequence-modulated eligibility:

```text
eligibility_j = mass_j * conjunction_j
score_j       = mean(error * eligibility_j)
growth_j      = max(score_j, 0)
```

There is deliberately **no explicit negative shrink rule**.

The only way an old claim gets smaller is that a rival grows while the pair budget stays fixed.

A small protected exploratory reserve is kept:

```text
minimum mass per candidate = 0.02
```

## Phase 1 result

Twelve seeds:

```text
mean mass = [0.9795, 0.0204, 0.9796, 0.0205]
useful mass = 0.9795
NMSE = 0.000959 ± 0.000029
```

So repeated consequence has turned positive evidence into a strongly selective but not completely frozen capacity allocation.

## Reversal

After consolidation, usefulness flips:

```text
old: [1, 0, 1, 0]
new: [0, 1, 0, 1]
```

Nothing else changes.

The previously exploratory `2%` alternatives are now the useful relations.

With the conserved budget they start receiving positive utility. Their growth automatically takes capacity away from the old routes.

Across all 12 seeds, new useful mass crosses `0.90` after:

```text
13 epochs
```

and after 120 reversal epochs:

```text
mean mass = [0.0205, 0.9794, 0.0206, 0.9795]
new useful mass = 0.9795
NMSE = 0.000978 ± 0.000033
```

So the same growth-only rule can reverse the consolidated allocation because capacity is conserved and a small exploratory reserve survived.

## Kill 1 — hard consolidation with zero exploratory reserve

Set reserve to zero.

After phase 1, hard pruning produces:

```text
[1, 0, 1, 0]
```

The zero-mass alternatives transmit nothing, leave no eligibility, and therefore receive no positive growth evidence after reversal.

Result:

```text
new useful mass = 0.0000
phase-2 NMSE = 2.0127
```

The system is frozen in its obsolete structure.

This is the cleanest computational role yet found for "exploratory mass":

> **capacity that looks wasteful while the world is stable can be the only route through which a changed world becomes discoverable after consolidation.**

## Kill 2 — unlimited positive growth

Remove conservation entirely. Start every candidate small and let positive evidence only add mass.

Phase 1 is fine:

```text
phase-1 NMSE = 0.000450
```

But the old useful routes never retract.

After reversal the new routes grow too, until effectively all old and new conjunctions remain strong.

Result:

```text
phase-2 NMSE = 1.0063
```

So unlimited growth fails for the opposite reason from zero-reserve consolidation:

```text
zero reserve   -> remembers too rigidly
unlimited mass -> remembers too much
```

Finite conserved capacity creates reallocation between those extremes.

## Kill 3 — remove consequence

Let co-activation energy drive positive growth without downstream task error.

Result:

```text
phase-1 NMSE = 0.8061 mean
```

with high seed variability.

Activity alone does not reliably know which conjunction deserves the limited capacity.

This reprises Gate 2 in a cleaner object:

> **fit/co-activation can say what occurred; consequence is needed to say what capacity should preserve.**

## Kill 4 — shuffle eligibility

Preserve scalar consequence but attach it to the wrong local activity history.

Result:

```text
phase-1 NMSE = 0.4864
```

The capacity allocator therefore still depends on the Gate-8 credit-assignment bridge.

## Boring attacker — signed projected gradient

Allow an ordinary optimizer to use the signed gradient directly, so it can explicitly increase useful weights and decrease harmful ones while respecting the same pair budgets.

It wins easily:

```text
phase-1 NMSE = 0.000053
phase-2 NMSE = 0.000059
```

That is important.

Gate 9 is **not** a claim that positive-only conserved growth is a better optimization algorithm.

Its narrower architectural result is:

> **If local structure is allowed mainly to grow rather than receive precise signed anti-growth commands, conservation can supply the missing retraction: new positive claims automatically take capacity from old ones.**

And the exploratory reserve supplies plasticity after hardening.

## What survived

The main line can now be written more concretely:

```text
BROADCAST
    ↓
RECEIVER-RELATIVE STATE
    ↓
NONLINEAR COMPOSITION
    ↓
CONTEXT PERSISTS
    ↓
ELIGIBILITY
    ↓
DELAYED CONSEQUENCE
    ↓
POSITIVE LOCAL GROWTH EVIDENCE
    ↓
FINITE CAPACITY COMPETITION
    ↓
PERSISTENT ALLOCATION
```

Then when usefulness changes:

```text
EXPLORATORY RESERVE
    ↓
new relation remains sampleable
    ↓
new consequence can reach it
    ↓
new positive growth
    ↓
conservation retracts old allocation
```

This finally joins the old Gate-2 stability/plasticity problem to the newer composition/context/consequence road.

## What this does not show

- structural mass is biologically literal;
- the pairwise budget is the correct capacity geometry;
- 2% is a meaningful biological number;
- positive-only growth is preferable to signed gradient descent;
- morphology/path length is needed;
- the allocation should be permanent physical wiring;
- large networks will exhibit the same clean tradeoff;
- sequence completion or concept formation has been demonstrated.

## What comes next

For the first time I would **not** immediately add another verb.

The complete main hypothesis now has at least one toy implementation for every step:

```text
broadcast
 -> receiver-relative fit
 -> compose
 -> context
 -> consequence
 -> allocate
 -> consolidate/reallocate
```

The next work should attack the *whole chain* rather than append another mechanism.

A good next gate should remove one of the hand-designed conveniences:

- the explicit two-family capacity partition;
- the supplied binary context code;
- the known fixed conjunction bank;
- the isolated trial structure;
- or the clean scalar consequence.

And the signed projected-gradient attacker should remain in the room.

Only if the chained system survives a less hand-designed world should geometry/path length return as a possible physical parameterization of the persistent allocation.

Raw metrics: `results/gate9_capacity_metrics.json`.
