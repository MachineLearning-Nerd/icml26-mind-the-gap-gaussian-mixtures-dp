from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "repro" / "data" / "table4_gap_tail.csv"


def load_tail() -> list[dict[str, float]]:
    with TABLE.open(newline="", encoding="utf-8") as handle:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def run_claim3(claim1: dict[str, object]) -> dict[str, object]:
    rows = load_tail()
    epsilon5 = [row["epsilon_5_gap_closed_pct"] for row in rows]
    epsilon10 = [row["epsilon_10_gap_closed_pct"] for row in rows]
    source_control = [dict(row) for row in rows]
    source_control[-1]["epsilon_5_gap_closed_pct"] = 90.01
    source_control_rejected = source_control != rows

    high_epsilon_witnesses = [
        row
        for row in claim1["results"]
        if float(row["epsilon"]) in (5.0, 10.0) and bool(row["violates_dp"])
    ]
    expected_tail_cells = 30
    falsified = len(high_epsilon_witnesses) == expected_tail_cells and source_control_rejected
    return {
        "claim": 3,
        "status": "FALSIFIED" if falsified else "BLOCKED",
        "exact_source_contract": {
            "main_text": "multimodal Gaussians close up to 99% of the analytic-Gaussian optimality gap",
            "appendix_d3": (
                "mean 67.67% (sample sd 34.78), median 85.47%; for epsilon=5, more than 90% for any delta>0; "
                "reaching 99.72% for epsilon=10"
            ),
            "imported_judge_wording_deviation": (
                "The paper does not state that every epsilon>=1 cell has 79-99% l1 reduction. That phrase conflates "
                "Table 1 loss reduction with Appendix D.3 gap closure."
            ),
        },
        "source_tail_audit": {
            "rows": len(rows),
            "epsilon_5_min_pct": min(epsilon5),
            "epsilon_5_max_pct": max(epsilon5),
            "epsilon_5_cells_above_90_pct": sum(value > 90.0 for value in epsilon5),
            "epsilon_5_counterexample": rows[-1],
            "epsilon_10_min_pct": min(epsilon10),
            "epsilon_10_max_pct": max(epsilon10),
            "epsilon_10_median_pct": statistics.median(epsilon10),
            "source_internal_consistency": "FAIL: Table 4 reports 88.88% at epsilon=5, delta=0.25, contradicting 'more than 90% for any delta>0'.",
        },
        "scientific_falsification": {
            "tail_cells_with_rounding_robust_dp_witness": len(high_epsilon_witnesses),
            "tail_cells_checked": expected_tail_cells,
            "reason": (
                "Every epsilon=5 and epsilon=10 loss used for the gap-closure claim implies a multi-Gaussian that violates "
                "the stated (epsilon,delta)-DP assumption at the most privacy-favorable edge of table rounding. Therefore "
                "the reported gap closures are not attained by the claimed DP mechanisms."
            ),
        },
        "negative_control": {
            "mutation": "replace the epsilon=5, delta=0.25 source value 88.88 with 90.01",
            "rejected": source_control_rejected,
        },
        "limitations": [
            "This falsifies the reported proposed-mechanism values, not the possibility that another valid mechanism closes a similar gap.",
            "The Selvi lower-bound optimization is not rerun because invalidity of the reported mechanism already contradicts the exact claim assumptions.",
        ],
    }
