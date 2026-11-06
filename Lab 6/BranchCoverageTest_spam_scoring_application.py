import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- score_message: loop (zero / one / many iterations) ----------
def test_empty_text_loop_never_runs():
    assert score_message("", False, 0) == 0


def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


# ---------- spam-word branch: True / False ----------
def test_spam_word_true_branch():
    assert score_message("free", False, 0) == 2


def test_spam_word_with_punctuation_and_case():
    assert score_message("WINNER!", False, 0) == 2


def test_all_spam_words_recognised():
    assert score_message("free winner prize urgent cash", False, 0) == 10


# ---------- elif branch (shouting word): True / False ----------
def test_shouting_word_true_branch():
    assert score_message("HELLO", False, 0) == 1


def test_uppercase_but_too_short_false_branch():
    # isupper() True but len == 3 -> not counted
    assert score_message("HEY", False, 0) == 0


def test_long_word_but_not_uppercase_false_branch():
    assert score_message("Hello", False, 0) == 0


def test_uppercase_boundary_length_four():
    # len == 4 is just above the > 3 boundary
    assert score_message("ABCD", False, 0) == 1


# ---------- link_count branches: >3 / >0 / 0 ----------
def test_links_greater_than_three():
    assert score_message("hello", False, 4) == 4


def test_links_exactly_three_uses_elif():
    assert score_message("hello", False, 3) == 1


def test_links_exactly_one():
    assert score_message("hello", False, 1) == 1


def test_links_zero_skips_both():
    assert score_message("hello", False, 0) == 0


# ---------- sender_known branch + inner "score < 0" branch ----------
def test_unknown_sender_no_reduction():
    assert score_message("free prize", False, 0) == 4


def test_known_sender_score_stays_positive():
    # 4 - 3 = 1 -> inner if False
    assert score_message("free prize", True, 0) == 1


def test_known_sender_score_clamped_to_zero():
    # 0 - 3 = -3 -> inner if True -> clamped
    assert score_message("hello", True, 0) == 0


def test_known_sender_score_exactly_zero_not_clamped():
    # 3 - 3 = 0 -> inner if False (0 < 0 is False)
    assert score_message("free HELLO", True, 0) == 0


# ---------- classify boundaries ----------
def test_classify_clean_low():
    assert classify(0) == "clean"


def test_classify_clean_upper_boundary():
    assert classify(3) == "clean"


def test_classify_suspicious_lower_boundary():
    assert classify(4) == "suspicious"


def test_classify_suspicious_upper_boundary():
    assert classify(7) == "suspicious"


def test_classify_spam_lower_boundary():
    assert classify(8) == "spam"


def test_classify_spam_high():
    assert classify(20) == "spam"


# ---------- filter_inbox ----------
def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_filter_inbox_single_message():
    assert filter_inbox([("hello", False, 0)]) == {"spam": 0, "suspicious": 0, "clean": 1}


def test_filter_inbox_counts_each_label():
    messages = [
        ("free prize winner cash urgent", False, 5),  # spam
        ("free prize", False, 0),                      # suspicious
        ("hello there", False, 0),                     # clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


# ---------- inbox_status: total==0 / ratio thresholds ----------
def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


def test_inbox_status_exactly_half_is_noisy():
    # ratio == 0.5 -> not > 0.5, but > 0.2
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"


def test_inbox_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 2}) == "noisy"


def test_inbox_status_exactly_point_two_is_healthy():
    # ratio == 0.2 -> not > 0.2
    assert inbox_status({"spam": 1, "suspicious": 2, "clean": 2}) == "healthy"


def test_inbox_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 4}) == "healthy"
