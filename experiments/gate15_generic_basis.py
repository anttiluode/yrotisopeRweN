from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from generic_recurrent_field import run_generic_basis_world


def summarize(rows: list[dict], keys: list[str]) -> dict[str, dict[str, float]]:
    out = {}
    for key in keys:
        vals = np.array([float(r[key]) for r in rows], dtype=float)
        out[key] = {"mean": float(vals.mean()), "std": float(vals.std())}
    return out


def main() -> None:
    seeds = [0, 1, 2]
    arms = {
        "stable_generic_basis": {},
        "scrambled_feature_addresses": {"scramble_feature_addresses": True},
        "shuffled_eligibility": {"shuffle_eligibility": True},
        "no_learning": {"learn": False},
        "cut_return_after_growth": {"cut_returns_after": 7000, "freeze_after_cut": True},
        "linear_generic_basis": {"nonlinear": False},
        "six_feature_basis": {"n_features": 6},
    }
    keys = [
        "late_hold_accuracy",
        "a_effective_feature_count", "b_effective_feature_count",
        "a_max_feature_mass", "b_max_feature_mass",
        "a_max_axis_loading", "b_max_axis_loading",
    ]
    metrics = {}
    for name, kwargs in arms.items():
        rows = [run_generic_basis_world(seed=s, n_steps=10_000, **kwargs) for s in seeds]
        metrics[name] = summarize(rows, keys)

    path = Path(__file__).resolve().parents[1] / "results" / "gate15_generic_basis_metrics.json"
    path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    for name, value in metrics.items():
        print(name)
        for key, stat in value.items():
            print(f"  {key:30s} {stat['mean']:.6f} +/- {stat['std']:.6f}")


if __name__ == "__main__":
    main()
