# everydaystatistics

Astro static site, deployed on Cloudflare Pages.

## Dev environment

Node version is pinned in `.nvmrc` so local dev, CI, and the Cloudflare
Pages build all use the same major version.

```bash
nvm use            # or: install the Node version named in .nvmrc
npm ci             # clean install from package-lock.json
npm run dev        # local dev server
```

If you don't use `nvm`, ensure your Node satisfies `engines` in
`package.json` (`>=22.12.0`).

## Build

```bash
npm run build      # → dist/  (the deployable static site)
npm run preview    # serve the built dist/ locally
```

For a static Astro site, a successful `npm run build` is the gate: a
broken page, bad import, or malformed config fails the build.

## The verify-build gate

A change is "done" only when `npm run build` succeeds. Enforced in two
places:

- **Pre-commit hook** (`.githooks/pre-commit`) — runs the build when
  site source or config is staged, blocks the commit on failure.
  Enable once per clone: `git config core.hooksPath .githooks`.
  Emergency bypass: `git commit --no-verify`.
- **CI** (`.github/workflows/ci.yml`) — runs the build on every push to
  `main` and every pull request.

Commits touching only drafts / tooling / docs skip the hook gate.

## Deploy

Cloudflare Pages is connected to this GitHub repo and auto-builds-and-
deploys on every push to `main`. There is no manual deploy step:

```bash
git push origin main      # → Cloudflare Pages builds and deploys
```

After pushing, confirm the deployment succeeded in the Cloudflare Pages
dashboard (or `wrangler pages deployment list`), then check the live
site loads.

## Rollback

In the Cloudflare Pages dashboard, roll back to a previous deployment;
or `git revert <bad-sha> && git push`.
