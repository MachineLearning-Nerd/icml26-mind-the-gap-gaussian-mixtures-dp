# Claim 5 benchmark method

The verifier independently computes expected absolute loss for truncated Laplace, Tulap, and the pure-DP staircase mechanism on all 75 Table 2 cells with epsilon at least 2. It reconstructs each displayed mixture loss from Table 1 and compares the resulting relative improvement to Table 2.

Appendix D.6 says the winner among all named non-Gaussian benchmarks is always truncated Laplace or Tulap. Cactus and flipped Huber are therefore source-audited but not independently reimplemented; they cannot alter the source's selected comparator.

The scientific verdict does not depend on benchmark ranking alone: all 60 epsilon-at-least-3 mixture losses have rounding-robust fixed-set witnesses proving that the implied mixture violates the stated DP constraint. The comparison is therefore not at equal privacy.
