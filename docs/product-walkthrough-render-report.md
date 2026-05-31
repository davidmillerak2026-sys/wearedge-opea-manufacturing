# Product Walkthrough Render Report

Date: 2026-05-27

Status: local render complete; public GitHub raw video URL verified.

## Rendered Asset

```text
renders/wearedge-opea-manufacturing-product-walkthrough.mp4
```

The rendered `.mp4` is intentionally excluded from git by `.gitignore`.
The published product walkthrough is hosted on YouTube:

```text
https://www.youtube.com/watch?v=dd9k8m6PDco
```

This URL was verified with `curl -I -L` and returned `HTTP/1.1 200 OK` with
`Content-Length: 16135620`.

## Source Package

| File | Purpose |
| --- | --- |
| `public/product-walkthrough/DESIGN.md` | Visual identity, palette, typography, motion rules, and claim guardrails |
| `public/product-walkthrough/index.html` | HyperFrames composition source |
| `public/product-walkthrough/README.md` | Render instructions |
| `public/product-walkthrough-script.md` | Narration and shot list |
| `public/product-walkthrough-captions.srt` | Caption timing source |

## Validation Commands

Executed from `public/product-walkthrough`:

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

Executed from `public/product-walkthrough`:

```powershell
$env:Path='<local-ffmpeg-bin>;<local-ffprobe-bin>;' + $env:Path
$env:HYPERFRAMES_BROWSER_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_HEADLESS_SHELL_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
$env:PRODUCER_PUPPETEER_LAUNCH_TIMEOUT_MS='120000'
npx --yes hyperframes@0.6.7 render --output ..\..\renders\wearedge-opea-manufacturing-product-walkthrough.mp4 --quality standard --fps 30
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
