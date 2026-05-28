# Public Platform Publishing Handoff

Status: external article published on Dev.to; external demo video published on
YouTube.

The repository contains copy-ready materials for the knowledge-sharing bonus.
The external technical article is now published on Dev.to:

```text
https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh
```

The external demo video is now published on YouTube:

```text
https://www.youtube.com/watch?v=dd9k8m6PDco
```

## Why This Matters

The challenge bonus says:

```text
Knowledge Sharing: Technical articles, blogs, or videos on public platforms.
```

Current GitHub-hosted article and video assets are public and useful evidence,
but the strongest interpretation of this bonus is an external public article
and/or video URL that judges can open directly outside the repository.

## Ready-To-Publish Materials

| Material | Path | Intended platform |
| --- | --- | --- |
| External article | `public/external-platform-article.md` | Published on Dev.to |
| Video title/description/tags | `public/video-platform-description.md` | Published via YouTube |
| Rendered demo video asset | `renders/wearedge-opea-manufacturing-demo.mp4` | Upload as the public video if present locally |
| GitHub video asset page | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` | Fallback public video evidence |

## Published Public Platform URLs

| Item | URL |
| --- | --- |
| External article | `https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh` |
| External video | `https://www.youtube.com/watch?v=dd9k8m6PDco` |

## After URLs Are Available

The public article and video URLs have been backfilled into:

- `docs/publication-record.md`;
- `submission-fields.draft.json`;
- `docs/final-submission-form-fill-guide.md`.

Verification commands:

```powershell
python scripts\evidence_check.py
python -m json.tool submission-fields.draft.json
git diff --check
```

## Browser Automation Status

Manual mode was selected for publication. Chrome automation is no longer needed
for the external publishing step.

## Claim Boundary

Safe to claim now:

```text
The repository contains a public Dev.to article, a public YouTube demo video,
and GitHub article/video backup evidence.
```

Do not claim additional public platforms, such as Medium, LinkedIn, or Bilibili,
unless those URLs are also published and recorded.
