# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_eeeb3ebbb011", "created_at": "2026-07-31T03:09:12+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
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
```
