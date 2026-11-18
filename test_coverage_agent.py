"""
test_coverage_agent.py - Module 4: Test-Coverage Agent
Checks whether the code change is tested and verifies test assertion quality.
"""
from typing import List, Dict, Any
from models import ChangeState, Finding, FindingCategory, Severity
from tools import parse_git_diff, verify_test_file_pairing, inspect_assertion_quality

class TestCoverageAgent:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "TestCoverageAgent"

    def review(self, state: ChangeState) -> List[Dict[str, Any]]:
        """
        Executes Tool 1 (verify_test_file_pairing) and Tool 2 (inspect_assertion_quality).
        """
        diff_info = parse_git_diff(state.raw_diff)
        file_chunks = diff_info.get("file_chunks", {})

        # Tool 1: Test file pairing
        pairing_issues = verify_test_file_pairing(state.files_touched or diff_info.get("files", []))
        state.log_step(self.agent_name, "verify_test_file_pairing", {
            "unpaired_source_files": len(pairing_issues),
            "issues": pairing_issues
        })

        # Tool 2: Test assertion quality
        assertion_issues = inspect_assertion_quality(file_chunks)
        state.log_step(self.agent_name, "inspect_assertion_quality", {
            "weak_tests": len(assertion_issues),
            "issues": assertion_issues
        })

        all_coverage_issues = pairing_issues + assertion_issues
        # Record into shared state
        for issue in all_coverage_issues:
            state.findings.append(Finding(
                category=FindingCategory.TEST_COVERAGE,
                severity=Severity(issue.get("severity", "MEDIUM")),
                file_path=issue.get("file"),
                line_number=issue.get("line"),
                description=issue.get("desc"),
                rule_id=issue.get("rule"),
                recommendation=issue.get("fix")
            ))

        return all_coverage_issues
