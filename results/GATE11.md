# Gate 11 — CONTINUOUS CELL: the loop does not reset

Development receipt, not confirmatory evidence.

## Why this gate

Gate 10 still learned from isolated arrays. Even though the structural matrix persisted across epochs, the computational world itself remained trial-like.

The biological prompt for Gate 11 was narrower and more useful than "simulate a neuron."

Aizenbud et al. (PNAS, 2026) show that single-neuron functional complexity is strongly associated with dendritic surface/extent and branching organization, and discuss semi-independent dendritic integration plus nonlinear interactions among coactive excitatory synapses. Leterrier (J. Neurosci., 2018) emphasizes that the axon initial segment (AIS) is a specialized output boundary that initiates/shapes action potentials and whose excitability and morphology can themselves adapt.

The computational translation used here is deliberately modest:

```text
internal relation field
    keeps evolving

local state
    does not disappear when output occurs

eligibility
    persists on another timescale

structural mass
    persists on a slower timescale

output threshold
    is a boundary/readout, not an "end of trial" signal
```

This is **not** a detailed dendrite or AIS model.

## One uninterrupted stream

There are no examples and no trial resets.

At every timestep two six-dimensional broadcasts arrive:

```text
A(t), B(t)
```

The same 36 candidate relations from Gate 10 provide local drive:

```text
Q_ij(t) = A_i(t) B_j(t)
```

But now each cell is a persistent leaky compartment:

```text
Z_ij(t+1) = alpha_ij Z_ij(t) + (1-alpha_ij) Q_ij(t)
```

The `alpha_ij` values are fixed and heterogeneous (`0.65 ... 0.96`). This is only a temporal-compartment abstraction; no morphology is fitted or grown.

Structural mass remains globally conserved:

```text
sum_ij M_ij = 1
M_ij >= 0.001
```

The somatic-like readout is continuous:

```text
V(t) = sum_ij M_ij Z_ij(t)
```

and a fixed AIS-like observer emits when:

```text
V(t) > threshold
```

Crucially, output does **not** reset `Z`, eligibility, or mass.

## Delayed consequence in the stream

The useful four-cell pattern changes halfway through the same stream, with no reset of any state.

A local eligibility trace runs continuously:

```text
E(t+1) = lambda E(t) + Z(t) * M(t)
```

A scalar error arrives eight steps after the activity it evaluates. Positive local growth evidence is accumulated from the delayed consequence and eligibility. Global conservation supplies retraction exactly as in Gate 10.

So several past events can coexist in the same eligibility state. There is no clean credit-assignment boundary.

## Main result

Six seeds, 30,000 uninterrupted timesteps per seed.

| quantity | phase 1 | phase 2 after world change |
|---|---:|---:|
| voltage NMSE | `0.01010 ± 0.00135` | `0.00993 ± 0.00138` |
| useful matrix mass | `0.90947 ± 0.00284` | `0.91121 ± 0.00467` |
| thresholded output F1 | `0.9551 ± 0.0071` | `0.9547 ± 0.0080` |

The new disjoint matrix exceeds `0.90` useful mass after:

```text
8334 ± 924 continuous timesteps
```

in all 6/6 seeds.

So Gate 10's growing matrix survives removal of the trial boundary.

## Kill 1 — no consequence

Allow continuous activity to drive growth but remove task consequence.

```text
phase-1 NMSE     5.1639
phase-2 NMSE     6.4021
final new mass   0.0040
```

Continuous activity plus scarcity still does not supply purpose.

## Kill 2 — shuffle cell identity in eligibility

Give the delayed error the wrong matrix-cell traces.

```text
phase-1 NMSE     0.8639
phase-2 NMSE     0.8724
final new mass   0.1111
```

No run reaches the `0.90` adaptation criterion.

So continuous delayed consequence still needs causal addressability.

## Kill 3 — dendritic state is not enough to replace eligibility

Remove the explicit longer eligibility trace and let the current persistent compartment state be the only local memory available when delayed consequence arrives.

```text
phase-1 NMSE     0.8344
phase-2 NMSE     1.4461
final new mass   0.1475
```

The persistent local computation state and the credit-assignment trace are therefore **not the same variable** in this toy.

This sharpens the matrix-under-the-point decomposition:

```text
Z(t)    computational state
E(t)    credit state
M       structural state
```

## Kill 4 — treat output as "trial over"

Whenever the thresholded output fires, zero the local compartment state and eligibility.

```text
phase-1 NMSE     0.1001
phase-2 NMSE     0.0774
phase-2 mass     0.8314
```

No seed reaches `0.90` new-pattern mass within the available second half.

This is the most direct Gate-11 result:

> **An output event should not be interpreted as a reset of the internal computation.**

The model can emit while the slower local dynamics continue.

This is an architectural inference for the toy, not a claim that biological spikes literally preserve every dendritic variable unchanged.

## Ablation — instantaneous compartments

Set every local decay to zero so each relation cell contains only the current product.

```text
phase-1 NMSE     0.0946
phase-2 NMSE     0.0928
phase-2 mass     0.7379
```

The system still has a useful instantaneous computation, but it no longer reaches the `0.90` reallocation criterion.

Thus, in this delayed continuous-credit world, persistent local state materially helps. This does **not** show that the particular heterogeneous time constants are optimal or biologically correct.

## Attacker

A boring digital model stores the exact old local state in a delay buffer and uses an ordinary signed update when the delayed error arrives.

```text
phase-1 NMSE     0.000113
phase-2 NMSE     0.000114
phase-1 mass     0.99235
phase-2 mass     0.99312
adaptation       3952 ± 631 steps
```

It wins easily.

Good.

Gate 11 is not an optimizer claim.

## What the two papers actually changed

### From Aizenbud et al.

The paper does **not** say "use a leaky matrix." What it supports is the importance of spatially extended, compartmentalized, nonlinear dendritic integration. In their morphology analysis, total dendritic area is a much stronger single predictor of FCI than branch count, and long bifurcation paths also matter. Their discussion emphasizes semi-independent dendritic subregions and stronger combinatorial nonlinear interactions under NMDA-mediated integration.

That motivated us to stop equating complexity with "number of branches" and instead give the growing matrix persistent local computational state.

### From Leterrier

The paper does **not** say "never reset a software state." It establishes the AIS as a specialized boundary between somatodendritic computation and axonal propagation, with both rapid modulation and slower activity-dependent morphological plasticity.

That motivated the architectural separation:

```text
continuous internal computation
        -> output boundary
        -> broadcast
```

rather than:

```text
input -> output -> clear everything
```

## What survived

The current object is now:

```text
continuous broadcasts
        ↓
persistent local nonlinear relation states Z(t)
        ↓
continuous somatic readout
        ↓
output event / broadcast boundary

while simultaneously:

Z(t) -> eligibility E(t) -> delayed consequence -> positive structural growth
                                         ↓
                            conserved matrix mass M
```

The three states have distinct jobs:

> **local state computes; eligibility remembers credit; structural mass remembers investment.**

And none of them need to stop when the cell emits.

## What is still missing

This is still not a literal closed recurrent neural loop.

Gate 11 removes the artificial **trial reset**, but the emitted output is not yet fed into another continuously running cell and back again.

That is now a more natural next attack than adding more dendritic detail:

```text
Cell A continuous matrix
    -> broadcast
Cell B continuous matrix
    -> broadcast
back toward A
```

with external signals entering while the recurrent traffic never stops.

The known product coordinates `A_i*B_j` are also still supplied. One of these two cheats should be removed next, but not both at once.

## Sources that motivated the abstraction

- Ido Aizenbud et al., **Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons**, PNAS (2026), DOI: 10.1073/pnas.2533168123.
- Christophe Leterrier, **The Axon Initial Segment: An Updated Viewpoint**, Journal of Neuroscience 38(9):2135-2145 (2018), DOI: 10.1523/JNEUROSCI.1922-17.2018.

Raw metrics: `results/gate11_continuous_loop_metrics.json`.
