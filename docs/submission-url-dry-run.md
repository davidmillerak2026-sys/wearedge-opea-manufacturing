# Submission URL Dry Run

Date: 2026-05-27

Source of truth: `submission-fields.draft.json`

Result: pass. All extracted public URLs returned HTTP 200 with `curl -I -L`.

## Checked URLs

| HTTP | URL |
| --- | --- |
| 200 | https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/submission |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/demo-video-render-report.md |
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
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/raw/refs/heads/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4 |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/demo-video |
| 200 | https://github.com/davidmillerak2026-sys/WearEdge-Pro |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461 |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017 |

## Notes

- The demo video URL was changed from the `raw.githubusercontent.com` form to a
  `github.com/.../raw/refs/heads/...` URL after a local DNS lookup for
  `raw.githubusercontent.com` failed during the dry run. The replacement URL
  returned HTTP 200.
- This verifies link availability. The final challenge form should still be
  reviewed visually before pressing submit.
