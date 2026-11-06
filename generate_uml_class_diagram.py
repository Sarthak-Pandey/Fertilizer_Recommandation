import os
import subprocess

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

svg_uml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="2500" height="1620" viewBox="0 0 2500 1620">
  <defs>
    <!-- Drop Shadow Filter -->
    <filter id="shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>

    <!-- UML Generalization Hollow Triangle Marker -->
    <marker id="generalization" viewBox="0 0 16 16" refX="16" refY="8" markerWidth="14" markerHeight="14" orient="auto">
      <polygon points="0,0 16,8 0,16" fill="#FFFFFF" stroke="#1E293B" stroke-width="1.8"/>
    </marker>

    <!-- UML Composition Filled Black Diamond Marker -->
    <marker id="composition" viewBox="0 0 20 12" refX="0" refY="6" markerWidth="16" markerHeight="10" orient="auto">
      <polygon points="0,6 10,0 20,6 10,12" fill="#0F172A" stroke="#0F172A" stroke-width="1.5"/>
    </marker>

    <!-- UML Aggregation Hollow White Diamond Marker -->
    <marker id="aggregation" viewBox="0 0 20 12" refX="0" refY="6" markerWidth="16" markerHeight="10" orient="auto">
      <polygon points="0,6 10,0 20,6 10,12" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.8"/>
    </marker>

    <!-- UML Association Open Arrowhead Marker -->
    <marker id="assoc-arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 0 2 L 10 6 L 0 10" fill="none" stroke="#1E293B" stroke-width="1.8" stroke-linecap="round"/>
    </marker>

    <!-- UML Dependency Open Arrowhead Marker (Dashed) -->
    <marker id="dep-arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 0 2 L 10 6 L 0 10" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round"/>
    </marker>
  </defs>

  <style>
    .title-main { font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px; font-weight: bold; fill: #0f172a; }
    .title-sub  { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: 500; fill: #475569; }
    
    .pkg-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: bold; }
    
    .cls-box { rx: 6px; stroke-width: 1.5px; }
    .cls-stereo { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-style: italic; text-anchor: middle; }
    .cls-name { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: bold; text-anchor: middle; }
    .cls-divider { stroke-width: 1px; }
    
    .cls-attr { font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; fill: #1e293b; }
    .cls-meth { font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; fill: #0f172a; }
    
    .cls-attr-sm { font-family: 'Consolas', 'Courier New', monospace; font-size: 10px; fill: #1e293b; }
    .cls-meth-sm { font-family: 'Consolas', 'Courier New', monospace; font-size: 10px; fill: #0f172a; }
    
    .conn-line { fill: none; stroke: #334155; stroke-width: 1.7px; }
    .dep-line  { fill: none; stroke: #2563eb; stroke-width: 1.6px; stroke-dasharray: 6,4; }
    .mult-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; font-weight: bold; fill: #0f172a; }
    .rel-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-style: italic; fill: #334155; }
    
    .legend-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11.5px; fill: #334155; }
  </style>

  <!-- Canvas Background -->
  <rect width="2500" height="1620" fill="#FFFFFF"/>
  <rect x="15" y="15" width="2470" height="1590" fill="none" stroke="#E2E8F0" stroke-width="2" rx="10"/>

  <!-- ==================== HEADER BANNER ==================== -->
  <g transform="translate(1250, 38)">
    <text class="title-main" text-anchor="middle">Fieldwise: Intelligent Fertilizer Recommendation System</text>
    <text class="title-sub" y="22" text-anchor="middle">Standard UML 2.5 Detailed Class Diagram — Object-Oriented Analysis &amp; Architectural Design Model</text>
  </g>

  <!-- ==================== PACKAGE 1: CONTRACT & SCHEMAS ==================== -->
  <rect x="40" y="85" width="530" height="1440" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5" rx="8" stroke-dasharray="8,4"/>
  <rect x="40" y="85" width="320" height="28" fill="#E2E8F0" rx="6"/>
  <text x="55" y="104" class="pkg-title" fill="#1E293B">Package: schemas &amp; dtos (Contract Layer)</text>

  <!-- CLASS: BaseModel (Pydantic / Framework Base) -->
  <g filter="url(#shadow)" transform="translate(70, 130)">
    <rect width="470" height="90" fill="#F1F5F9" stroke="#64748B" class="cls-box"/>
    <text x="235" y="22" class="cls-stereo" fill="#475569">&lt;&lt;Abstract Base Class&gt;&gt;</text>
    <text x="235" y="41" class="cls-name" fill="#0F172A">BaseModel / BaseSchema</text>
    <line x1="0" y1="49" x2="470" y2="49" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="66" class="cls-attr">+ Config: ConfigDict</text>
    <line x1="0" y1="72" x2="470" y2="72" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="84" class="cls-meth">+ model_dump(): dict</text>
  </g>

  <!-- CLASS: RecommendRequest (DTO) -->
  <g filter="url(#shadow)" transform="translate(70, 265)">
    <rect width="470" height="245" fill="#FEF9C3" stroke="#CA8A04" class="cls-box"/>
    <text x="235" y="20" class="cls-stereo" fill="#854D0E">&lt;&lt;DTO / Request Boundary&gt;&gt;</text>
    <text x="235" y="38" class="cls-name" fill="#713F12">RecommendRequest</text>
    <line x1="0" y1="46" x2="470" y2="46" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ Soil_pH: float [0.0 .. 14.0]</text>
    <text x="14" y="80" class="cls-attr">+ Nitrogen_Level: float [&gt;= 0.0]</text>
    <text x="14" y="96" class="cls-attr">+ Phosphorus_Level: float [&gt;= 0.0]</text>
    <text x="14" y="112" class="cls-attr">+ Potassium_Level: float [&gt;= 0.0]</text>
    <text x="14" y="128" class="cls-attr">+ Crop_Growth_Stage: CropGrowthStage</text>
    <text x="14" y="144" class="cls-attr">+ Soil_Type: Optional[str] = None</text>
    <text x="14" y="160" class="cls-attr">+ Soil_Moisture: Optional[float] = None</text>
    <text x="14" y="176" class="cls-attr">+ Temperature: Optional[float] = None</text>
    <text x="14" y="192" class="cls-attr">+ Crop_Type: Optional[str] = None</text>
    <line x1="0" y1="198" x2="470" y2="198" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="216" class="cls-meth">+ validate_finite(v: float): float</text>
    <text x="14" y="232" class="cls-meth">+ to_model_features(): dict</text>
  </g>

  <!-- CLASS: CropGrowthStage (Enum) -->
  <g filter="url(#shadow)" transform="translate(120, 550)">
    <rect width="370" height="125" fill="#FEF3C7" stroke="#D97706" class="cls-box"/>
    <text x="185" y="20" class="cls-stereo" fill="#92400E">&lt;&lt;Enumeration&gt;&gt;</text>
    <text x="185" y="38" class="cls-name" fill="#78350F">CropGrowthStage</text>
    <line x1="0" y1="46" x2="370" y2="46" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ SOWING: str = "Sowing"</text>
    <text x="14" y="82" class="cls-attr">+ VEGETATIVE: str = "Vegetative"</text>
    <text x="14" y="100" class="cls-attr">+ FLOWERING: str = "Flowering"</text>
    <text x="14" y="118" class="cls-attr">+ HARVEST: str = "Harvest"</text>
  </g>

  <!-- CLASS: RecommendResponse (DTO) -->
  <g filter="url(#shadow)" transform="translate(70, 715)">
    <rect width="470" height="235" fill="#FEF9C3" stroke="#CA8A04" class="cls-box"/>
    <text x="235" y="20" class="cls-stereo" fill="#854D0E">&lt;&lt;DTO / Response Boundary&gt;&gt;</text>
    <text x="235" y="38" class="cls-name" fill="#713F12">RecommendResponse</text>
    <line x1="0" y1="46" x2="470" y2="46" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ success: bool = True</text>
    <text x="14" y="80" class="cls-attr">+ fertilizer: str</text>
    <text x="14" y="96" class="cls-attr">+ confidence: Optional[float]</text>
    <text x="14" y="112" class="cls-attr">+ model_version: str</text>
    <text x="14" y="128" class="cls-attr">+ preprocessing_version: str</text>
    <text x="14" y="144" class="cls-attr">+ feature_schema_version: str</text>
    <text x="14" y="160" class="cls-attr">+ prediction_id: Optional[str]</text>
    <text x="14" y="176" class="cls-attr">+ probabilities: Optional[Dict[str, float]]</text>
    <text x="14" y="192" class="cls-attr">+ latency_ms: Optional[float]</text>
    <line x1="0" y1="198" x2="470" y2="198" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="218" class="cls-meth">+ get_confidence_percentage(): float</text>
  </g>

  <!-- CLASS: PredictionDetail (DTO) -->
  <g filter="url(#shadow)" transform="translate(70, 985)">
    <rect width="470" height="235" fill="#F8FAFC" stroke="#64748B" class="cls-box"/>
    <text x="235" y="20" class="cls-stereo" fill="#475569">&lt;&lt;DTO / Detail View&gt;&gt;</text>
    <text x="235" y="38" class="cls-name" fill="#0F172A">PredictionDetail</text>
    <line x1="0" y1="46" x2="470" y2="46" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ prediction_id: str</text>
    <text x="14" y="80" class="cls-attr">+ request_id: Optional[str]</text>
    <text x="14" y="96" class="cls-attr">+ input_features: Dict[str, Any]</text>
    <text x="14" y="112" class="cls-attr">+ predicted_fertilizer: str</text>
    <text x="14" y="128" class="cls-attr">+ confidence: Optional[float]</text>
    <text x="14" y="144" class="cls-attr">+ model_version: str</text>
    <text x="14" y="160" class="cls-attr">+ latency_ms: Optional[float]</text>
    <text x="14" y="176" class="cls-attr">+ status: str = "success"</text>
    <text x="14" y="192" class="cls-attr">+ created_at: datetime</text>
    <line x1="0" y1="198" x2="470" y2="198" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="216" class="cls-meth">+ from_orm_record(log: PredictionLog)</text>
    <text x="14" y="228" class="cls-meth">+ to_summary_dict(): dict</text>
  </g>

  <!-- CLASS: FeedbackCreateRequest (DTO) -->
  <g filter="url(#shadow)" transform="translate(70, 1255)">
    <rect width="470" height="150" fill="#F8FAFC" stroke="#64748B" class="cls-box"/>
    <text x="235" y="20" class="cls-stereo" fill="#475569">&lt;&lt;DTO / Feedback Input&gt;&gt;</text>
    <text x="235" y="38" class="cls-name" fill="#0F172A">FeedbackCreateRequest</text>
    <line x1="0" y1="46" x2="470" y2="46" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ prediction_id: str</text>
    <text x="14" y="80" class="cls-attr">+ is_correct: bool</text>
    <text x="14" y="96" class="cls-attr">+ actual_fertilizer: Optional[str]</text>
    <text x="14" y="112" class="cls-attr">+ notes: Optional[str]</text>
    <line x1="0" y1="118" x2="470" y2="118" stroke="#CBD5E1" class="cls-divider"/>
    <text x="14" y="136" class="cls-meth">+ validate_payload(): bool</text>
  </g>


  <!-- ==================== PACKAGE 2: GATEWAY CONTROLLERS & RESILIENCE ==================== -->
  <rect x="635" y="85" width="570" height="1440" fill="#F5F3FF" stroke="#8B5CF6" stroke-width="1.5" rx="8" stroke-dasharray="8,4"/>
  <rect x="635" y="85" width="360" height="28" fill="#DDD6FE" rx="6"/>
  <text x="650" y="104" class="pkg-title" fill="#4C1D95">Package: routers &amp; services (Gateway Layer)</text>

  <!-- CLASS: RecommendationController (Boundary) -->
  <g filter="url(#shadow)" transform="translate(665, 130)">
    <rect width="510" height="240" fill="#FAF5FF" stroke="#A855F7" class="cls-box"/>
    <text x="255" y="20" class="cls-stereo" fill="#6B21A8">&lt;&lt;Boundary / Controller&gt;&gt;</text>
    <text x="255" y="38" class="cls-name" fill="#581C87">RecommendationController</text>
    <line x1="0" y1="46" x2="510" y2="46" stroke="#E9D5FF" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">- ml_client: MLClient</text>
    <text x="14" y="80" class="cls-attr">- router: APIRouter</text>
    <text x="14" y="96" class="cls-attr">- prefix: str = "/api/v1/fertilizer"</text>
    <line x1="0" y1="102" x2="510" y2="102" stroke="#E9D5FF" class="cls-divider"/>
    <text x="14" y="122" class="cls-meth">+ recommend(req: RecommendRequest, user): RecommendResponse</text>
    <text x="14" y="140" class="cls-meth">+ batch_recommend(reqs: List[RecommendRequest]): List</text>
    <text x="14" y="158" class="cls-meth">- extract_ml_payload(req: RecommendRequest): dict</text>
    <text x="14" y="176" class="cls-meth">- persist_audit_record(req_data, result, lat_ms): str</text>
    <text x="14" y="194" class="cls-meth">- record_telemetry_metrics(status, fertilizer, lat_ms)</text>
    <text x="14" y="212" class="cls-meth">- handle_fallback(req, error): RecommendResponse</text>
  </g>

  <!-- CLASS: MLClient (Service / HTTP Adapter) -->
  <g filter="url(#shadow)" transform="translate(665, 410)">
    <rect width="510" height="260" fill="#EFF6FF" stroke="#3B82F6" class="cls-box"/>
    <text x="255" y="20" class="cls-stereo" fill="#1D4ED8">&lt;&lt;Service / HTTP Adapter&gt;&gt;</text>
    <text x="255" y="38" class="cls-name" fill="#1E3A8A">MLClient</text>
    <line x1="0" y1="46" x2="510" y2="46" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ base_url: str</text>
    <text x="14" y="80" class="cls-attr">+ timeout: float = 10.0</text>
    <text x="14" y="96" class="cls-attr">+ max_retries: int = 3</text>
    <text x="14" y="112" class="cls-attr">+ retry_base_delay: float = 0.5</text>
    <text x="14" y="128" class="cls-attr">+ retry_max_delay: float = 2.0</text>
    <text x="14" y="144" class="cls-attr">+ circuit_breaker: CircuitBreaker</text>
    <text x="14" y="160" class="cls-attr">- _client: Optional[httpx.AsyncClient]</text>
    <line x1="0" y1="166" x2="510" y2="166" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="184" class="cls-meth">+ open(): Promise&lt;void&gt;</text>
    <text x="14" y="202" class="cls-meth">+ close(): Promise&lt;void&gt;</text>
    <text x="14" y="220" class="cls-meth">+ predict(input_data: dict[str, Any]): Promise&lt;dict&gt;</text>
    <text x="14" y="238" class="cls-meth">- _get_client(): httpx.AsyncClient</text>
    <text x="14" y="254" class="cls-meth">- _execute_with_retry(payload: dict): Promise&lt;dict&gt;</text>
  </g>

  <!-- CLASS: CircuitBreaker (Finite State Machine) -->
  <g filter="url(#shadow)" transform="translate(665, 715)">
    <rect width="510" height="240" fill="#EFF6FF" stroke="#3B82F6" class="cls-box"/>
    <text x="255" y="20" class="cls-stereo" fill="#1D4ED8">&lt;&lt;Service / Finite State Machine&gt;&gt;</text>
    <text x="255" y="38" class="cls-name" fill="#1E3A8A">CircuitBreaker</text>
    <line x1="0" y1="46" x2="510" y2="46" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ failure_threshold: int = 5</text>
    <text x="14" y="80" class="cls-attr">+ cooldown_seconds: float = 30.0</text>
    <text x="14" y="96" class="cls-attr">+ state: CircuitState = CircuitState.CLOSED</text>
    <text x="14" y="112" class="cls-attr">+ failure_count: int = 0</text>
    <text x="14" y="128" class="cls-attr">+ last_failure_time: Optional[float]</text>
    <text x="14" y="144" class="cls-attr">+ last_state_change: float</text>
    <text x="14" y="160" class="cls-attr">- _lock: asyncio.Lock</text>
    <line x1="0" y1="166" x2="510" y2="166" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="184" class="cls-meth">+ can_execute(): Promise&lt;bool&gt;</text>
    <text x="14" y="202" class="cls-meth">+ record_success(): Promise&lt;void&gt;</text>
    <text x="14" y="220" class="cls-meth">+ record_failure(): Promise&lt;void&gt;</text>
  </g>

  <!-- CLASS: CircuitState (Enum) -->
  <g filter="url(#shadow)" transform="translate(740, 1000)">
    <rect width="360" height="110" fill="#FEF3C7" stroke="#D97706" class="cls-box"/>
    <text x="180" y="20" class="cls-stereo" fill="#92400E">&lt;&lt;Enumeration&gt;&gt;</text>
    <text x="180" y="38" class="cls-name" fill="#78350F">CircuitState</text>
    <line x1="0" y1="46" x2="360" y2="46" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ CLOSED: str = "CLOSED"</text>
    <text x="14" y="82" class="cls-attr">+ OPEN: str = "OPEN"</text>
    <text x="14" y="100" class="cls-attr">+ HALF_OPEN: str = "HALF_OPEN"</text>
  </g>

  <!-- CLASS: PredictionHistoryController (Boundary) -->
  <g filter="url(#shadow)" transform="translate(665, 1155)">
    <rect width="510" height="175" fill="#FAF5FF" stroke="#A855F7" class="cls-box"/>
    <text x="255" y="20" class="cls-stereo" fill="#6B21A8">&lt;&lt;Boundary / Controller&gt;&gt;</text>
    <text x="255" y="38" class="cls-name" fill="#581C87">PredictionHistoryController</text>
    <line x1="0" y1="46" x2="510" y2="46" stroke="#E9D5FF" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">- router: APIRouter</text>
    <line x1="0" y1="70" x2="510" y2="70" stroke="#E9D5FF" class="cls-divider"/>
    <text x="14" y="88" class="cls-meth">+ list_history(page, limit, status, user_id): PredictionList</text>
    <text x="14" y="106" class="cls-meth">+ get_prediction_by_id(prediction_id, user_id): PredictionDetail</text>
    <text x="14" y="124" class="cls-meth">+ soft_delete_prediction(prediction_id, user_id): bool</text>
    <text x="14" y="142" class="cls-meth">+ export_predictions(format: str, user_id: str): Response</text>
    <text x="14" y="160" class="cls-meth">+ submit_feedback(feedback: FeedbackCreateRequest): FeedbackLog</text>
  </g>

  <!-- CLASS: AuthService (Security Control) -->
  <g filter="url(#shadow)" transform="translate(665, 1365)">
    <rect width="510" height="120" fill="#EFF6FF" stroke="#3B82F6" class="cls-box"/>
    <text x="255" y="20" class="cls-stereo" fill="#1D4ED8">&lt;&lt;Service / Security&gt;&gt;</text>
    <text x="255" y="38" class="cls-name" fill="#1E3A8A">AuthService</text>
    <line x1="0" y1="46" x2="510" y2="46" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="62" class="cls-attr">- _client: Optional[supabase.Client]</text>
    <line x1="0" y1="68" x2="510" y2="68" stroke="#BFDBFE" class="cls-divider"/>
    <text x="14" y="86" class="cls-meth">+ register_user(email: str, pass: str, role: str): dict</text>
    <text x="14" y="104" class="cls-meth">+ login_user(email: str, pass: str): dict</text>
  </g>


  <!-- ==================== PACKAGE 3: DOMAIN ENTITIES & PERSISTENCE ==================== -->
  <rect x="1265" y="85" width="540" height="1440" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5" rx="8" stroke-dasharray="8,4"/>
  <rect x="1265" y="85" width="360" height="28" fill="#D1FAE5" rx="6"/>
  <text x="1280" y="104" class="pkg-title" fill="#065F46">Package: domain &amp; database (Persistence Layer)</text>

  <!-- CLASS: UserAccount (Domain Entity) -->
  <g filter="url(#shadow)" transform="translate(1295, 130)">
    <rect width="480" height="175" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="240" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Domain Entity / User&gt;&gt;</text>
    <text x="240" y="38" class="cls-name" fill="#14532D">UserAccount</text>
    <line x1="0" y1="46" x2="480" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ user_id: str [PK, UUID]</text>
    <text x="14" y="80" class="cls-attr">+ email: str [Unique]</text>
    <text x="14" y="96" class="cls-attr">+ full_name: str</text>
    <text x="14" y="112" class="cls-attr">+ role: str = "farmer"  // agronomist | admin</text>
    <text x="14" y="128" class="cls-attr">+ organization: Optional[str]</text>
    <text x="14" y="144" class="cls-attr">+ created_at: datetime</text>
    <line x1="0" y1="150" x2="480" y2="150" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="168" class="cls-meth">+ is_agronomist(): bool</text>
  </g>

  <!-- CLASS: PredictionRecord (Aggregate Root Entity) -->
  <g filter="url(#shadow)" transform="translate(1295, 345)">
    <rect width="480" height="360" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="240" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Domain Entity / Aggregate Root&gt;&gt;</text>
    <text x="240" y="38" class="cls-name" fill="#14532D">PredictionRecord (PredictionLog)</text>
    <line x1="0" y1="46" x2="480" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ prediction_id: str [PK, UUID]</text>
    <text x="14" y="80" class="cls-attr">+ request_id: Optional[str] [Index]</text>
    <text x="14" y="96" class="cls-attr">+ user_id: Optional[str] [FK, Index]</text>
    <text x="14" y="112" class="cls-attr">+ input_features: str [Serialized JSON]</text>
    <text x="14" y="128" class="cls-attr">+ predicted_fertilizer: str</text>
    <text x="14" y="144" class="cls-attr">+ gate_decision: str = "N/A"</text>
    <text x="14" y="160" class="cls-attr">+ specialist_used: Optional[str]</text>
    <text x="14" y="176" class="cls-attr">+ confidence: Optional[float]</text>
    <text x="14" y="192" class="cls-attr">+ model_version: str [Index]</text>
    <text x="14" y="208" class="cls-attr">+ preprocessing_version: str</text>
    <text x="14" y="224" class="cls-attr">+ feature_schema_version: str</text>
    <text x="14" y="240" class="cls-attr">+ latency_ms: Optional[float]</text>
    <text x="14" y="256" class="cls-attr">+ status: str = "success"  // error</text>
    <text x="14" y="272" class="cls-attr">+ error_message: Optional[str]</text>
    <text x="14" y="288" class="cls-attr">+ is_deleted: bool = False [Index]</text>
    <text x="14" y="304" class="cls-attr">+ deleted_at: Optional[datetime]</text>
    <text x="14" y="320" class="cls-attr">+ created_at: datetime [Index]</text>
    <line x1="0" y1="326" x2="480" y2="326" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="344" class="cls-meth">+ get_parsed_features(): dict</text>
    <text x="14" y="356" class="cls-meth">+ mark_soft_deleted(): void</text>
  </g>

  <!-- CLASS: SoilSample (Left Sub-card) -->
  <g filter="url(#shadow)" transform="translate(1285, 745)">
    <rect width="230" height="210" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="115" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Value Object&gt;&gt;</text>
    <text x="115" y="38" class="cls-name" fill="#14532D">SoilSample</text>
    <line x1="0" y1="46" x2="230" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="10" y="64" class="cls-attr-sm">+ pH: float</text>
    <text x="10" y="80" class="cls-attr-sm">+ nitrogen: float</text>
    <text x="10" y="96" class="cls-attr-sm">+ phosphorus: float</text>
    <text x="10" y="112" class="cls-attr-sm">+ potassium: float</text>
    <text x="10" y="128" class="cls-attr-sm">+ moisture: float</text>
    <line x1="0" y1="136" x2="230" y2="136" stroke="#BBF7D0" class="cls-divider"/>
    <text x="10" y="154" class="cls-meth-sm">+ evaluate_ratio()</text>
    <text x="10" y="172" class="cls-meth-sm">+ detect_deficiency()</text>
    <text x="10" y="190" class="cls-meth-sm">+ validate_ranges()</text>
  </g>

  <!-- CLASS: FertilizerRecommendation (Right Sub-card, moved to x=1550) -->
  <g filter="url(#shadow)" transform="translate(1550, 745)">
    <rect width="230" height="210" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="115" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Value Object&gt;&gt;</text>
    <text x="115" y="38" class="cls-name" fill="#14532D">Recommendation</text>
    <line x1="0" y1="46" x2="230" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="10" y="64" class="cls-attr-sm">+ fertilizer: str</text>
    <text x="10" y="80" class="cls-attr-sm">+ confidence: float</text>
    <text x="10" y="96" class="cls-attr-sm">+ distribution: dict</text>
    <text x="10" y="112" class="cls-attr-sm">+ dosing_notes: str</text>
    <line x1="0" y1="136" x2="230" y2="136" stroke="#BBF7D0" class="cls-divider"/>
    <text x="10" y="154" class="cls-meth-sm">+ is_confident()</text>
    <text x="10" y="172" class="cls-meth-sm">+ runner_up_class()</text>
    <text x="10" y="190" class="cls-meth-sm">+ dosing_guidance()</text>
  </g>

  <!-- CLASS: FarmerFeedback (Domain Entity) -->
  <g filter="url(#shadow)" transform="translate(1295, 995)">
    <rect width="480" height="205" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="240" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Domain Entity / Feedback&gt;&gt;</text>
    <text x="240" y="38" class="cls-name" fill="#14532D">FarmerFeedback (FeedbackLog)</text>
    <line x1="0" y1="46" x2="480" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ feedback_id: str [PK, UUID]</text>
    <text x="14" y="80" class="cls-attr">+ prediction_id: str [FK, Index]</text>
    <text x="14" y="96" class="cls-attr">+ user_id: Optional[str] [FK, Index]</text>
    <text x="14" y="112" class="cls-attr">+ is_correct: bool</text>
    <text x="14" y="128" class="cls-attr">+ actual_fertilizer: Optional[str]</text>
    <text x="14" y="144" class="cls-attr">+ notes: Optional[str]</text>
    <text x="14" y="160" class="cls-attr">+ created_at: datetime</text>
    <line x1="0" y1="166" x2="480" y2="166" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="184" class="cls-meth">+ is_verified(): bool</text>
    <text x="14" y="198" class="cls-meth">+ compute_accuracy_contribution(): float</text>
  </g>

  <!-- CLASS: DatabaseManager (Data Access Layer) -->
  <g filter="url(#shadow)" transform="translate(1295, 1235)">
    <rect width="480" height="210" fill="#F0FDF4" stroke="#16A34A" class="cls-box"/>
    <text x="240" y="20" class="cls-stereo" fill="#14532D">&lt;&lt;Data Access / Database Gateway&gt;&gt;</text>
    <text x="240" y="38" class="cls-name" fill="#14532D">DatabaseManager (db.py)</text>
    <line x1="0" y1="46" x2="480" y2="46" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ db: peewee.Database [SQLite / Postgres]</text>
    <text x="14" y="80" class="cls-attr">+ DATABASE_URL: str</text>
    <line x1="0" y1="86" x2="480" y2="86" stroke="#BBF7D0" class="cls-divider"/>
    <text x="14" y="104" class="cls-meth">+ init_db(): void</text>
    <text x="14" y="122" class="cls-meth">+ close_db(): void</text>
    <text x="14" y="140" class="cls-meth">+ log_prediction(input_feat, pred, ver, conf, lat_ms): str</text>
    <text x="14" y="158" class="cls-meth">+ get_prediction(prediction_id, user_id): PredictionLog</text>
    <text x="14" y="176" class="cls-meth">+ list_predictions(page, per_page, filters, user_id): List</text>
    <text x="14" y="194" class="cls-meth">+ count_predictions(filters, user_id): int</text>
  </g>


  <!-- ==================== PACKAGE 4: ML MICROSERVICE ==================== -->
  <rect x="1875" y="85" width="555" height="1440" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.5" rx="8" stroke-dasharray="8,4"/>
  <rect x="1875" y="85" width="360" height="28" fill="#FDE68A" rx="6"/>
  <text x="1890" y="104" class="pkg-title" fill="#78350F">Package: ml_inference (ML Engine :8001)</text>

  <!-- CLASS: FertilizerPredictor (Service) -->
  <g filter="url(#shadow)" transform="translate(1910, 130)">
    <rect width="490" height="235" fill="#FFFDF5" stroke="#D97706" class="cls-box"/>
    <text x="245" y="20" class="cls-stereo" fill="#B45309">&lt;&lt;ML Service / Inference Engine&gt;&gt;</text>
    <text x="245" y="38" class="cls-name" fill="#78350F">FertilizerPredictor</text>
    <line x1="0" y1="46" x2="490" y2="46" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ registry: ModelRegistry</text>
    <line x1="0" y1="70" x2="490" y2="70" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="90" class="cls-meth">+ predict(input_features: dict, version: str): dict</text>
    <text x="14" y="110" class="cls-meth">- validate_required_features(features: dict, exp: list)</text>
    <text x="14" y="130" class="cls-meth">- build_feature_dataframe(features: dict): DataFrame</text>
    <text x="14" y="150" class="cls-meth">- execute_pipeline(df: DataFrame, pipe: Pipeline): int</text>
    <text x="14" y="170" class="cls-meth">- decode_label(idx: int, encoder: LabelEncoder): str</text>
    <text x="14" y="190" class="cls-meth">- extract_probabilities(pipe, df): dict</text>
    <text x="14" y="210" class="cls-meth">- compute_confidence(probas: np.ndarray): float</text>
  </g>

  <!-- CLASS: ModelRegistry (Registry Pattern) -->
  <g filter="url(#shadow)" transform="translate(1910, 415)">
    <rect width="490" height="245" fill="#FFFDF5" stroke="#D97706" class="cls-box"/>
    <text x="245" y="20" class="cls-stereo" fill="#B45309">&lt;&lt;Registry / Artifact Manager&gt;&gt;</text>
    <text x="245" y="38" class="cls-name" fill="#78350F">ModelRegistry</text>
    <line x1="0" y1="46" x2="490" y2="46" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ base_models_dir: Path</text>
    <text x="14" y="80" class="cls-attr">- _cache: Dict[str, ModelBundle]</text>
    <line x1="0" y1="86" x2="490" y2="86" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="106" class="cls-meth">+ get_active_version_name(): str</text>
    <text x="14" y="126" class="cls-meth">+ load_bundle(version: Optional[str] = None): ModelBundle</text>
    <text x="14" y="146" class="cls-meth">+ invalidate_cache(version: str): void</text>
    <text x="14" y="166" class="cls-meth">+ list_available_versions(): List[str]</text>
    <text x="14" y="186" class="cls-meth">- _validate_bundle(ver: str, pipe, enc, meta): void</text>
    <text x="14" y="206" class="cls-meth">- _load_metadata_json(meta_path: Path): dict</text>
    <text x="14" y="226" class="cls-meth">- _load_joblib_artifact(art_path: Path): Any</text>
  </g>

  <!-- CLASS: ModelBundle (Composite ML Entity) -->
  <g filter="url(#shadow)" transform="translate(1910, 705)">
    <rect width="490" height="180" fill="#FFFDF5" stroke="#D97706" class="cls-box"/>
    <text x="245" y="20" class="cls-stereo" fill="#B45309">&lt;&lt;Dataclass / Composite Bundle&gt;&gt;</text>
    <text x="245" y="38" class="cls-name" fill="#78350F">ModelBundle</text>
    <line x1="0" y1="46" x2="490" y2="46" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ model_version: str</text>
    <text x="14" y="80" class="cls-attr">+ pipeline: sklearn.pipeline.Pipeline</text>
    <text x="14" y="96" class="cls-attr">+ label_encoder: sklearn.preprocessing.LabelEncoder</text>
    <text x="14" y="112" class="cls-attr">+ metadata: Dict[str, Any]</text>
    <line x1="0" y1="118" x2="490" y2="118" stroke="#FDE68A" class="cls-divider"/>
    <text x="14" y="136" class="cls-meth">+ get_expected_features(): List[str]</text>
    <text x="14" y="154" class="cls-meth">+ get_target_classes(): np.ndarray</text>
    <text x="14" y="172" class="cls-meth">+ is_calibrated(): bool</text>
  </g>

  <!-- CLASS: FertilizerPredictionRequest (ML Ingress DTO) -->
  <g filter="url(#shadow)" transform="translate(1910, 930)">
    <rect width="490" height="190" fill="#FEF9C3" stroke="#CA8A04" class="cls-box"/>
    <text x="245" y="20" class="cls-stereo" fill="#854D0E">&lt;&lt;DTO / ML Ingress&gt;&gt;</text>
    <text x="245" y="38" class="cls-name" fill="#713F12">FertilizerPredictionRequest</text>
    <line x1="0" y1="46" x2="490" y2="46" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ Soil_pH: float [0.0 .. 14.0]</text>
    <text x="14" y="80" class="cls-attr">+ Nitrogen_Level: float [&gt;= 0.0]</text>
    <text x="14" y="96" class="cls-attr">+ Phosphorus_Level: float [&gt;= 0.0]</text>
    <text x="14" y="112" class="cls-attr">+ Potassium_Level: float [&gt;= 0.0]</text>
    <text x="14" y="128" class="cls-attr">+ Crop_Growth_Stage: str</text>
    <line x1="0" y1="134" x2="490" y2="134" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="154" class="cls-meth">+ model_dump(): dict</text>
    <text x="14" y="174" class="cls-meth">+ to_feature_vector(): np.ndarray</text>
  </g>

  <!-- CLASS: FertilizerPredictionResponse (ML Egress DTO) -->
  <g filter="url(#shadow)" transform="translate(1910, 1160)">
    <rect width="490" height="190" fill="#FEF9C3" stroke="#CA8A04" class="cls-box"/>
    <text x="245" y="20" class="cls-stereo" fill="#854D0E">&lt;&lt;DTO / ML Egress&gt;&gt;</text>
    <text x="245" y="38" class="cls-name" fill="#713F12">FertilizerPredictionResponse</text>
    <line x1="0" y1="46" x2="490" y2="46" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="64" class="cls-attr">+ fertilizer: str</text>
    <text x="14" y="80" class="cls-attr">+ confidence: Optional[float]</text>
    <text x="14" y="96" class="cls-attr">+ model_version: str</text>
    <text x="14" y="112" class="cls-attr">+ preprocessing_version: str</text>
    <text x="14" y="128" class="cls-attr">+ feature_schema_version: str</text>
    <text x="14" y="144" class="cls-attr">+ probabilities: Optional[Dict[str, float]]</text>
    <line x1="0" y1="150" x2="490" y2="150" stroke="#FDE047" class="cls-divider"/>
    <text x="14" y="170" class="cls-meth">+ get_highest_probability_class(): str</text>
  </g>


  <!-- ==================== CONNECTORS ==================== -->

  <!-- 1. Generalization: RecommendRequest -> BaseModel -->
  <path d="M 305 265 L 305 220" class="conn-line" marker-end="url(#generalization)"/>
  <text x="315" y="248" class="rel-label">&lt;&lt;inherits&gt;&gt;</text>

  <!-- 2. Association: RecommendRequest has CropGrowthStage -->
  <path d="M 305 510 L 305 550" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="315" y="535" class="mult-text">1</text>

  <!-- 3. Generalization: RecommendResponse -> BaseModel -->
  <path d="M 70 770 L 52 770 L 52 175 L 70 175" class="conn-line" marker-end="url(#generalization)"/>
  <text x="56" y="470" class="rel-label" transform="rotate(-90 56 470)">&lt;&lt;inherits BaseModel&gt;&gt;</text>

  <!-- 4. Dependency: RecommendationController validates RecommendRequest -->
  <path d="M 665 230 L 585 230 L 585 350 L 540 350" class="dep-line" marker-end="url(#dep-arrow)"/>
  <text x="592" y="290" class="rel-label">&lt;&lt;validates&gt;&gt;</text>

  <!-- 5. Dependency: RecommendationController produces RecommendResponse -->
  <path d="M 665 280 L 600 280 L 600 800 L 540 800" class="dep-line" marker-end="url(#dep-arrow)"/>
  <text x="605" y="590" class="rel-label">&lt;&lt;produces&gt;&gt;</text>

  <!-- 6. Association: RecommendationController -> MLClient (Clean Vertical 1 to 1) -->
  <path d="M 920 370 L 920 410" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="930" y="395" class="rel-label">invokes</text>
  <text x="905" y="385" class="mult-text">1</text>
  <text x="905" y="405" class="mult-text">1</text>

  <!-- 7. Aggregation: MLClient aggregates CircuitBreaker (Clean Vertical White Diamond) -->
  <path d="M 920 670 L 920 715" class="conn-line" marker-start="url(#aggregation)"/>
  <text x="930" y="697" class="rel-label">guards with</text>
  <text x="905" y="685" class="mult-text">1</text>
  <text x="905" y="708" class="mult-text">1</text>

  <!-- 8. Association: CircuitBreaker has CircuitState (Clean Vertical) -->
  <path d="M 920 955 L 920 1000" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="930" y="980" class="rel-label">current_state</text>
  <text x="905" y="990" class="mult-text">1</text>

  <!-- 9. HTTP REST Cross-Microservice Dependency: MLClient -> FertilizerPredictor -->
  <!-- Clean Skyway route above boxes at y=70 -->
  <path d="M 1175 480 L 1230 480 L 1230 70 L 1850 70 L 1850 200 L 1910 200" class="dep-line" marker-end="url(#dep-arrow)"/>
  <text x="1840" y="64" class="rel-label" fill="#1D4ED8" font-weight="bold" text-anchor="end">HTTP POST /predict [Isolated Virtual Bridge Network backend_net]</text>

  <!-- 10. Aggregation: FertilizerPredictor aggregates ModelRegistry (Clean Vertical White Diamond) -->
  <path d="M 2155 365 L 2155 415" class="conn-line" marker-start="url(#aggregation)"/>
  <text x="2165" y="395" class="rel-label">queries</text>
  <text x="2140" y="382" class="mult-text">1</text>
  <text x="2140" y="408" class="mult-text">1</text>

  <!-- 11. Composition: ModelRegistry creates & caches ModelBundle (Clean Vertical Black Diamond) -->
  <path d="M 2155 660 L 2155 705" class="conn-line" marker-start="url(#composition)"/>
  <text x="2165" y="687" class="rel-label">caches &amp; manages</text>
  <text x="2140" y="675" class="mult-text">1</text>
  <text x="2140" y="698" class="mult-text">0..*</text>

  <!-- 12. Dependency: FertilizerPredictor uses Request/Response (Routed down right alley) -->
  <path d="M 2400 290 L 2415 290 L 2415 1000 L 2400 1000" class="dep-line" marker-end="url(#dep-arrow)"/>
  <text x="2418" y="670" class="rel-label" transform="rotate(90 2418 670)">&lt;&lt;processes&gt;&gt;</text>

  <!-- 13. Association: UserAccount -> PredictionRecord (Clean Vertical 1 to 0..*) -->
  <path d="M 1535 305 L 1535 345" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1545" y="330" class="rel-label">submits</text>
  <text x="1518" y="320" class="mult-text">1</text>
  <text x="1518" y="338" class="mult-text">0..*</text>

  <!-- 14. Composition: PredictionRecord composite-has SoilSample (Left branch Black Diamond) -->
  <path d="M 1400 705 L 1400 745" class="conn-line" marker-start="url(#composition)"/>
  <text x="1408" y="730" class="rel-label">contains</text>
  <text x="1385" y="720" class="mult-text">1</text>
  <text x="1385" y="738" class="mult-text">1</text>

  <!-- 15. Composition: PredictionRecord composite-has FertilizerRecommendation (Right branch Black Diamond) -->
  <path d="M 1665 705 L 1665 745" class="conn-line" marker-start="url(#composition)"/>
  <text x="1673" y="730" class="rel-label">contains</text>
  <text x="1650" y="720" class="mult-text">1</text>
  <text x="1650" y="738" class="mult-text">1</text>

  <!-- 16. Association: PredictionRecord -> FarmerFeedback (Clean Vertical between sub-cards) -->
  <path d="M 1535 705 L 1535 995" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1530" y="975" class="rel-label" text-anchor="end">receives feedback</text>
  <text x="1518" y="720" class="mult-text">1</text>
  <text x="1518" y="985" class="mult-text">0..*</text>

  <!-- 17. Association: RecommendationController logs to DatabaseManager / PredictionRecord -->
  <path d="M 1175 220 L 1235 220 L 1235 410 L 1295 410" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1242" y="315" class="rel-label">logs audit</text>
  <text x="1185" y="212" class="mult-text">1</text>
  <text x="1275" y="402" class="mult-text">1..*</text>

  <!-- 18. Association: PredictionHistoryController queries PredictionRecord -->
  <path d="M 1175 1200 L 1220 1200 L 1220 520 L 1295 520" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1225" y="810" class="rel-label">queries history</text>
  <text x="1185" y="1192" class="mult-text">1</text>
  <text x="1275" y="512" class="mult-text">0..*</text>

  <!-- 19. Association: PredictionHistoryController submits FarmerFeedback -->
  <path d="M 1175 1270 L 1240 1270 L 1240 1080 L 1295 1080" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1245" y="1160" class="rel-label">submits</text>
  <text x="1185" y="1262" class="mult-text">1</text>
  <text x="1275" y="1072" class="mult-text">0..*</text>

  <!-- 20. Association: PredictionRecord and FarmerFeedback managed by DatabaseManager -->
  <path d="M 1535 1200 L 1535 1235" class="conn-line" marker-end="url(#assoc-arrow)"/>
  <text x="1545" y="1220" class="rel-label">persists</text>
  <text x="1518" y="1215" class="mult-text">1</text>


  <!-- ==================== UML NOTATION LEGEND ==================== -->
  <g transform="translate(60, 1545)">
    <rect width="2380" height="55" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2" rx="6"/>
    <text x="25" y="32" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">UML 2.5 Notation Standard Key:</text>
    
    <!-- Generalization -->
    <line x1="260" y1="28" x2="330" y2="28" stroke="#334155" stroke-width="1.8"/>
    <polygon points="330,22 344,28 330,34" fill="#FFFFFF" stroke="#1E293B" stroke-width="1.8"/>
    <text x="355" y="32" class="legend-text">Generalization (Inheritance)</text>

    <!-- Composition -->
    <polygon points="560,28 568,22 576,28 568,34" fill="#0F172A" stroke="#0F172A" stroke-width="1.5"/>
    <line x1="576" y1="28" x2="640" y2="28" stroke="#334155" stroke-width="1.8"/>
    <text x="650" y="32" class="legend-text">Composition (Strong Part-Of)</text>

    <!-- Aggregation -->
    <polygon points="850,28 858,22 866,28 858,34" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.8"/>
    <line x1="866" y1="28" x2="930" y2="28" stroke="#334155" stroke-width="1.8"/>
    <text x="940" y="32" class="legend-text">Aggregation (Weak Has-A)</text>

    <!-- Association -->
    <line x1="1130" y1="28" x2="1195" y2="28" stroke="#334155" stroke-width="1.8"/>
    <path d="M 1187 23 L 1197 28 L 1187 33" fill="none" stroke="#1E293B" stroke-width="1.8"/>
    <text x="1208" y="32" class="legend-text">Directed Association (Multiplicity)</text>

    <!-- Dependency -->
    <line x1="1450" y1="28" x2="1515" y2="28" stroke="#2563EB" stroke-width="1.8" stroke-dasharray="6,4"/>
    <path d="M 1507 23 L 1517 28 L 1507 33" fill="none" stroke="#2563EB" stroke-width="1.8"/>
    <text x="1528" y="32" class="legend-text">Dependency (&lt;&lt;uses&gt;&gt; / &lt;&lt;validates&gt;&gt;)</text>

    <!-- Multiplicity -->
    <text x="1800" y="32" class="legend-text">Multiplicities: 1 = Exactly One, 0..1 = Zero or One, 0..* = Zero or Many, 1..* = One or Many</text>
  </g>

</svg>
"""

with open("uml_class_diagram_fieldwise.svg", "w", encoding="utf-8") as f:
    f.write(svg_uml)

print("Saved updated SVG: uml_class_diagram_fieldwise.svg")

# Render to PNG using Edge headless
output_png = "uml_class_diagram_fieldwise.png"
temp_html = "temp_render_uml.html"

html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin: 0; padding: 0; background: #ffffff; display: flex; justify-content: center; align-items: center; }}
    svg {{ display: block; width: 2500px; height: 1620px; }}
  </style>
</head>
<body>
{svg_uml}
</body>
</html>
"""

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_wrapper)

file_url = f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    f"--screenshot={os.path.abspath(output_png)}",
    "--window-size=2500,1620",
    "--hide-scrollbars",
    file_url
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(temp_html):
    os.remove(temp_html)

if os.path.exists(output_png):
    print(f"Successfully re-rendered {output_png} (Size: {os.path.getsize(output_png)} bytes)")
else:
    print(f"Error generating PNG: {res.stderr}")
