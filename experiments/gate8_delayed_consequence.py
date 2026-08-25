from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from consequence_learning import (
    DelayedConsequenceLearner,
    cosine_alignment,
    fit_ridge,
    make_consequence_world,
    nmse,
    predict_ridge,
)

DELAYS = (0, 4, 8, 16, 32)


def run(seed: int) -> dict:
    w = make_consequence_world(n_trials=12_000, context_gap=4, seed=seed)
    cut = 8000
    train_features = w["features"][:cut]
    train_target = w["target"][:cut]
    test_features = w["features"][cut:]
    test_target = w["target"][cut:]

    row = {"seed": seed, "delays": {}}
    for delay in DELAYS:
        learner = DelayedConsequenceLearner(seed=100 + seed).fit(
            train_features,
            train_target,
            consequence_delay=delay,
        )
        pred = learner.predict(test_features)
        row["delays"][str(delay)] = {
            "nmse": nmse(pred, test_target),
            "weight_alignment": cosine_alignment(
                learner.weights, w["true_weights"]
            ),
        }

    no_trace = DelayedConsequenceLearner(seed=200 + seed).fit(
        train_features,
        train_target,
        consequence_delay=8,
        use_eligibility=False,
    )
    shuffled_consequence = DelayedConsequenceLearner(seed=300 + seed).fit(
        train_features,
        train_target,
        consequence_delay=8,
        shuffle_consequence=True,
    )
    shuffled_eligibility = DelayedConsequenceLearner(seed=400 + seed).fit(
        train_features,
        train_target,
        consequence_delay=8,
        shuffle_eligibility=True,
    )

    explicit_coef = fit_ridge(w["ideal_features"][:cut], train_target)
    transient_coef = fit_ridge(train_features, train_target)
    context_only = np.column_stack([w["context"], w["state"]])
    context_coef = fit_ridge(context_only[:cut], train_target)

    row.update(
        {
            "no_trace_nmse": nmse(no_trace.predict(test_features), test_target),
            "shuffled_consequence_nmse": nmse(
                shuffled_consequence.predict(test_features), test_target
            ),
            "shuffled_eligibility_nmse": nmse(
                shuffled_eligibility.predict(test_features), test_target
            ),
            "explicit_context_buffer_nmse": nmse(
                predict_ridge(w["ideal_features"][cut:], explicit_coef), test_target
            ),
            "batch_transient_features_nmse": nmse(
                predict_ridge(test_features, transient_coef), test_target
            ),
            "context_state_only_nmse": nmse(
                predict_ridge(context_only[cut:], context_coef), test_target
            ),
        }
    )
    return row


def main() -> None:
    rows = [run(seed) for seed in range(12)]

    def mean(key: str) -> float:
        return float(np.mean([row[key] for row in rows]))

    def std(key: str) -> float:
        return float(np.std([row[key] for row in rows]))

    def delaymean(delay: int, key: str) -> float:
        return float(
            np.mean([row["delays"][str(delay)][key] for row in rows])
        )

    def delaystd(delay: int, key: str) -> float:
        return float(
            np.std([row["delays"][str(delay)][key] for row in rows])
        )

    print("\n=== GATE 8: CONSEQUENCE ===")
    print("earlier context -> transient conjunction -> delayed scalar consequence")
    print("no growth; only slow efficacy over fixed local conjunctions.\n")
    print("delay   eligibility NMSE      utility-weight alignment")
    for delay in DELAYS:
        print(
            f"{delay:>3}     "
            f"{delaymean(delay, 'nmse'):.6f} ± {delaystd(delay, 'nmse'):.6f}"
            f"      {delaymean(delay, 'weight_alignment'):.6f}"
        )

    print("\nKills / attackers @ delayed consequence:")
    print(f"no eligibility trace        {mean('no_trace_nmse'):.4f}")
    print(f"shuffled consequence        {mean('shuffled_consequence_nmse'):.4f}")
    print(f"shuffled eligibility        {mean('shuffled_eligibility_nmse'):.4f}")
    print(f"context/state only          {mean('context_state_only_nmse'):.4f}")
    print(f"batch transient features    {mean('batch_transient_features_nmse'):.6f}")
    print(f"explicit context buffer     {mean('explicit_context_buffer_nmse'):.6f}")

    metrics = {
        "n_seeds": 12,
        "context_gap": 4,
        "consequence_delays": list(DELAYS),
        "delay_curve": {
            str(delay): {
                "nmse_mean": delaymean(delay, "nmse"),
                "nmse_std": delaystd(delay, "nmse"),
                "weight_alignment_mean": delaymean(delay, "weight_alignment"),
            }
            for delay in DELAYS
        },
        "no_trace_nmse_mean": mean("no_trace_nmse"),
        "no_trace_nmse_std": std("no_trace_nmse"),
        "shuffled_consequence_nmse_mean": mean("shuffled_consequence_nmse"),
        "shuffled_consequence_nmse_std": std("shuffled_consequence_nmse"),
        "shuffled_eligibility_nmse_mean": mean("shuffled_eligibility_nmse"),
        "shuffled_eligibility_nmse_std": std("shuffled_eligibility_nmse"),
        "context_state_only_nmse_mean": mean("context_state_only_nmse"),
        "batch_transient_features_nmse_mean": mean(
            "batch_transient_features_nmse"
        ),
        "explicit_context_buffer_nmse_mean": mean(
            "explicit_context_buffer_nmse"
        ),
    }
    out = ROOT / "results" / "gate8_consequence_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
