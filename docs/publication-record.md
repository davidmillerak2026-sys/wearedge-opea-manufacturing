# Publication Record

This file records public URLs that support the OPEA challenge bonus evidence.

## OPEA Upstream

| Item | Status | URL |
| --- | --- | --- |
| RFC issue | Posted | https://github.com/opea-project/GenAIExamples/issues/2461 |
| Implementation feedback comment | Posted upstream | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4551375202 |
| Official TEI update comment | Posted upstream | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017 |
| GCP C3 official TEI update | Posted to project tracker | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4553937045 |
| Public OPEA tracker | Posted | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2 |
| PR-ready upstream package | Prepared and locally smoke-tested | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready |
| Upstream PR | Pending fork/write path or maintainer feedback | TBD |

## Knowledge Sharing

| Item | Status | URL |
| --- | --- | --- |
| Technical article | Published in public GitHub repository | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md |
| Technical article issue | Posted | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1 |
| Demo video script | Ready | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/demo-video-script.md |
| Demo video source | Renderable HyperFrames package | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/demo-video |
| Demo video | Published as public raw MP4 asset | https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4 |
| Demo video render report | Local MP4 rendered; public URL verified | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/demo-video-render-report.md |
| Official OPEA TEI profile note | Published; local E2E passed | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md |
| Local OPEA TEI report | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md |
| GCP C3 OPEA TEI report | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md |

## Publication Notes

- The article URL is a public GitHub page in the submitted project repository.
- The RFC issue is the primary OPEA feedback channel until maintainers confirm whether the first contribution should live in `GenAIExamples`, `GenAIComps`, or `docs`.
- The official TEI update is posted directly in `opea-project/GenAIExamples#2461`. The GitHub App still cannot write to the upstream repository, so the browser-authenticated comment is the authoritative upstream evidence.
- The GCP C3 official TEI pass was also posted to the public project tracker after the cloud rerun passed.
- The demo video has a rendered local MP4, committed HyperFrames source package, and public raw GitHub URL on the `codex/video-assets` branch.
- The first PR scope is intentionally small: route registry, Docker Compose,
  Qdrant profile, OPEA embedding profiles, deterministic demo path, scorecard,
  and docs. A copyable PR-ready package is included under
  `docs/opea-upstream/pr-ready/`.
