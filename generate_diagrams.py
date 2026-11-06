import os
import subprocess

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content, output_png, width=1200, height=750):
    temp_html = output_png.replace(".png", ".html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    file_url = f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    cmd = [
        edge,
        "--headless",
        "--disable-gpu",
        f"--screenshot={os.path.abspath(output_png)}",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        file_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    if os.path.exists(output_png):
        print(f"Generated {output_png} ({os.path.getsize(output_png)} bytes)")
    else:
        print(f"Failed to generate {output_png}: {res.stderr}")

# Diagram 1: Module Decomposition / Structure Chart
html_diag1 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 24px; background: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  .canvas { width: 1150px; height: 700px; background: #fafbfc; border: 1.5px solid #d0d7de; border-radius: 8px; box-sizing: border-box; padding: 20px; position: relative; }
  .title { text-align: center; font-size: 20px; font-weight: bold; color: #1b4332; margin-bottom: 4px; }
  .subtitle { text-align: center; font-size: 13px; color: #52796f; margin-bottom: 25px; }
  
  .node { position: absolute; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.06); text-align: center; box-sizing: border-box; }
  .root { left: 375px; top: 75px; width: 400px; height: 55px; background: linear-gradient(135deg, #1b4332, #2d6a4f); color: white; border: 2px solid #081c15; padding-top: 8px; }
  .root .name { font-size: 15px; font-weight: bold; }
  .root .desc { font-size: 11px; opacity: 0.9; }

  .tier1 { width: 200px; height: 60px; top: 175px; color: white; border-width: 1.5px; border-style: solid; padding: 8px 6px; }
  .t1-1 { left: 35px; background: #2563eb; border-color: #1d4ed8; }
  .t1-2 { left: 265px; background: #059669; border-color: #047857; }
  .t1-3 { left: 495px; background: #7c3aed; border-color: #6d28d9; }
  .t1-4 { left: 725px; background: #d97706; border-color: #b45309; }
  .t1-5 { left: 955px; background: #475569; border-color: #334155; }
  
  .tier1 .t1-name { font-size: 13px; font-weight: bold; line-height: 1.2; }
  .tier1 .t1-tech { font-size: 10px; opacity: 0.9; margin-top: 3px; }

  .tier2-col { position: absolute; width: 200px; top: 260px; }
  .c1 { left: 35px; }
  .c2 { left: 265px; }
  .c3 { left: 495px; }
  .c4 { left: 725px; }
  .c5 { left: 955px; }

  .subnode { width: 200px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 5px; margin-bottom: 10px; padding: 8px 8px; text-align: left; box-sizing: border-box; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  .subnode-title { font-size: 11.5px; font-weight: bold; color: #1e293b; }
  .subnode-desc { font-size: 10px; color: #64748b; margin-top: 2px; }

  svg.lines { position: absolute; top: 0; left: 0; width: 1150px; height: 700px; pointer-events: none; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">Figure 2.1: Hierarchical Module Decomposition Structure Chart</div>
  <div class="subtitle">Fieldwise: Intelligent Fertilizer Recommendation Platform — System Modularization</div>

  <svg class="lines">
    <!-- Root down to horizontal spine -->
    <line x1="575" y1="130" x2="575" y2="155" stroke="#334155" stroke-width="2" />
    <line x1="135" y1="155" x2="1055" y2="155" stroke="#334155" stroke-width="2" />
    <!-- Down to each tier 1 box -->
    <line x1="135" y1="155" x2="135" y2="175" stroke="#334155" stroke-width="2" />
    <line x1="365" y1="155" x2="365" y2="175" stroke="#334155" stroke-width="2" />
    <line x1="595" y1="155" x2="595" y2="175" stroke="#334155" stroke-width="2" />
    <line x1="825" y1="155" x2="825" y2="175" stroke="#334155" stroke-width="2" />
    <line x1="1055" y1="155" x2="1055" y2="175" stroke="#334155" stroke-width="2" />
    <!-- Lines from tier 1 down to columns -->
    <line x1="135" y1="235" x2="135" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="365" y1="235" x2="365" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="595" y1="235" x2="595" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="825" y1="235" x2="825" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="1055" y1="235" x2="1055" y2="260" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
  </svg>

  <div class="node root">
    <div class="name">Fieldwise Fertilizer Recommendation System</div>
    <div class="desc">Top-Level Integrated Precision Agriculture Application</div>
  </div>

  <div class="node tier1 t1-1">
    <div class="t1-name">Presentation Tier</div>
    <div class="t1-tech">React 19 / TypeScript SPA</div>
  </div>
  <div class="tier2-col c1">
    <div class="subnode">
      <div class="subnode-title">Overview Cockpit</div>
      <div class="subnode-desc">Soil NPK & crop parameter form with dynamic dials</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Prediction History</div>
      <div class="subnode-desc">Interactive timeline view & telemetry logs</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Model Audit UI</div>
      <div class="subnode-desc">Confidence distributions & latency governance</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Auth Context & API</div>
      <div class="subnode-desc">Client state, token cache & HTTP client</div>
    </div>
  </div>

  <div class="node tier1 t1-2">
    <div class="t1-name">API Gateway Tier</div>
    <div class="t1-tech">FastAPI Microservice (:8000)</div>
  </div>
  <div class="tier2-col c2">
    <div class="subnode">
      <div class="subnode-title">Ingress Middleware</div>
      <div class="subnode-desc">X-Request-ID, CORS, Sliding rate limiter</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Auth & Security</div>
      <div class="subnode-desc">X-API-Key and JWT bearer verification</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Pydantic Schemas</div>
      <div class="subnode-desc">Strict contract validation & boundary checks</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Router Controllers</div>
      <div class="subnode-desc">/recommend, /predictions, /batch, /analytics</div>
    </div>
  </div>

  <div class="node tier1 t1-3">
    <div class="t1-name">ML Inference Tier</div>
    <div class="t1-tech">FastAPI ML Engine (:8001)</div>
  </div>
  <div class="tier2-col c3">
    <div class="subnode">
      <div class="subnode-title">Feature Pipeline</div>
      <div class="subnode-desc">RobustScaler & categorical OneHotEncoder</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Model Registry</div>
      <div class="subnode-desc">Versioned artifact loader (v1 XGBoost/RF)</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Predictor Engine</div>
      <div class="subnode-desc">Vectorized multi-class inference & probabilities</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Health & Probe</div>
      <div class="subnode-desc">Inference readiness & latency benchmark</div>
    </div>
  </div>

  <div class="node tier1 t1-4">
    <div class="t1-name">Persistence Tier</div>
    <div class="t1-tech">Peewee ORM / SQLite / Postgres</div>
  </div>
  <div class="tier2-col c4">
    <div class="subnode">
      <div class="subnode-title">DB Manager</div>
      <div class="subnode-desc">Thread-safe connection pool & lifecycles</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">PredictionLog Model</div>
      <div class="subnode-desc">Audit schema, latency, inputs, & output</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">User & Auth Models</div>
      <div class="subnode-desc">Credentials, API keys, & profile metadata</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Migration Runner</div>
      <div class="subnode-desc">Version-controlled schema migration scripts</div>
    </div>
  </div>

  <div class="node tier1 t1-5">
    <div class="t1-name">Resiliency Tier</div>
    <div class="t1-tech">Fault Tolerance & Telemetry</div>
  </div>
  <div class="tier2-col c5">
    <div class="subnode">
      <div class="subnode-title">Circuit Breaker</div>
      <div class="subnode-desc">State machine: CLOSED, OPEN, HALF_OPEN</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">ML Client Pool</div>
      <div class="subnode-desc">HTTPX connection reuse & retry backoff</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Prometheus Metrics</div>
      <div class="subnode-desc">/metrics scrape endpoint for latency/rates</div>
    </div>
    <div class="subnode">
      <div class="subnode-title">Structured Logging</div>
      <div class="subnode-desc">JSON logs with distributed request correlation</div>
    </div>
  </div>
</div>
</body>
</html>
"""

# Diagram 2: Top-Down Design
html_diag2 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 24px; background: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  .canvas { width: 1150px; height: 680px; background: #fafbfc; border: 1.5px solid #d0d7de; border-radius: 8px; box-sizing: border-box; padding: 20px; position: relative; }
  .title { text-align: center; font-size: 20px; font-weight: bold; color: #1e3a8a; margin-bottom: 4px; }
  .subtitle { text-align: center; font-size: 13px; color: #3b82f6; margin-bottom: 25px; }

  .level-label { position: absolute; left: 25px; font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; background: #e2e8f0; padding: 4px 8px; border-radius: 4px; }
  .ll-0 { top: 75px; }
  .ll-1 { top: 180px; }
  .ll-2 { top: 310px; }
  .ll-3 { top: 480px; }

  .box { position: absolute; border-radius: 6px; box-sizing: border-box; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }

  /* Level 0 */
  .b0 { left: 325px; top: 65px; width: 500px; height: 55px; background: #1e3a8a; color: white; border: 2px solid #172554; padding-top: 8px; }
  .b0 .title-txt { font-size: 15px; font-weight: bold; }
  .b0 .desc-txt { font-size: 11px; opacity: 0.9; }

  /* Level 1 */
  .b1-1 { left: 100px; top: 170px; width: 280px; height: 65px; background: #2563eb; color: white; border: 1.5px solid #1d4ed8; padding-top: 10px; }
  .b1-2 { left: 435px; top: 170px; width: 280px; height: 65px; background: #059669; color: white; border: 1.5px solid #047857; padding-top: 10px; }
  .b1-3 { left: 770px; top: 170px; width: 280px; height: 65px; background: #7c3aed; color: white; border: 1.5px solid #6d28d9; padding-top: 10px; }
  .b1-txt { font-size: 13.5px; font-weight: bold; }
  .b1-sub { font-size: 11px; opacity: 0.9; margin-top: 2px; }

  /* Level 2 */
  .b2 { width: 140px; height: 75px; top: 300px; background: white; border: 1.5px solid #94a3b8; color: #1e293b; padding: 8px 4px; }
  .b2 .h { font-size: 11.5px; font-weight: bold; color: #0f172a; line-height: 1.2; }
  .b2 .d { font-size: 9.5px; color: #64748b; margin-top: 4px; }
  
  .b2-1 { left: 80px; }
  .b2-2 { left: 240px; }
  .b2-3 { left: 410px; }
  .b2-4 { left: 570px; }
  .b2-5 { left: 740px; }
  .b2-6 { left: 900px; }

  /* Level 3 */
  .b3 { width: 140px; height: 80px; top: 460px; background: #f8fafc; border: 1.5px dashed #64748b; color: #334155; padding: 6px 4px; text-align: left; }
  .b3 .fn { font-family: 'Consolas', monospace; font-size: 10px; font-weight: bold; color: #0972d3; }
  .b3 .fdesc { font-size: 9px; color: #475569; margin-top: 3px; line-height: 1.25; }

  .b3-1 { left: 80px; }
  .b3-2 { left: 240px; }
  .b3-3 { left: 410px; }
  .b3-4 { left: 570px; }
  .b3-5 { left: 740px; }
  .b3-6 { left: 900px; }

  svg.decomp-lines { position: absolute; top: 0; left: 0; width: 1150px; height: 680px; pointer-events: none; }
  .decomp-tag { position: absolute; right: 25px; bottom: 20px; font-size: 11px; color: #64748b; font-style: italic; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">Figure 5.1: Top-Down Functional Decomposition Diagram</div>
  <div class="subtitle">Stepwise Refinement from High-Level System Objective to Atomic Implementation Routines</div>

  <div class="level-label ll-0">Level 0: Goal</div>
  <div class="level-label ll-1">Level 1: Subsystems</div>
  <div class="level-label ll-2">Level 2: Modules</div>
  <div class="level-label ll-3">Level 3: Primitives</div>

  <svg class="decomp-lines">
    <!-- Level 0 to Level 1 -->
    <line x1="575" y1="120" x2="575" y2="145" stroke="#475569" stroke-width="2" />
    <line x1="240" y1="145" x2="910" y2="145" stroke="#475569" stroke-width="2" />
    <line x1="240" y1="145" x2="240" y2="170" stroke="#475569" stroke-width="2" />
    <line x1="575" y1="145" x2="575" y2="170" stroke="#475569" stroke-width="2" />
    <line x1="910" y1="145" x2="910" y2="170" stroke="#475569" stroke-width="2" />

    <!-- Level 1 to Level 2 (Subsystem 1) -->
    <line x1="240" y1="235" x2="240" y2="265" stroke="#2563eb" stroke-width="1.5" />
    <line x1="150" y1="265" x2="310" y2="265" stroke="#2563eb" stroke-width="1.5" />
    <line x1="150" y1="265" x2="150" y2="300" stroke="#2563eb" stroke-width="1.5" />
    <line x1="310" y1="265" x2="310" y2="300" stroke="#2563eb" stroke-width="1.5" />

    <!-- Level 1 to Level 2 (Subsystem 2) -->
    <line x1="575" y1="235" x2="575" y2="265" stroke="#059669" stroke-width="1.5" />
    <line x1="480" y1="265" x2="640" y2="265" stroke="#059669" stroke-width="1.5" />
    <line x1="480" y1="265" x2="480" y2="300" stroke="#059669" stroke-width="1.5" />
    <line x1="640" y1="265" x2="640" y2="300" stroke="#059669" stroke-width="1.5" />

    <!-- Level 1 to Level 2 (Subsystem 3) -->
    <line x1="910" y1="235" x2="910" y2="265" stroke="#7c3aed" stroke-width="1.5" />
    <line x1="810" y1="265" x2="970" y2="265" stroke="#7c3aed" stroke-width="1.5" />
    <line x1="810" y1="265" x2="810" y2="300" stroke="#7c3aed" stroke-width="1.5" />
    <line x1="970" y1="265" x2="970" y2="300" stroke="#7c3aed" stroke-width="1.5" />

    <!-- Level 2 to Level 3 connects -->
    <line x1="150" y1="375" x2="150" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="310" y1="375" x2="310" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="480" y1="375" x2="480" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="640" y1="375" x2="640" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="810" y1="375" x2="810" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
    <line x1="970" y1="375" x2="970" y2="460" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
  </svg>

  <div class="box b0">
    <div class="title-txt">Autonomous Fertilizer Recommendation System</div>
    <div class="desc-txt">Root Purpose: Deliver accurate, real-time chemical fertilizer dosage to farmers</div>
  </div>

  <div class="box b1-1">
    <div class="b1-txt">User Ingress Subsystem</div>
    <div class="b1-sub">Client Interaction &amp; Routing</div>
  </div>
  <div class="box b1-2">
    <div class="b1-txt">Decision &amp; ML Subsystem</div>
    <div class="b1-sub">Feature Preprocessing &amp; Inference</div>
  </div>
  <div class="box b1-3">
    <div class="b1-txt">Persistence &amp; Audit Subsystem</div>
    <div class="b1-sub">Storage, Audits &amp; Governance</div>
  </div>

  <!-- Level 2 -->
  <div class="box b2 b2-1">
    <div class="h">Client UI Cockpit</div>
    <div class="d">NPK input dials, crop selection, result display</div>
  </div>
  <div class="box b2 b2-2">
    <div class="h">Gateway Router &amp; Auth</div>
    <div class="d">Token verify, rate limit, request tracing</div>
  </div>
  <div class="box b2 b2-3">
    <div class="h">Data Preprocessor</div>
    <div class="d">Soil scaling, imputer, one-hot category encoding</div>
  </div>
  <div class="box b2 b2-4">
    <div class="h">Ensemble Classifier</div>
    <div class="d">XGBoost &amp; Random Forest probability scoring</div>
  </div>
  <div class="box b2 b2-5">
    <div class="h">Audit Logger</div>
    <div class="d">Asynchronous logging of inputs, outputs &amp; latency</div>
  </div>
  <div class="box b2 b2-6">
    <div class="h">Telemetry &amp; Metrics</div>
    <div class="d">Prometheus /metrics &amp; structured JSON log stream</div>
  </div>

  <!-- Level 3 -->
  <div class="box b3 b3-1">
    <div class="fn">handleSliderChange()</div>
    <div class="fdesc">Captures N, P, K state updates &amp; triggers reactive re-render.</div>
  </div>
  <div class="box b3 b3-2">
    <div class="fn">verify_api_key()</div>
    <div class="fdesc">Validates X-API-Key header against config secret hash.</div>
  </div>
  <div class="box b3 b3-3">
    <div class="fn">RobustScaler.transform()</div>
    <div class="fdesc">Normalizes numerical pH and nutrient values.</div>
  </div>
  <div class="box b3 b3-4">
    <div class="fn">predict_proba()</div>
    <div class="fdesc">Computes multi-class probability distribution vector.</div>
  </div>
  <div class="box b3 b3-5">
    <div class="fn">PredictionLog.create()</div>
    <div class="fdesc">Inserts audit record with request_id foreign key.</div>
  </div>
  <div class="box b3 b3-6">
    <div class="fn">record_latency_metric()</div>
    <div class="fdesc">Pushes request timing to Prometheus histogram bucket.</div>
  </div>

  <div class="decomp-tag">Top-Down Refinement: Abstract Strategy ➔ Concrete Execution Routines</div>
</div>
</body>
</html>
"""

# Diagram 3: Bottom-Up Design
html_diag3 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 24px; background: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  .canvas { width: 1150px; height: 680px; background: #fafbfc; border: 1.5px solid #d0d7de; border-radius: 8px; box-sizing: border-box; padding: 20px; position: relative; }
  .title { text-align: center; font-size: 20px; font-weight: bold; color: #047857; margin-bottom: 4px; }
  .subtitle { text-align: center; font-size: 13px; color: #065f46; margin-bottom: 25px; }

  .layer-band { position: absolute; left: 160px; width: 950px; border-radius: 6px; box-sizing: border-box; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
  .layer-side { position: absolute; left: 25px; width: 120px; font-size: 11px; font-weight: bold; color: white; padding: 8px 6px; border-radius: 4px; text-align: center; box-sizing: border-box; }

  /* Layer 3 - Top Composite */
  .s3 { top: 75px; background: #065f46; }
  .b3 { top: 70px; height: 65px; background: #ecfdf5; border: 1.5px solid #10b981; }

  /* Layer 2 - Services */
  .s2 { top: 185px; background: #0d9488; }
  .b2 { top: 175px; height: 95px; background: #f0fdfa; border: 1.5px solid #14b8a6; }

  /* Layer 1 - Encapsulated Modules */
  .s1 { top: 335px; background: #0284c7; }
  .b1 { top: 315px; height: 115px; background: #f0f9ff; border: 1.5px solid #38bdf8; }

  /* Layer 0 - Foundational Primitives */
  .s0 { top: 505px; background: #475569; }
  .b0 { top: 480px; height: 135px; background: #f8fafc; border: 1.5px solid #94a3b8; }

  .card { background: white; border-radius: 5px; box-sizing: border-box; padding: 8px 10px; border: 1px solid #cbd5e1; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  .card-title { font-size: 12px; font-weight: bold; color: #0f172a; }
  .card-desc { font-size: 10px; color: #475569; margin-top: 3px; }

  .card-top { width: 100%; text-align: center; background: #10b981; color: white; border: none; padding: 8px; }
  .card-top .t-main { font-size: 14.5px; font-weight: bold; }
  .card-top .t-sub { font-size: 11px; opacity: 0.95; }

  .c-l2 { width: 300px; height: 75px; }
  .c-l1 { width: 220px; height: 90px; }
  .c-l0 { width: 170px; height: 110px; }

  .up-arrow { position: absolute; left: 80px; width: 2px; background: #94a3b8; pointer-events: none; }
  .arr-label { position: absolute; left: 630px; font-size: 11px; font-weight: bold; color: #059669; background: #d1fae5; padding: 3px 10px; border-radius: 12px; border: 1px solid #6ee7b7; }
  .al-1 { top: 450px; }
  .al-2 { top: 287px; }
  .al-3 { top: 147px; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">Figure 5.2: Bottom-Up Architectural Synthesis Diagram</div>
  <div class="subtitle">Progressive Composition from Reusable Low-Level Primitives to Enterprise Platform</div>

  <!-- Layer 3: Complete Unified System -->
  <div class="layer-side s3">Layer 3<br>System Level</div>
  <div class="layer-band b3">
    <div class="card card-top">
      <div class="t-main">Fieldwise Autonomous Fertilizer Recommendation Platform</div>
      <div class="t-sub">Fully Integrated React 19 Frontend + FastAPI Gateway (:8000) + ML Inference Microservice (:8001)</div>
    </div>
  </div>

  <div class="arr-label al-3">&#9650; Synthesizes into Fully Deployed Enterprise Architecture</div>

  <!-- Layer 2: Domain Microservices -->
  <div class="layer-side s2">Layer 2<br>Microservices</div>
  <div class="layer-band b2">
    <div class="card c-l2">
      <div class="card-title">Client Single Page App (SPA)</div>
      <div class="card-desc">React 19, TypeScript, GSAP Motion, Lenis scroll, Overview cockpit &amp; timeline</div>
    </div>
    <div class="card c-l2">
      <div class="card-title">FastAPI Gateway Service (:8000)</div>
      <div class="card-desc">HTTP ingress, authentication guard, rate limiting, circuit breaker, audit logger</div>
    </div>
    <div class="card c-l2">
      <div class="card-title">ML Inference Microservice (:8001)</div>
      <div class="card-desc">Dedicated model runner, vectorized feature transformer, soft-voting ensemble</div>
    </div>
  </div>

  <div class="arr-label al-2">&#9650; Assembled into Cohesive Autonomous Services</div>

  <!-- Layer 1: Encapsulated Core Components -->
  <div class="layer-side s1">Layer 1<br>Core Modules</div>
  <div class="layer-band b1">
    <div class="card c-l1">
      <div class="card-title">Circuit Breaker Engine</div>
      <div class="card-desc">State machine: CLOSED, OPEN, HALF_OPEN; failure threshold &amp; cooldown timers</div>
    </div>
    <div class="card c-l1">
      <div class="card-title">Predictor Engine</div>
      <div class="card-desc">Loads XGBoost &amp; Random Forest artifacts; calculates class probabilities</div>
    </div>
    <div class="card c-l1">
      <div class="card-title">Peewee ORM Layer</div>
      <div class="card-desc">PredictionLog &amp; User models; connection manager &amp; migration runner</div>
    </div>
    <div class="card c-l1">
      <div class="card-title">Auth &amp; Security Module</div>
      <div class="card-desc">JWT token encoding/decoding, X-API-Key validation &amp; request ID tracing</div>
    </div>
  </div>

  <div class="arr-label al-1">&#9650; Combined to Form Stateful Domain Components</div>

  <!-- Layer 0: Foundational Primitives -->
  <div class="layer-side s0">Layer 0<br>Primitives</div>
  <div class="layer-band b0">
    <div class="card c-l0">
      <div class="card-title">Pydantic Schemas</div>
      <div class="card-desc">Compile-time &amp; runtime validation models (RecommendRequest, PredictionDetail)</div>
    </div>
    <div class="card c-l0">
      <div class="card-title">Feature Scalers</div>
      <div class="card-desc">StandardScaler, RobustScaler, and OneHotEncoder numerical transforms</div>
    </div>
    <div class="card c-l0">
      <div class="card-title">Async HTTP Client</div>
      <div class="card-desc">HTTPX connection pool, timeout configs, exponential backoff retries</div>
    </div>
    <div class="card c-l0">
      <div class="card-title">Telemetry Utilities</div>
      <div class="card-desc">Prometheus Counter / Histogram metrics, JSON log formatter</div>
    </div>
    <div class="card c-l0">
      <div class="card-title">UI Widget Primitives</div>
      <div class="card-desc">Slider controls, Status Badges, Confidence Ring dials, Pill buttons</div>
    </div>
  </div>
</div>
</body>
</html>
"""

print("Rendering Diagram 1...")
render_html_to_png(html_diag1, "diagram_modularization.png", 1200, 750)

print("Rendering Diagram 2...")
render_html_to_png(html_diag2, "diagram_top_down.png", 1200, 720)

print("Rendering Diagram 3...")
render_html_to_png(html_diag3, "diagram_bottom_up.png", 1200, 720)
