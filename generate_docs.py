"""
generate_docs.py - Generates the Comprehensive Viva PDF Guide using ReportLab.
Covers:
- Project Overview & Architecture
- All Agents and Tools
- Endpoints, API Keys & Zero-Cost Setup
- Multi-Agent Terminology & Concepts (in simple English)
- Likely Viva Questions & Ready Answers
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def build_pdf(filename="VIVA_PREPARATION_GUIDE.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#B91C1C'),
        spaceBefore=5,
        spaceAfter=2
    )
    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )

    elements = []

    # Title & Subtitle
    elements.append(Paragraph("CSE476: AGENTIC AI & INTELLIGENT AUTOMATION", title_style))
    elements.append(Paragraph("CA2 Project Q14: Automated Code Review Board — Complete Viva Guide & Technical Reference", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=12))

    # Section 1: Executive Summary
    elements.append(Paragraph("1. Project Overview & Architecture", h1_style))
    summary_text = (
        "<b>Project Title:</b> Automated Code Review Board (Group 14)<br/>"
        "<b>Core Objective:</b> Automate pull request code reviews by fanning out specialized audits concurrently "
        "(Style, Security, Test Coverage) and fanning findings back into a Reviewer Manager that enforces enterprise gate policies "
        "and deduplicates/ranks issues by severity. A 6th agent (Fix-Suggestion Agent) synthesizes unified git replacement patches."
    )
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 6))

    # Architecture Table
    arch_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Design Details</b>", body_bold)],
        [Paragraph("<b>Coordination Architecture</b>", body_style), Paragraph("<b>Fan-Out / Fan-In with Reviewer Manager</b> (Parallel execution followed by structured aggregation).", body_style)],
        [Paragraph("<b>Framework</b>", body_style), Paragraph("<b>Microsoft Semantic Kernel (Python SDK)</b>. Modular agent design with separate module per agent.", body_style)],
        [Paragraph("<b>Shared State</b>", body_style), Paragraph("<code>ChangeState</code> object containing git diff, touched files, parsed AST components, findings list, severity rankings, and full execution trace.", body_style)],
        [Paragraph("<b>Concurreny Model</b>", body_style), Paragraph("Python <code>ThreadPoolExecutor</code> fanning out to Style, Security, and Test-Coverage agents simultaneously.", body_style)],
        [Paragraph("<b>Enterprise Gate Policy</b>", body_style), Paragraph("<b>REQUEST_CHANGES</b> if CRITICAL or HIGH findings exist; <b>APPROVE</b> with advisory if only MEDIUM/LOW exist; <b>APPROVE</b> cleanly if 0 issues.", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[150, 380])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_arch)
    elements.append(Spacer(1, 10))

    # Section 2: Agent Roster & Real Tools
    elements.append(Paragraph("2. Agent Roster & Mandatory Tools (2 Plain Python Tools Per Agent)", h1_style))
    agent_data = [
        [Paragraph("<b>Agent Name</b>", body_bold), Paragraph("<b>Role Description</b>", body_bold), Paragraph("<b>Mandatory Tools (Plain Python Functions)</b>", body_bold)],
        [
            Paragraph("<b>1. Diff Agent</b><br/>(diff_agent.py)", body_style),
            Paragraph("Ingests incoming pull request and extracts structural code modifications.", body_style),
            Paragraph("1. <code>parse_git_diff()</code>: Parses added/removed lines.<br/>2. <code>extract_touched_components()</code>: AST parsing to identify modified functions and classes.", body_style)
        ],
        [
            Paragraph("<b>2. Style Agent</b><br/>(style_agent.py)", body_style),
            Paragraph("Inspects readability, naming standards, and clean code hygiene.", body_style),
            Paragraph("1. <code>inspect_naming_conventions()</code>: Checks PEP8 snake_case vs camelCase.<br/>2. <code>check_formatting_and_comments()</code>: Flags >100 char lines and raw <code>print()</code> calls.", body_style)
        ],
        [
            Paragraph("<b>3. Security Agent</b><br/>(security_agent.py)", body_style),
            Paragraph("Audits code for vulnerabilities, injected attacks, and leaked credentials.", body_style),
            Paragraph("1. <code>scan_hardcoded_secrets()</code>: Regex audit for AWS keys, PATs, API keys.<br/>2. <code>scan_vulnerable_execution_patterns()</code>: Flags <code>eval()</code>, SQL injection, <code>shell=True</code>.", body_style)
        ],
        [
            Paragraph("<b>4. Test-Coverage Agent</b><br/>(test_coverage_agent.py)", body_style),
            Paragraph("Checks whether modifications include unit tests and assertion density.", body_style),
            Paragraph("1. <code>verify_test_file_pairing()</code>: Checks if source change has matching test file.<br/>2. <code>inspect_assertion_quality()</code>: Verifies test functions contain valid assertions.", body_style)
        ],
        [
            Paragraph("<b>5. Reviewer Manager</b><br/>(reviewer_manager.py)", body_style),
            Paragraph("Fans in specialist reports, deduplicates findings, and delivers final verdict.", body_style),
            Paragraph("1. <code>deduplicate_and_rank_findings()</code>: Sorts by CRITICAL > HIGH > MEDIUM > LOW.<br/>2. <code>evaluate_merge_policy()</code>: Applies enterprise approval/rejection gates.", body_style)
        ],
        [
            Paragraph("<b>6. Fix-Suggestion Agent</b><br/>(fix_suggestion_agent.py)<br/><i>[Group of 3 Extension]</i>", body_style),
            Paragraph("Proposes a concrete patch for the single highest-severity finding.", body_style),
            Paragraph("1. <code>extract_top_finding()</code>: Retrieves highest-priority issue from board.<br/>2. <code>synthesize_patch()</code>: Emits unified git replacement diff (e.g., env var for API key).", body_style)
        ]
    ]
    t_agent = Table(agent_data, colWidths=[120, 150, 260])
    t_agent.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_agent)
    elements.append(Spacer(1, 10))

    # Section 3: Endpoints, API Keys & Cost Architecture
    elements.append(Paragraph("3. Endpoints, API Keys & Zero-Cost Architecture Explained", h1_style))
    api_explanation = (
        "<b>Do we need paid API keys?</b><br/>"
        "No! Semantic Kernel is an orchestration framework. In enterprise systems, it can connect to Azure OpenAI "
        "(<code>https://&lt;resource&gt;.openai.azure.com/</code>) or OpenAI (<code>https://api.openai.com/v1</code>) using an <code>OPENAI_API_KEY</code>. "
        "However, our system is architected to be <b>deterministic, resilient, and zero-cost</b>. All specialist tools are implemented as pure "
        "Python functions and AST analysis. This means:<br/>"
        "• <b>100% Reliability:</b> Never suffers from API quota limits (429 Too Many Requests), network latency, or unexpected billing.<br/>"
        "• <b>Viva Defense:</b> You can state: <i>'We initialized Microsoft Semantic Kernel as the central orchestration bus. For tool execution and static code inspection, deterministic tools prevent LLM hallucination and ensure 0ms latency with complete offline capability.'</i>"
    )
    elements.append(Paragraph(api_explanation, body_style))
    elements.append(Spacer(1, 10))

    # Section 4: Terminology & Trilogy (In Simple English)
    elements.append(Paragraph("4. Key Terminology & Concepts (Trilogy in Simple English)", h1_style))
    glossary = [
        ("Agentic AI", "An AI system that doesn't just answer questions, but autonomously makes decisions, uses tools, coordinates with other agents, and works toward a goal."),
        ("Multi-Agent System (MAS)", "A setup where multiple specialized software programs ('agents') collaborate together to solve a complex workflow rather than doing everything in one giant script."),
        ("Fan-Out / Fan-In", "A parallel design pattern. 'Fan-out' means taking one input and sending it to multiple agents to inspect simultaneously. 'Fan-in' means gathering all their reports back into one manager."),
        ("Shared State Object", "A shared memory blackboard (in our code, `ChangeState`) that travels between agents. Each agent reads what was previously found and adds its own findings to it."),
        ("Semantic Kernel", "Microsoft's open-source framework designed to connect AI models, plugins, agents, and native Python tools into structured pipelines."),
        ("AST (Abstract Syntax Tree)", "Python's built-in way to turn source code into a tree of language components (classes, functions, variables) so an agent can analyze code structure without executing it."),
        ("Deterministic Tool", "A traditional Python function with 100% predictable, mathematical logic (like regex matching or AST parsing), ensuring zero hallucination."),
        ("Gate Policy / Policy Engine", "A strict set of corporate rules that decides whether a code change is permitted to merge into production (e.g., blocking if any critical vulnerability is found).")
    ]
    for term, definition in glossary:
        elements.append(Paragraph(f"• <b>{term}:</b> {definition}", body_style))
    elements.append(Spacer(1, 10))

    # Section 5: Top Viva Questions & Answers
    elements.append(Paragraph("5. Top Viva Questions & Answers (Guaranteed Marks)", h1_style))
    viva_qa = [
        (
            "Q1: Why did you choose the Fan-Out / Fan-In architecture instead of a Sequential Pipeline?",
            "Answer: Code review checks (style, security, and unit tests) are independent of each other. Running them in a sequential pipeline would needlessly slow down review time. With Fan-Out, all three specialists run concurrently using thread pooling. The Fan-In phase then brings all findings to the Reviewer Manager to deduplicate and evaluate the merge gate."
        ),
        (
            "Q2: How did you ensure every agent has two real tools as required by the rubric?",
            "Answer: Each agent has two dedicated Python functions in `tools.py`. For example, the Security Agent has `scan_hardcoded_secrets()` and `scan_vulnerable_execution_patterns()`. The Diff Agent has `parse_git_diff()` and `extract_touched_components()`. Every tool is a distinct, tested function."
        ),
        (
            "Q3: What failure scenario is handled gracefully by your system?",
            "Answer: If the developer submits a code snippet with broken or incomplete syntax, Python AST parsing would normally throw a SyntaxError and crash. Our system catches that exception and automatically falls back to regex pattern scanning, logging an advisory rather than terminating the pipeline."
        ),
        (
            "Q4: What is the role of the Fix-Suggestion Agent in the 'Group of Three' requirement?",
            "Answer: When the Reviewer Manager identifies and ranks findings, the Fix-Suggestion Agent extracts the single highest-severity finding (e.g., hardcoded API key or unsafe eval) and synthesizes a concrete unified git patch showing the exact replacement code."
        ),
        (
            "Q5: Where are the traces and execution steps saved?",
            "Answer: Every step, timestamp, agent action, and payload is recorded in real time inside `state.execution_trace` and appended to the append-only log file `review_run.log` and `test_run.log`."
        )
    ]
    for q, a in viva_qa:
        elements.append(Paragraph(q, qa_q_style))
        elements.append(Paragraph(a, qa_a_style))

    doc.build(elements)
    print(f"Viva PDF guide generated successfully at: {filename}")

if __name__ == "__main__":
    build_pdf(r"D:\PERSONAL\LPU\sem 7\CSE476  AGENTIC AI AND INTELLIGENT AUTOMATION\CA2\Q14_Automated_Code_Review_Board\VIVA_PREPARATION_GUIDE.pdf")
