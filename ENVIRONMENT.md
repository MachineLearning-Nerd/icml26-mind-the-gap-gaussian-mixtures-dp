# Environment and artifact record

## Fixed scientific command

~~~text
uv sync --frozen && .venv/bin/python repro/run_all.py
~~~

The cleanup did not start a new scientific run. The values below are the
historical cumulative campaign that produced the committed evidence.

## Recorded cumulative run

| Field | Value |
| --- | --- |
| Evidence revision | bfa49f476c523a944c121c8d81457912b0363ec1 |
| Backend | Hugging Face cpu-upgrade |
| Image | ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie |
| Estimated cores | 1 |
| Affinity CPUs | 64 |
| Accelerator | none |
| Python | 3.12.13 |
| NumPy | 2.5.1 |
| SciPy | 1.18.0 |
| SymPy | 1.14.0 |
| Matplotlib | 3.11.1 |
| Marimo | 0.23.16 |
| Seed | 260528078 |
| Scientific runtime | 13.390348709000136 seconds |
| Cumulative status | PASS |
| Notebook return code | 0, with three recorded formatting warnings |

## Content-addressed evidence

| Path | SHA-256 |
| --- | --- |
| hf_space/evidence/current/cumulative_run.json | de5c214842eecf3c4a9a6ddd6b9242f0da4bcd6d9c7bd306d5a4de21a5f8bb01 |
| hf_space/evidence/current/claim1_scientific_reproduction.json | f1328be890c3fec63efc9289fda516190353b65db199437d61f23e41ca45b9a5 |
| hf_space/evidence/current/claim2_proposition_33_regression.json | 22bb8e91d225739182f9817ad131055c402bcedc2c130402efd038d2ff709416 |
| hf_space/evidence/current/claim3_gap_closure_audit.json | f9b3b4fe52c77b730525c7ec6c6a19bad36961ff9c230781fd95f8b7c3dba0fe |
| hf_space/evidence/current/claim4_corollary_37_regression.json | d19f8778f310e387506cc66ed992cd7a70f648db251f4cd38576250020938e25 |
| hf_space/evidence/current/claim5_non_gaussian_benchmark_audit.json | e0e5e3a6f2d8c7c257d1ac2dfb9fd610a72820bdc6b9c3c8ea56e7322e618bd5 |
| hf_space/evidence/current/historical_subset_check.json | 90be3f32169004e30df8ae46264a97342d4827790649b960c1aa02ba428ee1c3 |
| hf_space/evidence/current/upload_allowlist.txt | aeed41a411d647dbb992e7a540571e3521a25413ded270af2c61e680386aadd3 |
| hf_space/evidence/current/upload_manifest.sha256 | 1e10860380f54ff5581b9fc56fa01aa855363d6cef842ae0160ddab771db6c3e |
| hf_space/logbook.json | 3921e1836a6b831ba6aa1836521b9914754b8e6e012894db3a178efd49ce2a82 |

The upload manifest covers 54 text and image paths; the allowlist adds the
manifest itself because a manifest cannot contain its own final hash.
