# Demo Video Render Report

Date: 2026-05-27

Status: local render complete; external upload URL still pending.

## Rendered Asset

```text
renders/wearedge-opea-manufacturing-demo.mp4
```

The rendered `.mp4` is intentionally excluded from git by `.gitignore`.
Upload this file to a public video host before final form submission and replace
`bonus_urls.demo_video_url` in `submission-fields.draft.json`.

## Source Package

| File | Purpose |
| --- | --- |
| `public/demo-video/DESIGN.md` | Visual identity, palette, typography, motion rules, and claim guardrails |
| `public/demo-video/index.html` | HyperFrames composition source |
| `public/demo-video/README.md` | Render instructions |
| `public/demo-video-script.md` | Narration and shot list |
| `public/demo-video-captions.srt` | Caption timing source |

## Validation Commands

Executed from `public/demo-video`:

```powershell
npx --yes hyperframes@0.6.7 lint
$env:HYPERFRAMES_BROWSER_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_HEADLESS_SHELL_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_PUPPETEER_LAUNCH_TIMEOUT_MS='120000'
npx --yes hyperframes@0.6.7 validate
npx --yes hyperframes@0.6.7 inspect --samples 14 --json
```

Validation result:

```text
validate: No console errors; 1218 text elements pass WCAG AA
inspect: ok=true, errorCount=0, warningCount=0, issueCount=0
```

The only remaining lint warning is `composition_file_too_large`, which is a
maintainability warning and does not block rendering.

## Render Command

Executed from `public/demo-video`:

```powershell
$env:Path='C:\Users\ryan hui\Documents\Codex\2026-05-15\hyperframe\node_modules\@ffmpeg-installer\win32-x64;C:\Users\ryan hui\Documents\Codex\2026-05-15\hyperframe\node_modules\@ffprobe-installer\win32-x64;' + $env:Path
$env:HYPERFRAMES_BROWSER_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_HEADLESS_SHELL_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_PUPPETEER_LAUNCH_TIMEOUT_MS='120000'
npx --yes hyperframes@0.6.7 render --output ..\..\renders\wearedge-opea-manufacturing-demo.mp4 --quality standard --fps 30
```

## Media Metadata

Verified with `ffprobe`:

```json
{
  "video": {
    "width": 1920,
    "height": 1080,
    "frame_rate": "30/1",
    "frames": 4200
  },
  "format": {
    "duration_seconds": 140.0,
    "size_bytes": 16135620
  }
}
```

## Visual QA

Extracted key frames at 00:00:05, 00:01:05, and 00:01:55. The title and hazard
frames are readable and framed correctly; the 00:01:05 sample lands during a
scene transition, confirming the mechanical shutter transition renders.
