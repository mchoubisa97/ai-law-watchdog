import difflib


def generate_diff(old_text: str, new_text: str, context_lines: int = 3) -> str:
    """Generate a unified diff between two text strings."""
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        lineterm="",
        n=context_lines,
    )
    return "\n".join(diff)


def is_meaningful_change(old_text: str, new_text: str, threshold: int = 50) -> bool:
    """
    Check if the change between two texts is meaningful.
    Uses both character-count delta AND line-level similarity ratio.
    Rejects changes that are purely whitespace/formatting.
    """
    # 1. Strip and compare — ignore pure whitespace changes
    if old_text.strip() == new_text.strip():
        return False

    # 2. Character delta threshold
    char_delta = abs(len(new_text) - len(old_text))
    if char_delta >= threshold:
        return True

    # 3. Sequence similarity — flag if content diverged meaningfully
    ratio = difflib.SequenceMatcher(None, old_text, new_text).ratio()
    return ratio < 0.98
