# Public URL Availability Check

Date: 2026-05-27

Incremental update: 2026-05-28. The real upstream OPEA PR URL was verified
after it opened.

Source of truth: `project-profile.json`

Result: pass. All extracted public URLs returned HTTP 200 with `curl -I -L`.

## Checked URLs

| HTTP | URL |
| --- | --- |
| 200 | https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/project |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-walkthrough-render-report.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/project-profile-fill-guide.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-docker-qdrant-e2e-report.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-profile-e2e-report.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-profile.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_docker_qdrant_e2e.summary.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_profile_e2e.summary.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/gcp_c3_opea_tei_profile_e2e.summary.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/intel_cpu_benchmark.xeon-amx.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/local_opea_tei_profile_e2e.summary.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1 |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2 |
| 200 | https://www.youtube.com/watch?v=dd9k8m6PDco |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/product-walkthrough |
| 200 | https://github.com/davidmillerak2026-sys/WearEdge-Pro |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461 |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017 |
| 200 | https://github.com/opea-project/GenAIExamples/pull/2462 |

## Notes

- The product walkthrough video URL was changed from the `raw.githubusercontent.com` form to a
  GitHub `blob` asset page after local DNS/connectivity to
  `raw.githubusercontent.com` failed during the availability check. The replacement URL
  returned HTTP 200 and avoids requiring the project profile to resolve the raw
  asset domain.
- This verifies link availability. The final project profile should still be
  reviewed visually before pressing publish.
