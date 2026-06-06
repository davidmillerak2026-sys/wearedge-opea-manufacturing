# Upstream OPEA PR Attempt

Date: 2026-05-28

## Result

A real upstream PR is now open:

```text
https://github.com/opea-project/GenAIExamples/pull/2462
```

Historical note: the PR had passing key checks on head `0c149a06eab8b53713e0bd208c5caa1ed58ee7a4`.
Current public PR status is tracked in `docs/public-url-check.md`.
DCO, pre-commit.ci, dependency-review, get-test-matrix, get-test-case, and
compose-test all passed on 2026-05-28.

The first direct push to `opea-project/GenAIExamples` failed because the current
GitHub account did not have write permission. After the fork was created under
`Ryanhuii/GenAIExamples`, the prepared branch was pushed to the fork and PR
`#2462` was opened against `opea-project:main`.

## What Was Tested

Local upstream branch:

```text
GenAIExamples-opea
branch: wear-edge-manufacturing-suite-pr-ready
commit: f5ea17a Add ManufacturingAgentSuite example
```

Direct push attempt:

```bash
git push origin wear-edge-manufacturing-suite-pr-ready
```

GitHub response:

```text
remote: Permission to opea-project/GenAIExamples.git denied to Ryanhuii.
fatal: unable to access 'https://github.com/opea-project/GenAIExamples.git/': The requested URL returned error: 403
```

Initial fork checks before the fork existed:

```text
https://github.com/davidmillerak2026-sys/GenAIExamples.git -> repository not found
https://github.com/Ryanhuii/GenAIExamples.git -> repository not found
https://github.com/ryanhuii/GenAIExamples.git -> repository not found
```

Fork push:

```bash
git remote add fork https://github.com/Ryanhuii/GenAIExamples.git
git push fork wear-edge-manufacturing-suite-pr-ready
```

Push result:

```text
To https://github.com/Ryanhuii/GenAIExamples.git
 * [new branch] wear-edge-manufacturing-suite-pr-ready -> wear-edge-manufacturing-suite-pr-ready
```

Opened PR:

```text
number=2462
state=open
head=Ryanhuii:wear-edge-manufacturing-suite-pr-ready
head_sha=0c149a06eab8b53713e0bd208c5caa1ed58ee7a4
base=opea-project:main
title=Add ManufacturingAgentSuite example
url=https://github.com/opea-project/GenAIExamples/pull/2462
```

CI repair:

```text
DCO: success after adding Signed-off-by: Ryan Hui <ryan.on2008@gmail.com>
compose-test: success after the test script was changed to start Docker Compose
pre-commit.ci: success after docformatter was pinned to Python 3.12 and pre-commit.ci applied autofixes
```

## Current Upstream Evidence

The upstream RFC and TEI update comment are posted:

```text
https://github.com/opea-project/GenAIExamples/issues/2461
https://github.com/opea-project/GenAIExamples/issues/2461#issuecomment-4554039017
https://github.com/opea-project/GenAIExamples/pull/2462
```

The TEI update comment was verified through the GitHub API on 2026-05-28:

```text
comment_id=4554039017
user=Ryanhuii
created_at=2026-05-27T11:18:57Z
```

## Remaining Status

The PR is open with key check-run evidence, but not merged. Do not claim it has been accepted
upstream until OPEA maintainers merge it.

The generated patch remains available as a fallback artifact:

```text
docs/opea-upstream/pr-ready/0001-add-manufacturing-agent-suite.patch
```
