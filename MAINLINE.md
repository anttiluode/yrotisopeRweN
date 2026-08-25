# yrotisopeRweN — main hypothesis compass

This file exists because several mathematically well-paved side roads are gravitational.

The differentiation branch remains useful but is **not** the current destination:

```text
Oja -> one direction
Sanger/GHA -> population differentiation
AMUSE -> temporal differentiation from one lag
```

The main hypothesis is different:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

The current chain is:

```text
BROADCAST
    -> RECEIVER-RELATIVE FIT
    -> COMPOSE
    -> CONTEXT
    -> CONSEQUENCE
    -> ALLOCATE
    -> GROW SPARSE MATRIX
    -> CONTINUE RUNNING WHILE OUTPUT IS EMITTED
    -> ? RECURRENT BROADCAST LOOP
```

Every completed verb has a small falsification gate. The question mark is intentional.

---

# Main-line receipts

## Gate 0 — receiver-relative fit

Receiver-specific fast phase/state can change which temporally structured arrivals are effective. A global oscillation is insufficient. A boring digital phase-feature attacker slightly wins.

Receipt: `results/GATE0.md`.

## Gate 1 — timing can write structure

Delay/path state changes temporal viability; finite structural mass can turn repeated viability into sparse routing.

Receipt: `results/GATE1.md`.

## Gate 2 — coherence says CAN; consequence says KEEP

Timing-identical routes can have opposite downstream consequences. Coherence alone cannot decide which should persist.

Receipt: `results/GATE2.md`.

## Gate 3 — bounded growth becomes allocation

Oja is useful on the main line as one precise demonstration of a primitive principle:

> **correlated growth plus a bound becomes allocation rather than unlimited amplification.**

Do not equate structural mass with Oja mathematically.

Receipt: `results/GATE3.md`.

## Gate 6 — COMPOSE

The same fixed nonlinear bank computes different relations when only fast receiver state changes. An ordinary scalar mode switch ties phase exactly.

Surviving claim:

> **fast receiver state can choose which relation fixed slow structure computes.**

Receipt: `results/GATE6.md`.

## Gate 7 — CONTEXT

Move the state-setting event into the past, let it disappear, insert distractors, then present the same later broadcast. Leftover receiver state changes the later composition. A one-scalar recurrent attacker ties/slightly wins.

Surviving claim:

> **receiver-carried context is the primitive; phase is merely one possible coordinate system.**

Receipt: `results/GATE7.md`.

## Gate 8 — CONSEQUENCE

Transient conjunctions disappear before a scalar consequence arrives. A decaying eligibility trace is the bridge back. Shuffle the trace or remove it and delayed credit collapses.

Surviving claim:

> **delayed consequence needs a surviving address for what happened earlier.**

Receipt: `results/GATE8.md`.

## Gate 9 — finite allocation / reversible consolidation

Allow positive growth evidence but no explicit negative shrink command. Conserved capacity supplies retraction; a small exploratory reserve preserves alternatives after consolidation. Hard pruning freezes; unlimited positive growth accumulates incompatible structure. Signed gradient wins numerically.

Receipt: `results/GATE9.md`.

## Gate 10 — GROWING MATRIX

Remove Gate 9's hand-written rival pairs. Put 36 possible relations in one `6 x 6` field under one global unit capacity budget.

A diffuse matrix grows four useful cells to about `96.8%` of total mass. When the useful pattern moves to four completely disjoint cells, the matrix dissolves and regrows there. Hard prune prevents regrowth; unlimited growth remembers too much; signed global gradient wins.

Surviving claim:

> **positive local utility evidence plus finite shared capacity can grow a sparse effective matrix without being told which structural variables are rivals.**

Receipt: `results/GATE10.md`.

## Gate 11 — CONTINUOUS CELL: output is not a reset

Gate 10 still had an artificial boundary: its data came as isolated samples/trials.

Gate 11 removes that boundary.

Every matrix cell now has a continuously evolving local state:

```text
Q_ij(t) = A_i(t) B_j(t)
Z_ij(t+1) = alpha_ij Z_ij(t) + (1-alpha_ij) Q_ij(t)
```

with fixed heterogeneous `alpha_ij` values. Structural mass `M` still shares one conserved budget, and a separate eligibility state `E` carries delayed credit.

The cell therefore contains three distinct timescales/roles:

```text
Z(t)    local computational state
E(t)    credit-assignment state
M       persistent structural allocation
```

A continuous soma-like readout is thresholded by a separate output observer. Emitting does **not** clear `Z`, `E`, or `M`.

Six seeds, 30,000 uninterrupted timesteps:

```text
continuous cell
phase-1 voltage NMSE       0.01010
phase-2 voltage NMSE       0.00993
phase-1 output F1          0.9551
phase-2 output F1          0.9547
phase-1 useful mass        0.9095
phase-2 useful mass        0.9112
new matrix > .90           8334 +/- 924 stream steps, 6/6 seeds
```

Important kills:

```text
no consequence
    -> phase-2 NMSE 6.4021

shuffled eligibility identity
    -> phase-2 NMSE 0.8724
    -> no .90 reallocation

persistent local state but no explicit eligibility trace
    -> phase-2 NMSE 1.4461
    -> no .90 reallocation

zero local state/eligibility whenever output fires
    -> phase-2 NMSE 0.0774
    -> phase-2 useful mass 0.8314
    -> no .90 reallocation

instantaneous relation cells, no local temporal persistence
    -> phase-2 NMSE 0.0928
    -> phase-2 useful mass 0.7379
    -> no .90 reallocation
```

A boring exact delay-buffer + signed-update attacker is much better:

```text
phase-1 NMSE              0.000113
phase-2 NMSE              0.000114
phase-2 useful mass       0.9931
reallocation              3952 +/- 631 steps
```

So Gate 11 is not an optimizer claim.

The useful decomposition is:

> **local state computes; eligibility remembers credit; structural mass remembers investment. Output is a boundary, not an episode terminator.**

Receipt: `results/GATE11.md`.

---

# What the two biology papers earned — and what they did not

Two papers were deliberately introduced only after the growing-matrix story existed.

### Aizenbud et al. 2026

Their detailed neuron models support the importance of extended dendritic morphology, compartmentalized integration, and nonlinear interactions among coactive synapses. Total dendritic area and long bifurcating paths predict their Functional Complexity Index much better than branch count alone.

Computational lesson used here:

```text
not "more branches = intelligence"

but

extended local integration + nonlinear compartments
can make a single cell's I/O transformation richer
```

That motivated persistent local matrix states, not a literal dendrite simulator.

### Leterrier 2018

The AIS is a specialized boundary between somatodendritic input processing and axonal propagation; it initiates/shapes the action potential, and its composition/morphology can adapt on several timescales.

Computational lesson used here:

```text
continuous internal computation
        -> output boundary
        -> broadcast
```

not

```text
input -> output -> clear the neuron
```

Neither paper establishes our exact equations, mass rule, eligibility trace, or matrix representation.

---

# Differentiation side branch

## Gate 4
Independent Oja points duplicate the strongest covariance mode; Sanger/GHA makes the population divide covariance structure. Explicit PCA wins.

Receipt: `results/GATE4.md`.

## Gate 5
When zero-lag covariance contains no source identity but lag-1 statistics do, AMUSE recovers temporal causes. Shuffle time or equalize memory laws and the advantage disappears.

Receipt: `results/GATE5.md`.

Do not add SOBI unless a future wall specifically requires several lagged statistics.

---

# Current object

The point is no longer well described as one weight vector evaluated once per example.

```text
incoming broadcasts never really stop
        ↓
local relation field is continuously driven
        ↓
local compartment states Z(t) overlap in time
        ↓
continuous readout can emit
        ↓
output leaves the cell

while internally:

Z(t) keeps evolving
E(t) keeps assigning delayed credit
M keeps reallocating finite structural capacity
```

The sparse matrix is therefore becoming a **continuously occupied dynamical structure**, not merely a static mask.

---

# NEXT — make the loop literal, but change only one scaffold

Gate 11 removed the artificial trial reset. It has **not** yet shown a closed recurrent neural loop.

The next clean attack is:

```text
continuous Cell A
      ↓ broadcast
continuous Cell B
      ↓ broadcast
back toward A
```

External signals should enter while recurrent traffic is already circulating. The cells must continue their local dynamics, eligibility, and structural allocation while broadcasts re-enter them.

Do **not** simultaneously remove the known product coordinates. Keep `A_i * B_j` for this gate so a recurrent failure has one interpretation.

Attacks should include:

```text
cut the return path
randomize return timing
reset internal state on output
shuffle delayed eligibility
ordinary small RNN / signed-gradient attacker
```

Only after a recurrent loop survives should the supplied relation coordinate field be attacked.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> finite allocation -> growing sparse matrix -> continuous internal dynamics -> broadcast again. Gate 11 shows the cell need not reset when it emits; the next test is whether several such continuously running cells can form a recurrent loop without losing causal credit or structural plasticity.**
