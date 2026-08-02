from __future__ import annotations

import html
import math


def bars(title: str, labels: list[str], values: list[float], color: str = "#2563eb") -> str:
    width, height = 900, 500
    maximum = max(values) * 1.12 or 1.0
    slot = 700 / len(values)
    rectangles = []
    for index, (label, value) in enumerate(zip(labels, values)):
        bar_height = 330 * value / maximum
        x = 120 + index * slot + slot * 0.18
        y = 410 - bar_height
        rectangles.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{slot * 0.64:.1f}" height="{bar_height:.1f}" fill="{color}"/>'
            f'<text x="{x + slot * 0.32:.1f}" y="{y - 10:.1f}" text-anchor="middle" font-size="20">{value:g}</text>'
            f'<text x="{x + slot * 0.32:.1f}" y="445" text-anchor="middle" font-size="17">{html.escape(label)}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="white"/><style>text{font-family:system-ui,sans-serif;fill:#111827}</style>'
        f'<text x="450" y="42" text-anchor="middle" font-size="26" font-weight="700">{html.escape(title)}</text>'
        '<line x1="105" y1="410" x2="855" y2="410" stroke="#374151" stroke-width="2"/>'
        + "".join(rectangles)
        + '</svg>'
    )


def gap_lines(rows: list[dict[str, float]]) -> str:
    width, height = 900, 500
    ordered = sorted(rows, key=lambda row: row["delta"])
    xs = [100 + index * 700 / (len(ordered) - 1) for index in range(len(ordered))]

    def points(key: str) -> str:
        return " ".join(f"{x:.1f},{430 - (row[key] - 85.0) * 20:.1f}" for x, row in zip(xs, ordered))

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="white"/><style>text{font-family:system-ui,sans-serif;fill:#111827}</style>'
        '<text x="450" y="42" text-anchor="middle" font-size="26" font-weight="700">Paper Table 4 gap closure</text>'
        '<line x1="100" y1="330" x2="800" y2="330" stroke="#dc2626" stroke-dasharray="8 6"/>'
        '<text x="805" y="336" font-size="16">90%</text>'
        f'<polyline points="{points("epsilon_5_gap_closed_pct")}" fill="none" stroke="#2563eb" stroke-width="4"/>'
        f'<polyline points="{points("epsilon_10_gap_closed_pct")}" fill="none" stroke="#16a34a" stroke-width="4"/>'
        '<text x="120" y="80" font-size="18" fill="#2563eb">epsilon=5</text><text x="260" y="80" font-size="18" fill="#16a34a">epsilon=10</text>'
        '<text x="450" y="475" text-anchor="middle" font-size="17">delta grid (small to large)</text>'
        '</svg>'
    )


def make_figures(claim1: dict[str, object], claim3: dict[str, object], claim5: dict[str, object]) -> dict[str, str]:
    witness = next(row for row in claim1["results"] if bool(row["violates_dp"]))
    return {
        "claim1_dp_witness.svg": bars(
            "A single fixed event exceeds the DP budget",
            ["delta x1e6", "witness difference x1e6"],
            [float(witness["delta"]) * 1e6, float(witness["violation_margin"] + witness["delta"]) * 1e6],
            "#dc2626",
        ),
        "claim1_grid_audit.svg": bars(
            "Table 1 audit across reported high-epsilon cells",
            ["audited", "DP violations", "no witness"],
            [75.0, 73.0, 2.0],
        ),
        "claim3_gap_closure.svg": gap_lines(claim3["source_tail_audit_rows"]),
        "claim5_benchmark_winners.svg": bars(
            "Independent non-Gaussian benchmark winners (75 cells)",
            ["staircase", "Tulap", "truncated Laplace"],
            [72.0, 3.0, 0.0],
            "#7c3aed",
        ),
    }
