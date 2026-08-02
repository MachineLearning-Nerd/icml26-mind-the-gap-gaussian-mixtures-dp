# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_28c02e16af00", "created_at": "2026-07-31T03:09:11+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Across 150 tested parameter settings in Table 1, multimodal (mixture-of-Gaussians) mechanisms achieve lower expected l1 noise loss than the analytic Gaussian mechanism in 142 of 150 cases, with mean reduction of 53.73% (std 34.86%) and median reduction of 61.86% (Section 5, Table 1).
2. Proposition 3.3 proves that for any delta in (0, 1/2) there exists an epsilon_0 such that the multimodal Gaussian mechanism has strictly lower l2 loss (variance) than the analytic Gaussian mechanism for all epsilon >= epsilon_0 (Section 3, Proposition 3.3).
3. In the low-privacy regime (epsilon >= 1), the proposed mixture mechanisms close up to 99% of the optimality gap between the analytic Gaussian mechanism and the theoretical lower bound, with l1-loss improvements of 79-99% depending on delta (Section 5).
4. Corollary 3.7 shows the multimodal Gaussian mechanisms satisfy the same zero-concentrated differential privacy guarantee (rho = Delta^2 / 2*sigma^2) as the standard Gaussian mechanism, preserving standard composition properties (Section 3, Corollary 3.7).
5. Table 2 compares the mixture mechanisms against truncated Laplace, Tulap, staircase, cactus, and flipped Huber mechanisms, finding the Gaussian mixtures competitive for epsilon >= 1 but inferior to non-Gaussian mechanisms for epsilon < 1 (Section 5, Table 2).
