# yrotisopeRweN — main hypothesis compass

This file exists because several well-paved side roads are gravitational.

The differentiation branch remains useful but is **not** the current destination:

```text
Oja -> Sanger/GHA -> AMUSE
```

The main hypothesis is:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

The main chain now reads:

```text
BROADCAST
    -> RECEIVER-RELATIVE FIT
    -> COMPOSE
    -> CONTEXT
    -> CONSEQUENCE
    -> ALLOCATE
    -> GROW SPARSE MATRIX
    -> KEEP RUNNING WHILE OUTPUT IS EMITTED
    -> RECURRENT TRAFFIC
    -> GROW THE RECURRENT LOOP
```

Every arrow above has at least one deliberately small falsification gate.

---

# Main-line receipts

## Gate 0 — receiver-relative fit

Receiver-specific fast state can alter which temporally structured arrivals are effective. A global oscillation is insufficient. A boring digital phase-feature attacker slightly wins.

Receipt: `results/GATE0.md`.

## Gate 1 — timing can write structure

Delay/path state changes temporal viability; finite structural mass can turn repeated viability into sparse routing.

Receipt: `results/GATE1.md`.

## Gate 2 — coherence says CAN; consequence says KEEP

Timing-identical routes can have opposite downstream effects. Coherence alone cannot say which should persist.

Receipt: `results/GATE2.md`.

## Gate 3 — bounded growth becomes allocation

Oja is useful on the main line mainly as one exact example of a primitive principle:

> **correlated growth plus a bound becomes allocation rather than unlimited amplification.**

Do not equate structural mass with Oja mathematically.

Receipt: `results/GATE3.md`.

## Gate 6 — COMPOSE

The same fixed nonlinear bank computes different relations when only fast receiver state changes. An ordinary scalar mode switch ties phase exactly.

> **fast receiver state can choose which relation fixed slow structure computes.**

Receipt: `results/GATE6.md`.

## Gate 7 — CONTEXT

Move the state-setting event into the past, let it disappear, insert distractors, then present the same later broadcast. Leftover receiver state changes the later composition. A one-scalar recurrent attacker ties/slightly wins.

> **receiver-carried context is the primitive; phase is merely one coordinate system.**

Receipt: `results/GATE7.md`.

## Gate 8 — CONSEQUENCE

Transient conjunctions disappear before scalar consequence arrives. A decaying eligibility trace is the bridge back. Shuffle the trace or remove it and delayed credit collapses.

> **delayed consequence needs a surviving address for what happened earlier.**

Receipt: `results/GATE8.md`.

## Gate 9 — finite allocation / reversible consolidation

Positive growth evidence is allowed but there is no explicit negative shrink command. Conserved capacity supplies retraction; a small exploratory reserve preserves alternatives. Hard pruning freezes; unlimited positive growth accumulates incompatible structure. Signed gradient wins numerically.

Receipt: `results/GATE9.md`.

## Gate 10 — GROWING MATRIX

Remove hand-written rival pairs. Put 36 possible relations in one `6 x 6` field under one conserved capacity budget.

A diffuse matrix grows four useful cells to about `96.8%` of total mass. When utility moves to four disjoint cells, the matrix dissolves and regrows there.

> **positive local utility evidence plus finite shared capacity can grow a sparse effective matrix without being told which structural variables are rivals.**

Receipt: `results/GATE10.md`.

## Gate 11 — CONTINUOUS CELL

Remove the trial boundary. Every matrix cell now has a continuously evolving local state `Z(t)`, a separate eligibility state `E(t)`, and persistent structural mass `M`.

Output is observed through a separate boundary and does **not** clear the internal state.

Six seeds, 30,000 uninterrupted steps:

```text
phase-1 voltage NMSE       0.01010
phase-2 voltage NMSE       0.00993
phase-1 output F1          0.9551
phase-2 output F1          0.9547
phase-1 useful mass        0.9095
phase-2 useful mass        0.9112
```

Important decomposition:

```text
Z(t)    computational state
E(t)    credit state
M       structural investment
```

> **local state computes; eligibility remembers credit; structural mass remembers investment. Output is a boundary, not an episode terminator.**

Receipt: `results/GATE11.md`.

## Gate 12 — RECURRENT TRAFFIC

Freeze structural matrices so recurrence itself gets the blame or credit.

A brief cue enters only Cell A. A broadcasts to B; B broadcasts back to A. The cue disappears, distractors continue, and later an opposite cue must overwrite the circulating state.

Twelve seeds:

```text
full A <-> B loop
first cue-free hold accuracy      1.0000
second hold after overwrite       1.0000
A mean state                      +0.9068 -> -0.9068

cut B -> A return
hold accuracy                     0.0000
state                             ~0

scramble return timing
first hold                        1.0000
second overwrite                  0.0000
old state keeps resurfacing

low loop gain
hold accuracy                     0.0000
```

Important ablation: make every local matrix compartment instantaneous. The recurrent pair still holds and overwrites perfectly.

So Gate 11 and Gate 12 describe **different places state can live**:

```text
inside a point
between points in recurrent traffic
```

A one-scalar recurrent attacker also solves the task perfectly.

> **recurrent state is the earned primitive; the matrix is not required for this toy memory.**

Receipt: `results/GATE12.md`.

## Gate 13 — GROW THE LOOP

Turn structural growth back on. Both cells begin with completely diffuse `6 x 6` mass (`1/36` per cell).

Brief alternating cues enter A. In the memory world, desired state must persist for the whole cue-free interval. Delayed consequence reaches both cells only through their own eligibility traces.

Six seeds, 15,000 uninterrupted steps:

```text
memory-required world
late cue-free accuracy            1.0000
A direct-cue mass                 0.5508
A B->A return mass                0.4152
B A->B forwarding mass            0.9650
closed-loop mass                  0.4152
first rolling >.90 memory         1560 +/- 85 steps
```

Kills:

```text
no learning
late memory                       0.0000
closed-loop mass                  0.0278

shuffled eligibility
late memory                       0.0000
closed-loop mass                  0.0234
```

Causal control: use the same cues and same available feedback, but require output only while the cue is physically present. Persistence is useless.

```text
no-memory world
A direct-cue mass                 0.9231
A return mass                     0.0020
B forwarding mass                 0.1367
closed-loop mass                  0.0020
```

B can grow a partial echo because it correlates with the cue, but A does not invest in the return leg, so no functional loop closes.

> **feedback availability alone does not force recurrence. When persistence is useful, finite consequence-driven growth reallocates matrix capacity into a closed A -> B -> A path; when persistence is unnecessary, A becomes almost purely feedforward.**

Receipt: `results/GATE13.md`.

---

# Biology papers: what they earned and what they did not

Aizenbud et al. (PNAS 2026) motivated the distinction between simple branch count and extended, compartmentalized, nonlinear local integration. Leterrier (J. Neurosci. 2018) motivated separating continuously evolving somatodendritic computation from an output/broadcast boundary.

They did **not** establish our matrix equations, eligibility rule, mass conservation, recurrent-learning rule, or any hippocampal interpretation.

The current recurrent gates are deliberately generic. They test recurrent traffic as a computational primitive, not a specific brain circuit.

---

# Differentiation side branch

Gate 4: independent Oja points duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: when zero-lag covariance contains no identity but lag-1 statistics do, AMUSE recovers temporal causes. Shuffle time or equalize temporal laws and it fails.

Do not continue to SOBI unless a future wall specifically requires several lags.

---

# Current object

The point-under-the-point is now better described as a continuously occupied structure embedded in a network:

```text
incoming broadcasts
      ↓
local nonlinear state Z(t)
      ↓
continuous output / broadcast
      ↓
other continuously running points
      ↓
returning traffic

while in parallel:

Z(t) -> eligibility E(t) -> delayed consequence -> structural mass M
```

Structural growth can now affect not only what a cell computes locally, but whether **network traffic closes into a persistent recurrent path**.

---

# NEXT — remove the named recurrent coordinate, not add more neurons

Gate 13 still knows that matrix coordinate `(1,0)` means:

```text
peer broadcast x constant carrier
```

That is now the largest cheat.

Do **not** immediately scale to a many-region recurrent network or invent a hippocampal analogue.

Next clean attack:

```text
several generic incoming channels
random / generic local nonlinear coordinates
one of them happens to carry useful returning traffic
others carry distractors / stale / irrelevant traffic
        ↓
finite consequence-driven growth
        ↓
can the matrix discover which returning traffic deserves structural capacity?
```

Controls:

```text
memory-required vs no-memory world
shuffle incoming channel identities
shuffle delayed eligibility
cut the useful return after growth
ordinary trained recurrent attacker
```

Only if useful recurrence can be selected without a named peer coordinate should the network expand beyond two points.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> finite allocation -> growing sparse matrix -> continuous internal dynamics -> recurrent traffic -> consequence-grown recurrent structure. The next job is to remove the hand-labelled recurrent coordinate and see whether useful returning traffic can be discovered rather than supplied.**
