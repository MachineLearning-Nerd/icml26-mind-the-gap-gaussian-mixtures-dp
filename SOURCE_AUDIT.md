# Source audit

## Paper identity

| Field | Record |
| --- | --- |
| Title | Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy |
| Authors | Huikang Liu; Aras Selvi; Wolfram Wiesemann |
| Primary source | https://arxiv.org/abs/2605.28078 |
| Public review record | https://openreview.net/forum?id=RdBsmhb9U7 |
| Venue announcement | https://wp.doc.ic.ac.uk/wwiesema/2026/05/04/mind-the-gap-mixtures-of-gaussians-in-approximate-differential-privacy/ |
| Collection label | ICML 2026 |
| Paper DOI | https://doi.org/10.48550/arXiv.2605.28078 |

The arXiv record identifies the title and three authors. The Imperial
announcement records acceptance at ICML 2026. The collection label is an
organizing label for this repository set, not a replacement for the paper's
source metadata.

## Source pin

- Source HTML: https://ar5iv.labs.arxiv.org/html/2605.28078
- Source SHA-256:
  523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53
- Retrieved: 2026-08-02T03:21:18Z
- Main source anchors: #S5.T1 for Table 1, #S3.Thmtheorem3 for
  Proposition 3.3, #S3.Thmtheorem7 for Corollary 3.7, and #A2.SS8 for its
  proof.

The repository preserves the source table files and records deviations
between the paper's exact wording and imported judge wording, especially for
Claim 3.

## Implementation provenance

No public author-maintained implementation was identified in the paper record.
The code under repro/ is an independent reconstruction. The mirrored
hf_space/code/current tree is the historical evaluator presentation of that
reconstruction, not an assertion that it is author code.

## Evidence boundaries

- A fixed-event hockey-stick witness is sufficient to falsify approximate DP,
  but it is not a numerical calculation of the supremum over all measurable
  events.
- Claims 2 and 4 retain theorem-level source statements, while their finite
  regressions and symbolic certificate are reproducibility checks.
- Cactus and flipped Huber are source-audited rather than independently
  implemented.
- The prior live score and projected score are evaluation provenance only.
  No current judge result is claimed.
- The cleanup did not start a new remote, paid, or GPU scientific run.
