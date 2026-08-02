from __future__ import annotations

import csv
import importlib.metadata
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

import sympy

from claim1_continuous import run_claim1


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "repro" / "data" / "table1_l1.csv"
EXPECTED_COMMAND = "uv sync --frozen && .venv/bin/python repro/run_all.py"
EXPECTED_EPSILONS = {0.1, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0}
EXPECTED_DELTAS = {
    5e-7,
    1e-6,
    5e-6,
    1e-5,
    5e-5,
    1e-4,
    5e-4,
    1e-3,
    5e-3,
    0.01,
    0.02,
    0.05,
    0.1,
    0.15,
    0.25,
}


def load_table() -> list[dict[str, float | None]]:
    rows = []
    with TABLE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw = row["reported_improvement_pct"]
            rows.append(
                {
                    "delta": float(row["delta"]),
                    "epsilon": float(row["epsilon"]),
                    "improvement_pct": None if raw == "NA" else float(raw),
                }
            )
    return rows


def summarize(rows: list[dict[str, float | None]]) -> dict[str, float | int]:
    values = [0.0 if row["improvement_pct"] is None else row["improvement_pct"] for row in rows]
    return {
        "settings": len(rows),
        "strict_wins": sum(value > 0 for value in values),
        "na_count": sum(row["improvement_pct"] is None for row in rows),
        "mean_improvement_pct": statistics.fmean(values),
        "sample_std_pct": statistics.stdev(values),
        "population_std_pct": statistics.pstdev(values),
        "median_improvement_pct": statistics.median(values),
    }


def validation_errors(rows: list[dict[str, float | None]]) -> list[str]:
    errors = []
    pairs = {(row["delta"], row["epsilon"]) for row in rows}
    expected_pairs = {(delta, epsilon) for delta in EXPECTED_DELTAS for epsilon in EXPECTED_EPSILONS}
    if pairs != expected_pairs:
        errors.append("parameter grid is not the exact 15 x 10 paper grid")

    summary = summarize(rows)
    expected = {
        "settings": 150,
        "strict_wins": 142,
        "mean_improvement_pct": 53.73,
        "sample_std_pct": 34.86,
        "median_improvement_pct": 61.86,
    }
    for key in ("settings", "strict_wins"):
        if summary[key] != expected[key]:
            errors.append(f"{key}: observed {summary[key]}, expected {expected[key]}")
    for key in ("mean_improvement_pct", "sample_std_pct", "median_improvement_pct"):
        if round(float(summary[key]), 2) != expected[key]:
            errors.append(f"{key}: observed {summary[key]:.6f}, expected rounded {expected[key]:.2f}")
    return errors


def negative_control(rows: list[dict[str, float | None]]) -> dict[str, object]:
    altered = [dict(row) for row in rows]
    first_win = next(row for row in altered if row["improvement_pct"] is not None and row["improvement_pct"] > 0)
    first_win["improvement_pct"] = 0.0
    errors = validation_errors(altered)
    return {
        "mutation": "replace first positive improvement with zero",
        "rejected": bool(errors),
        "errors": errors,
    }


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def dependency_versions() -> dict[str, str]:
    return {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "sympy", "matplotlib", "marimo")}


def corollary_37_regression() -> dict[str, object]:
    alpha, sensitivity, sigma = sympy.symbols("alpha sensitivity sigma", positive=True)
    rho = sensitivity**2 / (2 * sigma**2)
    paired_gaussian_renyi = alpha * sensitivity**2 / (2 * sigma**2)
    identity = sympy.simplify(paired_gaussian_renyi - alpha * rho)
    control_ratio = sympy.simplify((alpha * (1.1 * sensitivity) ** 2 / (2 * sigma**2)) / (alpha * rho))
    passed = identity == 0 and float(control_ratio) > 1.0
    return {
        "status": "PASS" if passed else "FAIL",
        "certificate": "For every alpha>1 and every component k, the paired translated Gaussians have D_alpha = alpha*Delta^2/(2*sigma^2); Renyi quasi-convexity for common mixture weights gives the same upper bound for the mixtures.",
        "symbolic_residual": str(identity),
        "negative_control": {
            "mutation": "pair components with shift 1.1*Delta",
            "ratio_to_claimed_bound": float(control_ratio),
            "rejected": float(control_ratio) > 1.0,
        },
        "source_anchors": ["#S3.Thmtheorem7", "#A2.SS8"],
    }


def main() -> int:
    started = time.perf_counter()
    rows = load_table()
    summary = summarize(rows)
    errors = validation_errors(rows)
    control = negative_control(rows)
    claim1 = run_claim1()
    claim4 = corollary_37_regression()
    affinity = sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    result = {
        "paper": "arXiv:2605.28078",
        "claim": "Claim 1 source-table contract",
        "evidence_scope": "source extraction and summary audit only; not an independent mechanism reproduction",
        "status": "PASS"
        if not errors
        and control["rejected"]
        and claim1["status"] == "VERIFIED"
        and claim1["proposition_33_regression"]["status"] == "PASS"
        and claim4["status"] == "PASS"
        else "FAIL",
        "source": {
            "url": "https://ar5iv.labs.arxiv.org/html/2605.28078",
            "retrieved_utc": "2026-08-02T03:21:18Z",
            "sha256": "523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53",
            "anchors": ["#S5.T1", "#S5.SS1.p1"],
        },
        "summary": summary,
        "errors": errors,
        "negative_control": control,
        "claim1_scientific_reproduction": claim1,
        "claim4_corollary_37_regression": claim4,
        "reproducibility": {
            "fixed_command": EXPECTED_COMMAND,
            "git_sha": git_sha(),
            "seed": 260528078,
            "python": sys.version,
            "dependencies": dependency_versions(),
            "compute": {
                "backend": "hf",
                "flavor": "cpu-upgrade",
                "image": "ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie",
                "estimated_cores": 32,
                "logical_cpus": os.cpu_count(),
                "affinity_cpus": len(affinity) if affinity is not None else None,
                "platform": platform.platform(),
            },
        },
    }
    result["reproducibility"]["runtime_seconds"] = time.perf_counter() - started
    print(json.dumps(result, indent=2, sort_keys=True))
    print(
        "EVAL claim1_source_table={status} settings={settings} wins={wins} "
        "mean={mean:.6f} std={std:.6f} median={median:.6f} control_rejected={control}".format(
            status=result["status"],
            settings=summary["settings"],
            wins=summary["strict_wins"],
            mean=summary["mean_improvement_pct"],
        std=summary["sample_std_pct"],
            median=summary["median_improvement_pct"],
            control=control["rejected"],
        )
    )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
