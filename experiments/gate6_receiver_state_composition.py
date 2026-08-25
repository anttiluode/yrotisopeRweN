from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from receiver_composition import (
    conjunction_basis,
    fit_ridge,
    make_paired_world,
    nmse,
    phase_compose,
    predict_ridge,
    scalar_mode_compose,
    state_conditioned_linear_features,
)


def run(seed: int) -> dict[str, float]:
    w = make_paired_world(seed=seed)
    n_pairs = int(w["pair_id"].max()) + 1
    cut_pair = int(0.60 * n_pairs)
    train = w["pair_id"] < cut_pair
    test = ~train

    A, B = w["A"], w["B"]
    q = conjunction_basis(A, B)
    y = w["target"]

    phase = phase_compose(A[test], B[test], w["theta"][test])
    scalar_switch = scalar_mode_compose(A[test], B[test], w["mode"][test])

    static_w = fit_ridge(q[train], y[train])
    static_bilinear = predict_ridge(q[test], static_w)

    linear_features = state_conditioned_linear_features(A, B, w["theta"])
    linear_w = fit_ridge(linear_features[train], y[train])
    state_linear = predict_ridge(linear_features[test], linear_w)

    rng = np.random.default_rng(1000 + seed)
    shuffled_theta = w["theta"][test].copy()
    rng.shuffle(shuffled_theta)
    shuffled_state = phase_compose(A[test], B[test], shuffled_theta)

    frozen_state = phase_compose(A[test], B[test], np.zeros(np.sum(test)))

    # Literal same-broadcast rebinding: evaluate each unseen A,B pair at
    # theta=0 -> theta=pi -> theta=0, with no weight/topology change.
    pair_first = np.flatnonzero(test)[::2]
    Ar = A[pair_first]
    Br = B[pair_first]
    y0 = phase_compose(Ar, Br, np.zeros(len(Ar)))
    y1 = phase_compose(Ar, Br, np.full(len(Ar), np.pi))
    y0_again = phase_compose(Ar, Br, np.zeros(len(Ar)))

    return {
        "seed": float(seed),
        "phase_nmse": nmse(phase, y[test]),
        "scalar_switch_nmse": nmse(scalar_switch, y[test]),
        "phase_switch_max_abs": float(np.max(np.abs(phase - scalar_switch))),
        "static_bilinear_nmse": nmse(static_bilinear, y[test]),
        "state_linear_nmse": nmse(state_linear, y[test]),
        "shuffled_state_nmse": nmse(shuffled_state, y[test]),
        "frozen_state_nmse": nmse(frozen_state, y[test]),
        "rebind_relation_gap": float(np.mean(np.abs(y1 - y0))),
        "roundtrip_max_abs": float(np.max(np.abs(y0 - y0_again))),
    }


def main() -> None:
    rows = [run(s) for s in range(12)]
    keys = [k for k in rows[0] if k != "seed"]

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in rows]))

    def std(key: str) -> float:
        return float(np.std([r[key] for r in rows]))

    print("\n=== GATE 6: COMPOSE — same broadcasts, different receiver state ===\n")
    print(f"phase-state composer      NMSE {mean('phase_nmse'):.6g}")
    print(f"scalar mode switch        NMSE {mean('scalar_switch_nmse'):.6g}")
    print(f"phase vs scalar max |d|        {mean('phase_switch_max_abs'):.3e}")
    print(
        f"static bilinear no state  NMSE {mean('static_bilinear_nmse'):.4f}"
        f" ± {std('static_bilinear_nmse'):.4f}"
    )
    print(
        f"state-gated LINEAR        NMSE {mean('state_linear_nmse'):.4f}"
        f" ± {std('state_linear_nmse'):.4f}"
    )
    print(
        f"shuffled receiver state   NMSE {mean('shuffled_state_nmse'):.4f}"
        f" ± {std('shuffled_state_nmse'):.4f}"
    )
    print(
        f"frozen receiver state     NMSE {mean('frozen_state_nmse'):.4f}"
        f" ± {std('frozen_state_nmse'):.4f}"
    )
    print(f"mean output change on rebind   {mean('rebind_relation_gap'):.4f}")
    print(f"0 -> pi -> 0 roundtrip |d|    {mean('roundtrip_max_abs'):.3e}")

    metrics = {"n_seeds": 12}
    for key in keys:
        metrics[key + "_mean"] = mean(key)
        metrics[key + "_std"] = std(key)

    out = ROOT / "results" / "gate6_composition_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
