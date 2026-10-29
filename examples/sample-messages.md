# Sample messages — commit-message skill walkthrough

Worked example for the commit-message skill, run on
`examples/sample-diff.diff` only. The diff touches two unrelated
areas, so the skill splits it into two commits instead of one
blurred message.

## Commit 1 — the token fix

```
fix(auth): reject expired tokens instead of refreshing them
```

- Type `fix`: the diff changes existing behaviour (an expired
  token used to be refreshed, now it is rejected).
- Scope `auth`: the changed path is `src/auth/tokens.py`.
- No body: the subject plus the diff is already clear.
- No breaking-change footer: no public function is removed or
  renamed here.

## Commit 2 — the renamed function

```
feat(api): rename list_users to list_customers

BREAKING CHANGE: list_users is removed. Callers must use
list_customers, which takes the same arguments.
```

- Type `feat`: the public surface changes (a function is renamed).
- Scope `api`: the changed path is `src/api/users.py`.
- Footer: the diff removes a public function, so the breaking
  change is flagged explicitly, with what callers must do instead.

## Refused drafts

- `fix stuff` — refused: no area, no behaviour, no fix named.
  Nothing in the diff could prove or disprove it.
- `update code and improve things` — refused: no subject and no
  scope, two vague verbs. A reader cannot tell what was updated
  or what improved.

## Deliberately omitted

- Ticket or issue number: not visible in the diff, and none was
  supplied with it.
- Test result: no test run is shown in the diff, so no test claim
  is made.
- Reason for the rename: the diff shows the rename, not why it was
  wanted, so no reason is invented for it.
