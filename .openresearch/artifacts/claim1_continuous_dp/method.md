# Claim 1 Route A: continuous-DP selected-K recalibration

For every Table 1 `(epsilon, delta)` setting, this route uses the K reported in paper Table 3, independently recalibrates sigma, and recomputes expected absolute loss. Calibration directly maximizes hockey-stick divergence over shifts in `[0, Delta]`; it does not use the paper's reported improvement as an input.

The independent checker uses a denser 129-shift scan and finer density-root bracketing. A 1% smaller sigma is the negative control and must violate the DP budget. All 150 settings execute on HF `cpu-upgrade` under the inherited fixed command and lock.

This route is not sufficient by itself to prove that the reported K minimizes loss over all K in `{1,...,20}`. A later route must perform the complete K search.
