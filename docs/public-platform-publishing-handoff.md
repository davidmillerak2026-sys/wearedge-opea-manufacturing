# Public Platform Publishing Handoff

Status: external article published on Dev.to; complete OPEA demo video and
external product walkthrough video published on YouTube; OPEA docs Publications
PR #395 open but not merged.

The repository contains ready-to-use materials for the knowledge-sharing evidence.
The external technical article is now published on Dev.to:

```text
https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh
```

The external product walkthrough video is now published on YouTube:

```text
https://www.youtube.com/watch?v=dd9k8m6PDco
```

The complete OPEA demo video is also published on YouTube:

```text
https://youtu.be/ID8QPYhhhtk
```

The article has also been released to the OPEA docs Publications / Blogs list:

```text
https://github.com/opea-project/docs/pull/395
```

## Why This Matters

The public evidence says:

```text
Knowledge Sharing: Technical articles, blogs, or videos on public platforms.
```

Current GitHub-hosted article and video assets are public and useful evidence,
but the strongest interpretation of this evidence is an external public article
and/or video URL that evaluators can open directly outside the repository.

## Ready-To-Publish Materials

| Material | Path | Intended platform |
| --- | --- | --- |
| External article | `public/external-platform-article.md` | Published on Dev.to |
| Video title/description/tags | `public/video-platform-description.md` | Published via YouTube |
| Rendered product walkthrough video asset | `renders/wearedge-opea-manufacturing-product-walkthrough.mp4` | Upload as the public video if present locally |
| Complete OPEA demo cover image | `public/images/wearedge-pro-complete-opea-demo-cover.png` | Published in README as the clickable YouTube entry |
| GitHub video asset page | `https://www.youtube.com/watch?v=dd9k8m6PDco` | Fallback public video evidence |

## Published Public Platform URLs

| Item | URL |
| --- | --- |
| External article | `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh` |
| Complete OPEA demo video | `https://youtu.be/ID8QPYhhhtk` |
| External video | `https://www.youtube.com/watch?v=dd9k8m6PDco` |
| OPEA Publications PR | `https://github.com/opea-project/docs/pull/395` |

## After URLs Are Available

The public article, video, and OPEA Publications PR URLs have been backfilled
into:

- `docs/publication-record.md`;
- `project-profile.json`;
- `docs/project-profile-fill-guide.md`.

Verification commands:

```powershell
python scripts\evidence_check.py
python -m json.tool project-profile.json
git diff --check
```

## Browser Automation Status

Manual mode was selected for publication. Chrome automation is no longer needed
for the external publishing step.

## Claim Boundary

Safe to claim now:

```text
The repository contains a public Dev.to article, a public complete OPEA demo
video, a public YouTube product walkthrough video, an open OPEA docs
Publications PR, and GitHub article/video backup evidence.
```

Do not claim official OPEA Publications listing until PR #395 is merged. Do not
claim additional public platforms, such as Medium, LinkedIn, or Bilibili, unless
those URLs are also published and recorded.
