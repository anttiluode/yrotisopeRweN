import json
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utility_wiring import UtilityGuidedGraph, utility_wiring_world, task_metrics, digital_oracle


def evaluate(seed: int, arm: str):
    w = utility_wiring_world(seed=seed)
    split = 9000
    Etr, Gtr, Ttr = w['sender_events'][:split], w['receiver_gates'][:split], w['target'][:split]
    Ete, Gte, Tte = w['sender_events'][split:], w['receiver_gates'][split:], w['target'][split:]
    A, useful = w['actuator_matrix'], w['useful_receivers']

    if arm == 'oracle':
        mass, delays = digital_oracle(Etr, Gtr, A, Ttr)
        graph = UtilityGuidedGraph(seed=seed)
        graph.mass = mass
        graph.delay[:] = 0
        for i in range(len(useful)):
            j = int(mass[i].argmax())
            graph.delay[i, j] = delays[i, j]
    else:
        graph = UtilityGuidedGraph(seed=seed)
        graph.fit(
            Etr, Gtr, A, Ttr,
            use_phase=arm != 'utility_only',
            use_utility=arm not in ('phase_only',),
            independent_utility=arm == 'destroyed_utility',
            adapt_delay=arm != 'utility_only',
        )

    pred = graph.predict(Ete, Gte, A)
    m = task_metrics(graph.mass, useful, pred, Tte)
    phase = graph.phase_scores(Ete, Gte)
    m['heldout_top_phase_score'] = float(np.mean([phase[i, graph.mass[i].argmax()] for i in range(3)]))
    return m, graph


def main():
    arms = ['phase_only', 'utility_only', 'phase_plus_utility', 'destroyed_utility', 'oracle']
    rows = {a: [] for a in arms}
    example = None
    for seed in range(12):
        for arm in arms:
            m, g = evaluate(seed, arm)
            rows[arm].append(m)
            if seed == 0 and arm == 'phase_plus_utility':
                example = {'mass': g.mass.tolist(), 'delay': g.delay.tolist()}

    summary = {}
    for arm in arms:
        summary[arm] = {}
        for key in rows[arm][0]:
            vals = np.array([r[key] for r in rows[arm]], dtype=float)
            summary[arm][key] = {'mean': float(vals.mean()), 'std': float(vals.std())}

    out = {'summary': summary, 'example_seed0': example}
    Path('results').mkdir(exist_ok=True)
    Path('results/gate2_metrics.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
