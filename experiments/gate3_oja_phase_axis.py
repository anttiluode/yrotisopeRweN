from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from oscillating_point import phase_locked_world, permutation_recovery, output_duplication
from oja_phase import (
    OjaPhaseAxis,
    PlainHebbPhaseAxis,
    axis_alignment,
    nonlinear_phase_pair,
    phase_energy_features,
    signed_phase_pair,
)


def run(seed: int, preferred_phases=(0.0, np.pi)) -> dict[str, float]:
    w = phase_locked_world(seed=seed, preferred_phases=preferred_phases)
    cut = int(0.60 * len(w["mixture"]))
    U = phase_energy_features(w["mixture"][:cut], w["phase"][:cut])

    hebb = PlainHebbPhaseAxis(seed=100 + seed).fit(U, epochs=1)
    oja = OjaPhaseAxis(seed=100 + seed).fit(U)

    x = w["mixture"][cut:]
    p = w["phase"][cut:]
    S = w["sources"][cut:]
    y_linear = signed_phase_pair(x, p, oja.theta)
    y_nonlinear = nonlinear_phase_pair(x, p, oja.theta)

    return {
        "seed": seed,
        "hebb_max_norm": float(hebb.max_norm),
        "hebb_diverged": float(hebb.diverged),
        "oja_final_norm": float(np.linalg.norm(oja.w)),
        "oja_axis_alignment": axis_alignment(oja.theta, 0.0),
        "linear_recovery": permutation_recovery(y_linear, S),
        "linear_duplication": output_duplication(y_linear),
        "nonlinear_recovery": permutation_recovery(y_nonlinear, S),
        "nonlinear_duplication": output_duplication(y_nonlinear),
    }


def main() -> None:
    seeds = range(12)
    rows = [run(s) for s in seeds]
    kill = [run(s, preferred_phases=(0.0, 0.0)) for s in seeds]

    def mean(key, src=rows):
        return float(np.mean([r[key] for r in src]))

    def std(key, src=rows):
        return float(np.std([r[key] for r in src]))

    print("\n=== GATE 3: Oja under the oscillating point ===")
    print("phase lift u(t)=sqrt(energy)[cos(phi), sin(phi)]")
    print("Oja learns a phase AXIS; nonlinear complementary gates split its two ends.\n")
    print(f"plain Hebb diverged       {mean('hebb_diverged')*12:.0f}/12 seeds")
    print(f"plain Hebb max norm       {mean('hebb_max_norm'):.1f} mean (capped at 1e6)")
    print(f"Oja final norm            {mean('oja_final_norm'):.6f} ± {std('oja_final_norm'):.6f}")
    print(f"Oja axis alignment        {mean('oja_axis_alignment'):.6f} ± {std('oja_axis_alignment'):.6f}")
    print(f"linear opposite outputs   recovery {mean('linear_recovery'):.4f} ± {std('linear_recovery'):.4f}"
          f"  duplication {mean('linear_duplication'):.4f}")
    print(f"NONLINEAR phase windows   recovery {mean('nonlinear_recovery'):.4f} ± {std('nonlinear_recovery'):.4f}"
          f"  duplication {mean('nonlinear_duplication'):.4f}")
    print(f"same-phase kill world     nonlinear recovery {mean('nonlinear_recovery', kill):.4f}")

    metrics = {
        "n_seeds": 12,
        "plain_hebb_diverged_fraction": mean("hebb_diverged"),
        "plain_hebb_max_norm_mean": mean("hebb_max_norm"),
        "oja_final_norm_mean": mean("oja_final_norm"),
        "oja_final_norm_std": std("oja_final_norm"),
        "oja_axis_alignment_mean": mean("oja_axis_alignment"),
        "linear_recovery_mean": mean("linear_recovery"),
        "linear_duplication_mean": mean("linear_duplication"),
        "nonlinear_recovery_mean": mean("nonlinear_recovery"),
        "nonlinear_recovery_std": std("nonlinear_recovery"),
        "nonlinear_duplication_mean": mean("nonlinear_duplication"),
        "same_phase_nonlinear_recovery_mean": mean("nonlinear_recovery", kill),
    }
    out = ROOT / "results" / "gate3_oja_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
