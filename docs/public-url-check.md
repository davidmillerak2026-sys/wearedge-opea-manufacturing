# Public URL Availability Check

Date: 2026-06-06

Source of truth: `project-profile.json`, `docs/project-profile-fill-guide.md`,
and current public submission links.

Result: pass for link availability. All checked public URLs returned HTTP 200
with `Invoke-WebRequest -Method Head -MaximumRedirection 5`.

Current release reference:

```text
https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/final-submission-2026-06-06-r30
```

The frozen tag is created after this audit commit and should resolve to the
same commit that contains this report. Verify with:

```text
git ls-remote --tags origin "refs/tags/final-submission-2026-06-06-r30*"
```

## Checked URLs

| HTTP | URL |
| --- | --- |
| 200 | https://competition.aiforgood.itu.int/web/challenges/challenge-page/492/project |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/main |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/tree/final-submission-2026-06-06-r30 |
| 200 | https://raw.githubusercontent.com/davidmillerak2026-sys/wearedge-opea-manufacturing/main/public/images/wearedge-smart-inspection-waist-mount.png |
| 200 | https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh |
| 200 | https://www.youtube.com/watch?v=dd9k8m6PDco |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461 |
| 200 | https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017 |
| 200 | https://github.com/opea-project/GenAIExamples/pull/2462 |
| 200 | https://github.com/opea-project/docs/pull/395 |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/official-genaieval-benchmark.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/genaieval/official_benchmark_summary.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/evidence/benchmarks/llm_adapter.local-gemma.json |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/opea-reranker-profile.md |
| 200 | https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/main/docs/kubernetes-optional-profile.md |

## Current PR Status Boundary

Checked: 2026-06-06T10:24:31+08:00.

| PR | State | Merged | Current head | Status boundary |
| --- | --- | --- | --- | --- |
| https://github.com/opea-project/GenAIExamples/pull/2462 | open | no | `4c4621a690dca0523f8ada32070b4a02b34d61fc` | DCO, dependency-review, get-test-matrix, get-test-case, and compose-test check runs pass; combined status is `failure` because legacy `pre-commit.ci - pr` reports failure. Do not describe the PR as fully green. |
| https://github.com/opea-project/docs/pull/395 | open | no | `9c2e259764ab05f8a2c9fe69fa7c186201523b9f` | DCO check run passes; combined status is `pending`. Do not claim official OPEA publication until merged. |

## Notes

- This file verifies public link availability and current public PR state. It
  does not claim maintainer acceptance, official OPEA publication, or merged
  upstream contribution.
- The primary runnable evaluation path remains the repository `main` branch and
  the frozen `final-submission-2026-06-06-r30` tag.
- The physical hardware image is checked through the raw GitHub URL so the
  README-rendered asset is covered by this audit.
