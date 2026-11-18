"""
test_scenarios.py - Automated Test Suite covering at least 3 required scenarios.
Scenario 1: Critical Security Vulnerability (Hardcoded secret + eval) -> Expect REQUEST_CHANGES + Patch.
Scenario 2: Style & Coverage Violations (Missing tests + camelCase) -> Expect Warning/Advisory.
Scenario 3: Clean, Perfect Code Change -> Expect clean APPROVE.
"""
import unittest
from orchestrator import CodeReviewOrchestrator

# Sample Diffs for Testing
DIFF_SCENARIO_1_SECURITY_BREACH = """diff --git a/auth/auth_service.py b/auth/auth_service.py
index 0000000..1111111 100644
--- a/auth/auth_service.py
+++ b/auth/auth_service.py
@@ -0,0 +1,8 @@
+import os
+
+api_key = "AKIA1234567890ABCDEF"
+
+def authenticate_user(raw_payload):
+    # Dangerous dynamic code execution
+    user_dict = eval(raw_payload)
+    return user_dict
"""

DIFF_SCENARIO_2_STYLE_AND_COVERAGE = """diff --git a/services/payment_calculator.py b/services/payment_calculator.py
index 0000000..2222222 100644
--- a/services/payment_calculator.py
+++ b/services/payment_calculator.py
@@ -0,0 +1,6 @@
+def CalculateDiscount(priceAmount, rate):
+    print("Calculating discount for amount...")
+    finalPrice = priceAmount - (priceAmount * rate)
+    return finalPrice
"""

DIFF_SCENARIO_3_CLEAN_APPROVED = """diff --git a/math_utils.py b/math_utils.py
index 0000000..3333333 100644
--- a/math_utils.py
+++ b/math_utils.py
@@ -0,0 +1,5 @@
+def add_numbers(a: int, b: int) -> int:
+    return a + b
diff --git a/test_math_utils.py b/test_math_utils.py
index 0000000..4444444 100644
--- a/test_math_utils.py
+++ b/test_math_utils.py
@@ -0,0 +1,6 @@
+import unittest
+from math_utils import add_numbers
+
+class TestMath(unittest.TestCase):
+    def test_add(self):
+        self.assertEqual(add_numbers(2, 3), 5)
"""

class TestCodeReviewBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.orchestrator = CodeReviewOrchestrator(log_file="test_run.log")

    def test_scenario_1_security_failure(self):
        print("\n" + "="*70)
        print("RUNNING SCENARIO 1: CRITICAL SECURITY & DANGEROUS CODE")
        print("="*70)
        state = self.orchestrator.run_review(
            raw_diff=DIFF_SCENARIO_1_SECURITY_BREACH,
            pr_id="PR-001-SECURITY-FAIL",
            author="junior_dev"
        )
        self.assertEqual(state.final_decision, "REQUEST_CHANGES")
        severities = [f.severity.value for f in state.findings]
        self.assertIn("CRITICAL", severities)
        self.assertTrue(len(state.fix_suggestions) > 0, "Fix-Suggestion Agent should generate a patch")
        print("[SUCCESS] Scenario 1 passed: Blocked merge and generated patch as expected.")

    def test_scenario_2_style_and_coverage(self):
        print("\n" + "="*70)
        print("RUNNING SCENARIO 2: STYLE ISSUES AND MISSING TEST COVERAGE")
        print("="*70)
        state = self.orchestrator.run_review(
            raw_diff=DIFF_SCENARIO_2_STYLE_AND_COVERAGE,
            pr_id="PR-002-STYLE-TESTS",
            author="contractor"
        )
        # Should flag style issues (PEP8) and missing test file
        rules = [f.rule_id for f in state.findings]
        self.assertTrue(any("PEP8" in r for r in rules))
        self.assertIn("TEST-MISSING-PAIR", rules)
        print("[SUCCESS] Scenario 2 passed: Successfully identified style non-compliance and missing tests.")

    def test_scenario_3_clean_merge(self):
        print("\n" + "="*70)
        print("RUNNING SCENARIO 3: CLEAN CODE WITH UNIT TESTS")
        print("="*70)
        state = self.orchestrator.run_review(
            raw_diff=DIFF_SCENARIO_3_CLEAN_APPROVED,
            pr_id="PR-003-CLEAN-PASS",
            author="lead_engineer"
        )
        self.assertEqual(state.final_decision, "APPROVE")
        self.assertEqual(len(state.findings), 0)
        print("[SUCCESS] Scenario 3 passed: Clean PR approved without friction.")

if __name__ == "__main__":
    unittest.main()
