import string

from hypothesis import example, given, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio

# Values a caller might wrongly pass in: text, None, numbers, lists
anything = st.one_of(st.text(), st.none(), st.integers(), st.floats(), st.lists(st.text()))
word = st.text(alphabet=string.ascii_letters + string.digits, min_size=1, max_size=10)


# ======================= 1. sender_domain =======================
@given(st.text() | st.none())
@example(None)
@example("")
@example("nobody")
@example("@")
def test_sender_domain_no_crash(s):
    try:
        sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {e!r}"


@given(anything)
def test_sender_domain_returns_clean_value(s):
    # Result is either None (invalid) or a non-empty, lowercase string with no '@' or whitespace
    result = sender_domain(s)
    assert result is None or isinstance(result, str)
    if result is not None:
        assert result != ""
        assert result == result.lower()
        assert "@" not in result
        assert not any(c.isspace() for c in result)


@given(word, word)
def test_sender_domain_valid_email_gives_lowercase_domain(user, domain):
    assert sender_domain(f"{user}@{domain}.com") == f"{domain}.com".lower()


@given(word)
@example("a")
def test_sender_domain_rejects_missing_parts(x):
    assert sender_domain(x) is None            # no '@'
    assert sender_domain(f"{x}@") is None      # no domain
    assert sender_domain(f"@{x}.com") is None  # no user
    assert sender_domain(f"{x}@{x}@{x}.com") is None  # two '@'


# ========================= 2. first_link ========================
@given(st.text() | st.none())
@example(None)
@example("")
@example("no link here")
def test_first_link_no_crash(s):
    try:
        first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {e!r}"


@given(anything)
def test_first_link_returns_clean_value(s):
    # Result is None or a link that really appears in the text and has no whitespace
    result = first_link(s)
    assert result is None or isinstance(result, str)
    if result is not None:
        assert result.lower().startswith(("http://", "https://"))
        assert not any(c.isspace() for c in result)
        assert result in s


@given(st.text(alphabet=string.ascii_letters + " ").filter(lambda t: "http" not in t.lower()))
@example("nothttp is a word")
@example("see http")
def test_first_link_text_without_a_link_gives_none(s):
    assert first_link(s) is None


@given(word, word)
def test_first_link_finds_link_and_stops_at_whitespace(path, after):
    link = f"https://example.com/{path}"
    assert first_link(f"click {link}\n{after}") == link
    assert first_link(f"click {link} {after}") == link


# ========================= 3. shout_ratio =======================
@given(st.text() | st.none())
@example(None)
@example("")
@example("123")
def test_shout_ratio_no_crash(s):
    try:
        shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {e!r}"


@given(anything)
def test_shout_ratio_is_between_0_and_1(s):
    result = shout_ratio(s)
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


@given(st.text(alphabet=string.digits + string.punctuation + " "))
def test_shout_ratio_text_without_letters_is_zero(s):
    assert shout_ratio(s) == 0.0


@given(st.text(alphabet=string.ascii_uppercase, min_size=1))
def test_shout_ratio_all_caps_is_one(s):
    assert shout_ratio(s) == 1.0


@given(st.text(alphabet=string.ascii_lowercase, min_size=1))
def test_shout_ratio_all_lowercase_is_zero(s):
    assert shout_ratio(s) == 0.0


# ================= known-good examples (sanity) ================
def test_known_examples():
    assert sender_domain("offers@Deals.com") == "deals.com"
    assert first_link("visit http://a.com now") == "http://a.com"
    assert shout_ratio("FREE prize NOW") == 7 / 12