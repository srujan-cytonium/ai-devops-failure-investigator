import re

ERROR_PATTERNS = [
    r"\bERROR\b",
    r"\bCRITICAL\b",
    r"\bFATAL\b",
    r"\bException\b",
    r"\bTraceback\b",
    r"\bFAILED\b",
    r"\bFAILURE\b",
    r"\bPermission denied\b",
    r"\bConnection timed out\b",
    r"\bModuleNotFoundError\b",
    r"\bOutOfMemoryError\b",
]

def extract_relevant_logs(log_text: str, context_lines: int = 2) -> list[str]:
    """Extract error lines and nearby context from CI/CD logs."""
    lines = log_text.splitlines()
    relevant_indices = set()

    for index, line in enumerate(lines):
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in ERROR_PATTERNS):
            start = max(0, index - context_lines)
            end = min(len(lines), index + context_lines + 1)
            relevant_indices.update(range(start, end))

    return [lines[index] for index in sorted(relevant_indices)]
