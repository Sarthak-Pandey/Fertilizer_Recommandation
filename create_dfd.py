import os

svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1280" viewBox="0 0 1920 1280">
  <defs>
    <!-- Drop Shadow for crisp academic depth -->
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.07"/>
    </filter>

    <!-- Arrowhead Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1B4332" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1D4ED8" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#EA580C" />
    </marker>
    
    <!-- Header Gradient for Process Boxes -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1B5E20" />
      <stop offset="100%" stop-color="#2E7D32" />
    </linearGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="1920" height="1280" fill="#FFFFFF"/>
  <rect width="1896" height="1256" x="12" y="12" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- Title Banner -->
  <rect x="40" y="30" width="1840" height="75" rx="8" fill="#F4FBF7" stroke="#A7F3D0" stroke-width="1.5"/>
  <text x="960" y="65" font-family="'Segoe UI', Arial, sans-serif" font-size="25" font-weight="bold" fill="#1B5E20" text-anchor="middle">
    Level 1 Data Flow Diagram – Fieldwise Fertilizer Recommendation System
  </text>
  <text x="960" y="91" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="600" fill="#047857" text-anchor="middle">
    Standard Gane &amp; Sarson DFD Notation | Complete System Data Pipeline &amp; Audit Workflows
  </text>


  <!-- ==================== DATA FLOW ARROWS & LABELS ==================== -->

  <!-- 1. USER -> 1.0 User Authentication -->
  <path d="M 190 460 L 190 180 L 480 180" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="235" y="167" width="200" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="335" y="184" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">1. Login / Registration Details</text>

  <!-- 2. 1.0 User Authentication -> USER -->
  <path d="M 480 205 L 230 205 L 230 460" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="235" y="218" width="200" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="335" y="235" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Authentication Status / Session</text>

  <!-- 3. 1.0 User Authentication -> D1 Supabase -->
  <path d="M 740 175 L 1200 175" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="850" y="161" width="240" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="970" y="178" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Store / Validate User Credentials</text>

  <!-- 4. D1 Supabase -> 1.0 User Authentication -->
  <path d="M 1200 205 L 740 205" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="850" y="218" width="240" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="970" y="235" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Validated User Profile &amp; Auth Tokens</text>

  <!-- 5. D1 -> External Supabase Auth Service -->
  <path d="M 1520 190 L 1580 190" fill="none" stroke="#1D4ED8" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-blue)" />
  <rect x="1512" y="177" width="80" height="26" rx="4" fill="#FFFFFF" stroke="#93C5FD" stroke-width="1"/>
  <text x="1552" y="194" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="600" fill="#1E40AF" text-anchor="middle">OAuth Sync</text>

  <!-- 6. USER -> 2.0 Submit Soil & Crop Data -->
  <path d="M 300 490 L 390 490 L 390 350 L 480 350" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="305" y="405" width="170" height="40" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="390" y="421" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Soil &amp; Crop Parameters</text>
  <text x="390" y="437" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#475569" text-anchor="middle">(N, P, K, Soil Type, Crop)</text>

  <!-- 7. 2.0 -> 3.0 Validate Request -->
  <path d="M 610 390 L 610 470" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="500" y="415" width="220" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="610" y="432" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Raw Soil &amp; Crop Parameter Input</text>

  <!-- 8. 3.0 -> 4.0 Preprocess Input Data -->
  <path d="M 610 550 L 610 630" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="490" y="575" width="240" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="610" y="592" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Validated Recommendation Request</text>

  <!-- 9. D3 ML Model Artifacts -> 4.0 Preprocess Input Data -->
  <path d="M 1200 700 L 980 700 L 980 670 L 740 670" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="850" y="657" width="250" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="975" y="674" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">StandardScaler &amp; OneHotEncoder Fits</text>

  <!-- 10. 4.0 -> 5.0 ML Fertilizer Prediction -->
  <path d="M 610 710 L 610 790" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="500" y="735" width="220" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="610" y="752" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Preprocessed Soil &amp; Crop Vector</text>

  <!-- 11. D3 ML Model Artifacts -> 5.0 ML Fertilizer Prediction -->
  <path d="M 1200 725 L 980 725 L 980 810 L 740 810" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="850" y="797" width="250" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="975" y="814" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">XGBoost &amp; Random Forest Models</text>

  <!-- 12. 5.0 -> 6.0 Generate Recommendation -->
  <path d="M 610 870 L 610 950" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="505" y="895" width="210" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="610" y="912" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Prediction + Confidence Score</text>

  <!-- 13. 6.0 -> USER (Recommendation Output) -->
  <path d="M 480 990 L 180 990 L 180 570" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="70" y="780" width="220" height="42" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="180" y="797" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Recommended Fertilizer,</text>
  <text x="180" y="813" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#475569" text-anchor="middle">Deficiency Analysis &amp; Instructions</text>

  <!-- 14. 5.0 -> 7.0 Store Prediction Audit Log -->
  <path d="M 740 830 L 870 830" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="748" y="817" width="114" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="805" y="834" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="600" fill="#1E293B" text-anchor="middle">Prediction &amp; Latency</text>

  <!-- 15. 7.0 -> D2 Prediction Audit History -->
  <path d="M 1130 830 L 1165 830 L 1165 930 L 1200 930" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="1110" y="867" width="110" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1165" y="884" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="600" fill="#1E293B" text-anchor="middle">Audit Log Record</text>

  <!-- 16. USER -> 8.0 View History -->
  <path d="M 270 570 L 270 1130 L 480 1130" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="270" y="1117" width="190" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="365" y="1134" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Historical Recommendation Request</text>

  <!-- 17. 8.0 -> D2 Prediction Audit History (Query) -->
  <path d="M 740 1130 L 1120 1130 L 1120 960 L 1200 960" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="840" y="1117" width="180" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="930" y="1134" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Fetch User Prediction Records</text>

  <!-- 18. D2 -> 8.0 View History (Response) -->
  <path d="M 1360 990 L 1360 1170 L 740 1170" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="930" y="1157" width="240" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1050" y="1174" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Historical Recommendation Records</text>

  <!-- 19. 8.0 View History -> USER -->
  <path d="M 480 1160 L 130 1160 L 130 570" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="200" y="1147" width="200" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="300" y="1164" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">Historical Recommendation Output</text>

  <!-- 20. D2 -> 9.0 System Audit / Health Monitoring -->
  <path d="M 1320 990 L 1320 1110" fill="none" stroke="#1B4332" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="1220" y="1037" width="200" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1320" y="1054" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#1E293B" text-anchor="middle">System Logs &amp; Inference Analytics</text>

  <!-- 21. 9.0 -> Prometheus Metrics -->
  <path d="M 1480 1150 L 1580 1150" fill="none" stroke="#EA580C" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-orange)" />
  <rect x="1485" y="1115" width="90" height="38" rx="4" fill="#FFFFFF" stroke="#FDBA74" stroke-width="1"/>
  <text x="1530" y="1131" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="600" fill="#9A3412" text-anchor="middle">ML Health &amp;</text>
  <text x="1530" y="1146" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#C2410C" text-anchor="middle">Metrics Stream</text>


  <!-- ==================== EXTERNAL ENTITIES ==================== -->
  
  <!-- USER / FARMER -->
  <g filter="url(#shadow)">
    <rect x="80" y="460" width="220" height="110" rx="8" fill="#E8F5E9" stroke="#1B5E20" stroke-width="2.5"/>
    <rect x="80" y="460" width="220" height="30" rx="8" fill="#2E7D32"/>
    <rect x="80" y="482" width="220" height="8" fill="#2E7D32"/>
    <text x="190" y="480" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EXTERNAL ENTITY</text>
    <text x="190" y="518" font-family="'Segoe UI', Arial, sans-serif" font-size="18" font-weight="bold" fill="#1B5E20" text-anchor="middle">USER / FARMER</text>
    <text x="190" y="542" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#388E3C" text-anchor="middle">(Primary System Actor)</text>
  </g>

  <!-- SUPABASE AUTHENTICATION SERVICE -->
  <g filter="url(#shadow)">
    <rect x="1580" y="145" width="260" height="90" rx="8" fill="#EFF6FF" stroke="#1D4ED8" stroke-width="2"/>
    <rect x="1580" y="145" width="260" height="26" rx="8" fill="#1D4ED8"/>
    <rect x="1580" y="163" width="260" height="8" fill="#1D4ED8"/>
    <text x="1710" y="163" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EXTERNAL SYSTEM</text>
    <text x="1710" y="193" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#1E40AF" text-anchor="middle">SUPABASE AUTH SERVICE</text>
    <text x="1710" y="215" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#2563EB" text-anchor="middle">Identity &amp; Auth Provider</text>
  </g>

  <!-- PROMETHEUS METRICS -->
  <g filter="url(#shadow)">
    <rect x="1580" y="1105" width="260" height="90" rx="8" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
    <rect x="1580" y="1105" width="260" height="26" rx="8" fill="#EA580C"/>
    <rect x="1580" y="1123" width="260" height="8" fill="#EA580C"/>
    <text x="1710" y="1123" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MONITORING INFRASTRUCTURE</text>
    <text x="1710" y="1153" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#9A3412" text-anchor="middle">PROMETHEUS METRICS</text>
    <text x="1710" y="1175" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#C2410C" text-anchor="middle">Telemetry &amp; Health Dashboard</text>
  </g>


  <!-- ==================== DATA STORES (Gane & Sarson Style) ==================== -->
  
  <!-- D1: Supabase User & Profile Data -->
  <g filter="url(#shadow)">
    <rect x="1200" y="145" width="320" height="90" rx="4" fill="#F4FBF7" stroke="#1B5E20" stroke-width="2"/>
    <rect x="1200" y="145" width="65" height="90" fill="#1B5E20"/>
    <text x="1232" y="198" font-family="'Segoe UI', Arial, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">D1</text>
    <text x="1395" y="185" font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="bold" fill="#1B5E20" text-anchor="middle">User &amp; Profile Data</text>
    <text x="1395" y="210" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#2E7D32" text-anchor="middle">Supabase Cloud User Store</text>
  </g>

  <!-- D3: ML Model Artifacts -->
  <g filter="url(#shadow)">
    <rect x="1200" y="660" width="320" height="90" rx="4" fill="#F4FBF7" stroke="#1B5E20" stroke-width="2"/>
    <rect x="1200" y="660" width="65" height="90" fill="#1B5E20"/>
    <text x="1232" y="713" font-family="'Segoe UI', Arial, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">D3</text>
    <text x="1395" y="697" font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="bold" fill="#1B5E20" text-anchor="middle">ML Model Artifacts</text>
    <text x="1395" y="722" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#2E7D32" text-anchor="middle">XGBoost, RF &amp; Scaler Models</text>
  </g>

  <!-- D2: Prediction / Audit History -->
  <g filter="url(#shadow)">
    <rect x="1200" y="890" width="320" height="100" rx="4" fill="#F4FBF7" stroke="#1B5E20" stroke-width="2"/>
    <rect x="1200" y="890" width="65" height="100" fill="#1B5E20"/>
    <text x="1232" y="948" font-family="'Segoe UI', Arial, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">D2</text>
    <text x="1395" y="930" font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="bold" fill="#1B5E20" text-anchor="middle">Prediction / Audit History</text>
    <text x="1395" y="955" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#2E7D32" text-anchor="middle">SQLite Database via Peewee ORM</text>
  </g>


  <!-- ==================== PROCESSES (Gane & Sarson Rounded Boxes) ==================== -->

  <!-- 1.0 USER AUTHENTICATION -->
  <g filter="url(#shadow)">
    <rect x="480" y="150" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 162 A 12 12 0 0 1 492 150 L 728 150 A 12 12 0 0 1 740 162 L 740 182 L 480 182 Z" fill="url(#header-grad)"/>
    <text x="610" y="172" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">1.0</text>
    <text x="610" y="208" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">USER AUTHENTICATION</text>
  </g>

  <!-- 2.0 SUBMIT SOIL & CROP DATA -->
  <g filter="url(#shadow)">
    <rect x="480" y="310" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 322 A 12 12 0 0 1 492 310 L 728 310 A 12 12 0 0 1 740 322 L 740 342 L 480 342 Z" fill="url(#header-grad)"/>
    <text x="610" y="332" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2.0</text>
    <text x="610" y="368" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">SUBMIT SOIL &amp; CROP DATA</text>
  </g>

  <!-- 3.0 VALIDATE REQUEST -->
  <g filter="url(#shadow)">
    <rect x="480" y="470" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 482 A 12 12 0 0 1 492 470 L 728 470 A 12 12 0 0 1 740 482 L 740 502 L 480 502 Z" fill="url(#header-grad)"/>
    <text x="610" y="492" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">3.0</text>
    <text x="610" y="528" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">VALIDATE REQUEST</text>
  </g>

  <!-- 4.0 PREPROCESS INPUT DATA -->
  <g filter="url(#shadow)">
    <rect x="480" y="630" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 642 A 12 12 0 0 1 492 630 L 728 630 A 12 12 0 0 1 740 642 L 740 662 L 480 662 Z" fill="url(#header-grad)"/>
    <text x="610" y="652" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">4.0</text>
    <text x="610" y="688" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">PREPROCESS INPUT DATA</text>
  </g>

  <!-- 5.0 ML FERTILIZER PREDICTION -->
  <g filter="url(#shadow)">
    <rect x="480" y="790" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 802 A 12 12 0 0 1 492 790 L 728 790 A 12 12 0 0 1 740 802 L 740 822 L 480 822 Z" fill="url(#header-grad)"/>
    <text x="610" y="812" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">5.0</text>
    <text x="610" y="848" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">ML FERTILIZER PREDICTION</text>
  </g>

  <!-- 6.0 GENERATE RECOMMENDATION -->
  <g filter="url(#shadow)">
    <rect x="480" y="950" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 962 A 12 12 0 0 1 492 950 L 728 950 A 12 12 0 0 1 740 962 L 740 982 L 480 982 Z" fill="url(#header-grad)"/>
    <text x="610" y="972" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">6.0</text>
    <text x="610" y="1008" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">GENERATE RECOMMENDATION</text>
  </g>

  <!-- 7.0 STORE PREDICTION AUDIT LOG -->
  <g filter="url(#shadow)">
    <rect x="870" y="790" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 870 802 A 12 12 0 0 1 882 790 L 1118 790 A 12 12 0 0 1 1130 802 L 1130 822 L 870 822 Z" fill="url(#header-grad)"/>
    <text x="1000" y="812" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">7.0</text>
    <text x="1000" y="848" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="bold" fill="#111827" text-anchor="middle">STORE PREDICTION AUDIT LOG</text>
  </g>

  <!-- 8.0 VIEW HISTORY -->
  <g filter="url(#shadow)">
    <rect x="480" y="1110" width="260" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 480 1122 A 12 12 0 0 1 492 1110 L 728 1110 A 12 12 0 0 1 740 1122 L 740 1142 L 480 1142 Z" fill="url(#header-grad)"/>
    <text x="610" y="1132" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">8.0</text>
    <text x="610" y="1168" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#111827" text-anchor="middle">VIEW HISTORY</text>
  </g>

  <!-- 9.0 SYSTEM AUDIT / HEALTH MONITORING -->
  <g filter="url(#shadow)">
    <rect x="1200" y="1110" width="280" height="80" rx="12" fill="#FFFFFF" stroke="#1B5E20" stroke-width="2"/>
    <path d="M 1200 1122 A 12 12 0 0 1 1212 1110 L 1468 1110 A 12 12 0 0 1 1480 1122 L 1480 1142 L 1200 1142 Z" fill="url(#header-grad)"/>
    <text x="1340" y="1132" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">9.0</text>
    <text x="1340" y="1168" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="bold" fill="#111827" text-anchor="middle">SYSTEM AUDIT / HEALTH MONITORING</text>
  </g>

  <!-- Footer Info -->
  <text x="40" y="1248" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#64748B">
    Fieldwise AI System Architecture • Level 1 Data Flow Diagram (DFD) • Academic Project Report Documentation
  </text>
</svg>
"""

with open("dfd_level1_fieldwise.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Pristine SVG written to dfd_level1_fieldwise.svg")
