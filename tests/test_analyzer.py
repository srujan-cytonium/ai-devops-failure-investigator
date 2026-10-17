import unittest

from pathlib import Path

from failure_investigator.classifier import classify_failure
from failure_investigator.log_processor import extract_relevant_logs
from failure_investigator.security import redact_secrets
from failure_investigator.ai_analyzer import analyze_failure
from failure_investigator.report_generator import generate_report


class TestFailureInvestigator(unittest.TestCase):

    def test_dependency_failure(self):
        self.assertEqual(
            classify_failure("ModuleNotFoundError: requests"),
            "dependency"
        )

    def test_network_failure(self):
        self.assertEqual(
            classify_failure("ERROR: Connection timed out"),
            "network"
        )

    def test_permission_failure(self):
        self.assertEqual(
            classify_failure("ERROR: Permission denied"),
            "permissions"
        )

    def test_unknown_failure(self):
        self.assertEqual(
            classify_failure("INFO: Everything is running"),
            "unknown"
        )

    def test_extract_error_evidence(self):
        log = "INFO: Start\nERROR: Failed\nINFO: Shutdown"
        result = extract_relevant_logs(log, context_lines=1)
        self.assertEqual(len(result), 3)

    def test_secret_redaction(self):
        result = redact_secrets("api_key=supersecret123")
        self.assertNotIn("supersecret123", result)

    def test_analysis_and_report(self):
        log = "ERROR: Connection timed out"
        category = classify_failure(log)
        analysis = analyze_failure(log, category)
        report = generate_report(analysis)

        self.assertIn("Likely Cause", report)
        self.assertIn("Supporting Evidence", report)
        self.assertIn("Recommended Investigation", report)

    def test_sample_logs_exist(self):
        self.assertTrue(
            Path("sample-logs/database-timeout.log").exists()
        )


if __name__ == "__main__":
    unittest.main()
