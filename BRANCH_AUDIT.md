# Branch audit

## Final public branch state

| Property | Final state |
| --- | --- |
| Canonical repository | MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp |
| Canonical branch | main |
| Public experiment branches | none |
| Legacy experiment prefix | orx/ |
| History policy | retired branch pointers are represented by reachable rewritten history |
| Commit identity | MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com> |

The former experiment names were temporary research labels, not public
interfaces. Their purposes and outcomes are recorded below. The historical
SHAs predate identity normalization; corresponding rewritten commits remain
represented in main.

| Former branch | Historical tip | Purpose and outcome | Disposition |
| --- | --- | --- | --- |
| orx/claim-1-continuous-dp-selected-k-recalibration | 3dfca2ebf687c3188b5eb25bb55d5dfc425b9446 | Continuous DP audit for selected K values and reported mixture losses. | Retire pointer; retain history |
| orx/claim-1-reference-cap-adversarial-audit | ba6035edc1659e31b22f177dd33cb9c10049ae6e | Reference-cap and rounding-robust fixed-event audit for Claim 1. | Retire pointer; retain history |
| orx/claim-1-stable-privacy-loss-quadrature | 82de82c3213d57abcc88f20ad829b6951904a37e | Stable privacy-loss quadrature and high-precision witness validation. | Retire pointer; retain history |
| orx/claim-3-exact-gap-closure-audit | 90456bb936d938190d2fec80b21611424f448f6e | Audit the exact Table 4 gap-closure quantifier and reported values. | Retire pointer; retain history |
| orx/claim-5-non-gaussian-benchmark-audit | 4191fb93fa6b74bf18485ac4c244af6692c89df2 | Independent truncated-Laplace, Tulap, and staircase benchmark checks. | Retire pointer; retain history |
| orx/cumulative-release-evidence-suite | 1be2569534197318cd5a36847b8eb786c5cfc52a | Combine claim checkers, negative controls, and cumulative evidence. | Retire pointer; retain history |
| orx/evaluator-visible-release-candidate | bfa49f476c523a944c121c8d81457912b0363ec1 | Assemble evaluator-visible claim pages and raw evidence paths. | Retire pointer; retain history |
| orx/final-publication-artifact-and-release-gates | cbb2dd2e7dc5778753797d143b4d884ccb3d24ce | Prepare publication artifacts, release files, and visibility gates. | Retire pointer; retain history |
| orx/judged-4-10-baseline | 18bfb414a572fe53d8fc3ffb0e2e7830fb37bdcd | Preserve the original judged 4/10 baseline and source-table reproduction. | Retire pointer; retain history |
| orx/serializer-exact-marimo-release | 88edf92edf912c5029de955bb96bb5b067666990 | Match the exact Marimo serializer indentation used by the final notebook. | Retire pointer; retain history |
| orx/warning-free-publication-verifier | ae1baba79655ce323b8b47bf67a60075c4e57081 | Remove notebook warnings and enforce the final publication verifier. | Retire pointer; retain history |

The separate historical record in branch-audit.md remains for backward
navigation. The final remote state is intentionally main-only.
