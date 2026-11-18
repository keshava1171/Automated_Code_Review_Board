# Automated Code Review Board (Project Q14) - README

**Course:** CSE476 - Agentic AI and Intelligent Automation  
**Academic Task:** CA2 (30 Marks) | **Section:** K2E2330 G-1 & G-2  
**Architecture:** Fan-Out / Fan-In with Reviewer Manager  
**Framework:** Microsoft Semantic Kernel (Python)

---

## 1. Agent Roster & Architecture Justification

The system reviews incoming code changes (pull request diffs), runs concurrent multi-perspective audits, and consolidates findings into an actionable merge verdict.

```
       [ Incoming Git Diff ]
                 │
                 ▼
          [ Diff Agent ]
                 │
      ┌──────────┼──────────┐ (Fan-out Concurrent Execution)
      ▼          ▼          ▼
[Style Agent] [Security] [Test-Coverage]
      └──────────┬──────────┘ (Fan-in Aggregation)
                 │
                 ▼
       [Reviewer Manager]  ──> Verdict: APPROVE / REQUEST_CHANGES
                 │
                 ▼ (Group of 3 Extension)
     [Fix-Suggestion Agent] ──> Concrete Replacement Patch
```

### Why Fan-Out / Fan-In Fits:
Code review consists of **independent dimensions** (style, vulnerability scanning, unit-test verification) that do not depend on each other's intermediate outputs. Fanning out to three specialist workers concurrently optimizes throughput. Fanning in to a central **Reviewer Manager** enables deduplication, cross-signal ranking by severity (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW`), and enterprise-level merge decisions.

---

## 2. Agent Modules & Tools (2 Tools Per Agent)

1. **Diff Agent (`diff_agent.py`)**:
   * *Tool 1: `parse_git_diff`*: Extracts modified file paths, line numbers, added and removed lines from git patches.
   * *Tool 2: `extract_touched_components`*: Utilizes Python Abstract Syntax Trees (AST) to identify declared classes and functions.
2. **Style Agent (`style_agent.py`)**:
   * *Tool 1: `inspect_naming_conventions`*: Enforces PEP8 standards (snake_case functions/variables, PascalCase classes).
   * *Tool 2: `check_formatting_and_comments`*: Detects lines $>100$ characters and raw `print()` statements.
3. **Security Agent (`security_agent.py`)**:
   * *Tool 1: `scan_hardcoded_secrets`*: Detects exposed AWS keys, GitHub PATs, and generic API keys.
   * *Tool 2: `scan_vulnerable_execution_patterns`*: Detects SQL injection, `eval()`, `exec()`, and `shell=True`.
4. **Test-Coverage Agent (`test_coverage_agent.py`)**:
   * *Tool 1: `verify_test_file_pairing`*: Verifies if corresponding unit test files were touched alongside source files.
   * *Tool 2: `inspect_assertion_quality`*: Audits test files to ensure they contain non-empty assertion statements.
5. **Reviewer Manager (`reviewer_manager.py`)**:
   * *Tool 1: `deduplicate_and_rank_findings`*: Removes overlapping findings and sorts them by strict severity priority.
   * *Tool 2: `evaluate_merge_policy`*: Applies gate criteria (blocks merge if any `CRITICAL` or `HIGH` findings exist).
6. **Fix-Suggestion Agent (`fix_suggestion_agent.py`) [Group of 3 Extension]**:
   * *Tool 1: `extract_top_finding`*: Selects the highest-severity issue from the ranked board.
   * *Tool 2: `synthesize_patch`*: Emits a unified git replacement patch to automatically resolve the issue.

---

## 3. Shared State & Failure Handling

* **Shared State (`models.py`)**: Carries `raw_diff`, `files_touched`, `findings`, `final_decision`, and `execution_trace`.
* **Failure Handled Gracefully**:
  * **Malformed/Unparseable Code Snippet**: When incomplete or malformed code diffs enter AST inspection, the system catches syntax parsing exceptions and automatically falls back to regex-based static scanning, logging the warning without crashing the pipeline.
  * **Missing Tests**: When a developer submits source modifications without unit tests, the system flags `TEST-MISSING-PAIR` as a Medium advisory, preventing silent untested deployments.

---

## 4. How to Run
```bash
# Run the test suite (3 mandatory test scenarios)
python test_scenarios.py

# Run the CLI interactive review
python main.py
```
