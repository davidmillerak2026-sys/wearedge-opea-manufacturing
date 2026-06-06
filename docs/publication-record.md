# Publication Record

This file records public URLs that support the OPEA ecosystem public evidence.

## OPEA Upstream

| Item | Status | URL |
| --- | --- | --- |
| RFC issue | Posted | https://github.com/opea-project/GenAIExamples/issues/2461 |
| Implementation feedback comment | Posted upstream | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4551375202 |
| Official TEI update comment | Posted upstream | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017 |
| GCP C3 official TEI update | Posted to project tracker | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4553937045 |
| Public OPEA tracker | Posted | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2 |
| Upstream contribution package | Prepared and locally smoke-tested | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/docs/opea-upstream/pr-ready |
| Upstream PR | Open against `opea-project/GenAIExamples:main`; key check runs pass on the current PR head; not merged yet | https://github.com/opea-project/GenAIExamples/pull/2462 |
| OPEA Publications PR | Open against `opea-project/docs:main`; DCO passes; not merged yet | https://github.com/opea-project/docs/pull/395 |
| Upstream PR attempt log | Direct upstream push failed with GitHub 403, then fork push succeeded and PR #2462 was opened | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/upstream-pr-attempt-2026-05-28.md |

## Knowledge Sharing

| Item | Status | URL |
| --- | --- | --- |
| External technical article | Published on Dev.to | https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh |
| Technical article backup | Published in public GitHub repository | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-wear-edge-opea-manufacturing.md |
| External-platform article package | Published via Dev.to; source package retained | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/external-platform-article.md |
| OPEA practical article | Published as a public GitHub issue; source retained in repo | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/3 |
| OPEA practical article source | Ready in public repository as the source copy | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/article-opea-tei-qdrant-guardrails-lessons.md |
| OPEA Publications blog-listing PR | Proposed for the official OPEA Publications page; open and not merged yet | https://github.com/opea-project/docs/pull/395 |
| External-platform publishing handoff | Ready; manual publish selected | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/public-platform-publishing-handoff.md |
| Technical article issue | Posted | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/1 |
| Product walkthrough video script | Ready | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/product-walkthrough-script.md |
| Product walkthrough video source | Renderable HyperFrames package | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main/public/product-walkthrough |
| YouTube product walkthrough video | Published on YouTube | https://www.youtube.com/watch?v=dd9k8m6PDco |
| Product walkthrough video backup | Published as public MP4 asset page | https://www.youtube.com/watch?v=dd9k8m6PDco |
| Public video platform metadata | Published via YouTube; source package retained | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/public/video-platform-description.md |
| Product walkthrough render report | Local MP4 rendered; public URL verified | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/product-walkthrough-render-report.md |
| Final form fill guide | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/project-profile-fill-guide.md |
| Official OPEA TEI profile note | Published; local E2E passed | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-opea-tei-profile.md |
| Local OPEA TEI report | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-opea-tei-profile-e2e-report.md |
| GCP C3 OPEA TEI report | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/gcp-c3-opea-tei-profile-e2e-report.md |
| Local Docker Desktop final validation | Published in repository docs | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/local-docker-desktop-final-validation.md |

## Publication Notes

- The primary article URL is now the public Dev.to article; the GitHub article
  remains as repository backup evidence.
- The Dev.to article is a technical article, not only a marketing post: it
  covers the five-agent route registry, OPEA architecture, Qdrant RAG, official
  TEI profile, guardrails, evaluation, and Intel evidence.
- The additional OPEA practical article is published as public issue #3 and
  covers OPEA TEI, Qdrant, five-agent guardrails, source VLM evidence, and
  recommendations back to OPEA.
- OPEA docs PR #395 proposes adding the Dev.to article to the official OPEA
  Publications / Blogs list. It is open, but not merged yet, so
  do not claim official OPEA publication until the PR is merged.
- `docs/public-platform-publishing-handoff.md` records the exact remaining
  non-GitHub publication task for manual posting.
- The RFC issue is the primary OPEA feedback channel until maintainers confirm whether the first contribution should live in `GenAIExamples`, `GenAIComps`, or `docs`.
- The official TEI update is posted directly in `opea-project/GenAIExamples#2461`; it was verified through the GitHub API as comment `4554039017` by `Ryanhuii`.
- A direct upstream PR push was attempted and rejected with `403 Permission denied`; after the fork was created, the prepared branch was pushed to `Ryanhuii/GenAIExamples` and real upstream PR #2462 was opened.
- Current PR head `e47ebb3bf363ecc15563bb8d05ab4c65f88e2268` has combined status success, with `pre-commit.ci - pr`, DCO, dependency-review, get-test-matrix, get-test-case, and compose-test passing. The PR is still open and not merged, so do not claim maintainer acceptance yet.
- The GCP C3 official TEI pass was also posted to the public project tracker after the cloud rerun passed.
- The product walkthrough video is published on YouTube; the rendered MP4, committed
  HyperFrames source package, and public GitHub asset page remain as backup
  evidence.
- The first upstream PR scope is intentionally small: route registry, Docker Compose,
  Qdrant profile, OPEA embedding profiles, deterministic sample path, scorecard,
  and docs. A copyable contribution package is included under
  `docs/opea-upstream/pr-ready/`.
