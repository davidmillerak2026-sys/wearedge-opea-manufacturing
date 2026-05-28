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
| Final tag | `final-submission-2026-05-28-r7` |

## Verification Already Passed

| Gate | Evidence |
| --- | --- |
| Unit tests | `python -m unittest discover -s tests` passed 15 tests |
| GenAIEval-compatible evaluation | `python evals\genaieval\run_wear_edge_eval.py --output evidence\genaieval\route_eval_results.json --summary-output evidence\genaieval\summary.md` passed 15/15 route cases |
| GenAIEval-compatible benchmark | `python evals\genaieval\run_wear_edge_benchmark.py --iterations 20 --output evidence\genaieval\benchmark_results.json` passed 300 route evaluations |
| LLM adapter benchmark | `python scripts\llm_adapter_benchmark.py --iterations 1 --output evidence\benchmarks\llm_adapter_contract.local-smoke.json` passed |
| Evidence manifest | `python scripts/evidence_check.py` passed |
| Submission JSON | `python -m json.tool submission-fields.draft.json` passed |
| Public URL dry run | `docs/submission-url-dry-run.md` |
| Local Docker runtime | `docs/local-docker-desktop-final-validation.md` |
| GCP C3 Docker/Qdrant | `docs/gcp-c3-docker-qdrant-e2e-report.md` |
| GCP C3 OPEA-compatible embedding | `docs/gcp-c3-opea-profile-e2e-report.md` |
| GCP C3 official OPEA TEI | `docs/gcp-c3-opea-tei-profile-e2e-report.md` |
| Xeon AVX-512/AMX evidence | `docs/intel-avx512-amx-benchmark-report.md` |
| Intel effective-use evidence | `docs/intel-effective-use-evidence.md` and `evidence/benchmarks/intel_effective_use.summary.json` |
| OPEA upstream RFC/update evidence | `docs/opea-upstream/` and `docs/publication-record.md` |
| OPEA upstream PR | `https://github.com/opea-project/GenAIExamples/pull/2462`, CI-green on head `0c149a06` |
| Knowledge-sharing package | GitHub article/video evidence plus copy-ready external article and public video metadata; external Medium/LinkedIn/Dev.to/YouTube/Bilibili URL still pending |
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
material. New r7 evidence adds the Intel effective-use summary and external
platform article/video publishing package.

## Remaining Human Action

The only required remaining action for challenge submission is to open the
challenge submission page, paste the values from
`docs/final-submission-form-fill-guide.md`, visually confirm the fields, and
press submit. To maximize the knowledge-sharing bonus, also publish
`public/external-platform-article.md` on a public blog/article platform and
upload the demo video using `public/video-platform-description.md`, then add the
resulting external URLs back into the submission notes if time allows.

Submission page:

```text
https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/submission
```

Do not change the project URL away from the OPEA competition repository, and do
not add claims for autonomous restart, quality release, maintenance release,
safety clearance, final root cause, production LLM acceleration, TEI/oneDNN
microkernel dispatch proof, or external public-platform publication unless the
corresponding URL or benchmark artifact is attached.
