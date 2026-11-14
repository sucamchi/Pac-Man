# Git Guidelines for Duo Team

## 1. Branching: keep `main` always working

- `main` always builds and runs. **Nobody commits directly to it.**
- Every piece of work gets a short-lived branch off the latest `main`:

  ```bash
  git switch main && git pull
  git switch -c feat/ghost-ai
  ```

- Branch naming: `feat/…`, `fix/…`, `refactor/…`, `docs/…`.
- Keep branches small and merge them within a day or two. Long-lived branches cause painful conflicts.
- Split work by module or file (e.g. map parsing vs. rendering vs. ghost logic) so we rarely touch the same lines.
- Agree on shared interfaces (headers, structs, function signatures) **before** both coding against them.

## 2. Pull requests

- Every branch goes through a PR. The **other person** reviews and merges it.
- Keep PRs small (ideally under ~300 lines).
- PR description: what changed, why, how to test it.
- Before requesting review, check that:
  - [ ] It builds with no warnings
  - [ ] The norm/linter passes (if the subject requires it)
  - [ ] It runs and the feature works
  - [ ] No debug prints or commented-out code left behind
- On GitHub, enable branch protection on `main`: require a PR and one approval.
- Review properly, not as a rubber stamp. Both of us must be able to explain every part of the code at evaluation.

## 3. Commits

- Small and focused: one logical change per commit.
- Use Conventional Commits:

  ```
  feat(ghost): add chase behaviour for blinky
  fix(map): handle trailing newline in parser
  docs: add build instructions to README
  refactor(render): split draw loop into helpers
  ```

- Imperative mood, subject line under ~50 characters, add a body only when the "why" isn't obvious.
- No `wip`, `fix`, `asdf`, `stuff`.
- Before every commit, run `git status` and `git diff --staged`. Prefer `git add -p` over `git add .`.

## 4. Staying in sync

- Start every work session with:

  ```bash
  git switch main && git pull --rebase
  ```

- Rebase your feature branch onto the latest `main` before opening the PR:

  ```bash
  git fetch origin
  git rebase origin/main
  ```

- **Never** rebase or force-push a branch the other person is also working on.
- If you must force-push your own branch after a rebase, use `--force-with-lease`, never plain `--force`:

  ```bash
  git push --force-with-lease
  ```

## 6. Communication

- Use GitHub Issues (or a shared checklist) to split tasks. **One assignee per issue** to avoid duplicated work.
- Announce when you're about to touch a shared file or core data structure.
- Short daily sync:
  1. What I did
  2. What I'm doing
  3. What's blocking me

## 7. 42-specific notes

- Evaluated code lives on the Vogsphere/intra remote. A common setup: work on GitHub with PRs, and push only a clean final `main` to intra.

  ```bash
  git remote add intra <vogsphere-url>
  git push intra main
  ```

- Before evaluation, **clone the repo fresh into an empty folder** and build/run it there. This catches missing files, wrongly ignored files, and "works on my machine" bugs.
- Check that the repo contains only what the subject asks for.

## Quick reference

| Goal | Command |
| --- | --- |
| New branch | `git switch -c feat/x` |
| Sync without merge commits | `git pull --rebase` |
| Stage in chunks | `git add -p` |
| Fix last (unpushed) commit | `git commit --amend` |
| Park changes temporarily | `git stash` / `git stash pop` |
| Visual history | `git log --oneline --graph` |
| Tidy commits before a PR | `git rebase -i main` |
| Safe force push | `git push --force-with-lease` |

## Daily workflow in short

1. `git switch main && git pull --rebase`
2. `git switch -c feat/my-task`
3. Code, commit small and often
4. `git fetch && git rebase origin/main`
5. Push and open a PR
6. Partner reviews and merges
7. Delete the branch, pull `main`, repeat
