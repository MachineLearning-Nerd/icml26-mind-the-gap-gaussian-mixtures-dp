# Claim 4 — VERIFIED

**Exact claim.** Corollary 3.7 (`#S3.Thmtheorem7`, proof `#A2.SS8`) states ρ-zCDP with `ρ=Δ²/(2σ²)` for the common-weight translated Gaussian mixture, preserving zCDP composition.

For every α>1, paired components have `Dα=αΔ²/(2σ²)`. Rényi quasi-convexity for identical mixture weights gives the same bound for the mixtures. SymPy independently simplifies the difference from `αρ` to exactly `0`.

The negative control pairs components at `1.1Δ`; its ratio to the claimed bound is 1.21 and is rejected. Raw certificate: [claim JSON](../../evidence/current/claim4_corollary_37_regression.json). Executable checker: [run_all.py](../../code/current/repro/run_all.py). This preserves and strengthens the previously full-credit evidence.

**Limit.** The certificate applies to the corollary's identical-weight paired-component construction. Unequal-weight mixtures are outside the stated result and are not tested.
