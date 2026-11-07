# AGENTS — Codex / local coding assistant operating constraints

## Scope
This repo is a **personal** GSoC preparation tracker, not an upstream target project's source code. Work only on the requested file(s) and branches. The `data/contributions.csv` file must reflect actual verified contributions; never fabricate PRs, comments, reviews, timestamps or mentor approval.

## Technical constraints
- Prefer Python 3.11+ standard library and simple offline HTML/JS. No database, Docker or GPU dependencies.
- Validate JSON and CSV format, run `python -m unittest discover -s tests -v`, and run `python scripts/build_dashboard.py` after changes.
- Do not expose authentication tokens, emails or private information in output, commits or logs.
- GitHub Search API is rate-limited; use small queries, deduplicate, avoid abusive polling.
- Never automatically send messages, claim issues, open PRs, or push patches to other organizations. This workspace's automation is read-only against external repos.
- Ignore project-specific AI permission ambiguity by stopping to check current contributor guidance, not by assuming permission.

## Safe workflow
For every change, explain files modified, rationale, tests actually run and remaining limitations. If adding a target repo, document its participating organization and verified current guidance, and avoid asserting GSoC 2027 selection before official confirmation.
