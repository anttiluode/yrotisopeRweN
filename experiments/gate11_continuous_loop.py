from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from continuous_loop import run_continuous_stream, run_buffered_attacker


def summarize(rows, keys):
    out = {}
    for key in keys:
        values = np.array([np.nan if row[key] is None else row[key] for row in rows], dtype=float)
        finite = values[np.isfinite(values)]
        out[f"{key}_mean"] = None if len(finite) == 0 else float(finite.mean())
        out[f"{key}_std"] = None if len(finite) == 0 else float(finite.std())
        if key == "adaptation_steps":
            out["adaptation_success_fraction"] = float(len(finite) / len(values))
    return out


def main() -> None:
    seeds = range(6)
    arms = {
        "continuous": {},
        "no_consequence": {"use_consequence": False},
        "shuffled_eligibility": {"shuffle_eligibility": True},
        "state_only_no_explicit_trace": {"use_explicit_eligibility": False},
        "reset_on_output": {"reset_on_output": True},
        "instantaneous_compartments": {"instantaneous_compartments": True},
    }
    keys = [
        "phase1_nmse",
        "phase2_nmse",
        "phase1_useful_mass",
        "phase2_useful_mass",
        "adaptation_steps",
        "phase1_spike_f1",
        "phase2_spike_f1",
    ]

    metrics = {"n_seeds": 6, "arms": {}}
    print("\n=== GATE 11: CONTINUOUS CELL / THE LOOP DOES NOT RESET ===")
    print("One uninterrupted stream; persistent relation compartments; separate output threshold.\n")
    for name, kwargs in arms.items():
        rows = [run_continuous_stream(seed=s, **kwargs) for s in seeds]
        metrics["arms"][name] = summarize(rows, keys)
        m = metrics["arms"][name]
        print(
            f"{name:31s} "
            f"nmse {m['phase1_nmse_mean']:.4f} -> {m['phase2_nmse_mean']:.4f}  "
            f"mass {m['phase1_useful_mass_mean']:.3f} -> {m['phase2_useful_mass_mean']:.3f}  "
            f"adapt {m['adaptation_steps_mean']}"
        )

    attacker_rows = [run_buffered_attacker(seed=s) for s in seeds]
    attacker_keys = [
        "phase1_nmse",
        "phase2_nmse",
        "phase1_useful_mass",
        "phase2_useful_mass",
        "adaptation_steps",
    ]
    metrics["buffered_signed_attacker"] = summarize(attacker_rows, attacker_keys)
    a = metrics["buffered_signed_attacker"]
    print(
        f"{'buffered signed attacker':31s} "
        f"nmse {a['phase1_nmse_mean']:.6f} -> {a['phase2_nmse_mean']:.6f}  "
        f"mass {a['phase1_useful_mass_mean']:.3f} -> {a['phase2_useful_mass_mean']:.3f}  "
        f"adapt {a['adaptation_steps_mean']:.1f}"
    )

    out = ROOT / "results" / "gate11_continuous_loop_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
