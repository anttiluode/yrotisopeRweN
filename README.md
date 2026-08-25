# yrotisopeRweN — the continuously growing matrix under the point

`NewRepository` backwards.

**Read `MAINLINE.md` before extending this repo.**

This is a falsification-first computational abstraction, not a biological neuron simulator.

The main hypothesis now reads:

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
 -> recurrent traffic
 -> grow the recurrent loop
```

A differentiation side branch remains:

```text
Oja -> Sanger/GHA -> AMUSE
```

Useful machinery, not the current destination.

---

# The object now

Externally:

```text
●
```

Internally one point carries several distinct states:

```text
Z(t)    local computational state
E(t)    delayed-credit / eligibility state
M       persistent structural allocation
```

and its output can enter other continuously running points and later return.

The latest architectural correction is therefore stronger than "output does not reset the neuron":

> **some state can live inside a point, while other state can live in circulating traffic between points.**

---

# Main-line gates

| gate | isolated question | surviving result |
|---|---|---|
| 0 | Can receiver state alter which broadcast matters now? | yes; receiver-relative fast state can gate temporally structured input |
| 1 | Can timing/geometry write persistent structure? | delay + finite mass can turn temporal viability into sparse routing |
| 2 | Is coherence itself purpose? | no: coherence says CAN, consequence says KEEP |
| 3 | What does bounded growth buy? | a bound turns amplification into allocation |
| 6 | Can fixed slow structure compute different relations? | yes, if fast state selects among nonlinear conjunctions; scalar switch ties phase |
| 7 | Can vanished context change a later identical input? | yes through transient receiver state; scalar recurrence ties/slightly wins |
| 8 | Can delayed consequence credit vanished conjunctions? | yes if eligibility still addresses what happened |
| 9 | Can positive-only growth retract obsolete structure? | conserved capacity supplies retraction; reserve preserves plasticity |
| 10 | Can a whole matrix grow without supplied rivals? | yes: one global budget grows a sparse matrix and later reallocates it |
| 11 | Does the cell survive without trial resets? | yes: local state, eligibility and mass coexist while output is emitted |
| 12 | Can state live in literal recurrent traffic? | yes: A<->B holds a vanished cue; cut return kills it |
| 13 | Can diffuse matrix capacity grow the useful loop? | yes: recurrence grows only when persistence is useful |

Receipts: `results/GATE0.md` through `results/GATE13.md`.

---

# Gate 11 — continuous cell

Each candidate relation becomes a continuously driven local state:

```text
Q_ij(t) = A_i(t) B_j(t)
Z_ij(t+1) = alpha_ij Z_ij(t) + (1-alpha_ij) Q_ij(t)
```

with a separate eligibility trace and conserved structural mass.

The cell can emit without clearing its internal computation.

Six seeds, 30,000 uninterrupted steps:

```text
phase-1 voltage NMSE       0.01010
phase-2 voltage NMSE       0.00993
phase-1 output F1          0.9551
phase-2 output F1          0.9547
phase-2 useful mass        0.9112
```

A boring exact delay-buffer + signed update is much better.

Receipt: `results/GATE11.md`.

---

# Gate 12 — recurrent traffic

Freeze structural matrices and ask only whether recurrence matters.

```text
brief cue -> Cell A -> Cell B -> back to A
              ^                 |
              +-----------------+
```

The cue enters only A for ten steps, disappears, and later an opposite cue must overwrite the state.

Twelve seeds:

```text
full loop
first cue-free hold        1.0000
second hold after flip     1.0000
A state                    +0.9068 -> -0.9068

cut B -> A return
hold accuracy              0.0000
state                      ~0

scramble return timing
first hold                 1.0000
second overwrite           0.0000

low loop gain
hold accuracy              0.0000
```

Important correction: make every local matrix compartment instantaneous and the recurrent loop still holds perfectly. For this toy, the memory can live in network recurrence rather than local persistence.

A one-scalar recurrent unit also solves it perfectly.

Receipt: `results/GATE12.md`.

---

# Gate 13 — grow the loop

Now remove the hand-set recurrent mass.

Both points begin with diffuse `6 x 6` matrices:

```text
M_ij = 1/36
```

A brief alternating cue enters A every 180 steps. In the memory world the desired signed state must survive after the cue is gone.

Delayed consequence acts through each cell's eligibility trace; only positive local growth evidence is allowed; conserved capacity supplies retraction.

Six seeds, 15,000 continuous steps:

```text
memory-required world
late cue-free accuracy     1.0000
A direct-cue mass          0.5508
A B->A return mass         0.4152
B A->B forwarding mass     0.9650
closed-loop mass           0.4152
first >.90 memory          1560 +/- 85 steps
```

Kills:

```text
no learning
late memory                0.0000
closed-loop mass           0.0278

shuffled eligibility
late memory                0.0000
closed-loop mass           0.0234
```

The causal control is the important result.

Use the same cue stream and the same available feedback, but require output only while the cue is physically present. Persistence is now useless:

```text
no-memory world
A direct-cue mass          0.9231
A return mass              0.0020
B forwarding mass          0.1367
closed-loop mass           0.0020
```

So feedback does not automatically claim structural capacity. The return leg grows only when the consequence requires state to survive between cues.

Receipt: `results/GATE13.md`.

---

# Why Aizenbud + Leterrier entered here

Aizenbud et al. (PNAS 2026) motivated treating dendritic complexity as extended, compartmentalized, nonlinear integration rather than simply counting branches.

Leterrier's AIS review (J. Neurosci. 2018) motivated separating continuously evolving internal computation from an output/broadcast boundary.

They do **not** validate our equations, matrix representation, eligibility rule, mass conservation, or recurrent-learning mechanism. Gate 12/13 are generic recurrent computation tests, not hippocampal models.

---

# Differentiation side branch

Gate 4: independent Oja points duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: when identity exists only in lagged statistics, AMUSE can recover it. Shuffle time or equalize temporal laws and it fails.

Do not continue to SOBI unless a future wall genuinely needs several lags.

---

# What is next

Gate 13 still contains one enormous convenience:

```text
matrix coordinate (1,0)
= peer broadcast x constant carrier
```

The learner does not have to discover *which incoming traffic is the useful return*; we named the coordinate for it.

So do **not** scale to a giant recurrent network yet.

Next attack:

```text
several generic return channels
stale / irrelevant / noisy broadcasts mixed in
small generic nonlinear local field
        ↓
finite consequence-driven growth
        ↓
can the matrix discover which returning traffic deserves capacity?
```

Controls must include a no-memory world, shuffled channel identity, shuffled eligibility, cut-after-growth, and an ordinary trained recurrent attacker.

Only if recurrence can be selected without a hand-labelled peer coordinate should the network expand beyond two points.

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
python experiments/gate12_recurrent_loop.py
python experiments/gate13_grow_the_loop.py

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **A continuously running point can keep local computational state while broadcasting; recurrent traffic between points can itself carry state; and when persistence matters, delayed consequence acting under finite structural capacity can grow a closed recurrent path from diffuse matrix mass. The next question is whether the system can discover useful returning traffic without being handed a named recurrent coordinate.**
