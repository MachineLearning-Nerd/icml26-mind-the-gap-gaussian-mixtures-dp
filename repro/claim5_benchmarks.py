from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path

from scipy.optimize import minimize_scalar

from claim1_continuous import load_settings
from mechanisms import analytic_gaussian_sigma


ROOT = Path(__file__).resolve().parents[1]
TABLE2 = ROOT / "repro" / "data" / "table2_high_epsilon.csv"


def truncated_laplace_l1(epsilon: float, delta: float) -> float:
    scale = 1.0 / epsilon
    cutoff = scale * math.log1p(math.expm1(epsilon) / (2.0 * delta))
    return scale - cutoff / math.expm1(cutoff / scale)


def integral_abs(lower: float, upper: float) -> float:
    if upper <= 0.0:
        return 0.5 * (lower * lower - upper * upper)
    if lower >= 0.0:
        return 0.5 * (upper * upper - lower * lower)
    return 0.5 * (lower * lower + upper * upper)


def tulap_l1(epsilon: float, delta: float, *, truncate: bool = True) -> float:
    b = math.exp(-epsilon)
    q = 2.0 * delta * b / (1.0 - b + 2.0 * delta * b) if truncate else 0.0
    target_tail = q / 2.0
    normalizer = (1.0 - b) / (1.0 + b)
    boundary = 0.5
    if q > 0.0:
        for index in range(1, 10000):
            after = b ** (index + 1) / (1.0 + b)
            weight = normalizer * b**index
            before = after + weight
            if after <= target_tail <= before:
                boundary = index + 0.5 - (target_tail - after) / weight
                break
    else:
        boundary = max(20.0, math.ceil(-math.log(1e-16) / epsilon) + 1.0)

    total = 0.0
    maximum_index = math.ceil(boundary + 0.5)
    for index in range(-maximum_index, maximum_index + 1):
        lower = max(index - 0.5, -boundary)
        upper = min(index + 0.5, boundary)
        if lower < upper:
            total += normalizer * b ** abs(index) * integral_abs(lower, upper)
    return total / (1.0 - q)


def staircase_l1(epsilon: float) -> float:
    b = math.exp(-epsilon)

    def expected(gamma: float) -> float:
        normalizer = (1.0 - b) / (2.0 * (gamma + b * (1.0 - gamma)))
        total = 0.0
        for index in range(10000):
            weight = b**index
            first = 0.5 * ((index + gamma) ** 2 - index**2)
            second = 0.5 * ((index + 1.0) ** 2 - (index + gamma) ** 2)
            total += weight * first + weight * b * second
            if weight < 1e-16:
                break
        return 2.0 * normalizer * total

    result = minimize_scalar(expected, bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-13})
    return float(result.fun)


def source_values() -> dict[tuple[float, float], float]:
    values = {}
    with TABLE2.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            delta = float(row["delta"])
            for epsilon in (2.0, 3.0, 4.0, 5.0, 10.0):
                values[(delta, epsilon)] = float(row[f"epsilon_{int(epsilon)}_pct"])
    return values


def run_claim5(claim1: dict[str, object]) -> dict[str, object]:
    settings = {(float(row["delta"]), float(row["epsilon"])): row for row in load_settings()}
    reported = source_values()
    results = []
    for (delta, epsilon), source_improvement in sorted(reported.items()):
        setting = settings[(delta, epsilon)]
        table1_improvement = float(setting["paper_improvement_pct"])
        analytic_l1 = analytic_gaussian_sigma(epsilon, delta) * math.sqrt(2.0 / math.pi)
        mixture_l1 = analytic_l1 * (1.0 - table1_improvement / 100.0)
        benchmarks = {
            "truncated_laplace": truncated_laplace_l1(epsilon, delta),
            "tulap": tulap_l1(epsilon, delta),
            "staircase": staircase_l1(epsilon),
        }
        winner = min(benchmarks, key=benchmarks.get)
        best_loss = benchmarks[winner]
        reproduced_improvement = 100.0 * (best_loss - mixture_l1) / max(best_loss, mixture_l1)
        results.append(
            {
                "epsilon": epsilon,
                "delta": delta,
                "mixture_l1_from_table1": mixture_l1,
                "benchmarks": benchmarks,
                "independent_winner": winner,
                "reproduced_improvement_pct": reproduced_improvement,
                "paper_table2_improvement_pct": source_improvement,
                "absolute_error_pp": abs(reproduced_improvement - source_improvement),
            }
        )

    errors = [row["absolute_error_pp"] for row in results]
    high_witnesses = [
        row for row in claim1["results"] if float(row["epsilon"]) >= 3.0 and bool(row["violates_dp"])
    ]
    tulap_controls = [
        tulap_l1(epsilon, delta) <= tulap_l1(epsilon, delta, truncate=False) + 1e-12
        for epsilon, delta in ((2.0, 1e-6), (5.0, 1e-3), (10.0, 0.25))
    ]
    falsified = len(results) == 75 and len(high_witnesses) == 60 and all(tulap_controls)
    return {
        "claim": 5,
        "status": "FALSIFIED" if falsified else "BLOCKED",
        "exact_source_contract": (
            "Table 2 compares the best Table 1 multimodal Gaussian against the best non-Gaussian benchmark. "
            "Appendix D.6 states that the benchmark winner is always truncated Laplace or Tulap; staircase, cactus, "
            "and flipped Huber are included in the benchmark pool but never win."
        ),
        "summary": {
            "high_epsilon_cells": len(results),
            "mean_absolute_error_pp_vs_table2": statistics.fmean(errors),
            "max_absolute_error_pp_vs_table2": max(errors),
            "cells_within_1pp": sum(error <= 1.0 for error in errors),
            "independent_winner_counts": {
                name: sum(row["independent_winner"] == name for row in results)
                for name in ("truncated_laplace", "tulap", "staircase")
            },
            "epsilon_ge_3_cells_with_rounding_robust_dp_violation": len(high_witnesses),
        },
        "results": results,
        "negative_control": {
            "mutation": "set Tulap truncation q to zero (pure-DP base distribution)",
            "rejected": all(tulap_controls),
            "reason": "removing approximate-DP tail truncation cannot lower expected absolute loss",
        },
        "named_mechanism_coverage": {
            "independently_implemented": ["truncated Laplace", "Tulap", "staircase"],
            "source-audited_only": ["cactus", "flipped Huber"],
            "paper_source_result": "Appendix D.6 says neither source-audited-only mechanism wins any tested cell.",
        },
        "falsification_basis": (
            "All 60 epsilon>=3 multimodal losses in the claimed competitive regime imply mechanisms that violate "
            "the stated DP assumption after conservative rounding. Their comparison with valid non-Gaussian DP "
            "benchmarks is therefore not a comparison at equal privacy."
        ),
        "limitations": [
            "Cactus and flipped Huber are source-audited but not independently reimplemented because neither can change the paper's stated benchmark winner.",
            "The independent benchmark comparison covers the 75 epsilon>=2 cells; source Table 2 contains 150 cells.",
        ],
    }
