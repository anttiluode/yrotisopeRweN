# yrotisopeRweN — main hypothesis compass

This file exists because well-paved side roads are gravitational.

The differentiation branch remains useful but is not the destination:

```text
Oja -> Sanger/GHA -> AMUSE
```

The main hypothesis is:

> **The sender broadcasts. The receiver decides whether an arrival belongs here; local dynamics decide what it becomes when combined with what is already here; consequence decides whether that temporary relation deserves persistent capacity.**

The current main line is:

```text
BROADCAST
 -> RECEIVER-RELATIVE FIT
 -> COMPOSE
 -> CONTEXT
 -> CONSEQUENCE
 -> FINITE ALLOCATION
 -> GROW SPARSE MATRIX
 -> CONTINUOUS INTERNAL STATE
 -> RECURRENT TRAFFIC
 -> GROW THE LOOP
 -> DISCOVER USEFUL RETURNING TRAFFIC
```

---

# Main-line receipts

## Gate 0 — receiver-relative fit
Receiver-specific fast state can change which temporally structured arrivals are effective. Digital phase features slightly win.

## Gate 1 — timing can write structure
Delay/path state plus finite mass can turn repeated temporal viability into sparse routing.

## Gate 2 — coherence says CAN; consequence says KEEP
Timing-compatible routes can have opposite downstream effects. Coherence alone is not purpose.

## Gate 3 — bounded growth becomes allocation
Oja supplies one exact example of the principle that correlated growth plus a bound becomes selection rather than unlimited amplification.

## Gate 6 — COMPOSE
The same fixed nonlinear bank computes different relations when only fast receiver state changes. A scalar switch ties phase.

## Gate 7 — CONTEXT
An earlier event can disappear while leftover receiver state changes how a later identical broadcast is composed.

## Gate 8 — CONSEQUENCE
Delayed consequence needs a surviving eligibility address for the transient relation that occurred earlier.

## Gate 9 — reversible consolidation
Positive-only growth plus conserved capacity can retract obsolete allocation; a small reserve preserves plasticity.

## Gate 10 — GROWING MATRIX
One shared budget over a dense `6 x 6` relation field grows a sparse effective matrix and later reallocates it elsewhere without supplied rival pairs.

## Gate 11 — CONTINUOUS CELL
Remove trial resets. Local computational state `Z(t)`, credit state `E(t)`, and structural mass `M` coexist while output is emitted.

```text
Z(t)    computes
E(t)    carries delayed credit
M       remembers structural investment
```

Output is a boundary, not an episode terminator.

## Gate 12 — RECURRENT TRAFFIC
Freeze structure and make two continuously running points broadcast into each other.

A brief cue enters A, disappears, and the A<->B loop holds it; a later opposite cue overwrites it.

```text
full loop hold/overwrite accuracy     1.0000
cut B->A return                       0.0000
scramble return timing                old state persists, overwrite fails
low loop gain                         state collapses
```

Make every local matrix compartment instantaneous and the loop still works. State can therefore live in network recurrence rather than inside one point.

A one-scalar recurrent unit solves the same toy perfectly.

Receipt: `results/GATE12.md`.

## Gate 13 — GROW THE LOOP
Start both cells with diffuse `6 x 6` structural mass. Brief alternating cues enter A; the task requires the signed state to persist between cues.

Delayed consequence plus eligibility reallocates finite matrix capacity into a closed path:

```text
late cue-free accuracy        1.0000
A direct-cue mass             0.5508
A B->A return mass            0.4152
B A->B forwarding mass        0.9650
closed-loop mass              0.4152
```

No learning or shuffled eligibility gives zero late memory.

In the same cue stream with **no persistence requirement**:

```text
A direct-cue mass             0.9231
A return mass                 0.0020
closed-loop mass              0.0020
```

So feedback availability alone does not force a loop. Recurrence claims capacity when persistence is useful.

Receipt: `results/GATE13.md`.

## Gate 14 — ANONYMOUS RETURN
Gate 13 still named one coordinate "peer return." Gate 14 gives each cell four generic return channels in a random fixed permutation per seed:

```text
one current peer stream
three unrelated streams
```

The growth rule is not told which is which.

With stable channel identities:

```text
late cue-free accuracy        1.0000
A useful return mass          0.4928
B useful return mass          0.9650
A best irrelevant return      0.00103
closed-loop mass              0.4928
```

Reshuffle channel identity every timestep:

```text
late memory                   0.0501
A useful-return mass          0.00161
closed-loop mass              0.00161
A direct-cue mass             0.9630
```

Shuffle eligibility instead:

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

Cut the useful return after growth and memory degrades while the matrix begins reallocating back toward direct cue.

The surviving condition is now sharper:

> **Useful recurrence does not need a pre-named feedback coordinate, but it does need stable structural addressability. A returning process can acquire meaning from repeated utility only if it repeatedly occupies a reusable structural address.**

Receipt: `results/GATE14.md`.

---

# Biology papers: what they earned

Aizenbud et al. motivated extended, compartmentalized, nonlinear local integration rather than "more branches = smarter." Leterrier motivated separating continuously evolving internal computation from an output/broadcast boundary.

They do not establish our matrix equations, eligibility, capacity conservation, recurrent-growth rule, or any hippocampal interpretation.

The recurrent gates are intentionally generic.

---

# Differentiation side branch

Gate 4: Oja units duplicate the strongest covariance mode; Sanger/GHA differentiates them. Explicit PCA wins.

Gate 5: lag-1 temporal statistics can identify causes that zero-lag covariance cannot. AMUSE solves that specific world; shuffle time and it fails.

Do not add SOBI unless a future wall genuinely needs multiple lags.

---

# Current object

```text
incoming broadcasts
      ↓
local nonlinear state Z(t)
      ↓
continuous output / broadcast
      ↓
other continuously running points
      ↓
stably addressed returning traffic
      ↓
receiver again

while in parallel:

Z(t) -> eligibility E(t) -> delayed consequence -> finite structural mass M
```

Persistent capacity can therefore shape both local computation and the recurrent routes through which future state circulates.

---

# NEXT — remove the coordinate basis, not add more brain regions

Gate 14 removed the semantic label from the return channel, but every incoming channel still maps directly to a simple known matrix coordinate.

That is now the largest scaffold.

Next clean attack:

```text
stable incoming processes
        ↓
randomly mixed / generic overcomplete local coordinates
        ↓
no coordinate is "the return channel"
        ↓
consequence + eligibility + finite growth
        ↓
can a useful recurrent computational subspace acquire structural mass?
```

Keep the two-point loop for that test. Do **not** simultaneously scale to many points.

Controls:

```text
memory-required vs no-memory task
shuffle coordinate basis over time
shuffle eligibility
cut useful return after growth
ordinary trained recurrent attacker
```

Only if a stable useful recurrent subspace can be selected without hand-designed coordinates should the network expand.

---

# Compass sentence

> **Broadcast -> receiver-relative fit -> compose -> context -> consequence -> finite allocation -> growing sparse matrix -> continuous state -> recurrent traffic -> grown recurrent structure -> anonymous useful return discovery. Stable addressability has now earned a job. The next wall is whether useful recurrent computation can be selected when even the local coordinate basis is generic rather than supplied.**
