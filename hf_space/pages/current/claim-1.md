# Claim 1 — FALSIFIED

**Exact claim.** Across the complete 15×10 Table 1 grid, the proposed `(ε,δ)`-DP mixtures beat analytic Gaussian in 142/150 settings, with mean 53.73%, sample SD 34.86%, and median 61.86% improvement.

**Source and assumptions.** Section 5 Table 1 (`#S5.T1`) and its following paragraph; Δ=1, η=0.01, K selected from 1…20, δ in the 15 printed rows, ε in the 10 printed columns. Source retrieved 2026-08-02 from `https://ar5iv.labs.arxiv.org/html/2605.28078`, SHA-256 `523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53`.

**Observed.** The source aggregate reproduces exactly: 150 settings, 142 strict wins, mean 53.729%, sample SD 34.856327%, median 61.86%. That does not validate privacy. On all 75 ε≥2 entries, we reconstruct the largest σ compatible with rounding and search one neighboring shift in `[0,1]` and one fixed interval. Independent 80-decimal evaluation finds 73 rounding-robust violations; the smallest margin is 0.0670362153556447.

The decisive witness is ε=3, δ=5×10⁻⁷, K=14, σ=0.23811581113482513, shift 0.75, interval `[-0.8690579055674126,-0.6309420944325874]`. Its hockey-stick difference is `0.067036715355644703485854324343982978957575295471098`, exceeding δ.

![Witness](../../evidence/current/claim1_dp_witness.svg)

**Checker and control.** Candidate intervals use float64; final probabilities use independent `mpmath` at 80 digits. Three calibrated analytic-Gaussian controls pass; a 1% σ reduction is rejected in every case. Code: [audit](../../code/current/repro/claim1_reported_loss_audit.py), [mechanisms](../../code/current/repro/mechanisms.py). Raw: [claim JSON](../../evidence/current/claim1_scientific_reproduction.json), [complete JSON](../../evidence/current/cumulative_run.json).

**Limits.** The DP audit targets ε≥2, where two prior independent calibration routes disagreed systematically with the paper. A single valid assumption-satisfying counterexample falsifies the exact claim; the audit does not assert that every possible Gaussian mixture fails.
