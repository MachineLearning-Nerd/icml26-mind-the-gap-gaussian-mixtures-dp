from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import ndtr


SQRT_2PI = math.sqrt(2.0 * math.pi)


def analytic_gaussian_sigma(epsilon: float, delta: float, sensitivity: float = 1.0) -> float:
    def case_a(s: float) -> float:
        return float(ndtr(math.sqrt(epsilon * s)) - math.exp(epsilon) * ndtr(-math.sqrt(epsilon * (s + 2.0))))

    def case_b(s: float) -> float:
        return float(ndtr(-math.sqrt(epsilon * s)) - math.exp(epsilon) * ndtr(-math.sqrt(epsilon * (s + 2.0))))

    threshold = case_a(0.0)
    if math.isclose(delta, threshold, rel_tol=0.0, abs_tol=1e-15):
        alpha = 1.0
    elif delta > threshold:
        upper = 1.0
        while case_a(upper) < delta:
            upper *= 2.0
        solution = brentq(lambda s: case_a(s) - delta, 0.0, upper, xtol=1e-13, rtol=1e-13)
        alpha = math.sqrt(1.0 + solution / 2.0) - math.sqrt(solution / 2.0)
    else:
        upper = 1.0
        while case_b(upper) > delta:
            upper *= 2.0
        solution = brentq(lambda s: case_b(s) - delta, 0.0, upper, xtol=1e-13, rtol=1e-13)
        alpha = math.sqrt(1.0 + solution / 2.0) + math.sqrt(solution / 2.0)
    return alpha * sensitivity / math.sqrt(2.0 * epsilon)


@dataclass(frozen=True)
class MultiGaussian:
    epsilon: float
    k: int
    sensitivity: float = 1.0

    def __post_init__(self) -> None:
        indices = np.arange(-self.k, self.k + 1, dtype=float)
        weights = np.exp(-np.abs(indices) * self.epsilon)
        object.__setattr__(self, "centers", indices * self.sensitivity)
        object.__setattr__(self, "weights", weights / weights.sum())

    def density(self, x: np.ndarray | float, sigma: float) -> np.ndarray:
        points = np.atleast_1d(np.asarray(x, dtype=float))
        z = (points[:, None] - self.centers[None, :]) / sigma
        values = np.exp(-0.5 * z * z) @ self.weights / (SQRT_2PI * sigma)
        return values

    def cdf(self, x: np.ndarray | float, sigma: float) -> np.ndarray:
        points = np.atleast_1d(np.asarray(x, dtype=float))
        return ndtr((points[:, None] - self.centers[None, :]) / sigma) @ self.weights

    def l1_loss(self, sigma: float) -> float:
        absolute_centers = np.abs(self.centers)
        component = (
            sigma * math.sqrt(2.0 / math.pi) * np.exp(-0.5 * (absolute_centers / sigma) ** 2)
            + absolute_centers * (1.0 - 2.0 * ndtr(-absolute_centers / sigma))
        )
        return float(component @ self.weights)

    def variance(self, sigma: float) -> float:
        return float((sigma * sigma + self.centers * self.centers) @ self.weights)


def hockey_stick_divergence(
    mechanism: MultiGaussian,
    sigma: float,
    shift: float,
    *,
    hotspot_points: int,
    global_points: int,
) -> float:
    if shift <= 0.0:
        return 0.0
    tail = 10.0
    hotspots = np.concatenate((mechanism.centers, mechanism.centers - shift))
    offsets = np.linspace(-tail, tail, hotspot_points) * sigma
    local = (hotspots[:, None] + offsets[None, :]).ravel()
    lower = float(hotspots.min() - tail * sigma)
    upper = float(hotspots.max() + tail * sigma)
    points = np.unique(np.concatenate((local, np.linspace(lower, upper, global_points))))
    exp_epsilon = math.exp(mechanism.epsilon)

    def values(x: np.ndarray | float) -> np.ndarray:
        array = np.atleast_1d(np.asarray(x, dtype=float))
        return mechanism.density(array + shift, sigma) - exp_epsilon * mechanism.density(array, sigma)

    signs = values(points)
    roots = []
    for index in np.flatnonzero(signs[:-1] * signs[1:] < 0.0):
        left = float(points[index])
        right = float(points[index + 1])
        left_value = float(values(left)[0])
        right_value = float(values(right)[0])
        if left_value == 0.0:
            roots.append(left)
        elif right_value == 0.0:
            roots.append(right)
        elif left_value * right_value < 0.0:
            roots.append(brentq(lambda x: float(values(x)[0]), left, right, xtol=1e-12, rtol=1e-12))
    if roots:
        roots = list(np.unique(np.round(roots, 13)))

    boundaries = [-math.inf, *roots, math.inf]
    divergence = 0.0
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        if math.isinf(left) and math.isinf(right):
            probe = 0.0
        elif math.isinf(left):
            probe = right - max(2.0 * sigma, 1.0)
        elif math.isinf(right):
            probe = left + max(2.0 * sigma, 1.0)
        else:
            probe = 0.5 * (left + right)
        if values(probe)[0] <= 0.0:
            continue
        shifted_mass = mechanism.cdf(right + shift, sigma)[0] - mechanism.cdf(left + shift, sigma)[0]
        base_mass = mechanism.cdf(right, sigma)[0] - mechanism.cdf(left, sigma)[0]
        divergence += shifted_mass - exp_epsilon * base_mass
    return max(float(divergence), 0.0)


def maximum_hockey_stick(
    mechanism: MultiGaussian,
    sigma: float,
    *,
    shift_points: int,
    hotspot_points: int,
    global_points: int,
) -> tuple[float, float]:
    shifts = np.linspace(0.0, mechanism.sensitivity, shift_points)

    def divergence(shift: float) -> float:
        return hockey_stick_divergence(
            mechanism,
            sigma,
            shift,
            hotspot_points=hotspot_points,
            global_points=global_points,
        )

    values = np.array([divergence(float(shift)) for shift in shifts])
    candidates = [(float(values[-1]), float(shifts[-1]))]
    for index in range(1, len(shifts) - 1):
        if values[index] >= values[index - 1] and values[index] >= values[index + 1]:
            result = minimize_scalar(
                lambda shift: -divergence(float(shift)),
                bounds=(float(shifts[index - 1]), float(shifts[index + 1])),
                method="bounded",
                options={"xatol": 2e-6},
            )
            candidates.append((-float(result.fun), float(result.x)))
    return max(candidates)


def calibrate_continuous_dp(
    epsilon: float,
    delta: float,
    k: int,
    *,
    eta: float = 0.01,
) -> tuple[float, float, float]:
    mechanism = MultiGaussian(epsilon, k)
    budget = (1.0 - eta) * delta
    upper = analytic_gaussian_sigma(epsilon, budget)

    def worst(sigma: float) -> tuple[float, float]:
        return maximum_hockey_stick(
            mechanism,
            sigma,
            shift_points=17,
            hotspot_points=17,
            global_points=257,
        )

    upper_value, upper_shift = worst(upper)
    while upper_value > budget:
        upper *= 2.0
        upper_value, upper_shift = worst(upper)
    lower = max(upper / 64.0, 1e-8)
    lower_value, _ = worst(lower)
    while lower_value <= budget and lower > 1e-12:
        lower *= 0.5
        lower_value, _ = worst(lower)

    for _ in range(28):
        midpoint = 0.5 * (lower + upper)
        value, shift = worst(midpoint)
        if value <= budget:
            upper = midpoint
            upper_value = value
            upper_shift = shift
        else:
            lower = midpoint
    return upper, upper_value, upper_shift


def check_continuous_dp(
    epsilon: float,
    delta: float,
    k: int,
    sigma: float,
) -> tuple[float, float]:
    mechanism = MultiGaussian(epsilon, k)
    return maximum_hockey_stick(
        mechanism,
        sigma,
        shift_points=129,
        hotspot_points=33,
        global_points=1025,
    )
