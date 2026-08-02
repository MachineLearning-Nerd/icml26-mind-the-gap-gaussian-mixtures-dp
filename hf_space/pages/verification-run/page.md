# Verification run


---
<!-- trackio-cell
{"type": "code", "id": "cell_a368ba638ba7", "created_at": "2026-07-31T03:09:16+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 2.483}
-->
````bash
$ .venv/bin/python repro/src/verify.py
````

exit 0 · 2.5s


````python title=verify.py
"""
verify.py - verify the anchored claims for "Mind the Gap: Mixtures of Gaussians in Approximate
Differential Privacy" (RdBsmhb9U7, arXiv 2605.28078).

  C0/[0] l1-loss reduction over the analytic Gaussian (low-privacy eps>=1, Table 1).
  C1/[1] Proposition 3.3: exists eps_0 s.t. mixture variance < analytic-Gaussian variance for eps>=eps_0.
  C2/[2] low-privacy: the l1 reduction grows with eps and is large (closing the AG->optimal gap).
  C3/[3] Corollary 3.7: rho-zCDP, rho = Delta^2/(2 sigma^2)  (Renyi quasi-convexity; exact).
  C4/[4] Table 2 regime split: helps eps>=1, not eps<1.

numpy/scipy only; Delta=1.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import core as C

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT, exist_ok=True)
verdict = {"paper": "RdBsmhb9U7", "arxiv": "2605.28078", "checks": {}}

r = C.claim0_l1_reduction()
verdict["checks"]["C0_l1_reduction"] = {
    "status": "PASS" if r["passed"] else "FAIL",
    "anchor": "[0]: mixture E|noise| (l1) < analytic Gaussian, most settings, ~50% reduction (Table 1)",
    "precision": f"wins {r['wins_over_AG']}, mean reduction {r['mean_reduction_pct']:.1f}%, "
                 f"median {r['median_reduction_pct']:.1f}% (low-privacy eps>=1)"}

r = C.prop33_l2()
verdict["checks"]["C1_prop33_l2"] = {
    "status": "PASS" if r["passed"] else "FAIL",
    "anchor": "Proposition 3.3 / [1]: exists eps_0 s.t. mixture l2 (variance) < analytic-Gaussian for eps>=eps_0",
    "precision": f"mixture variance < AG variance for all eps in a tail regime: {r['tail_regime_all_better']}"}

r = C.claim2_optimality_gap()
verdict["checks"]["C2_optimality_gap"] = {
    "status": "PASS" if r["passed"] else "FAIL",
    "anchor": "[2]: low-privacy, mixture closes most of the (AG -> optimal-Gaussian) gap",
    "precision": f"l1 reduction % by eps: {r['reduction_pct_by_eps']}"}

r = C.cor37_zcdp()
verdict["checks"]["C3_cor37_zcdp"] = {
    "status": "PASS" if r["passed"] else "FAIL",
    "anchor": "Corollary 3.7 / [3]: rho-zCDP with rho = Delta^2/(2 sigma^2)",
    "precision": f"D_alpha(mixture) <= alpha*rho for all alpha>1 (worst ratio {r['worst_ratio_renyi_over_alpha_rho']:.3f} <= 1); "
                 f"rho={r['rho']:.3f}"}

r = C.claim4_comparison()
verdict["checks"]["C4_regime_split"] = {
    "status": "PASS" if r["passed"] else "FAIL",
    "anchor": "[4] Table 2: Gaussian mixture helps in low-privacy (eps>=1), not high-privacy (eps<1)",
    "precision": f"mean reduction eps<1: {r['mean_reduction_eps_lt_1_pct']}%, eps>=1.5: {r['mean_reduction_eps_ge_1p5_pct']}%"}

verdict["n_claims_passed"] = sum(1 for v in verdict["checks"].values() if v["status"] == "PASS")
verdict["n_claims_total"] = 5
verdict["all_passed"] = all(v["status"] == "PASS" for v in verdict["checks"].values())
with open(os.path.join(OUT, "verdict.json"), "w") as fh:
    json.dump(verdict, fh, indent=2)
print(json.dumps(verdict, indent=2))
print("\nSUMMARY: claims {n}/{t} passed, all_passed={a}".format(
    n=verdict["n_claims_passed"], t=verdict["n_claims_total"], a=verdict["all_passed"]))

````


````output
{
  "paper": "RdBsmhb9U7",
  "arxiv": "2605.28078",
  "checks": {
    "C0_l1_reduction": {
      "status": "PASS",
      "anchor": "[0]: mixture E|noise| (l1) < analytic Gaussian, most settings, ~50% reduction (Table 1)",
      "precision": "wins 24/24, mean reduction 40.2%, median 44.8% (low-privacy eps>=1)"
    },
    "C1_prop33_l2": {
      "status": "PASS",
      "anchor": "Proposition 3.3 / [1]: exists eps_0 s.t. mixture l2 (variance) < analytic-Gaussian for eps>=eps_0",
      "precision": "mixture variance < AG variance for all eps in a tail regime: True"
    },
    "C2_optimality_gap": {
      "status": "PASS",
      "anchor": "[2]: low-privacy, mixture closes most of the (AG -> optimal-Gaussian) gap",
      "precision": "l1 reduction % by eps: [np.float64(2.2), np.float64(8.1), np.float64(16.4), np.float64(73.6), np.float64(73.0), np.float64(68.0)]"
    },
    "C3_cor37_zcdp": {
      "status": "PASS",
      "anchor": "Corollary 3.7 / [3]: rho-zCDP with rho = Delta^2/(2 sigma^2)",
      "precision": "D_alpha(mixture) <= alpha*rho for all alpha>1 (worst ratio 0.937 <= 1); rho=0.500"
    },
    "C4_regime_split": {
      "status": "PASS",
      "anchor": "[4] Table 2: Gaussian mixture helps in low-privacy (eps>=1), not high-privacy (eps<1)",
      "precision": "mean reduction eps<1: -0.0%, eps>=1.5: 42.78%"
    }
  },
  "n_claims_passed": 5,
  "n_claims_total": 5,
  "all_passed": true
}

SUMMARY: claims 5/5 passed, all_passed=True

````
