# First 30 days: 8 November — 7 December 2026

## Objective

At the end of the month, have evidence that you can navigate at least **two real codebases**, reproduce an issue, run meaningful tests, and communicate professionally. An accepted PR is a useful target, not a metric to game or a guarantee of anything.

### Days 1–3: high-quality triage
- Read the current GSoC FAQ, official student guide, AI guidance and the 2026 examples.
- Review the organization shortlist in the dashboard. Choose 3–5 for investigation. Confirm the community's contributing policy and communication channel.
- Search those organizations' recent merged PRs, not only their 'good first issue' labels. Are contributions from newcomers reviewed? How fast? Are issue discussions welcoming?
- Focus on **two** repos for setup, not nine simultaneously. For an 8 GB Windows laptop, p5.js/SymPy are reasonable starts; GRASS/DeepForest/OpenVINO may require a narrower Python-only module or stronger machine.

### Days 4–7: actual code
- Clone one chosen upstream repo (fork only after reading its policy).
- Read README, CONTRIBUTING, Code of Conduct, tests, and existing pull requests.
- Install the smallest supported environment, execute a narrow smoke test, and reproduce one issue. Save commands and outputs in an issue note.
- If you cannot reproduce the issue or understand the affected module, do not claim it. Select a different issue.

### Days 8–14: first useful contribution
- Confirm that no active PR already solves it. Follow project guidelines on asking for assignment or announcing intent.
- Prepare the minimal patch with a regression test. Run lint/tests relevant to that change.
- Submit a small, reviewable PR if permitted. Record the PR URL, tests and review follow-up in `data/contributions.csv`.

### Days 15–21: feedback and second issue
- Address maintainers' feedback promptly and respectfully; avoid pinging repeatedly.
- Read 2–3 merged PRs in the modules you are learning.
- Reproduce a second issue, preferably with more architectural understanding than the first.
- Check whether the 2026 GSoC ideas/proposals in the community reflect work you would enjoy for months.

### Days 22–30: commit to a direction
- Choose one primary target and one backup. Log what actual code and community interaction supports that choice in `data/decisions.csv`.
- Write a one-page design exploration: current architecture, limitations, proposed improvement, interfaces, test plan, risks.
- Ask a focused technical question in the approved channel; include what you investigated and a reproducible observation.
- Review any official GSoC 2027 announcements without assuming the final organizations list.

## Outcomes to review, not quotas

- One meaningful contribution or reproducible test case, ideally reviewed or merged.
- At least one maintainable local development environment.
- One or more substantive public technical interactions.
- A primary and fallback organization **provisionally** selected from genuine evidence.
- A detailed roadmap for the following six weeks.

## Time budget

Suggested baseline for a student: ~7–10 hours/week, adjusted around class tests and exams. Use 3–4 short focused sessions rather than endlessly hunting issues. Never sacrifice correctness or code review for a PR count.
