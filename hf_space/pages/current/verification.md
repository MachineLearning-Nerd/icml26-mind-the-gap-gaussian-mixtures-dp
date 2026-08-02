# Current verification run

This page supersedes the historical `repro/src/verify.py`. Current evidence revision: `1be2569534197318cd5a36847b8eb786c5cfc52a`; fixed command:

```bash
uv sync --frozen && .venv/bin/python repro/run_all.py
```

The cumulative HF `cpu-upgrade` run exited 0 in 12.9117 seconds. Estimated cores: 1; actual allocation/affinity: 64 CPUs; seed: 260528078; image: `ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie`; Python 3.12.13. The verifier returns nonzero if an exact source aggregate, scientific terminal verdict, accepted regression, control, or notebook check fails.

Dependencies are pinned by [pyproject.toml](../../code/current/pyproject.toml) and [uv.lock](../../code/current/uv.lock). Review [the executable verifier](../../code/current/repro/run_all.py), [complete raw output](../../evidence/current/cumulative_run.json), or individual claims: [1](#/claim-1), [2](#/claim-2), [3](#/claim-3), [4](#/claim-4), [5](#/claim-5).
