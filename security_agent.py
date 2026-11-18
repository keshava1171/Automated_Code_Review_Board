"""
security_agent.py - Module 3: Security Agent
Checks for unsafe patterns, hardcoded secrets, injection vectors, and command execution flaws.
"""
from typing import List, Dict, Any
from models import ChangeState, Finding, FindingCategory, Severity
from tools import parse_git_diff, scan_hardcoded_secrets, scan_vulnerable_execution_patterns

class SecurityAgent:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "SecurityAgent"

    def review(self, state: ChangeState) -> List[Dict[str, Any]]:
        """
        Executes Tool 1 (scan_hardcoded_secrets) and Tool 2 (scan_vulnerable_execution_patterns).
        """
        diff_info = parse_git_diff(state.raw_diff)
        file_chunks = diff_info.get("file_chunks", {})

        # Tool 1: Hardcoded secrets
        secret_findings = scan_hardcoded_secrets(file_chunks)
        state.log_step(self.agent_name, "scan_hardcoded_secrets", {
            "threats_found": len(secret_findings),
            "findings": secret_findings
        })

        # Tool 2: Unsafe code patterns (eval, sql injection, shell=True)
        vuln_findings = scan_vulnerable_execution_patterns(file_chunks)
        state.log_step(self.agent_name, "scan_vulnerable_execution_patterns", {
            "threats_found": len(vuln_findings),
            "findings": vuln_findings
        })

        all_security_findings = secret_findings + vuln_findings
        # Record into shared state
        for finding in all_security_findings:
            state.findings.append(Finding(
                category=FindingCategory.SECURITY,
                severity=Severity(finding.get("severity", "HIGH")),
                file_path=finding.get("file"),
                line_number=finding.get("line"),
                description=finding.get("desc"),
                rule_id=finding.get("rule"),
                recommendation=finding.get("fix")
            ))

        return all_security_findings
