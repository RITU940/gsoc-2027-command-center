# Issue-to-PR workflow

1. **Discover** candidate issues in your dashboard or the organization's maintained board. Search closed/merged PRs with related keywords to learn patterns.
2. **Validate** present status on GitHub; inspect linked PRs and recent comments. An issue labeled `good first issue` is not always available, easy, or appropriate for your hardware.
3. **Scope**: write expected versus actual behavior, files involved, minimal reproduction, and tests you will run. Estimate runtime/memory requirements.
4. **Communicate** in the organization-prescribed channel when useful; do not ask for assignment where the contributing guide explicitly discourages it. Avoid generic 'please assign me' comments or spam.
5. **Implement** in a feature branch from the correct default branch. Use the project's test framework and style requirements.
6. **Verify** with a targeted test, relevant broader tests and a readable diff. No code you can't explain. Don't use AI-generated submissions when the project prohibits them.
7. **Contribute** one coherent PR with an issue link, diagnosis, approach, test output and limitations.
8. **Respond** to review. Keep a personal evidence log; only mark merged after confirmation.

### Suggested commands

```powershell
git clone https://github.com/processing/p5.js.git
cd p5.js
git status
# Read the repo-specific instructions before installing packages.
# Create a branch using the project's preferred workflow.
```

Use `templates/issue-research.md` to document your investigation.
