# yrotisopeRweN — the oscillating point that starts to wire itself

`NewRepository` backwards, because apparently Tuesday kept going backwards until the matrix started growing.

This repo tests a small computational abstraction:

> **The wiring graph is potential connectivity. Fast receiver state determines what communicates now. Repeatedly successful timing can slowly change which connections physically persist.**

The point neuron can still be drawn as a point. Underneath it are several timescales:

```text
FAST
receiver oscillator / excitability state
arrival timing
instantaneous gate

SLOWER
edge delay / path length
structural mass
receiver vitality

PERSISTENT
which routes survive
```

This is not a biological neuron simulator. It is a falsification-first abstraction of dynamic effective connectivity and structural plasticity.

---

# The object

A static edge is usually written as

```text
y_j(t) = W_ij x_i(t)
```

Gate 0 made the effective edge state-dependent:

```text
W_eff_ij(t) = G_ij(t) * W_ij
```

where `G` depends on arrival time relative to receiver phase.

Gate 1 adds slow structure:

```text
M_ij       structural mass
D_ij       propagation delay / length proxy
G_ij(t)    fast phase gate

W_eff_ij(t) = M_ij * G_ij(t) * W_ij
```

and, crucially,

```text
fast successful traffic
        ↓
slow structural reinforcement
```

so the instantaneous network can slowly compile itself into a persistent sparse graph.

The current slogan is:

> **fast routing writes slow wiring.**

---

# Gate 0 — relative-phase routing

`experiments/gate0_relative_phase_routing.py`

Two hidden sources are summed into one scalar mixture but tend to express at opposite phases of a shared oscillator. Receiver points learn different listening phases from arrival energy plus competition.

Development result:

| arm | mean source recovery |
|---|---:|
| static point | 0.6950 |
| one global oscillation | 0.5088 |
| random receiver phases | 0.5991 ± 0.1610 |
| **learned receiver phases** | **0.9947 ± 0.0004** |
| oracle phase | 0.9947 ± 0.0004 |
| digital phase-feature attacker | **0.9960 ± 0.0006** |

Destroy source phase diversity and the advantage disappears.

Surviving claim:

> **Receiver-specific relative phase can be a fast routing coordinate when the world contains stable timing structure. A global wiggle is not enough.**

The digital feature attacker still wins slightly. Good.

Full receipt: `results/GATE0.md`.

---

# Gate 1 — self-wiring by phase coherence

`experiments/gate1_self_wiring_phase_graph.py`

This gate asks the new question:

> **Can a signal keep probing possible paths until repeated phase-compatible arrival makes one route grow, while incompatible routes lose mass?**

Three sender points emit jittered event trains with periods `17`, `23`, and `31` steps. Six downstream points exist with receiver periods:

```text
[31, 17, 27, 23, 41, DEAD]
```

The matching targets are deliberately permuted. Every sender initially has a candidate edge to every receiver.

Each edge carries:

```text
mass m_ij     slow structural commitment
delay d_ij    stand-in for path length / conduction delay
```

Each sender has a fixed material budget:

```text
sum_j m_ij = 1
```

During development, candidate paths make exploratory length changes. A proposal survives only when delayed sender events become more compatible with the receiver's oscillatory gate. Structural mass then competes across outgoing edges.

Twelve-seed held-out result:

| arm | top-1 correct target | correct mass | top-edge compatibility | mass entropy |
|---|---:|---:|---:|---:|
| static random | 0.3333 | 0.1667 | 0.1210 | 1.0000 |
| mass only | 0.3333 | 0.4271 | 0.2291 | 0.6931 |
| length only | 0.3333 | 0.1667 | 0.3103 | 1.0000 |
| **mass + length self-wiring** | **1.0000** | **0.9997** | **0.9270** | **0.0014** |
| digital exhaustive oracle | 1.0000 | 0.9999 | 0.9272 | 0.0005 |
| destroyed phase coherence | 0.4444 | 0.2060 | 0.0147 | 0.9751 |

The non-oscillating receiver receives essentially zero final mass in the self-wiring arm.

The ablation is the point:

```text
length adaptation without mass
    can improve timing but cannot create topology

mass adaptation without length
    cannot reliably rescue an initially wrong conduction phase

length + mass
    finds a workable arrival phase and consolidates the route
```

Destroy persistent receiver phase relationships and the graph stays almost diffuse.

The exhaustive digital delay search is still slightly cleaner than the developmental toy, so there is no algorithmic superiority claim.

Surviving claim:

> **Geometry/delay can determine whether a route is temporally viable, and a finite structural budget can turn repeated local viability into persistent sparse wiring.**

Full receipt: `results/GATE1.md`.

---

# What the "matrix" means now

At any instant we can still write a matrix, but it is no longer one thing:

```text
M           slow structural topology / mass
W           slower learned synaptic efficacy
G(t)        fast dynamical gate

W_eff(t) = M ⊙ W ⊙ G(t)
```

The useful conceptual split is:

```text
STRUCTURE
what can connect?

SLOW WEIGHT
what usually matters?

FAST STATE
what matters right now?

DEVELOPMENT
which repeatedly useful fast interactions deserve permanent structure?
```

That is the bridge between the oscillating-point experiment and the self-growing-matrix thought.

---

# Why length matters

If a path has propagation delay

```text
tau = L / v
```

then changing length changes arrival phase:

```text
Delta phi = omega * Delta L / v
```

So path growth is not merely "more wire." In this abstraction it changes the temporal relation between sender and receiver.

That is why Gate 1 lets edge geometry/delay adapt separately from edge mass.

---

# Current kill conditions

Demote the idea if:

- sparse wiring appears even when persistent phase coherence is destroyed;
- mass competition alone does everything;
- delay plasticity adds nothing;
- a non-oscillating receiver is reinforced anyway;
- the effect requires source/target labels during development;
- ordinary sparse adaptive filtering learns the same useful graph more simply;
- later task utility shows that synchronization merely preserves synchrony rather than useful information.

The final one is now the important test.

---

# Next

Gate 1 makes "phase compatibility" itself worth preserving. That is too easy.

The next attack should create **multiple phase-compatible routes**, only some of which help prediction or control.

Then ask:

> **Can local fast coherence propose structure while slower task utility decides which coherent path actually earns mass?**

That would separate

```text
can communicate
```

from

```text
is worth wiring.
```

Only after that is it worth returning to local oscillator synchronization, drifting clocks, dendritic state, or a GPU-hostile sparse implementation.

---

# Run

```bash
python -m pip install -r requirements.txt
python experiments/gate0_relative_phase_routing.py
python experiments/gate1_self_wiring_phase_graph.py
python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **A dynamical graph can have fast effective connectivity and slow structural connectivity. In the toy tested here, repeated phase-compatible traffic can tune propagation delay and consolidate scarce edge mass into a sparse persistent graph. Fast routing can compile into slow wiring.**
