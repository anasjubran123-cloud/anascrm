# launch-checklist.md — Convergent Technology corporate site

Run through this list **immediately before flipping the production robots.txt to allow crawl**. Every box must be ticked or have a documented waiver from the owner named in `OPERATIONS.md` §1.1.

This checklist composes the verification lists from `SECURITY.md`, `PERFORMANCE.md`, `DEPLOY.md`, and `CONTENT.md`. The honesty rule applies — only tick what was actually verified.

---

## 1. Content & legal

- [ ] All `{{TODO}}` markers in the codebase resolved or waived.
- [ ] `CONTENT.md` §1 (brand assets) all rows green: logo binaries, Cairo font files, favicon set, OG default, photography buckets at least populated for Home + the published case studies.
- [ ] `CONTENT.md` §3 (decisions) — every "decision needed" row has an answer.
- [ ] `CONTENT.md` §4 (Local SEO) — HQ address, phone, WhatsApp, hours, Maps URL, geo coordinates all present.
- [ ] CT legal counsel has signed off on Privacy, Cookies, Terms — draft banners removed, `pages/{en,ar}/legal/*` updated.
- [ ] Every published partner logo has written display approval; partners with `approved: false` are hidden.
- [ ] Every published case study has written disclosure approval; placeholders with `placeholder: true` and `approved: false` are hidden.

## 2. Build & code health

- [ ] `npm install` clean.
- [ ] `npm run typecheck` passes (no errors).
- [ ] `npm run build` succeeds and `dist/` contains the expected tree (per `DEPLOY.md` §1).
- [ ] `npm test` (Playwright + axe smoke) passes locally.
- [ ] CI on `main` is green.
- [ ] No source maps or `.env*` in `dist/`.

## 3. Routing & i18n

- [ ] Home redirects: `/` → `/en` (302).
- [ ] Both `/en/...` and `/ar/...` mirror correctly across all listed pages.
- [ ] Each page has hreflang for `en-SA`, `ar-SA`, and `x-default`.
- [ ] Each page has a unique title, description, canonical, and OG image.
- [ ] Apex (`https://convergent.sa/...`) 301s to `https://www.convergent.sa/...`.
- [ ] Any non-canonical host (e.g. `convergenttec.com` if it ever points here) is blocked or redirected.

## 4. SEO

- [ ] `sitemap-index.xml` lists every public page in both locales.
- [ ] Production `robots.txt` is `Allow: /` and references the sitemap.
- [ ] JSON-LD validates at `validator.schema.org` for Organization, LocalBusiness, BreadcrumbList. Article LD validates on the launch news entry.
- [ ] Sitemap submitted to Google Search Console + Bing Webmaster Tools.
- [ ] Search Console URL Inspection confirms hreflang pairs are recognised.
- [ ] Google Business Profile + Bing Places listings claimed and consistent with the JSON-LD `LocalBusiness`.

## 5. Performance

- [ ] Lighthouse mobile + desktop, both locales: Performance / A11y / Best Practices / SEO ≥ 95 on Home + Contact + a Capabilities + a Project + 404.
- [ ] LCP < 2 s, INP < 200 ms, CLS < 0.05 on Home and Contact.
- [ ] First-load JS under 100 KB gzipped per route. Recorded in PERFORMANCE.md.
- [ ] Brotli (or gzip fallback) confirmed via `curl -I -H 'Accept-Encoding: br' ...`.

## 6. Accessibility (WCAG 2.2 AA)

- [ ] axe-core scan clean on Home / Contact / a Capabilities / a Projects detail / 404 in both locales.
- [ ] Keyboard-only walk-through completes the entire site.
- [ ] Skip-to-content link is the first focusable element on every page.
- [ ] Focus is never obscured by the sticky header.
- [ ] All interactive targets ≥ 24×24 CSS px (preferably 44×44).
- [ ] Heading hierarchy is uninterrupted on every page.
- [ ] Reduced motion respected.

## 7. Security

- [ ] `securityheaders.com` grade recorded.
- [ ] `ssllabs.com/ssltest` grade recorded.
- [ ] OWASP ZAP baseline scan ran — no high findings, document any medium with mitigation.
- [ ] CSP Report-Only tail clean for at least 1 week before flipping to enforcement (or evidence the only violations are known, e.g. browser extensions injecting their own scripts).
- [ ] `.htaccess` at the production document root matches `public/.htaccess` in the repo.
- [ ] HSTS still at the conservative initial value; bump to 1 year only after operation is clean.
- [ ] `/.well-known/security.txt` reachable; `Expires` is in the future.

## 8. Email security

- [ ] SPF, DKIM, and DMARC records published; `mxtoolbox.com` validates each.
- [ ] DMARC starts at `p=quarantine` (or `p=none` for the very first 7 days if CT prefers).
- [ ] Test inbound delivery to `info@convergent.sa` from at least one external mailbox; confirm signed-DKIM headers.

## 9. Forms

- [ ] Real test submission from `/en/contact` lands at `info@convergent.sa`.
- [ ] Real test submission from `/ar/contact` lands with the Arabic body intact.
- [ ] Honeypot drop verified (DevTools — fill the hidden field, submit a valid form, confirm vendor never receives it).
- [ ] Min-time-to-submit drop verified (programmatic submit < 3 s after page load is dropped).
- [ ] hCaptcha (if configured) blocks submission until solved.
- [ ] Vendor-side spam controls enabled.

## 10. Operations

- [ ] HostGator weekly backup is enabled and the most recent backup tarball downloaded as a known-good baseline.
- [ ] Pre-deploy backup zip retained for the previous build.
- [ ] Uptime monitor configured (HostGator built-in or a free third-party).
- [ ] Incident escalation contacts in `OPERATIONS.md` §6 are accurate and up to date.

## 11. Cloudflare (only if onboarded at launch)

- [ ] DNS proxied through Cloudflare.
- [ ] SSL/TLS mode = Full (strict).
- [ ] Always Use HTTPS + Automatic HTTPS Rewrites + Bot Fight Mode + WAF managed rules ON.
- [ ] Free-tier feature availability verified before any feature is promised in user-facing docs (rate limits, Transform Rules, etc.).
- [ ] Origin firewall restricts inbound traffic to Cloudflare IPs only (HostGator firewall rule).

## 12. Final flip

When (and only when) every applicable box above is ticked or waived:

1. Replace `public_html/robots.txt` with the production version (`public/robots.production.txt`).
2. Verify `curl https://www.convergent.sa/robots.txt`.
3. Submit / re-submit the sitemap to Search Console and Bing Webmaster.
4. Announce the launch internally; tag the commit on the branch.

Welcome to www.convergent.sa.
