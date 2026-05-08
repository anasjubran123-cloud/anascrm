# REDIRECTS.md — Convergent Technology corporate site

## Status

**Greenfield launch — no migration.** Per session decisions on 2026-05-08, the existing convergent.sa property is being replaced from scratch and there is no indexed URL set worth preserving from the prior site.

## What this means at deploy

- No `301` redirect map is shipped in `public/.htaccess`. The only redirects there are:
  - `http://*` → `https://*` (transport)
  - `https://convergent.sa/*` → `https://www.convergent.sa/*` (canonical host)
- Internal links across `/en/...` and `/ar/...` are managed in code via `localizedPath()` (`src/lib/i18n.ts`); breaking them shows up in the linkinator pass during Phase 11 staging review.

## If this assumption changes

If the legacy site's URLs need to be preserved (Search Console reports lots of inbound traffic, valuable backlinks, etc.):

1. Run a crawl of the legacy site (Screaming Frog free tier or `wget --spider`) and dump the URL inventory to `migration/legacy-urls.txt`.
2. Build an old-→-new map. Use `301 Permanent` for permanent moves, `410 Gone` for content that intentionally won't exist on the new site.
3. Add the rules to `public/.htaccess` immediately above the canonical-host redirect block. Use `RewriteRule` with `[R=301,L,NE]` and order specific rules before broad ones.
4. Verify each redirect with `curl -I -L https://www.convergent.sa/<old-path>` post-deploy.
5. Update this file with the redirect inventory.

The launch checklist (`launch-checklist.md`, Phase 12) blocks production go-live unless this file is either confirmed greenfield (current state) or the redirect map above is documented and verified.
