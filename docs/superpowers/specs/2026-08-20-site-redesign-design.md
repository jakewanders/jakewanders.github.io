# jakewanders.github.io — redesign, repo cleanup, deploy pipeline

Date: 2026-08-20. Approved in chat by Jake.

## Goals
1. Replace the 2018 Bootstrap "Grayscale" portfolio with a clean, minimalist resume-first site with a light/dark toggle.
2. Separate, small "Work" page with only projects that show senior-level (React/TS/Node, AI-assisted dev, harness/MCP/skills) work.
3. Shrink the repo from 345 MB (166 MB git pack, 153 MB hero JPGs) to < 1 MB by deleting dead assets and rewriting history.
4. Make GitHub Pages deploy automatically on push to `master`, with a README playbook and documented access.

## Decisions (from Jake)
- Repo becomes **public** (Pages on private repos needs Pro).
- History rewrite + force-push: **yes**.
- Links: GitHub `jakewanders`, LinkedIn `linkedin.com/in/jnelson180`, email `jnelson180@gmail.com`. No Twitter.
- Keep `misc/privacy_policy.html`, `misc/terms_of_service.html` at their current paths. (TikTok verification files were removed on 2026-08-21 at Jake's request.)

## Architecture
- Pure static: `index.html` (resume), `work.html` (selected projects), `assets/site.css`, `assets/theme.js`. No framework, no npm, no build step.
- Theme: `data-theme` on `<html>`; inline head script applies saved/system preference before first paint; toggle persists to `localStorage`.
- Print stylesheet so `index.html` prints as a one-page resume.
- Deploy: `.github/workflows/deploy.yml` → `actions/upload-pages-artifact` + `actions/deploy-pages`; Pages source = GitHub Actions. `.nojekyll` present.
- Content lives directly in semantic HTML (no data layer) — simplest to edit and best for print/SEO.

## Content
- Header: name, title line, links. Summary (3 lines). Experience (slots marked `TODO` where Jake must supply employer/dates/bullets). "AI-assisted engineering" section (MCP server, custom skills, harness work, orchestration across SDLC). Skills grouped. Selected work (3 cards) linking to `/work`. Contact.
- Work page: LifeDash, EdgeSeeker, Site-launch pipeline (all private — case studies). hand-in-hand and rentahuman-bot-discord were removed on 2026-08-21.

## Repo cleanup
Delete: `old/ vendor/ img/ coffee/ piano/ weather/ css/ scss/ js/ misc/*.png misc/*.jpg misc/*.wav misc/bgs gulpfile.js package*.json .travis.yml public LICENSE(template)`. Then `git filter-repo` to purge those paths from all history; local bundle backup at `~/repos/jakewanders.github.io.pre-rewrite.bundle`.

## Deploy / access
- `gh` CLI authenticated as jakewanders with `repo` + `workflow` scope (done by Jake).
- Steps Claude performs: set repo public, enable Pages (build_type=workflow), push, watch run, verify HTTP 200.
- README documents all of this plus rollback.

## Testing
- Local: open in browser, check both themes, print preview, mobile width.
- Deploy: `gh run watch`, `curl -I https://jakewanders.github.io` → 200, spot-check `/work.html` and `/misc/privacy_policy.html`.
