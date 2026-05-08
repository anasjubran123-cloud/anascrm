# DEPLOY.md — Convergent Technology corporate site

Step-by-step runbook for getting `www.convergent.sa` live on HostGator, plus the path for adding Cloudflare later. Everything below assumes you have:

- HostGator cPanel access for the `convergent.sa` account.
- DNS access for `convergent.sa` (registrar control panel).
- The `info@convergent.sa` mailbox owner credentials (for SPF/DKIM/DMARC verification).
- A laptop with full network access to install npm dependencies (the sandbox in which this scaffold was authored had `registry.npmjs.org` blocked, so `npm install` and the first `npm run build` need to happen on your machine).

---

## 1. Build the site locally

```bash
git checkout claude/ct-corporate-website-YFYF2
npm install            # installs everything from package.json
npm run typecheck      # astro check — must be clean
npm run build          # static output in dist/
npm run preview        # open http://localhost:4321 and walk both locales
npm test               # Playwright smoke (optional but recommended)
```

Commit the resulting `package-lock.json` if you don't have one yet.

Verify the `dist/` tree contains:

- `dist/index.html` (locale redirect)
- `dist/en/...` and `dist/ar/...` mirrored
- `dist/sitemap-index.xml`
- `dist/robots.txt` (currently the disallow-everything dev posture; we replace this for production below)
- All hashed assets under `dist/_astro/`
- `dist/favicon.svg`, `dist/site.webmanifest`, `dist/.well-known/security.txt`
- `dist/.htaccess` (production-grade — includes the staged HSTS / CSP)

---

## 2. Configure DNS (one-time)

| Record | Type | Value | TTL | Notes |
|---|---|---|---|---|
| `convergent.sa` | A | HostGator IP from cPanel → "Server Information" | 1 h | apex |
| `www.convergent.sa` | A | HostGator IP | 1 h | canonical host |
| `staging.convergent.sa` | A | same HostGator IP | 1 h | password-gated subdomain |
| `convergent.sa` | TXT (SPF) | `v=spf1 include:secureserver.net include:hostgator.com -all` | 1 h | Adjust `include:` mechanisms to whatever sends mail for the domain. |
| `default._domainkey.convergent.sa` | TXT (DKIM) | `{{TODO — copy from cPanel → Email Deliverability}}` | 1 h | cPanel exposes the key under "Email Deliverability". |
| `_dmarc.convergent.sa` | TXT (DMARC) | `v=DMARC1; p=quarantine; rua=mailto:dmarc@convergent.sa; pct=100` | 1 h | Start at `p=quarantine`, move to `p=reject` after 2–4 weeks of clean RUA reports. |
| `_acme-challenge.convergent.sa` | (managed) | (HostGator AutoSSL handles) | — | Don't pre-create. |

Verify SPF/DKIM/DMARC at `mxtoolbox.com` after propagation.

---

## 3. Provision SSL on HostGator (one-time)

1. cPanel → **SSL/TLS Status**.
2. Tick `convergent.sa`, `www.convergent.sa`, `staging.convergent.sa`.
3. Click **Run AutoSSL**. Wait for the green check.
4. Confirm with `https://www.convergent.sa` and `https://convergent.sa` (both should serve, the apex redirected to www by `.htaccess` after deploy).

If AutoSSL fails (common in fresh accounts), use cPanel → **Let's Encrypt** to manually issue a cert covering all three hosts.

---

## 4. Deploy (every release)

1. **Local build** (per §1).
2. **Swap the production `robots.txt`**:
   ```bash
   cp public/robots.production.txt dist/robots.txt
   ```
   This file is the launch-time `Allow: /` + sitemap reference. The repo's `public/robots.txt` stays as the offline-during-development version so a stray local preview doesn't accidentally allow crawl.
3. **Zip `dist/`**:
   ```bash
   ( cd dist && zip -r ../dist.zip . )
   ```
4. **Upload via cPanel File Manager**:
   - Navigate to `public_html/`.
   - **Backup first** — right-click `public_html` → Compress → name it `pre-deploy-YYYY-MM-DD.zip` and download a copy.
   - Delete the existing contents of `public_html/` (after the backup is verified).
   - Upload `dist.zip` to `public_html/`.
   - Right-click → Extract.
   - Confirm `.htaccess` is present at `public_html/.htaccess`. If File Manager is hiding dotfiles, enable "Show Hidden Files".
5. **Verify**:
   - `curl -I https://www.convergent.sa/en/` returns `200 OK` with the security headers in §SECURITY.md.
   - `curl -I https://convergent.sa/` returns `301` redirecting to `https://www.convergent.sa/`.
   - `curl https://www.convergent.sa/robots.txt` shows `Allow: /` and the sitemap reference.
   - `curl https://www.convergent.sa/sitemap-index.xml` returns 200.
   - Walk five pages in both locales in a real browser.

---

## 5. Staging deploy

Same procedure as §4, but:

- Upload to the `staging.convergent.sa` document root (typically `public_html/staging/` mapped via cPanel → Subdomains).
- Use `public/staging.htaccess` (rename to `.htaccess` at the staging root).
- Use `public/staging-robots.txt` (rename to `robots.txt` at the staging root).
- Set up **Directory Privacy** (cPanel) on the staging directory to enforce HTTP basic auth.

Reviewers receive: staging URL + basic-auth user/pass.

---

## 6. Post-deploy verification (run for real, no claims before)

Each item below produces evidence; tick the box only after the test runs.

### 6.1 Security

- [ ] `securityheaders.com` against `https://www.convergent.sa` — record grade.
- [ ] `ssllabs.com/ssltest/analyze.html?d=www.convergent.sa` — record grade.
- [ ] `mxtoolbox.com/SuperTool.aspx` — SPF / DKIM / DMARC pass.
- [ ] OWASP ZAP baseline scan — no high findings.

### 6.2 Performance

- [ ] Lighthouse mobile + desktop, both locales, Home + Contact + a Capabilities + a Project + 404 — record scores in PERFORMANCE.md.
- [ ] DevTools Performance "Slow 4G" — LCP < 2 s, INP < 200 ms, CLS < 0.05 on Home and Contact.

### 6.3 SEO

- [ ] Submit `https://www.convergent.sa/sitemap-index.xml` to Google Search Console.
- [ ] Submit the same URL to Bing Webmaster Tools.
- [ ] Verify hreflang pairs (`en-SA` ↔ `ar-SA` ↔ `x-default`) with Search Console's URL inspection on a sample page.
- [ ] JSON-LD validates at `validator.schema.org` for `Organization`, `LocalBusiness`, `BreadcrumbList`.
- [ ] Local SEO: claim Google Business Profile + Bing Places listing for the Al Khobar HQ.

### 6.4 Content / governance

- [ ] All `{{TODO}}` markers in `CONTENT.md` are resolved or have a documented waiver.
- [ ] Legal counsel has signed off on Privacy / Cookie / Terms (drafts must lose the draft banner).
- [ ] All partner logos have written display approval (or remain hidden via `approved: false`).
- [ ] All published case studies have written disclosure approval.

---

## 7. Rollback

If something is wrong on production:

1. cPanel → File Manager → `public_html/`.
2. Delete the broken contents.
3. Upload `pre-deploy-YYYY-MM-DD.zip` (the backup from §4 step 4).
4. Extract.
5. Verify with `curl -I https://www.convergent.sa/en/`.
6. File an incident note in `OPERATIONS.md` §"Decision log".

Total downtime should stay under 5 minutes if the backup zip is at hand.

---

## 8. Add Cloudflare later

When CT is ready to onboard Cloudflare:

1. Create a Cloudflare account (free plan is sufficient for v1).
2. Add `convergent.sa` as a zone. Cloudflare gives you two nameservers — set them at the registrar.
3. Wait for "Active" status (~minutes to hours).
4. **SSL/TLS** → mode = **Full (strict)**.
5. **Edge Certificates**:
   - Always Use HTTPS — on
   - Automatic HTTPS Rewrites — on
   - Minimum TLS Version — 1.2
   - HSTS — leave OFF here (we already serve HSTS from the origin; bump origin max-age to a year only after a clean observation window)
6. **Security**:
   - Bot Fight Mode — on
   - WAF managed rules — on
   - Rate limiting — `/contact*` 5 req / minute / IP. **Verify free-tier rate-limit quota first**; if not free, leave for the form vendor.
7. **Rules → Transform Rules** (if available on free):
   - Mirror `.htaccess` security headers as a backup carrier. **Verify Transform Rules availability on the free tier first.**
8. **Caching**:
   - Cache Level — Standard
   - Cache Rules: long cache for `/_astro/*`, bypass cache for `*.html` (Cloudflare honours the origin's `Cache-Control: no-cache` automatically).
9. **Page Rules**: not needed at v1 (Cache Rules cover the cases).
10. **Workers** (optional): move the form endpoint to a Cloudflare Worker for stricter rate limiting and a Turnstile widget swap. Update `PUBLIC_CONTACT_FORM_ENDPOINT` to the Worker URL.
11. **Web Analytics**: add the JS tag for Cloudflare Web Analytics (free, no cookie). Update the cookie notice and analytics consent flow accordingly.
12. After 1–2 weeks of clean operation, bump origin HSTS to `max-age=31536000; includeSubDomains`. Add `preload` only with explicit owner approval.

After Cloudflare is on, re-run §6 verification and append a dated "post-Cloudflare" row to PERFORMANCE.md / SECURITY.md verification tables.

---

## 9. Email security wiring (post-launch task)

Done at §2 of this file. Once SPF / DKIM / DMARC are live, monitor the DMARC RUA mailbox for the first 30 days. If alignment is consistent at 99%+, promote DMARC from `p=quarantine` to `p=reject`.

For ongoing email hygiene CT can subscribe to a free DMARC report aggregator (e.g. dmarcian's free tier). Optional, not blocking.
