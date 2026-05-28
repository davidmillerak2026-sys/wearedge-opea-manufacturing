# Public Platform Publishing Handoff

Status: external article published on Dev.to; public video-platform URL is
still pending.

The repository contains copy-ready materials for the knowledge-sharing bonus.
The external technical article is now published on Dev.to:

```text
https://dev.to/ryan_hsu_wearedge/wearedge-pro-an-opea-manufacturing-five-agent-suite-for-frontline-operators-5afh
```

A true external video URL still needs to be published on a non-GitHub public
platform such as YouTube, Bilibili, or LinkedIn video.

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
| Video title/description/tags | `public/video-platform-description.md` | YouTube, Bilibili, LinkedIn video |
| Rendered demo video asset | `renders/wearedge-opea-manufacturing-demo.mp4` | Upload as the public video if present locally |
| GitHub video asset page | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` | Fallback public video evidence |

## Remaining Manual Video Publishing Steps

1. Open one video platform manually:
   YouTube, Bilibili, or LinkedIn video.
2. Upload `renders/wearedge-opea-manufacturing-demo.mp4` if it is available on
   your machine. If it is not available locally, use the GitHub MP4 asset page
   above as fallback video evidence.
3. Copy the title, description, and tags from
   `public/video-platform-description.md`.
4. Publish the video publicly and copy the final public URL.
5. Send the video URL back to Codex for repository and form backfill.

## After URLs Are Available

Add the resulting public video URL to:

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
The repository contains a public Dev.to article, public GitHub article/video
evidence, and copy-ready external video publication materials.
```

Do not claim yet:

```text
Published on YouTube/Bilibili/LinkedIn video
```

unless the real external public URL is recorded.
