# Claim 1 Route C: reported-loss adversarial audit

For each Table 1 cell with `epsilon >= 2`, this route reconstructs the largest sigma compatible with the paper's two-decimal reported improvement and the K reported in Table 3. It then searches for a single measurable interval and allowed shift whose exact DP difference exceeds delta. The selected witness is recomputed independently with 80-decimal arithmetic.

Using the lower edge of the rounding interval maximizes sigma and is conservative for privacy: if that mechanism violates DP, every sigma compatible with the displayed loss does. Analytic Gaussian controls must pass at their calibrated sigma, while a 1% scale reduction must be rejected. The run executes on HF `cpu-upgrade` under the inherited fixed command and lock.

This is a falsification route for the paper's reported high-epsilon loss values under its stated `(epsilon,delta)`-DP assumption. It does not independently optimize all `K in {1,...,20}`.
