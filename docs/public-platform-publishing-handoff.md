# Public Platform Publishing Handoff

Status: external public-platform URLs are still pending.

The repository now contains copy-ready materials for the knowledge-sharing
bonus, but a true external platform post still needs to be published on a
non-GitHub public platform such as LinkedIn Articles, Medium, Dev.to, YouTube,
Bilibili, or a public project blog.

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
| Rendered demo video asset | `renders/wearedge-opea-manufacturing-demo.mp4` | Upload as the public video |
| GitHub video asset page | `https://github.com/davidmillerak2026-sys/wearedge-opea-manufacturing/blob/codex/video-assets/renders/wearedge-opea-manufacturing-demo.mp4` | Fallback public video evidence |

## Recommended Fastest Path

1. Publish `public/external-platform-article.md` as a LinkedIn Article.
2. Upload `renders/wearedge-opea-manufacturing-demo.mp4` to YouTube or Bilibili
   using `public/video-platform-description.md`.
3. Add the resulting public URLs to:
   - `docs/publication-record.md`
   - `submission-fields.draft.json`
   - `docs/final-submission-form-fill-guide.md`
4. Re-run:

```powershell
python scripts\evidence_check.py
python -m json.tool submission-fields.draft.json
git diff --check
```

## Current Browser Automation Status

Chrome automation was attempted for this publishing step, but the local Codex
Chrome connector failed before it could list or control tabs. The failure is in
the local browser automation layer, not in the WearEdge repository or the
submission evidence.

Until the Chrome connector is repaired, publication should be done manually in
Chrome, or retried after reinstalling or repairing the Codex Chrome plugin from
the Codex plugin UI.

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
