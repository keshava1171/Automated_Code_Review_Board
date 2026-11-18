"""
generate_ppt.py - Builds a professional 16:9 widescreen presentation (.pptx)
for CSE476 CA2 Project Q14: Automated Code Review Board.
Includes:
- Slide 1: Title Slide (Group 14, Subject, Names)
- Slide 2: Problem Statement & Motivation
- Slide 3: Multi-Agent Architecture (Embeds architecture_diagram.png)
- Slide 4: Detailed Agent Roster & 12 Plain Python Tools
- Slide 5: The Fan-Out / Fan-In Execution Flow Explained
- Slide 6: Enterprise Gate Policy & Severity Priority
- Slide 7: Failure Handling & Zero-Cost Infrastructure
- Slide 8: Live Demonstration & 3 Test Scenarios
- Slide 9: Viva Defense Cheatsheet & Key Concepts
- Slide 10: Conclusion & Summary
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_pptx="Automated_Code_Review_Board_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    C_NAVY = RGBColor(15, 23, 42)      # #0F172A (Deep Slate/Navy)
    C_BLUE = RGBColor(37, 99, 235)     # #2563EB (Primary Royal Blue)
    C_CYAN = RGBColor(14, 165, 233)    # #0EA5E9
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 41, 59)      # #1E293B
    C_MUTED = RGBColor(100, 116, 139)  # #64748B
    C_BG_LIGHT = RGBColor(248, 250, 252) # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)
    C_RED = RGBColor(225, 29, 72)
    C_GREEN = RGBColor(16, 185, 129)
    C_BORDER = RGBColor(203, 213, 225)

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="CSE476: AGENTIC AI & INTELLIGENT AUTOMATION • CA2"):
        # Header banner
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY

        # Subtle divider
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.02))
        divider.fill.solid()
        divider.fill.fore_color.rgb = C_BORDER
        divider.line.fill.background()

    def add_card(slide, left, top, width, height, title, points, bg_color=C_CARD_BG, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Calibri"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE
        p0.space_after = Pt(8)

        for pt in points:
            p = tf.add_paragraph()
            p.text = "• " + pt
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(4)

    # ========================================================
    # SLIDE 1: Title Slide (Dark Theme for Executive Impact)
    # ========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CYAN
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "LOVELY PROFESSIONAL UNIVERSITY • CSE476 CA2 PROJECT"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = C_CYAN
    p_badge.space_after = Pt(10)

    p_title = tf1.add_paragraph()
    p_title.text = "AUTOMATED CODE REVIEW BOARD"
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Multi-Agent System Automating Enterprise Pull Request Auditing using Semantic Kernel"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(24)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Architecture: Fan-Out / Fan-In with Reviewer Manager  |  Group: Q14 (Group of Three Extension Included)"
    p_meta.font.name = "Calibri"
    p_meta.font.size = Pt(13)
    p_meta.font.color.rgb = C_CYAN

    # Footer note on Slide 1
    p_footer = tf1.add_paragraph()
    p_footer.text = "\nFramework: Microsoft Semantic Kernel  •  Language: Python 3.14  •  Deterministic AST Tools"
    p_footer.font.name = "Calibri"
    p_footer.font.size = Pt(11)
    p_footer.font.color.rgb = C_MUTED

    # ========================================================
    # SLIDE 2: Problem Statement & Real-World Motivation
    # ========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_LIGHT)
    add_header(s2, "Problem Statement & Real-World Motivation")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "The Enterprise Bottleneck", [
                 "Human engineers spend 20-30% of their work hours manually reviewing code diffs.",
                 "Manual review is error-prone: critical security vulnerabilities and hardcoded secrets slip into production.",
                 "Style debates and formatting squabbles clutter comments, distracting from architectural decisions."
             ])

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Why Single-Agent Fails", [
                 "Single prompts to general LLMs suffer from severe hallucinations on subtle code bugs.",
                 "Sequential chains run slowly because style, security, and test checks don't need to wait for one another.",
                 "No enterprise policy gate: LLMs give vague commentary rather than a definitive APPROVE / REJECT verdict."
             ])

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), 
             "Our Multi-Agent Solution", [
                 "Specialized division of labor: Dedicated agents for Diff, Style, Security, and Test Coverage.",
                 "High-speed concurrency: Independent agents run in parallel using Fan-Out thread pooling.",
                 "Decisive Governance: Reviewer Manager ranks issues by severity and enforces corporate merge criteria.",
                 "Automated Remediation: Synthesizes concrete git patches for immediate one-click fixes."
             ])

    # ========================================================
    # SLIDE 3: System Architecture (Diagram Slide)
    # ========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_LIGHT)
    add_header(s3, "Multi-Agent Coordination Architecture (Fan-Out / Fan-In)")

    # Left: Explanation Bullets
    add_card(s3, Inches(0.8), Inches(1.8), Inches(4.2), Inches(5.1), 
             "Architectural Flow", [
                 "Phase 1: Ingestion (Diff Agent)",
                 "   Parses git diff into modified chunks and AST nodes.",
                 "Phase 2: Concurrent Fan-Out (Parallel Audits)",
                 "   Style, Security, and Test-Coverage run simultaneously.",
                 "Phase 3: Fan-In Aggregation (Reviewer Manager)",
                 "   Deduplicates reports and sorts by CRITICAL > HIGH > MED > LOW.",
                 "Phase 4: Auto-Remediation (Fix-Suggestion)",
                 "   Generates unified git replacement patch for top blocker.",
                 "Shared Memory (ChangeState Object)",
                 "   All agents read and append to one unified state record."
             ])

    # Right: Embedded Architecture Diagram Image
    diagram_path = r"D:\PERSONAL\LPU\sem 7\CSE476  AGENTIC AI AND INTELLIGENT AUTOMATION\CA2\Q14_Automated_Code_Review_Board\architecture_diagram.png"
    if os.path.exists(diagram_path):
        s3.shapes.add_picture(diagram_path, Inches(5.2), Inches(1.8), width=Inches(7.3))

    # ========================================================
    # SLIDE 4: Agent Roster & 12 Plain Python Tools
    # ========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_LIGHT)
    add_header(s4, "Agent Roster & Mandatory Python Tools (2 Tools Per Agent)")

    # 6 boxes in a 3x2 grid
    col_w = Inches(3.6)
    row_h = Inches(2.4)
    c1, c2, c3 = Inches(0.8), Inches(4.8), Inches(8.8)
    r1, r2 = Inches(1.8), Inches(4.5)

    add_card(s4, c1, r1, col_w, row_h, "1. Diff Agent (diff_agent.py)", [
        "Tool 1: parse_git_diff() - Extracts modified files and line additions/deletions.",
        "Tool 2: extract_touched_components() - Uses Python AST to detect new functions and classes."
    ])
    add_card(s4, c2, r1, col_w, row_h, "2. Style Agent (style_agent.py)", [
        "Tool 1: inspect_naming_conventions() - Flags camelCase vs PEP8 snake_case.",
        "Tool 2: check_formatting_and_comments() - Flags >100 char lines and raw print() calls."
    ])
    add_card(s4, c3, r1, col_w, row_h, "3. Security Agent (security_agent.py)", [
        "Tool 1: scan_hardcoded_secrets() - Audits for AWS tokens, PAT keys, and passwords.",
        "Tool 2: scan_vulnerable_execution() - Flags unsafe eval(), raw SQL, shell=True."
    ])
    add_card(s4, c1, r2, col_w, row_h, "4. Test Agent (test_coverage_agent.py)", [
        "Tool 1: verify_test_file_pairing() - Checks if source changes include a test_*.py file.",
        "Tool 2: inspect_assertion_quality() - Ensures tests contain real assert statements."
    ])
    add_card(s4, c2, r2, col_w, row_h, "5. Reviewer Manager (reviewer_manager.py)", [
        "Tool 1: deduplicate_and_rank() - Sorts all agent signals by severity priority.",
        "Tool 2: evaluate_merge_policy() - Blocks merge if Critical/High findings exist."
    ])
    add_card(s4, c3, r2, col_w, row_h, "6. Fix Agent (fix_suggestion_agent.py)", [
        "Tool 1: extract_top_finding() - Extracts top blocker from consolidated board.",
        "Tool 2: synthesize_patch() - Emits unified git replacement patch."
    ])

    # ========================================================
    # SLIDE 5: Fan-Out / Fan-In Coordination Deep Dive
    # ========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_LIGHT)
    add_header(s5, "The Fan-Out / Fan-In Execution Pipeline")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Step 1 & 2: Ingestion & Parallel Fan-Out", [
                 "1. Pull Request Enters System:",
                 "   A developer submits a raw git diff or patch file.",
                 "2. Diff Agent Ingestion:",
                 "   The Diff Agent reads the diff, separates changed chunks, and parses declared Python classes and functions using AST.",
                 "3. Concurrent Thread Fanning:",
                 "   The orchestrator uses ThreadPoolExecutor(max_workers=3) to dispatch tasks to Style, Security, and Test-Coverage agents simultaneously.",
                 "4. Zero-Dependency Execution:",
                 "   Security checks do not need to wait for style checks. Running them concurrently eliminates sequential bottlenecks."
             ])

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), 
             "Step 3 & 4: Fan-In & Fix Remediation", [
                 "5. Fan-In Aggregation:",
                 "   The Reviewer Manager waits for all 3 worker threads to finish and collects their findings into one unified list.",
                 "6. Deduplication & Priority Ranking:",
                 "   Overlapping findings are purged. Issues are ordered strictly: CRITICAL (1) > HIGH (2) > MEDIUM (3) > LOW (4).",
                 "7. Enterprise Policy Enforcement:",
                 "   The manager executes evaluate_merge_policy() to issue a definitive APPROVE or REQUEST_CHANGES verdict.",
                 "8. Automated Patch Synthesis:",
                 "   If blockers exist, the Fix-Suggestion Agent synthesizes the exact git patch replacing vulnerable code."
             ])

    # ========================================================
    # SLIDE 6: Enterprise Gate Policy & Severity Matrix
    # ========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_LIGHT)
    add_header(s6, "Enterprise Merge Policy & Severity Ranking")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Severity Classification Matrix", [
                 "CRITICAL (Blocker):",
                 "   • Hardcoded AWS / GitHub / Database credentials.",
                 "   • Arbitrary code execution via eval() or exec().",
                 "HIGH (Major Defect):",
                 "   • SQL Injection via string interpolation.",
                 "   • Remote command injection via subprocess(shell=True).",
                 "   • Empty test files with zero assertions.",
                 "MEDIUM (Advisory):",
                 "   • Production source code modified with no matching unit test.",
                 "   • Raw print() debug statements in production code.",
                 "LOW (Hygiene):",
                 "   • PEP8 naming violations (camelCase instead of snake_case).",
                 "   • Lines exceeding 100 characters in length."
             ])

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), 
             "The Enterprise Merge Decision Engine", [
                 "Gate Rule 1: Zero-Tolerance on Security",
                 "   If Count(CRITICAL) > 0 OR Count(HIGH) > 0:",
                 "   ==> Final Verdict: REQUEST_CHANGES (Hard Block).",
                 "   The Pull Request cannot merge until the developer addresses findings.",
                 "Gate Rule 2: Advisory Tolerance",
                 "   If Count(CRITICAL) == 0 AND Count(HIGH) == 0 AND Count(MEDIUM) > 0:",
                 "   ==> Final Verdict: APPROVE (With Advisories).",
                 "   Merge is allowed, but warnings are flagged in the review log.",
                 "Gate Rule 3: Perfect Quality",
                 "   If All Counts == 0:",
                 "   ==> Final Verdict: APPROVE (Clean Pass).",
                 "   Immediate automated approval into production."
             ])

    # ========================================================
    # SLIDE 7: Failure Handling & Zero-Cost Architecture
    # ========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_LIGHT)
    add_header(s7, "Resilience: Failure Handling & Zero-Cost Infrastructure")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Graceful Failure Handling (Rubric Requirement)", [
                 "The Failure Challenge: Malformed Syntax",
                 "   Developers frequently submit incomplete snippets or partial diffs with syntax errors.",
                 "The Standard Crash:",
                 "   Running Python's native ast.parse() on incomplete snippets normally raises a fatal SyntaxError and crashes the pipeline.",
                 "Our Graceful Fallback Strategy:",
                 "   • Diff Agent wraps AST parsing in a robust try-except block.",
                 "   • If AST fails, it automatically falls back to regex-based structural pattern extraction.",
                 "   • The warning is logged in the append-only trace without halting the review pipeline."
             ])

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), 
             "Zero-Cost & Deterministic Architecture", [
                 "Why We Chose Deterministic Python Tools:",
                 "   1. Zero Latency (0ms network delay):",
                 "      Runs completely offline without waiting on external LLM APIs.",
                 "   2. Immunity from API Limits:",
                 "      Never suffers from HTTP 429 'Too Many Requests' or quota exhaustion during the viva.",
                 "   3. Zero LLM Hallucinations:",
                 "      Security audits and mathematical policies are 100% deterministic and reproducible.",
                 "   4. Semantic Kernel Integration:",
                 "      Microsoft Semantic Kernel provides the extensible orchestration bus connecting our agent modules."
             ])

    # ========================================================
    # SLIDE 8: Test Scenarios & Interactive Dashboard
    # ========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_BG_LIGHT)
    add_header(s8, "Automated Test Suite & Interactive Visual Dashboard")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Scenario 1: Critical Security", [
                 "Input: Hardcoded AWS secret key + dynamic eval() function.",
                 "Specialist Audits:",
                 "   Security Agent flags SEC-001 and SEC-010.",
                 "Manager Verdict:",
                 "   REQUEST_CHANGES.",
                 "Fix Agent:",
                 "   Emits unified git patch replacing secret with os.getenv('APP_API_KEY')."
             ])

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Scenario 2: Style & Tests", [
                 "Input: camelCase function + raw print() + missing test file.",
                 "Specialist Audits:",
                 "   • Style Agent flags PEP8-N802 & debug print.",
                 "   • Test Agent flags TEST-MISSING-PAIR.",
                 "Manager Verdict:",
                 "   APPROVE (with Advisories).",
                 "Fix Agent:",
                 "   Recommends structured logger."
             ])

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), 
             "Scenario 3: Clean PR", [
                 "Input: Clean math function + matching unit test with assertEqual().",
                 "Specialist Audits:",
                 "   Zero security flaws, zero style bugs, 100% test file pairing.",
                 "Manager Verdict:",
                 "   APPROVE (Clean Pass).",
                 "Output:",
                 "   Immediate green signal for deployment."
             ])

    # ========================================================
    # SLIDE 9: Viva Defense Cheatsheet & Key Concepts
    # ========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_BG_LIGHT)
    add_header(s9, "Viva Defense Cheatsheet (Quick Reference for Teachers)")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Core Multi-Agent Terminology", [
                 "Agentic AI:",
                 "   Autonomous programs that perceive inputs, use tools, collaborate with peers, and make goal-oriented decisions.",
                 "Shared State (ChangeState):",
                 "   A centralized memory object passed between agents carrying diff data, findings, decisions, and execution traces.",
                 "Fan-Out / Fan-In:",
                 "   A distributed design pattern where one task splits across concurrent workers (Fan-Out) and aggregates back to a manager (Fan-In).",
                 "Deterministic Tools:",
                 "   Native code functions with mathematically predictable logic, ensuring zero hallucinations."
             ])

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), 
             "Likely Questions & Ready Answers", [
                 "Q: Why separate files for each agent?",
                 "A: Strict adherence to rubric requirement: modular software engineering where each agent has one distinct responsibility.",
                 "Q: How do you verify test coverage quality?",
                 "A: Tool 2 checks assertion density to ensure test files aren't just empty mocks without assert statements.",
                 "Q: Where are logs saved?",
                 "A: Every step is timestamped and recorded into our append-only log files (review_run.log and test_run.log)."
             ])

    # ========================================================
    # SLIDE 10: Conclusion & Summary
    # ========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_NAVY)

    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(4.8))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p_end_badge = tf10.paragraphs[0]
    p_end_badge.text = "CSE476 CA2 PROJECT CONCLUSION"
    p_end_badge.font.name = "Calibri"
    p_end_badge.font.size = Pt(14)
    p_end_badge.font.bold = True
    p_end_badge.font.color.rgb = C_CYAN
    p_end_badge.space_after = Pt(12)

    p_end_title = tf10.add_paragraph()
    p_end_title.text = "Fully Verified & Ready for Evaluation"
    p_end_title.font.name = "Calibri"
    p_end_title.font.size = Pt(32)
    p_end_title.font.bold = True
    p_end_title.font.color.rgb = C_WHITE
    p_end_title.space_after = Pt(20)

    p_chk1 = tf10.add_paragraph()
    p_chk1.text = "✓ 100% Rubric Compliance: 6 separate agent modules, 12 plain Python tools, Fan-Out / Fan-In architecture."
    p_chk1.font.name = "Calibri"
    p_chk1.font.size = Pt(14)
    p_chk1.font.color.rgb = RGBColor(226, 232, 240)
    p_chk1.space_after = Pt(8)

    p_chk2 = tf10.add_paragraph()
    p_chk2.text = "✓ Group of Three Extension: Fix-Suggestion Agent generating concrete unified git patches."
    p_chk2.font.name = "Calibri"
    p_chk2.font.size = Pt(14)
    p_chk2.font.color.rgb = RGBColor(226, 232, 240)
    p_chk2.space_after = Pt(8)

    p_chk3 = tf10.add_paragraph()
    p_chk3.text = "✓ Multi-Faceted Visuals: Interactive Web Dashboard (dashboard.html), SVG diagram, and runnable notebook."
    p_chk3.font.name = "Calibri"
    p_chk3.font.size = Pt(14)
    p_chk3.font.color.rgb = RGBColor(226, 232, 240)
    p_chk3.space_after = Pt(8)

    p_chk4 = tf10.add_paragraph()
    p_chk4.text = "✓ Test Verified: 3/3 automated test scenarios passing with append-only logging."
    p_chk4.font.name = "Calibri"
    p_chk4.font.size = Pt(14)
    p_chk4.font.color.rgb = RGBColor(226, 232, 240)
    p_chk4.space_after = Pt(24)

    p_thanks = tf10.add_paragraph()
    p_thanks.text = "Thank you! We invite your questions."
    p_thanks.font.name = "Calibri"
    p_thanks.font.size = Pt(20)
    p_thanks.font.bold = True
    p_thanks.font.color.rgb = C_CYAN

    # Save presentation
    prs.save(output_pptx)
    print(f"PowerPoint Presentation generated successfully at: {output_pptx}")

if __name__ == "__main__":
    out = r"D:\PERSONAL\LPU\sem 7\CSE476  AGENTIC AI AND INTELLIGENT AUTOMATION\CA2\Q14_Automated_Code_Review_Board\Automated_Code_Review_Board_Presentation.pptx"
    create_deck(out)
