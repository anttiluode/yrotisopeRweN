# yrotisopeRweN — the matrix under the point

`NewRepository` backwards.

**Read `MAINLINE.md` before extending this repo.**

This repository contains two branches:

```text
DIFFERENTIATION SIDE BRANCH
Oja -> Sanger/GHA -> AMUSE

MAIN HYPOTHESIS
broadcast
 -> receiver-relative fit
 -> compose
 -> context
 -> consequence
 -> finite allocation
 -> growing sparse matrix
 -> reversible regrowth
```

The differentiation branch is valid science. It is not currently the destination.

The main hypothesis is:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

This is a falsification-first computational abstraction, not a biological neuron simulator.

---

# The point

Externally the object can still be drawn as:

```text
●
```

The abstraction underneath it contains different timescales:

```text
FAST
receiver/excitability state
arrival-relative gating
recent context
local nonlinear conjunctions

SLOW
eligibility traces
learned utility / efficacy
capacity claims

PERSISTENT
effective sparse matrix
consolidated capacity
eventually perhaps topology / geometry
```

At one instant:

```text
M           persistent capacity / structure
W           slower learned efficacy
G(t)        fast receiver-dependent gate

W_eff(t) = M ⊙ W ⊙ G(t)
```

The repo asks what each layer is actually for before allowing them to recombine.

---

# Main-hypothesis receipts

## Gate 0 — receiver-relative fit

Receiver-specific fast phase/state changes which temporally structured arrivals are effective. A global oscillation is not enough.

```text
learned receiver phases      recovery 0.9947
phase-feature attacker       recovery 0.9960
```

Destroy phase diversity and the effect disappears.

Receipt: `results/GATE0.md`.

## Gate 1 — timing can write structure

Delay/path state changes temporal viability; finite structural mass turns repeated viability into sparse routing.

```text
mass + length self-wiring    top-1 1.0000
correct mass                 0.9997
```

Receipt: `results/GATE1.md`.

This was an early structural result. Later gates removed growth again to determine what structure should preserve.

## Gate 2 — coherence says CAN; consequence says KEEP

Timing-identical receiver twins have opposite downstream consequences.

```text
phase only          useful mass 0.4877
phase + utility     useful mass 0.9992
```

So timing can say a route is viable without saying it is useful.

Receipt: `results/GATE2.md`.

## Gate 3 — bounded growth becomes selection

Plain Hebbian growth explodes. Oja normalisation stabilises a finite direction.

The main-line lesson is not "PCA is the brain."

It is:

> **bounded growth turns amplification into allocation.**

Receipt: `results/GATE3.md`.

## Gate 6 — COMPOSE

Freeze all learning and growth.

The same two broadcasts and fixed nonlinear conjunction bank compute two different relations when only fast receiver state changes:

```text
state 0:  a0*b0 + a1*b1
state pi: a0*b1 + a1*b0
```

```text
receiver-state composer      NMSE 0.0000
ordinary scalar switch       NMSE 0.0000
stateless bilinear           NMSE 0.4978
state but no conjunction     NMSE ~1.00
```

Phase is therefore just one possible fast state coordinate in this gate.

Receipt: `results/GATE6.md`.

## Gate 7 — CONTEXT

The state-setting context moves into the past and disappears before the later broadcast arrives.

```text
context
 -> receiver state
 -> gap + distractors
 -> identical later A,B
 -> different composition
```

Twelve-seed memory curve:

```text
gap 8   circular NMSE 0.0098   scalar NMSE 0.0058
gap 16  circular NMSE 0.1242   scalar NMSE 0.1111
gap 32  circular NMSE 0.4913   scalar NMSE 0.4649
gap 64  context decode ~chance
```

Reset receiver state and the context-dependent contrast disappears.

The scalar recurrent attacker ties/slightly wins.

> **Receiver-carried context is the primitive; phase is not.**

Receipt: `results/GATE7.md`.

## Gate 8 — CONSEQUENCE

Several transient context-gated conjunctions exist, but only some help a downstream target. They disappear before scalar error arrives.

A local eligibility trace is the only bridge back.

At consequence delay 8:

```text
delayed eligibility          NMSE 0.000059
no eligibility               NMSE 1.0001
shuffled consequence         NMSE 1.0096
shuffled eligibility         NMSE 1.0928
context/state only           NMSE 1.0005
batch transient attacker     NMSE 0.000059
```

The ordinary batch attacker ties once the transient conjunction features exist.

Receipt: `results/GATE8.md`.

## Gate 9 — finite allocation / reversible consolidation

Allow only **positive local growth evidence** from consequence-modulated eligibility.

Gate 9 still supplies two-way rival families. Within each family, growing one claim must shrink its rival. A small `2%` reserve survives consolidation.

```text
phase 1 mass      [.9795, .0204, .9796, .0205]
phase-1 NMSE      0.000959

usefulness reverses

phase 2 mass      [.0205, .9794, .0206, .9795]
phase-2 NMSE      0.000978
switch >.90       13 epochs
```

Two opposite kills:

```text
zero reserve + hard pruning
    -> freezes obsolete allocation
    -> phase-2 NMSE 2.0127

unlimited positive growth
    -> old and new both accumulate
    -> phase-2 NMSE 1.0063
```

The signed projected-gradient attacker wins cleanly.

> **If local structure mainly receives positive growth evidence, conservation can provide retraction by competition, while a small exploratory reserve preserves plasticity after consolidation.**

Receipt: `results/GATE9.md`.

## Gate 10 — GROWING MATRIX

Gate 9's biggest remaining cheat was that it told each structural variable who its rival was.

Gate 10 removes those pairwise families.

Two six-dimensional broadcasts produce a dense potential relation field:

```text
Q_ij = A_i * B_j

6 x 6 = 36 candidate cells
```

All 36 cells share **one** conserved material/capacity pool:

```text
sum_ij M_ij = 1
M_ij >= 0.001 exploratory reserve
```

No row, column, pair, or rival topology is supplied.

Only four cells are useful in phase 1:

```text
phase-1 useful mass      0.96795
phase-1 held-out NMSE    0.001158
```

Then usefulness jumps to four completely disjoint cells:

```text
new-pattern mass > .90   after 17.08 +/- 0.28 epochs
final new-pattern mass   0.96771
phase-2 held-out NMSE    0.001171
```

A seed-0 matrix literally changes from approximately:

```text
.242 .001 .001 .001 .001 .001
.001 .001 .001 .242 .001 .001
.001 .001 .001 .001 .001 .001
.001 .001 .001 .001 .001 .001
.001 .001 .242 .001 .001 .001
.001 .001 .001 .001 .001 .242
```

to:

```text
.001 .001 .001 .001 .242 .001
.001 .001 .001 .001 .001 .001
.001 .242 .001 .001 .001 .001
.001 .001 .001 .001 .001 .242
.001 .001 .001 .001 .001 .001
.242 .001 .001 .001 .001 .001
```

Kills:

```text
no consequence              NMSE 4.6094
shuffled eligibility        NMSE 0.8819
zero reserve + hard prune   new mass 0.0000, NMSE 1.9928
unlimited positive growth   NMSE 1.0310
```

The signed global-gradient attacker solves both phases essentially exactly.

So this is not an optimizer claim.

The surviving result is:

> **A dense field of potential relations can grow into a sparse effective matrix when positive local utility evidence acts under one conserved global capacity budget. A tiny distributed reserve lets that matrix dissolve and regrow elsewhere when utility changes.**

This is the repo's current computational analogue of **growing structure**.

It is not yet literal growing topology: the candidate relation coordinates are still supplied as all products `A_i * B_j`.

Receipt: `results/GATE10.md`.

---

# Differentiation side branch

## Gate 4 — population differentiation

Independent Oja points collapse onto the strongest covariance mode. Sanger/GHA makes a population divide covariance structure.

```text
independent Oja     duplication 1.0000   recovery 0.2735
Sanger/GHA          duplication 0.0368   recovery 0.9782
explicit PCA                           recovery 0.9990
```

Receipt: `results/GATE4.md`.

## Gate 5 — one-lag temporal identity

In a world with spherical zero-lag covariance but different temporal laws:

```text
PCA                 recovery 0.7643
Sanger              recovery 0.7440
AMUSE tau=1         recovery 0.999995
shuffle time        recovery 0.7872
same memory law     recovery 0.7940
```

History can contain identity that instantaneous covariance does not.

Receipt: `results/GATE5.md`.

Do not add SOBI to the main hypothesis unless some later wall genuinely needs several lags.

---

# Current object

The main line now reads:

```text
same broadcast
    ↓
receiver-relative state says what fits
    ↓
local nonlinearity creates candidate relations
    ↓
past context persists transiently
    ↓
relations leave eligibility
    ↓
later consequence marks some useful
    ↓
positive growth acts on finite capacity
    ↓
a diffuse potential matrix becomes sparse
    ↓
exploratory reserve allows the sparse matrix to dissolve and regrow elsewhere
```

This is closer to the old "growing neuron" intuition without requiring us to simulate dendrites.

The abstraction is:

```text
many possible local computations
        ↓
finite structural budget
        ↓
useful traffic claims persistent capacity
        ↓
unused capacity withers toward a reserve
        ↓
changed utility moves structural investment
```

Whether that persistent capacity later deserves a physical geometry is a separate question.

---

# What is next — remove more scaffolding, do not add another verb

Gate 10 removed the supplied rival pairs.

The largest remaining cheat is now the **known conjunction field** itself.

Best next attacks:

```text
1. replace exact A_i*B_j products with a generic nonlinear local field
   -> ask whether finite consequence-driven growth still discovers useful cells

2. keep the product field but remove isolated trials
   -> continuous stream with context, broadcasts, distractors,
      overlapping eligibility, consequences, and world reversal

3. remove the clean binary context event
   -> ordinary preceding sensory patterns instead of C0/C1
```

The standard recurrent/gated/signed-gradient attacker stays in the room and is allowed to win.

Geometry/path length should return only after the less hand-designed growing matrix has something worth physically parameterizing.

Do not yet claim concepts, associative sequence completion, biological implementation, or a new optimizer.

---

# Run

```bash
python -m pip install -r requirements.txt

python experiments/gate0_relative_phase_routing.py
python experiments/gate1_self_wiring_phase_graph.py
python experiments/gate2_useful_coherence.py
python experiments/gate3_oja_phase_axis.py

# differentiation side branch
python experiments/gate4_population_differentiation.py
python experiments/gate5_amuse_history.py

# main hypothesis continuation
python experiments/gate6_receiver_state_composition.py
python experiments/gate7_context_memory.py
python experiments/gate8_delayed_consequence.py
python experiments/gate9_capacity_reversal.py
python experiments/gate10_growing_matrix.py

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **The sender broadcasts. Receiver state decides what fits and which nonlinear relations are available; past context can persist in that state; delayed consequence can select useful transient relations through eligibility; positive growth under finite conserved capacity can turn a dense potential relation field into a sparse effective matrix, and exploratory reserve lets that matrix regrow when utility changes.**
