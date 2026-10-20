import unittest
from pathlib import Path
from unittest.mock import patch

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
        log = (
            "api_key=supersecret123 "
            "password=MyPassword123 "
            "Bearer eyJhbGciOiJIUzI1NiJ9 "
            "ghp_abcdefghijklmnopqrstuvwxyz123456"
        )

        result = redact_secrets(log)

        self.assertNotIn("supersecret123", result)
        self.assertNotIn("MyPassword123", result)
        self.assertNotIn("eyJhbGciOiJIUzI1NiJ9", result)
        self.assertNotIn(
            "ghp_abcdefghijklmnopqrstuvwxyz123456",
            result
        )
        self.assertIn("[REDACTED]", result)

    def test_fallback_analysis_does_not_expose_secrets(self):
        log = (
            "ERROR: Database connection failed "
            "api_key=supersecret123 "
            "password=MyPassword123"
        )

        with patch.dict("os.environ", {"GEMINI_API_KEY": ""}):
            analysis = analyze_failure(log, "database", api_key="")

        evidence = str(analysis.get("evidence", []))

        self.assertEqual(
            analysis["analysis_mode"],
            "rule_based_fallback"
        )
        self.assertNotIn("supersecret123", evidence)
        self.assertNotIn("MyPassword123", evidence)

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


    @patch("failure_investigator.ai_analyzer.genai.Client")
    def test_gemini_receives_redacted_logs(self, mock_client_class):
        mock_client = mock_client_class.return_value
        mock_client.models.generate_content.return_value.text = (
            '{"summary": "Database failure", '
            '"likely_cause": "Connection timeout", '
            '"evidence": ["ERROR: Database connection failed"], '
            '"recommendations": ["Check database connectivity"], '
            '"requires_human_review": true}'
        )

        log = (
            "ERROR: Database connection failed "
            "api_key=supersecret123 "
            "password=MyPassword123"
        )

        analyze_failure(log, "database", api_key="test-api-key")

        call_args = mock_client.models.generate_content.call_args
        prompt = call_args.kwargs["contents"]

        self.assertNotIn("supersecret123", prompt)
        self.assertNotIn("MyPassword123", prompt)
        self.assertIn("[REDACTED]", prompt)


if __name__ == "__main__":
    unittest.main()