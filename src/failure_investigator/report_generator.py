from datetime import datetime, timezone


def generate_report(analysis: dict) -> str:
    evidence = analysis.get("evidence", [])
    recommendations = analysis.get("recommendations", [])

    evidence_text = "\n".join(
        f"- `{line}`" for line in evidence
    ) or "- No matching evidence extracted."

    recommendations_text = "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(recommendations, 1)
    ) or "No recommendations available."

    return f"""# CI/CD Failure Investigation Report

**Generated:** {datetime.now(timezone.utc).isoformat()}
**Category:** {analysis.get('category', 'unknown')}
**Analysis mode:** {analysis.get('analysis_mode', 'unknown')}
**Human review required:** Yes

## Summary
{analysis.get('summary', 'No summary available.')}

## Likely Cause
{analysis.get('likely_cause', 'Insufficient evidence.')}

## Supporting Evidence
{evidence_text}

## Recommended Investigation
{recommendations_text}

> This report contains diagnostic suggestions, not a verified root cause.
> Validate the evidence before making changes.
"""
