"""
orchestrator.py - Coordination Engine implementing Fan-out / Fan-in Architecture.
Orchestrates:
1. Diff Agent (Ingestion)
2. Fan-out in parallel: Style Agent, Security Agent, Test-Coverage Agent
3. Fan-in: Reviewer Manager (Aggregation, Ranking, Policy Decision)
4. Group of Three: Fix-Suggestion Agent (Concrete Patch for Top Severity)
"""
import concurrent.futures
import json
import os
import semantic_kernel as sk
from models import ChangeState
from diff_agent import DiffAgent
from style_agent import StyleAgent
from security_agent import SecurityAgent
from test_coverage_agent import TestCoverageAgent
from reviewer_manager import ReviewerManager
from fix_suggestion_agent import FixSuggestionAgent

class CodeReviewOrchestrator:
    def __init__(self, log_file: str = "review_run.log"):
        self.kernel = sk.Kernel()
        self.log_file = log_file

        # Initialize specialist agent modules
        self.diff_agent = DiffAgent(self.kernel)
        self.style_agent = StyleAgent(self.kernel)
        self.security_agent = SecurityAgent(self.kernel)
        self.test_coverage_agent = TestCoverageAgent(self.kernel)
        self.reviewer_manager = ReviewerManager(self.kernel)
        self.fix_agent = FixSuggestionAgent(self.kernel)

    def append_log(self, entry: str):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def run_review(self, raw_diff: str, pr_id: str = "PR-101", author: str = "developer") -> ChangeState:
        state = ChangeState(raw_diff=raw_diff, pr_id=pr_id, author=author)
        self.append_log(f"[{state.created_at}] --- STARTING REVIEW FOR {pr_id} by {author} ---")

        # Step 1: Sequential Ingestion by Diff Agent
        print(f"\n[Phase 1] Diff Agent ingesting PR {pr_id}...")
        diff_res = self.diff_agent.review(state)
        print(f"  -> {state.summary_of_changes}")

        # Step 2: Fan-out (Parallel Execution of Specialist Agents)
        print(f"\n[Phase 2] FANNING OUT: Style, Security, and Test-Coverage Agents running in parallel...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_style = executor.submit(self.style_agent.review, state)
            future_security = executor.submit(self.security_agent.review, state)
            future_coverage = executor.submit(self.test_coverage_agent.review, state)

            # Wait for all specialists to complete
            style_findings = future_style.result()
            security_findings = future_security.result()
            coverage_findings = future_coverage.result()

        print(f"  -> Fan-out complete. Findings collected:")
        print(f"     - Style issues: {len(style_findings)}")
        print(f"     - Security threats: {len(security_findings)}")
        print(f"     - Coverage gaps: {len(coverage_findings)}")

        # Step 3: Fan-in (Aggregation and Decision by Reviewer Manager)
        print(f"\n[Phase 3] FANNING IN: Reviewer Manager aggregating, deduplicating, and ranking...")
        manager_res = self.reviewer_manager.consolidate(state)
        print(f"\n{state.consolidated_summary}")

        # Step 4: Fix-Suggestion Agent (Group of Three Requirement)
        if manager_res["ranked_findings"]:
            print(f"\n[Phase 4] Fix-Suggestion Agent generating concrete patch for top severity finding...")
            patch_res = self.fix_agent.generate_fix(state, manager_res["ranked_findings"])
            if patch_res:
                print(f"  -> Generated Patch for [{patch_res.get('rule_id')}]:\n{patch_res.get('patch')}")

        # Log trace to append-only run log
        for step in state.execution_trace:
            self.append_log(f"[{step['timestamp']}] [{step['agent']}] {step['action']}: {json.dumps(step['details'])}")
        self.append_log(f"[{state.created_at}] --- COMPLETED REVIEW FOR {pr_id}. DECISION: {state.final_decision} ---\n")

        return state
