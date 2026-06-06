# Final Release Audit

Date: 2026-05-28 Asia/Shanghai

Purpose: record the final evidence state immediately before the human review
form project.

## Repository State

| Check | Result |
| --- | --- |
| Local branch | `main` |
| Local/remote sync | clean on `main` before final tag anchoring |
| Project URL | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing` |
| Form source | `project-profile.json` |
| Form fill guide | `docs/project-profile-fill-guide.md` |
| Product evidence map | `docs/product-evaluation-map.md` |
| Current frozen tag | `final-submission-2026-06-06-r31` |

## Verification Already Passed

| Gate | Evidence |
| --- | --- |
| Unit tests | `python -m unittest discover -s tests` passed 15 tests |
| GenAIEval-compatible evaluation | `python evals\genaieval\run_wear_edge_eval.py --output evidence\genaieval\route_eval_results.json --summary-output evidence\genaieval\summary.md` passed 15/15 route cases |
| GenAIEval-compatible benchmark | `python evals\genaieval\run_wear_edge_benchmark.py --iterations 20 --output evidence\genaieval\benchmark_results.json` passed 300 route evaluations |
| Route concurrency benchmark | `python scripts\route_concurrency_benchmark.py --concurrency 8 --requests-per-route 20` passed 100 concurrent route requests with all action targets correct |
| Local Docker/OPEA TEI HTTP concurrency | Rebuilt Gateway through Docker Compose; 8 workers, 50 HTTP route requests, all OK, all `qdrant-opea-tei-vector-store` |
| LLM adapter benchmark | `python scripts\llm_adapter_benchmark.py --iterations 1 --output evidence\benchmarks\llm_adapter_contract.local-smoke.json` passed |
| Evidence manifest | `python scripts/evidence_check.py` passed |
| Project profile JSON | `python -m json.tool project-profile.json` passed |
| Public URL availability check | `docs/public-url-check.md` |
| Local Docker runtime | `docs/local-docker-desktop-final-validation.md` |
| GCP C3 Docker/Qdrant | `docs/gcp-c3-docker-qdrant-e2e-report.md` |
| GCP C3 OPEA-compatible embedding | `docs/gcp-c3-opea-profile-e2e-report.md` |
| GCP C3 official OPEA TEI | `docs/gcp-c3-opea-tei-profile-e2e-report.md` |
| Xeon AVX-512/AMX evidence | `docs/intel-avx512-amx-benchmark-report.md` |
| Intel effective-use evidence | `docs/intel-effective-use-evidence.md` and `evidence/benchmarks/intel_effective_use.summary.json` |
| OPEA upstream RFC/update evidence | `docs/opea-upstream/` and `docs/publication-record.md` |
| OPEA upstream PR | `https://github.com/opea-project/GenAIExamples/pull/2462`, open with combined status success on current head `e47ebb3bf363ecc15563bb8d05ab4c65f88e2268`; pre-commit.ci, DCO, dependency-review, get-test-matrix, get-test-case, and compose-test pass; not merged |
| OPEA docs Publications PR | `https://github.com/opea-project/docs/pull/395`, open with DCO passing; combined status pending; not merged yet |
| Knowledge-sharing package | External Dev.to article and YouTube product walkthrough video published; OPEA docs Publications PR #395 released; GitHub article/video backup evidence remains available |
| Product risk burn-down | `docs/product-risk-burn-down.md` |
| OPEA modular value framing | README, PROJECT_OVERVIEW, technical report, form guide, scorecard, and public article all state that Gateway, Megaservice, Retriever/RAG, Vector DB, LLM adapter, Evaluator, and Guardrails are modular; the model is pluggable |

## Live Runtime State

Docker Desktop is running the final OPEA TEI profile:

| Service | Evidence |
| --- | --- |
| Manufacturing Gateway | `wearedge-opea-manufacturing-manufacturing-gateway-1`, port `8088` |
| Qdrant | `wearedge-opea-manufacturing-qdrant-1`, ports `6333-6334` |
| OPEA embedding microservice | `wearedge-opea-manufacturing-opea-embedding-tei-1`, port `6000` |
| Hugging Face TEI | `wearedge-opea-manufacturing-tei-embedding-serving-1`, port `8090` |

The recorded local runtime validation confirms `/demo`, `/v1/agents`, all five
sample routes, all five infer routes, `/v1/scorecard`, and `/v1/embeddings`.

## Link Verification Notes

The last full URL availability check passed and is recorded in
`docs/public-url-check.md`. During this final audit, several GitHub HEAD
requests intermittently timed out from the local network while other GitHub URLs
returned HTTP 200 in the same run. GitHub API file fetches and `git ls-tree`
confirmed the key files exist on `origin/main`, including:

- `docs/project-profile-fill-guide.md`
- `docs/gcp-c3-opea-tei-profile-e2e-report.md`
- `public/article-wear-edge-opea-manufacturing.md`
- `evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json`

This is treated as transient local network instability, not missing project
material. New r7 evidence adds the Intel effective-use summary and external
platform article/video publishing package.

## Remaining Human Action

The only required remaining action for public release is to open the
public release page, paste the values from
`docs/project-profile-fill-guide.md`, visually confirm the fields, and
publish the release record.

Platform page:

```text
https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/project
```

Do not change the project URL away from the OPEA public repository, and do
not add claims for autonomous restart, quality release, maintenance release,
safety clearance, final root cause, production LLM acceleration, TEI/oneDNN
microkernel dispatch proof, or official OPEA Publications listing until PR
#395 is merged.
