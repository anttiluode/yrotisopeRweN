from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from capacity_allocation import (
    ConservedGrowthAllocator,
    PHASE1_PATTERN,
    PHASE2_PATTERN,
    SignedProjectedAttacker,
    UnlimitedPositiveGrowth,
    make_allocation_world,
    nmse,
    useful_mass,
)


def switch_latency(
    model: ConservedGrowthAllocator,
    features: np.ndarray,
    target: np.ndarray,
    threshold: float = 0.90,
    max_epochs: int = 120,
) -> int | None:
    for epoch in range(1, max_epochs + 1):
        model.develop(features, target, epochs=1)
        if useful_mass(model.mass, PHASE2_PATTERN) >= threshold:
            return epoch
    return None


def run(seed: int) -> dict:
    w = make_allocation_world(n_trials=10_000, seed=seed)
    X = w["features"]
    target1 = w["target1"]
    target2 = w["target2"]

    main = ConservedGrowthAllocator(reserve=0.02, seed=seed).develop(
        X, target1, epochs=120
    ).hard_consolidate()
    phase1_mass = main.mass.copy()
    phase1_nmse = nmse(main.predict(X), target1)
    phase1_useful = useful_mass(main.mass, PHASE1_PATTERN)

    probe = ConservedGrowthAllocator(reserve=0.02, seed=seed)
    probe.mass = main.mass.copy()
    latency = switch_latency(probe, X, target2)

    main.develop(X, target2, epochs=120)
    phase2_mass = main.mass.copy()
    phase2_nmse = nmse(main.predict(X), target2)
    phase2_useful = useful_mass(main.mass, PHASE2_PATTERN)

    frozen = ConservedGrowthAllocator(reserve=0.0, seed=seed).develop(
        X, target1, epochs=120
    ).hard_consolidate()
    frozen.develop(X, target2, epochs=120)

    unlimited = UnlimitedPositiveGrowth().develop(X, target1, epochs=120)
    unlimited_phase1_nmse = nmse(unlimited.predict(X), target1)
    unlimited.develop(X, target2, epochs=120)

    signed = SignedProjectedAttacker().develop(X, target1, epochs=40)
    signed_phase1_nmse = nmse(signed.predict(X), target1)
    signed.develop(X, target2, epochs=40)

    no_consequence = ConservedGrowthAllocator(
        reserve=0.02, seed=100 + seed
    ).develop(X, target1, epochs=120, use_consequence=False)
    shuffled = ConservedGrowthAllocator(
        reserve=0.02, seed=200 + seed
    ).develop(X, target1, epochs=120, shuffle_eligibility=True)

    return {
        "seed": seed,
        "phase1_nmse": phase1_nmse,
        "phase1_useful_mass": phase1_useful,
        "phase1_mass": phase1_mass.tolist(),
        "switch_latency": latency,
        "phase2_nmse": phase2_nmse,
        "phase2_useful_mass": phase2_useful,
        "phase2_mass": phase2_mass.tolist(),
        "zero_reserve_phase2_nmse": nmse(frozen.predict(X), target2),
        "zero_reserve_phase2_useful_mass": useful_mass(
            frozen.mass, PHASE2_PATTERN
        ),
        "unlimited_phase1_nmse": unlimited_phase1_nmse,
        "unlimited_phase2_nmse": nmse(unlimited.predict(X), target2),
        "signed_phase1_nmse": signed_phase1_nmse,
        "signed_phase2_nmse": nmse(signed.predict(X), target2),
        "no_consequence_phase1_nmse": nmse(
            no_consequence.predict(X), target1
        ),
        "shuffled_eligibility_phase1_nmse": nmse(
            shuffled.predict(X), target1
        ),
    }


def main() -> None:
    rows = [run(seed) for seed in range(12)]

    def mean(key: str) -> float:
        return float(np.mean([row[key] for row in rows]))

    def std(key: str) -> float:
        return float(np.std([row[key] for row in rows]))

    mean_phase1_mass = np.mean([row["phase1_mass"] for row in rows], axis=0)
    mean_phase2_mass = np.mean([row["phase2_mass"] for row in rows], axis=0)

    print("\n=== GATE 9: ALLOCATE / CONSOLIDATE ===")
    print("positive utility can only grow local claims; pair budgets force reallocation")
    print("after consolidation, usefulness reverses.\n")
    print(f"phase 1 useful mass        {mean('phase1_useful_mass'):.4f}")
    print(f"phase 1 NMSE               {mean('phase1_nmse'):.6f}")
    print(f"phase 1 mean mass          {np.round(mean_phase1_mass, 4)}")
    print(f"switch latency to >.90     {mean('switch_latency'):.1f} epochs")
    print(f"phase 2 useful mass        {mean('phase2_useful_mass'):.4f}")
    print(f"phase 2 NMSE               {mean('phase2_nmse'):.6f}")
    print(f"phase 2 mean mass          {np.round(mean_phase2_mass, 4)}\n")

    print("Kills / attackers:")
    print(f"zero reserve after prune   phase2 NMSE {mean('zero_reserve_phase2_nmse'):.4f}")
    print(f"unlimited positive growth  phase1 {mean('unlimited_phase1_nmse'):.6f} -> phase2 {mean('unlimited_phase2_nmse'):.4f}")
    print(f"no consequence             phase1 NMSE {mean('no_consequence_phase1_nmse'):.4f}")
    print(f"shuffled eligibility       phase1 NMSE {mean('shuffled_eligibility_phase1_nmse'):.4f}")
    print(f"signed projected attacker  phase1 {mean('signed_phase1_nmse'):.6f} -> phase2 {mean('signed_phase2_nmse'):.6f}")

    metrics = {
        "n_seeds": 12,
        "reserve": 0.02,
        "hard_prune_threshold": 0.01,
        "phase1_nmse_mean": mean("phase1_nmse"),
        "phase1_nmse_std": std("phase1_nmse"),
        "phase1_useful_mass_mean": mean("phase1_useful_mass"),
        "phase1_mass_mean": mean_phase1_mass.tolist(),
        "switch_latency_mean": mean("switch_latency"),
        "switch_latency_std": std("switch_latency"),
        "phase2_nmse_mean": mean("phase2_nmse"),
        "phase2_nmse_std": std("phase2_nmse"),
        "phase2_useful_mass_mean": mean("phase2_useful_mass"),
        "phase2_mass_mean": mean_phase2_mass.tolist(),
        "zero_reserve_phase2_nmse_mean": mean("zero_reserve_phase2_nmse"),
        "zero_reserve_phase2_useful_mass_mean": mean(
            "zero_reserve_phase2_useful_mass"
        ),
        "unlimited_phase1_nmse_mean": mean("unlimited_phase1_nmse"),
        "unlimited_phase2_nmse_mean": mean("unlimited_phase2_nmse"),
        "signed_phase1_nmse_mean": mean("signed_phase1_nmse"),
        "signed_phase2_nmse_mean": mean("signed_phase2_nmse"),
        "no_consequence_phase1_nmse_mean": mean("no_consequence_phase1_nmse"),
        "shuffled_eligibility_phase1_nmse_mean": mean(
            "shuffled_eligibility_phase1_nmse"
        ),
    }
    out = ROOT / "results" / "gate9_capacity_metrics.json"
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
