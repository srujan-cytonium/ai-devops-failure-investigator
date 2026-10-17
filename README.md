# AI-Powered DevOps Failure Investigator

An AI-assisted CI/CD troubleshooting tool that analyzes pipeline logs, classifies common failures, extracts evidence, and generates structured investigation reports.

> **Status:** Core log processing, rule-based classification, basic secret redaction, Markdown report generation, and automated tests are implemented. Real LLM integration and automatic GitHub log retrieval are planned.

## Problem

CI/CD failures require engineers to inspect logs manually. This project aims to reduce initial investigation effort by extracting relevant evidence and organizing troubleshooting recommendations.

## Architecture

```text
CI/CD Logs
    |
    v
Log Processor
    |
    v
Failure Classifier
    |
    v
Secret Redaction
    |
    v
Analysis Engine
    |
    v
Markdown Incident Report
Implemented Features

* Extract error messages and surrounding log context.
* Classify common dependency, network, permission, build, test, and memory failures.
* Redact selected common secret patterns.
* Generate structured Markdown incident reports.
* Run automated unit tests.
* Automatically test code through GitHub Actions.

Technology Stack

* Python
* GitHub Actions
* Git
* Google GenAI SDK installed; real AI integration pending.

Requirements

* Python 3.9+
* Git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m unittest discover -s tests -v
Generate an Example Report
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from failure_investigator.classifier import classify_failure
from failure_investigator.security import redact_secrets
from failure_investigator.ai_analyzer import analyze_failure
from failure_investigator.report_generator import generate_report

logs = Path("sample-logs/database-timeout.log").read_text()
safe_logs = redact_secrets(logs)
category = classify_failure(safe_logs)
analysis = analyze_failure(safe_logs, category)

report = generate_report(analysis)
Path("incident-report.md").write_text(report)
print(report)
PY
Security

* Basic pattern-based secret redaction is implemented.
* Recommendations require human verification.
* The tool does not execute remediation commands.
* Redaction cannot guarantee detection of every secret.

Limitations

* Real LLM integration is not yet implemented.
* Logs are currently provided as local files.
* Classification relies on predefined patterns.
* Production readiness has not been established.

Production Roadmap

1. Integrate a real LLM provider with structured output validation.
2. Retrieve failed workflow logs through the GitHub API.
3. Publish reports to GitHub Actions summaries or pull requests.
4. Improve secret detection and log processing.
5. Evaluate diagnosis quality against a larger test dataset.
6. Add monitoring, access controls, and audit logging.
7. Introduce controlled remediation with policy checks and human approval.

Project Status

This project demonstrates DevOps troubleshooting, Python automation, CI/CD integration, and AI-assisted incident analysis.

Future capabilities are documented as planned enhancements, not implemented features.
