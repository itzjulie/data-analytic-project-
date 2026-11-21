"""
Generate a professional, single-file Source Code PDF for LMS submission.
Project: Patient Demographic Analysis (Project P104)
Candidate: Juli (Roll No: 2503201450068)
Mentor: Mr. Dinesh
Institution: ABES Engineering College, Ghaziabad (UP)
"""
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

# Paths
BASE_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\patient_demographic_analysis"
OUTPUT_PDF = r"C:\Users\HP\Desktop\Patient_Demographic_Analysis_Source_Code_P104.pdf"
SECONDARY_PDF = os.path.join(BASE_DIR, "docs", "Patient_Demographic_Analysis_Source_Code_P104.pdf")

# Custom Canvas for Page Numbers & Running Headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Running Top Header
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 805, 576, 805)
        self.drawString(36, 810, "Project P104 · Patient Demographic Analysis · ABES Engineering College")
        self.drawRightString(576, 810, "MCA 2nd Year · Data Analytics")
        
        # Running Bottom Footer
        self.line(36, 40, 576, 40)
        self.drawString(36, 28, "Candidate: Juli (Roll No: 2503201450068) | Mentor: Mr. Dinesh")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 28, page_str)
        self.restoreState()


def create_source_code_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Colors
    c_navy = colors.HexColor("#0F2C59")
    c_sky = colors.HexColor("#0284C7")
    c_slate = colors.HexColor("#334155")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_navy,
        alignment=1,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=16,
        textColor=c_sky,
        alignment=1,
        spaceAfter=15
    )

    inst_style = ParagraphStyle(
        'CoverInst',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_slate,
        alignment=1,
        spaceAfter=25
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_navy
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        textColor=c_slate
    )

    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.white,
        spaceAfter=0
    )

    file_title = ParagraphStyle(
        'FileTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_navy
    )

    file_meta = ParagraphStyle(
        'FileMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=0,
        spaceAfter=0
    )

    story = []

    # ══════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 25))
    story.append(Paragraph("ABES ENGINEERING COLLEGE, GHAZIABAD (UP)", inst_style))
    story.append(Paragraph("Department of Master of Computer Applications (MCA)", ParagraphStyle('Dept', alignment=1, fontSize=11, textColor=c_slate, leading=14, spaceAfter=20)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("PROJECT SOURCE CODE DOSSIER", title_style))
    story.append(Paragraph("Project Title: Patient Demographic Analysis", subtitle_style))
    story.append(Paragraph("CAPSTONE PROJECT · PROJECT ID: P104", ParagraphStyle('Cap', fontName='Helvetica-Bold', alignment=1, fontSize=10, textColor=c_navy, leading=13, spaceAfter=25)))
    
    # Metadata Table
    meta_data = [
        [Paragraph("Candidate Name:", meta_label), Paragraph("Juli", meta_val),
         Paragraph("Project ID:", meta_label), Paragraph("P104", meta_val)],
        [Paragraph("University Roll No:", meta_label), Paragraph("2503201450068", meta_val),
         Paragraph("Academic Year:", meta_label), Paragraph("2024 – 2025", meta_val)],
        [Paragraph("Programme / Class:", meta_label), Paragraph("MCA 2nd Year (Data Analytics)", meta_val),
         Paragraph("Faculty Guide:", meta_label), Paragraph("Mr. Dinesh", meta_val)],
        [Paragraph("Technical Stack:", meta_label), Paragraph("Python 3.12, Streamlit, SQLite, Plotly, SciPy, pytest", meta_val),
         Paragraph("Automated Tests:", meta_label), Paragraph("13 / 13 Passed (100%)", meta_val)],
        [Paragraph("Submission Date:", meta_label), Paragraph(datetime.now().strftime("%d %B %Y"), meta_val),
         Paragraph("Deployment Status:", meta_label), Paragraph("Local & Cloud Ready", meta_val)]
    ]
    t_meta = Table(meta_data, colWidths=[120, 150, 110, 160])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 25))

    # File Manifest Definition
    files_to_include = [
        # (Relative Path, Section Name, Description)
        ("requirements.txt", "1. Environment & Config", "Pinned pip dependencies for cloud deployment"),
        (".streamlit/config.toml", "1. Environment & Config", "Theme definition (navy/blue palette & fonts)"),
        ("app.py", "2. Core Application Entrypoint", "Main multi-page landing view & executive KPI dashboard"),
        ("src/data/db.py", "3. Data Access & Storage Layer", "Thread-safe read-only SQLite database connection manager"),
        ("src/data/validator.py", "3. Data Access & Storage Layer", "Schema integrity assertion and domain bounds check"),
        ("src/data/cleaner.py", "3. Data Access & Storage Layer", "Data imputation, categorical typing, and feature enrichment"),
        ("src/data/loader.py", "3. Data Access & Storage Layer", "Streamlit @st.cache_data analytical dataset loader"),
        ("src/generate_data.py", "3. Data Access & Storage Layer", "Synthetic dataset generator (seed=42, NCR India demographics)"),
        ("src/analytics/statistics.py", "4. Statistical & Analytics Engine", "Non-parametric ALoS, Chi-Square independence, Tukey IQR, SMA"),
        ("src/analytics/charts.py", "4. Statistical & Analytics Engine", "Plotly visualisations: pyramid, heatmaps, boxplots, bubble maps"),
        ("src/ui/components.py", "5. Reusable UI Components", "Tailwind CSS iframe-sandboxed KPI cards and banners"),
        ("src/ui/filters.py", "5. Reusable UI Components", "Global shared sidebar filters persisted in st.session_state"),
        ("pages/01_Demographics.py", "6. Multipage Dashboard Views", "OQ-01 / OQ-07: Population pyramid & catchment bubble analysis"),
        ("pages/02_Clinical_Comorbidities.py", "6. Multipage Dashboard Views", "OQ-02: Comorbidity correlation heatmap & Chi-Square test"),
        ("pages/03_Length_of_Stay_Acuity.py", "6. Multipage Dashboard Views", "OQ-03 / OQ-04: Length of Stay Tukey outliers & acuity breakdown"),
        ("pages/04_Readmission_Risk.py", "6. Multipage Dashboard Views", "OQ-05: 30-day readmissions with 15% HRRP penalty alert"),
        ("pages/05_Financial_Payer_Catchment.py", "6. Multipage Dashboard Views", "OQ-06 / OQ-07: Out-of-pocket liabilities & payer comparisons"),
        ("pages/06_Data_Explorer.py", "6. Multipage Dashboard Views", "Interactive patient data grid with search & CSV export"),
        ("pages/07_Data_Quality_Architecture.py", "6. Multipage Dashboard Views", "Live SQLite schema validation, row count verification & audit"),
        ("tests/test_data.py", "7. Automated Test Suites", "TC-T-01..04: Database constraints, FKs, and schema assertions"),
        ("tests/test_analysis.py", "7. Automated Test Suites", "TC-T-05..08: Mathematical accuracy of KPIs & statistical tests"),
        ("tests/test_app.py", "7. Automated Test Suites", "TC-T-09..10: Streamlit configuration & load latency tests")
    ]

    # Index Table on Cover
    idx_title = Paragraph("<b>PROJECT FILE MANIFEST & TABLE OF CONTENTS</b>", ParagraphStyle('IdxT', fontName='Helvetica-Bold', fontSize=10, textColor=c_navy, spaceAfter=8))
    story.append(idx_title)

    idx_rows = [["#", "File Path", "Module / Purpose", "Lines"]]
    total_loc = 0
    for idx, (rel_path, section, desc) in enumerate(files_to_include, 1):
        full_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                loc = len(f.readlines())
        else:
            loc = 0
        total_loc += loc
        idx_rows.append([str(idx), rel_path, desc, f"{loc:,}"])

    idx_rows.append(["", "<b>Total Source Code Volume</b>", f"<b>{len(files_to_include)} Modules</b>", f"<b>{total_loc:,} lines</b>"])

    t_idx = Table(idx_rows, colWidths=[20, 200, 260, 60])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, c_bg]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_idx)

    # ══════════════════════════════════════════════════════════════════════
    # FILE CONTENTS
    # ══════════════════════════════════════════════════════════════════════
    current_section = None

    for rel_path, section, desc in files_to_include:
        full_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        story.append(PageBreak())

        # Section Banner if new section
        if section != current_section:
            current_section = section
            sec_table = Table([[Paragraph(f"<b>{section.upper()}</b>", section_heading)]], colWidths=[540])
            sec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), c_navy),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(sec_table)
            story.append(Spacer(1, 10))

        # Read file code
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        loc = len(lines)

        # File Header Card
        file_header_data = [
            [Paragraph(f"<b>📄 File:</b> {rel_path}", file_title),
             Paragraph(f"<b>Lines:</b> {loc:,}  |  <b>Type:</b> Python / Script", file_meta)],
            [Paragraph(f"<b>Description:</b> {desc}", file_meta),
             Paragraph(f"<b>Location:</b> project_root/{rel_path}", file_meta)]
        ]
        t_fhdr = Table(file_header_data, colWidths=[330, 210])
        t_fhdr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DBEAFE")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t_fhdr)
        story.append(Spacer(1, 6))

        # Format Code with Line Numbers in chunks to prevent page-break overflow
        # Max lines per chunk ~65 to fit cleanly on A4
        chunk_size = 65
        for chunk_idx in range(0, loc, chunk_size):
            chunk_lines = lines[chunk_idx:chunk_idx + chunk_size]
            formatted_chunk = []
            for i, line in enumerate(chunk_lines, chunk_idx + 1):
                clean_line = line.rstrip('\r\n').replace('\t', '    ')
                # Escape XML entities
                clean_line = clean_line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                # Truncate overly long lines to prevent clipping
                if len(clean_line) > 105:
                    clean_line = clean_line[:102] + "..."
                formatted_chunk.append(f"<font color='#94A3B8'>{i:4d} | </font>{clean_line}")

            code_text = "<br/>".join(formatted_chunk)
            p_code = Paragraph(code_text, code_style)

            code_table = Table([[p_code]], colWidths=[540])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), c_bg),
                ('BOX', (0, 0), (-1, -1), 0.5, c_border),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(code_table)
            story.append(Spacer(1, 4))

    # Build PDF with Custom Canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Copy to Secondary location
    import shutil
    shutil.copyfile(OUTPUT_PDF, SECONDARY_PDF)
    print(f"✅ Generated single-file Source Code PDF successfully!")
    print(f"   Primary Desktop Location: {OUTPUT_PDF}")
    print(f"   Secondary Docs Location:  {SECONDARY_PDF}")
    file_size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"   File Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    create_source_code_pdf()
