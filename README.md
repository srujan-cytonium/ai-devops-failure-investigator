# AI-Powered CI/CD Failure Investigator

An AI-assisted DevOps troubleshooting tool that analyzes CI/CD failure logs, classifies common errors, extracts supporting evidence, and generates structured Markdown investigation reports.

The tool uses Google's Gemini API for AI-assisted analysis and provides a rule-based fallback when the API key is unavailable or an AI request fails.

## Project Status

**Current stage:** Working portfolio MVP under validation.

Implemented capabilities include log processing, rule-based failure classification, secret redaction, Gemini integration, fallback analysis, Markdown report generation, automated tests, and GitHub Actions CI.

Automatic retrieval of GitHub Actions logs and automated remediation are not implemented.

## Problem

CI/CD failures often require engineers to inspect lengthy logs manually.

This project aims to reduce initial investigation effort by identifying likely failure categories, extracting relevant evidence, and organizing troubleshooting recommendations.

AI-generated diagnoses may be incorrect and must be reviewed by a human.

## Features

- **Failure classification:** Identifies common dependency, network, permission, build, test, memory, and unknown failures.
- **Log processing:** Extracts relevant error messages and surrounding context.
- **Secret redaction:** Redacts selected common credential patterns before analysis.
- **AI-assisted investigation:** Uses Google's Gemini API to generate a structured failure analysis.
- **Rule-based fallback:** Provides a basic analysis when an API key is unavailable or an AI request fails.
- **Structured reports:** Generates Markdown investigation reports with likely causes, supporting evidence, and recommendations.
- **Automated testing:** Uses Python's `unittest` framework.
- **Continuous integration:** Runs tests through GitHub Actions.

## Architecture

```text
CI/CD Failure Logs
        |
        v
Log Processing
        |
        v
Failure Classification
        |
        v
Secret Redaction
        |
        v
Gemini Analysis
        |
        +------> Rule-Based Fallback
        |         (when AI is unavailable)
        v
Structured Analysis
        |
        v
Markdown Investigation Report