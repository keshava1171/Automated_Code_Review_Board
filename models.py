"""
models.py - Shared data models and state object for Automated Code Review Board.
Architecture: Fan-out / Fan-in with Reviewer Manager.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import datetime

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FindingCategory(str, Enum):
    STYLE = "STYLE"
    SECURITY = "SECURITY"
    TEST_COVERAGE = "TEST_COVERAGE"
    SYNTAX = "SYNTAX"

@dataclass
class Finding:
    category: FindingCategory
    severity: Severity
    file_path: str
    line_number: Optional[int]
    description: str
    rule_id: str
    recommendation: str

@dataclass
class ChangeState:
    """
    Shared Change-State Object carried through the Fan-out / Fan-in pipeline.
    All specialist agents read from this state and append findings into it.
    """
    raw_diff: str
    pr_id: str
    author: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    files_touched: List[str] = field(default_factory=list)
    summary_of_changes: str = ""
    findings: List[Finding] = field(default_factory=list)
    final_decision: Optional[str] = None  # "APPROVE" or "REQUEST_CHANGES"
    consolidated_summary: Optional[str] = None
    fix_suggestions: List[Dict[str, Any]] = field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)

    def log_step(self, agent_name: str, action: str, details: Any):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execution_trace.append({
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details
        })
