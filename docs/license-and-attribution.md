# License And Third-Party Attribution

WearEdge OPEA Manufacturing is submitted under the MIT License. The root
`LICENSE` file is authoritative for original source code in this repository.
Source files include SPDX headers so automated reviewers can identify the
project license quickly.

## Original Work

The submitted source package is original WearEdge OPEA Manufacturing work:

- OPEA-style Gateway and Manufacturing Megaservice;
- five route agents for maintenance, IQC/OQC, changeover, work instruction,
  and hazard observation;
- deterministic evaluators, guardrails, action-card contracts, browser demo
  console, scorecard, and GenAIEval-compatible evaluation pack;
- sanitized manufacturing knowledge fixtures and benchmark evidence.

The full WearEdge-Pro engineering repository is referenced as field-evidence
provenance. Private customer plant data, labels, lot identifiers, and raw
production records are intentionally not redistributed in this public package.

## Declared Third-Party Components

| Component | License | Purpose | Usage boundary |
| --- | --- | --- | --- |
| Python standard library | PSF License | Dependency-free local demo, evaluators, route benchmarks, JSON evidence tooling | Required for local smoke path |
| FastAPI | MIT | Optional HTTP Gateway and embedding microservice API | Installed through `requirements.txt` and Docker profile |
| Uvicorn | BSD-3-Clause | Optional ASGI server for FastAPI services | Installed through `requirements.txt` and Docker profile |
| Qdrant container `qdrant/qdrant:v1.12.6` | Apache-2.0 | Optional Vector DB profile for RAG evidence | Used by `docker-compose.yml` |
| OPEA embedding image `opea/embedding:latest` | Apache-2.0 project family | Optional official OPEA TEI embedding microservice profile | Used by `docker-compose.opea-tei.yml` |
| Hugging Face Text Embeddings Inference | Apache-2.0 | Optional TEI embedding model server | Used by `docker-compose.opea-tei.yml` |
| BAAI `bge-base-en-v1.5` | MIT model family notice on Hugging Face model card | Optional TEI embedding model for 768-dimensional embedding evidence | Pulled by TEI profile only |
| OpenAI/OPEA-compatible or Gemini-compatible external model endpoints | Provider terms selected by deployer | Optional LLM/LMM adapter benchmarks | Not bundled, vendored, or required by default |
| HyperFrames demo-video source | Tooling only for public demo video source package | Optional demo video rendering evidence | Not required for runtime evaluation |

References:

- FastAPI license: `https://github.com/FastAPI/FastAPI`
- Uvicorn license: `https://github.com/encode/uvicorn`
- Qdrant license: `https://github.com/qdrant/qdrant`
- Hugging Face TEI license/API: `https://github.com/huggingface/text-embeddings-inference`
- BAAI model card: `https://huggingface.co/BAAI/bge-base-en-v1.5`
- OPEA project repositories: `https://github.com/opea-project`

## Restrictive-License Check

The application code does not vendor or intentionally import GPL, LGPL, AGPL,
or other restrictive-license packages. The default local demo and evaluation
pack are dependency-free beyond Python. The Docker/Qdrant and official OPEA TEI
profiles use permissive MIT, BSD, or Apache-compatible application components
as listed above.

If a downstream deployer swaps the optional embedding model, LLM/LMM endpoint,
or container images, that deployer must re-check the replacement component
licenses before using those artifacts for the competition or production.

## Attribution Boundary

OPEA, Qdrant, FastAPI, Uvicorn, Hugging Face TEI, and BAAI model names are used
only to identify compatible third-party components. This repository does not
claim ownership of those projects. The OPEA upstream contribution package under
`docs/opea-upstream/pr-ready/` is a proposed Apache-2.0-style contribution for
the OPEA project and is kept separate from the MIT-licensed WearEdge submission
source.

