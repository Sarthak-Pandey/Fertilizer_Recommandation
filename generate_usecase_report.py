import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
import win32com.client

from report_builder_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders,
    format_row, add_styled_heading, add_body_p, add_bullet_p, add_diagram_image
)

def build_usecase_report():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        section.different_first_page_header_footer = True
        
        # Subsequent pages header
        header = section.header
        p_head = header.paragraphs[0]
        p_head.text = "Experiment 5: UML Use Case Modeling | Software Engineering Lab"
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if p_head.runs:
            p_head.runs[0].font.name = 'Times New Roman'
            p_head.runs[0].font.size = Pt(8.5)
            p_head.runs[0].font.italic = True
            p_head.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Subsequent pages footer
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.text = "Student: Sarthak (Roll No: 277) — Fieldwise Fertilizer Recommendation Platform"
        p_foot.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if p_foot.runs:
            p_foot.runs[0].font.name = 'Times New Roman'
            p_foot.runs[0].font.size = Pt(8.5)
            p_foot.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # -------------------------------------------------------------
    # HEADER / TITLE BLOCK
    # -------------------------------------------------------------
    p_exp = doc.add_paragraph()
    p_exp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_exp.paragraph_format.space_before = Pt(0)
    p_exp.paragraph_format.space_after = Pt(2)
    r_exp = p_exp.add_run("Software Engineering Laboratory — Experiment 5")
    r_exp.font.name = 'Times New Roman'
    r_exp.font.size = Pt(13)
    r_exp.font.bold = True
    r_exp.font.color.rgb = RGBColor(0x0F, 0x76, 0x6E)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Actor & Use Case Identification, UML Use Case Diagram, and Use Case Narratives")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Project: Fieldwise — Intelligent Fertilizer Recommendation System")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="D0D7DE")
    
    meta_data = [
        ("Student Name & Roll No:", "Sarthak (Roll No: 277)"),
        ("Course / Lab:", "Software Engineering Laboratory (CS304)"),
        ("Approved Project Base:", "Fieldwise Fertilizer Recommendation System (SRS v1.0.0 Approved)"),
        ("Experiment Objective:", "Identify actors and use cases from approved requirements; construct UML 2.5 Use Case Diagram and rigorous use case descriptions/narratives.")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        format_row(row, is_header=False, bg_color="F8FAFC" if i % 2 == 0 else "FFFFFF")
        row.cells[0].paragraphs[0].text = k
        row.cells[0].paragraphs[0].runs[0].font.name = 'Times New Roman'
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        row.cells[0].width = Inches(2.3)

        row.cells[1].paragraphs[0].text = v
        row.cells[1].paragraphs[0].runs[0].font.name = 'Times New Roman'
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        row.cells[1].width = Inches(4.6)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 1: IDENTIFICATION OF ACTORS
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. Identification of Actors from Approved Requirements", level=1)
    add_body_p(doc, 
        "In accordance with SRS Section 2.2 and Section 3.2 of the approved Fieldwise Fertilizer Recommendation System, "
        "system actors are classified into Primary Actors (human end-users initiating business transactions) and "
        "Secondary/Supporting Actors (external services and automated subsystems collaborating to fulfill requests).",
        space_after=6
    )

    actor_table = doc.add_table(rows=1, cols=4)
    actor_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(actor_table, color="D0D7DE")
    headers = ["Actor Name", "Stereotype", "Access Channel", "Role & Responsibilities"]
    hdr_row = actor_table.rows[0]
    format_row(hdr_row, is_header=True, bg_color="1B5E20")
    for idx, text in enumerate(headers):
        p = hdr_row.cells[idx].paragraphs[0]
        p.text = text
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    actors_info = [
        ("Farmer / Agronomist", "Primary (Human)", "Web / Mobile Interface", "Submits soil nutrients (N, P, K, pH) and crop stages; views fertilizer dosage recommendations and past logs."),
        ("Agri-Tech Developer", "Primary (External)", "REST API Gateway (X-API-Key)", "Integrates automated soil IoT sensors and third-party farm management software with prediction endpoints."),
        ("System Administrator", "Primary (Human)", "Admin Portal & Prometheus Probes", "Monitors service uptime, telemetry, database logs, and configures circuit breaker thresholds."),
        ("ML Inference Service", "Secondary (Internal Subsystem)", "Internal REST API (:8001)", "Executes machine learning pipelines (XGBoost / Random Forest), outputs prediction classes and confidence scores."),
        ("Supabase Auth Service", "Secondary (External Service)", "OAuth2 / JWT Token Provider", "Verifies credentials, manages user registration, and issues cryptographic bearer tokens.")
    ]

    col_widths = [Inches(1.6), Inches(1.3), Inches(1.6), Inches(2.4)]
    for i, a in enumerate(actors_info):
        row = actor_table.add_row()
        format_row(row, is_header=False, bg_color="F8FAFC" if i % 2 == 0 else "FFFFFF")
        for c_idx in range(4):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            p = cell.paragraphs[0]
            p.text = a[c_idx]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9)
            if c_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            else:
                p.runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 2: IDENTIFICATION OF USE CASES
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. Identification of Use Cases from Approved Requirements", level=1)
    add_body_p(doc,
        "The functional requirements (SRS Sections 2.1, 3.1, and 3.2) yield the following organized catalog of core "
        "user-facing use cases and internal modular supporting use cases:",
        space_after=6
    )

    uc_table = doc.add_table(rows=1, cols=4)
    uc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(uc_table, color="D0D7DE")
    hdr_row = uc_table.rows[0]
    format_row(hdr_row, is_header=True, bg_color="1B5E20")
    for idx, text in enumerate(["Use Case ID", "Use Case Name", "Stereotype / Type", "Associated Actors & Purpose"]):
        p = hdr_row.cells[idx].paragraphs[0]
        p.text = text
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    use_cases_list = [
        ("UC-01", "Register Account", "User-Facing (Core)", "Farmer, Supabase Auth. Establishes secure tenant account."),
        ("UC-02", "Login / Authenticate", "User-Facing (Core)", "Farmer, Supabase Auth. Issues JWT session token."),
        ("UC-03", "Submit Soil & Crop Data", "User-Facing (Core)", "Farmer / User. Enters N, P, K, pH, and growth stage."),
        ("UC-04", "Get Fertilizer Recommendation", "User-Facing (Primary)", "Farmer, ML Service. Main business transaction generating recommendation."),
        ("UC-05", "Validate Input Data", "<<include>> of UC-04", "Backend Gateway. Checks domain boundary constraints (e.g., pH 0-14)."),
        ("UC-06", "Preprocess Soil & Crop Data", "<<include>> of UC-04", "Backend Gateway. Normalizes categorical strings and scales numerical vectors."),
        ("UC-07", "Run ML Prediction", "<<include>> of UC-04", "ML Inference Microservice. Computes multi-class probability scores."),
        ("UC-08", "Generate Recommendation", "<<include>> of UC-04", "Backend Gateway. Maps prediction vector to fertilizer type and dosage."),
        ("UC-09", "Store Prediction Audit Record", "<<include>> of UC-04", "Peewee ORM / SQLite. Asynchronously persists request, latency, and outcome."),
        ("UC-10", "View Recommendation Details", "<<include>> of UC-04", "Farmer / User. Displays fertilizer name, dosage, and rationale."),
        ("UC-11", "View Recommendation History", "User-Facing (Core)", "Farmer / User. Lists historical soil audits with pagination."),
        ("UC-12", "Search / Filter History", "<<extend>> of UC-11", "Farmer / User. Optional date-range and crop stage filtering on history."),
        ("UC-13", "Retrieve Historical Records", "<<include>> of UC-11", "Backend Database. Executes paginated SQL query from predictions table."),
        ("UC-14", "View System Audit Dashboard", "Administrative (Core)", "System Admin. Visualizes aggregated prediction stats and latency metrics.")
    ]

    uc_col_widths = [Inches(1.1), Inches(2.1), Inches(1.6), Inches(2.1)]
    for i, uc in enumerate(use_cases_list):
        row = uc_table.add_row()
        format_row(row, is_header=False, bg_color="F8FAFC" if i % 2 == 0 else "FFFFFF")
        for c_idx in range(4):
            cell = row.cells[c_idx]
            cell.width = uc_col_widths[c_idx]
            p = cell.paragraphs[0]
            p.text = uc[c_idx]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9)
            if c_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif c_idx == 2 and "include" in uc[c_idx]:
                p.runs[0].font.italic = True
                p.runs[0].font.color.rgb = RGBColor(0x04, 0x78, 0x57)
            else:
                p.runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 3: UML USE CASE DIAGRAM
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. UML 2.5 Use Case Diagram", level=1)
    add_body_p(doc,
        "The diagram below models the complete functional boundary of Fieldwise Fertilizer Recommendation Platform. "
        "It defines primary actors, secondary service actors, core transaction use cases, and modular relationships "
        "including six <<include>> dependencies and one <<extend>> relationship.",
        space_after=8
    )

    img_path = os.path.abspath("usecase_diagram_fieldwise.png")
    if os.path.exists(img_path):
        add_diagram_image(doc, img_path, caption_text="Figure 5.1: Standard UML 2.5 Use Case Diagram for Fieldwise Fertilizer Recommendation Platform", width_inches=6.8)
    else:
        add_body_p(doc, "[Use Case Diagram image not found at usecase_diagram_fieldwise.png]", italic=True)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 4: USE CASE DESCRIPTIONS / NARRATIVES
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. Structured Use Case Descriptions / Narratives", level=1)
    add_body_p(doc,
        "To eliminate ambiguity and ensure requirements traceability, detailed use case narratives are specified "
        "following the Alistair Cockburn industry-standard format. Each use case description contains non-duplicated, "
        "scenario-specific preconditions, postconditions, triggers, and concrete normal and exceptional execution flows.",
        space_after=6
    )

    def add_narrative_table(uc_id, uc_name, narrative_dict):
        add_styled_heading(doc, f"4.{narrative_dict['num']} Use Case Narrative: {uc_id} — {uc_name}", level=2)
        tbl = doc.add_table(rows=0, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="D0D7DE")

        fields = [
            ("Use Case ID & Name", f"{uc_id}: {uc_name}"),
            ("Primary Actor", narrative_dict["actor"]),
            ("Secondary Actors", narrative_dict["sec_actors"]),
            ("Scope & Level", narrative_dict["scope"]),
            ("Goal in Context", narrative_dict["goal"]),
            ("Preconditions", narrative_dict["pre"]),
            ("Success Postconditions", narrative_dict["post_success"]),
            ("Failure Postconditions", narrative_dict["post_fail"]),
            ("Trigger", narrative_dict["trigger"]),
            ("Main Success Scenario (Normal Flow)", narrative_dict["main_flow"]),
            ("Extensions / Exception Flows", narrative_dict["alt_flow"])
        ]

        for i, (k, v) in enumerate(fields):
            row = tbl.add_row()
            format_row(row, is_header=False, bg_color="F1F5F9" if i in [0, 9, 10] else ("F8FAFC" if i % 2 == 0 else "FFFFFF"))
            
            # Left cell (Key)
            c0 = row.cells[0]
            c0.width = Inches(2.0)
            p0 = c0.paragraphs[0]
            p0.text = k
            p0.runs[0].font.name = 'Times New Roman'
            p0.runs[0].font.size = Pt(9)
            p0.runs[0].font.bold = True
            p0.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

            # Right cell (Value)
            c1 = row.cells[1]
            c1.width = Inches(4.9)
            p1 = c1.paragraphs[0]
            p1.text = v
            p1.runs[0].font.name = 'Times New Roman'
            p1.runs[0].font.size = Pt(9)
            p1.runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Narrative 1: UC-04
    narrative_uc4 = {
        "num": "1",
        "actor": "Farmer / Agronomist",
        "sec_actors": "ML Inference Microservice, SQLite/PostgreSQL Database",
        "scope": "Fieldwise Fertilizer Recommendation Platform (User-Goal Level)",
        "goal": "Receive a machine-learning derived fertilizer recommendation with dosage and confidence metrics.",
        "pre": "1. User is authenticated with a valid session token.\n2. API Gateway is online with circuit breaker in CLOSED state.",
        "post_success": "1. Optimal fertilizer recommendation with probability score and application guidelines is displayed to the user.\n2. Transaction audit record is persisted with assigned UUID in database.",
        "post_fail": "User receives a descriptive error code (HTTP 422 for range violation, or HTTP 503 fallback message if ML service is down). No corrupted record saved.",
        "trigger": "User submits the recommendation form via web interface or invokes POST /api/v1/fertilizer/recommend.",
        "main_flow": "1. User submits soil parameters: Soil pH, Nitrogen (N), Phosphorus (P), Potassium (K), and Crop Growth Stage.\n"
                     "2. System invokes <<include>> UC-05 (Validate Input Data) to verify domain ranges (pH: 0-14, N/P/K >= 0).\n"
                     "3. System invokes <<include>> UC-06 (Preprocess Soil & Crop Data) to encode growth stage and scale numerical features.\n"
                     "4. System invokes <<include>> UC-07 (Run ML Prediction) by querying the ML Microservice over internal REST API.\n"
                     "5. ML microservice executes model inference and returns class probabilities.\n"
                     "6. System invokes <<include>> UC-08 (Generate Recommendation) to map top class to trade fertilizer name and application dosage.\n"
                     "7. System invokes <<include>> UC-09 (Store Prediction Audit Record) to asynchronously persist request and output to database.\n"
                     "8. System invokes <<include>> UC-10 (View Recommendation Details) to display results to the user.",
        "alt_flow": "2a. Input Validation Failure: System aborts execution, returns HTTP 422 Unprocessable Entity specifying exact invalid field, and highlights input box.\n"
                     "4a. ML Microservice Unreachable / Timeout: System retries with exponential backoff (2 retries). If still unavailable, circuit breaker increments failure count and triggers fallback response (HTTP 503) without crashing."
    }

    # Narrative 2: UC-02
    narrative_uc2 = {
        "num": "2",
        "actor": "Farmer / Agronomist",
        "sec_actors": "Supabase Authentication Service",
        "scope": "Security & Identity Management Subsystem (Subfunction Level)",
        "goal": "Authenticate user identity and acquire a cryptographic JWT access token for API requests.",
        "pre": "User possesses an existing registered account with verified email address.",
        "post_success": "JWT Bearer token and refresh token are issued; user session is initialized in browser client.",
        "post_fail": "Authentication fails; user is notified of invalid credentials; access to protected features remains blocked.",
        "trigger": "User inputs email and password on login screen and clicks 'Sign In'.",
        "main_flow": "1. User enters registered email address and password into the login interface.\n"
                     "2. Client transmits HTTPS credentials to the Supabase Auth endpoint.\n"
                     "3. Supabase verifies bcrypt password hash against user identity store.\n"
                     "4. Auth service generates signed JWT token containing user UID and expiry timestamp.\n"
                     "5. Client stores access token in secure storage and transitions user to recommendation dashboard.",
        "alt_flow": "3a. Invalid Credentials: Auth service returns HTTP 401 Unauthorized; login UI displays 'Invalid email or password' with 3 remaining attempts alert.\n"
                     "3b. Unverified Account: Auth service prompts user to verify email link before login is permitted."
    }

    # Narrative 3: UC-11
    narrative_uc3 = {
        "num": "3",
        "actor": "Farmer / Agronomist",
        "sec_actors": "Backend Database Subsystem (Peewee ORM)",
        "scope": "Prediction History & Auditing Subsystem (User-Goal Level)",
        "goal": "Review historical soil test evaluations and previous fertilizer recommendation outcomes.",
        "pre": "User is authenticated and has at least one previous recommendation recorded.",
        "post_success": "Paginated history table rendered with soil metrics, recommended fertilizer, confidence score, and timestamp.",
        "post_fail": "Empty state notification displayed if no records exist; error toast shown if database connection fails.",
        "trigger": "User navigates to the 'Recommendation History' tab in the navigation menu.",
        "main_flow": "1. User clicks 'View History' in the navigation bar.\n"
                     "2. Client issues GET /api/v1/predictions?page=1&limit=10 with Bearer authorization header.\n"
                     "3. System invokes <<include>> UC-13 (Retrieve Historical Records) to query database with pagination offset.\n"
                     "4. Database returns list of prediction records sorted chronologically descending.\n"
                     "5. Client renders tabular grid showing test dates, N-P-K readings, recommended fertilizer, and confidence percentage.",
        "alt_flow": "1a. User applies filtering criteria: <<extend>> UC-12 (Search / Filter History) is activated; user selects crop stage or date filter, triggering filtered query GET /api/v1/predictions?crop_stage=Vegetative.\n"
                     "4a. Zero Records Found: UI displays friendly empty-slate graphic inviting user to perform their first soil test."
    }

    # Narrative 4: UC-14
    narrative_uc4_admin = {
        "num": "4",
        "actor": "System Administrator / DevOps",
        "sec_actors": "FastAPI Gateway, Prometheus Metrics Collector",
        "scope": "System Administration & Telemetry Subsystem (Administrative Level)",
        "goal": "Inspect system operational performance, prediction volume, mean confidence, and error distributions.",
        "pre": "Administrator is logged in with administrative security role.",
        "post_success": "Real-time dashboard displays total queries, popular fertilizers, circuit breaker status, and p95 latency.",
        "post_fail": "Access denied (HTTP 403) for non-administrative users.",
        "trigger": "Administrator accesses /admin/dashboard or requests GET /api/v1/predictions/stats.",
        "main_flow": "1. Admin opens the System Telemetry page.\n"
                     "2. Gateway queries internal aggregation counters and Prometheus /metrics endpoint.\n"
                     "3. Backend aggregates total recommendation count, average confidence score, and top 5 fertilizers.\n"
                     "4. Admin dashboard renders visual charts (time-series inference latency, circuit breaker state CLOSED, and memory usage).",
        "alt_flow": "2a. Telemetry Collector Degraded: Gateway serves cached summary statistics with an 'Out of sync' warning badge."
    }

    add_narrative_table("UC-04", "Get Fertilizer Recommendation", narrative_uc4)
    add_narrative_table("UC-02", "Login / Authenticate", narrative_uc2)
    add_narrative_table("UC-11", "View Recommendation History", narrative_uc3)
    add_narrative_table("UC-14", "View System Audit Dashboard", narrative_uc4_admin)

    # -------------------------------------------------------------
    # SECTION 5: CONCLUSION & VERIFICATION
    # -------------------------------------------------------------
    add_styled_heading(doc, "5. Conclusion and Requirements Traceability", level=1)
    add_body_p(doc,
        "The identification of actors, use case structuring, UML 2.5 modeling, and formal Cockburn narratives for "
        "Experiment 5 successfully establish 100% requirements traceability to SRS v1.0.0. "
        "All user-facing capabilities (Farmer/Agronomist interactions), automated secondary services (Supabase, ML Microservice, Database), "
        "and architectural fault tolerances (Circuit Breaker and Validation) are systematically accounted for without redundancy.",
        space_after=12
    )

    # Sign-off paragraph
    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run("Experiment 5 Approved & Completed — Academic Lab Submission")
    r_sig.font.name = 'Times New Roman'
    r_sig.font.size = Pt(10)
    r_sig.font.italic = True
    r_sig.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    docx_file = "Experiment_5.docx"
    doc.save(docx_file)
    print(f"Successfully generated DOCX: {docx_file} (Size: {os.path.getsize(docx_file)} bytes)")
    return docx_file

def convert_docx_to_pdf(docx_path="Experiment_5.docx", pdf_path="Experiment_5.pdf"):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    
    print(f"Converting DOCX to PDF...")
    print(f"  Source: {abs_docx}")
    print(f"  Target: {abs_pdf}")
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    word.AutomationSecurity = 3
    
    try:
        doc = word.Documents.Open(abs_docx, ReadOnly=True, AddToRecentFiles=False)
        doc.SaveAs(abs_pdf, FileFormat=17)
        doc.Close(False)
        print(f"Conversion successful! PDF size: {os.path.getsize(abs_pdf)} bytes")
    finally:
        word.Quit()

if __name__ == "__main__":
    docx_file = build_usecase_report()
    pdf_file = "Experiment_5.pdf"
    convert_docx_to_pdf(docx_file, pdf_file)
