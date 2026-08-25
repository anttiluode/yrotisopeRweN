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
 -> growing sparse structure
 -> continuous internal dynamics
 -> recurrent traffic
 -> grow the recurrent loop
 -> discover useful returning traffic
 -> select it in generic stable coordinates
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

State can therefore live:

```text
inside a point
between points in recurrent traffic
in slow structural investment
```

The latest correction is that structural investment no longer needs semantically named internal axes. It can live in a fixed generic mixed coordinate system as long as those coordinates remain stable over time.

---

# Main-line gates

| gate | isolated question | surviving result |
|---|---|---|
| 0 | Can receiver state alter which broadcast matters now? | yes; receiver-relative fast state can gate temporally structured input |
| 1 | Can timing/geometry write persistent structure? | delay + finite mass can turn temporal viability into sparse routing |
| 2 | Is coherence itself purpose? | no: coherence says CAN, consequence says KEEP |
| 3 | What does bounded growth buy? | a bound turns amplification into allocation |
| 6 | Can fixed slow structure compute different relations? | yes; scalar switch ties phase, so phase is only a coordinate |
| 7 | Can vanished context change later identical input? | yes through transient receiver state |
| 8 | Can delayed consequence credit vanished conjunctions? | yes if eligibility still addresses them |
| 9 | Can positive-only growth retract obsolete structure? | conserved capacity supplies retraction; reserve preserves plasticity |
| 10 | Can a whole matrix grow without supplied rivals? | yes: one global budget grows and reallocates sparse structure |
| 11 | Does the cell survive without trial resets? | yes: computation, eligibility and structure coexist while output is emitted |
| 12 | Can state live in literal recurrent traffic? | yes: A<->B holds a vanished cue; cut return kills it |
| 13 | Can diffuse capacity grow a useful loop? | yes: recurrence grows only when persistence is useful |
| 14 | Can useful return traffic be discovered without a named peer channel? | yes if incoming address is stable |
| 15 | Can recurrence grow without hand-designed internal coordinates? | yes in a fixed dense random basis; stable internal address is the requirement |

Full receipts are in `results/GATE0.md` through `results/GATE15.md`.

---

# Gates 12–15: from recurrent traffic to coordinate-agnostic growth

## Gate 12 — recurrent traffic

Freeze structure. A brief cue enters A, then disappears while A and B continue broadcasting into each other.

```text
full loop hold/overwrite      1.0000
cut B->A return               0.0000
scrambled return timing       old state persists; overwrite fails
low loop gain                 state collapses
```

Instantaneous local compartments still work, so state can live in network recurrence itself.

Receipt: `results/GATE12.md`.

## Gate 13 — grow the loop

Start both points with diffuse structural capacity.

When persistence is useful:

```text
late cue-free accuracy        1.0000
A direct-cue mass             0.5508
A B->A return mass            0.4152
B A->B forwarding mass        0.9650
```

When persistence is not useful, A spends almost all capacity on direct cue and the loop remains open.

Receipt: `results/GATE13.md`.

## Gate 14 — anonymous return

Remove the label `peer return`. One of several stable anonymous input streams happens to carry the current peer output.

Stable addresses let the loop grow. Randomly reshuffling input-channel identity every timestep destroys it.

Surviving statement:

> **feedback does not need a semantic label, but useful returning traffic needs a persistent external address.**

Receipt: `results/GATE14.md`.

## Gate 15 — generic internal basis

Now remove the direct channel-to-structural-coordinate mapping.

Each point gets a fixed dense random projection of all six incoming streams. Every internal feature mixes every raw channel.

Default 24-feature field, three seeds:

```text
late cue-free memory              1.0000
A effective occupied features    4.83
B effective occupied features    3.05
max raw-channel loading          ~0.56
```

Scramble the **internal feature addresses** every timestep while leaving the same feature set available:

```text
late memory                       0.00283
```

Shuffle eligibility:

```text
late memory                       0.0000
```

No learning:

```text
late memory                       0.0000
```

Grow the generic field and then cut the recurrent returns while freezing learning:

```text
late memory                       0.0352
```

Two important negative results:

```text
linear random basis               1.0000
only six mixed features           1.0000
```

So Gate 15 does **not** earn nonlinear random features or overcompleteness.

It earns something smaller:

> **semantic internal coordinates are unnecessary; persistent internal addressability is necessary.**

For the linear case, the system is simply learning an effective direction expressed as finite positive mass over fixed random directions. A conventional recurrent network with signed trainable weights is still the simpler engineering solution.

Receipt: `results/GATE15.md`.

---

# Biology papers

Aizenbud et al. (PNAS 2026) motivated treating dendritic complexity as extended, compartmentalized integration rather than simply counting branches.

Leterrier's AIS review (J. Neurosci. 2018) motivated separating continuously evolving internal computation from an output/broadcast boundary.

They do **not** validate our equations, matrix representation, eligibility rule, mass conservation, recurrent-learning mechanism, or any hippocampal interpretation.

The recurrent gates are generic computational tests.

---

# Differentiation side branch

Gate 4: independent Oja points duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: when identity exists only in lagged statistics, AMUSE can recover it. Shuffle time or equalize temporal laws and it fails.

Do not continue to SOBI unless a future wall genuinely needs several lags.

---

# Next

Gate 15 has removed the hand-designed local coordinate basis far enough that the earlier roadmap now permits a scale change.

Next clean attack:

```text
4-8 continuously running points
        ↓
many stable anonymous broadcasts
        ↓
generic local coordinate fields
        ↓
finite structural capacity at each point
        ↓
only some possible recurrent loops help the task
```

The task should require one or a few temporary states while providing many useless possible loops. Success is **not** merely memory accuracy; the grown recurrent subgraph should remain selective.

Controls:

```text
remove persistence requirement
cut selected loops after growth
shuffle structural addresses
shuffle eligibility
ordinary small trained RNN attacker
```

Do not simultaneously add learned geometry, a new dendritic mechanism, or another credit rule.

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
python experiments/gate15_generic_basis.py

python -m unittest discover -s tests -v
```

Only NumPy is required.

---

# Current surviving sentence

> **A continuously running point can keep local state while broadcasting; recurrent traffic can carry state between points; finite consequence-driven growth can build recurrent structure when persistence is useful; useful return traffic need not be pre-named; and even the internal computational axes can be generic mixtures. What must remain stable is addressability itself, so delayed credit and structural investment keep referring to the same local computation.**
