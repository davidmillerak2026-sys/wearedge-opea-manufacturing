# Public Platform Publishing Handoff

Status: manual external publication selected; public-platform URLs are still
pending.

The repository contains copy-ready materials for the knowledge-sharing bonus,
but a true external platform post still needs to be published on a non-GitHub
public platform such as LinkedIn Articles, Medium, Dev.to, YouTube, Bilibili,
or a public project blog.

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
| External article | `public/external-platform-article.md` | LinkedIn Articles, Medium, Dev.to, public blog |
| Video title/description/tags | `public/video-platform-description.md` | YouTube, Bilibili, LinkedIn video |
| Rendered demo video asset | `renders/wearedge-opea-manufacturing-demo.mp4` | Upload as the public video if present locally |
| GitHub video asset page | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` | Fallback public video evidence |

## Manual Publishing Steps

1. Open one article platform manually:
   LinkedIn Articles, Medium, Dev.to, or a public project blog.
2. Copy the title, subtitle, tags, and article body from
   `public/external-platform-article.md`.
3. Publish the article publicly and copy the final public URL.
4. Open one video platform manually:
   YouTube, Bilibili, or LinkedIn video.
5. Upload `renders/wearedge-opea-manufacturing-demo.mp4` if it is available on
   your machine. If it is not available locally, use the GitHub MP4 asset page
   above as fallback video evidence.
6. Copy the title, description, and tags from
   `public/video-platform-description.md`.
7. Publish the video publicly and copy the final public URL.
8. Send the article URL and video URL back to Codex for repository and form
   backfill.

## After URLs Are Available

Add the resulting public URLs to:

- `docs/publication-record.md`;
- `submission-fields.draft.json`;
- `docs/final-submission-form-fill-guide.md`.

Then re-run:

```powershell
python scripts\evidence_check.py
python -m json.tool submission-fields.draft.json
git diff --check
```

## Browser Automation Status

Manual mode is selected. Chrome automation should not be used for the external
publishing step unless the user explicitly switches back to automation.

## Claim Boundary

Safe to claim now:

```text
The repository contains public GitHub article/video evidence and copy-ready
external article/video publication materials.
```

Do not claim yet:

```text
Published on Medium/LinkedIn/Dev.to/YouTube/Bilibili
```

unless the real external public URL is recorded.
