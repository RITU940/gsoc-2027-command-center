# GSoC 2027 Command Center

A practical, lightweight workspace for discovering potential GSoC organizations, scanning scoped GitHub issues, maintaining a contribution record and writing a well-evidenced application. Designed for **Windows 11 + VS Code + GitHub CLI + 8 GB RAM** and a Python/C++/web/CV/geospatial background.

> **As of 2026-11-08, 2027 organization acceptance and deadlines are NOT confirmed.** All organization choices are 2026 historical leads. The included GitHub issues are a search snapshot, not a guarantee that they are unclaimed or suitable. GitHub issue data updates only after you run the scanner or enable the scheduled GitHub Action.

## What's inside

| Folder | Purpose |
|---|---|
| `config/targets.json` | Organization watchlist, GitHub repos and bounded issue-search settings |
| `scripts/scan_issues.py` | GitHub Search API issue radar (standard Python library, token recommended) |
| `scripts/build_dashboard.py` | Builds the standalone responsive `docs/index.html` dashboard |
| `data/issues.json` | Initial issue snapshot, replaced after a successful live scan |
| `data/contributions.csv` | Your **actual** issues/PRs/reviews/tests evidence |
| `data/community_log.csv` | Recorded public conversations and guidance |
| `data/decisions.csv` | Why organizations/projects were shortlisted or dropped |
| `docs/` | Dashboard, plan, sourcing, issue workflow, proposal strategy |
| `templates/` | Proposal, issue notes, mentor discussions, weekly review |
| `.github/workflows/` | Weekday automatic scanning and optional GitHub Pages deployment |
| `.vscode/` | VS Code tasks for scan, dashboard, tests, local preview |
| `AGENTS.md` | Instructions for Codex in this workspace |
| `CHATGPT_PROJECT_PROMPT.md` | Copy into your ChatGPT GSoC project instructions |

## First 10 minutes on Windows

1. Extract the ZIP and open the folder in VS Code (`File > Open Folder`). Python 3.11+ and GitHub CLI (`gh`) are recommended; **no Python packages are needed**.
2. Open `docs/index.html` in your browser. It already contains a research-based sample watchlist and concrete issue leads. The snapshot is NOT live.
3. In PowerShell, from the extracted root:

   ```powershell
   gh auth status
   $env:GH_TOKEN = gh auth token
   python scripts/scan_issues.py
   python scripts/build_dashboard.py
   python -m unittest discover -s tests -v
   start .\docs\index.html
   ```

   **Security:** `GH_TOKEN` remains in your local session. Do not paste it into ChatGPT, a file, or a GitHub commit. The scanner only reads public issues. If authenticated API searches are unavailable or fail, it preserves the last snapshot and prints an error. GitHub rate limits apply.

4. In VS Code, `Terminal > Run Task` offers the same scanner and build steps. Edit `config/targets.json` to add/remove **specific** repositories you have checked.
5. Record work in `data/contributions.csv` and discussions in `data/community_log.csv` (these files contain only headers initially). Rebuild the dashboard after updates.

## Publish your own new GitHub repository

The ZIP does **not** create or change a GitHub repository by itself. To create `RITU940/gsoc-2027-command-center` after opening the extracted folder, run:

```powershell
git init -b main
git add .
git commit -m "Initialize GSoC 2027 command center"
gh repo create RITU940/gsoc-2027-command-center --public --source . --remote origin --push
```

If you have already initialized a Git repo, do not reinitialize it. If the repository name exists, choose a different name. Check which files are staged before the first commit. The repo can be private if preferred, but publishing via GitHub Pages might have different availability depending on plan/settings.

### Enable scheduled GitHub issue scanning

- In the new repo, go to **Settings > Actions > General** and check workflow permissions if the bot can't commit. `.github/workflows/issue-radar.yml` requests write permissions for the repository it runs in.
- Go to **Settings > Pages > Build and deployment > Source: GitHub Actions** to permit dashboard deployment.
- Go to the **Actions** tab, select **GSoC Issue Radar and Dashboard**, click **Run workflow**.
- A scheduled run is configured for weekdays at **08:00 IST**; GitHub scheduling is best-effort and may not execute at the exact time, and inactive repositories may have schedules paused.
- After a successful run, the GitHub Pages deployment reports a URL in Actions. Don't assume a URL is live before a successful deployment.

**Limitation:** The scanner searches configured repositories under the `good first issue` and `help wanted` labels and stops at configured results per query. It does NOT search every open source issue in the world or imply an issue is available. Some projects do not use these labels: check their official issue board and project chat manually. It does not auto-comment, auto-claim, auto-submit PRs, or send messages to maintainers.

## Recommended strategy

**A. High-fit main candidate:** GRASS GIS (NumFOCUS) for geospatial Python and raster-processing contributions; setup can be heavy, so prefer isolated Python tests or manageable modules first. **B. Quick contribution path:** p5.js (Processing Foundation), excellent for JavaScript and a CPU-light local setup. **C. Research-oriented reserve:** DeepForest, MNE-Python or OpenVINO depending on project fit and hardware. **D. ETCE alternate:** GNU Radio. **E. Algorithmic alternate:** SymPy.

From these, choose **3–5 to inspect** and **1–2 to actively contribute to** after testing community receptiveness. This is a strategy, not a statement that any organization will be accepted in 2027 or that these issues will become GSoC ideas.

Begin with [`docs/30-day-sprint.md`](docs/30-day-sprint.md). Review [`docs/source-notes.md`](docs/source-notes.md) for official documentation and historical evidence.

## Responsible use of AI and Code Assistants

Each organization may prohibit AI-written code or proposals. Read their actual contributor guidance before using Codex/ChatGPT in upstream work. You are responsible for understanding, independently testing and explaining every change. Use AI for reading, planning, learning, local test ideas and drafting notes only where permitted. **Do not mass-submit AI-generated comments or patches.** Avoid introducing unlicensed material. Maintainer instructions always supersede this workspace's preferences.

## Suggested weekly review (20 minutes)

Update the evidence CSV; review open issues you inspected and outstanding PR feedback; verify the newest published organization news; prune stale/high-resource leads; choose a single meaningful deliverable for the next seven days; adjust the proposal plan with evidence. Use `templates/weekly-review.md`.

---

This is a personal research and productivity workspace, not an official Google Summer of Code tool. No guarantee of selection or acceptance is implied.
