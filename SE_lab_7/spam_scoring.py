import re

# A link starts with http:// or https:// and runs until the next whitespace
_LINK_RE = re.compile(r"https?://\S+", re.IGNORECASE)


def sender_domain(email):
    """Return the lowercase domain of a sender email, or None if it is invalid."""
    if not isinstance(email, str):
        return None
    email = email.strip()
    if email.count('@') != 1 or any(c.isspace() for c in email):
        return None
    user, domain = email.split('@')
    if not user or not domain:
        return None
    return domain.lower()


def first_link(text):
    """Return the first http(s) link in text, or None if there is none."""
    if not isinstance(text, str):
        return None
    match = _LINK_RE.search(text)
    return match.group(0) if match else None


def shout_ratio(text):
    """Return the fraction of letters that are uppercase (0.0 if no letters)."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = [c for c in letters if c.isupper()]
    return len(upper) / len(letters)


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result if result is not None else "Invalid sender email")

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result if result is not None else "No link found")

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()