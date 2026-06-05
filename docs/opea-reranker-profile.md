# OPEA-Compatible Reranker Profile

Date: 2026-06-05

## Status

Implemented as an optional profile. The default WearEdge route path remains
dependency-free and deterministic. When enabled, the RAG path becomes:

```text
Retriever / Vector DB hits
  -> Reranker
  -> route evaluator
  -> guardrails
  -> action card
```

Runtime files:

```text
src/wear_edge_opea/reranker.py
src/wear_edge_opea/reranker_service.py
docker-compose.reranker.yml
tests/test_pipeline.py
```

## In-Process Reranker Smoke Test

```powershell
$env:PYTHONPATH="src"
$env:WEAREDGE_RERANKER_BACKEND="lexical"
python -m wear_edge_opea.run_demo
```

Expected marker in each route result:

```text
rag.reranker.status=lexical
rag.reranker.applied=true
```

## Microservice Profile

```bash
docker compose -f docker-compose.yml -f docker-compose.reranker.yml up --build -d
curl http://127.0.0.1:7000/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

Expected gateway environment:

```text
WEAREDGE_RERANKER_BACKEND=remote
WEAREDGE_RERANKER_URL=http://reranker:7000/v1/rerank
```

Expected result marker:

```text
rag.reranker.status=remote
rag.reranker.applied=true
```

## Claim Boundary

Safe wording:

```text
WearEdge now includes an optional OPEA-compatible reranking microservice
boundary and an in-process reranker smoke path.
```

Avoid:

```text
Official OPEA production reranker model benchmarked.
```

The current implementation is a lightweight lexical reranker designed to prove
the microservice boundary and preserve deterministic evaluation. It can be
replaced with a production reranking model or official GenAIComps reranking
service without changing the Gateway, Megaservice, evaluator, guardrails, or
action-card contracts.
