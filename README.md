# yrotisopeRweN — the continuously growing matrix under the point

`NewRepository` backwards.

**Read `MAINLINE.md` before extending this repo.**

This is a falsification-first computational abstraction, not a biological neuron simulator.

The main hypothesis currently reads:

```text
broadcast
 -> receiver-relative fit
 -> nonlinear composition
 -> receiver-carried context
 -> delayed consequence
 -> finite allocation
 -> growing sparse matrix
 -> continuous internal dynamics
 -> output / broadcast
 -> ? recurrent loop
```

A differentiation side branch remains in the repo:

```text
Oja -> Sanger/GHA -> AMUSE
```

It is useful machinery, but not the current destination.

---

# The object now

Externally the abstraction can still be drawn as a point:

```text
●
```

Internally it now has three distinct persistent variables:

```text
Z(t)    fast/local computational state
E(t)    slower eligibility / credit state
M       persistent structural allocation
```

and a separate output boundary.

At any moment many broadcasts may already have contributed to `Z(t)`, old events may still be represented in `E(t)`, and structural mass `M` may still be reallocating from older experience.

The latest important correction is:

> **output does not mean the internal computation has ended.**

---

# Main-line gates

| gate | isolated question | surviving result |
|---|---|---|
| 0 | Can receiver state alter which broadcast matters now? | receiver-relative fast state can gate temporally structured input; digital features slightly win |
| 1 | Can timing/geometry write persistent structure? | delay + finite mass can turn temporal viability into sparse routing |
| 2 | Is coherence itself purpose? | no: coherence says CAN, consequence says KEEP |
| 3 | What does bounded growth buy? | a bound turns amplification into allocation |
| 6 | Can fixed slow structure compute different relations? | yes, if fast state selects among nonlinear conjunctions; scalar mode switch ties phase |
| 7 | Can vanished context change a later identical input? | yes, through transient receiver state; scalar recurrent state ties/slightly wins |
| 8 | Can delayed consequence credit vanished conjunctions? | yes, if an eligibility trace still addresses what happened |
| 9 | Can positive-only growth retract obsolete structure? | finite conserved capacity supplies retraction; reserve preserves plasticity |
| 10 | Can a whole matrix grow without supplied rival pairs? | yes: one global budget grows a sparse matrix and later reallocates it elsewhere |
| 11 | Does the growing cell survive without trial resets? | yes: continuous local state, eligibility and mass coexist while output is emitted |

Full receipts are in `results/GATE0.md` through `results/GATE11.md`.

---

# Gate 10 — growing the matrix

Gate 10 replaces hand-written rival pairs with a dense `6 x 6` field of possible relations:

```text
Q_ij = A_i * B_j
```

All 36 cells share one conserved capacity pool.

Four useful cells acquire about `96.8%` of total mass. When utility moves to four completely disjoint cells, the old sparse matrix dissolves and a new sparse matrix grows elsewhere.

This is the repo's current meaning of **structural growth**:

```text
many possible local computations
        ↓
finite structural budget
        ↓
useful traffic claims capacity
        ↓
effective matrix becomes sparse
        ↓
changed utility moves the investment
```

Receipt: `results/GATE10.md`.

---

# Gate 11 — the loop does not reset

Gate 10 still treated the world like isolated samples. Gate 11 removes that convenience.

Each candidate relation is now a continuously driven leaky local compartment:

```text
Q_ij(t) = A_i(t) B_j(t)
Z_ij(t+1) = alpha_ij Z_ij(t) + (1-alpha_ij) Q_ij(t)
```

with heterogeneous fixed decay constants.

Structural mass remains globally conserved, eligibility runs continuously, and a separate thresholded output observes the ongoing somatic-like readout:

```text
V(t) = sum_ij M_ij Z_ij(t)
```

Output does **not** clear the local state or eligibility.

Six seeds, `30,000` uninterrupted steps:

```text
continuous cell
phase-1 voltage NMSE       0.01010
phase-2 voltage NMSE       0.00993
phase-1 output F1          0.9551
phase-2 output F1          0.9547
phase-1 useful mass        0.9095
phase-2 useful mass        0.9112
new matrix > .90           8334 +/- 924 steps, 6/6 seeds
```

Kills:

```text
no consequence
    -> phase-2 NMSE 6.4021

shuffled eligibility
    -> phase-2 NMSE 0.8724
    -> no .90 reallocation

no separate eligibility trace
    -> phase-2 NMSE 1.4461
    -> local computational state is not enough for delayed credit

reset local state whenever output fires
    -> phase-2 NMSE 0.0774
    -> final new mass 0.8314
    -> no .90 reallocation

make all compartments instantaneous
    -> phase-2 NMSE 0.0928
    -> final new mass 0.7379
```

A boring exact delay-buffer plus signed-gradient attacker wins strongly:

```text
phase-1 NMSE        0.000113
phase-2 NMSE        0.000114
phase-2 useful mass 0.9931
adaptation           3952 +/- 631 steps
```

So this is not an optimizer claim.

The surviving architecture is:

> **local state computes; eligibility remembers credit; structural mass remembers investment; output is a boundary rather than an episode terminator.**

Receipt: `results/GATE11.md`.

---

# Why Aizenbud + Leterrier entered here

The papers were introduced after the computational chain existed, rather than being used to decorate it.

Aizenbud et al. (PNAS 2026) link single-neuron functional complexity to dendritic extent/area, branching organization and nonlinear synaptic integration. The useful lesson for this abstraction is not “grow lots of branches,” but that extended, compartmentalized, nonlinear local integration can matter.

Leterrier's AIS review (J. Neurosci. 2018) emphasizes a specialized output compartment that generates/shapes action potentials and separates somatodendritic from axonal organization, while itself exhibiting activity-dependent plasticity.

Together they motivated a modest computational separation:

```text
continuously evolving internal computation
        ↓
separate output boundary
        ↓
broadcast
```

Neither paper validates the equations used here or implies that biological neurons implement a `6 x 6` matrix.

---

# Differentiation side branch

Gate 4: independent Oja points duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: when source identity exists only in lagged statistics, AMUSE can recover it. Shuffle time or equalize temporal laws and it fails.

Do not continue to SOBI unless a future problem genuinely requires several lags.

---

# Next

Gate 11 removed the artificial trial reset, but it has **not yet created a literal recurrent neural loop**.

The next clean attack is therefore:

```text
continuous growing Cell A
        ↓ broadcast
continuous growing Cell B
        ↓ broadcast
back toward A
```

External signals should enter while recurrent traffic is already circulating.

For that gate, keep the supplied product coordinates `A_i * B_j`. Do not simultaneously remove the feature scaffold; otherwise failure is uninterpretable.

Kill the return path, scramble its timing, reset state on output, shuffle eligibility, and keep an ordinary small recurrent/signed-gradient attacker in the room.

Only if the recurrent loop survives should the known relation coordinates be removed.

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

# main hypothesis
python experiments/gate6_receiver_state_composition.py
python experiments/gate7_context_memory.py
python experiments/gate8_delayed_consequence.py
python experiments/gate9_capacity_reversal.py
python experiments/gate10_growing_matrix.py
python experiments/gate11_continuous_loop.py

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **The sender broadcasts into a continuously occupied receiver. Local state decides what current and recent activity can compose; eligibility carries delayed causal credit; finite structural capacity grows a sparse effective matrix; an output event can broadcast onward without clearing the internal computation. The next question is whether several such continuously running points can form a recurrent loop that remains learnable and plastic.**
