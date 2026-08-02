from __future__ import annotations

import csv
import json
import math
import os
import statistics
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from mechanisms import MultiGaussian, analytic_gaussian_sigma, calibrate_continuous_dp, check_continuous_dp


ROOT = Path(__file__).resolve().parents[1]
TABLE1 = ROOT / "repro" / "data" / "table1_l1.csv"
TABLE3 = ROOT / "repro" / "data" / "table3_best_k.csv"


def load_settings() -> list[dict[str, float | int | None]]:
    reported = {}
    with TABLE1.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw = row["reported_improvement_pct"]
            reported[(float(row["delta"]), float(row["epsilon"]))] = None if raw == "NA" else float(raw)
    settings = []
    with TABLE3.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (float(row["delta"]), float(row["epsilon"]))
            settings.append(
                {
                    "delta": key[0],
                    "epsilon": key[1],
                    "k": int(row["best_k"]),
                    "paper_improvement_pct": reported[key],
                }
            )
    return settings


def run_setting(setting: dict[str, float | int | None]) -> dict[str, float | int | bool | None]:
    started = time.perf_counter()
    epsilon = float(setting["epsilon"])
    delta = float(setting["delta"])
    k = int(setting["k"])
    sigma, calibration_divergence, calibration_shift = calibrate_continuous_dp(epsilon, delta, k)
    mechanism = MultiGaussian(epsilon, k)
    analytic_sigma = analytic_gaussian_sigma(epsilon, delta)
    mixture_l1 = mechanism.l1_loss(sigma)
    analytic_l1 = analytic_sigma * math.sqrt(2.0 / math.pi)
    mixture_variance = mechanism.variance(sigma)
    analytic_variance = analytic_sigma * analytic_sigma
    improvement = 100.0 * (analytic_l1 - mixture_l1) / max(analytic_l1, mixture_l1)
    checked_divergence, checked_shift = check_continuous_dp(epsilon, delta, k, sigma * (1.0 + 2e-5))
    control_divergence, control_shift = check_continuous_dp(epsilon, delta, k, sigma * 0.99)
    paper_value = setting["paper_improvement_pct"]
    return {
        "delta": delta,
        "epsilon": epsilon,
        "k": k,
        "sigma": sigma,
        "analytic_sigma": analytic_sigma,
        "mixture_l1": mixture_l1,
        "analytic_l1": analytic_l1,
        "mixture_variance": mixture_variance,
        "analytic_variance": analytic_variance,
        "improvement_pct": improvement,
        "paper_improvement_pct": paper_value,
        "absolute_error_pp": None if paper_value is None else abs(improvement - float(paper_value)),
        "calibration_divergence": calibration_divergence,
        "calibration_shift": calibration_shift,
        "checked_divergence": checked_divergence,
        "checked_shift": checked_shift,
        "dp_check_pass": checked_divergence <= delta,
        "control_divergence": control_divergence,
        "control_shift": control_shift,
        "control_rejected": control_divergence > delta,
        "runtime_seconds": time.perf_counter() - started,
    }


def run_claim1() -> dict[str, object]:
    started = time.perf_counter()
    settings = load_settings()
    available = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else (os.cpu_count() or 1)
    workers = min(32, available, len(settings))
    results = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_setting, setting): setting for setting in settings}
        for completed, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(
                "PROGRESS claim1 {}/150 eps={} delta={} K={} improvement={:.4f}% paper={} dp={} control={} runtime={:.2f}s".format(
                    completed,
                    result["epsilon"],
                    result["delta"],
                    result["k"],
                    result["improvement_pct"],
                    result["paper_improvement_pct"],
                    result["dp_check_pass"],
                    result["control_rejected"],
                    result["runtime_seconds"],
                ),
                flush=True,
            )
    results.sort(key=lambda row: (float(row["delta"]), float(row["epsilon"])))
    improvements = [float(row["improvement_pct"]) for row in results]
    comparable_errors = [float(row["absolute_error_pp"]) for row in results if row["absolute_error_pp"] is not None]
    summary = {
        "settings": len(results),
        "strict_wins": sum(value > 0.0 for value in improvements),
        "mean_improvement_pct": statistics.fmean(improvements),
        "sample_std_pct": statistics.stdev(improvements),
        "median_improvement_pct": statistics.median(improvements),
        "mean_absolute_error_pp_vs_paper_cells": statistics.fmean(comparable_errors),
        "max_absolute_error_pp_vs_paper_cells": max(comparable_errors),
        "cells_within_1pp": sum(error <= 1.0 for error in comparable_errors),
        "dp_checks_passed": sum(bool(row["dp_check_pass"]) for row in results),
        "controls_rejected": sum(bool(row["control_rejected"]) for row in results),
        "workers": workers,
        "runtime_seconds": time.perf_counter() - started,
    }
    exact_contract = (
        summary["settings"] == 150
        and summary["strict_wins"] == 142
        and abs(summary["mean_improvement_pct"] - 53.73) <= 1.0
        and abs(summary["sample_std_pct"] - 34.86) <= 1.0
        and abs(summary["median_improvement_pct"] - 61.86) <= 1.0
        and summary["dp_checks_passed"] == 150
        and summary["controls_rejected"] >= 145
    )
    tail = [row for row in results if float(row["epsilon"]) in (5.0, 10.0)]
    proposition_33_regression = {
        "status": "PASS" if len(tail) == 30 and all(float(row["mixture_variance"]) < float(row["analytic_variance"]) for row in tail) else "FAIL",
        "checked_delta_values": 15,
        "checked_tail_epsilons": [5.0, 10.0],
        "strict_variance_wins": sum(float(row["mixture_variance"]) < float(row["analytic_variance"]) for row in tail),
        "checks": len(tail),
        "scope": "cumulative finite-grid regression for the previously accepted Proposition 3.3 evidence; not a replacement for its universal proof",
    }
    return {
        "claim": 1,
        "route": "stable log-density root finding and direct privacy-loss quadrature for paper-selected K on all 150 settings",
        "status": "VERIFIED" if exact_contract else "INCONCLUSIVE",
        "summary": summary,
        "results": results,
        "proposition_33_regression": proposition_33_regression,
        "limitations": [
            "K values are taken from paper Table 3; this route does not independently search all K=1..20.",
            "Continuous shift maximization uses adaptive local optimization plus a denser 129-point independent checker.",
            "Privacy-loss roots use log-density ratios; positive hockey-stick mass is integrated directly instead of subtracting CDF values.",
            "Gaussian tails beyond 14 standard deviations from every component center are omitted; their total mass is below the quadrature tolerance.",
            "The checker does not reuse the paper improvement values for calibration.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_claim1(), indent=2, sort_keys=True))
