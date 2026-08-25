from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from population_oja import (
    IndependentOjaPopulation,
    SangerPopulation,
    axis_recovery,
    distinct_source_claims,
    effective_rank,
    lag1_autocorrelations,
    lag_only_world,
    mean_weight_duplication,
    pca_attacker,
    rank1_world,
    source_recovery,
    variance_world,
)


def run_seed(seed: int) -> dict[str, float]:
    world = variance_world(seed)
    oja = IndependentOjaPopulation(seed=1000 + seed).fit(world.train_x)
    sanger = SangerPopulation(epochs=8, seed=2000 + seed).fit(world.train_x)
    pca_w = pca_attacker(world.train_x)

    yo = oja.transform(world.test_x)
    ys = sanger.transform(world.test_x)
    yp = world.test_x @ pca_w.T

    kill = rank1_world(seed)
    kill_sanger = SangerPopulation(seed=3000 + seed).fit(kill.train_x)
    ykill = kill_sanger.transform(kill.test_x)

    lag = lag_only_world(seed)
    lag_sanger = SangerPopulation(seed=4000 + seed).fit(lag.train_x)
    lag_pca_w = pca_attacker(lag.train_x)
    ylag_sanger = lag_sanger.transform(lag.test_x)
    ylag_pca = lag.test_x @ lag_pca_w.T

    return {
        "seed": float(seed),
        "oja_duplication": mean_weight_duplication(oja.W),
        "oja_axis_recovery": axis_recovery(oja.W, world.source_axes),
        "oja_source_recovery": source_recovery(yo, world.test_sources),
        "oja_claims": float(distinct_source_claims(yo, world.test_sources)),
        "sanger_duplication": mean_weight_duplication(sanger.W),
        "sanger_axis_recovery": axis_recovery(sanger.W, world.source_axes),
        "sanger_source_recovery": source_recovery(ys, world.test_sources),
        "sanger_claims": float(distinct_source_claims(ys, world.test_sources)),
        "pca_axis_recovery": axis_recovery(pca_w, world.source_axes),
        "pca_source_recovery": source_recovery(yp, world.test_sources),
        "rank1_sanger_effective_rank": effective_rank(ykill),
        "lag_only_sanger_source_recovery": source_recovery(ylag_sanger, lag.test_sources),
        "lag_only_pca_source_recovery": source_recovery(ylag_pca, lag.test_sources),
        "lag_only_sanger_duplication": mean_weight_duplication(lag_sanger.W),
        "lag_only_lag1_spread": float(np.ptp(lag1_autocorrelations(lag.train_sources))),
    }


def main() -> None:
    rows = [run_seed(seed) for seed in range(12)]

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in rows]))

    def std(key: str) -> float:
        return float(np.std([r[key] for r in rows]))

    print("\n=== GATE 4: population differentiation ===")
    print("One missing verb only: can several normalized-Hebbian points divide structure?\n")
    print("VARIANCE WORLD (4 real modes, all points see the same 4-D mixture)")
    print(f"independent Oja  duplication {mean('oja_duplication'):.4f}  source recovery {mean('oja_source_recovery'):.4f}  claims {mean('oja_claims'):.2f}/4")
    print(f"Sanger / GHA     duplication {mean('sanger_duplication'):.4f}  source recovery {mean('sanger_source_recovery'):.4f}  claims {mean('sanger_claims'):.2f}/4")
    print(f"explicit PCA                      source recovery {mean('pca_source_recovery'):.4f}")
    print(f"Sanger axis recovery             {mean('sanger_axis_recovery'):.4f} ± {std('sanger_axis_recovery'):.4f}")
    print(f"PCA axis recovery                {mean('pca_axis_recovery'):.4f} ± {std('pca_axis_recovery'):.4f}\n")

    print("RANK-1 KILL WORLD")
    print(f"Sanger output effective rank     {mean('rank1_sanger_effective_rank'):.4f}  (want ~1; orthogonal weights cannot invent information)\n")

    print("LAG-ONLY BOUNDARY WORLD (equal zero-lag variance, distinct temporal laws)")
    print(f"lag-1 autocorrelation spread     {mean('lag_only_lag1_spread'):.4f}")
    print(f"Sanger source recovery           {mean('lag_only_sanger_source_recovery'):.4f}")
    print(f"PCA source recovery              {mean('lag_only_pca_source_recovery'):.4f}")
    print(f"Sanger weight duplication        {mean('lag_only_sanger_duplication'):.4f}")
    print("Low duplication here is NOT a win: covariance is spherical, so the orthogonal basis is arbitrary.\n")

    metrics = {"n_seeds": len(rows)}
    for key in rows[0]:
        if key == "seed":
            continue
        metrics[f"{key}_mean"] = mean(key)
        metrics[f"{key}_std"] = std(key)
    out = ROOT / "results" / "gate4_population_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
