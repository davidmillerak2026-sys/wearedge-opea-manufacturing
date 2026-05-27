from __future__ import annotations


def build_demo_console_html() -> str:
    return _HTML


_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WearEdge OPEA Manufacturing Console</title>
  <style>
    :root {
      --bg: #101412;
      --surface: #171d1a;
      --surface-2: #202720;
      --line: #39443d;
      --text: #f4f1e8;
      --muted: #a9b4ad;
      --green: #56c271;
      --amber: #f6b44b;
      --red: #df5b57;
      --blue: #5d9cec;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      letter-spacing: 0;
    }

    button, select {
      font: inherit;
    }

    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 300px 1fr;
    }

    aside {
      border-right: 1px solid var(--line);
      background: #121714;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .brand {
      display: grid;
      grid-template-columns: 48px 1fr;
      gap: 14px;
      align-items: center;
      min-height: 56px;
    }

    .mark {
      width: 48px;
      height: 48px;
      display: grid;
      place-items: center;
      border: 2px solid var(--green);
      color: var(--green);
      font-weight: 900;
    }

    .brand-title {
      font-size: 19px;
      font-weight: 760;
      line-height: 1.18;
    }

    .brand-sub {
      color: var(--muted);
      font-size: 13px;
      margin-top: 3px;
    }

    .mode-list {
      display: grid;
      gap: 8px;
    }

    .mode-button {
      min-height: 52px;
      width: 100%;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--text);
      text-align: left;
      padding: 12px 14px;
      border-radius: 6px;
      cursor: pointer;
    }

    .mode-button.active {
      border-color: var(--green);
      background: #1c2920;
    }

    .mode-name {
      font-weight: 760;
      font-size: 15px;
    }

    .mode-target {
      margin-top: 3px;
      color: var(--muted);
      font-size: 12px;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      overflow-wrap: anywhere;
    }

    .side-note {
      margin-top: auto;
      border-top: 1px solid var(--line);
      padding-top: 16px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }

    main {
      min-width: 0;
      display: grid;
      grid-template-rows: auto auto 1fr;
    }

    header {
      min-height: 82px;
      padding: 20px 28px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }

    h1 {
      margin: 0;
      font-size: 25px;
      line-height: 1.2;
    }

    .header-copy {
      color: var(--muted);
      font-size: 14px;
      margin-top: 5px;
      max-width: 880px;
      line-height: 1.35;
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
      min-height: 40px;
      border-radius: 6px;
      padding: 0 14px;
      cursor: pointer;
    }

    .primary {
      border: 1px solid var(--green);
      background: var(--green);
      color: #07120b;
      font-weight: 760;
    }

    .secondary {
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--text);
    }

    .summary {
      padding: 18px 28px;
      border-bottom: 1px solid var(--line);
      display: grid;
      grid-template-columns: minmax(92px, 0.72fr) minmax(92px, 0.72fr) minmax(178px, 1.2fr) minmax(208px, 1.44fr) minmax(112px, 0.8fr);
      gap: 12px;
    }

    .summary-cell {
      min-height: 74px;
      padding: 12px;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 6px;
    }

    .summary-label {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 760;
    }

    .summary-value {
      margin-top: 8px;
      font-size: 18px;
      font-weight: 760;
      overflow-wrap: normal;
    }

    .summary-code {
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 14px;
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .workspace {
      min-height: 0;
      padding: 24px 28px 30px;
      display: grid;
      grid-template-columns: minmax(360px, 0.85fr) minmax(460px, 1.15fr);
      gap: 18px;
      overflow: auto;
    }

    section {
      min-width: 0;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
    }

    .panel-header {
      min-height: 54px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .panel-title {
      font-size: 15px;
      font-weight: 780;
      text-transform: uppercase;
      color: var(--muted);
    }

    .panel-body {
      padding: 16px;
    }

    pre {
      margin: 0;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-family: "Cascadia Mono", "SFMono-Regular", monospace;
      font-size: 12px;
      line-height: 1.42;
      color: #d8e8dd;
    }

    .stack {
      display: grid;
      gap: 18px;
      align-content: start;
    }

    .action-card {
      display: grid;
      gap: 14px;
    }

    .card-main {
      font-size: 22px;
      font-weight: 780;
      line-height: 1.22;
    }

    .card-action {
      color: var(--text);
      font-size: 15px;
      line-height: 1.45;
    }

    .facts {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .fact {
      padding: 10px;
      border: 1px solid var(--line);
      background: var(--surface-2);
      border-radius: 6px;
      min-height: 58px;
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
      border-radius: 4px;
      border: 1px solid rgba(223, 91, 87, 0.48);
      color: #ffd6d2;
      background: rgba(223, 91, 87, 0.14);
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
      background: var(--surface-2);
      border-radius: 6px;
    }

    .source-title,
    .score-title {
      font-weight: 760;
      margin-bottom: 5px;
    }

    .source-text,
    .score-text {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.42;
    }

    .ok {
      color: var(--green);
    }

    .warn {
      color: var(--amber);
    }

    .risk-high {
      color: var(--red);
    }

    .risk-medium {
      color: var(--amber);
    }

    .risk-low {
      color: var(--green);
    }

    @media (max-width: 980px) {
      .shell { grid-template-columns: 1fr; }
      aside { border-right: 0; border-bottom: 1px solid var(--line); }
      .summary { grid-template-columns: repeat(2, 1fr); }
      .summary-code { white-space: normal; overflow-wrap: anywhere; }
      .workspace { grid-template-columns: 1fr; }
      header { align-items: flex-start; flex-direction: column; }
      .actions { justify-content: flex-start; }
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
          <div class="brand-sub">OPEA Manufacturing</div>
        </div>
      </div>
      <div class="mode-list" id="modeList"></div>
      <div class="side-note">
        Submission shape: GitHub + Docker Compose + Web Console + API/scorecard.
        M400/Android is the real deployment front end and source evidence, not a required judge device.
      </div>
    </aside>
    <main>
      <header>
        <div>
          <h1>Manufacturing Demo Console</h1>
          <div class="header-copy">Run any route through the same OPEA-style Gateway, Megaservice, RAG, evaluator, guardrails, and action-card contract.</div>
        </div>
        <div class="actions">
          <button class="secondary" id="scorecardButton">Refresh Scorecard</button>
          <button class="primary" id="runButton">Run Selected Demo</button>
        </div>
      </header>
      <div class="summary">
        <div class="summary-cell"><div class="summary-label">Mode</div><div class="summary-value summary-code" id="summaryMode">-</div></div>
        <div class="summary-cell"><div class="summary-label">Risk</div><div class="summary-value" id="summaryRisk">-</div></div>
        <div class="summary-cell"><div class="summary-label">Owner</div><div class="summary-value summary-code" id="summaryOwner">-</div></div>
        <div class="summary-cell"><div class="summary-label">Target</div><div class="summary-value summary-code" id="summaryTarget">-</div></div>
        <div class="summary-cell"><div class="summary-label">Latency</div><div class="summary-value" id="summaryLatency">-</div></div>
      </div>
      <div class="workspace">
        <div class="stack">
          <section>
            <div class="panel-header"><div class="panel-title">Sample request</div><span id="requestPath" class="muted"></span></div>
            <div class="panel-body"><pre id="requestJson">Loading...</pre></div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">RAG source evidence</div><span id="ragBackend" class="muted"></span></div>
            <div class="panel-body"><div class="source-list" id="sourceList"></div></div>
          </section>
        </div>
        <div class="stack">
          <section>
            <div class="panel-header"><div class="panel-title">Action card</div><span id="humanGate" class="muted"></span></div>
            <div class="panel-body action-card">
              <div class="card-main" id="cardTitle">Run a demo to generate an action card.</div>
              <div class="card-action" id="cardAction"></div>
              <div class="facts">
                <div class="fact"><b>Channel</b><span id="cardChannel">-</span></div>
                <div class="fact"><b>Priority</b><span id="cardPriority">-</span></div>
                <div class="fact"><b>Integration</b><span id="cardIntegration">-</span></div>
                <div class="fact"><b>Source IDs</b><span id="cardSources">-</span></div>
              </div>
              <div class="chips" id="blockedClaims"></div>
            </div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">Scorecard</div><span class="muted">contract / guardrail / source / target / isolation</span></div>
            <div class="panel-body"><div class="score-list" id="scoreList"></div></div>
          </section>
          <section>
            <div class="panel-header"><div class="panel-title">Raw result</div><span class="muted">judge-verifiable JSON</span></div>
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

    function renderModeList() {
      el("modeList").innerHTML = state.agents.map((agent) => `
        <button class="mode-button ${agent.mode === state.selected ? "active" : ""}" data-mode="${agent.mode}">
          <div class="mode-name">${agent.mode}</div>
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
      el("summaryMode").textContent = result.mode;
      el("summaryRisk").textContent = evalResult.risk_level;
      el("summaryRisk").className = `summary-value ${riskClass(evalResult.risk_level)}`;
      el("summaryOwner").textContent = card.owner;
      el("summaryTarget").textContent = card.integration_target;
      el("summaryLatency").textContent = `${result.timing.pipeline_latency_ms} ms`;
      el("requestPath").textContent = agent ? agent.sample_request_path : "";
      el("requestJson").textContent = pretty(result.request || {});
      el("ragBackend").textContent = result.rag.vector_store;
      el("sourceList").innerHTML = result.rag.hits.map((hit) => `
        <div class="source">
          <div class="source-title">${hit.payload.id} - ${hit.payload.title}</div>
          <div class="source-text">${hit.payload.content}</div>
        </div>
      `).join("");
      el("humanGate").textContent = card.requires_human_confirmation ? "human confirmation required" : "guidance route";
      el("cardTitle").textContent = card.action;
      el("cardAction").textContent = result.llm_explanation;
      el("cardChannel").textContent = card.channel;
      el("cardPriority").textContent = card.priority;
      el("cardIntegration").textContent = card.integration_target;
      el("cardSources").textContent = card.source_ids.join(", ");
      el("blockedClaims").innerHTML = card.blocked_claims.map((claim) => `<span class="chip">${claim}</span>`).join("");
      el("rawJson").textContent = pretty(result);
    }

    async function runDemo() {
      el("rawJson").textContent = "Running...";
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
