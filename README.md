# ICML 2026 — Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy

Independent, claim-by-claim reproduction and audit of [Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy](https://arxiv.org/abs/2605.28078).

> Status: complete audit published on the normalized main branch. Claims 1, 3, and 5 are falsified under the paper's stated privacy contract; Claims 2 and 4 are verified within their stated scopes.

The printed Table 1 aggregate is reproduced exactly: 142 strict wins out of 150 settings, mean improvement 53.729%, sample standard deviation 34.856%, and median 61.86%. That numerical match is kept separate from the privacy audit. The reported high-epsilon mixture losses do not satisfy the stated approximate differential privacy condition, even when the most privacy-favorable value allowed by two-decimal rounding is used.

## Paper

| Item | Record |
| --- | --- |
| Title | Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy |
| Authors | Huikang Liu, Aras Selvi, and Wolfram Wiesemann |
| Paper | [arXiv:2605.28078](https://arxiv.org/abs/2605.28078) |
| Venue record | [Author announcement for ICML 2026](https://wp.doc.ic.ac.uk/wwiesema/2026/05/04/mind-the-gap-mixtures-of-gaussians-in-approximate-differential-privacy/) |
| Paper source used for checks | [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2605.28078), retrieved 2026-08-02 |
| Source SHA-256 | 523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53 |
| Current repository | [MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp](https://github.com/MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp) |
| Former repository name | icml26-repro-RdBsmhb9U7-mind-the-gap-mixtures-of-gaussians-in-approximate-differential-privacy |
| Canonical branch | main |

No public author implementation was identified in the paper record. The code in this repository is therefore an independent reproduction and audit, not an official release.

## What the paper is doing

The paper studies additive noise mechanisms for releasing a sensitive quantity. Its mechanism is a finite mixture of Gaussian distributions with common variance and separated means. The mixture weights and separation are chosen as a function of sensitivity, privacy parameters, and the desired loss. The paper compares the mixture against the analytic Gaussian mechanism and several non-Gaussian mechanisms under approximate differential privacy.

The central research question is whether a carefully selected Gaussian mixture can obtain lower L1 or L2 error than the analytic Gaussian mechanism while retaining the claimed privacy guarantee. The paper also gives a zCDP composition result for a common-weight translated mixture, and reports benchmark comparisons and gap closures against a theoretical lower bound.

## Claim ledger

| Claim | Paper statement | Production path in this repository | Evidence and verdict |
| --- | --- | --- | --- |
| 1 | Table 1 reports that the proposed mixtures beat analytic Gaussian in 142 of 150 settings, with 53.73% mean improvement. | Parse the printed tables; reconstruct sigma from each rounded loss; search a fixed event and neighboring shift; recompute the hockey-stick difference at 80 decimal digits. | The 150-cell aggregate matches exactly, but 73 of 75 epsilon greater than or equal to 2 cells have rounding-robust DP witnesses. **FALSIFIED as a privacy-qualified claim.** |
| 2 | For every delta in (0, 1/2), a sufficiently large epsilon gives strictly lower L2 mixture loss than analytic Gaussian. | Reconstruct the Proposition 3.3 tail regime over all 15 printed delta values at epsilon 5 and 10, and run the equality negative control. | 30 of 30 strict variance comparisons pass; the equality mutation is rejected at 29 of 30. **VERIFIED for the finite regression; the paper proof remains the universal basis.** |
| 3 | For epsilon at least 5, the multi-Gaussian closes more than 90% of the analytic-Gaussian-to-lower-bound gap for any positive delta, up to 99%. | Parse Table 4; independently audit the source quantifier; test the reported mechanisms with the same high-precision DP witness route. | Table 4 itself reports 88.88% at epsilon 5 and delta 0.25; all 30 reported epsilon 5 or 10 mechanisms also have DP witnesses. **FALSIFIED.** |
| 4 | The common-weight translated mixture satisfies rho-zCDP with rho equal to Delta squared divided by 2 sigma squared. | Reconstruct the paired-component Renyi calculation symbolically with SymPy and test a shifted-component negative control. | Symbolic residual is exactly zero; the 1.1 Delta control gives ratio 1.21 and is rejected. **VERIFIED within the corollary's equal-weight scope.** |
| 5 | Against truncated Laplace, Tulap, staircase, cactus, and flipped Huber, the mixture is competitive and the benchmark winner is always truncated Laplace or Tulap. | Implement independent truncated Laplace, Tulap, and optimal pure-DP staircase controls; compare 75 high-epsilon cells; source-audit the two remaining named families. | Staircase wins 72 cells and Tulap 3; truncated Laplace wins 0; no cell is within one percentage point of printed Table 2. All 60 epsilon at least 3 mixture entries have DP witnesses. **FALSIFIED.** |

Falsified means that the exact registered statement cannot hold under the paper's own stated assumptions, because this audit contains a reproducible contradiction or a valid privacy counterexample. It does not mean that every possible Gaussian mixture is invalid, nor does it assess the authors' intent.

## How each claim is produced

1. Pin the paper HTML and record its retrieval time, URL, and SHA-256.
2. Extract the printed epsilon, delta, K, loss, and benchmark tables into repository data files.
3. Reconstruct the mechanism and loss from the displayed values rather than copying a claimed conclusion.
4. For privacy claims, choose the largest sigma compatible with the printed two-decimal rounding. This favors the paper.
5. Search a fixed measurable interval and a neighboring shift. Re-evaluate the selected witness independently with 80-digit arithmetic.
6. Run theorem-specific checkers: a finite Proposition 3.3 tail regression, a symbolic Corollary 3.7 identity, a Table 4 source-quantifier audit, and independent benchmark controls.
7. Run negative controls that deliberately break the expected result. A checker is accepted only when the positive case passes and the mutated case is rejected.
8. Record the claim verdicts, controls, limitations, environment, and terminal status in JSON. The cumulative verifier exits nonzero when a required source, scientific, control, or notebook gate fails.

The fixed reproduction command is:

    uv sync --frozen && .venv/bin/python repro/run_all.py

Historical research computation ran on Hugging Face cpu-upgrade, with Python 3.12.13 and a locked environment. The cumulative run exited 0 in 13.3903 seconds; the job had an 8-vCPU quota and no accelerator. No GPU was used. This repository cleanup does not authorize a new remote or paid run.

## Repository map

| Path | Purpose |
| --- | --- |
| repro/ | Independent mechanism, claim, benchmark, and cumulative verification code |
| repro/data/ | Transcribed paper tables used by the checkers |
| hf_space/pages/current/ | Claim-by-claim evaluator-visible explanations |
| hf_space/evidence/current/ | Raw JSON, SVG figures, upload allowlist, and candidate manifest |
| hf_space/code/current/ | Hash-mirrored code used by the historical Hugging Face publication |
| reports/mind-the-gap/report.md | Reader-facing scientific report |
| notebooks/mind_the_gap_reproduction.py | Self-contained Marimo reproduction notebook |
| branch-audit.md | Former branch names, purposes, tips, and cleanup decisions |
| STATUS.md | Current paper, claim, source, and publication status |
| AUTONOMOUS_STATE.json | Machine-readable continuation state for the collection workflow |

Start with [Current verification](hf_space/pages/current/verification.md), then read the individual [Claim 1](hf_space/pages/current/claim-1.md), [Claim 2](hf_space/pages/current/claim-2.md), [Claim 3](hf_space/pages/current/claim-3.md), [Claim 4](hf_space/pages/current/claim-4.md), and [Claim 5](hf_space/pages/current/claim-5.md) pages. The [visibility matrix](hf_space/pages/current/visibility-matrix.md) maps every claim to its code, data, checker, control, and raw evidence.

## Branch policy

The public repository uses one stable branch: main. The former orx/* names were experiment labels, not public interfaces. Every former remote tip was an ancestor of the final pre-normalization main tip, so retiring those pointers does not discard their reachable history. Their purposes and outcomes are recorded in [branch-audit.md](branch-audit.md).

## Citation

Please cite the paper when using this reproduction:

    @article{liu2026mind,
      title = {Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy},
      author = {Liu, Huikang and Selvi, Aras and Wiesemann, Wolfram},
      journal = {arXiv preprint arXiv:2605.28078},
      year = {2026},
      doi = {10.48550/arXiv.2605.28078}
    }

## Thank you

Thank you to Huikang Liu, Aras Selvi, and Wolfram Wiesemann for making a precise, ambitious study of Gaussian mixtures and privacy-utility tradeoffs available for independent scrutiny. The paper's explicit tables, theorem statements, and mechanism definitions made it possible to reproduce the numerical aggregates, reconstruct the proof-level checks, and test the privacy assumptions directly. This repository is intended as a respectful reproducibility record and a contribution to transparent scientific discussion.

## Scope and limitations

- Claim 1 audits the epsilon at least 2 portion of the printed table and does not recalibrate every possible K value.
- A fixed-event witness is sufficient to falsify DP, but this audit does not compute the full supremum over all measurable events.
- Claim 2 is reported as a finite regression plus the paper's proof certificate; the finite run is not presented as a new universal proof.
- Claim 5 independently covers truncated Laplace, Tulap, and staircase across 75 high-epsilon cells. Cactus and flipped Huber are source-audited rather than fully reimplemented.
- The historical Hugging Face score was 4/10. The verdicts in this repository are scientific audit results, not a new judge score.
