---
name: commit-message
description: Write a Conventional Commits message from a real diff. Use when a user asks to write, fix, or review a commit message, or to turn a set of changes into a clear commit. Works from the actual diff and the files it touches, never from a vague summary, and refuses messages that say nothing.
---

# commit-message

Write a commit message a stranger can trust: what changed, why, and
whether anything breaks — derived from the diff itself.

## When to use this skill

Use it when the user asks to:
- Write a commit message for changes they have already made.
- Fix a vague commit message ("fixed stuff", "updates", "wip") into one
  that says what actually changed.
- Review a commit message against the diff it describes.
- Split one large set of changes into separate, honest commits.

## When NOT to use it

- Do not use it to describe changes you have not seen. Read the diff
  first; a summary from memory is not a diff.
- Do not use it as a release-notes writer, a changelog writer, or a
  code reviewer. Those are separate jobs with their own rules.
- Do not use it to commit anything by itself. This skill writes the
  message; the user runs the commit, after reading the message.
- Do not use it to invent a reason for a change. If the diff does not
  show why, say so and ask — do not fill the gap with a guess.

## Workflow

### 1. Read the real diff, in this order
1. List every file the diff touches, with added and removed lines.
2. Group the changes by what they do, not by which file they sit in.
   One behaviour change is one commit; a mixed diff is split, not
   summarised into one blurry message.
3. Note anything the diff alone cannot explain: a ticket number, a
   user-visible reason, a test result. Those stay out of the message
   unless the user supplies them.

### 2. Pick the type and the scope from the diff
Types, and what each one means:
- `feat` — a new user-facing capability.
- `fix` — a bug fix for existing behaviour.
- `docs` — documentation only.
- `style` — formatting only; no behaviour change.
- `refactor` — code restructured with no behaviour change.
- `perf` — a performance improvement.
- `test` — tests only.
- `chore` — build, tooling, or maintenance with no product change.
- `build` — build system or dependency changes.
- `ci` — continuous-integration configuration only.
- `revert` — undoing an earlier commit (name that commit).

Scope is the area the diff actually touches, in one lowercase word
taken from the changed paths: `auth` for `src/auth/`, `billing` for
`src/billing/`, `docs` for documentation files. If the diff spans
several unrelated areas, that is a sign it should be split, not a
reason to drop the scope.

### 3. Write the subject line
Format: `type(scope): subject`, all lowercase except proper nouns,
no trailing full stop, 72 characters or fewer.

The subject must name the change in the imperative mood ("add",
"fix", "remove", "raise") and must be checkable against the diff:
a reader with the diff in front of them should be able to point at
the lines that prove the subject true. Subjects that fail this test
— "fix stuff", "update code", "various changes", "wip" — are
refused, with the exact reason, not rewritten into a prettier
version of the same vagueness.

### 4. Add a body only when the diff needs explaining
A body is two to four lines, and it explains *why* the change was
made and *what it changes for the reader*, never a line-by-line
retelling of the diff (the diff already shows that). Leave the body
out entirely when the subject plus the diff is already clear — a
one-line typo fix needs no body.

### 5. Flag breaking changes in the footer, never in passing
A change is breaking when it removes or renames a public function,
changes a file format, drops a supported option, or changes
behaviour a caller depends on. Mark it exactly like this:

```
BREAKING CHANGE: <what breaks and what the caller must do instead>
```

A breaking change is never hidden inside the body, and a
non-breaking change never carries the flag. If the diff might break
something but you cannot tell from the diff alone, say that plainly
and ask the user — do not guess either way.

### 6. Report in this fixed format
1. The message, in a code block, ready to paste.
2. One line per refused draft, if any, naming the draft and the
   exact rule it broke.
3. Anything the message deliberately leaves out (a ticket number,
   a test result, a reason not visible in the diff), listed by name,
   with why it was left out.

## Good examples

A bug fix, scope taken from the changed path:

```
fix(auth): reject expired tokens instead of refreshing them
```

A new feature with a body that explains why:

```
feat(billing): add monthly usage summary to the invoice page

Customers asked for a single place to see what they used before
paying. The summary reads the same usage records the invoice
already totals, so the two can never disagree.
```

A breaking change, flagged in the footer:

```
feat(api): rename list_users to list_customers

BREAKING CHANGE: list_users is removed. Callers must use
list_customers, which takes the same arguments.
```

## Bad examples (do not write like this)

> `fix stuff`

It names no area, no behaviour, and no fix. Nothing in a diff could
prove or disprove it.

> `update code and improve things`

Two vague verbs, no subject, no scope. A reader cannot tell what
was updated or what improved.

> `feat: added new feature`

The type is right and everything else is missing: no scope, no
feature named, and the past tense where the imperative belongs.

> `fix(auth): fix the bug and also update the docs and bump deps`

Three unrelated changes in one message. Split it into three
commits, one message each.

## Output rules

- Output one message per commit, each in its own code block.
- Every claim in the message must be traceable to a line in the
  diff. If it cannot be traced, leave it out and list it as
  deliberately omitted.
- Never invent a ticket number, an issue link, a test result, or a
  reason the diff does not show.
- Never claim tests pass unless they were actually run, and never
  claim a change is safe, minor, or non-breaking without checking
  the diff for callers it affects.
- Never run `git commit`, `git push`, or any command that records
  the change. Writing the message is the whole job; committing is
  the user's decision, after reading it.

## Limits and safety rules

- This skill reads diffs and file paths only. It sends nothing
  anywhere, stages nothing, and commits nothing.
- It does not rewrite history, amend a commit, or force-push.
  A message for an already-made commit is a suggestion for the
  next one, not a rewrite of the past.
- It does not work from a remembered or summarised change. If
  there is no diff, the report says so and stops at that fact;
  it does not invent one.
- Local fixture diffs (see `examples/sample-diff.diff`) cannot
  prove a live reason or a live test result. A walkthrough run on
  fixtures marks those items as deliberately omitted, exactly as
  the sample messages do.
