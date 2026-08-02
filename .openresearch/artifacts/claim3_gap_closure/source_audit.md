# Claim 3 source audit

The imported judge wording conflates two paper quantities. Table 1 reports direct l1-loss reduction against the analytic Gaussian. Appendix D.3/Table 4 reports the fraction of the Selvi et al. optimality gap closed.

The exact Appendix D.3 statement is: mean gap closure 67.67% (sample sd 34.78), median 85.47%; more than 90% for epsilon=5 at any delta>0; reaching 99.72% for epsilon=10. Table 4 itself contains 88.88% at epsilon=5, delta=0.25, an internal counterexample to the universal epsilon=5 sentence.

Route C also proves that all 30 epsilon=5/10 displayed losses imply mechanisms violating the stated approximate-DP assumption, even after accounting conservatively for two-decimal rounding. Thus the proposed DP mechanisms do not attain the reported gap closures.
