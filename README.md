# Claim-by-claim reproduction: Mind the Gap

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-RdBsmhb9U7-mind-the-gap-mixtures-of-gaussians-in-approximate-differential-privacy/blob/main/notebooks/mind_the_gap_reproduction.py)

We audited all five judged claims from arXiv:2605.28078. The paper's Table 1 aggregates reproduce exactly (142/150 wins; mean 53.729%, sample SD 34.856%, median 61.86%), but the reported high-epsilon mixture losses do not satisfy the stated approximate-DP contract: 73 of 75 cells have rounding-robust fixed-event witnesses. Claims 1, 3, and 5 are therefore **FALSIFIED** under the paper's own assumptions. The already accepted Proposition 3.3 and Corollary 3.7 checks remain **VERIFIED**.

All research computation ran on Hugging Face `cpu-upgrade`; the local machine was used only for inspection, editing, and orchestration. Read the [illustrated report](reports/mind-the-gap/report.md), the [self-contained notebook](notebooks/mind_the_gap_reproduction.py), or the [candidate evaluator logbook](hf_space/pages/index.md).

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Reader-facing report and notebook | None |
| `orx/judged-4-10-baseline` | Freeze and reproduce judged source table | `uv sync --frozen && .venv/bin/python repro/run_all.py` | Exact Table 1 source aggregates | HF `cpu-upgrade`, 64 allocated CPUs |
| `orx/claim-1-reference-cap-adversarial-audit` | Rounding-robust DP counterexample search | `uv sync --frozen && .venv/bin/python repro/run_all.py` | Claim 1 FALSIFIED | HF `cpu-upgrade`, 64 allocated CPUs |
| `orx/claim-3-exact-gap-closure-audit` | Audit Table 4 and gap-closure assumptions | `uv sync --frozen && .venv/bin/python repro/run_all.py` | Claim 3 FALSIFIED | HF `cpu-upgrade`, 64 allocated CPUs |
| `orx/claim-5-non-gaussian-benchmark-audit` | Independent non-Gaussian benchmarks | `uv sync --frozen && .venv/bin/python repro/run_all.py` | Claim 5 FALSIFIED | HF `cpu-upgrade`, 64 allocated CPUs |
| `orx/cumulative-release-evidence-suite` | Rerun all accepted checks and controls | `uv sync --frozen && .venv/bin/python repro/run_all.py` | 5/5 terminal verdicts; cumulative PASS | HF `cpu-upgrade`, 64 allocated CPUs |

The paper value and observed value are deliberately separated: reproducing a printed aggregate is not evidence that its underlying mechanisms satisfy differential privacy. No GPU was used.
