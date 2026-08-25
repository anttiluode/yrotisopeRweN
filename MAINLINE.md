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
    -> CONTEXT
    -> CONSEQUENCE
    -> ALLOCATE
    -> CONSOLIDATE
```

Treat this as the main hypothesis, not as an established architecture.

---

## What is already established in the main hypothesis

### Receiver-relative fit — Gate 0

Receiver-specific fast phase/state can alter which temporally structured arrivals are effective. A global oscillation was not enough.

### Coherence is not purpose — Gate 2

Two timing-compatible routes can be behaviorally opposite. Phase/coherence says a route **can** communicate; task consequence is needed to say whether it **should** persist.

### Bounded growth is selection, not magic — Gate 3

Oja is a precise example of the principle that correlated growth cannot increase without bound. Its normalization term turns amplification into directional allocation. In the main line, that resource-allocation principle matters more than calling Oja a PCA algorithm.

### Compose — Gate 6

The same broadcasts and fixed nonlinear conjunction bank can implement two different relations by changing only fast receiver state:

```text
state 0:  a0*b0 + a1*b1
state pi: a0*b1 + a1*b0
```

No slow weight or topology changes, and the operation is reversible.

But an ordinary scalar switch implements the exact same computation. So phase earned no special expressive status.

Surviving claim:

> **Fast receiver state can select which nonlinear relation fixed slow structure computes.**

Receipt: `results/GATE6.md`.

### Context — Gate 7

Gate 6 was handed the state at composition time. Gate 7 moves the mode information into the past:

```text
context event
    ↓
receiver state changes
    ↓
context disappears
    ↓
gap + unrelated events
    ↓
identical later A,B
    ↓
composition depends on leftover state
```

No mode/context input exists at the final composition step and no weights change.

The circular receiver has a finite useful memory curve under distractors:

```text
gap 0   NMSE 0.0000
gap 8   NMSE 0.0098
gap 16  NMSE 0.1242
gap 32  NMSE 0.4913
gap 64  NMSE 0.7195
```

Resetting state before the later broadcast destroys the paired context-dependent contrast (`contrast NMSE ~1.0`). Shuffling which old context wrote the state also destroys the useful relation.

A one-scalar recurrent trace ties or slightly beats the circular receiver through the useful range. Therefore phase again gets demoted:

> **receiver-carried context is the primitive; phase is currently only one possible coordinate system for it.**

Receipt: `results/GATE7.md`.

### Consequence — Gate 8

Gate 8 gives the transient conjunctions delayed downstream consequences without allowing any structural growth.

Each remembered context makes two conjunctions available, but only one is useful:

```text
context 0: q00 useful, q11 irrelevant
context 1: q10 useful, q01 irrelevant
```

The conjunction vector disappears before the scalar error arrives. The only bridge back is a decaying local eligibility trace.

At consequence delay 8:

```text
delayed eligibility NMSE      0.000059
utility-weight alignment      0.9999999
no eligibility                1.0001
shuffled consequence          1.0096
shuffled eligibility          1.0928
context/state without q       1.0005
```

A batch readout with the old context explicitly buffered is essentially exact, and batch regression on the transient conjunction features ties the delayed learner.

So nothing exotic is being claimed about the optimizer.

The surviving operation is:

> **A later consequence can selectively modify slow efficacy only when the earlier transient conjunction left an eligibility trace that still identifies what happened.**

Receipt: `results/GATE8.md`.

---

# Branch map

```text
                              Gate 3
                         bounded selection
                           /            \
                          /              \
         DIFFERENTIATION SIDE BRANCH     MAIN HYPOTHESIS
                   |                           |
                Sanger                     COMPOSE       Gate 6
                   |                           |
                AMUSE                      CONTEXT       Gate 7
                   |                           |
                SOBI?                     CONSEQUENCE   Gate 8
                                               |
                                            ALLOCATE    next
                                               |
                                          CONSOLIDATE
                                               |
                                        mass / geometry
                                               |
                                   stability / plasticity
```

Do not add SOBI to the main hypothesis merely because it is nearby in the literature.

---

# Next main-line missing operation — ALLOCATE / CONSOLIDATE

The earlier growth experiments had a conceptual weakness: synchrony or utility could reinforce structure, but the object being preserved was still somewhat vague.

Gates 6–8 now give consolidation a much cleaner candidate object:

```text
earlier context
    -> receiver state
    -> later nonlinear conjunction
    -> local eligibility
    -> delayed consequence
    -> slow evidence that THIS relation mattered
```

Now introduce a finite capacity / structural budget and ask:

> **Can repeatedly useful conjunctions claim persistent capacity while unused or harmful conjunctions lose it?**

This should not merely multiply Gate-8 efficacy by Gate-1 mass.

The gate needs an actual resource conflict: preserving one useful relation must make another more expensive or less available.

Useful attackers / kills:

- ordinary fixed-capacity sparse or regularized readout;
- unlimited-capacity control: if everything can grow, allocation has not been tested;
- utility removed: structure should not know what to preserve;
- eligibility shuffled: delayed consequence should consolidate the wrong thing or nothing;
- mass without consequence: mere co-activation should not win;
- freeze after consolidation, then **reverse which conjunction is useful**.

That last reversal reconnects directly to the unfinished Gate-2 stability/plasticity problem.

A successful system must not:

```text
freeze forever
or
dissolve everything
```

It must retain enough exploratory / reallocatable capacity to move persistent structure when consequence changes.

Only after that survives should geometry/path length be allowed back in. First prove capacity allocation without spatial decoration.

---

# Later questions, not yet earned

Sequence completion / route-memory intuition belongs later:

```text
partial old state
    -> re-enter trajectory
    -> missing continuation becomes reachable
```

Do not call Gate 7 associative memory. It only established transient context-dependent interpretation over a finite noisy horizon.

Likewise, morphology, dendritic geometry, and path growth should not return until finite allocation itself has a job.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> allocate -> consolidate. If an experiment does not attack one of those verbs, it is probably a side branch.**
