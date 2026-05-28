# Final Pre-Submit Audit

Date: 2026-05-28 Asia/Shanghai

Purpose: record the final evidence state immediately before the human challenge
form submission.

## Repository State

| Check | Result |
| --- | --- |
| Local branch | `main` |
| Local/remote sync | clean on `main` before final tag anchoring |
| Project URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing` |
| Form source | `submission-fields.draft.json` |
| Form fill guide | `docs/final-submission-form-fill-guide.md` |
| Final tag | `final-submission-2026-05-28-r3` |

## Verification Already Passed

| Gate | Evidence |
| --- | --- |
| Unit tests | `python -m unittest discover -s tests` passed 14 tests |
| LLM adapter benchmark | `python scripts\llm_adapter_benchmark.py --iterations 1 --output evidence\benchmarks\llm_adapter_contract.local-smoke.json` passed |
| Evidence manifest | `python scripts/evidence_check.py` passed |
| Submission JSON | `python -m json.tool submission-fields.draft.json` passed |
| Public URL dry run | `docs/submission-url-dry-run.md` |
| Local Docker runtime | `docs/local-docker-desktop-final-validation.md` |
| GCP C3 Docker/Qdrant | `docs/gcp-c3-docker-qdrant-e2e-report.md` |
| GCP C3 OPEA-compatible embedding | `docs/gcp-c3-opea-profile-e2e-report.md` |
| GCP C3 official OPEA TEI | `docs/gcp-c3-opea-tei-profile-e2e-report.md` |
| Xeon AVX-512/AMX evidence | `docs/intel-avx512-amx-benchmark-report.md` |
| OPEA upstream RFC/update evidence | `docs/opea-upstream/` and `docs/publication-record.md` |
| Champion risk burn-down | `docs/champion-risk-burn-down.md` |

## Live Runtime State

Docker Desktop is running the final OPEA TEI profile:

| Service | Evidence |
| --- | --- |
| Manufacturing Gateway | `wearedge-opea-manufacturing-manufacturing-gateway-1`, port `8088` |
| Qdrant | `wearedge-opea-manufacturing-qdrant-1`, ports `6333-6334` |
| OPEA embedding microservice | `wearedge-opea-manufacturing-opea-embedding-tei-1`, port `6000` |
| Hugging Face TEI | `wearedge-opea-manufacturing-tei-embedding-serving-1`, port `8090` |

The recorded local runtime validation confirms `/demo`, `/v1/agents`, all five
demo routes, all five infer routes, `/v1/scorecard`, and `/v1/embeddings`.

## Link Verification Notes

The last full URL dry run passed and is recorded in
`docs/submission-url-dry-run.md`. During this final audit, several GitHub HEAD
requests intermittently timed out from the local network while other GitHub URLs
returned HTTP 200 in the same run. GitHub API file fetches and `git ls-tree`
confirmed the key files exist on `origin/main`, including:

- `docs/final-submission-form-fill-guide.md`
- `docs/gcp-c3-opea-tei-profile-e2e-report.md`
- `public/article-wear-edge-opea-manufacturing.md`
- `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`

This is treated as transient local network instability, not missing submission
material.

## Remaining Human Action

The only required remaining action is to open the challenge submission page,
paste the values from `docs/final-submission-form-fill-guide.md`, visually
confirm the fields, and press submit.

Submission page:

```text
https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/submission
```

Do not change the project URL away from the OPEA competition repository, and do
not add claims for autonomous restart, quality release, maintenance release,
safety clearance, final root cause, or production LLM acceleration unless a
real endpoint benchmark is attached with `production_llm_endpoint_benchmarked`.
