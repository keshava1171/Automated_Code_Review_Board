"""
main.py - Interactive CLI runner for the Automated Code Review Board.
"""
from orchestrator import CodeReviewOrchestrator

SAMPLE_DIFF = """diff --git a/app/routes.py b/app/routes.py
index 1029384..5647382 100644
--- a/app/routes.py
+++ b/app/routes.py
@@ -1,5 +1,11 @@
 from flask import Flask, request, jsonify
+import subprocess
 
 app = Flask(__name__)
+ADMIN_SECRET = "ghp_1234567890abcdef1234567890abcdef1234"
+
+def run_diagnostic(cmd):
+    # Insecure command execution
+    return subprocess.run(cmd, shell=True, capture_output=True)
"""

def main():
    print("="*75)
    print(" CSE476 CA2: AUTOMATED CODE REVIEW BOARD (Q14)")
    print(" Architecture: Fan-out / Fan-in with Reviewer Manager")
    print(" Built on Microsoft Semantic Kernel Multi-Agent Framework")
    print("="*75)

    orchestrator = CodeReviewOrchestrator(log_file="review_run.log")
    state = orchestrator.run_review(
        raw_diff=SAMPLE_DIFF,
        pr_id="PR-DEMO-2026",
        author="student_dev"
    )

    print("\n" + "="*75)
    print("REVIEW COMPLETE. Log written to 'review_run.log'")
    print(f"Final Decision: {state.final_decision}")
    print("="*75)

if __name__ == "__main__":
    main()
