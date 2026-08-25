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
    -> CONSOLIDATE
```

`CONTEXT` is written explicitly now because Gate 7 showed that the receiver can remain transiently changed after the context event itself is gone.

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

---

# Branch map

```text
                              Gate 3
                         bounded selection
                           /            \
                          /              \
         DIFFERENTIATION SIDE BRANCH     MAIN HYPOTHESIS
                   |                           |
                Sanger                     COMPOSE      Gate 6
                   |                           |
                AMUSE                      CONTEXT      Gate 7
                   |                           |
                SOBI?                     CONSEQUENCE  next
                                               |
                                           ALLOCATION
                                               |
                                           CONSOLIDATE
                                               |
                                        mass / geometry
```

Do not add SOBI to the main hypothesis merely because it is nearby in the literature.

---

# Next main-line missing operation — CONSEQUENCE

Gate 7 gives consequence something real to act on: a useful later composition can depend on a transient state transition caused by an earlier event.

The next gate must **not** simply reward the context bit or the currently active input.

Instead create several possible transient context-dependent conjunctions, only one of which helps a downstream task, and ask:

> **Can consequence assign credit back to the earlier state transition / conjunction that made the later useful computation possible?**

That is a temporal credit-assignment problem inside the main hypothesis.

Keep structural growth off for this gate.

A clean Gate 8 should contain:

```text
EARLIER CONTEXT
writes transient receiver state

LATER BROADCASTS
produce one of several possible conjunctions

DOWNSTREAM CONSEQUENCE
arrives after the conjunction

ELIGIBILITY / LOCAL TRACE
is the only bridge back to what happened earlier
```

Attackers / kills:

- no eligibility trace: delayed consequence should not know what earlier relation to reinforce;
- shuffle consequence across trials: learning should disappear;
- immediate supervised mode label: digital upper bound;
- ordinary scalar eligibility trace: allowed to tie or win;
- no growth, no mass, no geometry yet;
- avoid rewarding the context code directly.

Only if delayed consequence can select useful transient compositions should the main line proceed to bounded allocation and physical consolidation.

---

# Later questions, not yet earned

Sequence completion / route-memory intuition belongs later:

```text
partial old state
    -> re-enter trajectory
    -> missing continuation becomes reachable
```

Do not call Gate 7 associative memory. It only established transient context-dependent interpretation over a finite noisy horizon.

Likewise, structural stability/plasticity from Gate 2 remains unfinished and should be revisited when consolidation is reintroduced.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> consolidate. If an experiment does not attack one of those verbs, it is probably a side branch.**
