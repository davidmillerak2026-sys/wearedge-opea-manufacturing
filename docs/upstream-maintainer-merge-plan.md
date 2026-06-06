# Upstream Maintainer Merge Plan

Date: 2026-06-05

Target PR:

```text
https://github.com/opea-project/GenAIExamples/pull/2462
```

## Current PR State

Checked through the GitHub connector on 2026-06-05:

| Field | State |
| --- | --- |
| PR state | Open |
| Draft | false |
| Merged | false |
| Mergeable | true as of 2026-06-06 API check |
| Head branch | `Ryanhuii/GenAIExamples:codex/wear-edge-manufacturing-suite-pr-ready` |
| Current checked head SHA | `4c4621a690dca0523f8ada32070b4a02b34d61fc` |
| Changed files | 9 |
| Review threads | 0 |
| Review submissions | 0 |
| Visible commit status | key GitHub check runs pass; legacy `pre-commit.ci - pr` currently reports failure |
| PR comments | Dependency Review bot only |

Requested reviewers are already present:

```text
ftian1
lkk12014402
chensuyue
minmin-intel
rbrugaro
lvliang-intel
```

## What Is Blocked

Codex attempted these upstream write actions through the GitHub connector:

| Action | Result |
| --- | --- |
| Comment on `opea-project/GenAIExamples#2462` | `403 Resource not accessible by integration` |
| Re-request reviewers on `opea-project/GenAIExamples#2462` | `403 Resource not accessible by integration` |

This is a GitHub App permission boundary. Local filesystem or terminal
permission does not grant write access to `opea-project/GenAIExamples`.

## How To Give Codex Upstream Write Ability

Use one of these routes:

| Route | What it enables | Requirement |
| --- | --- | --- |
| Browser session | Codex can use the already logged-in GitHub web UI to paste comments or request review | Chrome/GitHub session must be logged in as `Ryanhuii` and able to comment on the PR |
| GitHub CLI user auth | Codex can run `gh pr comment`, `gh pr edit`, and potentially push to the fork | Install `gh`, run `gh auth login`, authorize `public_repo` or equivalent public-repo write access |
| Git push credentials | Codex can update `Ryanhuii/GenAIExamples:codex/wear-edge-manufacturing-suite-pr-ready` | Windows Git credential manager or HTTPS/SSH credentials must be available for `Ryanhuii/GenAIExamples` |
| OPEA org collaborator/maintainer | Codex can help with branch updates and possibly merge, depending on granted role | OPEA org owner or maintainer must grant role on `opea-project/GenAIExamples` |

The fourth route is the only one that can make the final merge button available
to this side. Otherwise, OPEA maintainers must review and merge.

## Maintainer Review Request Text

Use this exact comment when write access is available:

```markdown
Maintainer review request update:

The broader WearEdge OPEA Manufacturing reference package has been further
consolidated after this PR was opened. The latest evidence summary is tracked
here:

https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/issues/2#issuecomment-4631635695

Highlights:

- official OPEA TEI local and GCP C3 evidence
- five-route Manufacturing RAG
- optional reranker profile
- strict local Ollama `gemma4:31b` benchmark with `fallback_count=0`
- strict DeepSeek `deepseek-chat` OpenAI-compatible benchmark with `fallback_count=0`
- official OPEA GenAIEval `chatqnafixed` local benchmark summary with zero failures
- optional Kubernetes manifest

Boundary:

Please review this PR as a minimal CI-friendly GenAIExamples addition. It does
not claim official OPEA publication before merge, and it intentionally excludes
GraphRAG and fine-tuning/SFT/DPO/PPO for this release path.
```

## Merge Readiness Checklist

Before pinging maintainers again:

1. Keep the PR small; do not expand it with GraphRAG, fine-tuning, Helm/GMC, or
   heavy reranker changes.
2. Repair or re-run the legacy `pre-commit.ci - pr` status before saying the PR is fully green.
3. Preserve mergeability if maintainers request updates.
4. Keep `maintainer_can_modify` enabled on the fork PR if the GitHub UI exposes
   that setting.
5. Respond quickly if any requested reviewer leaves comments.
6. Do not claim official OPEA acceptance or publication until the PR is merged.

## Current Recommendation

Do not rewrite the PR unless a maintainer asks for changes. The PR is already
small, review-requested, and CI-friendly in its key GitHub check runs; legacy
pre-commit status still needs repair before claiming fully green. The next useful action is
to post the maintainer review request comment above through a GitHub identity
that has upstream comment permission, then wait for reviewer feedback.
