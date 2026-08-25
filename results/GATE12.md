# Gate 12 — RECURRENT TRAFFIC: state can live in the loop

Development receipt, not confirmatory evidence.

## Why this gate

Gate 11 removed trial resets and separated continuous internal computation from output. It still was not a literal recurrent network: emitted activity did not enter another continuously running point and return.

Gate 12 isolates that missing operation.

Structural mass is **frozen**. There is no growth, eligibility, utility learning, geometry, or source separation in this gate.

The question is only:

> **Can ongoing mutual broadcast carry a state after the initiating input disappears, and can a later input overwrite that state without resetting either point?**

This is not a hippocampal model. It is a generic two-point recurrent traffic test.

## Frozen matrix cells

Each point still owns a `6 x 6` relation field, but only two coordinates have substantial frozen mass:

```text
(0,0) external cue x constant carrier
(1,0) peer broadcast x constant carrier
```

Cell A receives the brief external cue and the returned broadcast from B.

Cell B receives only A's broadcast.

Both continue to receive unrelated distractor/background traffic.

The cells run continuously:

```text
A(t) -> broadcast -> B(t+1)
 ^                    |
 |                    v
 +------ broadcast ---+
```

A `+2` cue enters A for ten steps, then disappears. Much later a `-2` cue enters A for ten steps. No state is reset between them.

Memory is scored only during long cue-free windows.

## Main result

Twelve seeds.

Full A <-> B loop:

```text
first cue-free hold, A accuracy     1.0000
first cue-free hold, B accuracy     1.0000
second hold after overwrite, A      1.0000
second hold after overwrite, B      1.0000

A mean state, first hold             +0.906824
A mean state, second hold            -0.906823
```

The brief cue therefore places the recurrent pair into a persistent state. The opposite cue later flips that state without clearing either cell.

## Kill 1 — cut only the return path B -> A

A can still drive B, but B can no longer close the loop.

```text
first-hold A accuracy    0.0000
second-hold A accuracy   0.0000
A mean after cue         ~ 0
```

So persistence is not coming from the brief external cue or from a hidden trial buffer.

## Kill 2 — scramble return timing

Instead of returning B's current broadcast, return a randomly selected recent B broadcast.

The old state remains strong:

```text
first-hold A accuracy    1.0000
A mean                   +0.9062
```

but the later opposite cue cannot cleanly overwrite it:

```text
second-hold A accuracy   0.0000
A mean                   +0.9012
```

The loop keeps resurrecting stale positive traffic.

Thus in this toy, recurrence is not merely "feedback exists." The temporal organization of the returning traffic matters for state transition.

## Kill 3 — reduce loop gain

Scale both recurrent broadcasts to `0.10` of normal strength.

```text
first-hold A accuracy    0.0000
second-hold A accuracy   0.0000
A mean                   ~ 0
```

The recurrent attractor has a gain boundary.

## Important ablation — remove local persistence

Set every matrix-cell decay to zero:

```text
Z(t+1) = Q(t)
```

so no individual local compartment remembers the previous timestep.

The recurrent pair still scores:

```text
first-hold accuracy      1.0000
second-hold accuracy     1.0000
```

This is a useful correction to Gate 11.

Gate 11 showed that persistent local state helps continuous delayed credit assignment. Gate 12 shows that this particular state-maintenance problem does **not** require local persistence once network recurrence exists.

So memory-like persistence can live at more than one level:

```text
inside a point
or
between points in recurrent traffic
```

Those are distinct mechanisms.

## Attacker

A boring one-scalar recurrent unit has no matrix and no two-point loop:

```text
h(t+1) = leaky_tanh(recurrent_gain * h(t) + cue)
```

It also obtains:

```text
first-hold accuracy      1.0000
second-hold accuracy     1.0000
```

and holds a slightly stronger mean state (`~ +/-0.9575`).

So Gate 12 is not an expressivity claim for the growing-matrix architecture.

The primitive that has earned a job is simply **recurrent state**.

## What survived

> **A brief broadcast can move a continuously running recurrent pair into a self-maintaining state that persists after the original signal disappears. Cutting the return path destroys that state, while stale return timing can prevent a later signal from overwriting it. The state can live in network recurrence even when local matrix compartments themselves are instantaneous.**

This is deliberately generic. It does not identify a hippocampal mechanism or claim that this is how biological working memory is implemented.

## What comes next

Because recurrence now has a clean gate, structural growth can be turned back on without conflating the two questions.

The next attack is:

```text
start with diffuse recurrent structural capacity
        ↓
continuous external traffic
        ↓
only some return paths help preserve / update useful state
        ↓
delayed consequence + eligibility
        ↓
can the recurrent matrices grow the loop they need?
```

The hard control is a world where recurrence is unnecessary. In that world, recurrent structural mass should **not** grow merely because feedback is available.

Raw metrics: `results/gate12_recurrent_loop_metrics.json`.
