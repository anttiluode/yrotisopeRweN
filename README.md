# yrotisopeRweN — the oscillating point

`NewRepository` backwards, because apparently that is where Tuesday went.

This repo tests one very small computational abstraction pulled out of the biology-inspired discussion:

> **A connection can be structurally present yet have a time-varying effective strength because the arriving signal meets a receiver whose internal state is oscillating.**

The incoming signal does **not** need a permanent phase tag. Arrival time relative to the receiver oscillator is enough.

The point neuron is still drawn as a point. But underneath the point is fast dynamical state.

```text
structural connection W
        │
        │        receiver oscillator state theta(t)
        │                    │
        └────────────┬───────┘
                     ↓
             relative-phase gate
                     ↓
          W_eff(t) = G(t) ⊙ W
                     ↓
                 output
```

This is not a biological neuron simulator and not a claim that brains implement this exact equation. It is a deliberately cheap abstraction of **dynamic effective connectivity**.

---

## Why make this?

A static point neuron exposes roughly

```text
y(t) = f(W x(t))
```

where the weights are the computation.

The object tested here exposes

```text
y(t) = f(W_eff(t) x(t))
W_eff(t) = G(relative phase, fast state) ⊙ W
```

so there are at least three distinct things:

```text
STRUCTURE
what can connect?

SLOW WEIGHT
what usually matters?

FAST OSCILLATORY GATE
what matters right now?
```

The immediate biological inspiration is modest: oscillatory receiver state can modulate the efficacy of afferent input according to arrival phase. The repo asks only whether that principle is computationally coherent and learnable in a toy world.

---

# Gate 0 — can receiver phase route a mixed signal?

`experiments/gate0_relative_phase_routing.py`

Two independent hidden processes are added into **one scalar mixture**. They differ in one extra piece of structure: they tend to express their energy at opposite phases of a shared oscillator.

```text
source A ─┐             around phase 0
          ├── scalar mixture x(t) ──► receivers
source B ─┘             around phase pi
```

Every receiver gets the same scalar mixture. There is no source label in the input.

A receiver has phase offset `theta_j` and instantaneous gain

```text
g_j(t) = ((1 + cos(phi(t) - theta_j)) / 2)^p
```

so its output is

```text
y_j(t) = g_j(t) x(t)
```

The phase offsets are learned from **arrival energy + soft lateral competition**. Energetic arrivals pull a receiver toward their phase, while competition prevents every receiver from claiming the same arrivals.

This is not presented as a biologically exact learning rule. It is the smallest test of the idea that receivers can learn different temporal "listening phases".

## Development result

Eight seeds, held-out final 40% of each run:

| arm | mean source recovery |
|---|---:|
| static point, duplicated mixture | 0.6950 |
| one global oscillatory gate duplicated to both outputs | 0.5088 |
| random receiver phases | 0.5991 ± 0.1610 |
| **learned receiver phases** | **0.9947 ± 0.0004** |
| oracle receiver phases | 0.9947 ± 0.0004 |
| **digital phase-feature attacker** | **0.9960 ± 0.0006** |

The learned receivers converge to offsets near `0` and `pi`, and their output duplication is only `0.0215` on average.

So in this world, the fast oscillatory gate really does act like a routing coordinate.

But the boring attacker still wins slightly. Give an ordinary linear model the explicit features

```text
x(t)
x(t) cos(phi(t))
x(t) sin(phi(t))
```

and it recovers the sources just as well or better.

**That is the correct result.** Oscillation has not discovered information unavailable to a normal computer. It is one way to *instantiate* a useful time-varying basis.

---

# The negative control matters more than the win

Now put both hidden processes at the **same oscillator phase**.

The learned system cannot separate them:

```text
learned recovery     ≈ 0.7335
output duplication   ≈ 0.9996
```

The phase-feature attacker also falls to the same regime.

So the experiment is not simply "add oscillations and separation appears."

The useful claim is narrower:

> **Relative phase can route information only when the world actually contains stable phase-relative structure to exploit.**

No phase diversity, no phase-routing advantage.

Full receipt: `results/GATE0.md`.

---

# What this is trying to become

The interesting object is not a complex number for its own sake and not a globally wiggling neural net.

It is a **dynamical point**:

```text
(signal_in, point_state)
          ↓
        interaction
          ↓
(signal_out, new_point_state)
```

A future version can have:

```text
fast oscillator phase
fast cable / branch state
slow homeostatic state
slow learned weights
```

and therefore a temporary effective operator

```text
W_eff(t) = W_slow + state-dependent gated suboperators
```

The graph may still draw one dot. The dot is no longer stateless.

---

# Next gates

## Gate 1 — drifting world

Slowly move the preferred arrival phases after training.

Question:

> can receiver oscillators track the drift online, or is "learned synchronization" just a batch clustering trick?

Compare against an ordinary adaptive phase-feature filter.

## Gate 2 — remove the supplied global phase

Gate 0 hands the model `phi(t)`.

Replace that convenience with local oscillators / PLL-like state that must synchronize from the event stream itself.

If it cannot recover a useful clock, the story stops there.

## Gate 3 — signal changes the receiver

Let an arriving event perturb receiver phase/state:

```text
arrival
  ↓
current gate decides efficacy
  ↓
arrival shifts receiver state
  ↓
next arrival sees a different point
```

Now the signal is simultaneously cargo, operand, and write operation.

## Gate 4 — combine with the dynamical neuron

Use branch/cable state as additional fast coordinates and let oscillatory gating select which state/suboperator is effective at a given moment.

The attacker remains an ordinary matched state-space model / adaptive filter / MLP.

---

# Kill conditions

This project should be demoted immediately if:

- random oscillation performs as well as learned phase;
- the effect survives when source phase structure is destroyed;
- a static equal-budget model gets the same result without using time;
- online phase tracking is unstable;
- supplying the explicit clock is doing all the work and local oscillators cannot recover it;
- ordinary adaptive filtering reproduces the useful behavior more cleanly.

In that case the oscillating point is an implementation metaphor, not an algorithmic advance.

That is fine.

---

# Run

```bash
python -m pip install -r requirements.txt
python experiments/gate0_relative_phase_routing.py
python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **The wiring graph describes potential connectivity. A dynamical receiver state can turn that into a different effective graph from moment to moment. Relative phase is one mathematically cheap coordinate for that fast routing.**
