# Claim 1 source audit

- URL: https://ar5iv.labs.arxiv.org/html/2605.28078
- Retrieved with explicit User-Agent: 2026-08-02T03:21:18Z
- SHA-256: `523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53`
- Section anchor: `#S5.SS1`
- Table anchor: `#S5.T1`
- Assumptions: scalar additive noise; sensitivity Delta > 0 (normalized to 1); epsilon > 0; delta in (0,1); eta=0.01; K searched over integers 1 through 20.
- Quantifiers: the empirical claim covers the complete Cartesian product of 15 delta values and 10 epsilon values, not only epsilon >= 1.
- Loss: expected absolute scalar noise, E|Z|.
- Improvement: `100 * (a - m) / max(a, m)`, where `a` is analytic-Gaussian loss and `m` is the best multi-Gaussian loss.

This baseline only checks transcription and arithmetic. Independent recalibration of all mechanisms is required before a scientific VERIFIED verdict.
