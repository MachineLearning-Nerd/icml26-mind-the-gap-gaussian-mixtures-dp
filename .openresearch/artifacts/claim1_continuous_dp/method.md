# Claim 1 Route B: stable privacy-loss quadrature

For every Table 1 `(epsilon, delta)` setting, this route uses the K reported in paper Table 3, independently recalibrates sigma, and recomputes expected absolute loss. Privacy-loss roots are found from log-density ratios. Adaptive quadrature then integrates `p(x+s)-exp(epsilon)p(x)` directly on every positive interval instead of subtracting nearly equal CDF values. Calibration maximizes this hockey-stick divergence over shifts in `[0, Delta]`; it does not use the paper's reported improvement as an input.

The independent checker uses a denser 129-shift scan and finer log-ratio root bracketing. A 1% smaller sigma is the negative control and must violate the DP budget. All 150 settings execute on HF `cpu-upgrade` under the inherited fixed command and lock.

This route is not sufficient by itself to prove that the reported K minimizes loss over all K in `{1,...,20}`. A later route must perform the complete K search.
