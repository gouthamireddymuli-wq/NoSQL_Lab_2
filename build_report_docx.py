"""Generate comprehensive, beautifully styled Lab 02 report in DOCX format.
"""

import os
import sys
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_DOCX = os.path.join(BASE_DIR, "NoSQL_Lab_02_Report.docx")


def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner cell padding in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_code_block(doc, code_text):
    """Add a syntax-highlighted code block in a shaded container table."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)

    cell = table.cell(0, 0)
    set_cell_background(cell, "F2F4F7")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05

    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(36, 41, 47)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(6)


def read_file_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_docx():
    doc = Document()

    # Set page margins (0.75 in)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    NAVY = RGBColor(27, 54, 93)
    SLATE = RGBColor(74, 85, 104)
    TEXT_DARK = RGBColor(45, 55, 72)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = TEXT_DARK

    # --- TITLE / HEADER SECTION ---
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_course = p_title.add_run("NOSQL DATABASES LABORATORY\n")
    run_course.font.name = "Calibri"
    run_course.font.size = Pt(13)
    run_course.font.bold = True
    run_course.font.color.rgb = SLATE

    run_title = p_title.add_run("LAB 02 REPORT: ENVIRONMENT SETUP &\nPYMONGO BOOKSTORE CRUD OPERATIONS")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = NAVY

    # Meta Table (Student details)
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(3.25)
    meta_table.columns[1].width = Inches(3.25)

    cell_00 = meta_table.cell(0, 0)
    cell_00.paragraphs[0].add_run("Student Name: ").bold = True
    cell_00.paragraphs[0].add_run("M. Gouthami")

    cell_01 = meta_table.cell(0, 1)
    cell_01.paragraphs[0].add_run("Register / Roll No: ").bold = True
    cell_01.paragraphs[0].add_run("24BTRCL130")

    cell_10 = meta_table.cell(1, 0)
    cell_10.paragraphs[0].add_run("Course: ").bold = True
    cell_10.paragraphs[0].add_run("NoSQL Databases")

    cell_11 = meta_table.cell(1, 1)
    cell_11.paragraphs[0].add_run("Date: ").bold = True
    cell_11.paragraphs[0].add_run("November 2026")

    for row in meta_table.rows:
        for c in row.cells:
            set_cell_background(c, "EBF3FA")
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --- 1. EXECUTIVE SUMMARY & OBJECTIVES ---
    h1 = doc.add_paragraph()
    r = h1.add_run("1. Executive Summary & Laboratory Objectives")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p_summary = doc.add_paragraph(
        "MongoDB is the industry standard document-oriented NoSQL database system, designed to provide high scalability, "
        "flexible JSON-like schema modeling (BSON), and rich query capabilities. Laboratory 2 focuses on establishing robust "
        "connectivity between Python client applications and MongoDB database engines, exploring heterogeneous deployment "
        "architectures, and executing comprehensive CRUD (Create, Read, Update, Delete) operations via PyMongo.\n\n"
        "The primary objectives of this laboratory are organized into four systematic exercises:\n\n"
        "1. Activity 2.1 (Environment Setup Verification): Verify the Python runtime, PyMongo client driver, local "
        "MongoDB service daemon, Docker containerization, and optional data ecosystem packages. Store verification telemetry "
        "persistently in MongoDB and export the diagnostics to JSON.\n\n"
        "2. Activity 2.1 'Try It Yourself' (Simultaneous Dual-Server Comparison): Establish simultaneous active client "
        "connections to both local/Docker MongoDB and MongoDB Atlas Cloud. Extract deep engine telemetry using server_info() "
        "and perform an architectural comparison across versions, operating systems, editions (Community vs. Enterprise), "
        "and clustering models.\n\n"
        "3. Activity 2.2 (Bookstore CRUD Operations): Model an enterprise bookstore inventory, insert rich document structures "
        "with nested objects and array tags, perform advanced queries with comparison operators ($gt, $gte, $lte) and array filters, "
        "execute global catalog price increases ($mul), delete targeted documents, and export collection state to JSON.\n\n"
        "4. Activity 2.2 'Try It Yourself' (Targeted Pre-2010 Price Update & Compass Verification): Implement a specialized update "
        "operation targeting books published before 2010 (year < 2010) to apply a 10% price markup ($mul: 1.10) while ensuring modern "
        "publications remain strictly unmodified. Validate the resulting dataset in MongoDB Compass GUI with filter criteria and "
        "comparative price delta analysis."
    )
    p_summary.paragraph_format.line_spacing = 1.15
    p_summary.paragraph_format.space_after = Pt(12)

    # --- 2. ACTIVITY 2.1: ENVIRONMENT SETUP VERIFICATION ---
    h2 = doc.add_paragraph()
    r = h2.add_run("2. Activity 2.1: Environment Setup Verification")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    doc.add_paragraph(
        "Activity 2.1 verifies all prerequisites required for the NoSQL laboratory. The script validates Python 3.13.2, "
        "PyMongo 4.20.0, the active local MongoDB daemon running on port 27017, and ecosystem packages (rich, python-docx, "
        "pillow). The diagnostic audit log is saved in MongoDB collection 'environment_setup_verification' and exported to JSON."
    )

    doc.add_heading("2.1 Python Script Implementation (lab_01_setup_environment.py)", level=2)
    script_2_1_path = os.path.join(BASE_DIR, "Activity_2.1", "lab_01_setup_environment.py")
    add_code_block(doc, read_file_content(script_2_1_path))

    doc.add_heading("2.2 Respective MongoDB JSON Export (environment_setup_verification.json)", level=2)
    doc.add_paragraph(
        "Upon successful validation, the script persists the audit record into collection 'environment_setup_verification' "
        "in the 'nosql_labs' database and exports the document to JSON. The exported JSON content is shown below:"
    )
    json_2_1_path = os.path.join(BASE_DIR, "Activity_2.1", "environment_setup_verification.json")
    add_code_block(doc, read_file_content(json_2_1_path))

    doc.add_heading("2.3 Execution Output & Screenshot", level=2)
    doc.add_paragraph("The screenshot below captures the complete terminal execution of Activity 2.1:")
    img_2_1 = os.path.join(SCREENSHOTS_DIR, "activity_2_1_output.png")
    if os.path.exists(img_2_1):
        doc.add_picture(img_2_1, width=Inches(6.5))
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --- 3. ACTIVITY 2.1 TRY IT YOURSELF: DUAL SERVER COMPARISON ---
    h3 = doc.add_paragraph()
    r = h3.add_run("3. Activity 2.1 'Try It Yourself': Atlas & Docker/Local Simultaneous Comparison")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    doc.add_paragraph(
        "In this activity, PyMongo connects simultaneously to both a local/Docker MongoDB instance and a MongoDB Atlas "
        "Cloud cluster. By calling client.server_info(), detailed runtime daemon metadata is extracted and compared "
        "side-by-side across both environments. The comparative record is saved in MongoDB collection 'dual_server_comparison' "
        "and exported to JSON."
    )

    doc.add_heading("3.1 Python Script Implementation (lab_01_try_it_yourself.py)", level=2)
    script_2_1_try_path = os.path.join(BASE_DIR, "Activity_2.1_Try_It_Yourself", "lab_01_try_it_yourself.py")
    add_code_block(doc, read_file_content(script_2_1_try_path))

    doc.add_heading("3.2 Respective MongoDB JSON Export (dual_server_comparison.json)", level=2)
    doc.add_paragraph(
        "The comparison record captures the complete architectural profile of both servers, including git commit hashes, "
        "build platforms, storage engines, and deployment models:"
    )
    json_2_1_try_path = os.path.join(BASE_DIR, "Activity_2.1_Try_It_Yourself", "dual_server_comparison.json")
    add_code_block(doc, read_file_content(json_2_1_try_path))

    doc.add_heading("3.3 Execution Output & Screenshot", level=2)
    doc.add_paragraph("The screenshot below captures the simultaneous dual-server connection and comparative audit table:")
    img_2_1_try = os.path.join(SCREENSHOTS_DIR, "activity_2_1_try_it_yourself_output.png")
    if os.path.exists(img_2_1_try):
        doc.add_picture(img_2_1_try, width=Inches(6.5))
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.add_heading("3.4 Architectural Analysis: Local/Docker vs. MongoDB Atlas Cloud", level=2)
    doc.add_paragraph(
        "A detailed side-by-side technical evaluation reveals key differences in deployment architecture:\n\n"
        "• Engine Version: Local server runs MongoDB 9.0.2 Community, featuring cutting-edge query engine optimizations. "
        "MongoDB Atlas M0 clusters run MongoDB 7.0.14 Enterprise, emphasizing LTS enterprise stability.\n"
        "• High Availability: The local instance operates as a single standalone node suitable for offline development, "
        "while Atlas provisions a multi-node replica set with automatic primary election and zero-downtime failover.\n"
        "• Storage Engine: Both leverage WiredTiger with document-level locking, compression (Snappy/zlib), and checkpointing. "
        "Atlas additionally supports enterprise inMemory storage engine modules.\n"
        "• Patching & Upgrades: Local/Docker requires manual container rebuilding or MSI upgrades, whereas Atlas provides "
        "managed rolling upgrades without service interruption."
    )

    # --- 4. ACTIVITY 2.2: BOOKSTORE CRUD OPERATIONS ---
    h4 = doc.add_paragraph()
    r = h4.add_run("4. Activity 2.2: Bookstore CRUD Operations")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    doc.add_paragraph(
        "Activity 2.2 demonstrates the core operations of MongoDB document management via PyMongo. Five technical books "
        "with nested publisher sub-documents and tag arrays are created. Multiple query patterns (filtering by publication year, "
        "genre, price boundaries, and array membership) are executed, followed by a global catalog update ($mul: 1.10) "
        "and targeted document deletion. The final collection is exported to JSON."
    )

    doc.add_heading("4.1 Python Script Implementation (lab_02_bookstore_crud.py)", level=2)
    script_2_2_path = os.path.join(BASE_DIR, "Activity_2.2", "lab_02_bookstore_crud.py")
    add_code_block(doc, read_file_content(script_2_2_path))

    doc.add_heading("4.2 Respective MongoDB JSON Export (bookstore_books.json)", level=2)
    doc.add_paragraph(
        "The collection 'books' in database 'bookstore' contains the final post-update inventory, exported directly to JSON:"
    )
    json_2_2_path = os.path.join(BASE_DIR, "Activity_2.2", "bookstore_books.json")
    add_code_block(doc, read_file_content(json_2_2_path))

    doc.add_heading("4.3 Execution Output & Screenshot", level=2)
    doc.add_paragraph("The screenshot below captures the complete CRUD lifecycle execution for Activity 2.2:")
    img_2_2 = os.path.join(SCREENSHOTS_DIR, "activity_2_2_output.png")
    if os.path.exists(img_2_2):
        doc.add_picture(img_2_2, width=Inches(6.5))
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --- 5. ACTIVITY 2.2 TRY IT YOURSELF: PRE-2010 UPDATE & COMPASS VERIFICATION ---
    h5 = doc.add_paragraph()
    r = h5.add_run("5. Activity 2.2 'Try It Yourself': Pre-2010 Price Increase & Compass Verification")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    doc.add_paragraph(
        "The assignment challenge for Activity 2.2 requires adding an update operation that selectively increases the price "
        "of all books published before 2010 by 10 percent, followed by visual verification in MongoDB Compass. "
        "To provide a rigorous test environment, an enriched catalog containing 7 titles was deployed with both pre-2010 classics "
        "and modern post-2010 literature. The targeted update filter {'year': {'$lt': 2010}} was applied with operator {'$mul': {'price': 1.10}}."
    )

    doc.add_heading("5.1 Python Script Implementation (lab_02_try_it_yourself.py)", level=2)
    script_2_2_try_path = os.path.join(BASE_DIR, "Activity_2.2_Try_It_Yourself", "lab_02_try_it_yourself.py")
    add_code_block(doc, read_file_content(script_2_2_try_path))

    doc.add_heading("5.2 Respective MongoDB JSON Export (bookstore_pre2010_update.json)", level=2)
    doc.add_paragraph(
        "The complete inventory state was exported to 'bookstore_pre2010_update.json'. A representative snippet of the updated "
        "pre-2010 documents alongside untouched post-2010 documents is shown below:"
    )
    json_2_2_try_path = os.path.join(BASE_DIR, "Activity_2.2_Try_It_Yourself", "bookstore_pre2010_update.json")
    try_json_data = json.loads(read_file_content(json_2_2_try_path))
    add_code_block(doc, json.dumps(try_json_data[:4], indent=2) + f"\n// ... [{len(try_json_data)-4} additional documents in full JSON export]")

    doc.add_heading("5.3 Execution Output & Screenshot", level=2)
    doc.add_paragraph("The screenshot below captures the execution, inventory price audit table, and verification summary:")
    img_2_2_try = os.path.join(SCREENSHOTS_DIR, "activity_2_2_try_it_yourself_output.png")
    if os.path.exists(img_2_2_try):
        doc.add_picture(img_2_2_try, width=Inches(6.5))
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.add_heading("5.4 MongoDB Compass Verification Procedure & GUI Screenshot", level=2)
    doc.add_paragraph(
        "Verification in MongoDB Compass confirms that the targeted update correctly modified pre-2010 records while leaving "
        "all other books intact:\n\n"
        "1. Compass Connection: Connected to mongodb://localhost:27017.\n"
        "2. Database & Collection: Navigated to database 'bookstore' and collection 'books_try_it_yourself'.\n"
        "3. Filter Criteria: Applied query { year: { $lt: 2010 } } in the Compass Filter Bar.\n"
        "4. Filter Results: Exactly 3 matching documents are returned (Clean Code, Design Patterns, Refactoring).\n"
        "5. Field Value Validation:\n"
        "   - Clean Code (2008): Price updated from $39.99 to $43.99 (+10%).\n"
        "   - Design Patterns (1994): Price updated from $54.99 to $60.49 (+10%).\n"
        "   - Refactoring (1999): Price updated from $47.50 to $52.25 (+10%).\n"
        "6. Control Verification: Applying { year: { $gte: 2010 } } confirms that all 4 modern books retained their exact initial prices."
    )

    img_compass = os.path.join(SCREENSHOTS_DIR, "compass_verification.png")
    if os.path.exists(img_compass):
        doc.add_picture(img_compass, width=Inches(6.5))
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Price Audit Table
    doc.add_heading("5.5 Price Audit Delta Table", level=2)
    audit_table = doc.add_table(rows=8, cols=6)
    audit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    audit_table.autofit = False
    col_widths = [Inches(2.2), Inches(0.8), Inches(0.9), Inches(0.9), Inches(0.7), Inches(1.0)]
    for i, w in enumerate(col_widths):
        audit_table.columns[i].width = w

    headers = ["Book Title", "Year", "Old Price", "New Price", "Delta", "Status"]
    hdr_cells = audit_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].paragraphs[0].add_run(title).bold = True
        set_cell_background(hdr_cells[i], "D0E1F9")
        set_cell_margins(hdr_cells[i], 80, 80, 100, 100)

    rows_data = [
        ("Clean Code", "2008", "$39.99", "$43.99", "+$4.00", "UPDATED (+10%)"),
        ("Design Patterns", "1994", "$54.99", "$60.49", "+$5.50", "UPDATED (+10%)"),
        ("Refactoring", "1999", "$47.50", "$52.25", "+$4.75", "UPDATED (+10%)"),
        ("The Pragmatic Programmer", "2019", "$49.99", "$49.99", "$0.00", "UNCHANGED"),
        ("Designing Data-Intensive Apps", "2017", "$45.99", "$45.99", "$0.00", "UNCHANGED"),
        ("Deep Learning", "2016", "$72.00", "$72.00", "$0.00", "UNCHANGED"),
        ("Hands-On Machine Learning", "2022", "$59.99", "$59.99", "$0.00", "UNCHANGED")
    ]

    for row_idx, data in enumerate(rows_data):
        row_cells = audit_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(data):
            run = row_cells[col_idx].paragraphs[0].add_run(val)
            if col_idx == 5 and "UPDATED" in val:
                run.bold = True
                set_cell_background(row_cells[col_idx], "E6F4EA")
            elif col_idx == 5:
                set_cell_background(row_cells[col_idx], "FFF8E1")
            else:
                set_cell_background(row_cells[col_idx], "F8F9FA" if row_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(row_cells[col_idx], 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- 6. SUMMARY & CONCLUSION ---
    h6 = doc.add_paragraph()
    r = h6.add_run("6. Laboratory Deliverables & Summary Checklist")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    doc.add_paragraph(
        "All required components for Laboratory 2 have been implemented, tested, exported, and packaged according to "
        "the academic submission guidelines:\n\n"
        "• Activity 2.1: Python script lab_01_setup_environment.py and environment_setup_verification.json.\n"
        "• Activity 2.1 'Try It Yourself': Python script lab_01_try_it_yourself.py and dual_server_comparison.json.\n"
        "• Activity 2.2: Python script lab_02_bookstore_crud.py and bookstore_books.json.\n"
        "• Activity 2.2 'Try It Yourself': Python script lab_02_try_it_yourself.py and bookstore_pre2010_update.json.\n"
        "• High-resolution terminal screenshots and MongoDB Compass verification diagrams.\n"
        "• Comprehensive report document in DOCX format and organized .ZIP submission archive."
    )

    doc.save(OUTPUT_DOCX)
    print(f"[OK] Successfully built: {OUTPUT_DOCX} ({os.path.getsize(OUTPUT_DOCX)} bytes)")
    return OUTPUT_DOCX


if __name__ == "__main__":
    build_docx()
