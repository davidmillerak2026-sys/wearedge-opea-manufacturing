# SPDX-License-Identifier: MIT

from __future__ import annotations


def build_demo_console_html() -> str:
    return _HTML


_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WearEdge Pro OPEA Manufacturing Console</title>
  <style>
    :root {
      --bg: #0d1110;
      --rail: #121815;
      --panel: #171f1c;
      --panel-2: #1f2824;
      --panel-3: #25312b;
      --line: #33423a;
      --line-strong: #5b7466;
      --text: #f5f2e9;
      --muted: #a8b7ae;
      --dim: #73827a;
      --green: #65d47f;
      --cyan: #57c7dd;
      --amber: #f0b957;
      --red: #ef6a63;
      --violet: #a78bfa;
      --ink: #07100a;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        linear-gradient(90deg, rgba(101, 212, 127, 0.05) 1px, transparent 1px),
        linear-gradient(0deg, rgba(101, 212, 127, 0.04) 1px, transparent 1px),
        var(--bg);
      background-size: 44px 44px, 44px 44px, auto;
      color: var(--text);
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      letter-spacing: 0;
    }

    button { font: inherit; }

    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 312px minmax(0, 1fr);
    }

    aside {
      min-width: 0;
      border-right: 1px solid var(--line);
      background: rgba(18, 24, 21, 0.97);
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .brand {
      display: grid;
      grid-template-columns: 52px 1fr;
      gap: 14px;
      align-items: center;
      min-height: 58px;
    }

    .mark {
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      border: 2px solid var(--green);
      background: #102018;
      color: var(--green);
      font-weight: 900;
      border-radius: 8px;
      box-shadow: inset 0 0 0 1px rgba(101, 212, 127, 0.24);
    }

    .brand-title {
      font-size: 20px;
      font-weight: 820;
      line-height: 1.14;
    }

    .brand-sub {
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }

    .system-badge {
      border: 1px solid var(--line-strong);
      background: #102018;
      border-radius: 8px;
      padding: 12px;
      color: #dff8e7;
      font-size: 13px;
      line-height: 1.42;
    }

    .system-badge b {
      display: block;
      margin-bottom: 5px;
      color: var(--green);
      font-size: 12px;
      text-transform: uppercase;
    }

    .mode-list {
      display: grid;
      gap: 9px;
    }

    .mode-button {
      width: 100%;
      min-height: 66px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--text);
      text-align: left;
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
      display: grid;
      gap: 6px;
      transition: border-color 150ms ease, background 150ms ease, transform 150ms ease;
    }

    .mode-button:hover { transform: translateY(-1px); border-color: var(--line-strong); }

    .mode-button.active {
      border-color: var(--green);
      background: #1a2b21;
      box-shadow: inset 3px 0 0 var(--green);
    }

    .mode-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .mode-name {
      font-weight: 820;
      font-size: 15px;
      text-transform: uppercase;
    }

    .mode-pill {
      border: 1px solid var(--line);
      color: var(--muted);
      padding: 3px 6px;
      border-radius: 999px;
      font-size: 11px;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      white-space: nowrap;
    }

    .mode-target {
      color: var(--muted);
      font-size: 12px;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      overflow-wrap: anywhere;
    }

    .side-note {
      margin-top: auto;
      border-top: 1px solid var(--line);
      padding-top: 15px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }

    main {
      min-width: 0;
      display: grid;
      grid-template-rows: auto auto auto 1fr;
    }

    header {
      padding: 22px 28px 18px;
      border-bottom: 1px solid var(--line);
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      background: rgba(13, 17, 16, 0.86);
    }

    h1 {
      margin: 0;
      font-size: 28px;
      line-height: 1.12;
      font-weight: 860;
    }

    .header-copy {
      margin-top: 7px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
      max-width: 960px;
    }

    .actions {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .primary,
    .secondary {
      min-height: 42px;
      border-radius: 8px;
      padding: 0 14px;
      cursor: pointer;
      white-space: nowrap;
    }

    .primary {
      border: 1px solid var(--green);
      background: var(--green);
      color: var(--ink);
      font-weight: 820;
    }

    .secondary {
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--text);
    }

    .mission-strip {
      padding: 14px 28px;
      border-bottom: 1px solid var(--line);
      display: grid;
      grid-template-columns: repeat(5, minmax(136px, 1fr));
      gap: 10px;
      background: rgba(18, 24, 21, 0.62);
    }

    .metric {
      min-height: 76px;
      padding: 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }

    .metric-label {
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 820;
    }

    .metric-value {
      margin-top: 8px;
      font-size: 18px;
      font-weight: 820;
      line-height: 1.2;
    }

    .metric-code {
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 13px;
      overflow-wrap: anywhere;
    }

    .pipeline {
      padding: 13px 28px;
      border-bottom: 1px solid var(--line);
      display: grid;
      grid-template-columns: repeat(8, minmax(82px, 1fr));
      gap: 8px;
    }

    .stage {
      min-height: 54px;
      padding: 9px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(31, 40, 36, 0.78);
      display: grid;
      align-content: center;
      gap: 3px;
    }

    .stage b {
      font-size: 12px;
      color: var(--text);
    }

    .stage span {
      color: var(--muted);
      font-size: 11px;
      line-height: 1.25;
    }

    .workspace {
      min-height: 0;
      padding: 22px 28px 28px;
      display: grid;
      grid-template-columns: minmax(360px, 0.9fr) minmax(480px, 1.1fr);
      gap: 18px;
      overflow: auto;
    }

    section {
      min-width: 0;
      background: rgba(23, 31, 28, 0.96);
      border: 1px solid var(--line);
      border-radius: 8px;
    }

    .panel-header {
      min-height: 54px;
      padding: 13px 15px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .panel-title {
      font-size: 13px;
      font-weight: 840;
      text-transform: uppercase;
      color: var(--muted);
    }

    .muted {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }

    .panel-body {
      padding: 15px;
    }

    pre {
      margin: 0;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 12px;
      line-height: 1.42;
      color: #d9ece0;
    }

    .stack {
      min-width: 0;
      display: grid;
      gap: 16px;
      align-content: start;
    }

    .action-card {
      display: grid;
      gap: 14px;
    }

    .card-main {
      font-size: 22px;
      font-weight: 860;
      line-height: 1.24;
    }

    .card-action {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.48;
    }

    .facts {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .fact {
      padding: 10px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      border-radius: 8px;
      min-height: 60px;
    }

    .fact b {
      display: block;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    .fact span {
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 13px;
      overflow-wrap: anywhere;
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .chip {
      padding: 6px 8px;
      border-radius: 999px;
      border: 1px solid rgba(239, 106, 99, 0.45);
      color: #ffd6d3;
      background: rgba(239, 106, 99, 0.12);
      font-size: 12px;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
    }

    .source-list,
    .score-list {
      display: grid;
      gap: 10px;
    }

    .source,
    .score-row {
      padding: 11px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      border-radius: 8px;
    }

    .source-title,
    .score-title {
      font-weight: 820;
      margin-bottom: 5px;
    }

    .source-score {
      color: var(--cyan);
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 12px;
      margin-left: 6px;
    }

    .source-text,
    .score-text {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.44;
    }

    .lineage-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .lineage-item {
      min-height: 74px;
      padding: 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-2);
    }

    .lineage-item b {
      display: block;
      margin-bottom: 6px;
      font-size: 12px;
      color: var(--text);
    }

    .lineage-item span {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }

    .ok { color: var(--green); }
    .warn { color: var(--amber); }
    .info { color: var(--cyan); }
    .risk-high { color: var(--red); }
    .risk-medium { color: var(--amber); }
    .risk-low { color: var(--green); }

    @media (max-width: 1120px) {
      .shell { grid-template-columns: 1fr; }
      aside { border-right: 0; border-bottom: 1px solid var(--line); }
      .mode-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .mission-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .pipeline { grid-template-columns: repeat(4, minmax(0, 1fr)); }
      .workspace { grid-template-columns: 1fr; }
      header { grid-template-columns: 1fr; }
      .actions { justify-content: flex-start; }
    }

    @media (max-width: 680px) {
      aside, header, .mission-strip, .pipeline, .workspace { padding-left: 16px; padding-right: 16px; }
      .mode-list, .mission-strip, .pipeline, .facts, .lineage-grid { grid-template-columns: 1fr; }
      h1 { font-size: 24px; }
      .card-main { font-size: 19px; }
    }
  </style>
</head>
<body data-supported-modes="maintenance,iqc,changeover,wi,hazard">
  <div class="shell">
    <aside>
      <div class="brand">
        <div class="mark">WE</div>
        <div>
          <div class="brand-title">WearEdge Pro</div>
          <div class="brand-sub">Real industrial AI agent system, packaged for OPEA Manufacturing</div>
        </div>
      </div>
      <div class="system-badge">
        <b>Production lineage</b>
        M400 frontline evidence, Jetson edge gateway, private customer production data, and a reproducible OPEA judge package.
      </div>
      <div class="mode-list" id="modeList"></div>
      <div class="side-note">
        Judge-facing product: Docker + Web Console + API + scorecard. Real deployment front end: Vuzix M400 / Android from WearEdge-Pro.
      </div>
    </aside>
    <main>
      <header>
        <div>
          <h1>Manufacturing Demo Console</h1>
          <div class="header-copy">
            Five industrial agents run through one OPEA-aligned Gateway, Manufacturing Megaservice, Dataprep, RAG, LLM adapter, evaluator, guardrail, and action-card contract.
          </div>
        </div>
        <div class="actions">
          <button class="secondary" id="scorecardButton">Refresh Scorecard</button>
          <button class="primary" id="runButton">Run Selected Agent</button>
        </div>
      </header>

      <div class="mission-strip">
        <div class="metric"><div class="metric-label">Selected Agent</div><div class="metric-value metric-code" id="summaryMode">-</div></div>
        <div class="metric"><div class="metric-label">Risk</div><div class="metric-value" id="summaryRisk">-</div></div>
        <div class="metric"><div class="metric-label">Owner</div><div class="metric-value metric-code" id="summaryOwner">-</div></div>
        <div class="metric"><div class="metric-label">Action Target</div><div class="metric-value metric-code" id="summaryTarget">-</div></div>
        <div class="metric"><div class="metric-label">Pipeline Latency</div><div class="metric-value" id="summaryLatency">-</div></div>
      </div>

      <div class="pipeline" aria-label="OPEA pipeline">
        <div class="stage"><b>Gateway</b><span>M400 / API entry</span></div>
        <div class="stage"><b>Megaservice</b><span>Five-route orchestration</span></div>
        <div class="stage"><b>Dataprep</b><span>Route KB normalization</span></div>
        <div class="stage"><b>Retriever</b><span>Qdrant RAG isolation</span></div>
        <div class="stage"><b>TEI Embedding</b><span>OPEA profile ready</span></div>
        <div class="stage"><b>LLM Adapter</b><span>OpenAI/OPEA-compatible</span></div>
        <div class="stage"><b>Evaluator</b><span>Deterministic checks</span></div>
        <div class="stage"><b>Guardrails</b><span>Blocked unsafe claims</span></div>
      </div>

      <div class="workspace">
        <div class="stack">
          <section>
            <div class="panel-header"><div class="panel-title">Agent request</div><span id="requestPath" class="muted"></span></div>
            <div class="panel-body"><pre id="requestJson">Loading...</pre></div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">RAG source evidence</div><span id="ragBackend" class="muted"></span></div>
            <div class="panel-body"><div class="source-list" id="sourceList"></div></div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">Enterprise data boundary</div><span class="muted">private data is not leaked</span></div>
            <div class="panel-body">
              <div class="lineage-grid">
                <div class="lineage-item"><b>Private production lineage</b><span>Customer plant evidence includes real quality-inspection flows, including toothbrush workshop visual-inspection data.</span></div>
                <div class="lineage-item"><b>Public judge package</b><span>Committed samples are sanitized, reproducible fixtures with source IDs, thresholds, and blocked claims.</span></div>
                <div class="lineage-item"><b>Route isolation</b><span>Maintenance, IQC, changeover, WI, and hazard routes keep targets and claims separate.</span></div>
                <div class="lineage-item"><b>Human confirmation</b><span>High-risk outputs remain bounded action cards, not autonomous release authority.</span></div>
              </div>
            </div>
          </section>
        </div>
        <div class="stack">
          <section>
            <div class="panel-header"><div class="panel-title">Action card</div><span id="humanGate" class="muted"></span></div>
            <div class="panel-body action-card">
              <div class="card-main" id="cardTitle">Run a route to generate an action card.</div>
              <div class="card-action" id="cardAction"></div>
              <div class="facts">
                <div class="fact"><b>Channel</b><span id="cardChannel">-</span></div>
                <div class="fact"><b>Priority</b><span id="cardPriority">-</span></div>
                <div class="fact"><b>Integration</b><span id="cardIntegration">-</span></div>
                <div class="fact"><b>LLM runtime</b><span id="cardLlmRuntime">-</span></div>
                <div class="fact"><b>Source IDs</b><span id="cardSources">-</span></div>
                <div class="fact"><b>Entity</b><span id="cardEntity">-</span></div>
              </div>
              <div class="chips" id="blockedClaims"></div>
            </div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">Scorecard</div><span class="muted">contract / guardrail / source / target / isolation</span></div>
            <div class="panel-body"><div class="score-list" id="scoreList"></div></div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">Raw judge-verifiable JSON</div><span class="muted">/v1/agents and /v1/scorecard compatible</span></div>
            <div class="panel-body"><pre id="rawJson">{}</pre></div>
          </section>
        </div>
      </div>
    </main>
  </div>
  <script>
    const state = { agents: [], selected: "maintenance", lastResult: null };

    const el = (id) => document.getElementById(id);
    const pretty = (value) => JSON.stringify(value, null, 2);
    const riskClass = (risk) => risk === "high" ? "risk-high" : risk === "medium" ? "risk-medium" : "risk-low";

    async function getJson(url) {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
      return response.json();
    }

    function selectedAgent() {
      return state.agents.find((agent) => agent.mode === state.selected);
    }

    function modeLabel(mode) {
      const labels = {
        maintenance: "CMMS",
        iqc: "QMS",
        changeover: "MES",
        wi: "WI",
        hazard: "EHS",
      };
      return labels[mode] || mode;
    }

    function renderModeList() {
      el("modeList").innerHTML = state.agents.map((agent) => `
        <button class="mode-button ${agent.mode === state.selected ? "active" : ""}" data-mode="${agent.mode}">
          <div class="mode-top">
            <div class="mode-name">${agent.mode}</div>
            <div class="mode-pill">${modeLabel(agent.mode)}</div>
          </div>
          <div class="mode-target">${agent.integration_target}</div>
        </button>
      `).join("");
      for (const button of document.querySelectorAll(".mode-button")) {
        button.addEventListener("click", () => {
          state.selected = button.dataset.mode;
          renderModeList();
          runDemo();
        });
      }
    }

    function renderResult(result) {
      state.lastResult = result;
      const agent = selectedAgent();
      const card = result.action_card;
      const evalResult = result.agent_evaluation;
      const llm = result.llm_runtime || { backend: "unknown", claim_status: "unknown" };

      el("summaryMode").textContent = result.mode;
      el("summaryRisk").textContent = evalResult.risk_level;
      el("summaryRisk").className = `metric-value ${riskClass(evalResult.risk_level)}`;
      el("summaryOwner").textContent = card.owner;
      el("summaryTarget").textContent = card.integration_target;
      el("summaryLatency").textContent = `${result.timing.pipeline_latency_ms} ms`;
      el("requestPath").textContent = agent ? agent.sample_request_path : "";
      el("requestJson").textContent = pretty(result.request || {});
      el("ragBackend").textContent = result.rag.vector_store;
      el("sourceList").innerHTML = result.rag.hits.map((hit) => `
        <div class="source">
          <div class="source-title">${hit.payload.id} - ${hit.payload.title}<span class="source-score">score ${Number(hit.score).toFixed(4)}</span></div>
          <div class="source-text">${hit.payload.content}</div>
        </div>
      `).join("");
      el("humanGate").textContent = card.requires_human_confirmation ? "human confirmation required" : "guidance route";
      el("cardTitle").textContent = card.action;
      el("cardAction").textContent = result.llm_explanation;
      el("cardChannel").textContent = card.channel;
      el("cardPriority").textContent = card.priority;
      el("cardIntegration").textContent = card.integration_target;
      el("cardLlmRuntime").textContent = `${llm.backend} / ${llm.claim_status}`;
      el("cardSources").textContent = card.source_ids.join(", ");
      el("cardEntity").textContent = result.entity_id;
      el("blockedClaims").innerHTML = card.blocked_claims.map((claim) => `<span class="chip">${claim}</span>`).join("");
      el("rawJson").textContent = pretty(result);
    }

    async function runDemo() {
      el("rawJson").textContent = "Running selected industrial agent...";
      const result = await getJson(`/v1/agents/${state.selected}/demo`);
      renderResult(result);
    }

    async function refreshScorecard() {
      const scorecard = await getJson("/v1/scorecard");
      el("scoreList").innerHTML = scorecard.routes.map((route) => `
        <div class="score-row">
          <div class="score-title">${route.mode}: <span class="${route.status === "pass" ? "ok" : "warn"}">${route.status}</span></div>
          <div class="score-text">
            ${route.latency_ms} ms | ${route.integration_target}<br>
            contract=${route.contract_pass} guardrail=${route.guardrail_pass} source=${route.rag_source_match} target=${route.action_target_correctness} isolation=${route.route_isolation_pass}
          </div>
        </div>
      `).join("");
    }

    async function boot() {
      const catalog = await getJson("/v1/agents");
      state.agents = catalog.agents;
      renderModeList();
      await Promise.all([runDemo(), refreshScorecard()]);
    }

    el("runButton").addEventListener("click", runDemo);
    el("scorecardButton").addEventListener("click", refreshScorecard);
    boot().catch((error) => {
      el("rawJson").textContent = String(error.stack || error);
    });
  </script>
</body>
</html>"""
