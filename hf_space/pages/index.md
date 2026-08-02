# Mind the Gap: current claim-by-claim verification

The live judged baseline is 4/10 at revision `efa0aed7e74a2b7977424d27b1d928da1116588d`. This candidate does not claim that score has changed.

The fixed verifier reproduces all 150 printed Table 1 entries, then checks the underlying privacy assumptions. It finds rounding-robust DP counterexamples for Claims 1, 3, and 5; the previously full-credit Claims 2 and 4 remain verified.

| Claim | Result | Decisive observed evidence |
|---|---|---|
| 1 | **FALSIFIED** | 73/75 audited high-ε cells violate `(ε,δ)`-DP |
| 2 | **VERIFIED** | Accepted Proposition 3.3 evidence preserved; 30/30 tail regressions pass |
| 3 | **FALSIFIED** | Table 4 contains 88.88%; all 30 tail mechanisms violate DP |
| 4 | **VERIFIED** | Symbolic zCDP residual 0; 1.1Δ control rejected |
| 5 | **FALSIFIED** | 60/60 ε≥3 comparisons lack equal privacy; staircase wins 72/75 |

Continue with [Current verification](#/current-verification), the [visibility matrix](#/visibility-matrix), the [release report](#/release-report), and the [red-team record](#/red-team). The [Historical rejected baseline](#/historical-index) is retained as evidence of the prior state.
