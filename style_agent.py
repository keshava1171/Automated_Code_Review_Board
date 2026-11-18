"""
style_agent.py - Module 2: Style Agent
Checks code style, naming conventions, docstrings, and readability issues.
"""
from typing import List, Dict, Any
from models import ChangeState, Finding, FindingCategory, Severity
from tools import parse_git_diff, inspect_naming_conventions, check_formatting_and_comments

class StyleAgent:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "StyleAgent"

    def review(self, state: ChangeState) -> List[Dict[str, Any]]:
        """
        Executes Tool 1 (inspect_naming_conventions) and Tool 2 (check_formatting_and_comments).
        """
        diff_info = parse_git_diff(state.raw_diff)
        file_chunks = diff_info.get("file_chunks", {})

        # Tool 1: Check naming conventions
        naming_issues = inspect_naming_conventions(file_chunks)
        state.log_step(self.agent_name, "inspect_naming_conventions", {
            "issues_count": len(naming_issues),
            "issues": naming_issues
        })

        # Tool 2: Check formatting & debug prints
        format_issues = check_formatting_and_comments(file_chunks)
        state.log_step(self.agent_name, "check_formatting_and_comments", {
            "issues_count": len(format_issues),
            "issues": format_issues
        })

        all_issues = naming_issues + format_issues
        # Record into shared state
        for issue in all_issues:
            state.findings.append(Finding(
                category=FindingCategory.STYLE,
                severity=Severity(issue.get("severity", "LOW")),
                file_path=issue.get("file"),
                line_number=issue.get("line"),
                description=issue.get("desc"),
                rule_id=issue.get("rule"),
                recommendation=issue.get("fix")
            ))

        return all_issues
