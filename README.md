# commit-message-skill

Write Conventional Commits messages from a real diff — and refuse vague messages.

[![CI](https://github.com/hai02487/commit-message-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/hai02487/commit-message-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it turns a diff into a
commit message in a fixed format:

- Picks the type (`feat`, `fix`, `docs`, `style`, `refactor`,
  `perf`, `test`, `chore`, `build`, `ci`, `revert`) from what the
  diff actually does, and the scope from the paths it touches.
- Writes a subject line in the imperative mood, 72 characters or
  fewer, that a reader can check against the diff line by line.
- Adds a body only when the change needs explaining, explaining
  why — never retelling the diff.
- Flags breaking changes in a `BREAKING CHANGE` footer, never
  hidden inside the body.
- Refuses vague messages ("fix stuff", "update code", "wip") with
  the exact rule each one broke, instead of polishing them.

## What it does NOT do

- It does not commit, push, amend, or rewrite history. It writes
  the message; the user runs the commit after reading it.
- It does not invent a ticket number, an issue link, a test result,
  or a reason the diff does not show. Anything not visible in the
  diff is listed as deliberately omitted.
- It is not a release-notes writer, a changelog writer, or a code
  reviewer. Those are separate jobs.
- It does not work from a summary or a memory of the change. No
  diff, no message.

## Who it is for

Developers whose commit history is read by other people — teammates,
reviewers, future maintainers, and anyone bisecting a regression —
and who want each message to say, honestly, what changed and why.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/commit-message .agents/skills/commit-message
```

## Usage

Ask the agent to write a commit message, pasting or pointing at the
diff. The agent follows `skills/commit-message/SKILL.md` and returns
the message in a code block, any refused drafts with their reasons,
and anything deliberately omitted.

## Example

The main job, walked through on the bundled fixture in
`examples/sample-diff.diff` (two hunks: an expired-token fix in
`src/auth/tokens.py`, and a renamed public function in
`src/api/users.py`). The resulting messages are in
`examples/sample-messages.md`:

- `fix(auth): reject expired tokens instead of refreshing them` —
  the token fix, subject checkable against the diff, no body needed.
- `feat(api): rename list_users to list_customers`, with a
  `BREAKING CHANGE` footer naming the removed function and its
  replacement — because the diff removes a public function.
- Two refused drafts, each with its exact rule: "fix stuff" (no
  area, no behaviour) and "update code and improve things" (no
  subject, no scope).

The edge case the skill also covers: a mixed diff. The sample diff
touches two unrelated areas, so the skill splits it into two
commits instead of squeezing both changes into one message — the
sample messages show the split, and the test suite verifies that
both messages are present and separately well-formed.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check the skill's frontmatter and sections, scan the
skill and README for unfinished markers and filler text, and walk
the skill through the bundled fixtures: they re-parse the sample
diff, confirm the two changed paths, confirm the sample messages
match the Conventional Commits format with the right types and
scopes, confirm the breaking-change footer is present, and confirm
both vague drafts are refused with a reason.

## Contributing

Small, focused improvements are welcome. Open an issue first for
anything larger than a typo, so the scope can be agreed before work
starts. Never weaken the safety rules: a message must be traceable
to a line in the diff, a check that was not run must not be claimed,
and nothing is committed, amended, or pushed by the skill.

## Licence

MIT — see [LICENSE](LICENSE). This is original work, written for
this repo; it builds on the public Conventional Commits format
(type, scope, subject, body, footer), which is documented in the
skill itself.
