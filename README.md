# jakewanders.github.io

Personal résumé site for Jake Nelson. Live at **https://jakewanders.github.io**.

Plain HTML + CSS + ~40 lines of JS. No framework, no package manager, no build step. What is in `master` is what is served.

```
index.html            résumé (the home page)
work.html             selected projects
assets/site.css       all styles; light/dark tokens at the top
assets/theme.js       theme toggle (persists to localStorage)
misc/                 privacy policy / terms pages for other apps — keep
.github/workflows/    deploy pipeline
docs/superpowers/     design specs
```

## Editing content

Everything is in the HTML. To update the résumé, edit `index.html`; to add a project, copy a `<article class="card">` block in `work.html`. Preview locally with any static server:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Print preview (Cmd/Ctrl+P) on the résumé page produces a clean PDF — the print stylesheet hides nav and the theme toggle.

## Deploy playbook

### How deploys happen

Every push to `master` runs `.github/workflows/deploy.yml`, which uploads the repo root as a Pages artifact and deploys it. Typical time from push to live: under a minute. You can also trigger it by hand from the Actions tab ("Run workflow") or with:

```bash
gh workflow run deploy.yml
```

### Verify a deploy

```bash
gh run list --workflow deploy.yml --limit 3      # status of recent runs
gh run watch                                     # follow the latest run
curl -sI https://jakewanders.github.io | head -1 # expect HTTP/2 200
```

If the run is green but the site looks stale, it is browser/CDN cache. The HTML links `assets/site.css?v=<sha>` and `assets/theme.js?v=<sha>`; **bump that `?v=` value in both HTML files whenever you change CSS or JS** (e.g. `sed -i "s/?v=[a-f0-9]*/?v=$(git rev-parse --short HEAD)/" index.html work.html`) so visitors never see an old stylesheet.

### Roll back

Pages serves whatever the last successful run deployed. To roll back, revert the commit and push:

```bash
git revert <bad-sha> && git push
```

or re-run an older green run from the Actions tab ("Re-run all jobs").

### One-time setup (done 2026-08-21 — recorded here so it can be redone)

The repo must be **public** (GitHub Pages on a private repo requires a paid plan — this was the reason the site was dark), and Pages must be set to build from **GitHub Actions**, not from a branch.

```bash
gh repo edit jakewanders/jakewanders.github.io --visibility public --accept-visibility-change-consequences
gh api -X POST repos/jakewanders/jakewanders.github.io/pages -f build_type=workflow
gh api repos/jakewanders/jakewanders.github.io/pages --jq '{build_type, html_url, status}'
```

Equivalent in the UI: Settings → General → Danger Zone → Change visibility; Settings → Pages → Build and deployment → Source: *GitHub Actions*. After either, re-run the last workflow (`gh run rerun --failed $(gh run list --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')`) or push any commit.

### Access needed to operate this (for a human or an agent)

| Need | How it is provided |
|---|---|
| Push to `master` | SSH key or `gh auth` token with `repo` scope |
| Inspect / re-run workflows | `gh` CLI logged in as `jakewanders`. Fine-grained PAT: **Actions: read** (or classic token with `repo` scope) |
| Enable Pages, change visibility (one-time setup only) | Fine-grained PAT additionally needs **Administration: write** and **Pages: write** on this repo. Without them the setup commands return `HTTP 403: Resource not accessible by personal access token` and must be done in the web UI instead |
| Deploy itself | No secret required — the workflow uses the repo's built-in `GITHUB_TOKEN` with `pages: write` + `id-token: write`, granted in the workflow file |

Check current auth with `gh auth status`. Nothing else (no PATs in repo secrets, no third-party services) is involved.

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Site 404s, no runs in Actions | Repo is private, or Pages not enabled | Run the one-time setup commands above |
| Run fails at `configure-pages` | Pages source is "branch", not "Actions" | `gh api -X PUT repos/jakewanders/jakewanders.github.io/pages -f build_type=workflow` |
| Run fails at `deploy-pages` with a permissions error | `permissions:` block in the workflow was edited | Restore `pages: write` and `id-token: write` |
| New page returns 404 but others work | File not committed, or wrong case in filename | `git ls-files` to confirm it's tracked |
