# Gate 13 — GROW THE LOOP

Development receipt, not confirmatory evidence.

## Why this gate

Gate 12 showed that a frozen A <-> B recurrent path can carry state after a cue disappears. Gate 13 asks the structural question that Gate 12 deliberately postponed:

> **Can diffuse matrix capacity grow a closed recurrent path because persistence is useful, rather than because feedback was supplied by hand?**

There is still substantial scaffolding:

- the `6 x 6` product coordinates are known;
- the global scalar task consequence is supplied;
- the cue statistics are simple;
- only two cells are involved.

The point is to isolate growth of recurrent structure, not to claim a biological learning rule.

## Continuous world

There are no resets.

A brief signed cue enters cell A for 10 steps every 180 steps. The sign alternates between `+` and `-`.

For the memory task, the desired state remains after the cue disappears:

```text
cue +2 for 10 steps
    -> desired +0.9 for the whole 180-step block

cue -2 for 10 steps
    -> desired -0.9 for the whole next block
```

Cell A receives:

```text
direct cue
returned broadcast from B
distractors
```

Cell B receives:

```text
broadcast from A
distractors
```

Both begin with completely diffuse structural mass:

```text
36 cells
M_ij = 1/36
```

All mass remains globally conserved within each cell, with a small reserve floor.

A delayed scalar error from A is applied to both cells through their own eligibility traces. Only positive local growth evidence is allowed. Conservation supplies the retraction.

## Main result — a closed loop grows

Six seeds, 15,000 uninterrupted steps.

The learner begins weak: early cue-free accuracy is only:

```text
0.7366 +/- 0.0095
```

By the final 3,000 steps:

```text
late cue-free accuracy    1.0000 +/- 0.0000
```

The first rolling >90% memory criterion is reached after:

```text
1560 +/- 85 steps
```

The final structural allocation is the interesting part.

Cell A:

```text
direct-cue mass      0.55082 +/- 0.00582
B -> A return mass   0.41517 +/- 0.00582
```

Cell B:

```text
A -> B forward mass  0.96498 +/- 0.00001
```

The weaker leg determines the effective closed-loop structural claim:

```text
closed-loop mass     0.41517 +/- 0.00582
```

So A learns to split finite capacity between "listen to the new cue" and "listen to the circulating state," while B becomes almost entirely a forwarding element.

This is the first gate in the repo where recurrent structure itself grows from diffuse matrix capacity.

## Kill 1 — no learning

Leave both matrices diffuse.

```text
late cue-free accuracy    0.0000
closed-loop mass          0.02778
```

The initial diffuse feedback is not strong enough to support the state.

## Kill 2 — shuffle eligibility across matrix cells

Preserve consequence but destroy which earlier local activity receives it.

```text
late cue-free accuracy    0.0000
A return mass             0.02339
B forward mass            0.02859
closed-loop mass          0.02339
```

The loop does not grow.

So correlation with delayed task error is not sufficient if the credit is assigned to the wrong structural coordinates.

## Causal control — same cue stream, but no persistence required

This is the important control.

Use the same alternating cues and the same available feedback, but make the desired output zero as soon as the cue disappears.

Now recurrent persistence is useless.

The system develops a very different matrix:

```text
A direct-cue mass      0.92306 +/- 0.02326
A return mass          0.00205 +/- 0.00059
B forward mass         0.13667 +/- 0.04138
closed-loop mass       0.00205 +/- 0.00059
```

A becomes almost purely feedforward. B may still grow a partial echo because its activity correlates with the cue, but A does not invest in the return leg, so a functional closed loop does not form.

This is why the gate uses **closed-loop mass = min(A return, B forward)** rather than counting any recurrent-looking edge as success.

Surviving statement:

> **Feedback availability alone does not force the matrix to become recurrent. When the task requires state after the cue has vanished, delayed consequence reallocates finite matrix capacity into a closed A -> B -> A path; when persistence is unnecessary, A spends its capacity on direct input instead.**

## Attacker

The one-scalar recurrent control from Gate 12 holds both signs perfectly without a matrix or structural growth.

So Gate 13 is not an efficiency or expressivity claim.

The result is about structural allocation under the repo's deliberately weak positive-growth rule.

## What changed conceptually

Gate 11 separated three kinds of state:

```text
local computation Z
credit trace E
structural investment M
```

Gate 12 added another place where state can live:

```text
circulating network activity
```

Gate 13 now lets persistent structural investment respond to that network-level need:

```text
brief cue
    -> weak circulating activity
    -> delayed consequence says persistence is useful
    -> recurrent coordinates claim more finite mass
    -> loop gain rises
    -> circulating state becomes self-maintaining
```

That is much closer to the intended "growing matrix" idea than drawing biological-looking dendrites first.

## What is still not earned

- the relevant matrix coordinates are still supplied;
- the recurrent topology is only two cells;
- global scalar consequence is highly convenient;
- eligibility is explicit;
- the return timing is fixed;
- no new cells or channels are created;
- this is not a hippocampal model;
- this does not establish a biological working-memory mechanism;
- a standard trained recurrent network is expected to solve this more directly.

## Next attack

Do **not** immediately grow a large recurrent brain.

The largest remaining cheat is now sharper:

> the system knows that coordinate `(1,0)` means "peer broadcast x carrier."

A useful next attack is to replace the named recurrent coordinate with several generic incoming channels / random local nonlinear coordinates and ask whether finite growth can discover which returning traffic is worth structural investment.

Only after that survives should the loop expand to more than two points.

Raw metrics: `results/gate13_growing_recurrent_metrics.json`.
