from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from recurrent_loop import run_recurrent_loop, run_scalar_recurrent_attacker


def summarize(rows: list[dict], keys: list[str]) -> dict[str, dict[str, float]]:
    out = {}
    for key in keys:
        vals = np.array([float(r[key]) for r in rows], dtype=float)
        out[key] = {"mean": float(vals.mean()), "std": float(vals.std())}
    return out


def main() -> None:
    seeds = list(range(12))
    arms = {
        "full_loop": {},
        "cut_return": {"cut_return": True},
        "scrambled_return_timing": {"scramble_return_timing": True},
        "low_loop_gain": {"recurrent_gain_scale": 0.10},
        "instantaneous_compartments": {"instantaneous_compartments": True},
    }
    keys = [
        "hold1_a_accuracy", "hold1_b_accuracy",
        "hold2_a_accuracy", "hold2_b_accuracy",
        "hold1_a_mean", "hold2_a_mean",
    ]
    metrics: dict[str, object] = {}
    for name, kwargs in arms.items():
        rows = [run_recurrent_loop(seed=s, **kwargs) for s in seeds]
        metrics[name] = summarize(rows, keys)

    attacker_rows = [run_scalar_recurrent_attacker(seed=s) for s in seeds]
    metrics["scalar_recurrent_attacker"] = summarize(
        attacker_rows,
        ["hold1_accuracy", "hold2_accuracy", "hold1_mean", "hold2_mean"],
    )

    path = Path(__file__).resolve().parents[1] / "results" / "gate12_recurrent_loop_metrics.json"
    path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    for name, value in metrics.items():
        print(name)
        for key, stat in value.items():
            print(f"  {key:24s} {stat['mean']:.6f} +/- {stat['std']:.6f}")


if __name__ == "__main__":
    main()
