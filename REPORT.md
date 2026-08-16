# Audit report

## Decision

Claims 1, 3, and 5 are FALSIFIED at the paper's stated
privacy-qualified scope. Claims 2 and 4 remain VERIFIED within their stated
theorem scopes. The result is based on exact source-table checks,
assumption-satisfying privacy witnesses, a symbolic zCDP identity, and
independent benchmark controls.

## Interpretation

The printed Table 1 aggregate is reproduced exactly, but that numerical match
does not establish differential privacy. The high-epsilon mechanisms implied
by the printed rounded losses fail the stated privacy condition on fixed
events. Claim 3 also fails directly from the paper's own Table 4 value of
88.88 percent at epsilon 5 and delta 0.25. Claim 5's independent benchmark
route finds staircase winning 72 of 75 audited cells.

## Publication boundary

The public repository is renamed to
MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp, keeps only main,
and has 18 canonical MachineLearning-Nerd commits after the dossier commit.
Eleven former orx branches are documented rather than exposed as public
interfaces. The historical live judge score is 4/10 and the 8–10/10 range is
a forecast only; no current judge score is claimed.

## Limitations

- Claim 1 uses one fixed event per counterexample and audits epsilon at least
  2; it does not compute the full privacy supremum.
- Claim 2's finite regression is not a replacement for the universal proof.
- Claim 3's source quantifier audit does not rerun the lower-bound optimizer.
- Claim 5 independently implements three benchmark families; cactus and
  flipped Huber are source-audited only.
- The cleanup did not authorize a new remote, paid, or GPU run.
