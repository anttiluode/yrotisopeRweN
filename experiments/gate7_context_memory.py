from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from receiver_composition import nmse, scalar_mode_compose
from receiver_context import (
    CircularContextReceiver,
    ScalarContextReceiver,
    explicit_context_features,
    fit_ridge,
    make_context_world,
    make_distractors,
    paired_contrast_nmse,
    predict_ridge,
    stateless_bilinear_features,
)

GAPS = (0, 1, 2, 4, 8, 16, 32, 64)


def split_world(w: dict[str, np.ndarray], frac: float = 0.60):
    n_pairs = int(w["pair_id"].max() + 1)
    cut_rows = 2 * int(frac * n_pairs)
    train = {key: value[:cut_rows] for key, value in w.items()}
    test = {key: value[cut_rows:] for key, value in w.items()}
    return train, test


def run(seed: int) -> dict:
    w = make_context_world(n_pairs=3500, seed=seed)
    train, test = split_world(w)

    stateless_w = fit_ridge(
        stateless_bilinear_features(train["A"], train["B"]),
        train["target"],
    )
    explicit_w = fit_ridge(
        explicit_context_features(train["A"], train["B"], train["context"]),
        train["target"],
    )
    stateless_pred = predict_ridge(
        stateless_bilinear_features(test["A"], test["B"]), stateless_w
    )
    explicit_pred = predict_ridge(
        explicit_context_features(test["A"], test["B"], test["context"]),
        explicit_w,
    )
    current_cheat = scalar_mode_compose(test["A"], test["B"], test["context"])

    row = {
        "seed": seed,
        "stateless_bilinear_nmse": nmse(stateless_pred, test["target"]),
        "stateless_bilinear_contrast_nmse": paired_contrast_nmse(
            stateless_pred, test["target"], test["pair_id"]
        ),
        "explicit_context_buffer_nmse": nmse(explicit_pred, test["target"]),
        "current_context_cheat_nmse": nmse(current_cheat, test["target"]),
        "gaps": {},
    }

    circular = CircularContextReceiver()
    scalar = ScalarContextReceiver()
    true_sign = np.where(test["context"] == 0.0, 1.0, -1.0)

    for gap in GAPS:
        real, imag = make_distractors(
            len(test["A"]), gap, seed=10000 + seed * 101 + gap
        )
        z = circular.state_after(test["context"], real, imag)
        h = scalar.state_after(test["context"], real)
        circular_pred = circular.compose(test["A"], test["B"], z)
        scalar_pred = scalar.compose(test["A"], test["B"], h)

        reset_pred = circular.compose(
            test["A"],
            test["B"],
            np.zeros(len(test["A"]), dtype=complex),
        )

        rng = np.random.default_rng(20000 + seed * 101 + gap)
        shuffled_context = test["context"][rng.permutation(len(test["context"]))]
        z_shuffled = circular.state_after(shuffled_context, real, imag)
        shuffled_pred = circular.compose(test["A"], test["B"], z_shuffled)

        row["gaps"][str(gap)] = {
            "circular_nmse": nmse(circular_pred, test["target"]),
            "scalar_nmse": nmse(scalar_pred, test["target"]),
            "circular_context_accuracy": float(np.mean(np.sign(z.real) == true_sign)),
            "scalar_context_accuracy": float(np.mean(np.sign(h) == true_sign)),
            "circular_contrast_nmse": paired_contrast_nmse(
                circular_pred, test["target"], test["pair_id"]
            ),
            "scalar_contrast_nmse": paired_contrast_nmse(
                scalar_pred, test["target"], test["pair_id"]
            ),
            "state_reset_nmse": nmse(reset_pred, test["target"]),
            "state_reset_contrast_nmse": paired_contrast_nmse(
                reset_pred, test["target"], test["pair_id"]
            ),
            "shuffled_context_nmse": nmse(shuffled_pred, test["target"]),
            "shuffled_context_contrast_nmse": paired_contrast_nmse(
                shuffled_pred, test["target"], test["pair_id"]
            ),
        }

    return row


def main() -> None:
    rows = [run(seed) for seed in range(12)]

    def mean(key: str) -> float:
        return float(np.mean([row[key] for row in rows]))

    def std(key: str) -> float:
        return float(np.std([row[key] for row in rows]))

    def gapmean(gap: int, key: str) -> float:
        return float(np.mean([row["gaps"][str(gap)][key] for row in rows]))

    def gapstd(gap: int, key: str) -> float:
        return float(np.std([row["gaps"][str(gap)][key] for row in rows]))

    print("\n=== GATE 7: CONTEXT ===")
    print("context happens -> disappears -> gap/distractors -> identical broadcasts")
    print("no mode input is present at composition time; no weights change.\n")
    print(f"stateless bilinear          NMSE {mean('stateless_bilinear_nmse'):.4f}")
    print(f"explicit context buffer    NMSE {mean('explicit_context_buffer_nmse'):.6f}")
    print(f"current-context cheat      NMSE {mean('current_context_cheat_nmse'):.6f}\n")
    print("gap   circular NMSE      scalar NMSE       context decode")
    for gap in GAPS:
        print(
            f"{gap:>3}   "
            f"{gapmean(gap, 'circular_nmse'):.4f} ± {gapstd(gap, 'circular_nmse'):.4f}   "
            f"{gapmean(gap, 'scalar_nmse'):.4f} ± {gapstd(gap, 'scalar_nmse'):.4f}   "
            f"{gapmean(gap, 'circular_context_accuracy'):.4f}"
        )

    print("\nKills:")
    print(
        "state reset               "
        f"NMSE {gapmean(8, 'state_reset_nmse'):.4f}; "
        f"contrast NMSE {gapmean(8, 'state_reset_contrast_nmse'):.4f}"
    )
    print(
        "shuffled old context @8   "
        f"NMSE {gapmean(8, 'shuffled_context_nmse'):.4f}"
    )

    curve_keys = list(rows[0]["gaps"]["0"].keys())
    metrics = {
        "n_seeds": 12,
        "gaps": list(GAPS),
        "stateless_bilinear_nmse_mean": mean("stateless_bilinear_nmse"),
        "stateless_bilinear_nmse_std": std("stateless_bilinear_nmse"),
        "stateless_bilinear_contrast_nmse_mean": mean(
            "stateless_bilinear_contrast_nmse"
        ),
        "explicit_context_buffer_nmse_mean": mean("explicit_context_buffer_nmse"),
        "current_context_cheat_nmse_mean": mean("current_context_cheat_nmse"),
        "memory_curve": {
            str(gap): {
                **{key + "_mean": gapmean(gap, key) for key in curve_keys},
                **{
                    key + "_std": gapstd(gap, key)
                    for key in (
                        "circular_nmse",
                        "scalar_nmse",
                        "circular_context_accuracy",
                    )
                },
            }
            for gap in GAPS
        },
    }
    out = ROOT / "results" / "gate7_context_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
