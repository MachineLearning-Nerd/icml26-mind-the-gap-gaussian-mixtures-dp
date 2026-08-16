# Claim evidence ledger

This ledger separates the paper's universal statements from finite
regressions, source-table checks, and assumption-satisfying counterexamples.
The printed numerical aggregate is not treated as evidence that the privacy
premise holds.

## Claim 1 — Table 1 privacy-qualified improvement

- Status: FALSIFIED.
- Paper anchor: Section 5, Table 1, HTML anchor #S5.T1.
- Contract: the proposed multi-Gaussian mechanisms beat the analytic Gaussian
  mechanism in 142 of 150 settings while satisfying the stated
  (epsilon, delta)-differential privacy assumptions.
- Producers: repro/claim1_reported_loss_audit.py, repro/mechanisms.py,
  repro/claim1_continuous.py, and repro/run_all.py.
- Evidence: the 150-cell aggregate matches exactly: 142 strict wins, mean
  53.729 percent, sample standard deviation 34.856327 percent, and median
  61.86 percent. On 75 epsilon-at-least-2 entries, 73 rounding-robust
  privacy witnesses were found. The smallest violation margin is
  0.0670362153556447.
- Boundary: the audit uses one fixed measurable event and shift per witness,
  audits epsilon at least 2, and chooses the largest sigma compatible with
  two-decimal rounding. A single valid witness is sufficient to falsify the
  privacy-qualified claim; this does not show that every Gaussian mixture is
  invalid.

## Claim 2 — Proposition 3.3 eventual L2 advantage

- Status: VERIFIED.
- Paper anchor: Proposition 3.3, HTML anchors #S3.Thmtheorem3 and #A2.SS5.
- Contract: for every delta in (0, 1/2), sufficiently large epsilon gives
  strictly lower mixture L2 loss than the analytic Gaussian mechanism.
- Producers: repro/run_all.py and the preserved Proposition 3.3 evidence.
- Evidence: 30 of 30 finite tail regressions pass across 15 printed delta
  values and epsilon in {5, 10}. Replacing one strict win with equality
  produces 29 of 30 and is rejected by the negative control.
- Boundary: the finite regression is coverage evidence; the paper's theorem
  and appendix proof remain the universal basis.

## Claim 3 — Appendix D.3 gap closure

- Status: FALSIFIED.
- Paper anchor: Appendix D.3 and Table 4, including the main text's
  “up to 99 percent” gap-closure statement.
- Contract: the reported mechanisms close more than 90 percent of the
  analytic-Gaussian-to-lower-bound gap for every positive delta at epsilon 5.
- Producers: repro/claim3_gap_audit.py, repro/data/table4_gap_tail.csv,
  and repro/run_all.py.
- Evidence: Table 4 reports only 88.88 percent at epsilon 5 and delta 0.25,
  contradicting the universal wording. Separately, all 30 reported epsilon
  5 or 10 mechanisms have rounding-robust privacy witnesses.
- Boundary: this falsifies the reported mechanism values and their stated
  privacy-qualified claim, not the possibility that another valid mechanism
  could close a similar gap. The lower-bound optimization is not rerun.

## Claim 4 — Corollary 3.7 common-weight zCDP

- Status: VERIFIED.
- Paper anchor: #S3.Thmtheorem7 and proof anchor #A2.SS8.
- Contract: the common-weight translated Gaussian mixture satisfies
  rho-zCDP with rho equal to Delta squared divided by 2 sigma squared.
- Producers: the symbolic route in repro/run_all.py and the current
  Corollary 3.7 evidence.
- Evidence: SymPy reduces the certificate residual to exactly zero. A
  1.1 Delta shift gives ratio 1.21 and is rejected by the negative control.
- Boundary: the result covers the identical-weight paired-component
  construction; unequal-weight mixtures are outside scope.

## Claim 5 — non-Gaussian benchmark comparison

- Status: FALSIFIED.
- Paper anchor: Table 2 and Appendix D.6.
- Contract: the best reported mixture is competitive with truncated Laplace,
  Tulap, staircase, cactus, and flipped Huber, with truncated Laplace or
  Tulap always winning.
- Producers: repro/claim5_benchmarks.py, mechanisms.py, and run_all.py.
- Evidence: the independent benchmark covers 75 epsilon-at-least-2 cells:
  staircase wins 72, Tulap wins 3, and truncated Laplace wins 0. No cell is
  within one percentage point of the printed Table 2 value. All 60
  epsilon-at-least-3 mixture entries have rounding-robust privacy violations.
  The staircase closed form matches within 2.22e-16 and its 1 percent
  mutation is rejected.
- Boundary: cactus and flipped Huber are source-audited but not independently
  reimplemented. Their omission cannot repair the equal-privacy contradiction
  or the independent staircase result.

## Shared evidence path

- Current evaluator pages: hf_space/pages/current/.
- Raw JSON and manifest: hf_space/evidence/current/.
- Independent source and data: repro/ and repro/data/.
- Fixed command: uv sync --frozen && .venv/bin/python repro/run_all.py.
