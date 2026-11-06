import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_pdf():
    pdf_path = r"C:\Users\27730\.gemini\antigravity-ide\scratch\solutions-engineer-portfolio\MAGWADI_ADELAIDE_PALANE_CV.pdf"
    
    # Precise margins (28 pt / ~0.38 in) to ensure a flawless single-page layout
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette: Professional Navy & Charcoal
    PRIMARY = colors.HexColor("#0f2a4a")   # Deep Corporate Navy
    SECONDARY = colors.HexColor("#1b4d89") # Accent Blue
    TEXT_COLOR = colors.HexColor("#1e293b")# Dark Slate Body
    MUTED = colors.HexColor("#475569")     # Subtext Muted Slate
    LINE_COLOR = colors.HexColor("#0f2a4a")
    BORDER_LIGHT = colors.HexColor("#cbd5e1")
    
    # Typography Styles
    name_style = ParagraphStyle(
        'DocName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16.5,
        leading=19,
        textColor=PRIMARY,
        alignment=1 # Center
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=MUTED,
        alignment=1 # Center
    )
    
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=11.5,
        textColor=PRIMARY,
        spaceAfter=2,
        spaceBefore=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.4,
        textColor=TEXT_COLOR
    )
    
    bold_style = ParagraphStyle(
        'DocBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.4,
        textColor=TEXT_COLOR
    )
    
    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=PRIMARY
    )
    
    job_meta_style = ParagraphStyle(
        'JobMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=SECONDARY,
        alignment=2 # Right
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.8,
        textColor=TEXT_COLOR,
        leftIndent=10,
        firstLineIndent=-7
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("MAGWADI ADELAIDE PALANE", name_style))
    story.append(Spacer(1, 2))
    
    contact_line = (
        "Tzaneen, Limpopo, South Africa &bull; +27 78 632 5143 &bull; "
        "<a href='mailto:magwadiadelaide28@gmail.com' color='#1b4d89'>magwadiadelaide28@gmail.com</a> &bull; "
        "<a href='https://www.linkedin.com/in/magwadi-palane-0bb553431/' color='#1b4d89'>LinkedIn Profile</a> &bull; "
        "<a href='https://github.com/Adelaide2828/solutions-engineer-portfolio' color='#1b4d89'>GitHub Portfolio</a>"
    )
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.2, color=LINE_COLOR, spaceBefore=1, spaceAfter=3))
    
    # 2. Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    summary_text = (
        "Results-driven <b>Information and Communication Technology (BICT) Graduate</b> with practical experience "
        "in solutions engineering, data modeling, API validation pipelines, and business intelligence reporting. "
        "Proven track record in orchestrating event-driven webhook oracles, querying GraphQL endpoints, enforcing strict "
        "data integrity (SQL/JSON Schema), and translating complex datasets into actionable stakeholder dashboards. "
        "Combines solid academic foundations in Data Scalability, Analytics, and Database Systems with hands-on enterprise "
        "integration skills and POPIA compliance awareness to deliver reliable technical solutions."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_LIGHT, spaceBefore=2, spaceAfter=3))
    
    # 3. Core Competencies & Technical Toolkit
    story.append(Paragraph("CORE COMPETENCIES & TECHNICAL TOOLKIT", section_style))
    competencies = [
        ("Solutions Engineering & Integrations:", "REST APIs, Webhooks, GraphQL (Blocksync), JSON Schema (Draft-07), Workflow Automation (Make.com, Zapier), Data Mapping."),
        ("Data Analytics & BI:", "SQL (PostgreSQL, Supabase), Advanced Excel (Power Query, PivotTables, Formulas), Power BI, Python, Data Cleaning & Scalability."),
        ("Enterprise Systems & Modeling:", "CRM Data Modeling, Record-Triggered Flows, SLA Monitoring, Human-in-the-Loop (HITL) Exception Handling, Airtable Relational Bases."),
        ("Governance & Compliance:", "POPIA Guidelines, Data Confidentiality, KYC Verification Support, Verifiable Claim Provenance.")
    ]
    for category, skills in competencies:
        line = f"&bull; <b>{category}</b> {skills}"
        story.append(Paragraph(line, bullet_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_LIGHT, spaceBefore=2, spaceAfter=3))
    
    # 4. Technical Projects & Portfolio
    story.append(Paragraph("TECHNICAL PROJECTS & PORTFOLIO", section_style))
    portfolio_meta = Table([
        [Paragraph("<b>Technical Solutions & Platform Engineering Portfolio</b>", job_title_style),
         Paragraph("<a href='https://github.com/Adelaide2828/solutions-engineer-portfolio' color='#1b4d89'>github.com/Adelaide2828/solutions-engineer-portfolio</a>", job_meta_style)]
    ], colWidths=[330, 222])
    portfolio_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(portfolio_meta)
    
    # Project 1
    story.append(Paragraph("<b>Event-Driven Webhook Validation Oracle & Data Firewall</b> <i>(Make.com, Supabase SQL, Airtable, Postman)</i>", bold_style))
    story.append(Paragraph("&bull; Architected an event-driven validation pipeline inspecting 100% of incoming payloads against strict JSON Schema contracts before database ingestion.", bullet_style))
    story.append(Paragraph("&bull; Configured conditional routing logic quarantining anomalous records (HTTP 422), dispatching real-time alerts to ops, and committing clean records (HTTP 200).", bullet_style))
    story.append(Paragraph("&bull; Authored automated Postman API test collections to perform regression testing across multi-scenario payloads.", bullet_style))
    story.append(Spacer(1, 1.5))
    
    # Project 2
    story.append(Paragraph("<b>Decentralized Provenance & Analytical Dashboard</b> <i>(NumiKnow / IXO Protocol, GraphQL, Modern UI)</i>", bold_style))
    story.append(Paragraph("&bull; Engineered an interactive web analytics dashboard querying Blocksync GraphQL to track verified educational outcomes across 5 regional school domains.", bullet_style))
    story.append(Paragraph("&bull; Established a 4-Tier Data Trust Framework (Cryptographic Proofs, Device Telemetry, Curated Datasets, Assertions), reducing audit cycles from 3 weeks to real-time.", bullet_style))
    story.append(Spacer(1, 1.5))

    # Project 3
    story.append(Paragraph("<b>Agentic Verification Oracle & Human-in-the-Loop Governance</b> <i>(Python, Policy Manifests, Cosmos Authz)</i>", bold_style))
    story.append(Paragraph("&bull; Implemented a deterministic verification engine enforcing declarative Policy Manifest Rubrics across facilitator credentials, geofenced GPS, and score outliers.", bullet_style))
    story.append(Paragraph("&bull; Automated 85% of standard grant claim verifications with sub-second execution while systematically escalating complex edge cases to human auditors.", bullet_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_LIGHT, spaceBefore=2, spaceAfter=3))
    
    # 5. Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
    
    # Role 1
    exp1_meta = Table([
        [Paragraph("<b>IXO Solutions Engineering Cohort Programme</b> &mdash; <i>Solutions Engineer Trainee</i>", job_title_style),
         Paragraph("2025 &ndash; 2026", job_meta_style)]
    ], colWidths=[390, 162])
    exp1_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(exp1_meta)
    story.append(Paragraph("&bull; Supported project partners in translating operational and grant funding requirements into technical integration blueprints and POD system definitions.", bullet_style))
    story.append(Paragraph("&bull; Monitored real-time submission pipelines across pending, approved, and rejected states using GraphQL queries and event logs.", bullet_style))
    story.append(Paragraph("&bull; Assisted participants and partner organizations in completing KYC verification workflows adhering to strict data verification protocols.", bullet_style))
    story.append(Paragraph("&bull; Collaborated across technical cohort pods to troubleshoot validation bottlenecks and optimize claim processing turnaround.", bullet_style))
    story.append(Spacer(1, 2.5))
    
    # Role 2
    exp2_meta = Table([
        [Paragraph("<b>Community Educational Initiative | Youth Development Project</b> &mdash; <i>Data Administrator & Project Coordinator</i>", job_title_style),
         Paragraph("Jan 2026 &ndash; Jul 2026", job_meta_style)]
    ], colWidths=[410, 142])
    exp2_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(exp2_meta)
    story.append(Paragraph("&bull; Administered educational datasets tracking 100+ Grade 6&ndash;7 learners' attendance, test metrics, and performance progressions across Hoedspruit Hub initiatives.", bullet_style))
    story.append(Paragraph("&bull; Cleaned, transformed, and standardized messy field spreadsheets using Advanced Excel and Power Query, removing duplicates and correcting formatting inconsistencies.", bullet_style))
    story.append(Paragraph("&bull; Maintained strict POPIA compliance by implementing anonymization and data masking protocols on all student and facilitator identifying records.", bullet_style))
    story.append(Paragraph("&bull; Prepared weekly and monthly analytical reports with visual charts for program managers, identifying trends in student numeracy improvement.", bullet_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_LIGHT, spaceBefore=2, spaceAfter=3))
    
    # 6. Education
    story.append(Paragraph("EDUCATION", section_style))
    edu_meta = Table([
        [Paragraph("<b>Bachelor of Information and Communication Technology (BICT)</b> &mdash; <i>NQF Level 7</i>", job_title_style),
         Paragraph("Conferred May 2025", job_meta_style)]
    ], colWidths=[390, 162])
    edu_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(edu_meta)
    story.append(Paragraph("<i>University of Mpumalanga</i> | Completed: December 2024", body_style))
    story.append(Paragraph("&bull; <b>Data Analytics & Statistics:</b> Data Analytics 321, Data Scalability & Analytics 202, Statistics for ICT 201, Mathematics for Computing.", bullet_style))
    story.append(Paragraph("&bull; <b>Databases & Architecture:</b> Database Systems 201, Introduction to Databases 101, Data Structures & Algorithms 202.", bullet_style))
    story.append(Paragraph("&bull; <b>Software & Systems:</b> System Development Project 300, Principles of Software Engineering 201, Programming Techniques (I, II, III), Web Development.", bullet_style))
    story.append(Paragraph("&bull; <b>Infrastructure & Networks:</b> Introduction to IoT 202, Communication Networks (101, 102, 322), Cybersecurity (202, 312), Operating Systems.", bullet_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_LIGHT, spaceBefore=2, spaceAfter=3))

    # 7. Certificates, Recognition & Languages
    story.append(Paragraph("CERTIFICATES, RECOGNITION & LANGUAGES", section_style))
    story.append(Paragraph("&bull; <b>Certificate of Appreciation &ndash; Program Management:</b> Hoedspruit Hub (Awarded for outstanding operational management and data tracking of Grade 7 Enrichment Program) | <i>Sept 2026</i>", bullet_style))
    story.append(Paragraph("&bull; <b>Languages:</b> English (Professional Working Proficiency / Fluent), Sepedi (Native / Fluent), Zulu (Conversational).", bullet_style))
    
    doc.build(story)
    print(f"SUCCESS: Compact 1-Page PDF generated at {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
