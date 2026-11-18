"""
fix_suggestion_agent.py - Module 6: Fix-Suggestion Agent (Group of Three Extension)
Proposes a concrete patch for the single highest-severity finding from the consolidated review.
"""
from typing import Dict, Any, Optional
from models import ChangeState
from tools import extract_top_finding, synthesize_patch

class FixSuggestionAgent:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "FixSuggestionAgent"

    def generate_fix(self, state: ChangeState, ranked_findings: list) -> Optional[Dict[str, Any]]:
        """
        Executes Tool 1 (extract_top_finding) and Tool 2 (synthesize_patch).
        """
        # Tool 1: Identify top priority issue
        top_finding = extract_top_finding(ranked_findings)
        state.log_step(self.agent_name, "extract_top_finding", {
            "top_finding": top_finding
        })

        if not top_finding:
            return None

        # Tool 2: Formulate patch
        patch_payload = synthesize_patch(top_finding, state.raw_diff)
        state.log_step(self.agent_name, "synthesize_patch", patch_payload)

        state.fix_suggestions.append(patch_payload)
        return patch_payload
