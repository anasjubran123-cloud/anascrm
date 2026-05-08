# SECURITY.md — Convergent Technology corporate site

This document records the security posture of www.convergent.sa: the threat model, the controls we ship, the residual risks, and the verification steps that must run *for real* before any A/A+ claim appears anywhere.

The honesty rule from the master prompt applies here. Items below that say **Pending verification** are not yet validated; do not claim them.

---

## 1. System under protection

A static, bilingual marketing site for Convergent Technology Company at **www.convergent.sa**. No databases, no admin panel, no PHP, no server-side application logic. Astro-built static HTML/CSS/JS, served by Apache on HostGator shared hosting. **Cloudflare is not yet in front of the origin** and is documented as a Phase 12 add-on; controls below assume HostGator-only at launch and call out the Cloudflare-add path explicitly.

The contact form posts to a third-party form vendor (Web3Forms by default; Formspree is the documented alternative). Phase 6 wired the env vars; the site falls back to `mailto:info@convergent.sa` if no endpoint is configured.

---

## 2. Threat model (compact)

| Threat | Likelihood | Impact | Primary control(s) |
|---|---|---|---|
| Form spam / bot submission | High | Lead-pipeline pollution; vendor-quota burn | hCaptcha (when configured), honeypot, min-time-to-submit, vendor-side rate limiting |
| Phishing using the brand | Medium | Reputational | DMARC `p=quarantine` then `p=reject` (Phase 12); `info@` is the only public email |
| Subdomain takeover | Low | Reputational | Restricted host header in `.htaccess`; subsidiary subdomains must each maintain their own DNS hygiene |
| TLS downgrade / MITM | Low (modern browsers) | Confidentiality | HTTPS enforced via 301; HSTS staged; AutoSSL renewal monitored |
| Indexing of pre-launch site | Medium | SEO mess + brand damage | `noindex` meta + header + `robots.txt: Disallow: /` until Phase 7 flip |
| XSS via injected partner content | Low (no UGC) | Account compromise | CSP (Report-Only → enforce); strict autoescaping in Astro; no inline event handlers |
| Source disclosure (`.git`, `.env`) | Low | Code & secret leak | `.htaccess` dotfile blocks; secrets are not in the build |
| DoS / volumetric | Medium until Cloudflare lands | Availability | HostGator's mod_security only; Cloudflare adds WAF + Bot Fight Mode + rate limits when onboarded |
| Data exposure via form vendor | Medium | PII in third-party hands | Sub-processor disclosed in Privacy notice; data minimisation on the form (no file uploads at v1) |
| Stale dependency CVE | Low | Build-time only (no runtime) | `npm audit` in CI fails high/critical; renovate / dependabot can be added in Phase 9 |

---

## 3. Controls

### 3.1 Static architecture (primary control)

The site has no server-side application logic. There is no DB to inject, no PHP to execute, no admin UI to compromise. The blast radius of an Apache misconfiguration or a CVE is bounded to the read-only static HTML output. Everything in this file is layered on top of that primary control.

### 3.2 Transport & host

- HTTPS enforced via `.htaccess` (HTTP → HTTPS 301). Implemented.
- Canonical host: `www.convergent.sa`. Apex 301 → www. Implemented.
- HostGator AutoSSL / Let's Encrypt issues and renews the certificate. Configured in cPanel; verify post-deploy.
- HSTS: starts at `max-age=300`. Bump to `max-age=31536000` after 1–2 weeks of clean operation; add `includeSubDomains` only after every active subdomain is HTTPS-clean. **`preload` is NOT auto-submitted to the preload list** — owner approval required.

### 3.3 HTTP security headers

Shipped via `public/.htaccess`:

| Header | Value | Note |
|---|---|---|
| `Strict-Transport-Security` | `max-age=300` | Staged; bump after observation. |
| `X-Content-Type-Options` | `nosniff` | |
| `X-Frame-Options` | `DENY` | Plus CSP `frame-ancestors 'none'` for redundancy. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | |
| `Cross-Origin-Opener-Policy` | `same-origin` | |
| `Cross-Origin-Resource-Policy` | `same-origin` | |
| `Permissions-Policy` | locks down camera, mic, geolocation, payment, USB, etc. | |

### 3.4 Content Security Policy

CSP is shipped **in Report-Only mode at launch** so we can observe violations from real traffic before enforcing. Promotion to enforcement is a single comment-toggle in `.htaccess`.

Static hosting cannot generate per-request nonces, so the policy uses hash-based allowances for any inline content. The only inline script today is the FOUC-prevention theme bootstrap in `src/components/layout/ThemeBootstrap.astro`. Its sha256 hash lives in the `script-src` directive; recompute it whenever the script body changes:

```bash
# from the project root, after a build:
node -e "console.log('sha256-' + require('crypto').createHash('sha256').update(require('fs').readFileSync('/path/to/inline/script.js')).digest('base64'))"
```

If we add Cloudflare later, Transform Rules can serve as a backup carrier of the policy; document the current values in `DEPLOY.md`.

### 3.5 `.htaccess` hardening

`public/.htaccess` ships with:

- `Options -Indexes -ExecCGI` (no directory listing, no script execution).
- `ServerSignature Off`.
- Dotfile and config-file blocks (`.env`, `.git`, `node_modules`, `package*.json`, `astro.config*`, `tailwind.config*`, `tsconfig*`, source maps, npmrc/yarnrc/eslintrc/prettierrc, our `.md` runbooks).
- Custom 404 → `/en/404`.
- Long cache for hashed assets, `no-cache` for HTML, frequent revalidation for `robots.txt` / `sitemap.xml`.
- Brotli + gzip via `mod_brotli` and `mod_deflate`.
- Allowed extension mapping for `.avif`, `.webp`, `.svg`, `.woff2`, `.webmanifest`.

### 3.6 Forms

- Honeypot field hidden via CSS `display:none`-equivalent + `aria-hidden`. Bots populate it; real users don't.
- Min-time-to-submit guard at 3 seconds; submissions faster than that are dropped client-side.
- Server-side validation runs at the form vendor (Web3Forms / Formspree); CT must keep the vendor's spam controls enabled.
- hCaptcha widget renders only when `PUBLIC_HCAPTCHA_SITE_KEY` is set. Until then we lean on honeypot + min-time + vendor controls (recorded as a residual risk below).
- No file uploads at v1. If file uploads are added later they require: server-side MIME check, size limit, virus scan.
- No SMTP credentials in the client bundle; no PHP mail script anywhere.

### 3.7 Dependencies & supply chain

- `package-lock.json` lands once `npm install` runs locally (sandbox blocked the registry; user runs install in their environment). Commit the lockfile after first install.
- `npm audit` ought to run in CI; Phase 9 wires that with a fail-on-high gate.
- Self-host all assets where possible. The hCaptcha script is the only third-party JS at launch; it loads only when configured. SRI is not currently emitted on it because hCaptcha's URL does not publish stable hashes; this is documented as a residual risk.
- No tracking pixels. Analytics is deferred and gated on a granular consent banner that ships when CT picks an analytics tool.

### 3.8 Privacy (PDPL-aware)

See `src/pages/{en,ar}/legal/privacy.astro` and `cookies.astro`. All legal pages currently carry a draft banner; they are **pending CT legal counsel review** before public launch. Highlights:

- Lawful basis: consent (form's required consent checkbox) + legitimate interest in commercial communication.
- Retention: `{{TODO: confirm windows.}}` Default proposal — 24 months for inquiry data, 12 months for unsuccessful careers applications.
- Sub-processors: `{{TODO: complete list}}` — at minimum the form vendor, the hosting provider, and Cloudflare when added.
- Data subject rights: access, correction, deletion, restriction, objection — handled by emailing `info@convergent.sa`. The DSR workflow lives in `OPERATIONS.md` (Phase 11).

### 3.9 Cookie consent

Currently the site sets only two `localStorage` keys (`ct-theme`, `ct-locale`) used strictly for user preferences. **No analytics or marketing scripts run.** Per the master prompt §14.10 the cookie banner can therefore be reduced to a notice. When analytics is later added:

- Granular categories (necessary / analytics / marketing).
- Non-essential default OFF.
- No analytics or marketing script loads before consent.
- Consent persisted in `localStorage`; user can change anytime.

---

## 4. Operational controls

### 4.1 Backups

Git is the source of truth for code and content. HostGator weekly backups are enabled (cPanel → Backups). DEPLOY.md documents the restore procedure step-by-step. Verify quarterly that a restore actually works by spinning up a fresh subdomain from the backup tarball.

### 4.2 Monitoring

At launch:
- HostGator's built-in uptime alert (free) on `https://www.convergent.sa`.
- Browser-side error visibility — none beyond the user's console.

When Cloudflare lands:
- Cloudflare Web Analytics (free, no cookie).
- Cloudflare alerting for spike traffic / WAF events.

### 4.3 Incident response (compact)

- **Defacement** — pull the most recent clean Git commit's `dist/`, re-zip, and re-upload via cPanel File Manager. Rotate any cPanel / API credentials. Document in an incident log.
- **Form spam / vendor abuse** — flip the form to a stricter hCaptcha threshold; if persistent, deploy a temporary Cloudflare Worker between the form and the vendor.
- **SSL break** — re-issue from cPanel's SSL/TLS Status page; if AutoSSL is stuck, manually request a Let's Encrypt cert.
- **DNS change** — confirm with the registrar; reset NS records; re-run mxtoolbox checks.
- **Malware / unexpected files in `public_html/`** — immediately `git diff` against the last clean deploy, replace with the clean build, rotate credentials, and trigger a full HostGator security scan.
- **Cloudflare false positive** (post-onboarding) — use Cloudflare Logs to find the rule, exempt the necessary path, and document the change.

The incident log goes in `OPERATIONS.md` (Phase 11) and gets retained for 24 months.

### 4.4 Disclosure

`/.well-known/security.txt` ships at launch and points reports to `info@convergent.sa`. Update the `Expires` value annually.

---

## 5. Residual risks (carry honestly)

| Risk | Mitigation strategy | Owner |
|---|---|---|
| Form vendor outage takes the contact form offline. | Mailto fallback documented; CT pre-sales monitors the inbox. | CT |
| Free-tier form quotas exceeded. | Vendor monitoring; switch to next vendor or to a Cloudflare Worker. | CT |
| Edge WAF / rate limiting absent until Cloudflare lands. | mod_security at HostGator + form-level controls; planned migration. | CT IT |
| Inline FOUC script complicates strict CSP. | Hash-based allowance; rotate hash on edits. | Dev |
| hCaptcha SRI not stable. | Loaded only post-consent on form pages, never globally. | Dev |
| Partner logos before written approval would be a reputational risk. | Site stays offline until approvals land; logos hidden behind `approved: true` flag in content collection. | CT marketing + CT legal |

---

## 6. Post-deployment verification (run for real before claiming)

- [ ] `securityheaders.com/?q=https://www.convergent.sa` — target A/A+. **Pending verification.**
- [ ] `ssllabs.com/ssltest/analyze.html?d=www.convergent.sa` — target A/A+. **Pending verification.**
- [ ] Lighthouse mobile + desktop, both locales, Home / Contact / a Capabilities page / a Project detail / 404 — Performance / A11y / Best Practices / SEO ≥ 95. **Pending verification.**
- [ ] OWASP ZAP baseline scan — no high findings. **Pending verification.**
- [ ] mxtoolbox.com — SPF, DKIM, DMARC pass. **Pending verification.**
- [ ] Manual: every page returns the expected security headers (curl -I).
- [ ] Manual: production `robots.txt` allows crawl + references `sitemap.xml`; staging `robots.txt` disallows everything.
- [ ] Manual: CSP Report-Only tail clean for ≥ 1 week before flipping to enforcement.

---

## 7. When Cloudflare lands

- DNS proxied through Cloudflare; SSL/TLS mode `Full (strict)`.
- "Always Use HTTPS" + "Automatic HTTPS Rewrites" on.
- Bot Fight Mode on (free tier).
- WAF managed rule set on.
- Rate limit `/contact` and `/careers/apply`. **Verify rate-limit allowance on the free tier before promising it in this file.**
- Transform Rules: mirror the `.htaccess` security headers as a backup carrier. **Verify Transform Rules availability on the free tier first.**
- Page Rules / cache rules: aggressive on hashed assets, bypass on HTML.
- Workers: optionally move the form endpoint to a Cloudflare Worker for tighter rate-limit + per-IP throttling.
- HSTS: bump max-age, then `includeSubDomains`, then (with explicit owner approval) preload.

When the Cloudflare swap completes, append a dated row to the verification list above and re-run all six checks.
