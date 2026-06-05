# Kubernetes Optional Profile

Date: 2026-06-05

## Status

Optional Kubernetes manifest added. Docker Compose remains the primary
one-command evaluation path.

Runtime file:

```text
deploy/kubernetes/wearedge-opea-manufacturing.yaml
```

The manifest deploys:

- Qdrant
- WearEdge reranker microservice
- WearEdge Manufacturing Gateway

## Local Cluster Example

Build the local image:

```powershell
docker build -t wearedge-opea-manufacturing:local .
```

For kind:

```powershell
kind load docker-image wearedge-opea-manufacturing:local
kubectl apply -f deploy\kubernetes\wearedge-opea-manufacturing.yaml
kubectl -n wearedge-opea rollout status deploy/qdrant
kubectl -n wearedge-opea rollout status deploy/reranker
kubectl -n wearedge-opea rollout status deploy/manufacturing-gateway
kubectl -n wearedge-opea port-forward svc/manufacturing-gateway 8088:8088
```

Validate:

```powershell
curl http://127.0.0.1:8088/healthz
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/scorecard
```

## Claim Boundary

Safe wording:

```text
WearEdge includes an optional Kubernetes manifest for Qdrant, reranker, and
Manufacturing Gateway deployment.
```

Avoid:

```text
Production Helm/GMC deployment is certified.
```

Helm and GMC can still be added later. This manifest is intentionally small so
it does not destabilize the Docker Compose evaluation path.
