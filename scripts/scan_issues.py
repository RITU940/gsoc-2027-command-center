#!/usr/bin/env python3
"""Scan scoped public GitHub issues. Standard library only.

Usage (PowerShell):
  $env:GH_TOKEN = gh auth token
  python scripts/scan_issues.py

Do not assume an unassigned or labeled issue is available: inspect comments,
linked PRs and maintainer guidance before claiming work.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "config" / "targets.json"
OUTPUT = ROOT / "data" / "issues.json"


def calculate_score(item, org_weight=3, now=None):
    """Heuristic attention score, NOT an estimate of acceptance probability."""
    now = now or datetime.now(timezone.utc)
    labels = {x["name"].casefold() if isinstance(x, dict) else str(x).casefold()
              for x in item.get("labels", [])}
    score = 20 + org_weight * 7
    if "good first issue" in labels or "easy to fix" in labels:
        score += 18
    if "help wanted" in labels:
        score += 11
    if "documentation" in labels or "tests" in labels or "test" in labels:
        score += 6
    score += 10 if not item.get("assignees") else -8
    comments = int(item.get("comments") or 0)
    score += 6 if comments <= 3 else (2 if comments <= 10 else -5)
    try:
        updated = datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00"))
        days = (now - updated).days
        score += 12 if days <= 30 else (8 if days <= 90 else (3 if days <= 180 else -4))
    except (ValueError, KeyError, AttributeError):
        pass
    title = item.get("title", "").casefold()
    if any(s in title for s in ["test", "documentation", "docs", "typo", "bug", "pathlib"]):
        score += 5
    if any(s in title for s in ["gpu", "cuda", "build entire", "kernel"]):
        score -= 10  # hardware constraint, not difficulty estimate
    return max(0, min(100, score))


def normalize_issue(item, repo, weight):
    return {
        "repo": repo,
        "number": item["number"],
        "title": item.get("title", ""),
        "url": item["html_url"],
        "labels": [x.get("name", "") for x in item.get("labels", [])],
        "updated_at": item.get("updated_at", ""),
        "comments": item.get("comments", 0),
        "assignees": [x.get("login", "") for x in item.get("assignees", [])],
        "score": calculate_score(item, weight),
    }


def search(query, token, limit):
    params = urlencode({"q": query, "per_page": limit, "sort": "updated", "order": "desc"})
    req = Request("https://api.github.com/search/issues?" + params,
                  headers={"Accept": "application/vnd.github+json",
                           "X-GitHub-Api-Version": "2022-11-28",
                           "User-Agent": "gsoc-2027-personal-issue-radar",
                           **({"Authorization": "Bearer " + token} if token else {})})
    with urlopen(req, timeout=25) as response:
        payload = json.load(response)
    return [x for x in payload.get("items", []) if "pull_request" not in x]


def run(max_queries=None, quiet=False):
    config = json.loads(TARGETS.read_text(encoding="utf-8"))
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    cap = max_queries if max_queries is not None else int(config.get("max_queries", 18))
    if not token:
        print("No GH_TOKEN/GITHUB_TOKEN found. Limiting to 5 queries to reduce unauthenticated rate-limit errors.", file=sys.stderr)
        cap = min(cap, 5)
    requests_used = 0
    by_url = {}
    errors = []
    jobs = [(o, label) for o in config["organizations"] if o.get("repo")
            for label in config.get("search_labels", ["good first issue"])]
    for org, label in jobs[:cap]:
        repo = org["repo"]
        query = f'repo:{repo} is:issue is:open label:"{label}"'
        try:
            found = search(query, token, min(int(config.get("per_query", 25)), 100))
            for x in found:
                obj = normalize_issue(x, repo, org.get("fit", 3))
                old = by_url.get(obj["url"])
                if old is None or obj["score"] > old["score"]:
                    by_url[obj["url"]] = obj
            if not quiet:
                print(f"{repo}: {label}: {len(found)} candidates")
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as e:
            errors.append(f"{repo} [{label}]: {type(e).__name__}: {getattr(e, 'code', '')}")
            if not quiet:
                print(errors[-1], file=sys.stderr)
        requests_used += 1
        if requests_used < min(cap, len(jobs)):
            time.sleep(float(config.get("pause_seconds", 2)))
    if not by_url:
        print("No successful results; preserving existing issue radar file.", file=sys.stderr)
        return 1
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "live-github-search",
        "note": "Scoped GitHub issue search, not an exhaustive search of all repositories. Recheck assignment, discussion, linked PRs and AI policies.",
        "partial": bool(errors) or requests_used < len(jobs),
        "errors": errors,
        "issues": sorted(by_url.values(), key=lambda x: (-x["score"], x["repo"], x["number"])),
    }
    tmp = OUTPUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUTPUT)
    print(f"Saved {len(result['issues'])} unique issues across {requests_used} scoped searches; errors: {len(errors)}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-queries", type=int, default=None, help="Maximum API search queries. Normally 18.")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.max_queries is not None and args.max_queries < 1:
        ap.error("--max-queries must be >= 1")
    return run(args.max_queries, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
