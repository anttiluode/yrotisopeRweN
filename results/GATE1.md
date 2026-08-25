# Gate 1 — self-wiring by phase coherence

Development receipt, not confirmatory evidence.

## Question

Can fast phase-compatible traffic slowly compile itself into persistent topology?

More concretely:

> **If candidate edges have both a finite structural mass and a propagation delay, can repeated coherent arrivals cause the graph to move mass toward useful receivers while exploratory growth/retraction tunes delay?**

This is the first direct test of the "grow toward something you can oscillate with" thought.

## World

Three sender points emit jittered periodic event trains with periods `17`, `23`, and `31` steps.

Six possible receivers exist:

```text
receiver periods = [31, 17, 27, 23, 41, DEAD]
```

The three frequency-compatible receivers are deliberately permuted:

```text
sender 17 -> receiver 17 at index 1
sender 23 -> receiver 23 at index 3
sender 31 -> receiver 31 at index 0
```

The `DEAD` receiver has no oscillatory cycle at all; its gate is constant.

No correct-target labels are used for development. They are used only after training to score the graph.

## Edge state

Every possible sender→receiver edge begins as a weak candidate with two slow variables:

```text
mass m_ij       structural commitment
delay d_ij      stand-in for path length / conduction delay
```

Each sender has a fixed outgoing material budget:

```text
sum_j m_ij = 1
```

So growing one connection necessarily takes structural mass away from the alternatives.

Arrival compatibility is a positive centered correlation between the delayed sender event train and the receiver excitability gate. A matching frequency can sustain phase coherence; a different frequency drifts and averages toward zero. A constant/dead receiver has zero phase compatibility.

## Development rule

Each epoch:

1. every edge gets a small exploratory length change, with occasional larger "sprout" proposals;
2. a proposal is retained only if local phase compatibility improves;
3. outgoing edge masses compete under the fixed budget, moving toward phase-compatible paths;
4. receiver vitality is a slow trace of incoming coherent support.

This is an intentionally cheap developmental abstraction, not a biological axon-growth model.

## Arms

```text
static_random
    random delays, uniform mass

mass_only
    structural mass can move, delays stay random

length_only
    delays can adapt, mass stays uniform

self_wiring
    both delay and structural mass adapt

oracle
    exhaustive digital search over all delays, then optimal mass allocation

destroyed_coherence
    self_wiring rule, but receiver phase is independently scrambled each cycle
```

Twelve seeds. First `9000` samples are development; final `5000` are held out.

## Result

| arm | top-1 correct target | mass on correct receiver | top-edge held-out compatibility | mass entropy | mass on dead receiver |
|---|---:|---:|---:|---:|---:|
| static random | 0.3333 | 0.1667 | 0.1210 | 1.0000 | 0.1667 |
| mass only | 0.3333 | 0.4271 | 0.2291 | 0.6931 | 0.1091 |
| length only | 0.3333 | 0.1667 | 0.3103 | 1.0000 | 0.1667 |
| **self wiring** | **1.0000** | **0.9997** | **0.9270** | **0.0014** | **~0.0000** |
| digital oracle | 1.0000 | 0.9999 | 0.9272 | 0.0005 | ~0.0000 |
| destroyed coherence | 0.4444 | 0.2060 | 0.0147 | 0.9751 | 0.0996 |

The full self-wiring system reaches the same target permutation as the exhaustive delay-search attacker on every development seed, while the one-variable ablations do not.

For seed 0 the final mass matrix is essentially:

```text
sender 17: [0, 1, 0, 0, 0, 0]
sender 23: [0, 0, 0, 1, 0, 0]
sender 31: [1, 0, 0, 0, 0, 0]
```

The compatible receiver vitality traces remain near `1`, while distractors and the non-oscillating receiver decay to approximately zero.

## The important result is the ablation

`mass_only` cannot reliably self-wire because a compatible target may initially be reached at the wrong conduction phase. It moves more mass toward useful targets on average, but top-1 wiring remains chance.

`length_only` improves temporal compatibility but cannot create topology because every edge retains equal mass.

Together:

```text
length/delay adaptation
    finds a phase at which a route can work

mass competition
    makes successful routes persist at the expense of alternatives
```

That composition is what produces the sparse graph.

## Negative control

When receiver phase is independently scrambled every cycle, no fixed path delay can establish a persistent timing relationship.

The same developmental rule then stays nearly diffuse:

```text
correct mass        0.2060
mass entropy        0.9751
top-edge coherence  0.0147
```

So this is not merely a winner-take-all system that invents sparse edges regardless of evidence.

## Attacker

The boring attacker exhaustively evaluates every receiver at every possible delay and then allocates mass to the best edges.

It gets:

```text
top-1             1.0000
correct mass      0.9999
top-edge score    0.9272
```

It is slightly cleaner than the developmental system.

Therefore the claim is **not** that phase-guided growth is a better graph-learning algorithm than explicit digital search.

The surviving abstraction is:

> **Fast temporal compatibility can provide a local signal that slowly writes persistent structure. Geometry/delay determines whether repeated traffic arrives at a useful receiver state; resource competition determines which successful paths survive.**

Or shorter:

> **fast routing can compile into slow wiring.**

## What this does *not* show

- axons literally optimize Pearson correlation;
- real neurites search integer delays;
- synchronization is sufficient for useful cognition;
- phase should be added to ordinary neural networks;
- this beats sparse matrix learning;
- the learned topology carries task meaning beyond temporal compatibility.

The last point is now the important attacker.

## Next gate

The current world makes temporal compatibility itself the developmental objective.

Next, give the graph **two coherent but behaviorally different possibilities** so phase matching alone is insufficient. Then let prediction/control utility decide which coherent edge earns mass.

That asks whether structural growth can preserve something useful rather than merely something synchronous.
