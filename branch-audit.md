# Historical branch audit

Before normalization, this repository had one publication branch and eleven remote experiment branches. Every former branch tip was an ancestor of the pre-normalization main tip 88edf92edf912c5029de955bb96bb5b067666990. The experiment history therefore remains reachable through main after the branch pointers are retired.

| Former branch | Pre-normalization tip | Purpose and recorded outcome | Disposition |
| --- | --- | --- | --- |
| main | 88edf92edf912c5029de955bb96bb5b067666990 | Final publication surface, exact Table 1 aggregate, claim ledger, and release artifacts. | Keep as canonical main |
| orx/claim-1-continuous-dp-selected-k-recalibration | 3dfca2ebf687c3188b5eb25bb55d5dfc425b9446 | Continuous differential privacy audit for selected K values and reported mixture losses. | Retire pointer; history retained |
| orx/claim-1-reference-cap-adversarial-audit | ba6035edc1659e31b22f177dd33cb9c10049ae6e | Reference-cap and rounding-robust fixed-event audit for Claim 1. | Retire pointer; history retained |
| orx/claim-1-stable-privacy-loss-quadrature | 82de82c3213d57abcc88f20ad829b6951904a37e | Stable privacy-loss quadrature route and high-precision witness validation. | Retire pointer; history retained |
| orx/claim-3-exact-gap-closure-audit | 90456bb936d938190d2fec80b21611424f448f6e | Audit the exact Table 4 gap-closure quantifier and reported values. | Retire pointer; history retained |
| orx/claim-5-non-gaussian-benchmark-audit | 4191fb93fa6b74bf18485ac4c244af6692c89df2 | Independent truncated-Laplace, Tulap, and staircase benchmark checks. | Retire pointer; history retained |
| orx/cumulative-release-evidence-suite | 1be2569534197318cd5a36847b8eb786c5cfc52a | Combine the claim checkers, negative controls, and cumulative evidence output. | Retire pointer; history retained |
| orx/evaluator-visible-release-candidate | bfa49f476c523a944c121c8d81457912b0363ec1 | Assemble the evaluator-visible claim pages and raw evidence paths. | Retire pointer; history retained |
| orx/final-publication-artifact-and-release-gates | cbb2dd2e7dc5778753797d143b4d884ccb3d24ce | Prepare the publication artifact, release files, and visibility gates. | Retire pointer; history retained |
| orx/judged-4-10-baseline | 18bfb414a572fe53d8fc3ffb0e2e7830fb37bdcd | Preserve the original judged 4/10 baseline and source-table reproduction. | Retire pointer; history retained |
| orx/serializer-exact-marimo-release | 88edf92edf912c5029de955bb96bb5b067666990 | Match the exact Marimo serializer indentation used by the final notebook. | Retire pointer; history retained |
| orx/warning-free-publication-verifier | ae1baba79655ce323b8b47bf67a60075c4e57081 | Remove notebook warnings and enforce the final publication verifier. | Retire pointer; history retained |

The orx/* names were generated experiment labels, not stable public APIs. The normalized public surface uses only main; the claim pages, raw evidence, commit history, and this audit preserve the experiment purposes and outcomes.

Before normalization, the branch tips used the local Dinesh identity. The final history rewrite sets both author and committer to MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com> for every reachable commit.
