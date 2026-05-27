# WearEdge OPEA Demo Video Design

## Style Prompt

Industrial evidence-room motion system for a manufacturing AI competition demo.
The video should feel like a serious plant-floor control package: precise,
dense, verifiable, and ready for technical judges. It should not look like a
marketing landing page. The visual language uses machine-console panels,
route-isolated evidence lanes, scorecard readouts, and bounded action cards.

## Colors

| Role | Hex | Usage |
| --- | --- | --- |
| Background | `#101414` | Deep graphite canvas |
| Panel | `#18201f` | Console and API surfaces |
| Panel Alt | `#202927` | Evidence blocks and route strips |
| Primary Text | `#edf4ef` | Headlines and key labels |
| Secondary Text | `#aebbb4` | Captions and body copy |
| OPEA Teal | `#50d8bc` | Pipeline, pass states, RAG evidence |
| Copper | `#c98f55` | Manufacturing warmth and action cards |
| Safety Amber | `#f0bf4c` | Human-confirmation and guardrail markers |
| Critical Red | `#e36a5f` | Blocked claims and safety risk |

## Typography

- Display: `Archivo Black`, fallback `Arial Black`, sans-serif.
- Body: `IBM Plex Sans`, fallback `Arial`, sans-serif.
- Data/code: `IBM Plex Mono`, fallback `Consolas`, monospace.
- Use high contrast between display and data. Body text must stay at 24px or
  larger for rendered readability.

## Motion

- Medium-energy technical explainer.
- Primary transition: full-frame mechanical shutter bars, 0.42s.
- Accent transition: wider copper/teal split before the maintenance hero and
  final scorecard.
- Every scene has entrance motion. No content exits before a transition.
- Ambient movement is subtle: slow scan lines and route pulses only.

## What NOT to Do

- No purple/blue gradient hero.
- No decorative orbs, bokeh, or generic AI blobs.
- No rounded landing-page cards; panels use 8px radius or less.
- No claims of autonomous restart, safety clearance, product release, final root
  cause, or production LLM acceleration.
- No dense paragraph walls; show evidence as structured UI.
