#!/usr/bin/env python3
"""Build a standalone offline HTML GSoC 2027 command center. No dependencies."""
import csv
from datetime import date
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(filename):
    with (ROOT / "data" / filename).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build():
    config = json.loads((ROOT / "config" / "targets.json").read_text(encoding="utf-8"))
    issues = json.loads((ROOT / "data" / "issues.json").read_text(encoding="utf-8"))
    payload = {
        "orgs": config["organizations"], "issueData": issues,
        "contributions": read_csv("contributions.csv"),
        "community": read_csv("community_log.csv"),
        "updated": date.today().isoformat()
    }
    embedded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    page = r'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>GSoC 2027 | Command Center</title>
<meta name="description" content="Personal GSoC preparation and open source contribution radar."/>
<style>
:root{color-scheme:dark;--bg:#0b1120;--pane:#141e31;--panel:#19263d;--border:#2b3d58;--text:#e8efff;--muted:#9bb0cc;--accent:#67e8f9;--violet:#b4a0f6;--green:#76e5b0}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 80% 0%,#183150 0%,var(--bg) 45%);color:var(--text);font-family:Inter,Segoe UI,system-ui,-apple-system,sans-serif;line-height:1.5}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1230px;margin:0 auto;padding:30px 24px 80px}
.eyebrow{color:var(--accent);font-size:.77rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
h1{font-size:clamp(2rem,5vw,3.45rem);letter-spacing:-.05em;line-height:1.13;margin:12px 0 10px}
.subtitle{color:var(--muted);max-width:800px;margin:0 0 25px}.notice{border:1px solid #526d80;padding:13px 16px;background:#172639;border-radius:12px;color:#cae0ee;font-size:.87rem;margin:12px 0 28px}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0 38px}
.stat{border:1px solid var(--border);border-radius:16px;background:linear-gradient(145deg,#19283e,#111a2c);padding:20px}
.stat strong{font-size:2.35rem;line-height:1.2;display:block}.stat small{font-size:.8rem;color:var(--muted)}
h2{font-size:1.52rem;letter-spacing:-.025em;margin:42px 0 10px}.section-info{color:var(--muted);margin:0 0 15px}
.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
input,select{background:#141f32;color:var(--text);border:1px solid var(--border);border-radius:10px;padding:11px 13px;font:inherit;max-width:100%}
input{flex:1;min-width:230px}select{min-width:155px}
.issue-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.issue{background:var(--pane);border:1px solid var(--border);border-radius:14px;padding:18px 19px;min-width:0}
.issue .top{display:flex;justify-content:space-between;align-items:center;gap:10px}.score{border:1px solid #345d6b;color:#9febf5;font-size:.76rem;font-weight:700;padding:3px 9px;border-radius:999px;white-space:nowrap}
.issue h3{font-size:1.04rem;margin:9px 0 8px;line-height:1.38}.meta{color:var(--muted);font-size:.81rem;overflow-wrap:anywhere}
.tag{display:inline-block;background:#283852;border-radius:6px;color:#c8d4ee;font-size:.7rem;margin:6px 6px 0 0;padding:3px 7px}
.orgs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.org{background:var(--pane);border:1px solid var(--border);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:8px}
.org h3{margin:0;font-size:1.01rem}.org p{margin:0;color:var(--muted);font-size:.86rem}.org .foot{margin-top:auto;padding-top:8px;display:flex;flex-wrap:wrap;gap:12px;font-size:.82rem}
.pill{font-size:.71rem;border:1px solid #46636f;color:#b5e7e8;border-radius:99px;padding:3px 9px;white-space:nowrap}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.step{background:var(--pane);border-radius:13px;border:1px solid var(--border);padding:15px}.step b{color:var(--green);font-size:.84rem}.step p{font-size:.84rem;color:var(--muted);margin:6px 0 0}
table{border-collapse:collapse;width:100%;font-size:.86rem}th,td{border-bottom:1px solid var(--border);padding:12px 7px;text-align:left;word-break:break-word}th{color:var(--muted);font-weight:500}small{color:var(--muted)}
footer{margin-top:45px;color:var(--muted);font-size:.8rem}
@media(max-width:900px){.stats,.steps{grid-template-columns:repeat(2,minmax(0,1fr))}.orgs{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:590px){.container{padding:23px 14px 65px}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.stat{padding:12px}.stat strong{font-size:1.8rem}.issue-grid,.orgs,.steps{grid-template-columns:1fr}h1{font-size:2.2rem}}
</style></head><body><main class="container">
<div class="eyebrow">OPEN SOURCE · CAMPAIGN 2027</div>
<h1>GSoC 2027<br/>Command Center<span style="color:var(--accent)">.</span></h1>
<p class="subtitle">Your shortlist, issue radar, contribution evidence, community engagement and proposal strategy — in one place. Built for a lightweight Windows laptop.</p>
<div class="notice"><b>Verification status:</b> 2027 mentoring organizations and dates are not yet confirmed. The list below uses verified 2026 leads only. Issue results are scoped search suggestions, not permission to start a task; always inspect linked PRs, assignees, discussion, and the organization's AI guidance first.</div>
<section class="stats"><div class="stat"><strong id="nOrg">—</strong><small>2026 candidate organizations</small></div><div class="stat"><strong id="nIssue">—</strong><small>Discovered issue leads</small></div><div class="stat"><strong id="nPr">—</strong><small>Logged submitted PRs</small></div><div class="stat"><strong id="nComm">—</strong><small>Logged community interactions</small></div></section>
<section><h2>Four phases to selection</h2><p class="section-info">Actual deadlines will be updated when Google publishes the 2027 calendar.</p><div class="steps">
<div class="step"><b>Nov 2026 · Explore</b><p>Choose 3–5 organizations, read guides, run tests, and start with one carefully chosen issue.</p></div>
<div class="step"><b>Dec 2026 · Contribute</b><p>Make useful reviewable PRs, address reviewer feedback and learn architecture.</p></div>
<div class="step"><b>Jan–Feb 2027 · Focus</b><p>Reduce to 1–2 organizations, deepen technical ownership and track official announcements.</p></div>
<div class="step"><b>Mar 2027 · Propose</b><p>Write design, milestones, validation plan, risks, and submit early on the official portal.</p></div>
</div></section>
<section><h2>Open issue radar</h2><p class="section-info" id="issueStamp"></p><div class="toolbar"><input id="q" type="search" placeholder="Filter titles, repository, labels…" aria-label="Search issues"/><select id="repo" aria-label="Filter repository"><option value="">All repositories</option></select><select id="sort" aria-label="Issue sorting"><option value="score">Highest heuristic score</option><option value="updated">Most recently updated</option><option value="title">Title A–Z</option></select></div><div class="issue-grid" id="issues"></div><p id="issueCount" class="section-info"></p></section>
<section><h2>Organization watchlist</h2><p class="section-info">Personal technical fit is subjective, not a prediction of available slots or acceptance chances.</p><div class="orgs" id="orgs"></div></section>
<section><h2>Contribution evidence</h2><p class="section-info">Edit <code>data/contributions.csv</code> after each change, review, discussion, or PR update. Rebuild this page to reflect it.</p><div id="contributions"></div></section>
<section><h2>Official links</h2><p><a href="https://developers.google.com/open-source/gsoc/timeline" target="_blank" rel="noopener">Google timeline</a> · <a href="https://developers.google.com/open-source/gsoc/faq" target="_blank" rel="noopener">Eligibility and FAQ</a> · <a href="https://summerofcode.withgoogle.com/programs/2026/organizations" target="_blank" rel="noopener">2026 organization directory</a> · <a href="https://developers.google.com/open-source/gsoc/resources/ai_guidance" target="_blank" rel="noopener">AI guidance</a></p></section>
<footer>Dashboard build date: <span id="built"></span>. Scanner uses the GitHub Search API with bounded queries and rate limits. No affiliation with Google or participating organizations.</footer>
</main>
<script>
const DATA = __PAYLOAD__;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cleanURL=s=>/^https:\/\/([a-z0-9.-]+)(\/|$)/i.test(String(s??''))?esc(s):'#';
function drawOrgs(){ $('orgs').innerHTML=DATA.orgs.map(x=>`<article class="org"><span class="pill">${esc(x.track)}</span><h3>${esc(x.name)}</h3><p>${esc(x.why)}</p><p>Setup: ${esc(x.setup)} · Fit: ${esc(x.fit)}/5</p><div class="foot">${x.repo?`<a href="https://github.com/${esc(x.repo)}" target="_blank" rel="noopener">Code ↗</a>`:''}<a href="${cleanURL(x.guide)}" target="_blank" rel="noopener">Guidance ↗</a><a href="${cleanURL(x.gsoc_2026)}" target="_blank" rel="noopener">2026 evidence ↗</a></div></article>`).join('');}
function drawIssues(){ let list=[...(DATA.issueData.issues||[])];let term=$('q').value.toLowerCase().trim();let repo=$('repo').value;
 list=list.filter(x=>(!repo||x.repo===repo)&&(!term||[x.title,x.repo,...(x.labels||[])].join(' ').toLowerCase().includes(term)));
 const mode=$('sort').value;
 list.sort((a,b)=>mode==='title'?a.title.localeCompare(b.title):mode==='updated'?String(b.updated_at).localeCompare(String(a.updated_at)):(b.score||0)-(a.score||0));
 $('issues').innerHTML=list.map(x=>`<article class="issue"><div class="top"><span class="meta">${esc(x.repo)} #${esc(x.number)}</span><span class="score">${esc(x.score??'–')} /100</span></div><h3><a href="${cleanURL(x.url)}" target="_blank" rel="noopener">${esc(x.title)} ↗</a></h3><div class="meta">${x.updated_at?'Updated '+esc(x.updated_at.slice(0,10))+' · ':''}${(x.assignees||[]).length?'Assigned':'Assignment unverified or unassigned'}${x.comments===null||x.comments===undefined?'':' · '+esc(x.comments)+' comments'}</div><div>${(x.labels||[]).map(l=>`<span class="tag">${esc(l)}</span>`).join('')}</div></article>`).join('')||'<p class="section-info">No issues found for this filter. Check new searches or organization-specific onboarding channels.</p>';
 $('issueCount').textContent=`Showing ${list.length} of ${(DATA.issueData.issues||[]).length} issue leads.`;
}
function drawContrib(){if(!DATA.contributions.length){$('contributions').innerHTML='<div class="notice">No contributions logged yet. First milestone: reproduce an issue locally, write a test or patch, and log the evidence in data/contributions.csv.</div>';return;}
 $('contributions').innerHTML='<div style="overflow:auto"><table><thead><tr><th>Date</th><th>Organization</th><th>Stage</th><th>PR</th><th>Next action</th></tr></thead><tbody>'+DATA.contributions.map(x=>`<tr><td>${esc(x.date)}</td><td>${esc(x.organization)}</td><td>${esc(x.stage)}</td><td>${x.pr_url?`<a target="_blank" rel="noopener" href="${cleanURL(x.pr_url)}">View PR</a>`:'—'}</td><td>${esc(x.next_action)}</td></tr>`).join('')+'</tbody></table></div>';
}
function init(){ $('nOrg').textContent=DATA.orgs.length;$('nIssue').textContent=(DATA.issueData.issues||[]).length;$('nPr').textContent=DATA.contributions.filter(x=>x.pr_url).length;$('nComm').textContent=DATA.community.length;$('built').textContent=DATA.updated;
 $('issueStamp').textContent=`Source: ${DATA.issueData.mode}. Last checked: ${DATA.issueData.generated_at}. ${DATA.issueData.partial?'Partial scan/snapshot; verify current state.':'Full configured search completed; not all GitHub issues.'}`;
 for(const r of [...new Set((DATA.issueData.issues||[]).map(x=>x.repo))].sort()){const opt=document.createElement('option');opt.value=r;opt.textContent=r;$('repo').appendChild(opt)}
 $('q').addEventListener('input',drawIssues);$('repo').addEventListener('change',drawIssues);$('sort').addEventListener('change',drawIssues);drawOrgs();drawIssues();drawContrib();}
init();
</script></body></html>'''
    out = page.replace("__PAYLOAD__", embedded)
    target = ROOT / "docs" / "index.html"
    target.write_text(out, encoding="utf-8")
    print("Built", target)


if __name__ == "__main__":
    build()
