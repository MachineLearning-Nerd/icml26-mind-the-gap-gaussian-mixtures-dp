#!/usr/bin/env python3
"""Fail-closed verification for the published Mind the Gap audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = "MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_COMMIT_COUNT = 18
EXPECTED_STATUSES = {
    "C1": "FALSIFIED",
    "C2": "VERIFIED",
    "C3": "FALSIFIED",
    "C4": "VERIFIED",
    "C5": "FALSIFIED",
}


def command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def main() -> None:
    failures: list[str] = []

    origin = command("git", "config", "--get", "remote.origin.url").strip()
    if EXPECTED_REPOSITORY not in origin:
        failures.append(f"unexpected origin: {origin}")

    branches = set(command("git", "for-each-ref", "--format=%(refname)", "refs/heads").splitlines())
    if branches != {"refs/heads/main"}:
        failures.append(f"local branches are {sorted(branches)}")

    remote_branches = set(
        command("git", "for-each-ref", "--format=%(refname)", "refs/remotes/origin").splitlines()
    )
    if remote_branches - {"refs/remotes/origin/HEAD", "refs/remotes/origin/main"}:
        failures.append(f"unexpected remote branches: {sorted(remote_branches)}")

    if command("git", "for-each-ref", "--format=%(refname)", "refs/original").splitlines():
        failures.append("backup refs remain")

    commits = command("git", "rev-list", "main").splitlines()
    if len(commits) != EXPECTED_COMMIT_COUNT:
        failures.append(f"expected {EXPECTED_COMMIT_COUNT} commits, found {len(commits)}")
    if command("git", "rev-parse", "main") != command("git", "rev-parse", "origin/main"):
        failures.append("main and origin/main differ")

    for sha in commits:
        identity = command("git", "show", "-s", "--format=%an%n%ae%n%cn%n%ce", sha).splitlines()
        if identity != [CANONICAL_NAME, CANONICAL_EMAIL, CANONICAL_NAME, CANONICAL_EMAIL]:
            failures.append(f"non-canonical identity at {sha[:12]}")
            break

    if "co-authored-by:" in command("git", "log", "main", "--format=%B").lower():
        failures.append("co-author trailer found")

    manifest = load_json("EVIDENCE_MANIFEST.json")
    for relative in manifest["required_audit_files"]:
        if not (ROOT / relative).is_file():
            failures.append(f"missing audit file: {relative}")
    for relative in manifest["required_evidence_paths"]:
        if not (ROOT / relative).is_file():
            failures.append(f"missing evidence path: {relative}")

    claims = load_json("claims.json")
    statuses = {claim["id"]: claim["status"] for claim in claims["claims"]}
    if statuses != EXPECTED_STATUSES:
        failures.append(f"unexpected claim statuses: {statuses}")

    for item in manifest["content_addressed_artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file():
            failures.append(f"missing artifact: {item['path']}")
        elif sha256(path) != item["sha256"]:
            failures.append(f"artifact hash mismatch: {item['path']}")

    cumulative = load_json("hf_space/evidence/current/cumulative_run.json")
    if cumulative["status"] != "PASS":
        failures.append("cumulative evidence is not PASS")
    if cumulative["summary"] != {
        "mean_improvement_pct": 53.729,
        "median_improvement_pct": 61.86,
        "na_count": 8,
        "population_std_pct": 34.73994461231432,
        "sample_std_pct": 34.85632666230424,
        "settings": 150,
        "strict_wins": 142,
    }:
        failures.append("source-table aggregate changed")
    if cumulative["notebook_check"]["returncode"] != 0:
        failures.append("notebook check failed")

    claim1 = load_json("hf_space/evidence/current/claim1_scientific_reproduction.json")
    if claim1["status"] != "FALSIFIED" or claim1["summary"]["rounding_robust_dp_violations"] != 73:
        failures.append("Claim 1 evidence mismatch")
    claim2 = load_json("hf_space/evidence/current/claim2_proposition_33_regression.json")
    if claim2["status"] != "PASS" or claim2["strict_variance_wins"] != 30 or not claim2["negative_control"]["rejected"]:
        failures.append("Claim 2 evidence mismatch")
    claim3 = load_json("hf_space/evidence/current/claim3_gap_closure_audit.json")
    if claim3["status"] != "FALSIFIED" or claim3["scientific_falsification"]["tail_cells_with_rounding_robust_dp_witness"] != 30:
        failures.append("Claim 3 evidence mismatch")
    claim4 = load_json("hf_space/evidence/current/claim4_corollary_37_regression.json")
    if claim4["status"] != "PASS" or claim4["symbolic_residual"] != "0" or not claim4["negative_control"]["rejected"]:
        failures.append("Claim 4 evidence mismatch")
    claim5 = load_json("hf_space/evidence/current/claim5_non_gaussian_benchmark_audit.json")
    if claim5["status"] != "FALSIFIED" or claim5["summary"]["independent_winner_counts"] != {"staircase": 72, "truncated_laplace": 0, "tulap": 3}:
        failures.append("Claim 5 evidence mismatch")

    historical = load_json("hf_space/evidence/current/historical_subset_check.json")
    if not historical["all_old_paths_present"] or not historical["all_old_bytes_preserved"]:
        failures.append("historical subset preservation failed")

    upload_manifest = ROOT / "hf_space/evidence/current/upload_manifest.sha256"
    manifest_paths: set[str] = set()
    for line in upload_manifest.read_text().splitlines():
        digest, relative = line.split(maxsplit=1)
        manifest_paths.add(relative)
        path = ROOT / "hf_space" / relative
        if not path.is_file() or sha256(path) != digest:
            failures.append(f"upload manifest mismatch: {relative}")
    allowlist = {
        line.strip()
        for line in (ROOT / "hf_space/evidence/current/upload_allowlist.txt").read_text().splitlines()
        if line.strip()
    }
    if allowlist != manifest_paths | {"evidence/current/upload_manifest.sha256"}:
        failures.append("upload allowlist and manifest disagree")

    branch_rows = [
        line for line in (ROOT / "BRANCH_AUDIT.md").read_text().splitlines()
        if line.startswith("| orx/")
    ]
    if len(branch_rows) != 11:
        failures.append("branch audit does not contain eleven retired orx branches")

    readme = (ROOT / "README.md").read_text()
    for marker in ["CLAIM_EVIDENCE.md", "SOURCE_AUDIT.md", "BRANCH_AUDIT.md", "CITATION.cff", "Thank you"]:
        if marker not in readme:
            failures.append(f"README missing dossier marker: {marker}")

    result = {
        "passed": not failures,
        "failures": failures,
        "repository": EXPECTED_REPOSITORY,
        "commit_count": len(commits),
        "claim_statuses": statuses,
        "retired_experiment_branches": len(branch_rows),
        "upload_manifest_entries": len(manifest_paths),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
