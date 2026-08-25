# Gate 14 — ANONYMOUS RETURN: discover useful recurrent traffic

Development receipt, not confirmatory evidence.

## Why this gate

Gate 13 still contained one enormous convenience:

```text
matrix coordinate (1,0) = peer return
```

The learner did not have to discover which incoming stream was the useful recurrent one.

Gate 14 removes that label.

Each cell receives four generic return channels. Their positions are randomly permuted independently for every seed:

```text
one current peer broadcast
three unrelated low-amplitude return streams
```

The growth rule sees only local activity, eligibility, delayed scalar consequence, and finite structural capacity.

The experimenter records which anonymous channel happened to carry the current peer only for evaluation.

This still does **not** remove the generic coordinate field itself; it removes only the named recurrent channel.

## Stable anonymous addresses

Three development seeds, 12,000 continuous steps.

When channel identity remains stable over time:

```text
late cue-free memory accuracy     1.0000
A direct-cue mass                 0.47310
A useful anonymous return mass    0.49284
B useful anonymous return mass    0.96497
closed-loop mass                  0.49284

A best irrelevant return mass     0.00103
B best irrelevant return mass     0.00101
```

So the useful current peer stream is discovered despite occupying a different anonymous channel in each seed.

The matrix therefore does not need a hard-coded symbol meaning "feedback." It needs a **stable structural address** whose traffic is repeatedly useful.

## Kill 1 — reshuffle channel identity every timestep

Keep the same current-peer source and the same nuisance sources, but randomly permute which physical channel carries each one on every timestep.

Now no matrix coordinate has a stable meaning.

```text
late memory accuracy              0.0501
A useful-return mass              0.00161
closed-loop mass                  0.00161
A direct-cue mass                 0.96301
```

The system retreats to almost pure feedforward cue structure.

B can still place mass on some fluctuating return channels, but A cannot establish the stable return leg required to close the loop.

This is the cleanest Gate-14 result:

> **useful recurrence needs persistent addressability. If the same returning process lands on a different structural coordinate every moment, consequence cannot consolidate a reusable path.**

## Kill 2 — shuffle eligibility

Preserve stable channel identity but give delayed consequence the wrong earlier matrix-cell traces.

```text
late memory accuracy              0.0000
A useful-return mass              0.03483
B useful-return mass              0.02663
closed-loop mass                  0.02663
```

Stable address alone is not enough; delayed credit still has to point back to the activity that occurred there.

## Causal control — memory not required

Use the same anonymous return channels, but make desired output zero once the cue disappears.

```text
cue-free task accuracy            0.9298
A direct-cue mass                 0.8650
A useful-return mass              0.00223
B useful-return mass              0.08055
closed-loop mass                  0.00223
```

Some nuisance/echo structure can grow because correlated activity still exists, especially in B. But A does not invest in the useful return leg, so a functional recurrent loop does not close.

Again the relevant quantity is the **closed-loop mass**, not whether any single feedback-looking edge became large.

## Cut after growth

Let the stable anonymous loop develop, then remove the current peer stream after step 9,600 while learning remains active.

```text
late memory accuracy              0.2342
closed-loop mass                  0.00100
A direct-cue mass                 0.96476
```

Two things happen at once:

1. memory degrades because the selected return path is causally load-bearing;
2. continued consequence-driven growth reallocates A back toward direct cue after the return disappears.

So this is both a lesion and a plastic-compensation experiment, not a frozen lesion.

## What survived

Gate 13 said:

> consequence can grow a recurrent path when persistence is useful.

Gate 14 sharpens it:

> **the recurrent path does not need a pre-named "peer" coordinate. A stable anonymous incoming channel can earn structural capacity because the traffic it repeatedly carries helps the task. But if channel identity itself is unstable, the matrix cannot consolidate that useful process.**

That makes the current growing-matrix picture less like a weight table with semantic columns and more like persistent physical addresses that acquire meaning from the traffic that repeatedly occupies them.

## What is still scaffolded

- every generic incoming channel still maps to a known simple matrix coordinate;
- nuisance streams are synthetic and weak;
- only two points exist;
- consequence is global and scalar;
- eligibility is explicit;
- return delays are not learned;
- no geometry/topology is grown;
- this is not a hippocampal model;
- a trained recurrent network remains the obvious engineering attacker.

## Next

The next honest scaffold to remove is no longer "which channel is feedback?"

It is the **coordinate basis itself**.

A useful next attack would replace the direct channel-to-matrix mapping with a small generic overcomplete nonlinear field or randomly mixed local coordinates, then ask whether finite growth can still select a stable recurrent computational subspace.

Alternatively, before adding that difficulty, expand from two points to a small population **only if** each connection still has stable addressability and the no-memory controls remain clean.

Do not do both at once.

Raw metrics: `results/gate14_anonymous_return_metrics.json`.
