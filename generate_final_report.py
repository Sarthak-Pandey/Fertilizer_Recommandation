import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from report_builder_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders,
    format_row, add_styled_heading, add_body_p, add_bullet_p, add_diagram_image
)

def create_report():
    doc = docx.Document()

    # Set page margins: 1 inch (72 pt) all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Professional header and footer
        section.different_first_page_header_footer = True
        
        # Subsequent pages header
        header = section.header
        p_head = header.paragraphs[0]
        p_head.text = "Experiment 8: Design Analysis Report | Software Engineering Lab"
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if p_head.runs:
            p_head.runs[0].font.name = 'Times New Roman'
            p_head.runs[0].font.size = Pt(9)
            p_head.runs[0].font.italic = True
            p_head.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Subsequent pages footer
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.text = "Student: Sarthak (Roll No: 277) — Fieldwise Fertilizer Recommendation Platform"
        p_foot.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if p_foot.runs:
            p_foot.runs[0].font.name = 'Times New Roman'
            p_foot.runs[0].font.size = Pt(9)
            p_foot.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # -------------------------------------------------------------
    # HEADER / TITLE BLOCK
    # -------------------------------------------------------------
    p_exp = doc.add_paragraph()
    p_exp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_exp.paragraph_format.space_before = Pt(0)
    p_exp.paragraph_format.space_after = Pt(2)
    r_exp = p_exp.add_run("Experiment 8")
    r_exp.font.name = 'Times New Roman'
    r_exp.font.size = Pt(18)
    r_exp.font.bold = True
    r_exp.font.color.rgb = RGBColor(0x1B, 0x43, 0x32) # Forest green

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Design Analysis Report")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    p_topics = doc.add_paragraph()
    p_topics.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topics.paragraph_format.space_before = Pt(0)
    p_topics.paragraph_format.space_after = Pt(14)
    r_topics = p_topics.add_run("Topics: Modularization, Coupling and Cohesion Analysis, Function-Oriented vs. Object-Oriented Design, Top-Down and Bottom-Up Design")
    r_topics.font.name = 'Times New Roman'
    r_topics.font.size = Pt(10.5)
    r_topics.font.italic = True
    r_topics.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # Metadata Table / Card
    meta_table = doc.add_table(rows=3, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    set_table_borders(meta_table, color="94A3B8", sz="6", val="single")

    meta_data = [
        ("Project Name:", "Fieldwise — Intelligent Fertilizer Recommendation System"),
        ("Student Name:", "Sarthak"),
        ("Roll Number:", "277")
    ]

    col_widths = [Inches(1.8), Inches(4.7)]
    for row_idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        format_row(row, bg_color="F8FAFC" if row_idx % 2 == 0 else "FFFFFF")
        
        c0 = row.cells[0]
        c0.width = col_widths[0]
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        c1 = row.cells[1]
        c1.width = col_widths[1]
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.bold = (row_idx > 0)
        r1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) if row_idx > 0 else RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. Introduction", level=1)

    add_body_p(doc, 
        "The software system selected and comprehensively analyzed in this report is Fieldwise — an enterprise-grade, microservice-based Intelligent Fertilizer Recommendation Platform designed for precision agriculture. In contemporary farming, chemical fertilizers are critical for sustaining crop yields; however, injudicious and uncalibrated fertilizer application severely degrades agricultural ecosystems. Over-fertilization leads to soil acidification, hazardous nutrient runoff, groundwater contamination via nitrate leaching, and unnecessary financial expenditures for farmers. Conversely, under-fertilization starves crops of essential nutrients, stunting crop development and causing substantial yield reductions. Traditional agricultural soil laboratory testing requires turnaround times ranging from days to weeks, leaving farmers without timely, actionable insights during critical planting and vegetative growth windows. Fieldwise addresses this critical engineering and societal challenge by providing an autonomous, sub-50-millisecond decision-support platform that ingests real-time soil chemistry, environmental variables, and crop taxonomy to generate high-precision, customized fertilizer prescriptions.",
        bold_prefix="Name and Purpose of Selected Software System: "
    )

    add_body_p(doc, 
        "Fieldwise is engineered to serve three distinct tiers of agricultural stakeholders: (1) Smallholder and Commercial Farmers, who require intuitive, low-latency, and actionable dosage recommendations without navigating complex biochemical data; (2) Agricultural Extension Officers and Professional Agronomists, who require deep diagnostic telemetry, historical soil condition drift trends, feature sensitivity audits, and formal reporting; and (3) Agricultural Cooperatives and Enterprise Farm Managers, who manage multi-plot acreage, run high-volume batch soil evaluations, and track regulatory and environmental compliance.",
        bold_prefix="Target Users: "
    )

    add_body_p(doc, "Major System Functionalities include:", bold_prefix="Major System Functionalities: ")
    add_bullet_p(doc, "Real-Time Multi-Parameter Soil Diagnosis: ", "Ingests continuous numerical inputs (Soil Nitrogen [N], Phosphorus [P], Potassium [K] in mg/kg, soil moisture percentage, ambient temperature, and relative humidity) alongside categorical factors (soil type: Clayey, Loamy, Sandy, Black, Red; and crop type: Paddy, Maize, Cotton, Wheat, Sugarcane, etc.).")
    add_bullet_p(doc, "Ensemble Machine Learning Inference: ", "Executes a serialized machine learning pipeline comprising scikit-learn preprocessors (RobustScaler, categorical encoders) and calibrated XGBoost (v2.1.4) and Random Forest (v1.6.1) classifiers, delivering multiclass fertilizer classifications (e.g., Urea, DAP, 14-35-14, 28-28, 17-17-17, 20-20, 10-26-26) with probability confidence distributions in under 15 milliseconds.")
    add_bullet_p(doc, "Fault-Tolerant Microservice Architecture: ", "Decouples public HTTP API ingress and request validation from compute-intensive machine learning workloads. Incorporates a state-machine Circuit Breaker (CLOSED, OPEN, HALF_OPEN) with exponential backoff retries and non-blocking fallbacks to eliminate cascading failures during inference service degradation.")
    add_bullet_p(doc, "Persistent Telemetry & Historical Auditing: ", "Asynchronously logs every inference request to a relational database (SQLite / PostgreSQL via Peewee ORM), preserving exact input vectors, model versions, predicted outputs, and latency metrics tagged with unique distributed correlation IDs (X-Request-ID).")
    add_bullet_p(doc, "Interactive Client Visualization & Model Governance: ", "Provides a modern Single Page Application (React 19 + TypeScript) featuring dynamic NPK input dials, a historical waveform timeline, dataset export tools (CSV/JSON), and dedicated model governance audit dashboards.")

    # -------------------------------------------------------------
    # 2. SYSTEM ARCHITECTURE AND MODULARIZATION
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. System Architecture and Modularization", level=1)

    add_body_p(doc, 
        "Fieldwise is engineered following clean architecture and decoupled microservices separation of concerns. Rather than relying on a monolithic architecture where a failure in machine learning libraries could destabilize user sessions or database transactions, the system cleanly partitions responsibilities across independent physical and logical modules. Ingress routing, client authentication, rate limiting, and persistent auditing reside within the API Gateway Service (running on port 8000), while model artifact management, numerical feature scaling, and ensemble inference are encapsulated within a dedicated ML Inference Microservice (running on port 8001). Communication between microservices occurs over an isolated bridge network via lightweight HTTP REST contracts with JSON payloads.",
        bold_prefix="Architectural Modularization Overview: "
    )

    add_body_p(doc, 
        "Modularization serves as the cornerstone of maintainability, reusability, and long-term software quality in Fieldwise: (1) Maintainability is significantly elevated because internal refactoring, dependency upgrades, or algorithm tuning inside the ML service (e.g., transitioning from scikit-learn pipelines to deep learning models) do not affect or destabilize the API Gateway, its database schemas, or client authentication logic. Similarly, user interface enhancements in the React frontend occur independently of backend endpoints. (2) Reusability is achieved through centralized domain abstractions: Pydantic validation schemas enforce uniform data validation across API endpoints; the thread-safe Circuit Breaker module can be repurposed across any downstream microservice client; and modular React UI components (such as sliders, confidence dials, and status badges) are reused across the overview cockpit, history dashboard, and model audit interfaces. (3) Independent Scalability allows compute-intensive inference containers to scale horizontally across multiple instances under peak harvest/sowing seasons without requiring identical replication of the I/O-bound API Gateway.",
        bold_prefix="How Modularization Improves Maintainability and Reusability: "
    )

    add_body_p(doc, "The primary modules comprising the Fieldwise platform and their dedicated functional responsibilities are summarized in Table 2.1:")

    # Table 2.1: Major Modules and Responsibilities
    t0 = doc.add_table(rows=7, cols=2)
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    t0.autofit = False
    set_table_borders(t0, color="CBD5E1", sz="4", val="single")

    t0_headers = ["Module Name", "Responsibility"]
    t0_widths = [Inches(2.2), Inches(4.3)]
    for i, h in enumerate(t0_headers):
        cell = t0.rows[0].cells[i]
        cell.width = t0_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t0.rows[0], is_header=True, bg_color="1B4332")

    t0_rows = [
        ("Frontend Client Presentation Tier\n(frontend/)", 
         "Renders the interactive agricultural user interface in React 19 / TypeScript; manages local application state; captures soil NPK telemetry via responsive dial controls; displays real-time prediction results, confidence rings, historical waveform timeline, and model governance dashboards."),
        ("API Gateway & Routing Controller\n(backend/routers/, main.py)", 
         "Serves as the central ingress gateway (FastAPI :8000); orchestrates HTTP routing, CORS configuration, lifecycle events, distributed request tracing (X-Request-ID), sliding-window rate limiting, and dispatching to business services."),
        ("Authentication & Security Module\n(backend/middleware/auth.py)", 
         "Validates API keys (X-API-Key) and cryptographic JWT bearer tokens; enforces role-based access control policies across protected endpoints; prevents unauthorized system ingress."),
        ("Contract Validation Schemas\n(backend/schemas/, ml-service/schemas/)", 
         "Defines strict compile-time and runtime Pydantic v2 data models (RecommendRequest, RecommendResponse, PredictionDetail); validates numerical feature boundaries (e.g., pH 0-14, nutrient levels >= 0) and handles serialization."),
        ("Resilience & Circuit Breaker Engine\n(backend/services/)", 
         "Maintains a thread-safe finite state machine (CLOSED, OPEN, HALF_OPEN) governing downstream calls to the ML service; manages HTTPX connection pools, exponential backoff retries with jitter, and sub-50ms fast fallback responses."),
        ("ML Inference Microservice Engine\n(ml-service/inference/)", 
         "Dedicated machine learning engine (FastAPI :8001); loads versioned model artifacts; performs feature scaling via RobustScaler and OneHotEncoding; computes multi-class probability vectors using XGBoost and Random Forest pipelines; returns fertilizer recommendations.")
    ]

    for r_idx, (m_name, m_resp) in enumerate(t0_rows, start=1):
        row = t0.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = t0_widths[0], t0_widths[1]
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(m_name)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = p1.add_run(m_resp)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Embedded Decomposition Diagram
    add_diagram_image(doc, "diagram_modularization.png", 
                      "Figure 2.1: Hierarchical Module Decomposition Structure Chart of Fieldwise Platform")

    # -------------------------------------------------------------
    # 3. COUPLING AND COHESION ANALYSIS
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. Coupling and Cohesion Analysis", level=1)

    add_styled_heading(doc, "Coupling Analysis", level=2)
    add_body_p(doc, 
        "In software engineering, coupling quantifies the degree of interdependence between interacting software modules. High coupling creates fragile architectures where a modification to one component induces unpredictable breaking changes across dependent modules. Conversely, low coupling promotes loose integration, enabling independent maintenance, testing, and replacement. Fieldwise intentionally targets low coupling by employing standard RESTful HTTP contracts, strictly typed Pydantic data transfer objects (DTOs), and asynchronous database auditing. Table 3.1 analyzes five critical module pairs within the system, evaluating their nature of dependency, coupling level, and formal justification:")

    # Table 3.1: Coupling Analysis
    t1 = doc.add_table(rows=6, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    set_table_borders(t1, color="CBD5E1", sz="4", val="single")

    t1_headers = ["Module Pair", "Nature of Dependency", "Coupling Level", "Justification"]
    t1_widths = [Inches(1.5), Inches(1.5), Inches(1.2), Inches(2.3)]
    for i, h in enumerate(t1_headers):
        cell = t1.rows[0].cells[i]
        cell.width = t1_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t1.rows[0], is_header=True, bg_color="1E3A8A") # Navy

    t1_rows = [
        ("API Router ↔\nPydantic Schemas", 
         "Data Passing / Data Transfer Objects (DTO)", 
         "Low\n(Data Coupling)", 
         "Routers pass raw JSON request payloads to Pydantic models (RecommendRequest) for boundary and type validation. The schema returns typed, immutable data structures. Neither module accesses the internal execution logic or private attributes of the other."),
        ("API Gateway ↔\nML Inference Service", 
         "HTTP/REST Network Communication", 
         "Low\n(Message / Loose Data Coupling)", 
         "The Gateway communicates with the ML Service exclusively via asynchronous HTTP POST requests over an isolated bridge network. Neither service shares memory, local files, database instances, or runtime language dependencies."),
        ("Recommendation Router ↔\nCircuit Breaker & ML Client", 
         "Service Invocation & Control Signals", 
         "Medium-Low\n(Control / Stamp Coupling)", 
         "The router invokes ml_client.predict() and receives either a prediction result dictionary or an MLServiceError exception. The router acts on the control status (e.g., mapping an OPEN circuit to an HTTP 503 fallback), but the state machine mechanics remain encapsulated."),
        ("Gateway Routers ↔\nPeewee Database Models", 
         "Shared Relational Database Store", 
         "Medium\n(External / Data-Store Coupling)", 
         "Routers and background tasks write PredictionLog records directly into the database via Peewee ORM. While the ORM isolates SQL dialect specifics, any modification to underlying table columns requires coordinated updates across models and database migrations."),
        ("Frontend Client ↔\nBackend Gateway API", 
         "HTTP REST JSON API Contract", 
         "Low\n(Contract / Interface Coupling)", 
         "The React 19 single page application interacts with the backend strictly via standardized JSON REST endpoints (/api/v1/fertilizer/recommend). Changes to frontend styling, UI layout, or rendering libraries cause zero side effects in backend business logic.")
    ]

    for r_idx, (m_pair, n_dep, c_lvl, just) in enumerate(t1_rows, start=1):
        row = t1.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for i, val in enumerate([m_pair, n_dep, c_lvl, just]):
            c = row.cells[i]
            c.width = t1_widths[i]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = (i == 0 or i == 2)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) if i != 2 else RGBColor(0x04, 0x78, 0x57)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Cohesion Analysis
    add_styled_heading(doc, "Cohesion Analysis", level=2)
    add_body_p(doc, 
        "Cohesion measures the degree of functional relatedness and focus among the responsibilities belonging to a single software module. In a highly cohesive system, every procedure, class, and method is focused on executing a single, well-defined conceptual task. High cohesion is a fundamental design goal because it simplifies intellectual manageability, minimizes accidental coupling, facilitates modular unit testing, and reduces maintenance costs. Table 3.2 details the cohesion characteristics of five representative modules within Fieldwise:")

    # Table 3.2: Cohesion Analysis
    t2 = doc.add_table(rows=6, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    set_table_borders(t2, color="CBD5E1", sz="4", val="single")

    t2_headers = ["Module Name", "Responsibilities", "Type of Cohesion", "Justification"]
    t2_widths = [Inches(1.6), Inches(2.0), Inches(1.3), Inches(1.6)]
    for i, h in enumerate(t2_headers):
        cell = t2.rows[0].cells[i]
        cell.width = t2_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t2.rows[0], is_header=True, bg_color="1E3A8A")

    t2_rows = [
        ("ml-service/inference/\npredictor.py", 
         "Loads serialized model pickles (XGBoost, Random Forest), applies scalers to incoming features, executes matrix inference, and computes class probabilities.", 
         "Functional Cohesion\n(Highest Cohesion)", 
         "Every method inside this module is exclusively dedicated to the single, well-defined mathematical task of machine learning inference. There are no peripheral concerns such as HTTP routing or database persistence."),
        ("backend/middleware/\nauth.py", 
         "Intercepts ingress HTTP requests, extracts X-API-Key and Bearer JWT headers, validates credentials against security configuration, and raises 401 exceptions on mismatch.", 
         "Functional Cohesion\n(Highest Cohesion)", 
         "The module executes exactly one focused security task: cryptographic identity verification and authentication enforcement."),
        ("backend/services/\ncircuit_breaker.py", 
         "Tracks consecutive failure thresholds, monitors cooldown timers, transitions between CLOSED, OPEN, and HALF_OPEN states, and executes trial probes.", 
         "Sequential / Functional Cohesion", 
         "All internal procedures and state variables work in tight coordination to implement the finite state machine required for fault isolation and service resilience."),
        ("backend/database/\nmigrations/runner.py", 
         "Scans migration directory, checks migration history in the database, applies unapplied SQL migrations sequentially, and records version metadata.", 
         "Procedural / Sequential Cohesion", 
         "The operations must execute in a strictly defined step-by-step procedural sequence to guarantee schema integrity and prevent version drift."),
        ("frontend/src/context/\nAuthContext.tsx", 
         "Manages client user session state, handles login/logout token persistence in browser storage, and provides reactive authentication status to child components.", 
         "Communicational / Functional Cohesion", 
         "All state variables and callback functions operate on the same core data entity: the active authenticated user profile and token lifecycle.")
    ]

    for r_idx, (m_name, m_resp, c_type, just) in enumerate(t2_rows, start=1):
        row = t2.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for i, val in enumerate([m_name, m_resp, c_type, just]):
            c = row.cells[i]
            c.width = t2_widths[i]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = (i == 0 or i == 2)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) if i != 2 else RGBColor(0x1D, 0x4E, 0xD8)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Narrative on Low Coupling and High Cohesion
    add_body_p(doc, 
        "A critical criterion in evaluating software architecture is whether the system adheres to the foundational software engineering principle of 'Low Coupling and High Cohesion.' Based on empirical analysis of the Fieldwise codebase, the system rigorously adheres to this principle: (1) Low Coupling is achieved through clear architectural boundaries. By decoupling the API Gateway from the ML service via network-isolated REST endpoints, changes to ML algorithms, feature scaling logic, or Python scientific libraries do not propagate breaking changes to the Gateway or database layer. Furthermore, the use of Pydantic data models establishes explicit data contracts, ensuring modules communicate via minimal, typed data structures rather than shared memory or global state. (2) High Cohesion is demonstrated across individual modules, where classes and functions exhibit single-responsibility focus. The predictor module handles solely mathematical matrix operations; the authentication middleware strictly handles cryptographic verification; and the Circuit Breaker encapsulates fault tolerance state management. Consequently, Fieldwise achieves high intellectual manageability, streamlined unit testability, and resilient operational stability.",
        bold_prefix="Architectural Evaluation — Adherence to Low Coupling and High Cohesion: "
    )

    # -------------------------------------------------------------
    # 4. FUNCTION-ORIENTED VS. OBJECT-ORIENTED DESIGN
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. Function-Oriented vs. Object-Oriented Design", level=1)

    add_body_p(doc, 
        "Software design methodologies are fundamentally divided into Function-Oriented Design (FOD) and Object-Oriented Design (OOD). Function-Oriented Design (exemplified by Structured Analysis and Design Technique, Data Flow Diagrams, and Structure Charts) decomposes a system based on what the system does, organizing software around computational algorithms and procedures that operate on external data. In contrast, Object-Oriented Design decomposes a system based on real-world domain entities, packaging state (data attributes) and behavior (methods) into cohesive classes that communicate via message passing, inheritance, and polymorphic interfaces. Table 4.1 provides a detailed comparative analysis between these two paradigms across six standardized software engineering criteria:")

    # Table 4.1: FOD vs OOD
    t3 = doc.add_table(rows=7, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    set_table_borders(t3, color="CBD5E1", sz="4", val="single")

    t3_headers = ["Criterion", "Function-Oriented Design (FOD)", "Object-Oriented Design (OOD)"]
    t3_widths = [Inches(1.5), Inches(2.5), Inches(2.5)]
    for i, h in enumerate(t3_headers):
        cell = t3.rows[0].cells[i]
        cell.width = t3_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t3.rows[0], is_header=True, bg_color="1B4332")

    t3_rows = [
        ("Basic design unit", 
         "Functions, subroutines, and procedures. The system is decomposed into procedural transformations (e.g., calculate_dosage(), parse_features()).", 
         "Objects, classes, and encapsulated domain entities (e.g., PredictionLog, CircuitBreaker, PredictorEngine, AuthToken)."),
        ("Data and operations", 
         "Data and procedures are segregated. Data structures are passed between independent functions via arguments or maintained in shared global memory.", 
         "Data attributes and related operations are tightly encapsulated within class boundaries, hiding internal implementation details via encapsulation."),
        ("Modularity", 
         "Decomposition is functional, structured through top-down stepwise refinement based on functional processes.", 
         "Decomposition is object-based, modeled directly around real-world domain abstractions, service boundaries, and stateful lifecycles."),
        ("Reusability", 
         "Low to Moderate. Functions are often tightly coupled to specific parameter lists, data layouts, and contextual calling sequences.", 
         "High. Encapsulated classes, interfaces, and polymorphic abstractions can be extended and reused across disparate subsystems without modification."),
        ("Maintainability", 
         "Challenging in large systems. Modifying a central data structure often triggers cascading ripple effects across numerous dependent procedures.", 
         "High. Changes to private class attributes or internal algorithms remain shielded behind stable public interfaces, preventing collateral defects."),
        ("Suitability for the system", 
         "Moderate. Suitable for localized mathematical data transformations (e.g., feature scaling, matrix multiplication, and categorical encoding).", 
         "Highly Suitable. Ideal for modeling persistent ORM database entities, the stateful Circuit Breaker machine, microservice clients, and UI component hierarchies.")
    ]

    for r_idx, (crit, fod, ood) in enumerate(t3_rows, start=1):
        row = t3.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for i, val in enumerate([crit, fod, ood]):
            c = row.cells[i]
            c.width = t3_widths[i]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = (i == 0)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "Fieldwise implements an intentional hybrid paradigm that capitalizes on the complementary strengths of both design methodologies. Object-Oriented Design serves as the foundational structural paradigm across the platform: Peewee ORM models (e.g., PredictionLog) encapsulate database schema definitions and query methods; the Circuit Breaker engine is implemented as a stateful Python class encapsulating failure thresholds, timers, and state transitions; and the React frontend utilizes an object-component tree model where state and view logic are encapsulated in reusable components. Simultaneously, Functional Design principles are applied within high-throughput, computational sub-pipelines: Pydantic schemas enforce immutable data transformations; feature scaling routines (RobustScaler) operate as pure mathematical functions without mutating input vectors; and stateless FastAPI request handlers ensure predictable, concurrent request execution.",
        bold_prefix="Architectural Justification for Fieldwise: "
    )

    # -------------------------------------------------------------
    # 5. TOP-DOWN AND BOTTOM-UP DESIGN
    # -------------------------------------------------------------
    add_styled_heading(doc, "5. Top-Down and Bottom-Up Design", level=1)

    # 5.1 Top-Down Design
    add_styled_heading(doc, "5.1 Top-Down Design", level=2)
    add_body_p(doc, 
        "Top-Down Design is an analytical, deductive methodology that commences with the global, highest-level system objective and progressively decomposes it through stepwise refinement into increasingly specific subsystems, modules, and concrete leaf subroutines. In the context of Fieldwise, top-down design started with the overarching operational goal: 'Deliver accurate, real-time chemical fertilizer prescriptions to agricultural producers.' This macro-level objective was hierarchically decomposed as follows: (1) Level 1 established three foundational subsystems: the User Ingress Subsystem (managing client interaction and traffic routing), the Decision & ML Subsystem (governing feature transformation and predictive modeling), and the Persistence & Governance Subsystem (handling historical audit logging and observability). (2) Level 2 decomposed each subsystem into cohesive modules: the Ingress Subsystem was divided into the React UI Cockpit, Gateway Routing Controllers, and Authentication Middleware; the Decision Subsystem was partitioned into the Feature Preprocessor, ML Ensemble Classifier, and Model Registry; and the Persistence Subsystem was resolved into the Database Connection Manager, PredictionLog ORM Model, and Prometheus Telemetry Exporter. (3) Level 3 refined these modules into atomic leaf routines, such as handleSliderChange(), verify_api_key(), RobustScaler.transform(), predict_proba(), and PredictionLog.create(). Figure 5.1 visualizes this top-down functional decomposition hierarchy:",
        bold_prefix="Decomposition of the Overall System into Subsystems and Modules: "
    )

    # Embedded Top-Down Diagram
    add_diagram_image(doc, "diagram_top_down.png", 
                      "Figure 5.1: Top-Down Functional Decomposition Diagram of Fieldwise Platform")

    add_body_p(doc, 
        "The primary advantage of Top-Down Design is that it guarantees complete alignment with user requirements and global business objectives from the outset. It establishes early architectural clarity, defines system-level interface boundaries, and facilitates efficient task distribution among engineering teams. However, its principal limitation is that low-level technical complexities—such as machine learning library compatibility, database concurrency locks, or network serialization overheads—may be underestimated during initial high-level abstractions, requiring structural adjustments when concrete leaf components are implemented.",
        bold_prefix="Advantages and Limitations of Top-Down Design: "
    )

    # 5.2 Bottom-Up Design
    add_styled_heading(doc, "5.2 Bottom-Up Design", level=2)
    add_body_p(doc, 
        "Bottom-Up Design is an inductive, synthetic engineering methodology that begins by identifying, implementing, and rigorously testing low-level, reusable primitive components and libraries before aggregating them into higher-level composite services and ultimate system architectures. In Fieldwise, bottom-up design was essential for developing the underlying machine learning and data persistence pipelines. Development initiated at Layer 0 (Foundational Primitives): implementing mathematical normalization scalers (RobustScaler), categorical one-hot encoders, Pydantic type validation models, async HTTPX connection clients, and basic Prometheus metric gauges. At Layer 1 (Encapsulated Modules), these primitives were assembled into stateful domain components: trained XGBoost and Random Forest pipelines were packaged with artifact loaders into a dedicated Predictor Engine; authentication utilities were bundled into a token verifier; and connection pools were bound to Peewee ORM models. At Layer 2 (Microservices), these modules were encapsulated into standalone deployable services: the FastAPI ML Inference Microservice (:8001), the FastAPI API Gateway (:8000), and the React 19 Client SPA. Finally, at Layer 3, these independent services were composed via Docker Compose and virtual bridge networking into the fully integrated Fieldwise enterprise platform. Figure 5.2 illustrates this bottom-up synthesis hierarchy:",
        bold_prefix="Identification and Progressive Combination of Reusable Components: "
    )

    # Embedded Bottom-Up Diagram
    add_diagram_image(doc, "diagram_bottom_up.png", 
                      "Figure 5.2: Bottom-Up Architectural Synthesis Diagram of Fieldwise Platform")

    add_body_p(doc, 
        "The preeminent advantage of Bottom-Up Design is that foundational building blocks are thoroughly verified and optimized through rigorous unit testing prior to system integration, resulting in robust, reusable, and dependable primitives. Furthermore, hardware constraints and library execution bottlenecks are identified immediately during prototyping. Conversely, the key limitation of an exclusively bottom-up approach is the risk of conceptual drift: without continuous high-level architectural governance, independently created low-level components may fail to integrate cleanly or may not align with end-user functional workflows, necessitating refactoring during final integration.",
        bold_prefix="Advantages and Limitations of Bottom-Up Design: "
    )

    # 5.3 Comparison
    add_styled_heading(doc, "5.3 Comparison", level=2)
    add_body_p(doc, 
        "Both Top-Down and Bottom-Up paradigms offer distinct software engineering merits. Table 5.1 compares both approaches across five essential software development dimensions:")

    # Table 5.1: Top-Down vs Bottom-Up
    t4 = doc.add_table(rows=6, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4.autofit = False
    set_table_borders(t4, color="CBD5E1", sz="4", val="single")

    t4_headers = ["Criterion", "Top-Down Design", "Bottom-Up Design"]
    t4_widths = [Inches(1.5), Inches(2.5), Inches(2.5)]
    for i, h in enumerate(t4_headers):
        cell = t4.rows[0].cells[i]
        cell.width = t4_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t4.rows[0], is_header=True, bg_color="1E3A8A")

    t4_rows = [
        ("Starting point", 
         "Global system goal and top-level user requirements; works downward toward implementation details.", 
         "Low-level reusable primitives, hardware/library interfaces, and foundational utilities; works upward toward the complete system."),
        ("Development approach", 
         "Deductive, analytical decomposition through stepwise refinement and functional partitioning.", 
         "Inductive, synthetic composition through iterative assembly and progressive aggregation of verified units."),
        ("Reusability", 
         "Low initially; decomposed components are frequently tailored to specific functional branches of the system hierarchy.", 
         "High; foundational primitives are deliberately engineered as generic, decoupled utilities suitable for multi-module reuse."),
        ("Testing considerations", 
         "Requires extensive mock stubs and test doubles to simulate unbuilt lower-level modules during early testing phases.", 
         "Straightforward unit testing using isolated test drivers; integration testing proceeds incrementally as layers are combined."),
        ("Suitability", 
         "Highly suited for high-level enterprise system architecture, requirement traceability, and defining REST API contracts.", 
         "Highly suited for scientific computing, ML model training pipelines, mathematical preprocessing algorithms, and low-level utility libraries.")
    ]

    for r_idx, (crit, td, bu) in enumerate(t4_rows, start=1):
        row = t4.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for i, val in enumerate([crit, td, bu]):
            c = row.cells[i]
            c.width = t4_widths[i]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = (i == 0)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(doc, 
        "In modern commercial software engineering, superior outcomes are attained by synthesizing both paradigms into a hybrid approach (often referred to as 'sandwich' or 'contract-driven' development). Fieldwise employed Top-Down design to define the overarching microservice topology, API contracts, and user interaction flows, while simultaneously utilizing Bottom-Up engineering to prototype the machine learning pipelines, feature transformation modules, and database access utilities. This dual-track strategy guaranteed that all implemented primitives converged cleanly into a cohesive, user-aligned enterprise platform.",
        bold_prefix="Methodological Synthesis: "
    )

    # -------------------------------------------------------------
    # 6. OVERALL DESIGN EVALUATION
    # -------------------------------------------------------------
    add_styled_heading(doc, "6. Overall Design Evaluation", level=1)

    add_body_p(doc, 
        "An objective evaluation of the Fieldwise software design requires analyzing its strengths, identifying architectural trade-offs, and formulating concrete suggestions for improvement across its primary design aspects. Table 6.1 synthesizes this comprehensive design evaluation:")

    # Table 6.1: Overall Design Evaluation
    t5 = doc.add_table(rows=5, cols=4)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5.autofit = False
    set_table_borders(t5, color="CBD5E1", sz="4", val="single")

    t5_headers = ["Design Aspect", "Strengths", "Weaknesses", "Suggested Improvements"]
    t5_widths = [Inches(1.3), Inches(1.8), Inches(1.6), Inches(1.8)]
    for i, h in enumerate(t5_headers):
        cell = t5.rows[0].cells[i]
        cell.width = t5_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    format_row(t5.rows[0], is_header=True, bg_color="1B4332")

    t5_rows = [
        ("Modularization", 
         "Clean physical decoupling of Gateway, ML Inference, Persistence, and Frontend tiers. Independent Docker containerization enables isolated deployment, technology independence, and horizontal scaling.", 
         "Introduces inter-process network overhead (~5-8 ms per inference request) and minor operational complexity compared to an in-process monolithic Python script.", 
         "Implement high-throughput binary protocols (gRPC over HTTP/2) for inter-service communication to reduce serialization latency to sub-2ms."),
        ("Coupling and Cohesion", 
         "High functional cohesion in prediction and security modules; low coupling across microservices via REST JSON contracts and Circuit Breaker isolation.", 
         "Database schema alterations (e.g., adding user foreign keys) require synchronous updates across ORM models, migration scripts, and Pydantic schemas.", 
         "Adopt contract-first schema generation tools (OpenAPI/Protobuf generators) to automate synchronization between database schemas and client models."),
        ("Design Approach", 
         "Successful harmony of Top-Down structural decomposition with Bottom-Up component engineering, ensuring both conceptual coherence and unit-tested rigor.", 
         "Initial standalone ML training scripts required post-hoc refactoring to conform to the strict Pydantic schemas defined during top-down API design.", 
         "Institute automated MLOps pipelines where model serialization artifacts automatically export matching schema validators during training runs."),
        ("System Decomposition", 
         "Clear separation between compute-intensive predictive workloads (port 8001) and I/O-bound web traffic (port 8000), optimizing system resource allocation.", 
         "Single relational database instance currently serves both transactional user authentication and high-frequency prediction audit logging.", 
         "Segregate analytical prediction logs from operational user credentials using CQRS (Command Query Responsibility Segregation) or a dedicated time-series datastore.")
    ]

    for r_idx, (d_asp, strn, wkn, sug) in enumerate(t5_rows, start=1):
        row = t5.rows[r_idx]
        format_row(row, bg_color="F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for i, val in enumerate([d_asp, strn, wkn, sug]):
            c = row.cells[i]
            c.width = t5_widths[i]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = (i == 0)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 7. RECOMMENDATIONS
    # -------------------------------------------------------------
    add_styled_heading(doc, "7. Recommendations", level=1)

    add_body_p(doc, 
        "To elevate the architectural robustness, throughput, and long-term maintainability of the Fieldwise platform, four specific, concrete design and architectural improvements are recommended:")

    add_bullet_p(doc, "1. Asynchronous Task Queue & Streaming for Batch Inferences: ", 
        "Currently, high-volume batch soil evaluations submitted by agricultural cooperatives are processed via synchronous HTTP loops, which risk exhausting Gateway worker connections during traffic spikes. The system should integrate an asynchronous task queue (e.g., Celery with Redis or RabbitMQ). Clients submitting batch soil records receive an immediate acknowledgment with a unique job ID, while background worker processes consume batches, execute inference asynchronously, and stream real-time completion status back to the frontend via WebSockets or Server-Sent Events (SSE).")

    add_bullet_p(doc, "2. High-Performance gRPC Communication with Protocol Buffers: ", 
        "Inter-service communication between the API Gateway and the ML Inference Microservice currently relies on JSON serialization over HTTP/1.1. Transitioning internal microservice communication to gRPC over HTTP/2 using binary Protocol Buffers (protobuf) will eliminate text-based JSON parsing overhead, enforce strictly typed cross-service contracts at compile time, and reduce network serialization latency by approximately 65%, driving internal round-trip times down to sub-2 milliseconds.")

    add_bullet_p(doc, "3. Automated Continuous Model Drift Monitoring & MLOps Pipeline: ", 
        "Soil chemical dynamics and regional crop cultivars evolve across seasons. In the current implementation, model retraining is triggered manually. The architecture should be augmented with an automated MLOps monitoring pipeline (such as Evidently AI or MLflow). Incoming soil test distributions should be continuously benchmarked against training baselines to detect data drift or concept degradation. When statistical drift exceeds predefined thresholds, automated alerts should notify agronomists and trigger automated retraining pipelines using newly verified harvest audit logs.")

    add_bullet_p(doc, "4. Client-Side Edge Inference via WebAssembly (Wasm) / PWA: ", 
        "Agricultural producers frequently operate in remote geographical plots characterized by weak or nonexistent cellular network connectivity. To overcome this infrastructure limitation, the system should export lightweight, quantized inference models (using ONNX Runtime Web or TensorFlow Lite) capable of executing directly within the client browser via WebAssembly. Coupled with Progressive Web App (PWA) offline caching, farmers can receive instantaneous fertilizer prescriptions directly in the field, with prediction audit records automatically synchronizing to the central database once connectivity is restored.")

    # -------------------------------------------------------------
    # 8. CONCLUSION
    # -------------------------------------------------------------
    add_styled_heading(doc, "8. Conclusion", level=1)

    add_body_p(doc, 
        "This design analysis report has conducted an exhaustive, rigorous examination of the Fieldwise Fertilizer Recommendation Platform across core software engineering dimensions: modularization, coupling and cohesion, functional versus object-oriented design, and top-down versus bottom-up development methodologies. Software design principles do not merely represent theoretical academic standards; they are the fundamental determinants of whether a software system succeeds or fails in production environments.",
        bold_prefix="Summary of Findings: "
    )

    add_body_p(doc, 
        "The empirical analysis demonstrates that: (1) Disciplined Modularization prevents cascading system failures, decouples rapid frontend and algorithmic iteration from backend stability, and enables independent horizontal scaling. (2) Maintaining Low Coupling via well-defined REST contracts, strongly typed Pydantic schemas, and Circuit Breaker isolation eliminates fragile cross-service dependencies, allowing components to evolve without unintended ripple effects. (3) Enforcing High Cohesion ensures that individual modules remain tightly focused on single conceptual responsibilities, dramatically reducing software defect density and accelerating developer onboarding. (4) Employing a Hybrid Paradigm—synthesizing Object-Oriented Design for domain state modeling with Functional Design for data transformation pipelines—delivers an optimal balance of robustness, immutability, and runtime performance. Finally, integrating Top-Down architectural decomposition with Bottom-Up primitive construction ensures that system capabilities remain perfectly aligned with user requirements while resting upon thoroughly verified, reusable foundation blocks. By adhering faithfully to these foundational design principles, Fieldwise achieves an exceptional standard of maintainability, reusability, fault tolerance, and software quality, serving as an exemplar of modern software engineering in precision agriculture.",
        bold_prefix="Impact of Design Principles on Software Quality: "
    )

    # Save DOCX
    docx_filename = "Design Analysis Report.docx"
    doc.save(docx_filename)
    print(f"Report saved to {docx_filename} ({os.path.getsize(docx_filename)} bytes)")

if __name__ == "__main__":
    create_report()
