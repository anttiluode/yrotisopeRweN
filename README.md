# yrotisopeRweN — the matrix under the point

`NewRepository` backwards.

**Read `MAINLINE.md` before extending this repo.**

This repository now contains two branches:

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
 -> reversible consolidation
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
learned efficacy / utility
capacity allocation

PERSISTENT
consolidated capacity / topology / geometry
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

This was an early structural result. Later gates remove growth again to determine what structure should preserve.

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

The same two broadcasts and fixed nonlinear conjunction bank can compute two different relations when only fast receiver state changes:

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

## Gate 9 — ALLOCATE / CONSOLIDATE / REALLOCATE

Now allow only **positive local growth evidence** from consequence-modulated eligibility.

Each context family has a conserved two-way capacity budget. Growing one claim must shrink its rival. A small `2%` exploratory reserve survives consolidation.

Phase 1:

```text
useful pattern     [1, 0, 1, 0]
mean mass          [.9795, .0204, .9796, .0205]
NMSE               0.000959
```

Then usefulness reverses:

```text
new pattern        [0, 1, 0, 1]
```

The old exploratory reserve now becomes useful. Across 12 seeds:

```text
new useful mass > .90 after 13 epochs
final mean mass   [.0205, .9794, .0206, .9795]
phase-2 NMSE      0.000978
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

The boring signed projected-gradient attacker wins cleanly:

```text
phase-1 NMSE 0.000053
phase-2 NMSE 0.000059
```

So Gate 9 is not an optimizer claim.

Its architectural result is narrower:

> **If local structure mainly receives positive growth evidence, conservation can provide retraction by competition, while a small exploratory reserve preserves plasticity after consolidation.**

Receipt: `results/GATE9.md`.

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

History can contain identity that the instantaneous covariance does not.

Receipt: `results/GATE5.md`.

Do not add SOBI to the main hypothesis unless some later wall genuinely needs several lags.

---

# Current chain

The repo now has a deliberately tiny implementation of every verb in the hypothesis:

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
competition consolidates useful relations
    ↓
exploratory reserve allows later reallocation
```

This chain is still heavily scaffolded.

That is now the problem.

---

# What is next — remove scaffolding, do not add another verb

The next experiment should attack the **whole chained hypothesis** by removing one hand-designed convenience.

Best candidates:

```text
1. remove the explicit pairwise capacity families
   -> one shared capacity pool / emergent competition

2. remove the supplied binary context code
   -> preceding sensory patterns instead of C0/C1

3. remove the known conjunction bank
   -> small generic nonlinear local basis

4. remove isolated trials
   -> continuous stream with overlapping context, broadcasts,
      distractors, eligibility, and consequences
```

The standard recurrent/gated/signed-gradient attacker stays in the room and is allowed to win.

Only if a less hand-designed chained system survives should geometry/path length return as a possible physical parameterization of persistent allocation.

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

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **The sender broadcasts. Receiver state decides what fits and which nonlinear relations are available; past context can persist in that state; delayed consequence can select useful transient conjunctions through eligibility; finite conserved capacity can turn positive evidence into persistent but reversible allocation. The next job is to remove scaffolding and see whether that chain survives.**
