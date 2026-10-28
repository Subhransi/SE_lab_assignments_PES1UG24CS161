# Issues Found and Fixed - movie_reviews.py

Tools: Pylint, Bandit, Flake8. Pylint score: 5.47/10 before, 10.00/10 after. Bandit: 4 issues before, 0 after. Flake8: 4 before, 0 after.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Weak MD5 hash (B324, High) | Security | 46 | `hashlib.md5` is a broken hash, flagged for security use when generating review ids | Replaced with `hashlib.sha256` (id still truncated to 10 chars) |
| Bind to all interfaces (B104, Medium) | Security | 4 | `STREAM_HOST = "0.0.0.0"` exposes the stream on every network interface | Default to `127.0.0.1`, overridable through the `STREAM_HOST` environment variable |
| Hardcoded password (B105, Low) | Security | 6 | `MODERATOR_PASSWORD = "reviews-demo"` stored in source code | Read from the `MODERATOR_PASSWORD` environment variable |
| Insecure random (B311, Low) | Security | 41 | `random.choice` is a predictable pseudo-random generator | Replaced with `secrets.choice` |
| Naming convention (C0103) | Style/Bug-risk | 11, 16, 26, 34, 39, 45, 48, 54 | camelCase function and argument names (`addMovie`, `reviewText`, ...) violate PEP 8 snake_case | Renamed all to snake_case (`add_movie`, `review_text`, ...) and updated every call |
| Missing docstrings (C0114, C0116) | Documentation | 1, 11, 16, 26, 34, 39, 45, 48, 54, 58 | Module and all functions undocumented | Added a module docstring and a docstring to every function |
| Global statement (W0603) | Design | 8, 40 | `global featured` mutated module state inside `pickFeatured`; the variable was never read elsewhere | Removed the unused global; function now simply returns the choice |
| Unnecessary else after return (R1705) | Refactor | 28-31 | `else` after `return` adds needless nesting | Removed the `else` and de-indented |
| range(len()) loop (C0200) | Refactor | 50 | Index-based loop over a list | Replaced with `enumerate` |
| Missing whitespace around operator (E225) | Style | 35 | `ranked=sorted(...)` | `ranked = sorted(...)` |
| Expected 2 blank lines (E302) | Style | 48 | Only one blank line before `printAllReviews` | Added a second blank line |
| Inline comment spacing (E261) | Style | 70 | Only one space before `# demo id` | Used two spaces before `#` |
| Missing whitespace after comma (E231) | Style | 72 | `print("Genres:",sorted(...))` | Added a space after the comma |

Additional improvement: wrapped the `main()` call in `if __name__ == "__main__":` so importing the module no longer runs the demo.

Behaviour note: output is the same except the review id (now SHA-256 based) and the streaming host (now 127.0.0.1 by default); featured movie is random by design.
