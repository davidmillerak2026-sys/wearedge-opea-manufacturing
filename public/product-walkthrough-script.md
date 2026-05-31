# Product Walkthrough Script

Target length: 2 minutes 20 seconds

Title: `WearEdge Pro: Five OPEA Manufacturing Agents`

## Shot List

| Time | Visual | Narration |
| --- | --- | --- |
| 0:00-0:10 | Title, OPEA-aligned architecture, five route names | "WearEdge Pro is an OPEA-aligned manufacturing agent suite. One Gateway and Megaservice power five plant-floor workflows." |
| 0:10-0:25 | Architecture flow: Gateway, Megaservice, Dataprep, RAG, LLM, evaluator, guardrails | "The architecture follows the same pipeline for every route: evidence enters the Gateway, the Megaservice selects a route, RAG retrieves source evidence, and guardrails produce a bounded action card." |
| 0:25-0:45 | `GET /v1/agents` output with five modes | "The route registry exposes maintenance, IQC, changeover, work instruction, and hazard agents through one API." |
| 0:45-1:05 | Maintenance sample action card | "Maintenance is the hero scenario. Gearbox vibration, temperature, lubrication interval, PLC alarm, and operator observation become a CMMS-ready work-order proposal, but final root cause and restart permission stay blocked." |
| 1:05-1:20 | IQC sample action card | "The IQC route turns defect evidence on an aluminum housing into a QMS quality event and blocks unsupported product release." |
| 1:20-1:35 | Changeover sample action card | "The changeover route checks SKU setup evidence and holds restart until first-piece sign-off is recorded." |
| 1:35-1:50 | WI sample action card | "The work-instruction route answers from released source instructions and blocks unreleased instructions or interlock bypass guidance." |
| 1:50-2:05 | Hazard sample action card | "The hazard route detects blocked walkways, PPE gaps, or moving-parts exposure and creates an EHS observation without claiming the area is safe." |
| 2:05-2:20 | Scorecard endpoint showing all pass | "The scorecard verifies latency, contract pass, guardrails, source match, action target correctness, and route isolation for all five routes." |

## Recording Commands

Run the service:

```bash
docker compose up --build -d
```

Capture the route registry:

```bash
curl http://127.0.0.1:8088/v1/agents
```

Capture samples:

```bash
curl http://127.0.0.1:8088/v1/agents/maintenance/demo
curl http://127.0.0.1:8088/v1/agents/iqc/demo
curl http://127.0.0.1:8088/v1/agents/changeover/demo
curl http://127.0.0.1:8088/v1/agents/wi/demo
curl http://127.0.0.1:8088/v1/agents/hazard/demo
curl http://127.0.0.1:8088/v1/scorecard
```

## Caption File

Use `public/product-walkthrough-captions.srt` as the initial subtitle file.
