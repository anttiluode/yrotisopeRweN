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
 -> recurrent traffic
 -> grow the recurrent loop
 -> discover useful returning traffic
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

Internally:

```text
Z(t)    local computational state
E(t)    eligibility / delayed-credit state
M       persistent structural allocation
```

and output can enter other continuously running points and later return.

So state can live in more than one place:

```text
inside a point
between points in recurrent traffic
in slow structural investment
```

---

# Main-line gates

| gate | isolated question | surviving result |
|---|---|---|
| 0 | Can receiver state alter which broadcast matters now? | yes; receiver-relative fast state can gate temporally structured input |
| 1 | Can timing/geometry write persistent structure? | delay + finite mass can turn temporal viability into sparse routing |
| 2 | Is coherence itself purpose? | no: coherence says CAN, consequence says KEEP |
| 3 | What does bounded growth buy? | a bound turns amplification into allocation |
| 6 | Can fixed slow structure compute different relations? | yes, if fast state selects nonlinear conjunctions; scalar switch ties phase |
| 7 | Can vanished context change later identical input? | yes through transient receiver state |
| 8 | Can delayed consequence credit vanished conjunctions? | yes if eligibility still addresses them |
| 9 | Can positive-only growth retract obsolete structure? | conserved capacity supplies retraction; reserve preserves plasticity |
| 10 | Can a whole matrix grow without supplied rivals? | yes: one global budget grows and reallocates a sparse matrix |
| 11 | Does the cell survive without trial resets? | yes: computation, eligibility and structure coexist while output is emitted |
| 12 | Can state live in literal recurrent traffic? | yes: A<->B holds a vanished cue; cut return kills it |
| 13 | Can diffuse matrix capacity grow a useful loop? | yes: recurrence grows only when persistence is useful |
| 14 | Can useful return traffic be discovered without a named peer channel? | yes if the incoming channel identity is stable |

Full receipts are in `results/GATE0.md` through `results/GATE14.md`.

---

# Gates 11–14: from continuous cell to grown recurrence

## Gate 11 — continuous cell

Remove trial resets. Matrix cells keep local state, eligibility keeps delayed credit, and structural mass keeps long-term investment while output continues.

```text
Z(t) computes
E(t) assigns delayed credit
M remembers structural investment
```

Output is a boundary, not an episode terminator.

Receipt: `results/GATE11.md`.

## Gate 12 — recurrent traffic

Freeze structure and let two continuously running cells broadcast into each other.

```text
brief cue -> A -> B -> A -> B -> ...
```

The cue disappears but the loop keeps its sign. A later opposite cue flips the state.

```text
full loop hold/overwrite      1.0000
cut B->A return               0.0000
scrambled return timing       old state persists; overwrite fails
low loop gain                 state collapses
```

Make every local compartment instantaneous and the loop still works. For this toy, state can live in recurrence itself.

A one-scalar recurrent unit solves the same task perfectly.

Receipt: `results/GATE12.md`.

## Gate 13 — grow the loop

Start both cells with diffuse `6 x 6` structural mass.

When the cue's sign must survive between brief presentations:

```text
late cue-free accuracy        1.0000
A direct-cue mass             0.5508
A B->A return mass            0.4152
B A->B forwarding mass        0.9650
closed-loop mass              0.4152
```

No learning or shuffled eligibility gives zero late memory.

In the same cue stream with no persistence requirement:

```text
A direct-cue mass             0.9231
A return mass                 0.0020
closed-loop mass              0.0020
```

So feedback availability alone does not force recurrent structure. Persistence utility does.

Receipt: `results/GATE13.md`.

## Gate 14 — anonymous return channels

Now remove the label "peer return."

Each cell receives four generic incoming return streams in a random fixed permutation per seed:

```text
one current peer broadcast
three unrelated low-amplitude streams
```

The growth rule is not told which is which.

Stable identities:

```text
late memory                   1.0000
A useful return mass          0.4928
B useful return mass          0.9650
A best irrelevant return      0.00103
closed-loop mass              0.4928
```

Randomly reshuffle channel identity every timestep:

```text
late memory                   0.0501
A useful-return mass          0.00161
closed-loop mass              0.00161
A direct-cue mass             0.9630
```

Shuffle eligibility:

```text
late memory                   0.0000
closed-loop mass              0.0266
```

No-memory control:

```text
A direct-cue mass             0.8650
A useful-return mass          0.00223
closed-loop mass              0.00223
```

So the matrix does not need a semantic symbol called "feedback," but it does need a **stable structural address** that repeatedly carries useful returning traffic.

Cut the useful return after growth and memory degrades while continued learning reallocates A back toward direct cue.

Receipt: `results/GATE14.md`.

---

# Biology papers

Aizenbud et al. (PNAS 2026) motivated treating dendritic complexity as extended, compartmentalized, nonlinear integration rather than simply counting branches.

Leterrier's AIS review (J. Neurosci. 2018) motivated separating continuously evolving internal computation from an output/broadcast boundary.

They do **not** validate our equations, matrix representation, eligibility rule, mass conservation, recurrent-learning mechanism, or any hippocampal interpretation.

The recurrent gates here are generic computational tests.

---

# Differentiation side branch

Gate 4: independent Oja points duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: when identity exists only in lagged statistics, AMUSE can recover it. Shuffle time or equalize temporal laws and it fails.

Do not continue to SOBI unless a future wall genuinely needs several lags.

---

# Next

Gate 14 removed the semantic label from the useful recurrent channel, but every incoming process still maps directly to a simple known coordinate.

That coordinate basis is now the largest scaffold.

Next attack:

```text
stable incoming processes
        ↓
random mixtures / generic overcomplete local nonlinear coordinates
        ↓
no coordinate is "the return channel"
        ↓
consequence + eligibility + finite growth
        ↓
can a useful recurrent computational subspace acquire structural capacity?
```

Keep the loop at two points while attacking this. Do not simultaneously scale to a larger network.

Controls should include a no-memory world, time-varying coordinate shuffle, shuffled eligibility, cut-after-growth, and an ordinary trained recurrent attacker.

Only if useful recurrence survives without hand-designed coordinates should the network expand.

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
python experiments/gate14_anonymous_return.py

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **A continuously running point can keep local state while broadcasting; recurrent traffic between points can itself carry state; finite consequence-driven growth can build the recurrent path when persistence is useful; and the useful return need not be pre-named, but it must occupy a stable structural address long enough for consequence to consolidate it. The next wall is whether that useful recurrent computation can be selected when even the local coordinate basis is generic rather than supplied.**
