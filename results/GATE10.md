# Gate 10 — GROWING MATRIX: remove the hand-written rivals

Development receipt, not confirmatory evidence.

## Why this gate

Gate 9 still contained a large piece of scaffolding.

It was told:

```text
q00 competes with q11
q01 competes with q10
```

That made the stability/plasticity result clean, but it also meant the experimenter had already supplied the competition topology.

Gate 10 removes that topology.

The question is:

> **Can a whole field of possible relations allocate itself under one finite material budget, using only positive local growth evidence from consequence, without being told which cell is whose rival?**

This is the first sense in which the repo now contains a literal **growing matrix** rather than a few hand-paired structural variables.

It is still a computational abstraction. No dendrites or physical geometry are being simulated.

## World

Two six-dimensional broadcasts arrive:

```text
A = [a0 ... a5]
B = [b0 ... b5]
```

A fixed local nonlinear field exposes every pairwise conjunction:

```text
Q_ij = A_i * B_j
```

so there are:

```text
6 x 6 = 36
```

candidate relation cells.

Initially every cell has equal structural mass.

All 36 cells share **one** conserved budget:

```text
sum_ij M_ij = 1
```

There are no row budgets, column budgets, pairs, families, or supplied rival sets.

A tiny reserve remains available in every cell:

```text
M_ij >= 0.001
```

The learning primitive remains intentionally weak:

```text
earlier cell activity
    -> decaying eligibility

later scalar consequence
    -> positive growth evidence only

positive growth anywhere
    -> global conservation renormalizes the whole matrix
```

There is no explicit local instruction saying "shrink this obsolete cell."

## Phase 1

Only four of the 36 relations are useful:

```text
(0,0)  (1,3)  (4,2)  (5,5)
```

The desired total matrix budget is split equally between them.

Across 12 seeds:

```text
held-out NMSE            0.001158 +/- 0.000016
mass on useful cells     0.96795
```

Seed 0 finishes approximately as:

```text
.242 .001 .001 .001 .001 .001
.001 .001 .001 .242 .001 .001
.001 .001 .001 .001 .001 .001
.001 .001 .001 .001 .001 .001
.001 .001 .242 .001 .001 .001
.001 .001 .001 .001 .001 .242
```

So one shared pool is enough to create a sparse matrix without being told which irrelevant cell should lose mass when a useful one grows.

## Reversal

Now replace the useful structure with a **completely disjoint** four-cell pattern:

```text
(0,4)  (2,1)  (3,5)  (5,0)
```

Nothing marks these cells as the "alternatives" to the old four.

They are simply tiny surviving cells in the same matrix.

Across 12 seeds:

```text
new-pattern mass > 0.90 after 17.08 +/- 0.28 epochs

final new-pattern mass       0.96771
held-out phase-2 NMSE        0.001171 +/- 0.000017
```

Seed 0 ends approximately as:

```text
.001 .001 .001 .001 .242 .001
.001 .001 .001 .001 .001 .001
.001 .242 .001 .001 .001 .001
.001 .001 .001 .001 .001 .242
.001 .001 .001 .001 .001 .001
.242 .001 .001 .001 .001 .001
```

The old sparse matrix has effectively disappeared and a new sparse matrix has grown elsewhere.

## Kill 1 — remove consequence

Let cells grow from co-activation alone.

Across 12 seeds:

```text
held-out NMSE               4.6094
mass on truly useful cells  0.0843
```

The finite budget still creates competition, but without consequence it has no reason to allocate material to the relations that matter.

So:

> **scarcity creates selection pressure; it does not supply purpose.**

## Kill 2 — shuffle eligibility

Preserve the later consequence but pair it with the wrong earlier cell traces.

```text
held-out NMSE            0.8819
mass on useful cells     0.1178
```

So the delayed consequence must remain causally addressed to the relation that actually occurred.

## Kill 3 — hard consolidation with zero reserve

Train phase 1 with no reserve, then prune every low-mass cell to exactly zero.

Switch to the disjoint phase-2 target.

Because eligibility is activity times current structural mass, the dead cells produce no trace and receive no positive growth evidence.

Across all 12 seeds:

```text
new useful mass          0.0000
phase-2 NMSE             1.9928
```

This is the same stability/plasticity failure as Gate 9, but now over a whole matrix rather than supplied pairs.

## Kill 4 — unlimited positive growth

Remove conservation.

Old useful cells can remain large while new useful cells also grow.

After reversal:

```text
phase-2 NMSE             1.0310
```

Again the failure is opposite to hard pruning:

```text
hard prune
    -> remembers too rigidly

unlimited positive growth
    -> remembers too much

finite conserved matrix + tiny reserve
    -> reallocates
```

## Attacker

Ordinary signed projected gradient is allowed to grow and retract every cell directly.

It solves both phases essentially exactly:

```text
phase-1 NMSE    2.9e-28
phase-2 NMSE    7.9e-29
```

So Gate 10 is **not** an optimizer claim.

## What survived

The hand-written rivalry topology from Gate 9 was unnecessary in this world.

A stronger architectural statement now survives:

> **A dense field of potential relations can grow into a sparse effective matrix when positive local utility evidence acts under one conserved global capacity budget. A small distributed reserve lets that matrix dissolve and regrow somewhere else when utility changes.**

This is the current computational analogue of "growing structure."

Not:

```text
grow a dendrite because biology has dendrites
```

but:

```text
many possible local relations
        ↓
finite material / capacity
        ↓
useful activity claims more of it
        ↓
the effective matrix becomes sparse
        ↓
changed consequence moves the material elsewhere
```

## What this still does not show

- the conjunction basis itself can emerge;
- the 36 candidate cells are physical dendritic branches;
- global normalization is biologically local;
- a real continuous stream can assign these credits cleanly;
- context and consequence can be discovered without trial scaffolding;
- the system scales;
- this beats ordinary optimization.

The largest remaining cheat is now obvious:

> **the candidate relation matrix is still handed in as all products `A_i * B_j`.**

So the next attack should not add another biological mechanism.

Either:

1. replace the known product matrix with a small generic nonlinear local field and ask whether useful cells can be selected/grown; or
2. keep the product field but remove isolated trials and run the whole chain continuously.

Metrics: `results/gate10_growing_matrix_metrics.json`.
