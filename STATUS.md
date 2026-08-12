# Repository status

Paper: Mind the Gap: Mixtures of Gaussians in Approximate Differential Privacy
Authors: Huikang Liu, Aras Selvi, and Wolfram Wiesemann
Primary source: arXiv:2605.28078
Collection label: ICML 2026

Former GitHub repository: https://github.com/MachineLearning-Nerd/icml26-repro-RdBsmhb9U7-mind-the-gap-mixtures-of-gaussians-in-approximate-differential-privacy
Target GitHub repository: https://github.com/MachineLearning-Nerd/icml26-mind-the-gap-gaussian-mixtures-dp
Canonical branch: main

Current phase: published_and_verified
Publication status: normalized repository publication is in progress; no new scientific run was started for cleanup
Compute policy: historical evidence used Hugging Face cpu-upgrade with no accelerator; no new remote, paid, or GPU run is authorized by this cleanup

Source pins:

- ar5iv HTML URL: https://ar5iv.labs.arxiv.org/html/2605.28078
- ar5iv HTML SHA-256: 523ac5e6672fd75a38acb0c881b466364921fca5ff5fbf74f2ec480993957f53
- retrieval time: 2026-08-02T03:21:18Z
- validated evidence revision: bfa49f476c523a944c121c8d81457912b0363ec1

Claim status:

- Claim 1: FALSIFIED as a privacy-qualified claim; the printed 150-cell aggregate matches, but 73 of 75 audited high-epsilon cells have rounding-robust DP witnesses
- Claim 2: VERIFIED finite Proposition 3.3 tail regression; 30 of 30 strict wins and a rejected equality control
- Claim 3: FALSIFIED by the printed 88.88% Table 4 value and by 30 of 30 reported high-epsilon mechanisms having DP witnesses
- Claim 4: VERIFIED within the common-weight translated-mixture corollary; symbolic residual zero and a rejected 1.1 Delta control
- Claim 5: FALSIFIED by the independent high-epsilon benchmark winners and the missing equal-privacy premise

The current main branch contains the publication surface. Eleven historical experiment branch pointers are documented in branch-audit.md and are retired after the audit is committed. The complete raw evidence remains under hf_space/evidence/current.
