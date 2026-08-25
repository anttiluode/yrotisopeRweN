# yrotisopeRweN — main hypothesis compass

This file exists because the mathematically well-paved differentiation branch is gravitational.

Gates 4/5 are valid and should remain in the repo, but they are a **side branch**:

```text
Oja -> one direction
Sanger/GHA -> population differentiation
AMUSE -> temporal differentiation from one lag
```

The originating hypothesis that made this backwards repo interesting is different:

> **The sender broadcasts. The receiver decides whether the arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves permanent structure.**

In verbs:

```text
BROADCAST
    -> RECEIVER-RELATIVE FIT
    -> COMPOSE
    -> CONSEQUENCE
    -> CONSOLIDATE
```

Treat that as the main hypothesis, not as an established result.

---

## What is already established in the main hypothesis

### Receiver-relative fit

Gate 0 showed that receiver-specific fast phase/state can alter which temporally structured arrivals are effective. A global oscillation was not enough.

### Coherence is not purpose

Gate 2 showed that two timing-compatible routes can be behaviorally opposite. Phase/coherence says a route **can** communicate; task consequence is needed to say whether it **should** persist.

### Bounded growth is selection, not magic

Gate 3 used Oja only as a precise example of the principle that correlated growth cannot increase without bound. The normalization term turns amplification into directional allocation. In the main line, that resource-allocation principle matters more than calling Oja a PCA algorithm.

---

## Gate 6 — COMPOSE

Gate 6 isolates the next verb with no learning or growth.

The same two broadcasts and the same fixed conjunction bank can be rebound into two different relations by changing only fast receiver state:

```text
state 0:  a0*b0 + a1*b1
state pi: a0*b1 + a1*b0
```

No slow weight or topology changes.

The operation is perfectly reversible.

But an ordinary scalar mode switch implements the exact same computation. Therefore Gate 6 does **not** establish phase as a special computational resource.

What survived is narrower:

> **A fast receiver state can serve as the mode variable that selects which nonlinear relation the fixed slow structure computes.**

Phase is currently one possible coordinate for that state.

The local nonlinearity is load-bearing: state-dependent linear routing cannot produce the conjunction target in this toy.

Receipt: `results/GATE6.md`.

---

# Branch map

```text
                            Gate 3
                       bounded selection
                         /            \
                        /              \
       DIFFERENTIATION SIDE BRANCH     MAIN HYPOTHESIS
                 |                           |
              Sanger                     COMPOSE  <- Gate 6
                 |                           |
              AMUSE                     context/state?
                 |                           |
              SOBI?                     CONSEQUENCE
                                             |
                                         CONSOLIDATE
                                             |
                                      mass / geometry
```

Do not add SOBI to the main hypothesis merely because it is nearby in the literature.

---

# Next main-line missing operation

Gate 6 was handed the receiver state explicitly.

So the next clean question is:

> **Can preceding local context put the receiver into a transient state that changes how a later identical broadcast is composed, without an explicit mode variable being supplied at composition time?**

This is not yet utility and not yet growth.

A future gate should keep the conjunction bank and slow weights fixed, use context only to perturb/store fast receiver state, then present the same later broadcasts.

Kill conditions:

- resetting receiver state between context and broadcast should destroy the context-dependent composition;
- a boring scalar recurrent-state baseline should be allowed to tie or win;
- if the experiment simply hides an explicit mode label inside a phase variable, say so;
- no weight update may occur during rebinding;
- no utility or mass signal is allowed until transient context-dependent composition is real.

Only after that survives should the main line proceed:

```text
transient composition
      -> consequence/error
      -> did this relation matter?
      -> bounded allocation
      -> structural consolidation
```

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> consequence -> consolidate. If an experiment does not attack one of those verbs, it is probably a side branch.**
