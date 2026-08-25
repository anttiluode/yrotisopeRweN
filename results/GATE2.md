# Gate 2 — useful coherence

Development receipt, not confirmatory evidence.

## Question

Gate 1 made phase compatibility itself the developmental objective. That was too friendly.

Gate 2 asks:

> **If several destinations are equally phase-compatible, can structural growth preserve the one that is useful for prediction/control rather than merely the one that synchronizes?**

The intended decomposition is now:

```text
phase coherence   -> can this route communicate?
task utility      -> is that communication useful?
structural mass   -> is it worth preserving this route?
```

## World

There are three senders with periods `17`, `23`, and `31` steps.

Each sender has **two receiver twins with exactly the same oscillatory gate**:

```text
sender 17 -> receiver 0 (+ actuator) / receiver 1 (- actuator)
sender 23 -> receiver 2 (- actuator) / receiver 3 (+ actuator)
sender 31 -> receiver 4 (+ actuator) / receiver 5 (- actuator)
```

A seventh receiver is non-oscillating.

Within each twin pair, phase and frequency are identical. Therefore phase coherence alone contains **zero information** about which twin is useful.

The twins differ only in what they do downstream: one pushes a control/prediction dimension in the useful direction, the other pushes the same dimension with opposite sign.

The environment supplies a 3-D target signal. It never supplies a label saying which receiver is correct.

## Edge state

As in Gate 1, every candidate edge has:

```text
mass m_ij       persistent structural commitment
delay d_ij      propagation delay / path-length stand-in
```

Each sender obeys a fixed mass budget:

```text
sum_j m_ij = 1
```

Delay proposals are accepted using **phase compatibility only**.

Mass receives a second signal: error-modulated eligibility. If increasing an edge would reduce the current downstream residual, that edge gets positive task utility; if it pushes the residual the wrong way, utility is negative.

No correct-edge labels are used.

## Arms

```text
phase_only
    delay adapts and mass follows phase coherence; no task utility

utility_only
    utility can move mass, but delays remain random and phase score is removed

phase_plus_utility
    phase tunes viable timing; task utility chooses among viable routes

destroyed_utility
    same phase machinery, but the utility target is replaced by independent noise

oracle
    exhaustive digital search over receiver and delay using held-out task objective
```

Twelve development seeds. First `9000` samples train/develop; final `5000` are held out.

## Result

| arm | top-1 useful receiver | mass on useful receiver | held-out target corr. | target NMSE | held-out phase score |
|---|---:|---:|---:|---:|---:|
| phase only | 0.4167 | 0.4877 | 0.0158 | 0.9999 | 0.7662 |
| utility only | 0.3889 | 0.3720 | 0.2436 | 0.9260 | 0.1103 |
| **phase + utility** | **1.0000** | **0.9992** | **0.9061** | **0.5182** | **0.7660** |
| destroyed utility | 0.4722 | 0.4846 | 0.0023 | 1.0080 | 0.7661 |
| digital oracle | 1.0000 | 1.0000 | 0.9248 | 0.5070 | 0.7660 |

The phase+utility graph finds the useful twin for all three senders on all 12 seeds and reaches nearly the same held-out target correlation as exhaustive digital search.

For seed 0 the final mass matrix is approximately:

```text
sender 17: [0.9996, 0,      0.0002, 0,      0.0002, 0,      0]
sender 23: [0,      0.0005, 0,      0.9991, 0,      0.0004, 0]
sender 31: [0.0001, 0,      0.0001, 0,      0.9998, 0,      0]
```

## The important failure: phase-only

The phase-only graph successfully finds the **pair** of compatible receivers, but it cannot tell the useful twin from the harmful twin.

Its mass on the useful twin remains about `0.488`, essentially a 50/50 split inside the coherent pair. Because the two twins have opposite downstream actuator signs, their effects cancel and held-out task correlation is approximately zero.

So:

> **synchrony can identify where communication is possible without identifying what communication is for.**

That is exactly the distinction Gate 2 was meant to force.

## The other failure: utility-only

Task utility without adaptable timing also fails to wire reliably.

With random fixed delays, many candidate routes expose weak or unstable eligibility. Utility can extract some target correlation (`0.244` mean) but topological selection remains near chance and the selected edges have low phase compatibility (`0.110`).

So utility does not replace temporal compatibility either.

## Negative control

Replace the real task target used during development with independent noise.

The graph still discovers coherent twin pairs because phase structure remains intact, but it no longer knows which twin is useful:

```text
useful mass       0.4846
held-out corr.    0.0023
phase score       0.7661
```

Thus the correct sparse graph is not being produced by phase bias alone or by a hard-coded useful receiver index.

## Attacker

The exhaustive attacker simply searches every edge and every delay under the explicit task objective.

It obtains:

```text
top-1 useful      1.0000
useful mass       1.0000
target corr.      0.9248
NMSE              0.5070
```

It remains slightly cleaner than the developmental system.

Therefore the claim is not that phase-guided growth is a superior optimizer.

## What survived

Gate 1 gave:

> **fast routing can compile into slow wiring.**

Gate 2 sharpens that to:

> **Fast coherence can propose viable routes; task error can decide which viable route deserves scarce structure.**

Or, even shorter:

> **coherence says can; utility says keep.**

This is the first gate where structural mass is preserving something other than synchronization itself.

## What this does not show

- real axons optimize this error-modulated eligibility equation;
- phase is necessary for graph learning in ordinary AI;
- the 3-D target is biologically realistic;
- utility must be supervised prediction error rather than reward, novelty, control success, or local mismatch;
- this beats a sparse learned matrix;
- self-grown topology will remain useful once the world changes.

## Next

The next serious attack is **reversal / remapping**.

After the graph hardens, swap which coherent twin is useful.

Ask whether a finite mass budget can:

1. retract an obsolete route,
2. regrow the alternative,
3. preserve enough exploratory mass to avoid developmental lock-in.

That turns structural plasticity into a stability-plasticity problem rather than a one-shot graph discovery toy.
