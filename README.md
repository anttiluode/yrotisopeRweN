# yrotisopeRweN — the matrix under the point

`NewRepository` backwards, because the interesting road turned out not to be another ordinary forward architecture.

**Read `MAINLINE.md` before extending this repo.**

The repo now contains two legitimate branches. One is a well-paved differentiation branch (`Oja -> Sanger -> AMUSE`). Keep it. It is not the current destination.

The main hypothesis is:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

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

This is a falsification-first computational abstraction, not a biological neuron simulator.

---

# The object

The point can still be drawn as:

```text
●
```

but the abstraction underneath it now contains different timescales:

```text
FAST
receiver/excitability state
arrival-relative gating
recent context
local nonlinear conjunctions

SLOW
learned efficacy / utility
eligibility traces
bounded allocation

PERSISTENT
structural mass / topology / geometry
```

At one instant a network can still be written as a matrix, but that matrix is not one object:

```text
M           persistent structural capacity
W           slower learned efficacy
G(t)        fast receiver-dependent gating

W_eff(t) = M ⊙ W ⊙ G(t)
```

The core question is no longer merely "what are the weights?"

It is:

> **How can the same fixed slow structure compute differently because the receiver is in a different transient state, and how can useful transient relations later earn persistent resources?**

---

# Main-hypothesis gates

## Gate 0 — receiver-relative fit

`experiments/gate0_relative_phase_routing.py`

Two hidden processes are summed into one scalar mixture but tend to arrive at different phases of a supplied oscillator.

Development result:

| arm | source recovery |
|---|---:|
| static point | `0.6950` |
| one global oscillation | `0.5088` |
| random receiver phases | `0.5991 ± 0.1610` |
| learned receiver phases | **`0.9947 ± 0.0004`** |
| digital phase-feature attacker | **`0.9960 ± 0.0006`** |

Destroy phase diversity and the advantage disappears.

Surviving claim:

> **Fast receiver-relative state can decide which temporally structured arrivals are effective. A global wiggle is not enough.**

Receipt: `results/GATE0.md`.

---

## Gate 1 — timing can write structure

`experiments/gate1_self_wiring_phase_graph.py`

Candidate paths have structural mass and propagation delay. Delay changes whether sender events arrive during a receiver-compatible window; finite mass makes viable routes compete.

Twelve-seed result:

| arm | top-1 target | correct mass |
|---|---:|---:|
| static random | `0.3333` | `0.1667` |
| mass only | `0.3333` | `0.4271` |
| length only | `0.3333` | `0.1667` |
| mass + length | **`1.0000`** | **`0.9997`** |
| destroyed coherence | `0.4444` | `0.2060` |

Surviving claim:

> **Geometry/delay can determine temporal viability, and a finite structural budget can turn repeated viability into sparse wiring.**

Receipt: `results/GATE1.md`.

This was an early structural result. Later gates deliberately remove growth again so we can identify what structure should actually preserve.

---

## Gate 2 — coherence says CAN; consequence says KEEP

`experiments/gate2_useful_coherence.py`

Each sender gets two timing-identical receiver twins with opposite downstream consequences. Phase cannot distinguish them.

| arm | useful mass | target correlation |
|---|---:|---:|
| phase only | `0.4877` | `0.0158` |
| utility only | `0.3720` | `0.2436` |
| phase + utility | **`0.9992`** | **`0.9061`** |
| destroyed utility | `0.4846` | `0.0023` |

Surviving decomposition:

```text
FIT / TIMING
can this relation occur?

CONSEQUENCE
was it useful?

STRUCTURE
should it persist?
```

Receipt: `results/GATE2.md`.

Gate 2 also left an unfinished stability/plasticity problem: once useful structure hardens, what happens if usefulness reverses?

---

## Gate 3 — bounded growth becomes selection

`experiments/gate3_oja_phase_axis.py`

Oja was introduced as a precise example of a more primitive principle:

```text
plain correlated growth -> runaway magnitude
normalised growth       -> finite directional allocation
```

Plain Hebb hits the `1e6` guard in 12/12 runs. Oja settles at unit norm and learns the dominant phase axis.

But Oja learns an axis, not two opposite identities. A nonlinear/nonnegative local gate is required to make the two ends computationally distinct.

Surviving principle:

> **Bounded growth forces correlated experience to become selective allocation instead of unlimited amplification.**

Receipt: `results/GATE3.md`.

---

## Gate 6 — COMPOSE

`experiments/gate6_receiver_state_composition.py`

Gates 4/5 are described below as a side branch. Gate 6 returns to the main hypothesis and freezes all learning and growth.

Two broadcasts carry:

```text
A = [a0, a1]
B = [b0, b1]
```

The same fixed nonlinear conjunction bank can compute:

```text
state 0:  a0*b0 + a1*b1
state pi: a0*b1 + a1*b0
```

by changing only fast receiver state.

| arm | NMSE |
|---|---:|
| receiver-state composition | **`0.0000`** |
| ordinary scalar mode switch | **`0.0000`** |
| stateless bilinear readout | `0.4978` |
| state but no nonlinear conjunction | `1.0024` |
| shuffled/frozen state | ~`0.99` |

So phase earned no special expressive status. The scalar switch ties exactly.

Surviving claim:

> **Fixed slow structure plus changed fast receiver state can produce a different nonlinear computation, reversibly and without relearning.**

Receipt: `results/GATE6.md`.

---

## Gate 7 — CONTEXT

`experiments/gate7_context_memory.py`

Gate 6 was handed its fast state at composition time. Gate 7 moves that information into the past:

```text
context happens
    -> receiver changes
context disappears
    -> unrelated gap events
identical later A,B arrive
    -> leftover receiver state changes composition
```

No mode input exists at composition time and no weights change.

Twelve-seed memory curve under distractors:

| gap | circular state NMSE | scalar state NMSE | context decode |
|---:|---:|---:|---:|
| 0 | `0.0000` | `0.0000` | `1.0000` |
| 8 | **`0.0098`** | **`0.0058`** | `0.9985` |
| 16 | **`0.1242`** | **`0.1111`** | `0.9244` |
| 32 | `0.4913` | `0.4649` | `0.6694` |
| 64 | `0.7195` | `0.6960` | `0.5140` |

Reset receiver state before the later broadcast and the context-dependent contrast disappears (`contrast NMSE ~1`). Shuffle the old context and the useful relation disappears too.

Again the one-scalar recurrent attacker ties/slightly wins.

Surviving claim:

> **Past input can disappear while a transient receiver state remains changed, causing the same later broadcast to be interpreted/composed differently.**

Not "phase memory." Receiver-carried context is the primitive.

Receipt: `results/GATE7.md`.

---

## Gate 8 — CONSEQUENCE

`experiments/gate8_delayed_consequence.py`

Gate 8 keeps structural growth off.

Earlier context leaves receiver state. Later broadcasts create several state-gated nonlinear conjunctions. Only some help a downstream target. The conjunction activity disappears before scalar error arrives.

The only bridge back is a decaying local eligibility trace:

```text
conjunction phi_j
      -> eligibility e_j
      ... delay ...
scalar consequence/error
      -> Δw_j ∝ error * e_j
```

At consequence delay 8:

| arm | held-out NMSE |
|---|---:|
| delayed eligibility | **`0.000059`** |
| no eligibility | `1.0001` |
| shuffled consequence | `1.0096` |
| shuffled eligibility | `1.0928` |
| context/state alone, no conjunctions | `1.0005` |
| batch transient-feature attacker | **`0.000059`** |
| explicit old-context buffer | ~`0.000000` |

The learned slow efficacy pattern aligns with the hidden useful conjunction pattern at `0.9999999`.

Surviving claim:

> **A delayed consequence can selectively change slow efficacy only when the earlier transient conjunction left a trace that still identifies what happened.**

Receipt: `results/GATE8.md`.

---

# Differentiation side branch — keep the receipts, do not follow automatically

## Gate 4 — population differentiation

Independent Oja points all chase the strongest covariance direction. Sanger/GHA adds across-point competition and makes them divide covariance structure.

| arm | weight duplication | source recovery |
|---|---:|---:|
| independent Oja | `1.0000` | `0.2735` |
| Sanger/GHA | **`0.0368`** | **`0.9782`** |
| explicit PCA | — | **`0.9990`** |

A rank-1 kill remains information-rank 1. In a spherical zero-lag world with temporal differences, Sanger/PCA cannot identify the causes.

Receipt: `results/GATE4.md`.

## Gate 5 — one delayed covariance

In the matched zero-lag world, AMUSE with one lag recovers the temporally distinct causes almost perfectly:

| arm | source recovery |
|---|---:|
| PCA | `0.7643` |
| Sanger | `0.7440` |
| AMUSE tau=1 | **`0.999995`** |
| shuffled time | `0.7872` |
| same memory law | `0.7940` |

Surviving claim:

> **History can contain source identity that the instantaneous covariance does not.**

Receipt: `results/GATE5.md`.

This is valid machinery. It is currently a side branch. Do not add SOBI to the main hypothesis unless a future problem specifically requires multi-lag differentiation.

---

# What is next — ALLOCATE / CONSOLIDATE

Gates 6–8 finally give the old growth story a cleaner object to preserve:

```text
earlier context
    -> transient receiver state
    -> later nonlinear conjunction
    -> eligibility
    -> delayed consequence
    -> evidence that THIS relation mattered
```

The next gate should introduce **finite capacity**, but still avoid geometry at first.

Ask:

> **Can repeatedly useful conjunctions claim persistent capacity while unused/harmful conjunctions lose it?**

The resource conflict must be real: preserving one relation must make another less available.

Critical attacks:

```text
unlimited capacity
    -> if everything grows, allocation was never tested

remove consequence
    -> co-activation alone should not decide persistence

shuffle eligibility
    -> delayed utility should consolidate the wrong thing or nothing

ordinary sparse/regularized fixed-capacity model
    -> boring attacker

reverse usefulness after consolidation
    -> stability/plasticity kill
```

The reversal is load-bearing. A useful system must avoid both:

```text
freeze forever
and
dissolve everything
```

Only after finite allocation survives should structural mass and then geometry/path length be reintroduced.

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

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **The sender broadcasts. Fast receiver state decides what fits and which nonlinear relations are available; past context can persist in that state; delayed consequence can select useful transient conjunctions through eligibility. The next unanswered question is whether finite capacity can turn that repeated usefulness into persistent allocation without destroying the ability to change later.**
