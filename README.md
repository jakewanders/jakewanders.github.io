# jakewanders.github.io

Personal résumé site for Jake Nelson. Live at **https://jakewanders.github.io**.

Plain HTML + CSS + ~40 lines of JS. No framework, no package manager. CI runs two stdlib-Python steps before deploying: `scripts/build_blog.py` generates `/blog` from Sanity, then `scripts/inline_assets.py` copies `site.css` and `theme.js` into every page so first paint needs only the HTML request. Source pages keep normal `<link>`/`<script src>` tags, so editing and local preview are unchanged. Fonts (IBM Plex, latin subset, SIL OFL) are self-hosted in `assets/fonts/` with `font-display: optional` and preloaded, so text never reflows when they arrive.

```
index.html            résumé (the home page)
work/index.html       selected projects (served at /work/)
contact/index.html    email, GitHub, LinkedIn (served at /contact/)
work.html             redirect stub so old /work.html links still land on /work/
scripts/build_blog.py generates blog/ (gitignored) from the Sanity posts twoweeksites.com uses
scripts/inline_assets.py  CI only: inlines site.css + theme.js into every page (rewrites files in place)
assets/fonts/         self-hosted IBM Plex woff2 + license
assets/site.css       all styles; light/dark tokens at the top
assets/theme.js       theme toggle (persists to localStorage)
misc/                 privacy policy / terms pages for other apps — keep
.github/workflows/    deploy pipeline
docs/superpowers/     design specs
```

## Editing content

Everything is in the HTML. To update the résumé, edit `index.html`; to add a project, copy a `<article class="card">` block in `work/index.html`. Pages live in their own folder as `index.html` so URLs stay extension-free (`/work/`, not `/work.html`); link between pages and to `/assets/` with root-relative paths. The nav is repeated in each page and in `scripts/build_blog.py` — update all of them when adding a tab. Preview locally with any static server:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

### Blog

Posts are written and published in Sanity (see the `site-launch` repo's `publish-post` skill); this site never edits them. The deploy workflow runs `python3 scripts/build_blog.py` before uploading, and also runs daily at 13:00 UTC so new posts appear without a push. To publish a new post here immediately, run `gh workflow run deploy.yml`. Post pages set `rel=canonical` to `twoweeksites.com/post/<slug>` so search engines don't treat them as duplicate content. If Sanity is unreachable or returns no posts, the build fails and Pages keeps serving the last good deploy.

Preview locally: `python3 scripts/build_blog.py && python3 -m http.server 8000`, then open http://localhost:8000/blog/.

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

Lighthouse target is 100 in all four categories on every page; run it in an Incognito window (extensions skew Best Practices and add fake "unused JavaScript"). If you add a new font weight, add its `@font-face` in `site.css` and a preload line in each page and in `build_blog.py`.

If the run is green but the site looks stale, it is browser/CDN cache. The HTML links `assets/site.css?v=<sha>` and `assets/theme.js?v=<sha>`; **bump that `?v=` value in every HTML page whenever you change CSS or JS** (e.g. `sed -i '' "s/?v=[a-z0-9]*/?v=$(git rev-parse --short HEAD)/" index.html work/index.html contact/index.html` and update `ASSET_VERSION` in `scripts/build_blog.py`) so visitors never see an old stylesheet.

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
