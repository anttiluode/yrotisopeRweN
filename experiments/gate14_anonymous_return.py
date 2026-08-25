from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from anonymous_recurrent_loop import run_anonymous_return_world


def summarize(rows: list[dict], keys: list[str]) -> dict[str, dict[str, float]]:
    out = {}
    for key in keys:
        vals = np.array([float(r[key]) for r in rows], dtype=float)
        out[key] = {"mean": float(vals.mean()), "std": float(vals.std())}
    return out


def main() -> None:
    seeds = [0, 1, 2]
    arms = {
        "stable_anonymous": {},
        "dynamic_channel_shuffle": {"dynamic_channel_shuffle": True},
        "shuffled_eligibility": {"shuffle_eligibility": True},
        "no_memory_required": {"memory_required": False},
        "cut_after_growth": {"cut_useful_return_after": 9600},
    }
    keys = [
        "late_hold_accuracy", "a_direct_cue_mass",
        "a_useful_return_mass", "b_useful_return_mass", "closed_loop_mass",
        "a_best_other_return_mass", "b_best_other_return_mass",
    ]
    metrics = {}
    for name, kwargs in arms.items():
        rows = [run_anonymous_return_world(seed=s, n_steps=12_000, **kwargs) for s in seeds]
        metrics[name] = summarize(rows, keys)

    path = Path(__file__).resolve().parents[1] / "results" / "gate14_anonymous_return_metrics.json"
    path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    for name, value in metrics.items():
        print(name)
        for key, stat in value.items():
            print(f"  {key:28s} {stat['mean']:.6f} +/- {stat['std']:.6f}")


if __name__ == "__main__":
    main()
