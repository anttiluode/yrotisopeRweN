# Gate 0 — relative-phase routing

Development receipt, not confirmatory evidence.

## Question

Can the same scalar mixture be routed into different outputs purely because its hidden causes arrive preferentially at different phases of a receiver clock?

And can receiver phase offsets be learned without source labels?

## World

Two independent slowly varying signed source amplitudes are expressed through narrow periodic envelopes centered near phase `0` and `pi`. They are summed into one noisy scalar stream.

The receiver sees:

```text
x(t) = s1(t) + s2(t) + noise
phi(t) = global oscillator phase
```

It does not see source identity.

Source phase centers jitter independently each cycle, so the problem is not an exact clock lookup.

## Receiver

For receiver offset `theta_j`:

```text
g_j(t) = ((1 + cos(phi(t)-theta_j))/2)^3
y_j(t) = g_j(t) x(t)
```

Phase learning is an intentionally simple circular Hebbian/competition procedure:

1. input energy indicates that something arrived;
2. receivers compete softly according to phase proximity;
3. each receiver phase moves toward the circular mean of energetic arrivals it owns.

No source labels enter the phase learning.

## Arms

```text
static
    duplicate x to both outputs

global oscillation
    both outputs share the same phase gate

random phase
    two fixed random receiver offsets

learned phase
    competitive phase plasticity

oracle phase
    receiver offsets fixed to the true source phase centers

phase-feature attacker
    supervised linear readout of [x, x cos(phi), x sin(phi)]
```

## Result

Eight seeds, held-out last 40%:

| arm | recovery mean | std |
|---|---:|---:|
| static | 0.6950 | 0.0113 |
| global oscillation | 0.5088 | 0.0125 |
| random phase | 0.5991 | 0.1610 |
| **learned phase** | **0.9947** | **0.0004** |
| oracle phase | 0.9947 | 0.0004 |
| **phase-feature attacker** | **0.9960** | **0.0006** |

Learned-output duplication: `0.0215 ± 0.0238`.

The learned phase offsets converge near the two source phase centers, modulo permutation on the circle.

## Negative control — remove phase diversity

Both source envelopes are moved to the **same phase center**.

| arm | recovery mean |
|---|---:|
| static | 0.7340 |
| learned phase | 0.7335 |
| oracle phase | 0.7334 |
| phase-feature attacker | 0.7352 |

Learned-output duplication rises to `0.9996`.

So the learned receivers collapse to effectively the same listener when there is no phase structure that distinguishes the sources.

## Interpretation

What survived:

> **A receiver oscillator can instantiate fast time-dependent effective connectivity, and competitive adaptation can discover useful listening phases when arrival timing contains stable structure.**

What did not survive:

> oscillation is a superior source-separation algorithm.

The explicit digital phase-feature attacker slightly beats the oscillatory implementation. The information is in `(x, phi)`; the receiver gate is one physical/computational bias for using it.

## Why the global-oscillation arm matters

Adding one oscillation to the whole system is not enough. If both outputs have the same oscillatory gain, they do not become different listeners.

The useful quantity is **relative receiver phase / receiver-specific state**.

That is closer to the biological intuition: the same arriving input can have different efficacy because it encounters a different receiver state.

## Next

Gate 1 should remove the static-world convenience:

- source preferred phases drift;
- receivers must adapt online;
- compare tracking speed/stability against a normal adaptive phase-feature model.

The strongest later attack is to remove the supplied global phase entirely and see whether local oscillators can synchronize from events rather than being handed a clock.
