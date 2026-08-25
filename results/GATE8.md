# Gate 8 — CONSEQUENCE: can delayed error find the conjunction that mattered?

Development receipt, not confirmatory evidence.

## Why this gate

Gate 7 established a finite version of:

```text
old context
    -> transient receiver state
    -> later identical input is composed differently
```

That finally gives consequence something nontrivial to act on.

Gate 8 asks:

> **Can a delayed downstream error assign credit back to the earlier transient nonlinear conjunctions that made the useful computation possible?**

Structural growth is still forbidden.

No mass moves. No geometry moves. No source-separation objective exists.

The only slow variables are efficacy weights over fixed local conjunction subunits.

## World

The receiver gets an earlier binary context, then four unrelated gap events. A one-scalar recurrent state from Gate 7 carries that context forward.

Later two broadcasts arrive:

```text
A = [a0, a1]
B = [b0, b1]
```

The receiver state gates the same four fixed Gate-6 conjunctions:

```text
q00 = a0*b0
q01 = a0*b1
q10 = a1*b0
q11 = a1*b1
```

Under context 0 the same-index family is available:

```text
q00, q11
```

Under context 1 the crossed family is available:

```text
q01, q10
```

But context itself is not the downstream answer.

Only one conjunction in each available family is useful:

```text
context 0 -> q00 matters; q11 should get no slow efficacy
context 1 -> q10 matters; q01 should get no slow efficacy
```

So the hidden utility pattern is

```text
[q00, q01, q10, q11]
   [1,   0,   1,   0]
```

The learner is not given those coefficients.

## Temporal order

A trial is conceptually:

```text
EARLIER CONTEXT
       ↓
transient receiver state
       ↓
LATER A,B
       ↓
state-gated nonlinear conjunctions phi
       ↓
phi disappears
       ↓
consequence delay
       ↓
scalar downstream error
```

At consequence time the original conjunction vector is unavailable.

Each local conjunction may leave only a decaying scalar eligibility value:

```text
e_j <- phi_j

e_j after D steps = 0.85^D * phi_j
```

Then delayed error modulates that trace:

```text
Delta w_j = eta * error * e_j
```

This is deliberately ordinary eligibility-trace credit assignment. No phase-specific learning rule is introduced.

## Result

Twelve-seed held-out result with one training pass:

| consequence delay | held-out NMSE | utility-weight alignment |
|---:|---:|---:|
| 0 | `0.000060 ± 0.000035` | `0.9999996` |
| 4 | `0.000060 ± 0.000036` | `0.9999998` |
| **8** | **`0.000059 ± 0.000036`** | **`0.9999999`** |
| 16 | `0.002713 ± 0.000461` | `0.9999858` |
| 32 | `0.6433 ± 0.0077` | `0.9995930` |

With the fixed trace decay and fixed learning budget, delay 8 is essentially as good as immediate consequence. By delay 32 the trace is too weak for this training budget.

Do **not** interpret that as a fundamental memory time constant. More epochs or rescaled learning could move the boundary. The load-bearing result is the ablation below.

## Kill 1 — no eligibility trace

Let the scalar consequence arrive after eight steps but erase the local conjunction traces.

Result:

```text
NMSE = 1.0001
```

The slow efficacies remain at their uninformed baseline because the delayed error has no address for the earlier local event.

## Kill 2 — shuffle consequence across trials

Keep eligibility traces intact but pair each trace with another trial's delayed target/error.

Result:

```text
NMSE = 1.0096
```

Useful learning disappears.

## Kill 3 — shuffle eligibility across trials

Keep the correct delayed consequence but attach it to the wrong earlier conjunction trace.

Result:

```text
NMSE = 1.0928
```

This is the sharper credit-assignment kill:

> **consequence alone is insufficient; it must meet the trace left by the event it is supposed to credit.**

## Attackers

| arm | held-out NMSE |
|---|---:|
| explicit old-context buffer + batch bilinear readout | ~`0.000000` |
| batch regression on transient receiver features | `0.000059` |
| delayed eligibility, D=8 | **`0.000059`** |
| no eligibility | `1.0001` |
| shuffled consequence | `1.0096` |
| shuffled eligibility | `1.0928` |
| context/state alone, no conjunctions | `1.0005` |

The explicit buffer is the boring digital upper bound. If the old context is simply stored exactly and supplied to an ordinary bilinear model, the task is trivial.

The batch regression attacker also shows that once the transient conjunction features exist, no exotic optimizer is needed.

## What survived

The clean main-line statement is now:

> **A past event can leave receiver state; that state can determine which later nonlinear conjunctions exist; and a still later scalar consequence can selectively change slow efficacy only when the earlier conjunction left an eligibility trace.**

In verbs:

```text
BROADCAST / CONTEXT
        ↓
RECEIVER STATE
        ↓
COMPOSE
        ↓
ELIGIBILITY
        ↓
CONSEQUENCE
        ↓
SLOW SELECTION
```

This is not structural consolidation yet.

It is only the bridge that tells later consolidation **what** deserves a claim on capacity.

## What this does not show

- the receiver learns which context to store;
- eligibility traces are biologically implemented this way;
- scalar prediction error is the only useful consequence signal;
- phase is required anywhere in Gate 8;
- the learned slow efficacies should become physical structure;
- structural mass should obey the same update;
- long-delayed credit is solved generally;
- sequence completion or concept formation has been demonstrated.

## Next

The next missing verb is no longer consequence.

It is **ALLOCATION / CONSOLIDATION**.

But this time there is a much cleaner object to consolidate than in the earlier growth experiments:

```text
a transient state transition
    made certain conjunctions available
those conjunctions left eligibility
later consequence marked some of them useful
```

Now introduce a **finite capacity budget** and ask whether useful slow efficacies can claim persistent mass while unused or harmful conjunctions lose it.

The critical attacker should be an ordinary fixed-capacity sparse/regularized model.

And the structural question should be reversible: after consolidation, change which conjunction is useful and ask whether the system can reallocate without either freezing forever or dissolving everything.

That would finally reconnect the main line to the unfinished Gate-2 stability/plasticity question.

Raw metrics: `results/gate8_consequence_metrics.json`.
