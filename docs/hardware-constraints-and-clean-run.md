# Hardware Constraints And Clean-Run Evidence

This note maps WearEdge OPEA Manufacturing to the challenge hardware
constraints and separates measured evidence from claim boundaries.

## Constraint Status

| Challenge constraint | WearEdge status | Evidence |
| --- | --- | --- |
| 64GB RAM or less | Pass | Google Cloud C3 `c3-standard-4` evidence uses 16 GiB RAM, with Docker stats captured for Gateway, Qdrant, OPEA-compatible embedding, and official TEI profiles. |
| 4-core CPU, Intel preferred | Pass | `c3-standard-4` was used as the cloud validation target: 4 vCPU, Intel Xeon Platinum 8481C, AVX-512 and AMX flags detected. |
| GPU optional | Pass | The C3 validation profile used no GPU. |
| Single-node only | Pass | Each GCP run used one temporary VM; Docker Compose services ran on that same node and the VM was deleted after the run. |
| Installation and initial run within 10 minutes on a clean environment | Pass | The default Docker/Qdrant C3 runner completed clean installation and initial run in 45 seconds, with `validation.clean_initial_run_under_10_min=true` and `all_checks_pass=true`; summary artifact: `evidence/benchmarks/gcp_c3_docker_qdrant_e2e_timed.summary.json`. |

## Required One-Click Path

The strict hardware and 10-minute claim should use the default required profile:

```text
deploy.sh
docker-compose.yml
```

That path starts only:

```text
qdrant
manufacturing-gateway
```

It is the smallest reviewer-facing path for the five-agent suite, `/demo`,
`/healthz`, `/v1/agents`, and `/v1/scorecard`.

The optional OPEA-compatible and official TEI profiles are stronger OPEA-depth
evidence:

```text
docker-compose.opea.yml
docker-compose.opea-tei.yml
docker-compose.onednn-verbose.yml
```

Do not use the optional TEI profile as the strict 10-minute installation claim:
TEI image and model pulls are network-dependent. Use it as supplemental OPEA
and Intel evidence.

## Timed Evidence Procedure

Run the default C3 Docker/Qdrant fresh-clone benchmark:

```bash
PROJECT_ID=gen-lang-client-0555254036 \
ZONE=us-central1-a \
BRANCH=main \
bash scripts/gcp_c3_docker_qdrant_e2e_cloudshell.sh
```

The updated runner records:

```text
runtime.setup_seconds
runtime.clean_initial_run_seconds
runtime.clean_initial_run_under_10_min
validation.clean_initial_run_under_10_min
```

Interpretation:

- `setup_seconds` measures Docker Compose build/start until `/healthz`.
- `clean_initial_run_seconds` measures package installation, Docker startup,
  fresh clone, Compose build/start, `/demo`, `/healthz`, five demo routes, five
  infer routes, and `/v1/scorecard` until the initial run is complete.
- `clean_initial_run_under_10_min=true` is the field to cite for the challenge
  10-minute requirement.

## Timed Run Result

The timed default Docker/Qdrant run passed on 2026-05-29:

```text
Project: gen-lang-client-0555254036
Zone: us-central1-a
Machine: c3-standard-4
VM: wearedge-docker-e2e-0529041313
Profile: docker-compose.yml only
validation.clean_initial_run_under_10_min: true
runtime.setup_seconds: 23
runtime.clean_initial_run_seconds: 45
all_checks_pass: true
VM cleanup: deleted after run
```

The timed value includes the remote script's package installation phase, Docker
startup, fresh clone, Compose build/start, `/demo`, `/healthz`, five demo
routes, five infer routes, and `/v1/scorecard` until the initial run is
complete.

## Current Claim Boundary

Safe wording:

```text
The default one-click Docker/Qdrant profile completed clean installation and initial run in 45 seconds on Google Cloud C3 c3-standard-4, staying within the challenge envelope of single node, 4 vCPU, 16 GiB RAM, and no GPU. The timed run passed all route, scorecard, Docker stats, and clean-run validation checks, and the temporary VM was deleted after the run.
```
