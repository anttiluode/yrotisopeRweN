from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from growing_matrix import (
    GrowingRelationMatrix,
    SignedGlobalAttacker,
    UnlimitedMatrixGrowth,
    make_growing_matrix_world,
    nmse,
    pattern_mass,
)


def run(seed: int) -> dict:
    w = make_growing_matrix_world(seed=seed)
    cut = int(0.60 * len(w["features"]))
    Xtr, Xte = w["features"][:cut], w["features"][cut:]
    y1tr, y1te = w["target1"][:cut], w["target1"][cut:]
    y2tr, y2te = w["target2"][:cut], w["target2"][cut:]
    p1, p2 = w["pattern1"], w["pattern2"]

    grow = GrowingRelationMatrix(seed=seed).develop(Xtr, y1tr)
    phase1_nmse = nmse(grow.predict(Xte), y1te)
    phase1_mass = pattern_mass(grow.mass, p1)
    phase1_matrix = grow.matrix.copy()

    switch_epoch = 121
    for epoch in range(1, 121):
        grow.develop(Xtr, y2tr, epochs=1)
        if pattern_mass(grow.mass, p2) > 0.90:
            switch_epoch = epoch
            break
    if switch_epoch <= 120:
        grow.develop(Xtr, y2tr, epochs=120 - switch_epoch)

    phase2_nmse = nmse(grow.predict(Xte), y2te)
    phase2_mass = pattern_mass(grow.mass, p2)
    phase2_matrix = grow.matrix.copy()

    no_consequence = GrowingRelationMatrix(seed=seed).develop(
        Xtr, y1tr, use_consequence=False
    )
    no_consequence_nmse = nmse(no_consequence.predict(Xte), y1te)
    no_consequence_mass = pattern_mass(no_consequence.mass, p1)

    shuffled = GrowingRelationMatrix(seed=seed).develop(
        Xtr, y1tr, shuffle_eligibility=True
    )
    shuffled_nmse = nmse(shuffled.predict(Xte), y1te)
    shuffled_mass = pattern_mass(shuffled.mass, p1)

    frozen = GrowingRelationMatrix(reserve=0.0, seed=seed).develop(Xtr, y1tr)
    frozen.hard_consolidate(threshold=0.01)
    frozen.develop(Xtr, y2tr, epochs=120)
    frozen_nmse = nmse(frozen.predict(Xte), y2te)
    frozen_new_mass = pattern_mass(frozen.mass, p2)

    unlimited = UnlimitedMatrixGrowth().develop(Xtr, y1tr)
    unlimited.develop(Xtr, y2tr, epochs=120)
    unlimited_nmse = nmse(unlimited.predict(Xte), y2te)

    attacker = SignedGlobalAttacker().develop(Xtr, y1tr)
    attacker_phase1_nmse = nmse(attacker.predict(Xte), y1te)
    attacker.develop(Xtr, y2tr)
    attacker_phase2_nmse = nmse(attacker.predict(Xte), y2te)

    return {
        "seed": seed,
        "phase1_nmse": phase1_nmse,
        "phase1_pattern_mass": phase1_mass,
        "switch_epoch": switch_epoch,
        "phase2_nmse": phase2_nmse,
        "phase2_pattern_mass": phase2_mass,
        "no_consequence_nmse": no_consequence_nmse,
        "no_consequence_pattern_mass": no_consequence_mass,
        "shuffled_eligibility_nmse": shuffled_nmse,
        "shuffled_eligibility_pattern_mass": shuffled_mass,
        "hard_pruned_phase2_nmse": frozen_nmse,
        "hard_pruned_new_pattern_mass": frozen_new_mass,
        "unlimited_growth_phase2_nmse": unlimited_nmse,
        "attacker_phase1_nmse": attacker_phase1_nmse,
        "attacker_phase2_nmse": attacker_phase2_nmse,
        "phase1_matrix": phase1_matrix.tolist(),
        "phase2_matrix": phase2_matrix.tolist(),
    }


def main() -> None:
    rows = [run(s) for s in range(12)]

    scalar_keys = [
        "phase1_nmse",
        "phase1_pattern_mass",
        "switch_epoch",
        "phase2_nmse",
        "phase2_pattern_mass",
        "no_consequence_nmse",
        "no_consequence_pattern_mass",
        "shuffled_eligibility_nmse",
        "shuffled_eligibility_pattern_mass",
        "hard_pruned_phase2_nmse",
        "hard_pruned_new_pattern_mass",
        "unlimited_growth_phase2_nmse",
        "attacker_phase1_nmse",
        "attacker_phase2_nmse",
    ]
    summary = {
        key + "_mean": float(np.mean([r[key] for r in rows]))
        for key in scalar_keys
    }
    summary.update({
        key + "_std": float(np.std([r[key] for r in rows]))
        for key in scalar_keys
    })
    summary["n_seeds"] = len(rows)
    summary["n_channels"] = 6
    summary["n_candidate_cells"] = 36
    summary["global_budget"] = 1.0
    summary["reserve_per_cell"] = 0.001
    summary["consequence_delay"] = 8
    summary["phase1_matrix_seed0"] = rows[0]["phase1_matrix"]
    summary["phase2_matrix_seed0"] = rows[0]["phase2_matrix"]

    print("\n=== GATE 10: GROWING MATRIX ===")
    print("36 candidate relation cells; ONE conserved capacity pool; no hand-written rivals.\n")
    print(f"phase 1: NMSE {summary['phase1_nmse_mean']:.6f}"
          f"  useful matrix mass {summary['phase1_pattern_mass_mean']:.4f}")
    print(f"reversal: new pattern >.90 mass after"
          f" {summary['switch_epoch_mean']:.2f} ± {summary['switch_epoch_std']:.2f} epochs")
    print(f"phase 2: NMSE {summary['phase2_nmse_mean']:.6f}"
          f"  new useful mass {summary['phase2_pattern_mass_mean']:.4f}")
    print(f"no consequence: NMSE {summary['no_consequence_nmse_mean']:.4f}"
          f"  useful mass {summary['no_consequence_pattern_mass_mean']:.4f}")
    print(f"shuffled eligibility: NMSE {summary['shuffled_eligibility_nmse_mean']:.4f}"
          f"  useful mass {summary['shuffled_eligibility_pattern_mass_mean']:.4f}")
    print(f"hard prune + zero reserve after reversal: NMSE"
          f" {summary['hard_pruned_phase2_nmse_mean']:.4f}"
          f"  new mass {summary['hard_pruned_new_pattern_mass_mean']:.4f}")
    print(f"unlimited positive growth after reversal: NMSE"
          f" {summary['unlimited_growth_phase2_nmse_mean']:.4f}")
    print(f"signed global attacker: phase1 {summary['attacker_phase1_nmse_mean']:.3e}"
          f"  phase2 {summary['attacker_phase2_nmse_mean']:.3e}")

    out = ROOT / "results" / "gate10_growing_matrix_metrics.json"
    out.write_text(json.dumps({"summary": summary, "seeds": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
