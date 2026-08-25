from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from population_oja import SangerPopulation, lag_only_world, pca_attacker, source_recovery
from temporal_amuse import fit_amuse, same_memory_world, shuffle_time


def run_seed(seed: int) -> dict[str, float]:
    world = lag_only_world(seed)
    amuse = fit_amuse(world.train_x, lag=1)
    sanger = SangerPopulation(seed=4000 + seed).fit(world.train_x)
    pca_w = pca_attacker(world.train_x)

    shuffled_amuse = fit_amuse(shuffle_time(world.train_x, seed=9000 + seed), lag=1)

    kill = same_memory_world(seed)
    kill_amuse = fit_amuse(kill.train_x, lag=1)

    cov = np.cov(world.train_x, rowvar=False, bias=True)

    return {
        "seed": float(seed),
        "amuse_source_recovery": source_recovery(amuse.transform(world.test_x), world.test_sources),
        "sanger_source_recovery": source_recovery(sanger.transform(world.test_x), world.test_sources),
        "pca_source_recovery": source_recovery(world.test_x @ pca_w.T, world.test_sources),
        "shuffled_amuse_source_recovery": source_recovery(shuffled_amuse.transform(world.test_x), world.test_sources),
        "same_memory_amuse_source_recovery": source_recovery(kill_amuse.transform(kill.test_x), kill.test_sources),
        "lag_eigenvalue_spread": float(np.ptp(amuse.lag_eigenvalues)),
        "zero_lag_identity_error": float(np.linalg.norm(cov - np.eye(cov.shape[0]), ord="fro")),
    }


def main() -> None:
    rows = [run_seed(seed) for seed in range(12)]

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in rows]))

    def std(key: str) -> float:
        return float(np.std([r[key] for r in rows]))

    print("\n=== GATE 5: one lag gets one chance ===")
    print("Same zero-lag covariance. Different temporal laws. Does one delayed matrix identify them?\n")
    print(f"zero-lag identity error         {mean('zero_lag_identity_error'):.3e}")
    print(f"lag-eigenvalue spread          {mean('lag_eigenvalue_spread'):.4f}\n")
    print(f"PCA source recovery            {mean('pca_source_recovery'):.4f} ± {std('pca_source_recovery'):.4f}")
    print(f"Sanger source recovery         {mean('sanger_source_recovery'):.4f} ± {std('sanger_source_recovery'):.4f}")
    print(f"AMUSE(tau=1) source recovery   {mean('amuse_source_recovery'):.6f} ± {std('amuse_source_recovery'):.6f}\n")
    print(f"shuffle time -> AMUSE          {mean('shuffled_amuse_source_recovery'):.4f} ± {std('shuffled_amuse_source_recovery'):.4f}")
    print(f"same memory law -> AMUSE       {mean('same_memory_amuse_source_recovery'):.4f} ± {std('same_memory_amuse_source_recovery'):.4f}")

    metrics = {"n_seeds": len(rows)}
    for key in rows[0]:
        if key == "seed":
            continue
        metrics[f"{key}_mean"] = mean(key)
        metrics[f"{key}_std"] = std(key)
    out = ROOT / "results" / "gate5_amuse_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
