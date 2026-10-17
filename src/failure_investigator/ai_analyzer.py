import json


def analyze_failure(log_text: str, category: str, api_key: str = None) -> dict:
    """
    Analyze CI/CD failures.
    Uses a local fallback when no AI API key is configured.
    """
    if not api_key:
        return {
            "analysis_mode": "rule_based_fallback",
            "category": category,
            "summary": f"A CI/CD failure was classified as: {category}.",
            "likely_cause": _fallback_cause(category),
            "evidence": [
                line.strip()
                for line in log_text.splitlines()
                if any(word in line.lower() for word in
                       ["error", "failed", "exception", "denied", "timeout"])
            ][:5],
            "recommendations": _fallback_recommendations(category),
            "requires_human_review": True,
        }

    # Real AI integration will be added when an API key is available.
    raise NotImplementedError(
        "AI integration is not configured yet. "
        "Add an API key to enable real LLM analysis."
    )


def _fallback_cause(category: str) -> str:
    causes = {
        "dependency": "A required package or module may be missing.",
        "permissions": "The process may lack permission to access a resource.",
        "network": "A connection may have timed out or been refused.",
        "memory": "The process may have exceeded available memory.",
        "test": "A test assertion or expected behavior may have failed.",
        "build": "The application may have a compilation or build error.",
        "unknown": "The available log evidence is insufficient to identify a cause.",
    }
    return causes.get(category, causes["unknown"])


def _fallback_recommendations(category: str) -> list[str]:
    recommendations = {
        "dependency": [
            "Check the dependency manifest and lockfile.",
            "Verify that dependencies are installed in the CI environment.",
        ],
        "permissions": [
            "Verify file and directory permissions.",
            "Review the CI job's access permissions.",
        ],
        "network": [
            "Verify the destination hostname and port.",
            "Check network connectivity and service availability.",
        ],
        "memory": [
            "Review memory usage and resource limits.",
            "Inspect the process for excessive memory consumption.",
        ],
        "test": [
            "Inspect the failing test and its assertion.",
            "Reproduce the failure in a local test environment.",
        ],
        "build": [
            "Review the compiler or build error.",
            "Verify the build configuration and dependencies.",
        ],
        "unknown": [
            "Inspect the complete logs for additional context.",
            "Collect more diagnostic evidence before taking action.",
        ],
    }
    return recommendations.get(category, recommendations["unknown"])
