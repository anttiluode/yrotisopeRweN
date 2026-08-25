# Gate 7 — CONTEXT: the context is gone, the receiver is not

Development receipt, not confirmatory evidence.

## Why this gate

Gate 6 showed that the same fixed conjunction bank can compute two different relations when fast receiver state is changed.

But Gate 6 cheated in exactly one way:

```text
A,B arrive
+
mode/state is handed in now
```

Gate 7 removes that current mode input.

The main question is:

> **Can an earlier event leave a transient receiver state that changes how a later identical broadcast is composed after the context event itself has disappeared?**

No weights change. No utility signal exists. No mass or geometry moves.

## World

As in Gate 6, two broadcasts carry

```text
A = [a0, a1]
B = [b0, b1]
```

and the two possible target relations are

```text
context 0 -> a0*b0 + a1*b1
context 1 -> a0*b1 + a1*b0
```

Every exact `(A,B)` pair is presented under both earlier contexts.

The temporal order is now:

```text
context event C0 or C1
        ↓
receiver state changes
        ↓
context disappears
        ↓
0,1,2,4,8,16,32,64 unrelated gap events
        ↓
identical A,B arrive
        ↓
composition uses only A,B + leftover receiver state
```

There is no context/mode input at the final composition step.

## Receiver state

The deliberately tiny circular receiver starts with a context-written direction:

```text
C0 -> +1
C1 -> -1
```

During the gap its internal complex state is leaky and is perturbed by unrelated events:

```text
z <- 0.93 z + 0.12 d
```

The final direction selects the same fixed nonlinear conjunction bank from Gate 6.

This is not presented as a biological mechanism. It is a minimal transient-state carrier.

## Boring scalar attacker

A one-number recurrent trace gets the same persistence and the same real distractor stream:

```text
h <- 0.93 h + 0.12 d_real
```

It is allowed to tie or win.

It does.

That matters because the result is **not phase memory**.

The result, if anything survives, is receiver-carried context.

## Memory curve

Twelve-seed held-out result:

| context→broadcast gap | circular state NMSE | scalar state NMSE | context decode |
|---:|---:|---:|---:|
| 0 | `0.0000` | `0.0000` | `1.0000` |
| 1 | `0.00003` | `0.00000` | `1.0000` |
| 2 | `0.00012` | `0.00000` | `1.0000` |
| 4 | `0.00075` | `0.00004` | `1.0000` |
| 8 | **`0.0098 ± 0.0053`** | **`0.0058 ± 0.0039`** | `0.9985` |
| 16 | **`0.1242 ± 0.0174`** | **`0.1111 ± 0.0148`** | `0.9244` |
| 32 | `0.4913 ± 0.0645` | `0.4649 ± 0.0561` | `0.6694` |
| 64 | `0.7195 ± 0.0596` | `0.6960 ± 0.0552` | `0.5140` |

So the state has a finite useful horizon under perturbation.

It is essentially exact through short gaps, still useful at 16 unrelated events, marginal by 32, and gone by 64.

At very long gaps the noisy stale state can become worse than simply admitting uncertainty and averaging the two possible relations. That is a useful failure, not a bug in the receipt.

## Kill 1 — reset the receiver before the broadcast

Set the internal state to neutral immediately before `A,B` arrive.

The ordinary output NMSE becomes:

```text
0.4977
```

which is the same compromise reached by a stateless bilinear model.

More importantly, the **paired context contrast** is destroyed:

```text
contrast NMSE = 1.0002
```

For the same exact `(A,B)` pair, the reset receiver can no longer produce two different context-dependent answers.

That is the clean kill.

## Kill 2 — shuffle which old context wrote the state

At gap 8, keep the broadcasts and distractors unchanged but randomly reassign the old context before generating receiver state.

Result:

```text
NMSE = 0.9373
```

The context relation is therefore carried by the preceding event, not by the instantaneous broadcast statistics.

## Attackers

| arm | held-out NMSE |
|---|---:|
| current-context cheat | `0.0000` |
| explicit remembered-context buffer | ~`0.0000` |
| circular receiver, gap 8 | `0.0098` |
| one-scalar recurrent state, gap 8 | **`0.0058`** |
| stateless bilinear | `0.4977 ± 0.0275` |
| state reset | `0.4977 ± 0.0275` |
| shuffled old context, gap 8 | `0.9373` |

The explicit buffer is the boring digital upper bound: if the old context bit is simply kept somewhere and supplied to a state-conditioned bilinear readout, the task is trivial.

So Gate 7 is not a memory breakthrough. It isolates what the dynamic-point hypothesis needs to claim and no more.

## What survived

The clean statement is:

> **Past input can change a transient receiver state, the past input can disappear, and that leftover state can change how a later identical broadcast is nonlinearly composed.**

Or in the main-line grammar:

```text
PAST CONTEXT
writes fast receiver state

FAST RECEIVER STATE
persists imperfectly through unrelated events

IDENTICAL LATER BROADCAST
is interpreted/composed according to that leftover state
```

This is the first gate in the main line where immediate sensory input at composition time is deliberately identical while the correct output differs because of history.

## What did not survive

Phase did not earn a privileged role.

The one-scalar recurrent trace ties or slightly beats the circular state throughout the useful range.

Therefore:

> **receiver-carried context is the primitive; phase is currently only one possible coordinate system for it.**

## What this does not show

- the context code is learned rather than supplied;
- the receiver chooses what to remember;
- useful memory is protected from distractors;
- phase is better than a scalar recurrent state;
- a biological neuron implements this recurrence;
- this is associative memory or sequence completion;
- utility can decide which transient state transitions matter;
- growth can consolidate a useful context-dependent composition.

## Next

Gate 7 has finally made `CONSEQUENCE` worth testing, but there is still one important design choice.

Do not reward the context bit itself.

Instead make several transient context-dependent compositions possible and arrange the downstream task so only one helps.

Then ask:

> **Can consequence reinforce the state transition / conjunction that made a later useful computation possible, rather than merely reinforcing whichever input was active at reward time?**

That is the credit-assignment version of the main hypothesis.

Only if that survives should finite allocation and structural consolidation return.

Raw metrics: `results/gate7_context_metrics.json`.
