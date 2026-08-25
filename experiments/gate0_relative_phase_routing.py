from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from oscillating_point import (
    CompetitivePhaseReceivers,
    fixed_phase_receivers,
    fit_linear_multioutput,
    output_duplication,
    permutation_recovery,
    phase_feature_attacker,
    phase_locked_world,
    predict_linear,
)


def run_seed(seed: int, same_phase: bool = False) -> dict[str, float | list[float]]:
    centers = (0.0, 0.0) if same_phase else (0.0, np.pi)
    world = phase_locked_world(preferred_phases=centers, seed=seed)
    p, s, x = world["phase"], world["sources"], world["mixture"]
    split = int(0.60 * len(x))

    static = np.column_stack([x, x])
    global_gate = fixed_phase_receivers(x, p, [0.0, 0.0])

    rng = np.random.default_rng(seed + 1000)
    random_theta = rng.uniform(-np.pi, np.pi, 2)
    random_phase = fixed_phase_receivers(x, p, random_theta)

    learner = CompetitivePhaseReceivers(seed=seed + 2000)
    learner.fit(x[:split], p[:split], passes=5)
    learned = learner.transform(x, p)

    oracle = fixed_phase_receivers(x, p, np.asarray(centers))

    feat = phase_feature_attacker(x, p)
    w = fit_linear_multioutput(feat[:split], s[:split])
    attacker = predict_linear(feat, w)

    sl = slice(split, None)
    return {
        "static": permutation_recovery(static[sl], s[sl]),
        "global_oscillation": permutation_recovery(global_gate[sl], s[sl]),
        "random_phase": permutation_recovery(random_phase[sl], s[sl]),
        "learned_phase": permutation_recovery(learned[sl], s[sl]),
        "oracle_phase": permutation_recovery(oracle[sl], s[sl]),
        "phase_feature_attacker": permutation_recovery(attacker[sl], s[sl]),
        "learned_duplication": output_duplication(learned[sl]),
        "learned_theta": learner.theta.tolist(),
    }


def summarize(rows: list[dict]) -> dict:
    keys = [k for k in rows[0] if k != "learned_theta"]
    out = {}
    for key in keys:
        vals = np.asarray([r[key] for r in rows], dtype=float)
        out[key] = {"mean": float(vals.mean()), "std": float(vals.std(ddof=0))}
    out["learned_theta"] = [r["learned_theta"] for r in rows]
    return out


def main() -> None:
    seeds = list(range(8))
    phase_separated = [run_seed(s, same_phase=False) for s in seeds]
    same_phase = [run_seed(s, same_phase=True) for s in seeds]
    receipt = {
        "description": "Gate 0: same scalar mixture, routing by arrival phase relative to receiver oscillators",
        "seeds": seeds,
        "phase_separated": summarize(phase_separated),
        "negative_control_same_phase": summarize(same_phase),
    }
    out = ROOT / "results" / "gate0_relative_phase_routing.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
