# OPERATIONS.md — Convergent Technology corporate site

How this site is governed, who owns what, how leads are handled, and how it stays healthy after launch.

---

## 1. Governance

### 1.1 Owners

| Role | Owner | Responsibility |
|---|---|---|
| Business owner | `{{TODO: name}}` | Strategy, brand voice, launch sign-off. |
| Technical owner | `{{TODO: name}}` | Build, deploy, monitoring, incident response. |
| Content owner | `{{TODO: name}}` | Copy, news posts, project case studies. |
| Security owner | `{{TODO: name}}` | SECURITY.md, security.txt updates, incident triage. |
| SEO owner | `{{TODO: name}}` | Search Console, Bing Webmaster, content optimisation. |
| Forms owner | `{{TODO: name}}` | Lead routing, hCaptcha, vendor account, CRM handover. |
| Legal owner (CT counsel) | `{{TODO: name}}` | Privacy, cookies, terms — final wording before public launch. |

Approval authority for **public release of a content change** (case study, news post, partner logo, role posting) is the business owner unless explicitly delegated.

### 1.2 Decision log

Material decisions are tracked here. Each row is dated and the responsible owner is named.

| Date | Decision | Owner |
|---|---|---|
| 2026-05-08 | Mother site only this engagement; the four business units (AV/IT/DC/Landscaping) live on subdomains and are linked-out, not duplicated. | Business owner |
| 2026-05-08 | Cloudflare deferred; site launches on HostGator only with documented swap path. | Technical owner |
| 2026-05-08 | Optima font replaced by Cairo (free, OFL) for both EN and AR. | Business owner |
| 2026-05-08 | Partner logos shown without tier claims; written approvals collected separately. | Business + Legal |

---

## 2. Lead management

The contact form posts to a free-tier vendor (Web3Forms by default; Formspree as fallback) which forwards to **info@convergent.sa**.

### 2.1 Routing by inquiry category

| Category | Primary recipient | Backup | SLA |
|---|---|---|---|
| DC design & build | DC business unit pre-sales | Group pre-sales | 1 business day |
| DCIM | DC business unit pre-sales | Group pre-sales | 1 business day |
| UPS & power | DC business unit pre-sales | Group pre-sales | 1 business day |
| Precision cooling | DC business unit pre-sales | Group pre-sales | 1 business day |
| Modular DC | DC business unit pre-sales | Group pre-sales | 1 business day |
| Low-current systems | IT business unit pre-sales | Group pre-sales | 1 business day |
| CCTV / access control | IT business unit pre-sales | Group pre-sales | 1 business day |
| Audiovisual | AV business unit pre-sales | Group pre-sales | 1 business day |
| Maintenance & support | Operations team | Group pre-sales | 1 business day |
| Partnership | Business owner | Group pre-sales | 2 business days |
| Careers | HR | Business owner | 5 business days |
| Other | Group pre-sales | Business owner | 1 business day |

Routing happens in the form vendor's settings (one mailbox + a category-driven Zapier/Make rule, or a small Cloudflare Worker post-onboarding). The `info@convergent.sa` mailbox stays the single inbound address — the routing rules live elsewhere.

### 2.2 Qualification fields captured

Every submission carries: name, company, email, phone (optional), inquiry category, free-text message, and the submitter's `consent` flag. Optional fields the form can be extended with at any time (Phase 6+ — already supported by the form vendor): project location, stage (RFI / RFP / RFQ / scoping), timeline, new-build vs. existing, budget range, urgency, preferred contact channel.

### 2.3 RFQ / RFP handling

Treat any submission marked "Project stage = RFQ" or with an attached document (Phase 7+ if file uploads are enabled) as a tender lead. Hand to the pre-sales lead within the SLA above. Record outcomes in CT's CRM.

### 2.4 Careers handling

Career inquiries forward to HR with the submitter's email and CV attachment (when file uploads are enabled). Default retention for unsuccessful applications is 12 months unless the candidate consents to longer holding for future roles. Detailed handling lives in CT's HR policy.

### 2.5 Archive

Form submissions older than the retention window (default 24 months for inquiries, 12 months for careers) are deleted. The form vendor's data-export view supports periodic offline archive to a controlled CT location. Document who runs the archive in `{{TODO}}`.

---

## 3. Maintenance schedule

### 3.1 Weekly

- [ ] Inbox sweep on `info@convergent.sa` — every lead acknowledged inside SLA.
- [ ] Form vendor dashboard — submission volume vs. quota; spam rate; abuse signals.
- [ ] Glance at HostGator uptime alert log.

### 3.2 Monthly

- [ ] Review analytics (when enabled) — top pages, top sources, AR vs. EN split, contact-form conversion. Decide if any content needs sharpening.
- [ ] Check Search Console + Bing Webmaster for crawl errors, manual actions, structured-data warnings.
- [ ] Run a broken-link sweep with `linkinator` on the deployed site.
- [ ] Run Lighthouse on Home + Contact (mobile + desktop, both locales). Compare to PERFORMANCE.md targets.

### 3.3 Quarterly

- [ ] Backup restore drill — pull a HostGator backup tarball and stand it up on a fresh subdomain. Confirm the site renders.
- [ ] Dependency upgrade pass — bump Astro/Tailwind/integrations to latest patch; run typecheck + tests + build.
- [ ] CSP review — read the Report-Only logs (when Cloudflare is in front, this is in the Cloudflare dashboard; until then, sample with a one-off script).
- [ ] Privacy notice / cookies notice review — update if processors or behaviour changed.

### 3.4 Annually

- [ ] Renew `Expires` field in `public/.well-known/security.txt`.
- [ ] Full a11y audit (axe + manual WCAG 2.2 AA checklist) before any major redesign.
- [ ] Review owner roster in §1.1 — anyone who left rotates out.
- [ ] Decide whether to keep, retire, or refresh the existing 12-month-old copy.

### 3.5 Event-driven

- A new partner approves logo display → set `approved: true` in `src/content/partners/<name>.json`, push, deploy.
- A new case study is ready → MDX file lands in `src/content/projects/`, marked `approved: true`, deploy.
- An open role lands or closes → MDX file in `src/content/careers/` flips `open` and the page renders/hides automatically.

---

## 4. Analytics review (when enabled)

Today: site does not run any analytics. Cookie banner notes "no analytics yet" by virtue of the cookies notice (see `src/pages/{en,ar}/legal/cookies.astro`).

When CT picks an analytics tool (Cloudflare Web Analytics is the recommended free option after Cloudflare onboards; Plausible Community / self-hosted Umami are alternatives):

- Tracking is **post-consent only**. The cookie banner will be added in the same change.
- Track: contact-form starts and submits, RFQ/RFP CTA clicks, WhatsApp/email/phone clicks, service & case-study visits, careers application starts, AR vs. EN usage, top traffic sources.
- Monthly review summarises the above into one page in CT's internal wiki.

---

## 5. Backups & rollback

- Git is the source of truth for code and content.
- HostGator weekly backups are enabled; the technical owner verifies the most recent backup tarball is intact each month.
- Rollback drill (run quarterly):
  1. `git checkout` the last known good commit on the build server.
  2. `npm install && npm run build`.
  3. Zip `dist/`, upload via cPanel File Manager, extract over `public_html/`.
  4. Confirm a smoke pass (Home + Contact in both locales) and a `securityheaders.com` check.

If a deploy goes wrong mid-launch, `dist/` from the previous build is the rollback artefact — keep the previous build's `dist.zip` archived for 30 days.

---

## 6. Incident escalation

| Level | Trigger | Owner | Action |
|---|---|---|---|
| L0 — degradation | Single page error / broken link | Technical owner | Fix in next deploy. |
| L1 — feature outage | Contact form down | Forms owner | Switch vendor or fall back to mailto:; notify business owner. |
| L2 — site outage | Site unreachable for > 30 min | Technical owner | Open ticket with HostGator; consider rollback; notify business owner + security owner. |
| L3 — security event | Defacement, malware, credential leak | Security owner | Run `SECURITY.md` §4.3; rotate creds; notify legal. |
| L4 — legal / regulatory | DSR, takedown notice, regulator inquiry | Legal owner | Engage CT counsel; respond within statutory window. |

Escalation contacts and out-of-hours numbers live in CT's internal directory, not in this file.

---

## 7. Staging workflow

The `staging.convergent.sa` subdomain runs the same build as production, gated by HTTP basic auth and `X-Robots-Tag: noindex,nofollow` (see `public/staging.htaccess` and `public/staging-robots.txt`).

Review flow before any production change:

1. Push to `claude/ct-corporate-website-YFYF2`.
2. Build locally and upload to staging (or run a CI deploy step once configured).
3. Send the staging URL + basic-auth creds to reviewers.
4. Reviewers sign off in the related GitHub PR or via email.
5. Promote to production by re-uploading `dist/` to `public_html/`.

Do not promote to production without a clean staging review.
