# Baseline method

`repro/run_all.py` reads the 150 source-table cells, verifies the exact parameter grid, recomputes the published aggregates, and mutates one positive cell as a negative control. It exits nonzero if the source table or control does not satisfy the contract.

This is deliberately labeled a source audit. A child experiment must generate losses from the paper's Algorithm 1 and analytic Gaussian calibration rather than reuse these published improvements.

HF runs use the pinned CPU-only image `ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie` because the default Python image does not include `uv`.
