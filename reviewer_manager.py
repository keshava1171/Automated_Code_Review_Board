"""
reviewer_manager.py - Module 5: Reviewer Manager
Fans the findings back in, deduplicates them, ranks by priority order, and outputs the final merge recommendation.
"""
from typing import Dict, Any, List
from models import ChangeState
from tools import deduplicate_and_rank_findings, evaluate_merge_policy

class ReviewerManager:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "ReviewerManager"

    def consolidate(self, state: ChangeState) -> Dict[str, Any]:
        """
        Executes Tool 1 (deduplicate_and_rank_findings) and Tool 2 (evaluate_merge_policy).
        """
        # Convert state.findings dataclasses into dictionary list for tool processing
        findings_dicts = [
            {
                "category": f.category.value,
                "severity": f.severity.value,
                "file": f.file_path,
                "line": f.line_number,
                "rule": f.rule_id,
                "desc": f.description,
                "fix": f.recommendation
            }
            for f in state.findings
        ]

        # Tool 1: Deduplicate and sort by severity
        ranked_findings = deduplicate_and_rank_findings(findings_dicts)
        state.log_step(self.agent_name, "deduplicate_and_rank_findings", {
            "total_ranked_findings": len(ranked_findings)
        })

        # Tool 2: Apply enterprise merge policy
        policy_eval = evaluate_merge_policy(ranked_findings)
        state.log_step(self.agent_name, "evaluate_merge_policy", policy_eval)

        decision = policy_eval["decision"]
        reason = policy_eval["reason"]
        counts = policy_eval["counts"]

        # Build clean consolidated summary
        summary_lines = [
            f"=== CONSOLIDATED CODE REVIEW DECISION: {decision} ===",
            f"Reason: {reason}",
            f"Findings Breakdown: {counts['CRITICAL']} Critical, {counts['HIGH']} High, {counts['MEDIUM']} Medium, {counts['LOW']} Low",
            "",
            "Grouped Findings by Severity Priority:"
        ]

        if not ranked_findings:
            summary_lines.append("  (No code review issues found. Ready for merge!)")
        else:
            for i, f in enumerate(ranked_findings, 1):
                loc = f"{f['file']}" + (f":L{f['line']}" if f['line'] else "")
                summary_lines.append(f"  {i}. [{f['severity']}] [{f['category']}] ({loc}): {f['desc']}")
                summary_lines.append(f"     -> Fix: {f['fix']}")

        consolidated_summary = "\n".join(summary_lines)
        state.final_decision = decision
        state.consolidated_summary = consolidated_summary

        return {
            "decision": decision,
            "reason": reason,
            "counts": counts,
            "ranked_findings": ranked_findings,
            "consolidated_summary": consolidated_summary
        }
