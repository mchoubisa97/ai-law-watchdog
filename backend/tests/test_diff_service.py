from app.services.diff_service import is_meaningful_change, generate_diff


def test_no_change():
    text = "The regulation requires all AI systems to be audited annually."
    assert is_meaningful_change(text, text) is False


def test_small_change_is_not_meaningful():
    old = "The regulation requires all AI systems to be audited annually."
    new = "The regulation requires all AI systems to be audited annually. "
    assert is_meaningful_change(old, new) is False


def test_large_change_is_meaningful():
    old = "AI systems must be audited."
    new = "AI systems must be audited. New penalties include fines up to €30 million or 6% of global turnover, whichever is higher. Enforcement begins January 2026."
    assert is_meaningful_change(old, new) is True


def test_diff_shows_added_lines():
    old = "Line one."
    new = "Line one.\nLine two added."
    diff = generate_diff(old, new)
    assert "+Line two added." in diff


def test_diff_shows_removed_lines():
    old = "Line one.\nLine two removed."
    new = "Line one."
    diff = generate_diff(old, new)
    assert "-Line two removed." in diff