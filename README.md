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

# Gate 2 — coherence says can; utility says keep

Gate 1 still had a cheat: the connection that synchronized best was, by construction, the connection we wanted.

Gate 2 removes that convenience. Each sender now has **two receiver twins with identical oscillatory timing**. Phase coherence cannot distinguish them. The twins differ only in downstream consequence: one helps a 3-D prediction/control target and the other pushes the same output in the wrong direction.

The graph gets no correct-edge label. Delay growth still uses phase compatibility only. Structural mass additionally receives an error-modulated eligibility signal telling it whether more of an edge would reduce the current task residual.

Twelve-seed held-out result:

| arm | useful mass | target correlation |
|---|---:|---:|
| phase only | 0.4877 | 0.0158 |
| utility only | 0.3720 | 0.2436 |
| **phase + utility** | **0.9992** | **0.9061** |
| destroyed utility | 0.4846 | 0.0023 |
| digital oracle | 1.0000 | 0.9248 |

The full graph chooses the useful twin for all three senders on all 12 seeds. Phase-only finds the compatible pair but remains almost exactly 50/50 between useful and harmful twins. Destroying the utility signal leaves the same 50/50 ambiguity. Utility-only cannot reliably discover routes because timing remains wrong.

So the new decomposition is:

```text
PHASE / DELAY
can this route communicate?

TASK UTILITY
is that communication useful?

MASS
is it worth preserving this route?
```

Full receipt: `results/GATE2.md`. Raw metrics: `results/gate2_metrics.json`.

---

# Gate 3 — Oja under the oscillating point

The "point matrix" idea now has a concrete two-dimensional version. Lift local arrival energy into an in-phase/quadrature subspace:

```text
u(t) = sqrt(e(t)) [cos(phi(t)), sin(phi(t))]
```

A slow vector `w=[cos(theta), sin(theta)]` is then a preferred phase **axis**. Oja's rule

```text
y = w^T u
Delta w = eta * y * (u - y w)
```

rotates that axis toward persistent phase-conditioned energy while preventing ordinary Hebbian positive feedback from blowing the weight norm up.

This is the precise relation to the old "keep the pipes from growing too large" intuition: **the normalising term is what turns growth into a choice of direction.** A finite structural-mass budget has the same resource-competition flavour, but it is not literally Oja's update.

Twelve-seed result:

| arm / quantity | result |
|---|---:|
| plain Hebb | hits `1e6` norm guard in 12/12 runs |
| Oja final norm | `1.000059 ± 0.000027` |
| Oja phase-axis alignment | `0.999929 ± 0.000078` |
| linear opposite outputs | recovery `0.7017`, duplication `1.0000` |
| **Oja axis + nonlinear phase windows** | **recovery `0.9944 ± 0.0006`**, duplication `0.0162` |
| same-phase kill world | recovery `0.3979` |

The limitation is as useful as the win. Oja/PCA learns an **axis**, so `theta` and `theta+pi` are the same covariance direction. Two linear outputs at opposite ends are merely negatives of one another. A nonnegative local gate is what makes the two ends computationally distinct.

So the current decomposition is:

```text
FAST PHASE       where is the arrival now?
OJA              which direction has persisted?
NONLINEARITY     which side / conjunction is effective?
UTILITY          did it help?
MASS / GEOMETRY  should the relation persist physically?
```

Full receipt: `results/GATE3.md`. Raw metrics: `results/gate3_oja_metrics.json`.


---

# Next

Gate 2 is still a one-shot developmental world. Once the right path hardens, the environment stays put.

The next attack should **reverse which coherent twin is useful after consolidation**.

Ask whether the graph can retract obsolete structure and regrow an alternative without either freezing forever or dissolving its useful wiring. That is a stability-plasticity test, and it makes "exploratory mass" an actual computational quantity rather than decoration.

Only after that should we return to local oscillator synchronization, no supplied clock, dendritic state, or GPU-hostile sparse execution.

---

# Run

```bash
python -m pip install -r requirements.txt
python experiments/gate0_relative_phase_routing.py
python experiments/gate1_self_wiring_phase_graph.py
python experiments/gate2_useful_coherence.py
python experiments/gate3_oja_phase_axis.py
python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **A dynamical point can carry a fast relational coordinate, a slowly learned selection axis, and still slower structural commitment. Oja shows how normalised growth can become directional selection; phase says what fits now, utility says what helped, and mass/geometry says what should persist.**
