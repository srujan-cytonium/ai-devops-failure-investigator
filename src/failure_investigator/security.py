import re

SECRET_PATTERNS = [
    # API keys, tokens, and passwords assigned using common formats
    (
        re.compile(
            r"""(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)\b"""
            r"""(\s*[:=]\s*)["']?([^\s"'&,;]+)"""
        ),
        r"\1\2[REDACTED]",
    ),
    # Bearer authentication tokens
    (
        re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
        "Bearer [REDACTED]",
    ),
    # Common GitHub personal access token formats
    (
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
        "[REDACTED_GITHUB_TOKEN]",
    ),
]


def redact_secrets(text: str) -> str:
    """Redact common secret patterns before log analysis."""
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)

    return text
