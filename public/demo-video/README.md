# WearEdge OPEA Demo Video

This folder contains a renderable HyperFrames composition for the final ITU AI
for Good / OPEA Manufacturing submission video.

## Composition

| File | Purpose |
| --- | --- |
| `DESIGN.md` | Visual identity and claim guardrails |
| `index.html` | 140-second 1920x1080 HyperFrames composition |
| `../demo-video-script.md` | Shot list and narration source |
| `../demo-video-captions.srt` | Subtitle timing source |

## Render

From this folder:

```bash
npx --yes hyperframes@0.6.7 lint
npx --yes hyperframes@0.6.7 validate
npx --yes hyperframes@0.6.7 inspect --samples 14 --json
npx --yes hyperframes@0.6.7 render --output ..\\..\\renders\\wearedge-opea-manufacturing-demo.mp4 --quality standard --fps 30
```

The rendered `.mp4` is intentionally ignored by git. Upload it externally and
put the public URL into `submission-fields.draft.json` under
`bonus_urls.demo_video_url`.

## Narrative

The video presents WearEdge Pro as a Docker-runnable OPEA Manufacturing
Five-Agent Suite rather than an Android-only submission. It shows the shared
Gateway/Megaservice/RAG/Guardrails architecture, the five route registry, the
maintenance hero action card, the other four manufacturing agents, the official
OPEA TEI profile, and the final scorecard/evidence set.
