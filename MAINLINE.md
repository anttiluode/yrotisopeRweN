# yrotisopeRweN — main hypothesis compass

This file exists because the mathematically well-paved differentiation branch is gravitational.

Gates 4/5 are valid and should remain in the repo, but they are a **side branch**:

```text
Oja -> one direction
Sanger/GHA -> population differentiation
AMUSE -> temporal differentiation from one lag
```

The originating hypothesis that made this backwards repo interesting is different:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

The current main-line verbs are:

```text
BROADCAST
    -> RECEIVER-RELATIVE FIT
    -> COMPOSE
    -> CONTEXT
    -> CONSEQUENCE
    -> ALLOCATE
    -> CONSOLIDATE / REALLOCATE
```

For the first time, each verb now has at least one deliberately tiny gate behind it.

That does **not** mean the architecture is established. It means the next job is no longer to append a verb.

---

# What the gates established

## Gate 0 — receiver-relative fit

Receiver-specific fast state can alter which temporally structured arrivals are effective. A global oscillation was not enough.

The digital phase-feature attacker still wins slightly.

Receipt: `results/GATE0.md`.

## Gate 1 — timing can write structure

Delay/path state changes temporal viability; finite structural mass can turn repeated viability into sparse routing.

This was an early growth result, before the repo knew clearly what structure should preserve.

Receipt: `results/GATE1.md`.

## Gate 2 — coherence says CAN; consequence says KEEP

Timing-identical receiver twins can be behaviorally opposite. Coherence alone remains ~50/50; consequence selects the useful route.

This gate also exposed the stability/plasticity problem that Gate 9 finally revisits.

Receipt: `results/GATE2.md`.

## Gate 3 — bounded growth becomes selection

Oja is useful here mainly as a precise example of a primitive principle:

> **correlated growth plus a bound becomes allocation rather than unlimited amplification.**

Do not equate structural mass with Oja mathematically.

Receipt: `results/GATE3.md`.

## Gate 6 — COMPOSE

The same fixed conjunction bank computes two different bilinear relations when only fast receiver state changes.

The operation is reversible without a weight update.

An ordinary scalar switch ties phase exactly, so phase gets no privileged status.

Surviving claim:

> **fast receiver state can select which nonlinear relation fixed slow structure computes.**

Receipt: `results/GATE6.md`.

## Gate 7 — CONTEXT

Move the state-setting event into the past. Let it disappear. Insert unrelated events. Present the same later broadcasts.

The leftover receiver state changes the later composition.

Under the chosen noisy recurrence:

```text
gap 8   circular NMSE 0.0098   scalar NMSE 0.0058
gap 16  circular NMSE 0.1242   scalar NMSE 0.1111
gap 32  circular NMSE 0.4913   scalar NMSE 0.4649
gap 64  context decode ~chance
```

Reset receiver state and the paired context-dependent contrast disappears.

Again the scalar recurrent attacker ties/slightly wins.

Surviving claim:

> **receiver-carried context is the primitive; phase is only one possible coordinate system for it.**

Receipt: `results/GATE7.md`.

## Gate 8 — CONSEQUENCE

Several transient context-gated nonlinear conjunctions exist, but only some help a downstream task.

The conjunction vector disappears before scalar error arrives.

A decaying local eligibility trace is the only bridge back.

At consequence delay 8:

```text
delayed eligibility NMSE     0.000059
no eligibility               1.0001
shuffled consequence         1.0096
shuffled eligibility         1.0928
context/state alone          1.0005
```

Batch regression on the transient conjunction features ties the delayed learner, and an explicit old-context buffer is essentially exact.

Surviving claim:

> **delayed consequence can select earlier transient conjunctions only if some trace still identifies what happened.**

Receipt: `results/GATE8.md`.

## Gate 9 — ALLOCATE / CONSOLIDATE / REALLOCATE

Positive utility evidence is allowed to **grow** local capacity claims, but there is no explicit negative shrink command.

Each context family has a conserved two-way capacity budget. A small `2%` exploratory reserve survives consolidation.

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

The reserve keeps the previously unused relations sampleable. New positive evidence grows them; conservation automatically takes capacity from the old routes.

Across 12 seeds:

```text
new useful mass > .90 after 13 epochs
final mean mass   [.0205, .9794, .0206, .9795]
phase-2 NMSE      0.000978
```

Two opposite kills are important:

```text
zero reserve + hard pruning
    -> obsolete allocation freezes
    -> phase-2 NMSE 2.0127

unlimited positive growth
    -> old + new both accumulate
    -> phase-2 NMSE 1.0063
```

And the boring signed projected-gradient attacker is much cleaner:

```text
phase-1 NMSE 0.000053
phase-2 NMSE 0.000059
```

So Gate 9 is not an optimizer claim.

Its surviving architectural point is:

> **When local structure mainly receives positive growth evidence, conservation can provide retraction by competition, while a small exploratory reserve preserves the ability to discover changed utility after consolidation.**

Receipt: `results/GATE9.md`.

---

# Differentiation side branch

## Gate 4 — population differentiation

Independent Oja points collapse onto the strongest covariance mode. Sanger/GHA makes a population divide covariance structure. Explicit PCA still wins.

Receipt: `results/GATE4.md`.

## Gate 5 — one-lag temporal identity

In a world whose zero-lag covariance is spherical but whose temporal laws differ, AMUSE(tau=1) recovers the sources almost perfectly. Shuffle time or equalize the memory laws and the advantage disappears.

Receipt: `results/GATE5.md`.

This is real machinery. It is not currently the main hypothesis.

Do not add SOBI unless some future wall specifically requires several lagged statistics.

---

# The current chain

The repo has now walked this toy chain:

```text
same broadcast
    ↓
receiver-relative state says what fits
    ↓
local nonlinearity creates candidate relations
    ↓
past context can persist in receiver state
    ↓
transient relations leave eligibility
    ↓
later consequence marks some relations useful
    ↓
positive growth evidence acts on finite capacity
    ↓
competition consolidates useful relations
    ↓
exploratory reserve allows later reallocation
```

That is the current object.

It is still extremely hand-designed.

---

# What comes next — ATTACK THE CHAIN, DO NOT ADD A VERB

A fresh chat should **not** respond to this repo by adding another learning rule or biological mechanism.

Remove one hand-designed convenience and see whether the chain survives.

Best candidates:

### 1. Remove the explicit pairwise capacity families

Gate 9 currently knows that `q00` competes with `q11` and `q01` competes with `q10`.

Give all candidate conjunctions one shared capacity pool or let competition topology emerge.

Ask whether useful relations still allocate without being told who their rival is.

### 2. Remove the supplied binary context code

Gate 7 receives a clean `C0/C1` event.

Replace it with an ordinary preceding sensory pattern whose relevance is not explicitly labeled.

Ask whether a small receiver state can still carry the useful distinction.

### 3. Remove the known conjunction bank

Gate 6 is handed the four products `q00,q01,q10,q11` through fixed square-law subunits.

Give the receiver a small generic nonlinear local basis and ask whether useful relational features emerge/select under consequence.

### 4. Remove isolated trials

Run a continuous stream:

```text
context-ish events
broadcasts
distractors
consequences
```

with overlapping eligibility and no clean reset between examples.

This is probably the most brutal attack on the current story.

### 5. Keep the boring attacker

A standard recurrent/gated network with ordinary signed gradient is allowed to tie or win.

If it wins more simply, say so.

---

# What is still not earned

Do not yet claim:

- biological neurons implement this chain;
- phase is important in general;
- morphology is required;
- structural mass is literal biological material;
- concepts have emerged;
- associative sequence completion has been shown;
- this is a new learning algorithm;
- the chain scales.

Geometry/path length should return only after the less hand-designed chain has something worth physically parameterizing.

The route/music sequence-completion intuition belongs later:

```text
partial old state
    -> re-enter trajectory
    -> missing continuation becomes reachable
```

Gate 7 is not yet that.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> finite allocation -> reversible consolidation. The next job is to remove scaffolding and see whether the chain survives.**
