# Current verification run

This page supersedes the historical `repro/src/verify.py`. Current validated evidence revision: `bfa49f476c523a944c121c8d81457912b0363ec1`; fixed command:

```bash
uv sync --frozen && .venv/bin/python repro/run_all.py
```

The cumulative HF `cpu-upgrade` run exited 0 in 13.3903 seconds. Estimated cores: 1; actual allocation/affinity: 64 CPUs; seed: 260528078; image: `ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie`; Python 3.12.13. The notebook check also exited 0. The verifier returns nonzero if an exact source aggregate, scientific terminal verdict, accepted regression, control, or notebook check fails.

Paper source for every claim: `https://ar5iv.labs.arxiv.org/html/2605.28078`, retrieved 2026-08-02T03:21:18Z with an explicit browser User-Agent, SHA-256 `523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53`. Claim pages give the theorem, table, or appendix anchors and exact quantifiers.

Dependencies are pinned by [pyproject.toml](../../code/current/pyproject.toml) and [uv.lock](../../code/current/uv.lock). Review [the executable verifier](../../code/current/repro/run_all.py), [complete raw output](../../evidence/current/cumulative_run.json), the [historical subset proof](../../evidence/current/historical_subset_check.json), or individual claims: [1](#/claim-1), [2](#/claim-2), [3](#/claim-3), [4](#/claim-4), [5](#/claim-5).
