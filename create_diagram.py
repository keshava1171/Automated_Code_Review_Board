import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_diagram(output_path="architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.axis('off')

    # Colors
    c_blue = "#2563EB"
    c_slate = "#475569"
    c_emerald = "#059669"
    c_rose = "#E11D48"
    c_amber = "#D97706"
    c_purple = "#7C3AED"
    c_box = "#F8FAFC"
    c_stroke = "#CBD5E1"

    # Title
    ax.text(0.5, 0.96, "Automated Code Review Board - Fan-out / Fan-in Architecture", 
            ha='center', va='center', fontsize=16, fontweight='bold', color="#0F172A")
    ax.text(0.5, 0.92, "CSE476 CA2 Project Q14 | Framework: Microsoft Semantic Kernel", 
            ha='center', va='center', fontsize=11, color="#64748B")

    # Helper function to draw box
    def draw_box(x, y, w, h, title, subtitle, color, bg="#FFFFFF"):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                      facecolor=bg, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=11, fontweight='bold', color=color)
        ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=8.5, color="#334155")

    # Helper function for arrow
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, mutation_scale=15))
        if label:
            ax.text((x1+x2)/2 + 0.02, (y1+y2)/2, label, fontsize=8, color="#64748B", fontweight='semibold')

    # 1. Ingestion: Raw Diff & Diff Agent
    draw_box(0.38, 0.77, 0.24, 0.09, "1. Ingestion & Diff Agent", "Parses files, AST components (+Lines)", c_blue)
    ax.text(0.5, 0.88, "Raw Pull Request Diff (Git)", ha='center', va='center', fontsize=9.5, 
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#F1F5F9', edgecolor='#94A3B8'))
    draw_arrow(0.5, 0.86, 0.5, 0.86-0.09)

    # 2. Fan-Out Branching line
    ax.plot([0.16, 0.84], [0.69, 0.69], color="#64748B", lw=1.5, linestyle="--")
    draw_arrow(0.5, 0.77, 0.5, 0.69)
    ax.text(0.5, 0.71, "Concurrent Fan-Out Phase", ha='center', va='center', fontsize=9, fontweight='bold', color="#2563EB")

    # 3 Specialist Agents (Parallel)
    draw_box(0.06, 0.50, 0.24, 0.14, "Style Agent", "• PEP8 Naming\n• Formatting & Prints\n(Tools 1 & 2)", c_amber)
    draw_arrow(0.18, 0.69, 0.18, 0.64)

    draw_box(0.38, 0.50, 0.24, 0.14, "Security Agent", "• Secret Token Scanner\n• Eval/SQL/Shell Audits\n(Tools 1 & 2)", c_rose)
    draw_arrow(0.50, 0.69, 0.50, 0.64)

    draw_box(0.70, 0.50, 0.24, 0.14, "Test-Coverage Agent", "• File Pairing Check\n• Assertion Density\n(Tools 1 & 2)", c_emerald)
    draw_arrow(0.82, 0.69, 0.82, 0.64)

    # 4. Fan-In Aggregation Line
    ax.plot([0.18, 0.82], [0.44, 0.44], color="#64748B", lw=1.5, linestyle="--")
    draw_arrow(0.18, 0.50, 0.18, 0.44)
    draw_arrow(0.50, 0.50, 0.50, 0.44)
    draw_arrow(0.82, 0.50, 0.82, 0.44)
    ax.text(0.5, 0.46, "Fan-In Aggregation Phase", ha='center', va='center', fontsize=9, fontweight='bold', color="#7C3AED")

    # 5. Reviewer Manager
    draw_arrow(0.5, 0.44, 0.5, 0.38)
    draw_box(0.35, 0.26, 0.30, 0.12, "Reviewer Manager", "Deduplicate & Rank Severity\nEnterprise Merge Gate Policy", c_purple)

    # 6. Verdict and Fix-Suggestion
    draw_arrow(0.5, 0.26, 0.26, 0.16)
    draw_arrow(0.5, 0.26, 0.74, 0.16)

    draw_box(0.12, 0.05, 0.28, 0.11, "Merge Decision", "APPROVE / REQUEST_CHANGES\nPriority Ranked Log", c_emerald)
    draw_box(0.60, 0.05, 0.30, 0.11, "Fix-Suggestion Agent", "Group of 3 Extension:\nSynthesizes Unified Git Patch", c_blue)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Architecture diagram generated at: {output_path}")

if __name__ == "__main__":
    generate_diagram(r"D:\PERSONAL\LPU\sem 7\CSE476  AGENTIC AI AND INTELLIGENT AUTOMATION\CA2\Q14_Automated_Code_Review_Board\architecture_diagram.png")
