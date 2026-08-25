from pathlib import Path
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from self_wiring import (
    SelfWiringPhaseGraph,
    oracle_delay_matrix,
    self_wiring_world,
    softmax_mass,
    wiring_metrics,
)


def run_arm(seed: int, adapt_delay: bool, adapt_mass: bool, destroy: bool = False):
    world = self_wiring_world(seed=seed, destroy_coherence=destroy)
    split = 9000
    Etr, Ete = world["sender_events"][:split], world["sender_events"][split:]
    Gtr, Gte = world["receiver_gates"][:split], world["receiver_gates"][split:]
    graph = SelfWiringPhaseGraph(Etr.shape[1], Gtr.shape[1], seed=seed)
    graph.fit(Etr, Gtr, adapt_delay=adapt_delay, adapt_mass=adapt_mass)
    scores = graph.scores(Ete, Gte)
    metrics = wiring_metrics(graph.mass, scores, world["matching_receivers"])
    metrics["mean_vitality_dead"] = float(graph.vitality[-1])
    return metrics, graph


def run_oracle(seed: int):
    world = self_wiring_world(seed=seed)
    split = 9000
    train_scores, delays = oracle_delay_matrix(
        world["sender_events"][:split], world["receiver_gates"][:split]
    )
    mass = softmax_mass(train_scores)
    graph = SelfWiringPhaseGraph(3, 6, seed=seed)
    graph.delay = delays
    graph.mass = mass
    test_scores = graph.scores(
        world["sender_events"][split:], world["receiver_gates"][split:]
    )
    return wiring_metrics(mass, test_scores, world["matching_receivers"])


def summarize(rows):
    keys = rows[0].keys()
    return {
        k: {
            "mean": float(np.mean([r[k] for r in rows])),
            "std": float(np.std([r[k] for r in rows])),
        }
        for k in keys
    }


def main():
    seeds = range(12)
    arms = {
        "static_random": (False, False, False),
        "mass_only": (False, True, False),
        "length_only": (True, False, False),
        "self_wiring": (True, True, False),
        "destroyed_coherence": (True, True, True),
    }
    result = {}
    examples = {}
    for name, cfg in arms.items():
        rows = []
        for seed in seeds:
            metrics, graph = run_arm(seed, *cfg)
            rows.append(metrics)
            if seed == 0:
                examples[name] = {
                    "mass": graph.mass.tolist(),
                    "delay": graph.delay.tolist(),
                    "vitality": graph.vitality.tolist(),
                }
        result[name] = summarize(rows)
    result["oracle"] = summarize([run_oracle(seed) for seed in seeds])
    result["examples_seed0"] = examples

    print("Gate 1 — self-wiring by phase coherence")
    print("arm                  top1   correct_mass   top_score   entropy   dead_mass")
    for name in [
        "static_random",
        "mass_only",
        "length_only",
        "self_wiring",
        "oracle",
        "destroyed_coherence",
    ]:
        s = result[name]
        print(
            f"{name:20s} "
            f"{s['top1_accuracy']['mean']:.4f}  "
            f"{s['correct_mass']['mean']:.4f}       "
            f"{s['top_edge_score']['mean']:.4f}     "
            f"{s['mass_entropy']['mean']:.4f}    "
            f"{s['dead_receiver_mass']['mean']:.4f}"
        )

    out = ROOT / "results" / "gate1_self_wiring.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
