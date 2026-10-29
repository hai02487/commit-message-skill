"""Validation + fixture walkthrough tests for the commit-message skill.

Run: python3 tests/test_skill.py
No third-party dependencies. Parses the bundled fixture diff in
examples/sample-diff.diff and checks the sample messages against
it, so the walkthrough is verified, not just the skill's headings.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "commit-message" / "SKILL.md"
README = ROOT / "README.md"
DIFF = ROOT / "examples" / "sample-diff.diff"
MESSAGES = ROOT / "examples" / "sample-messages.md"

# type(scope): subject — subject 72 chars or fewer, no trailing stop.
CONVENTIONAL = re.compile(
    r"^([a-z]+)\(([a-z]+)\): ([A-Z]?[a-z0-9][^.\n]{0,68})$")


def _text(path):
    return path.read_text(encoding="utf-8")


def test_skill_frontmatter():
    text = _text(SKILL)
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    frontmatter = text.split("---", 2)[1]
    assert re.search(r"^name:\s*commit-message\s*$", frontmatter, re.M) is not None
    assert re.search(r"^description:\s*.+", frontmatter, re.M) is not None


def test_skill_sections():
    text = _text(SKILL)
    for heading in ("When to use this skill", "When NOT to use it",
                    "Workflow", "Output rules", "Limits and safety rules"):
        assert heading in text, f"missing section: {heading}"
    for rule in ("BREAKING CHANGE", "72 characters", "git commit"):
        assert rule in text, f"missing rule: {rule}"
    assert "never invent" in text.lower(), "missing rule: never invent"


def test_no_placeholders():
    for path in (SKILL, README):
        lower = _text(path).lower()
        for word in ("todo", "lorem"):
            assert word not in lower, f"{path.name} contains placeholder: {word}"
    assert "coming soon" not in _text(README).lower()


def test_readme_sections():
    text = _text(README)
    for heading in ("What it does", "What it does NOT do", "Install",
                    "Usage", "Example", "How it is tested", "Licence"):
        assert heading in text, f"README missing section: {heading}"


def test_diff_paths_and_split():
    diff = _text(DIFF)
    paths = re.findall(r"^diff --git a/(\S+) b/\S+", diff, re.M)
    assert paths == ["src/auth/tokens.py", "src/api/users.py"], \
        f"diff should touch auth + api paths, got {paths}"
    assert "-        return refresh(token)" in diff
    assert "+        return False" in diff
    assert "-def list_users" in diff and "+def list_customers" in diff


def test_sample_messages_conventional():
    messages = _text(MESSAGES)
    subjects = re.findall(r"^```\n([a-z]+\([a-z]+\): .+?)\n", messages, re.M)
    # The two commit subjects, each in its own code block.
    assert "fix(auth): reject expired tokens instead of refreshing them" in subjects
    assert "feat(api): rename list_users to list_customers" in subjects
    for subject in subjects:
        assert CONVENTIONAL.match(subject), f"not conventional: {subject}"
        assert len(subject) <= 72, f"subject over 72 chars: {subject}"
    assert "BREAKING CHANGE: list_users is removed" in messages
    assert "list_customers" in messages


def test_refusals_and_omissions():
    messages = _text(MESSAGES)
    for draft in ("fix stuff", "update code and improve things"):
        assert draft in messages, f"refused draft missing: {draft}"
    assert "Refused drafts" in messages
    assert "Deliberately omitted" in messages
    assert "Ticket or issue number" in messages
    assert "Test result" in messages


def main():
    tests = [test_skill_frontmatter, test_skill_sections,
             test_no_placeholders, test_readme_sections,
             test_diff_paths_and_split, test_sample_messages_conventional,
             test_refusals_and_omissions]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"All {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
