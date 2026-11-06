import os
import subprocess

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_svg_to_png(svg_content, svg_filename, png_filename, width, height):
    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Saved SVG: {svg_filename}")

    temp_html = f"temp_render_{os.path.splitext(png_filename)[0]}.html"
    html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin: 0; padding: 0; background: #ffffff; display: flex; justify-content: center; align-items: center; }}
    svg {{ display: block; width: {width}px; height: {height}px; }}
  </style>
</head>
<body>
{svg_content}
</body>
</html>
"""
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_wrapper)

    file_url = f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={os.path.abspath(png_filename)}",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        file_url
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    if os.path.exists(png_filename):
        print(f"Successfully generated {png_filename} (Size: {os.path.getsize(png_filename)} bytes)")
    else:
        print(f"Error generating PNG {png_filename}: {res.stderr}")

# -------------------------------------------------------------
# 1. SEQUENCE DIAGRAM 1: REAL-TIME RECOMMENDATION FLOW
# -------------------------------------------------------------
def get_seq_diag_1():
    w, h = 2200, 1400
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <filter id="shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    
    <marker id="sync-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>

    <marker id="async-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round"/>
    </marker>

    <marker id="return-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9" fill="none" stroke="#475569" stroke-width="1.8" stroke-linecap="round"/>
    </marker>

    <marker id="self-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>
  </defs>

  <style>
    .title-main {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #0f172a; }}
    .title-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: 500; fill: #475569; }}
    
    .lifeline-name {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: bold; text-anchor: middle; }}
    .lifeline-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; font-style: italic; text-anchor: middle; fill: #64748B; }}
    .lifeline-line {{ stroke: #94A3B8; stroke-width: 1.5px; stroke-dasharray: 6,6; }}
    
    .act-bar {{ fill: #E2E8F0; stroke: #475569; stroke-width: 1.2px; rx: 3px; }}
    .act-bar-focus {{ fill: #BAE6FD; stroke: #0284C7; stroke-width: 1.4px; rx: 3px; }}
    
    .msg-sync   {{ stroke: #1E293B; stroke-width: 1.8px; marker-end: url(#sync-arrow); }}
    .msg-async  {{ stroke: #2563EB; stroke-width: 1.8px; marker-end: url(#async-arrow); }}
    .msg-return {{ stroke: #475569; stroke-width: 1.6px; stroke-dasharray: 6,4; marker-end: url(#return-arrow); }}
    
    .msg-text {{ font-family: 'Consolas', 'Segoe UI', monospace; font-size: 11px; fill: #0F172A; font-weight: 600; }}
    .msg-ret-text {{ font-family: 'Consolas', 'Segoe UI', monospace; font-size: 10.5px; fill: #475569; font-style: italic; }}
    
    .frame-box {{ fill: #F8FAFC; fill-opacity: 0.6; stroke: #64748B; stroke-width: 1.5px; rx: 5px; }}
    .frame-tag {{ fill: #334155; rx: 3px; }}
    .frame-tag-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #FFFFFF; }}
    .frame-guard {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; font-weight: bold; fill: #1E3A8A; }}
    .frame-divider {{ stroke: #64748B; stroke-width: 1.2px; stroke-dasharray: 8,6; }}

    .legend-box {{ fill: #F1F5F9; stroke: #CBD5E1; stroke-width: 1px; rx: 6px; }}
    .legend-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #334155; }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <rect x="15" y="15" width="{w-30}" height="{h-30}" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- Header Banner -->
  <g transform="translate({w/2}, 42)">
    <text class="title-main" text-anchor="middle">Fieldwise: Intelligent Fertilizer Recommendation System</text>
    <text class="title-sub" y="24" text-anchor="middle">UML 2.5 Sequence Diagram 1: Real-Time Fertilizer Recommendation &amp; Inference Pipeline Interaction</text>
  </g>

  <!-- Lifeline 1: Farmer / Client UI -->
  <g transform="translate(160, 90)">
    <rect x="-90" y="0" width="180" height="52" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#1E3A8A">:Farmer / Client</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Actor / Web UI&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 2: RecommendationController -->
  <g transform="translate(430, 90)">
    <rect x="-105" y="0" width="210" height="52" fill="#ECFDF5" stroke="#10B981" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#065F46">:RecommendationController</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Boundary / API Router&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 3: MLClient -->
  <g transform="translate(720, 90)">
    <rect x="-85" y="0" width="170" height="52" fill="#EEF2FF" stroke="#6366F1" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#312E81">:MLClient</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Service / HTTP Adapter&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 4: CircuitBreaker -->
  <g transform="translate(1000, 90)">
    <rect x="-85" y="0" width="170" height="52" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#78350F">:CircuitBreaker</text>
    <text y="38" class="lifeline-sub">&lt;&lt;FSM / Resiliency Guard&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 5: FertilizerPredictor -->
  <g transform="translate(1290, 90)">
    <rect x="-100" y="0" width="200" height="52" fill="#F5F3FF" stroke="#8B5CF6" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#4C1D95">:FertilizerPredictor</text>
    <text y="38" class="lifeline-sub">&lt;&lt;ML Service Engine :8001&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 6: ModelRegistry -->
  <g transform="translate(1570, 90)">
    <rect x="-85" y="0" width="170" height="52" fill="#FDF2F8" stroke="#EC4899" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#831843">:ModelRegistry</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Cache / Artifact Manager&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 7: DatabaseManager -->
  <g transform="translate(1840, 90)">
    <rect x="-90" y="0" width="180" height="52" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#134E4A">:DatabaseManager</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Data Access / Peewee ORM&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Lifeline 8: PrometheusMetrics -->
  <g transform="translate(2060, 90)">
    <rect x="-80" y="0" width="160" height="52" fill="#FEF2F2" stroke="#EF4444" stroke-width="1.8" rx="6" filter="url(#shadow)"/>
    <text y="22" class="lifeline-name" fill="#7F1D1D">:PrometheusMetrics</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Observability Exporter&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1240" class="lifeline-line"/>
  </g>

  <!-- Activation Bars -->
  <rect x="153" y="170" width="14" height="1030" class="act-bar"/>
  <rect x="423" y="185" width="14" height="990" class="act-bar-focus"/>
  <rect x="713" y="325" width="14" height="570" class="act-bar"/>
  <rect x="993" y="355" width="14" height="60" class="act-bar"/>
  <rect x="993" y="835" width="14" height="45" class="act-bar"/>
  <rect x="1283" y="475" width="14" height="310" class="act-bar-focus"/>
  <rect x="1563" y="505" width="14" height="50" class="act-bar"/>
  <rect x="1833" y="945" width="14" height="75" class="act-bar"/>
  <rect x="2053" y="1040" width="14" height="50" class="act-bar"/>

  <!-- Messages -->
  <line x1="167" y1="185" x2="423" y2="185" class="msg-sync"/>
  <text x="180" y="177" class="msg-text">1: POST /api/v1/fertilizer/recommend (soil_pH, N, P, K, crop_stage)</text>

  <path d="M 437 205 L 475 205 L 475 235 L 437 235" fill="none" stroke="#1E293B" stroke-width="1.6" marker-end="url(#self-arrow)"/>
  <text x="485" y="224" class="msg-text">2: validate_finite_and_ranges(request: RecommendRequest)</text>

  <rect x="110" y="250" width="410" height="70" class="frame-box"/>
  <rect x="110" y="250" width="40" height="20" class="frame-tag"/>
  <text x="118" y="265" class="frame-tag-text">alt</text>
  <text x="160" y="266" class="frame-guard">[Soil_pH &lt; 0 or &gt; 14 or N,P,K &lt; 0]</text>
  <line x1="423" y1="295" x2="167" y2="295" class="msg-return"/>
  <text x="195" y="289" class="msg-ret-text">3: HTTP 422 Unprocessable Entity (ValidationError)</text>

  <line x1="437" y1="335" x2="713" y2="335" class="msg-sync"/>
  <text x="450" y="328" class="msg-text">4: predict(ml_payload: dict)</text>

  <line x1="727" y1="365" x2="993" y2="365" class="msg-sync"/>
  <text x="740" y="358" class="msg-text">5: can_execute()</text>

  <path d="M 1007 375 L 1040 375 L 1040 395 L 1007 395" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1050" y="389" class="msg-text" style="font-size: 10px;">async with self._lock: state == CLOSED</text>

  <line x1="993" y1="410" x2="727" y2="410" class="msg-return"/>
  <text x="780" y="403" class="msg-ret-text">6: return True (Execution permitted)</text>

  <path d="M 727 430 L 760 430 L 760 450 L 727 450" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="770" y="444" class="msg-text">7: _get_client(): httpx.AsyncClient (pool)</text>

  <line x1="727" y1="475" x2="1283" y2="475" class="msg-sync"/>
  <text x="740" y="468" class="msg-text">8: async POST /predict (JSON: Soil_pH, N, P, K, Crop_Growth_Stage)</text>

  <line x1="1297" y1="510" x2="1563" y2="510" class="msg-sync"/>
  <text x="1310" y="503" class="msg-text">9: load_bundle(version=None)</text>

  <line x1="1563" y1="545" x2="1297" y2="545" class="msg-return"/>
  <text x="1320" y="538" class="msg-ret-text">10: return ModelBundle(pipeline, label_encoder, metadata)</text>

  <path d="M 1297 565 L 1335 565 L 1335 590 L 1297 590" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1345" y="582" class="msg-text">11: df_input = pd.DataFrame(ordered_features)</text>

  <path d="M 1297 605 L 1335 605 L 1335 630 L 1297 630" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1345" y="622" class="msg-text">12: raw_pred = bundle.pipeline.predict(df_input) -> [3]</text>

  <path d="M 1297 645 L 1335 645 L 1335 670 L 1297 670" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1345" y="662" class="msg-text">13: label = bundle.label_encoder.inverse_transform([3]) -> "DAP"</text>

  <path d="M 1297 685 L 1335 685 L 1335 710 L 1297 710" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1345" y="702" class="msg-text">14: probas = bundle.pipeline.predict_proba(df_input) -> confidence: 0.942</text>

  <line x1="1283" y1="765" x2="727" y2="765" class="msg-return"/>
  <text x="750" y="758" class="msg-ret-text">15: HTTP 200 OK {{'fertilizer':'DAP', 'confidence':0.942, 'model_version':'v1.0.0', 'probabilities':{{..}}}}</text>

  <line x1="727" y1="835" x2="993" y2="835" class="msg-sync"/>
  <text x="740" y="828" class="msg-text">16: record_success()</text>

  <path d="M 1007 845 L 1035 845 L 1035 865 L 1007 865" fill="none" stroke="#1E293B" stroke-width="1.4" marker-end="url(#self-arrow)"/>
  <text x="1045" y="859" class="msg-text" style="font-size: 10px;">failure_count = 0; state = CLOSED</text>

  <line x1="713" y1="895" x2="437" y2="895" class="msg-return"/>
  <text x="460" y="888" class="msg-ret-text">17: return ml_result dict (latency_ms = 38.4ms)</text>

  <rect x="370" y="920" width="1760" height="195" class="frame-box"/>
  <rect x="370" y="920" width="40" height="20" class="frame-tag"/>
  <text x="378" y="935" class="frame-tag-text">par</text>
  <text x="420" y="936" class="frame-guard">[Parallel Execution: Database Persistence &amp; Metrics Telemetry]</text>

  <line x1="437" y1="960" x2="1833" y2="960" class="msg-sync"/>
  <text x="450" y="953" class="msg-text">18a: log_prediction(input_features, "DAP", confidence=0.942, latency_ms=38.4, status="success")</text>

  <path d="M 1847 975 L 1880 975 L 1880 1000 L 1847 1000" fill="none" stroke="#1E293B" stroke-width="1.5" marker-end="url(#self-arrow)"/>
  <text x="1890" y="992" class="msg-text">PredictionRecord.create() -> SQL INSERT</text>

  <line x1="1833" y1="1015" x2="437" y2="1015" class="msg-return"/>
  <text x="470" y="1008" class="msg-ret-text">18b: return prediction_id = "pred_a8f9c2e4"</text>

  <line x1="370" y1="1035" x2="2130" y2="1035" class="frame-divider"/>

  <line x1="437" y1="1065" x2="2053" y2="1065" class="msg-async"/>
  <text x="450" y="1058" class="msg-text" style="fill:#2563EB;">19: record_prediction(status="success", fertilizer="DAP", latency_ms=38.4)</text>

  <line x1="423" y1="1145" x2="167" y2="1145" class="msg-return"/>
  <text x="185" y="1138" class="msg-ret-text" style="font-weight: bold; fill: #065F46;">20: HTTP 200 OK RecommendResponse(success=True, fertilizer="DAP", confidence=0.942, prediction_id="pred_a8f9c2e4")</text>

  <path d="M 167 1165 L 210 1165 L 210 1195 L 167 1195" fill="none" stroke="#1E293B" stroke-width="1.6" marker-end="url(#self-arrow)"/>
  <text x="220" y="1184" class="msg-text">21: renderPrescriptionCard("DAP", 94.2%, NPK_Advice)</text>

  <g transform="translate(160, 1260)"><rect x="-70" y="0" width="140" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">Farmer / UI</text></g>
  <g transform="translate(430, 1260)"><rect x="-80" y="0" width="160" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">RecommendationCtrl</text></g>
  <g transform="translate(720, 1260)"><rect x="-60" y="0" width="120" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">MLClient</text></g>
  <g transform="translate(1000, 1260)"><rect x="-65" y="0" width="130" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">CircuitBreaker</text></g>
  <g transform="translate(1290, 1260)"><rect x="-75" y="0" width="150" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">FertilizerPredictor</text></g>
  <g transform="translate(1570, 1260)"><rect x="-65" y="0" width="130" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">ModelRegistry</text></g>
  <g transform="translate(1840, 1260)"><rect x="-70" y="0" width="140" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">DatabaseManager</text></g>
  <g transform="translate(2060, 1260)"><rect x="-70" y="0" width="140" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size: 11px;">Prometheus</text></g>

  <g transform="translate(60, 1315)">
    <rect width="2080" height="55" class="legend-box"/>
    <text x="20" y="24" class="legend-text" font-weight="bold">UML 2.5 Sequence Notation Legend:</text>
    <line x1="260" y1="20" x2="310" y2="20" class="msg-sync"/>
    <text x="320" y="24" class="legend-text">Synchronous Call (Filled Arrowhead)</text>
    <line x1="600" y1="20" x2="650" y2="20" class="msg-async"/>
    <text x="660" y="24" class="legend-text">Asynchronous Signal (Open Arrowhead)</text>
    <line x1="960" y1="20" x2="1010" y2="20" class="msg-return"/>
    <text x="1020" y="24" class="legend-text">Reply / Return Message (Dashed Line)</text>
    <rect x="1330" y="10" width="14" height="22" class="act-bar"/>
    <text x="1355" y="24" class="legend-text">Execution Specification (Activation Bar)</text>
    <rect x="1660" y="8" width="50" height="26" class="frame-box"/>
    <text x="1665" y="24" class="legend-text" font-weight="bold">alt / par</text>
    <text x="1725" y="24" class="legend-text">Combined Interaction Fragments</text>
  </g>
</svg>
"""
    return svg

# -------------------------------------------------------------
# 2. SEQUENCE DIAGRAM 2: RESILIENCY & CIRCUIT BREAKER
# -------------------------------------------------------------
def get_seq_diag_2():
    w, h = 2200, 1500
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <filter id="shadow2" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    
    <marker id="sync-arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>

    <marker id="return-arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9" fill="none" stroke="#475569" stroke-width="1.8" stroke-linecap="round"/>
    </marker>

    <marker id="fail-x" viewBox="0 0 12 12" refX="6" refY="6" markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 2 2 L 10 10 M 10 2 L 2 10" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round"/>
    </marker>

    <marker id="self-arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>
  </defs>

  <style>
    .title-main {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #0f172a; }}
    .title-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: 500; fill: #475569; }}
    
    .lifeline-name {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: bold; text-anchor: middle; }}
    .lifeline-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-style: italic; text-anchor: middle; fill: #64748B; }}
    .lifeline-line {{ stroke: #94A3B8; stroke-width: 1.5px; stroke-dasharray: 6,6; }}
    
    .act-bar {{ fill: #E2E8F0; stroke: #475569; stroke-width: 1.2px; rx: 3px; }}
    .act-bar-focus {{ fill: #BAE6FD; stroke: #0284C7; stroke-width: 1.4px; rx: 3px; }}
    .act-bar-warn  {{ fill: #FED7AA; stroke: #EA580C; stroke-width: 1.4px; rx: 3px; }}
    .act-bar-err   {{ fill: #FECACA; stroke: #DC2626; stroke-width: 1.4px; rx: 3px; }}

    .msg-sync   {{ stroke: #1E293B; stroke-width: 1.8px; marker-end: url(#sync-arrow2); }}
    .msg-return {{ stroke: #475569; stroke-width: 1.6px; stroke-dasharray: 6,4; marker-end: url(#return-arrow2); }}
    .msg-fail   {{ stroke: #DC2626; stroke-width: 1.8px; stroke-dasharray: 4,4; marker-end: url(#fail-x); }}
    
    .msg-text {{ font-family: 'Consolas', 'Segoe UI', monospace; font-size: 11px; fill: #0F172A; font-weight: 600; }}
    .msg-ret-text {{ font-family: 'Consolas', 'Segoe UI', monospace; font-size: 10.5px; fill: #475569; font-style: italic; }}
    .msg-err-text {{ font-family: 'Consolas', 'Segoe UI', monospace; font-size: 11px; fill: #DC2626; font-weight: bold; }}

    .frame-box {{ fill: #F8FAFC; fill-opacity: 0.65; stroke: #64748B; stroke-width: 1.5px; rx: 5px; }}
    .frame-tag {{ fill: #334155; rx: 3px; }}
    .frame-tag-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #FFFFFF; }}
    .frame-guard {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; font-weight: bold; fill: #1E3A8A; }}
    .frame-divider {{ stroke: #64748B; stroke-width: 1.2px; stroke-dasharray: 8,6; }}
    
    .state-badge {{ rx: 4px; stroke-width: 1.2px; }}
    .state-text  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; font-weight: bold; text-anchor: middle; }}

    .legend-box {{ fill: #F1F5F9; stroke: #CBD5E1; stroke-width: 1px; rx: 6px; }}
    .legend-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #334155; }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <rect x="15" y="15" width="{w-30}" height="{h-30}" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- Header Banner -->
  <g transform="translate({w/2}, 42)">
    <text class="title-main" text-anchor="middle">Fieldwise: Fault Tolerance &amp; Resiliency Modeling</text>
    <text class="title-sub" y="24" text-anchor="middle">UML 2.5 Sequence Diagram 2: Exponential Backoff Retries, Circuit Breaker Tripping &amp; Half-Open Probe Recovery</text>
  </g>

  <!-- Lifeline 1: Client -->
  <g transform="translate(200, 95)">
    <rect x="-90" y="0" width="180" height="52" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#1E3A8A">:Client / Farmer</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Actor / Mobile or Web&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Lifeline 2: RecommendationController -->
  <g transform="translate(560, 95)">
    <rect x="-110" y="0" width="220" height="52" fill="#ECFDF5" stroke="#10B981" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#065F46">:RecommendationController</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Boundary / REST Controller&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Lifeline 3: MLClient -->
  <g transform="translate(960, 95)">
    <rect x="-95" y="0" width="190" height="52" fill="#EEF2FF" stroke="#6366F1" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#312E81">:MLClient</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Service / Resilient Adapter&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Lifeline 4: CircuitBreaker -->
  <g transform="translate(1360, 95)">
    <rect x="-105" y="0" width="210" height="52" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#78350F">:CircuitBreaker</text>
    <text y="38" class="lifeline-sub">&lt;&lt;FSM / State Monitor&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Lifeline 5: FertilizerPredictor (Degraded) -->
  <g transform="translate(1760, 95)">
    <rect x="-115" y="0" width="230" height="52" fill="#FEF2F2" stroke="#EF4444" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#991B1B">:FertilizerPredictor</text>
    <text y="38" class="lifeline-sub">&lt;&lt;ML Service Engine (Failing)&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Lifeline 6: DatabaseManager -->
  <g transform="translate(2020, 95)">
    <rect x="-85" y="0" width="170" height="52" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.8" rx="6" filter="url(#shadow2)"/>
    <text y="22" class="lifeline-name" fill="#134E4A">:DatabaseManager</text>
    <text y="38" class="lifeline-sub">&lt;&lt;Data Access / Peewee&gt;&gt;</text>
    <line x1="0" y1="52" x2="0" y2="1330" class="lifeline-line"/>
  </g>

  <!-- Initial State Badge: CLOSED -->
  <g transform="translate(1360, 160)">
    <rect x="-45" y="0" width="90" height="20" fill="#DCFCE7" stroke="#16A34A" class="state-badge"/>
    <text y="14" class="state-text" fill="#15803D">State: CLOSED</text>
  </g>

  <!-- Phase 1: Retries & Tripping -->
  <line x1="200" y1="195" x2="553" y2="195" class="msg-sync"/>
  <text x="220" y="188" class="msg-text">1: POST /api/v1/fertilizer/recommend (Soil_pH=6.5, N=120, P=45, K=60)</text>

  <rect x="553" y="195" width="14" height="420" class="act-bar"/>
  <line x1="567" y1="215" x2="953" y2="215" class="msg-sync"/>
  <text x="580" y="208" class="msg-text">2: predict(ml_payload)</text>

  <rect x="953" y="215" width="14" height="380" class="act-bar-warn"/>

  <line x1="967" y1="235" x2="1353" y2="235" class="msg-sync"/>
  <text x="980" y="228" class="msg-text">3: can_execute()</text>

  <rect x="1353" y="235" width="14" height="30" class="act-bar"/>
  <line x1="1353" y1="260" x2="967" y2="260" class="msg-return"/>
  <text x="1000" y="253" class="msg-ret-text">4: return True [State == CLOSED, failure_count = 4]</text>

  <rect x="900" y="280" width="940" height="190" class="frame-box"/>
  <rect x="900" y="280" width="45" height="20" class="frame-tag"/>
  <text x="908" y="295" class="frame-tag-text">loop</text>
  <text x="955" y="296" class="frame-guard">[attempt = 1 to 3, max_retries = 3]</text>

  <line x1="967" y1="315" x2="1750" y2="315" class="msg-fail"/>
  <text x="980" y="308" class="msg-err-text">5a: POST /predict (attempt 1) -> httpx.ConnectError / Timeout (10.0s)</text>

  <path d="M 967 330 L 1005 330 L 1005 350 L 967 350" fill="none" stroke="#EA580C" stroke-width="1.4" marker-end="url(#self-arrow2)"/>
  <text x="1015" y="344" class="msg-text" style="fill:#EA580C;">sleep(base_delay * 2^0 = 0.5s + jitter)</text>

  <line x1="967" y1="375" x2="1750" y2="375" class="msg-fail"/>
  <text x="980" y="368" class="msg-err-text">5b: POST /predict (attempt 2) -> HTTP 504 Gateway Timeout</text>

  <path d="M 967 390 L 1005 390 L 1005 410 L 967 410" fill="none" stroke="#EA580C" stroke-width="1.4" marker-end="url(#self-arrow2)"/>
  <text x="1015" y="404" class="msg-text" style="fill:#EA580C;">sleep(base_delay * 2^1 = 1.0s + jitter)</text>

  <line x1="967" y1="435" x2="1750" y2="435" class="msg-fail"/>
  <text x="980" y="428" class="msg-err-text">5c: POST /predict (attempt 3) -> Connection Refused / Service Unreachable</text>

  <line x1="967" y1="490" x2="1353" y2="490" class="msg-sync"/>
  <text x="980" y="483" class="msg-text">6: record_failure()</text>

  <rect x="1353" y="490" width="14" height="65" class="act-bar-err"/>
  
  <path d="M 1367 505 L 1410 505 L 1410 535 L 1367 535" fill="none" stroke="#DC2626" stroke-width="1.6" marker-end="url(#self-arrow2)"/>
  <text x="1420" y="518" class="msg-err-text">failure_count (5) >= threshold (5)</text>
  <text x="1420" y="534" class="msg-err-text">transitionState(CLOSED ➔ OPEN)</text>

  <g transform="translate(1360, 565)">
    <rect x="-40" y="0" width="80" height="20" fill="#FEE2E2" stroke="#DC2626" class="state-badge"/>
    <text y="14" class="state-text" fill="#B91C1C">State: OPEN</text>
  </g>

  <line x1="953" y1="585" x2="567" y2="585" class="msg-return" style="stroke:#DC2626;"/>
  <text x="590" y="578" class="msg-err-text">7: raise MLServiceError("ML service unavailable", status_code=503)</text>

  <line x1="567" y1="605" x2="2013" y2="605" class="msg-sync"/>
  <text x="580" y="598" class="msg-text">8: log_prediction(features, predicted="N/A", status="error", error_message="MLServiceError: 503")</text>

  <line x1="553" y1="625" x2="200" y2="625" class="msg-return" style="stroke:#DC2626;"/>
  <text x="220" y="618" class="msg-err-text">9: HTTP 503 Service Unavailable (Fallback Agronomic Advisory)</text>

  <!-- Phase 2: Fast Fail -->
  <g transform="translate(1100, 670)">
    <rect x="-450" y="0" width="900" height="28" fill="#FEF3C7" stroke="#F59E0B" rx="5"/>
    <text y="19" class="msg-text" text-anchor="middle" style="fill:#B45309; font-size:12px;">TIME ADVANCES: Subsequent Request arrives while Circuit is OPEN (within 30s Cooldown)</text>
  </g>

  <line x1="200" y1="720" x2="553" y2="720" class="msg-sync"/>
  <text x="220" y="713" class="msg-text">10: POST /api/v1/fertilizer/recommend (Soil_pH=7.1, N=80, P=30, K=40)</text>

  <rect x="553" y="720" width="14" height="150" class="act-bar"/>
  <line x1="567" y1="740" x2="953" y2="740" class="msg-sync"/>
  <text x="580" y="733" class="msg-text">11: predict(ml_payload)</text>

  <rect x="953" y="740" width="14" height="110" class="act-bar"/>
  <line x1="967" y1="760" x2="1353" y2="760" class="msg-sync"/>
  <text x="980" y="753" class="msg-text">12: can_execute()</text>

  <rect x="1353" y="760" width="14" height="40" class="act-bar-err"/>
  <path d="M 1367 770 L 1400 770 L 1400 790 L 1367 790" fill="none" stroke="#DC2626" stroke-width="1.4" marker-end="url(#self-arrow2)"/>
  <text x="1410" y="784" class="msg-err-text">elapsed (12.4s) &lt; cooldown (30.0s)</text>

  <line x1="1353" y1="805" x2="967" y2="805" class="msg-return" style="stroke:#DC2626;"/>
  <text x="1000" y="798" class="msg-err-text">13: return False [State == OPEN]</text>

  <line x1="953" y1="835" x2="567" y2="835" class="msg-return" style="stroke:#DC2626;"/>
  <text x="580" y="828" class="msg-err-text">14: fast-fail: raise MLServiceError("Circuit is OPEN", status_code=503) [Latency &lt; 2ms]</text>

  <line x1="553" y1="865" x2="200" y2="865" class="msg-return" style="stroke:#DC2626;"/>
  <text x="220" y="858" class="msg-err-text">15: HTTP 503 (Fast-Fail Response: Downstream Service Isolated)</text>

  <!-- Phase 3: Cooldown & Recovery -->
  <g transform="translate(1100, 915)">
    <rect x="-450" y="0" width="900" height="28" fill="#E0F2FE" stroke="#0284C7" rx="5"/>
    <text y="19" class="msg-text" text-anchor="middle" style="fill:#0369A1; font-size:12px;">TIME ADVANCES: 31 seconds pass (Cooldown expired: elapsed &gt;= 30.0s)</text>
  </g>

  <line x1="200" y1="965" x2="553" y2="965" class="msg-sync"/>
  <text x="220" y="958" class="msg-text">16: POST /api/v1/fertilizer/recommend (Soil_pH=6.8, N=110, P=40, K=55)</text>

  <rect x="553" y="965" width="14" height="320" class="act-bar-focus"/>
  <line x1="567" y1="985" x2="953" y2="985" class="msg-sync"/>
  <text x="580" y="978" class="msg-text">17: predict(ml_payload)</text>

  <rect x="953" y="985" width="14" height="275" class="act-bar"/>
  <line x1="967" y1="1005" x2="1353" y2="1005" class="msg-sync"/>
  <text x="980" y="998" class="msg-text">18: can_execute()</text>

  <rect x="1353" y="1005" width="14" height="55" class="act-bar-warn"/>
  <path d="M 1367 1015 L 1405 1015 L 1405 1040 L 1367 1040" fill="none" stroke="#D97706" stroke-width="1.5" marker-end="url(#self-arrow2)"/>
  <text x="1415" y="1026" class="msg-text" style="fill:#D97706;">elapsed (31.2s) &gt;= cooldown (30.0s)</text>
  <text x="1415" y="1042" class="msg-text" style="fill:#D97706;">transitionState(OPEN ➔ HALF_OPEN)</text>

  <line x1="1353" y1="1060" x2="967" y2="1060" class="msg-return"/>
  <text x="990" y="1053" class="msg-ret-text">19: return True (Trial Probe Request Allowed)</text>

  <g transform="translate(1360, 1075)">
    <rect x="-55" y="0" width="110" height="20" fill="#FEF3C7" stroke="#D97706" class="state-badge"/>
    <text y="14" class="state-text" fill="#92400E">State: HALF_OPEN</text>
  </g>

  <line x1="967" y1="1115" x2="1753" y2="1115" class="msg-sync"/>
  <text x="980" y="1108" class="msg-text" style="fill:#065F46;">20: Trial Probe: POST /predict (Downstream Service Restored)</text>

  <rect x="1753" y="1115" width="14" height="40" class="act-bar"/>
  <line x1="1753" y1="1145" x2="967" y2="1145" class="msg-return" style="stroke:#16A34A;"/>
  <text x="990" y="1138" class="msg-ret-text" style="fill:#16A34A; font-weight:bold;">21: HTTP 200 OK {{'fertilizer':'Urea', 'confidence':0.965}}</text>

  <line x1="967" y1="1180" x2="1353" y2="1180" class="msg-sync"/>
  <text x="980" y="1173" class="msg-text">22: record_success()</text>

  <rect x="1353" y="1180" width="14" height="45" class="act-bar"/>
  <path d="M 1367 1190 L 1405 1190 L 1405 1210 L 1367 1210" fill="none" stroke="#16A34A" stroke-width="1.5" marker-end="url(#self-arrow2)"/>
  <text x="1415" y="1204" class="msg-text" style="fill:#16A34A;">failure_count = 0; transitionState(HALF_OPEN ➔ CLOSED)</text>

  <g transform="translate(1360, 1235)">
    <rect x="-45" y="0" width="90" height="20" fill="#DCFCE7" stroke="#16A34A" class="state-badge"/>
    <text y="14" class="state-text" fill="#15803D">State: CLOSED</text>
  </g>

  <line x1="953" y1="1235" x2="567" y2="1235" class="msg-return"/>
  <text x="600" y="1228" class="msg-ret-text">23: return ml_result (Service fully operational)</text>

  <line x1="553" y1="1265" x2="200" y2="1265" class="msg-return" style="stroke:#16A34A;"/>
  <text x="220" y="1258" class="msg-ret-text" style="font-weight:bold; fill:#065F46;">24: HTTP 200 OK RecommendResponse(success=True, fertilizer="Urea", confidence=0.965)</text>

  <!-- Bottom Timeline -->
  <g transform="translate(200, 1350)"><rect x="-70" y="0" width="140" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">Client / Farmer</text></g>
  <g transform="translate(560, 1350)"><rect x="-80" y="0" width="160" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">RecommendationCtrl</text></g>
  <g transform="translate(960, 1350)"><rect x="-60" y="0" width="120" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">MLClient</text></g>
  <g transform="translate(1360, 1350)"><rect x="-65" y="0" width="130" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">CircuitBreaker</text></g>
  <g transform="translate(1760, 1350)"><rect x="-75" y="0" width="150" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">FertilizerPredictor</text></g>
  <g transform="translate(2020, 1350)"><rect x="-70" y="0" width="140" height="26" fill="#F8FAFC" stroke="#94A3B8" rx="4"/><text y="18" class="lifeline-name" fill="#475569" style="font-size:11px;">DatabaseManager</text></g>

  <!-- Legend -->
  <g transform="translate(60, 1410)">
    <rect width="2080" height="55" class="legend-box"/>
    <text x="20" y="24" class="legend-text" font-weight="bold">Resiliency States &amp; Notations:</text>
    <rect x="230" y="10" width="80" height="20" fill="#DCFCE7" stroke="#16A34A" class="state-badge"/>
    <text x="270" y="24" class="state-text" fill="#15803D">CLOSED (Normal)</text>
    <rect x="420" y="10" width="80" height="20" fill="#FEE2E2" stroke="#DC2626" class="state-badge"/>
    <text x="460" y="24" class="state-text" fill="#B91C1C">OPEN (Tripped)</text>
    <rect x="610" y="10" width="95" height="20" fill="#FEF3C7" stroke="#D97706" class="state-badge"/>
    <text x="657" y="24" class="state-text" fill="#92400E">HALF_OPEN (Probe)</text>
    <line x1="820" y1="20" x2="860" y2="20" class="msg-fail"/>
    <text x="870" y="24" class="legend-text">Failed Invocations (Timeout / Refused)</text>
    <rect x="1160" y="8" width="40" height="24" class="frame-box"/>
    <text x="1165" y="24" class="legend-text" font-weight="bold">loop</text>
    <text x="1210" y="24" class="legend-text">Exponential Backoff Iteration Loop</text>
    <text x="1560" y="24" class="legend-text" font-style="italic">Failure Threshold: 5 | Cooldown: 30.0s | Max Retries: 3 (0.5s, 1.0s, 2.0s)</text>
  </g>
</svg>
"""
    return svg

# -------------------------------------------------------------
# 3. ACTIVITY DIAGRAM 1: COMPREHENSIVE WORKFLOW (PARALLEL LANE 5)
# -------------------------------------------------------------
def get_act_diag_1():
    w, h = 2400, 1550
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <filter id="shadow3" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>

    <marker id="act-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>

    <marker id="err-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#DC2626"/>
    </marker>
  </defs>

  <style>
    .title-main {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #0f172a; }}
    .title-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: 500; fill: #475569; }}
    
    .lane-bg-1 {{ fill: #F8FAFC; }}
    .lane-bg-2 {{ fill: #F0FDF4; }}
    .lane-bg-3 {{ fill: #EEF2FF; }}
    .lane-bg-4 {{ fill: #FAF5FF; }}
    .lane-bg-5 {{ fill: #F0FDFA; }}
    
    .lane-border {{ stroke: #CBD5E1; stroke-width: 1.5px; }}
    .lane-hdr-txt {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; font-weight: bold; text-anchor: middle; }}
    
    .act-node {{ rx: 16px; stroke-width: 1.6px; filter: url(#shadow3); }}
    .act-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; font-weight: 600; text-anchor: middle; }}
    .act-text-sm {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; text-anchor: middle; fill: #475569; }}

    .obj-node {{ rx: 4px; stroke-width: 1.4px; stroke-dasharray: 4,3; filter: url(#shadow3); }}
    .obj-text {{ font-family: 'Consolas', monospace; font-size: 10.5px; text-anchor: middle; font-weight: bold; }}

    .flow-line {{ fill: none; stroke: #1E293B; stroke-width: 1.8px; marker-end: url(#act-arrow); }}
    .flow-line-err {{ fill: none; stroke: #DC2626; stroke-width: 1.8px; stroke-dasharray: 5,4; marker-end: url(#err-arrow); }}
    
    .guard-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #1E3A8A; }}
    .guard-err  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #B91C1C; }}

    .fork-bar {{ fill: #0F172A; rx: 3px; }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <rect x="15" y="15" width="{w-30}" height="{h-30}" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- Header Banner -->
  <g transform="translate({w/2}, 42)">
    <text class="title-main" text-anchor="middle">Fieldwise: Operational Activity Workflow Modeling</text>
    <text class="title-sub" y="24" text-anchor="middle">UML 2.5 Activity Diagram 1: End-to-End Soil Ingestion, Resiliency Validation, ML Inference &amp; Telemetry Swimlanes</text>
  </g>

  <!-- Swimlanes -->
  <rect x="40" y="85" width="440" height="1370" class="lane-bg-1"/>
  <rect x="40" y="85" width="440" height="42" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="260" y="112" class="lane-hdr-txt" fill="#1E293B">Swimlane 1: Farmer / Client Interface</text>

  <rect x="480" y="85" width="480" height="1370" class="lane-bg-2"/>
  <rect x="480" y="85" width="480" height="42" fill="#DCFCE7" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="720" y="112" class="lane-hdr-txt" fill="#065F46">Swimlane 2: API Gateway (RecommendationController)</text>

  <rect x="960" y="85" width="480" height="1370" class="lane-bg-3"/>
  <rect x="960" y="85" width="480" height="42" fill="#E0E7FF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="1200" y="112" class="lane-hdr-txt" fill="#312E81">Swimlane 3: Resiliency Guard (MLClient &amp; CircuitBreaker)</text>

  <rect x="1440" y="85" width="480" height="1370" class="lane-bg-4"/>
  <rect x="1440" y="85" width="480" height="42" fill="#F3E8FF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="1680" y="112" class="lane-hdr-txt" fill="#581C87">Swimlane 4: ML Inference Engine (FertilizerPredictor :8001)</text>

  <rect x="1920" y="85" width="440" height="1370" class="lane-bg-5"/>
  <rect x="1920" y="85" width="440" height="42" fill="#CCFBF1" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="2140" y="112" class="lane-hdr-txt" fill="#134E4A">Swimlane 5: Persistence &amp; Metrics Telemetry</text>

  <!-- Dividers -->
  <line x1="480" y1="85" x2="480" y2="1455" class="lane-border"/>
  <line x1="960" y1="85" x2="960" y2="1455" class="lane-border"/>
  <line x1="1440" y1="85" x2="1440" y2="1455" class="lane-border"/>
  <line x1="1920" y1="85" x2="1920" y2="1455" class="lane-border"/>

  <!-- Initial Node -->
  <circle cx="260" cy="165" r="14" fill="#0F172A"/>

  <!-- Action 1 -->
  <g transform="translate(260, 225)">
    <rect x="-140" y="-24" width="280" height="48" fill="#EFF6FF" stroke="#3B82F6" class="act-node"/>
    <text y="-4" class="act-text" fill="#1E3A8A">Enter Soil Metrics &amp; Growth Stage</text>
    <text y="12" class="act-text-sm">pH, Nitrogen, Phosphorus, Potassium, Moisture</text>
  </g>
  <line x1="260" y1="179" x2="260" y2="201" class="flow-line"/>

  <!-- Action 2 -->
  <g transform="translate(260, 315)">
    <rect x="-120" y="-22" width="240" height="44" fill="#EFF6FF" stroke="#3B82F6" class="act-node"/>
    <text y="5" class="act-text" fill="#1E3A8A">Submit Recommendation Form</text>
  </g>
  <line x1="260" y1="249" x2="260" y2="293" class="flow-line"/>

  <!-- Flow to Lane 2 -->
  <path d="M 380 315 L 720 315 L 720 355" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  <text x="430" y="307" class="guard-text">HTTP POST /api/v1/fertilizer/recommend</text>

  <!-- Action 3 -->
  <g transform="translate(720, 385)">
    <rect x="-140" y="-24" width="280" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Ingest Payload &amp; Assign UUID</text>
    <text y="12" class="act-text-sm">Extract request_id from headers or uuid4()</text>
  </g>

  <!-- Action 4 -->
  <g transform="translate(720, 470)">
    <rect x="-140" y="-24" width="280" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Validate Pydantic Boundary Schema</text>
    <text y="12" class="act-text-sm">Enforce [0 &lt;= pH &lt;= 14], N,P,K &gt;= 0, finite floats</text>
  </g>
  <line x1="720" y1="409" x2="720" y2="446" class="flow-line"/>

  <!-- Decision Node 1 -->
  <polygon points="720,535 755,560 720,585 685,560" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="720" y1="494" x2="720" y2="535" class="flow-line"/>

  <!-- Branch 1a: Invalid -->
  <path d="M 685 560 L 260 560 L 260 620" fill="none" stroke="#DC2626" stroke-width="1.8" marker-end="url(#err-arrow)"/>
  <text x="350" y="552" class="guard-err">[Validation Fails: Out of Bounds]</text>

  <g transform="translate(260, 645)">
    <rect x="-130" y="-22" width="260" height="44" fill="#FEE2E2" stroke="#DC2626" class="act-node"/>
    <text y="5" class="act-text" fill="#991B1B">Display 422 Validation Error Alert</text>
  </g>
  
  <circle cx="260" cy="725" r="14" fill="#FFFFFF" stroke="#DC2626" stroke-width="2"/>
  <line x1="250" y1="715" x2="270" y2="735" stroke="#DC2626" stroke-width="2"/>
  <line x1="270" y1="715" x2="250" y2="735" stroke="#DC2626" stroke-width="2"/>
  <line x1="260" y1="667" x2="260" y2="711" class="flow-line-err"/>

  <!-- Branch 1b: Valid -->
  <line x1="755" y1="560" x2="830" y2="560" class="flow-line"/>
  <text x="760" y="552" class="guard-text">[Valid Inputs]</text>

  <!-- Object Node -->
  <g transform="translate(830, 560)">
    <rect x="0" y="-18" width="165" height="36" fill="#FEF9C3" stroke="#CA8A04" class="obj-node"/>
    <text x="82" y="4" class="obj-text" fill="#854D0E">RecommendRequest [DTO]</text>
  </g>

  <path d="M 995 560 L 1200 560 L 1200 600" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>

  <!-- Action 5: Query Circuit Breaker -->
  <g transform="translate(1200, 630)">
    <rect x="-140" y="-24" width="280" height="48" fill="#EEF2FF" stroke="#6366F1" class="act-node"/>
    <text y="-4" class="act-text" fill="#312E81">Acquire Lock &amp; Check Circuit State</text>
    <text y="12" class="act-text-sm">async with _lock: evaluate can_execute()</text>
  </g>

  <!-- Decision Node 2: Circuit State? -->
  <polygon points="1200,690 1240,715 1200,740 1160,715" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="1200" y1="654" x2="1200" y2="690" class="flow-line"/>

  <!-- Branch 2a: OPEN -> Fallback Route -->
  <path d="M 1160 715 L 720 715 L 720 755" fill="none" stroke="#EA580C" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  <text x="820" y="707" class="guard-err" style="fill:#C2410C;">[Circuit == OPEN &amp; Cooldown Active]</text>

  <g transform="translate(720, 785)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FFF7ED" stroke="#EA580C" class="act-node"/>
    <text y="-4" class="act-text" fill="#9A3412">Execute Agronomic Fallback Rules</text>
    <text y="12" class="act-text-sm">Return safe baseline advisory (e.g. NPK 10:26:26)</text>
  </g>

  <path d="M 720 809 L 720 850 L 260 850 L 260 885" fill="none" stroke="#EA580C" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  
  <g transform="translate(260, 915)">
    <rect x="-130" y="-22" width="260" height="44" fill="#FFF7ED" stroke="#EA580C" class="act-node"/>
    <text y="5" class="act-text" fill="#9A3412">Display Fallback Advisory Banner</text>
  </g>

  <!-- Branch 2b: CLOSED / HALF_OPEN -> Proceed to ML Service -->
  <line x1="1240" y1="715" x2="1680" y2="715" class="flow-line"/>
  <text x="1270" y="707" class="guard-text">[CLOSED or HALF_OPEN: Allowed]</text>

  <!-- Action 6: Load Bundle in Lane 4 -->
  <g transform="translate(1680, 785)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FAF5FF" stroke="#8B5CF6" class="act-node"/>
    <text y="-4" class="act-text" fill="#581C87">Load ModelBundle from Registry</text>
    <text y="12" class="act-text-sm">Cache lookup for active sklearn pipeline &amp; encoder</text>
  </g>
  <line x1="1680" y1="715" x2="1680" y2="761" class="flow-line"/>

  <!-- Action 7: DataFrame & Feature Pipeline -->
  <g transform="translate(1680, 870)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FAF5FF" stroke="#8B5CF6" class="act-node"/>
    <text y="-4" class="act-text" fill="#581C87">Construct Ordered Pandas DataFrame</text>
    <text y="12" class="act-text-sm">Order: Soil_pH, N, P, K, Crop_Growth_Stage</text>
  </g>
  <line x1="1680" y1="809" x2="1680" y2="846" class="flow-line"/>

  <!-- Action 8: Execute XGBoost Inference & Label Decoding -->
  <g transform="translate(1680, 955)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FAF5FF" stroke="#8B5CF6" class="act-node"/>
    <text y="-4" class="act-text" fill="#581C87">Execute Pipeline.predict() &amp; Probas</text>
    <text y="12" class="act-text-sm">Decode label with LabelEncoder; compute confidence</text>
  </g>
  <line x1="1680" y1="894" x2="1680" y2="931" class="flow-line"/>

  <!-- Object Node: Positioned Cleanly below Action 8 at x=1680, y=1025 -->
  <g transform="translate(1680, 1025)">
    <rect x="-90" y="-18" width="180" height="36" fill="#FDF2F8" stroke="#DB2777" class="obj-node"/>
    <text y="5" class="obj-text" fill="#9D174D">InferenceResult [dict]</text>
  </g>
  <line x1="1680" y1="979" x2="1680" y2="1007" class="flow-line"/>

  <!-- Flow from Object Node to Lane 3 Action 9 (record_success) -->
  <path d="M 1590 1025 L 1200 1025 L 1200 1060" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>

  <!-- Action 9: Record Circuit Success in Lane 3 -->
  <g transform="translate(1200, 1085)">
    <rect x="-140" y="-22" width="280" height="44" fill="#EEF2FF" stroke="#6366F1" class="act-node"/>
    <text y="5" class="act-text" fill="#312E81">record_success(): Reset FSM to CLOSED</text>
  </g>

  <!-- Flow to Controller in Lane 2 -->
  <path d="M 1060 1085 L 720 1085 L 720 1130" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>

  <!-- FORK NODE: Parallel Execution in Lane 2 (y=1135) -->
  <rect x="520" y="1135" width="400" height="8" class="fork-bar"/>

  <!-- Parallel Branch A: Database Persistence -> Lane 5 (Left Box at x=2025) -->
  <path d="M 600 1143 L 600 1180 L 2025 1180 L 2025 1222" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  <text x="1100" y="1173" class="guard-text">[Thread A: Asynchronous Audit Logging]</text>

  <g transform="translate(2025, 1250)">
    <rect x="-95" y="-26" width="190" height="52" fill="#F0FDFA" stroke="#0D9488" class="act-node"/>
    <text y="-5" class="act-text" fill="#134E4A" style="font-size:10.5px;">log_prediction() in DB</text>
    <text y="11" class="act-text-sm">Insert features, label, latency</text>
  </g>

  <!-- Parallel Branch B: Prometheus Metrics -> Lane 5 (Right Box at x=2255) -->
  <path d="M 720 1143 L 720 1200 L 2255 1200 L 2255 1222" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  <text x="1450" y="1195" class="guard-text">[Thread B: Real-Time Observability Metrics]</text>

  <g transform="translate(2255, 1250)">
    <rect x="-95" y="-26" width="190" height="52" fill="#FEF2F2" stroke="#EF4444" class="act-node"/>
    <text y="-5" class="act-text" fill="#991B1B" style="font-size:10.5px;">record_prediction()</text>
    <text y="11" class="act-text-sm">Prometheus latency histogram</text>
  </g>

  <!-- Parallel Branch C: Serialize RecommendResponse -> Lane 2 -->
  <g transform="translate(720, 1250)">
    <rect x="-130" y="-24" width="260" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Construct RecommendResponse DTO</text>
    <text y="12" class="act-text-sm">success=True, fertilizer, confidence</text>
  </g>
  <line x1="840" y1="1143" x2="840" y2="1226" class="flow-line"/>

  <!-- JOIN NODE: Synchronize All Threads (y=1355) -->
  <rect x="520" y="1355" width="1800" height="8" class="fork-bar"/>
  
  <path d="M 720 1274 L 720 1355" fill="none" stroke="#1E293B" stroke-width="1.8"/>
  <path d="M 2025 1276 L 2025 1355" fill="none" stroke="#1E293B" stroke-width="1.8"/>
  <path d="M 2255 1276 L 2255 1355" fill="none" stroke="#1E293B" stroke-width="1.8"/>

  <!-- Return Flow to Client Lane 1 -->
  <path d="M 600 1363 L 600 1395 L 260 1395 L 260 1415" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow)"/>
  <text x="320" y="1388" class="guard-text">HTTP 200 OK (RecommendResponse)</text>

  <!-- Action 10: Render Prescription Card in Lane 1 -->
  <g transform="translate(260, 1445)">
    <rect x="-140" y="-24" width="280" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Render Prescription &amp; Dosing Guidance</text>
    <text y="12" class="act-text-sm">Display Fertilizer Name, Confidence %, Radar Chart</text>
  </g>

  <!-- Activity Final Node: Lane 1 (x=260, y=1515) -->
  <circle cx="260" cy="1515" r="14" fill="#FFFFFF" stroke="#0F172A" stroke-width="2"/>
  <circle cx="260" cy="1515" r="8" fill="#0F172A"/>

  <line x1="260" y1="1469" x2="260" y2="1501" class="flow-line"/>

  <!-- Fallback connection to Final Node -->
  <path d="M 260 937 L 260 1000 L 120 1000 L 120 1515 L 246 1515" fill="none" stroke="#EA580C" stroke-width="1.6" stroke-dasharray="6,4" marker-end="url(#act-arrow)"/>
</svg>
"""
    return svg

# -------------------------------------------------------------
# 4. ACTIVITY DIAGRAM 2: FEEDBACK & RETRAINING LIFECYCLE (POLISHED)
# -------------------------------------------------------------
def get_act_diag_2():
    w, h = 2200, 1450
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <filter id="shadow4" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>

    <marker id="act-arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#1E293B"/>
    </marker>

    <marker id="err-arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,1 10,5 0,9" fill="#DC2626"/>
    </marker>
  </defs>

  <style>
    .title-main {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #0f172a; }}
    .title-sub  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: 500; fill: #475569; }}
    
    .lane-bg-1 {{ fill: #F8FAFC; }}
    .lane-bg-2 {{ fill: #F0FDF4; }}
    .lane-bg-3 {{ fill: #FFFBEB; }}
    .lane-bg-4 {{ fill: #FAF5FF; }}
    
    .lane-border {{ stroke: #CBD5E1; stroke-width: 1.5px; }}
    .lane-hdr-txt {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; font-weight: bold; text-anchor: middle; }}
    
    .act-node {{ rx: 16px; stroke-width: 1.6px; filter: url(#shadow4); }}
    .act-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; font-weight: 600; text-anchor: middle; }}
    .act-text-sm {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; text-anchor: middle; fill: #475569; }}

    .obj-node {{ rx: 4px; stroke-width: 1.4px; stroke-dasharray: 4,3; filter: url(#shadow4); }}
    .obj-text {{ font-family: 'Consolas', monospace; font-size: 10.5px; text-anchor: middle; font-weight: bold; }}

    .flow-line {{ fill: none; stroke: #1E293B; stroke-width: 1.8px; marker-end: url(#act-arrow2); }}
    .flow-line-err {{ fill: none; stroke: #DC2626; stroke-width: 1.8px; stroke-dasharray: 5,4; marker-end: url(#err-arrow2); }}
    
    .guard-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #1E3A8A; }}
    .guard-err  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #B91C1C; }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <rect x="15" y="15" width="{w-30}" height="{h-30}" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- Header Banner -->
  <g transform="translate({w/2}, 42)">
    <text class="title-main" text-anchor="middle">Fieldwise: Model Governance &amp; Retraining Loop</text>
    <text class="title-sub" y="24" text-anchor="middle">UML 2.5 Activity Diagram 2: Ground-Truth Feedback Ingestion, Agronomic Verification, Drift Detection &amp; Automated MLOps</text>
  </g>

  <!-- Swimlanes -->
  <rect x="40" y="85" width="530" height="1320" class="lane-bg-1"/>
  <rect x="40" y="85" width="530" height="42" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="305" y="112" class="lane-hdr-txt" fill="#1E293B">Swimlane 1: Farmer / Field Operator</text>

  <rect x="570" y="85" width="530" height="1320" class="lane-bg-2"/>
  <rect x="570" y="85" width="530" height="42" fill="#DCFCE7" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="835" y="112" class="lane-hdr-txt" fill="#065F46">Swimlane 2: Feedback Router &amp; Persistence Engine</text>

  <rect x="1100" y="85" width="530" height="1320" class="lane-bg-3"/>
  <rect x="1100" y="85" width="530" height="42" fill="#FEF3C7" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="1365" y="112" class="lane-hdr-txt" fill="#92400E">Swimlane 3: Agronomist &amp; Domain Verification</text>

  <rect x="1630" y="85" width="530" height="1320" class="lane-bg-4"/>
  <rect x="1630" y="85" width="530" height="42" fill="#F3E8FF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="1895" y="112" class="lane-hdr-txt" fill="#581C87">Swimlane 4: Automated MLOps Pipeline &amp; ModelRegistry</text>

  <line x1="570" y1="85" x2="570" y2="1405" class="lane-border"/>
  <line x1="1100" y1="85" x2="1100" y2="1405" class="lane-border"/>
  <line x1="1630" y1="85" x2="1630" y2="1405" class="lane-border"/>

  <!-- Initial Node -->
  <circle cx="305" cy="165" r="14" fill="#0F172A"/>

  <!-- Action 1 -->
  <g transform="translate(305, 225)">
    <rect x="-140" y="-24" width="280" height="48" fill="#EFF6FF" stroke="#3B82F6" class="act-node"/>
    <text y="-4" class="act-text" fill="#1E3A8A">Apply Recommended Fertilizer</text>
    <text y="12" class="act-text-sm">Apply dosage on plot during target growth stage</text>
  </g>
  <line x1="305" y1="179" x2="305" y2="201" class="flow-line"/>

  <!-- Action 2 -->
  <g transform="translate(305, 315)">
    <rect x="-140" y="-24" width="280" height="48" fill="#EFF6FF" stroke="#3B82F6" class="act-node"/>
    <text y="-4" class="act-text" fill="#1E3A8A">Observe Crop Growth &amp; Yield</text>
    <text y="12" class="act-text-sm">Monitor foliage coloration, deficiency symptoms</text>
  </g>
  <line x1="305" y1="249" x2="305" y2="291" class="flow-line"/>

  <!-- Decision 1 -->
  <polygon points="305,385 345,410 305,435 265,410" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="305" y1="339" x2="305" y2="385" class="flow-line"/>

  <path d="M 345 410 L 460 410 L 460 475" fill="none" stroke="#16A34A" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="355" y="402" class="guard-text" style="fill:#16A34A;">[Optimal Growth]</text>

  <g transform="translate(460, 500)">
    <rect x="-90" y="-20" width="180" height="40" fill="#DCFCE7" stroke="#16A34A" class="act-node"/>
    <text y="5" class="act-text" fill="#15803D">is_correct = True</text>
  </g>

  <path d="M 265 410 L 150 410 L 150 475" fill="none" stroke="#EA580C" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="160" y="402" class="guard-err" style="fill:#C2410C;">[Deficiency / Outlier]</text>

  <g transform="translate(150, 500)">
    <rect x="-95" y="-20" width="190" height="40" fill="#FFF7ED" stroke="#EA580C" class="act-node"/>
    <text y="5" class="act-text" fill="#9A3412">is_correct = False, actual=..</text>
  </g>

  <!-- Merge Node -->
  <polygon points="305,570 335,590 305,610 275,590" fill="#E2E8F0" stroke="#64748B" stroke-width="1.4"/>
  <path d="M 460 520 L 460 590 L 335 590" fill="none" stroke="#1E293B" stroke-width="1.8"/>
  <path d="M 150 520 L 150 590 L 275 590" fill="none" stroke="#1E293B" stroke-width="1.8"/>

  <!-- Action 3 -->
  <g transform="translate(305, 665)">
    <rect x="-140" y="-24" width="280" height="48" fill="#EFF6FF" stroke="#3B82F6" class="act-node"/>
    <text y="-4" class="act-text" fill="#1E3A8A">Submit Feedback Payload</text>
    <text y="12" class="act-text-sm">POST /api/v1/predictions/{{id}}/feedback</text>
  </g>
  <line x1="305" y1="610" x2="305" y2="641" class="flow-line"/>

  <!-- Flow to Lane 2 -->
  <path d="M 445 665 L 835 665 L 835 705" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow2)"/>

  <!-- Action 4 -->
  <g transform="translate(835, 735)">
    <rect x="-140" y="-24" width="280" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Lookup Target PredictionRecord</text>
    <text y="12" class="act-text-sm">Verify prediction_id exists &amp; active in DB</text>
  </g>

  <!-- Action 5 -->
  <g transform="translate(835, 825)">
    <rect x="-140" y="-24" width="280" height="48" fill="#ECFDF5" stroke="#10B981" class="act-node"/>
    <text y="-4" class="act-text" fill="#065F46">Persist FarmerFeedback Entity</text>
    <text y="12" class="act-text-sm">INSERT into feedback_log (UUID, Foreign Key)</text>
  </g>
  <line x1="835" y1="759" x2="835" y2="801" class="flow-line"/>

  <!-- Decision 2 -->
  <polygon points="835,890 870,915 835,940 800,915" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="835" y1="849" x2="835" y2="890" class="flow-line"/>

  <!-- Branch 2a: Positive Feedback -->
  <path d="M 835 940 L 835 1070 L 1680 1070 L 1680 1105" fill="none" stroke="#16A34A" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="850" y="990" class="guard-text" style="fill:#16A34A;">[is_correct == True: Ground Truth Tagged]</text>

  <!-- Branch 2b: Negative Feedback -->
  <path d="M 870 915 L 1365 915 L 1365 955" fill="none" stroke="#EA580C" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="920" y="907" class="guard-err" style="fill:#C2410C;">[is_correct == False: Anomaly Flagged]</text>

  <!-- Action 6 -->
  <g transform="translate(1365, 985)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FFFBEB" stroke="#D97706" class="act-node"/>
    <text y="-4" class="act-text" fill="#92400E">Agronomic Review &amp; Soil Audit</text>
    <text y="12" class="act-text-sm">Cross-examine climate, salinity &amp; micronutrients</text>
  </g>

  <!-- Decision 3 -->
  <polygon points="1365,1045 1400,1070 1365,1095 1330,1070" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="1365" y1="1009" x2="1365" y2="1045" class="flow-line"/>

  <line x1="1330" y1="1070" x2="1240" y2="1070" class="flow-line-err"/>
  <text x="1245" y="1062" class="guard-err">[Contaminated / Spurious]</text>
  
  <circle cx="1215" cy="1070" r="14" fill="#FFFFFF" stroke="#DC2626" stroke-width="2"/>
  <line x1="1205" y1="1060" x2="1225" y2="1080" stroke="#DC2626" stroke-width="2"/>
  <line x1="1225" y1="1060" x2="1205" y2="1080" stroke="#DC2626" stroke-width="2"/>

  <path d="M 1400 1070 L 1895 1070 L 1895 1105" fill="none" stroke="#16A34A" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="1420" y="1062" class="guard-text" style="fill:#16A34A;">[Approved: Valid Edge Case Correction]</text>

  <!-- Action 7 -->
  <g transform="translate(1895, 1135)">
    <rect x="-140" y="-24" width="280" height="48" fill="#FAF5FF" stroke="#8B5CF6" class="act-node"/>
    <text y="-4" class="act-text" fill="#581C87">Append to Dataset &amp; Run KS Drift Test</text>
    <text y="12" class="act-text-sm">Compute Kolmogorov-Smirnov p-val on N,P,K</text>
  </g>

  <!-- Decision 4 -->
  <polygon points="1895,1195 1930,1215 1895,1235 1860,1215" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>
  <line x1="1895" y1="1159" x2="1895" y2="1195" class="flow-line"/>

  <!-- No Retrain: Routes straight to final node! -->
  <path d="M 1860 1215 L 1750 1215 L 1750 1255" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="1760" y="1207" class="guard-text" style="fill:#475569;">[Drift &lt; 0.05 &amp; N &lt; 100]</text>

  <g transform="translate(1750, 1280)">
    <rect x="-85" y="-18" width="170" height="36" fill="#F1F5F9" stroke="#64748B" class="act-node"/>
    <text y="4" class="act-text" fill="#475569" style="font-size:10px;">Queue for Scheduled Batch</text>
  </g>
  <path d="M 1750 1298 L 1750 1425 L 1881 1425" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#act-arrow2)"/>

  <!-- Yes -> Trigger Retraining Pipeline -->
  <path d="M 1930 1215 L 2040 1215 L 2040 1255" fill="none" stroke="#16A34A" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
  <text x="1940" y="1207" class="guard-text" style="fill:#16A34A;">[Threshold Met: Retrain]</text>

  <!-- Action 8 -->
  <g transform="translate(2040, 1285)">
    <rect x="-95" y="-24" width="190" height="48" fill="#FAF5FF" stroke="#8B5CF6" class="act-node"/>
    <text y="-4" class="act-text" fill="#581C87">Train Candidate Model</text>
    <text y="12" class="act-text-sm">XGBoost 5-Fold Stratified CV</text>
  </g>

  <!-- Action 9 -->
  <g transform="translate(1980, 1365)">
    <rect x="-130" y="-24" width="260" height="48" fill="#DCFCE7" stroke="#16A34A" class="act-node"/>
    <text y="-4" class="act-text" fill="#15803D">Hot-Swap Model in ModelRegistry</text>
    <text y="12" class="act-text-sm">Promote bundle: v1.0.0 ➔ v1.1.0 (Zero Downtime)</text>
  </g>
  <path d="M 2040 1309 L 2040 1341" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow2)"/>

  <!-- Final Node -->
  <circle cx="1895" cy="1425" r="14" fill="#FFFFFF" stroke="#0F172A" stroke-width="2"/>
  <circle cx="1895" cy="1425" r="8" fill="#0F172A"/>
  <path d="M 1980 1389 L 1980 1425 L 1909 1425" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#act-arrow2)"/>
</svg>
"""
    return svg

def main():
    print("Re-rendering Sequence and Activity Diagrams with perfected routing...")
    svg1 = get_seq_diag_1()
    render_svg_to_png(svg1, "uml_sequence_recommendation_fieldwise.svg", "uml_sequence_recommendation_fieldwise.png", 2200, 1400)
    
    svg2 = get_seq_diag_2()
    render_svg_to_png(svg2, "uml_sequence_circuit_breaker_fieldwise.svg", "uml_sequence_circuit_breaker_fieldwise.png", 2200, 1500)
    
    svg3 = get_act_diag_1()
    render_svg_to_png(svg3, "uml_activity_workflow_fieldwise.svg", "uml_activity_workflow_fieldwise.png", 2400, 1550)
    
    svg4 = get_act_diag_2()
    render_svg_to_png(svg4, "uml_activity_feedback_lifecycle_fieldwise.svg", "uml_activity_feedback_lifecycle_fieldwise.png", 2200, 1450)

    print("All 4 diagrams polished and rendered successfully!")

if __name__ == "__main__":
    main()
