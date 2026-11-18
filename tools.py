"""
tools.py - Dedicated tools for each specialized agent in the Code Review Board.
Requirement: Each agent calls at least TWO real tools written as plain Python functions.
"""
import re
import ast
from typing import List, Dict, Any, Optional

# ==========================================
# Tools for Diff Agent
# ==========================================
def parse_git_diff(diff_text: str) -> Dict[str, Any]:
    """
    Tool 1 for Diff Agent:
    Parses raw git diff text into structured files, added lines, and removed lines.
    """
    files = []
    current_file = None
    added_lines = []
    removed_lines = []
    file_chunks = {}

    for line in diff_text.strip().splitlines():
        if line.startswith("diff --git"):
            match = re.search(r"b/(.*)$", line)
            current_file = match.group(1) if match else "unknown"
            files.append(current_file)
            file_chunks[current_file] = {"added": [], "removed": []}
        elif line.startswith("+++ b/"):
            current_file = line[6:].strip()
            if current_file not in files:
                files.append(current_file)
            if current_file not in file_chunks:
                file_chunks[current_file] = {"added": [], "removed": []}
        elif line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
            if current_file:
                file_chunks[current_file]["added"].append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line[1:])
            if current_file:
                file_chunks[current_file]["removed"].append(line[1:])

    return {
        "files": files,
        "total_added": len(added_lines),
        "total_removed": len(removed_lines),
        "file_chunks": file_chunks
    }

def extract_touched_components(file_chunks: Dict[str, Any]) -> List[str]:
    """
    Tool 2 for Diff Agent:
    Analyzes added code lines using Python AST (or regex) to detect newly added classes/functions.
    """
    components = []
    for filename, chunks in file_chunks.items():
        if filename.endswith(".py"):
            content = "\n".join(chunks.get("added", []))
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        components.append(f"{filename} -> function: {node.name}()")
                    elif isinstance(node, ast.ClassDef):
                        components.append(f"{filename} -> class: {node.name}")
            except Exception:
                # Fallback to regex if parsing a snippet with indentation issues
                for line in chunks.get("added", []):
                    func_match = re.search(r"def\s+([a-zA-Z0-9_]+)\s*\(", line)
                    if func_match:
                        components.append(f"{filename} -> function: {func_match.group(1)}()")
                    class_match = re.search(r"class\s+([a-zA-Z0-9_]+)", line)
                    if class_match:
                        components.append(f"{filename} -> class: {class_match.group(1)}")
    return components


# ==========================================
# Tools for Style Agent
# ==========================================
def inspect_naming_conventions(file_chunks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool 1 for Style Agent:
    Validates PEP8 naming conventions: functions should be snake_case, classes CamelCase.
    """
    issues = []
    for filename, chunk in file_chunks.items():
        for line_no, line in enumerate(chunk.get("added", []), start=1):
            # Check function names
            func_match = re.search(r"def\s+([a-zA-Z0-9_]+)\s*\(", line)
            if func_match:
                func_name = func_match.group(1)
                if not func_name.startswith("__") and any(c.isupper() for c in func_name):
                    issues.append({
                        "file": filename,
                        "line": line_no,
                        "rule": "PEP8-N802",
                        "severity": "LOW",
                        "desc": f"Function name '{func_name}' is not in snake_case.",
                        "fix": f"Rename '{func_name}' to lowercase with underscores."
                    })
            # Check variable names that look like camelCase
            var_match = re.search(r"^\s*([a-z]+[A-Z][a-zA-Z0-9]*)\s*=", line)
            if var_match:
                var_name = var_match.group(1)
                issues.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "PEP8-N806",
                    "severity": "LOW",
                    "desc": f"Variable name '{var_name}' uses camelCase instead of snake_case.",
                    "fix": f"Rename '{var_name}' to snake_case."
                })
    return issues

def check_formatting_and_comments(file_chunks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool 2 for Style Agent:
    Detects lines exceeding standard 100 character length, missing docstrings, or debug prints.
    """
    issues = []
    for filename, chunk in file_chunks.items():
        for line_no, line in enumerate(chunk.get("added", []), start=1):
            if len(line) > 100:
                issues.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "PEP8-E501",
                    "severity": "LOW",
                    "desc": f"Line exceeds 100 characters ({len(line)} chars).",
                    "fix": "Wrap line or split into multiple expressions."
                })
            if re.search(r"\bprint\s*\(", line):
                issues.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "STYLE-DEBUG-PRINT",
                    "severity": "MEDIUM",
                    "desc": "Found raw 'print()' call. Use structured logging instead.",
                    "fix": "Replace print with logger.info() or logger.debug()."
                })
    return issues


# ==========================================
# Tools for Security Agent
# ==========================================
def scan_hardcoded_secrets(file_chunks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool 1 for Security Agent:
    Scans for exposed API keys, private keys, passwords, or tokens in added lines.
    """
    findings = []
    patterns = [
        (r"(?i)(api[_-]?key|secret|token|password|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-\.]{8,}['\"]", "SEC-001", "CRITICAL", "Hardcoded API key or credential detected."),
        (r"ghp_[A-Za-z0-9]{36}", "SEC-002", "CRITICAL", "GitHub Personal Access Token detected."),
        (r"AKIA[0-9A-Z]{16}", "SEC-003", "CRITICAL", "AWS Access Key ID detected."),
        (r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "SEC-004", "CRITICAL", "Private encryption key embedded in source code.")
    ]
    for filename, chunk in file_chunks.items():
        for line_no, line in enumerate(chunk.get("added", []), start=1):
            for pattern, rule_id, sev, desc in patterns:
                if re.search(pattern, line):
                    findings.append({
                        "file": filename,
                        "line": line_no,
                        "rule": rule_id,
                        "severity": sev,
                        "desc": desc,
                        "fix": "Remove hardcoded secret and load from environment variables (os.getenv) or secret vault."
                    })
    return findings

def scan_vulnerable_execution_patterns(file_chunks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool 2 for Security Agent:
    Scans for SQL injection patterns, dangerous eval()/exec(), and shell=True calls.
    """
    findings = []
    for filename, chunk in file_chunks.items():
        for line_no, line in enumerate(chunk.get("added", []), start=1):
            if re.search(r"\b(eval|exec)\s*\(", line):
                findings.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "SEC-010",
                    "severity": "CRITICAL",
                    "desc": "Arbitrary code execution via 'eval()' or 'exec()'.",
                    "fix": "Use safe parsing (e.g., ast.literal_eval or json.loads) instead of eval."
                })
            # SQL string interpolation
            if re.search(r"(?i)(SELECT|INSERT|UPDATE|DELETE)\s+.*f['\"].*\{.+\}", line) or \
               re.search(r"(?i)(SELECT|INSERT|UPDATE|DELETE)\s+.*%s.*%\s*\(", line) or \
               re.search(r"(?i)execute\s*\(\s*f['\"].*\{", line):
                findings.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "SEC-020",
                    "severity": "HIGH",
                    "desc": "Potential SQL Injection via string formatting/interpolation.",
                    "fix": "Use parameterized queries with placeholders (? or %s) provided separately."
                })
            # Shell command execution
            if re.search(r"subprocess\.(Popen|run|call)\s*\(.*shell\s*=\s*True", line):
                findings.append({
                    "file": filename,
                    "line": line_no,
                    "rule": "SEC-030",
                    "severity": "HIGH",
                    "desc": "subprocess execution with shell=True invites command injection.",
                    "fix": "Pass arguments as an argument list and set shell=False."
                })
    return findings


# ==========================================
# Tools for Test-Coverage Agent
# ==========================================
def verify_test_file_pairing(files_touched: List[str]) -> List[Dict[str, Any]]:
    """
    Tool 1 for Test-Coverage Agent:
    Ensures that for every source code file modified, a corresponding test file is also touched.
    """
    findings = []
    source_files = [f for f in files_touched if not f.startswith("test") and not "/test" in f and not "tests/" in f and f.endswith(".py")]
    test_files = [f for f in files_touched if ("test_" in f or "_test.py" in f or "tests/" in f)]

    for src in source_files:
        expected_test = f"test_{src}"
        has_test = any(expected_test in tf or src.replace(".py", "") in tf for tf in test_files)
        if not has_test:
            findings.append({
                "file": src,
                "line": None,
                "rule": "TEST-MISSING-PAIR",
                "severity": "MEDIUM",
                "desc": f"Source file '{src}' was changed without corresponding changes in test suite.",
                "fix": f"Add or update unit tests in 'tests/test_{src}'."
            })
    return findings

def inspect_assertion_quality(file_chunks: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool 2 for Test-Coverage Agent:
    Checks if added test files actually contain assertions or if they are empty/mocked tests.
    """
    findings = []
    for filename, chunk in file_chunks.items():
        if "test" in filename and filename.endswith(".py"):
            added_code = "\n".join(chunk.get("added", []))
            assertions = re.findall(r"\bassert\b|assertEqual|assertTrue|assertRaises", added_code)
            if len(assertions) == 0:
                findings.append({
                    "file": filename,
                    "line": None,
                    "rule": "TEST-EMPTY-ASSERTIONS",
                    "severity": "HIGH",
                    "desc": f"Test file '{filename}' was added/modified but contains zero assertions.",
                    "fix": "Ensure test functions contain explicit assert statements verifying behavior."
                })
    return findings


# ==========================================
# Tools for Reviewer Manager
# ==========================================
def deduplicate_and_rank_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Tool 1 for Reviewer Manager:
    Deduplicates overlapping agent reports and sorts them by severity priority order:
    CRITICAL (1) > HIGH (2) > MEDIUM (3) > LOW (4) > INFO (5).
    """
    severity_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4, "INFO": 5}
    seen = set()
    deduped = []
    for f in findings:
        key = (f.get("file"), f.get("line"), f.get("rule"))
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    deduped.sort(key=lambda x: severity_order.get(x.get("severity", "INFO"), 99))
    return deduped

def evaluate_merge_policy(ranked_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tool 2 for Reviewer Manager:
    Applies enterprise gate policy:
    - If any CRITICAL or HIGH finding exists: REQUEST_CHANGES
    - If only MEDIUM/LOW/INFO findings exist: APPROVE with suggestions
    - If no findings: APPROVE cleanly
    """
    critical_count = sum(1 for f in ranked_findings if f.get("severity") == "CRITICAL")
    high_count = sum(1 for f in ranked_findings if f.get("severity") == "HIGH")
    medium_count = sum(1 for f in ranked_findings if f.get("severity") == "MEDIUM")
    low_count = sum(1 for f in ranked_findings if f.get("severity") == "LOW")

    if critical_count > 0 or high_count > 0:
        decision = "REQUEST_CHANGES"
        reason = f"Blocked by {critical_count} CRITICAL and {high_count} HIGH severity finding(s)."
    elif medium_count > 0:
        decision = "APPROVE"
        reason = f"Approved with advisories: {medium_count} medium-priority items noted."
    else:
        decision = "APPROVE"
        reason = "Clean merge approved. All security, style, and coverage checks passed."

    return {
        "decision": decision,
        "reason": reason,
        "counts": {
            "CRITICAL": critical_count,
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        }
    }


# ==========================================
# Tools for Fix-Suggestion Agent (Group of Three Extension)
# ==========================================
def extract_top_finding(ranked_findings: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Tool 1 for Fix-Suggestion Agent:
    Picks the single highest-severity finding from the consolidated review board.
    """
    if not ranked_findings:
        return None
    return ranked_findings[0]

def synthesize_patch(finding: Dict[str, Any], raw_diff: str) -> Dict[str, Any]:
    """
    Tool 2 for Fix-Suggestion Agent:
    Generates a concrete unified diff / replacement code snippet fixing the highest severity finding.
    """
    if not finding:
        return {"patch": None, "explanation": "No actionable findings found."}

    rule = finding.get("rule", "")
    fix_text = finding.get("fix", "")
    target_file = finding.get("file", "source.py")

    # Example patch patterns
    if "SEC-001" in rule or "SEC-002" in rule:
        patch = (
            f"--- {target_file}\n"
            f"+++ {target_file}\n"
            f"@@ Replace hardcoded secret with environment variable @@\n"
            f"- API_KEY = 'secret_key_12345'\n"
            f"+ import os\n"
            f"+ API_KEY = os.getenv('APP_API_KEY')\n"
            f"+ if not API_KEY:\n"
            f"+     raise EnvironmentError('Missing APP_API_KEY environment variable')\n"
        )
    elif "SEC-010" in rule:
        patch = (
            f"--- {target_file}\n"
            f"+++ {target_file}\n"
            f"@@ Replace dangerous eval() with ast.literal_eval @@\n"
            f"- result = eval(user_input)\n"
            f"+ import ast\n"
            f"+ result = ast.literal_eval(user_input)\n"
        )
    elif "SEC-020" in rule:
        patch = (
            f"--- {target_file}\n"
            f"+++ {target_file}\n"
            f"@@ Use parameterized SQL query @@\n"
            f"- cursor.execute(f'SELECT * FROM users WHERE username = \"{{user}}\"')\n"
            f"+ cursor.execute('SELECT * FROM users WHERE username = %s', (user,))\n"
        )
    else:
        patch = (
            f"--- {target_file}\n"
            f"+++ {target_file}\n"
            f"@@ Recommended patch @@\n"
            f"# Follow fix instruction:\n"
            f"# {fix_text}\n"
        )

    return {
        "target_file": target_file,
        "rule_id": rule,
        "patch": patch,
        "explanation": f"Automated fix applied for [{finding.get('severity')}] {finding.get('desc')}: {fix_text}"
    }
