import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- score_message ----------
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_spam_word_adds_two():
    assert score_message("free", False, 0) == 2


def test_spam_word_with_punctuation_and_case():
    # "WINNER!" -> lower + strip punctuation -> "winner"
    assert score_message("WINNER!", False, 0) == 2


def test_shouting_word_adds_one():
    assert score_message("HELLO", False, 0) == 1


def test_many_links_adds_four():
    assert score_message("hello", False, 5) == 4


def test_few_links_adds_one():
    assert score_message("hello", False, 2) == 1


def test_known_sender_reduces_score():
    # 2 (free) + 2 (prize) = 4, minus 3 = 1
    assert score_message("free prize", True, 0) == 1


def test_known_sender_score_never_negative():
    assert score_message("hello", True, 0) == 0


# ---------- classify ----------
def test_low_score_is_clean():
    assert classify(1) == "clean"


def test_mid_score_is_suspicious():
    assert classify(5) == "suspicious"


def test_high_score_is_spam():
    assert classify(10) == "spam"


# ---------- filter_inbox ----------
def test_filter_inbox_counts_each_label():
    messages = [
        ("free prize winner cash urgent", False, 5),  # spam
        ("free prize", False, 0),                      # suspicious
        ("hello there", False, 0),                     # clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


# ---------- inbox_status ----------
def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


def test_inbox_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 2}) == "noisy"


def test_inbox_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 4}) == "healthy"
