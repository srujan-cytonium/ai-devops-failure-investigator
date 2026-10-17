import re

FAILURE_RULES = [
    ("dependency", [r"ModuleNotFoundError", r"No module named", r"package not found"]),
    ("permissions", [r"Permission denied", r"AccessDenied", r"403 Forbidden"]),
    ("network", [r"Connection timed out", r"Connection refused", r"Name or service not known"]),
    ("memory", [r"OutOfMemoryError", r"OOMKilled", r"out of memory"]),
    ("test", [r"AssertionError", r"FAILED", r"test.*failed"]),
    ("build", [r"Compilation failed", r"Build failed", r"SyntaxError"]),
]

def classify_failure(log_text: str) -> str:
    """Classify a failure using deterministic rules."""
    for category, patterns in FAILURE_RULES:
        for pattern in patterns:
            if re.search(pattern, log_text, re.IGNORECASE):
                return category

    return "unknown"
