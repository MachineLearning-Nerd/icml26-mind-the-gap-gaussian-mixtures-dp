from __future__ import annotations

import math
import statistics

import mpmath
import numpy as np
from scipy.optimize import brentq

from claim1_continuous import load_settings
from mechanisms import MultiGaussian, analytic_gaussian_sigma


def sigma_from_improvement(epsilon: float, delta: float, k: int, improvement_pct: float) -> float:
    mechanism = MultiGaussian(epsilon, k)
    analytic_l1 = analytic_gaussian_sigma(epsilon, delta) * math.sqrt(2.0 / math.pi)
    if improvement_pct >= 0.0:
        target_l1 = analytic_l1 * (1.0 - improvement_pct / 100.0)
    else:
        target_l1 = analytic_l1 / (1.0 + improvement_pct / 100.0)
    lower = 1e-10
    upper = analytic_l1 * math.sqrt(math.pi / 2.0) * 2.0
    return brentq(lambda sigma: mechanism.l1_loss(sigma) - target_l1, lower, upper, xtol=1e-14, rtol=1e-14)


def fixed_set_difference(
    mechanism: MultiGaussian,
    sigma: float,
    shift: float,
    lower: float,
    upper: float,
) -> float:
    shifted_mass = mechanism.cdf(upper + shift, sigma)[0] - mechanism.cdf(lower + shift, sigma)[0]
    base_mass = mechanism.cdf(upper, sigma)[0] - mechanism.cdf(lower, sigma)[0]
    return float(shifted_mass - math.exp(mechanism.epsilon) * base_mass)


def find_witness(mechanism: MultiGaussian, sigma: float) -> tuple[float, float, float, float]:
    best = (-math.inf, 0.0, 0.0, 0.0)
    for shift in np.linspace(0.025, 0.975, 39):
        for center in mechanism.centers:
            shifted_center = float(center - shift)
            for radius_multiplier in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
                lower = shifted_center - radius_multiplier * sigma
                upper = shifted_center + radius_multiplier * sigma
                candidate = fixed_set_difference(mechanism, sigma, float(shift), lower, upper)
                best = max(best, (candidate, float(shift), lower, upper))
    return best


def mp_normal_cdf(value: mpmath.mpf) -> mpmath.mpf:
    return mpmath.erfc(-value / mpmath.sqrt(2)) / 2


def certified_difference(
    epsilon: float,
    k: int,
    sigma: float,
    shift: float,
    lower: float,
    upper: float,
) -> mpmath.mpf:
    with mpmath.workdps(80):
        mp_epsilon = mpmath.mpf(str(epsilon))
        mp_sigma = mpmath.mpf(str(sigma))
        weights = [mpmath.exp(-abs(index) * mp_epsilon) for index in range(-k, k + 1)]
        normalizer = sum(weights)

        def cdf(point: float) -> mpmath.mpf:
            mp_point = mpmath.mpf(str(point))
            return sum(
                weight * mp_normal_cdf((mp_point - index) / mp_sigma)
                for index, weight in zip(range(-k, k + 1), weights)
            ) / normalizer

        shifted_mass = cdf(upper + shift) - cdf(lower + shift)
        base_mass = cdf(upper) - cdf(lower)
        return shifted_mass - mpmath.exp(mp_epsilon) * base_mass


def analytic_gaussian_divergence(epsilon: float, sigma: float, shift: float = 1.0) -> float:
    first = shift / (2.0 * sigma) - epsilon * sigma / shift
    second = -shift / (2.0 * sigma) - epsilon * sigma / shift
    return 0.5 * math.erfc(-first / math.sqrt(2.0)) - math.exp(epsilon) * 0.5 * math.erfc(-second / math.sqrt(2.0))


def run_claim1() -> dict[str, object]:
    results = []
    for setting in load_settings():
        paper_value = setting["paper_improvement_pct"]
        epsilon = float(setting["epsilon"])
        if paper_value is None or epsilon < 2.0:
            continue
        delta = float(setting["delta"])
        k = int(setting["k"])
        reported = float(paper_value)
        conservative_improvement = reported - 0.005
        sigma = sigma_from_improvement(epsilon, delta, k, conservative_improvement)
        mechanism = MultiGaussian(epsilon, k)
        search_value, shift, lower, upper = find_witness(mechanism, sigma)
        checked = certified_difference(epsilon, k, sigma, shift, lower, upper)
        checked_float = float(checked)
        analytic_sigma = analytic_gaussian_sigma(epsilon, delta)
        results.append(
            {
                "epsilon": epsilon,
                "delta": delta,
                "k": k,
                "reported_improvement_pct": reported,
                "conservative_improvement_pct": conservative_improvement,
                "conservative_sigma": sigma,
                "mixture_variance": mechanism.variance(sigma),
                "analytic_variance": analytic_sigma * analytic_sigma,
                "witness_shift": shift,
                "witness_set": [lower, upper],
                "search_difference": search_value,
                "mpmath_80dps_difference": mpmath.nstr(checked, 50),
                "violation_margin": checked_float - delta,
                "violates_dp": checked_float > delta + 1e-10,
            }
        )

    analytic_controls = []
    for epsilon, delta in ((2.0, 1e-6), (5.0, 1e-3), (10.0, 0.25)):
        sigma = analytic_gaussian_sigma(epsilon, delta)
        calibrated = analytic_gaussian_divergence(epsilon, sigma)
        reduced = analytic_gaussian_divergence(epsilon, 0.99 * sigma)
        analytic_controls.append(
            {
                "epsilon": epsilon,
                "delta": delta,
                "calibrated_divergence": calibrated,
                "calibrated_passes": calibrated <= delta * (1.0 + 1e-8) + 1e-14,
                "negative_control": "reduce analytic Gaussian sigma by 1%",
                "negative_control_divergence": reduced,
                "negative_control_rejected": reduced > delta,
            }
        )

    violating = [row for row in results if row["violates_dp"]]
    margins = [float(row["violation_margin"]) for row in violating]
    controls_pass = all(row["calibrated_passes"] and row["negative_control_rejected"] for row in analytic_controls)
    falsified = bool(violating) and controls_pass
    tail = [row for row in results if float(row["epsilon"]) in (5.0, 10.0)]
    strict_variance_wins = sum(float(row["mixture_variance"]) < float(row["analytic_variance"]) for row in tail)
    proposition_33_regression = {
        "status": "PASS" if len(tail) == 30 and strict_variance_wins == 30 else "FAIL",
        "checked_delta_values": 15,
        "checked_tail_epsilons": [5.0, 10.0],
        "checks": len(tail),
        "strict_variance_wins": strict_variance_wins,
        "scope": "cumulative coverage check; the accepted Proposition 3.3 proof certificate is unchanged",
    }
    return {
        "claim": 1,
        "route": "rounding-robust reconstruction of paper-reported loss followed by fixed-measurable-set DP witnesses",
        "status": "FALSIFIED" if falsified else "BLOCKED",
        "exact_interpretation": (
            "Table 1 reports losses of (epsilon,delta)-DP multi-Gaussian mechanisms with eta=0.01 and K from Table 3. "
            "For each rounded high-epsilon entry, the largest sigma compatible with rounding is reconstructed. A single "
            "measurable set and shift in [0,1] falsifies DP whenever its hockey-stick difference exceeds delta."
        ),
        "summary": {
            "audited_high_epsilon_cells": len(results),
            "rounding_robust_dp_violations": len(violating),
            "smallest_violation_margin": min(margins) if margins else None,
            "median_violation_margin": statistics.median(margins) if margins else None,
            "controls_passed": controls_pass,
        },
        "results": results,
        "independent_controls": analytic_controls,
        "proposition_33_regression": proposition_33_regression,
        "limitations": [
            "This route audits epsilon>=2, where Routes A/B showed systematic disagreement; it does not recalibrate all K values.",
            "A violation is accepted only for the largest sigma compatible with the table's two-decimal rounding, making it robust to rounding.",
            "Each certificate uses one fixed measurable interval, not a numerical approximation to the supremum over events.",
            "Candidate intervals are selected in float64, then independently evaluated at 80 decimal digits.",
        ],
    }
