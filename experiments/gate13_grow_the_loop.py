from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from growing_recurrent_loop import run_growing_recurrent_world
from recurrent_loop import run_scalar_recurrent_attacker


def summarize(rows: list[dict], keys: list[str]) -> dict[str, dict[str, float]]:
    out = {}
    for key in keys:
        vals = np.array([float(r[key]) for r in rows], dtype=float)
        out[key] = {"mean": float(vals.mean()), "std": float(vals.std())}
    return out


def main() -> None:
    seeds = list(range(6))
    arms = {
        "memory_task": {},
        "no_learning": {"learn": False},
        "shuffled_eligibility": {"shuffle_eligibility": True},
        "no_memory_required": {"memory_required": False},
    }
    keys = [
        "early_hold_accuracy", "late_hold_accuracy",
        "a_cue_mass", "a_return_mass", "b_forward_mass", "closed_loop_mass",
    ]
    metrics: dict[str, object] = {}
    for name, kwargs in arms.items():
        rows = [run_growing_recurrent_world(seed=s, **kwargs) for s in seeds]
        metrics[name] = summarize(rows, keys)
        if name == "memory_task":
            steps = np.array([float(r["first_good_step"]) for r in rows], dtype=float)
            metrics[name]["first_good_step"] = {"mean": float(steps.mean()), "std": float(steps.std())}

    attacker = [run_scalar_recurrent_attacker(seed=s) for s in seeds]
    metrics["scalar_recurrent_attacker"] = summarize(
        attacker, ["hold1_accuracy", "hold2_accuracy"],
    )

    path = Path(__file__).resolve().parents[1] / "results" / "gate13_growing_recurrent_metrics.json"
    path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    for name, value in metrics.items():
        print(name)
        for key, stat in value.items():
            print(f"  {key:24s} {stat['mean']:.6f} +/- {stat['std']:.6f}")


if __name__ == "__main__":
    main()
