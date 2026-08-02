import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Mind the Gap: a claim-by-claim reproduction

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
          <div style="padding:1rem;border:1px solid #ddd;border-radius:12px"><b>Paper DP budget</b><br><span style="font-size:2rem">0.5 × 10⁻⁶</span></div>
          <div style="padding:1rem;border:2px solid #b91c1c;border-radius:12px;color:#b91c1c"><b>Fixed-event witness</b><br><span style="font-size:2rem">67,036.7 × 10⁻⁶</span></div>
        </div>

        The strongest result is a concrete counterexample at ε=3, δ=5×10⁻⁷. Even after choosing the largest noise scale compatible with Table 1 rounding, one fixed measurable interval exceeds the allowed DP budget by 0.0670362.
        """
    )
    return


@app.cell
def _(mo):
    claims = [
        {"Claim": 1, "Paper statement": "142/150 Table 1 improvements", "Verdict": "FALSIFIED", "Observed evidence": "73/75 high-ε cells violate DP"},
        {"Claim": 2, "Paper statement": "eventual ℓ₂ advantage", "Verdict": "VERIFIED", "Observed evidence": "30/30 tail regression checks pass"},
        {"Claim": 3, "Paper statement": "up to 99% gap closure", "Verdict": "FALSIFIED", "Observed evidence": "30/30 reported tail mechanisms violate DP"},
        {"Claim": 4, "Paper statement": "same zCDP guarantee", "Verdict": "VERIFIED", "Observed evidence": "symbolic residual 0"},
        {"Claim": 5, "Paper statement": "competitive benchmark regime", "Verdict": "FALSIFIED", "Observed evidence": "staircase wins 72/75 independent cells"},
    ]
    mo.ui.table(claims)
    return (claims,)


@app.cell
def _(mo):
    mo.md(
        """
        ## How the verifier works

        Table 1's expected absolute loss and selected `K` determine the Gaussian scale. We reconstruct the **largest** scale consistent with two-decimal rounding. A float64 search proposes a measurable interval; an independent 80-decimal checker evaluates `P[M(D)∈S] − exp(ε)P[M(D′)∈S]`. If this exceeds δ for one neighboring shift in `[0,1]`, the exact DP quantifier is contradicted. Analytic-Gaussian controls pass; reducing their calibrated scale by 1% is rejected.
        """
    )
    return


@app.cell
def _(mo):
    witness = {
        "epsilon": 3,
        "delta": 5e-7,
        "K": 14,
        "conservative_sigma": 0.23811581113482513,
        "shift": 0.75,
        "interval": [-0.8690579055674126, -0.6309420944325874],
        "80_digit_difference": "0.067036715355644703485854324343982978957575295471098",
        "violation_margin": 0.0670362153556447,
    }
    mo.ui.dictionary(witness)
    return (witness,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Interpretation and limits

        This does not say Gaussian mixtures can never help. It says the **reported mechanisms** do not attain Claims 1, 3, and 5 under their stated privacy assumptions. The benchmark audit implements truncated Laplace, Tulap, and staircase for 75 high-ε cells; cactus and flipped Huber are source-audited only because the paper states neither is ever the winner.

        Formal evidence used `uv sync --frozen && .venv/bin/python repro/run_all.py` on Hugging Face `cpu-upgrade`, seed `260528078`. This notebook embeds the decisive results and does not rerun the campaign.
        """
    )
    return


if __name__ == "__main__":
    app.run()
