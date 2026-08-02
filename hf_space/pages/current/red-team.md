# Evaluator-blind red-team record

## Pass 1 — 2026-08-02

The review used a fresh materialization of the exact candidate upload tree and only the canonical `README.md`, `pages/index.md`, evaluator rubric, and links discovered from them. No repository or OpenResearch state supplied missing facts.

Files opened, in order:

```text
README.md
pages/index.md
pages/current/verification.md
code/current/pyproject.toml
code/current/uv.lock
code/current/repro/run_all.py
evidence/current/cumulative_run.json
pages/current/visibility-matrix.md
pages/current/release-report.md
pages/historical-rejected-baseline-index.md
pages/current/claim-1.md
evidence/current/claim1_dp_witness.svg
code/current/repro/claim1_reported_loss_audit.py
code/current/repro/mechanisms.py
evidence/current/claim1_scientific_reproduction.json
pages/current/claim-2.md
evidence/current/claim2_proposition_33_regression.json
pages/current/claim-3.md
evidence/current/claim3_gap_closure.svg
code/current/repro/claim3_gap_audit.py
evidence/current/claim3_gap_closure_audit.json
code/current/repro/data/table4_gap_tail.csv
pages/current/claim-4.md
evidence/current/claim4_corollary_37_regression.json
pages/current/claim-5.md
evidence/current/claim5_benchmark_winners.svg
code/current/repro/claim5_benchmarks.py
evidence/current/claim5_non_gaussian_benchmark_audit.json
code/current/repro/data/table2_high_epsilon.csv
pages/overview/page.md
pages/claims/page.md
pages/evidence/page.md
pages/verification-run/page.md
pages/conclusion/page.md
```

No broken paths were found. One conclusion could not be independently verified: Claim 2 described a non-strict fail condition but did not expose an executed negative-control result. Repair: add an equality mutation to the fixed verifier, run it on HF `cpu-upgrade`, and mirror the observed 29/30 rejection. The HF run passed. Its notebook check also exposed three formatting warnings; the notebook strings were dedented before the final release run.

## Pass 2

Completed on 2026-08-02 from a second fresh candidate tree after mirroring the repaired HF output. The reviewer found no broken paths, no missing visibility cells, a five-row visibility matrix, current verification first in navigation, valid JSON, a passing historical subset proof, and matching SHA-256 values for every manifest entry.

Files opened, in order (duplicates removed after first access):

```text
README.md
pages/index.md
pages/current/verification.md
code/current/pyproject.toml
code/current/uv.lock
code/current/repro/run_all.py
evidence/current/cumulative_run.json
evidence/current/historical_subset_check.json
pages/current/visibility-matrix.md
pages/current/release-report.md
evidence/current/upload_allowlist.txt
evidence/current/upload_manifest.sha256
pages/current/red-team.md
pages/historical-rejected-baseline-index.md
pages/current/claim-1.md
evidence/current/claim1_dp_witness.svg
code/current/repro/claim1_reported_loss_audit.py
code/current/repro/mechanisms.py
evidence/current/claim1_scientific_reproduction.json
pages/current/claim-2.md
evidence/current/claim2_proposition_33_regression.json
pages/current/claim-3.md
evidence/current/claim3_gap_closure.svg
code/current/repro/claim3_gap_audit.py
evidence/current/claim3_gap_closure_audit.json
code/current/repro/data/table4_gap_tail.csv
pages/current/claim-4.md
evidence/current/claim4_corollary_37_regression.json
pages/current/claim-5.md
evidence/current/claim5_benchmark_winners.svg
code/current/repro/claim5_benchmarks.py
evidence/current/claim5_non_gaussian_benchmark_audit.json
code/current/repro/data/table2_high_epsilon.csv
pages/overview/page.md
pages/claims/page.md
pages/evidence/page.md
pages/verification-run/page.md
pages/conclusion/page.md
.gitattributes
bucket-icon.svg
code/current/notebooks-mind_the_gap_reproduction.py
code/current/repro/claim1_continuous.py
code/current/repro/data/table1_l1.csv
code/current/repro/data/table3_best_k.csv
code/current/repro/report_figures.py
evidence/current/claim1_grid_audit.svg
historical/judged-efa0aed7/README.md
historical/judged-efa0aed7/judged_space_manifest.sha256
historical/judged-efa0aed7/logbook.json
historical/judged-efa0aed7/pages-index.md
index.html
logbook.css
logbook.js
logbook.json
style.css
```

Conclusion: **PASS**. Claims 1–5 are directly discoverable with source quantifiers, inline results, code, raw data, checkers, controls, limitations, command, environment, seed, CPU/runtime metadata, and terminal verdicts. No repository-only fact was needed.
