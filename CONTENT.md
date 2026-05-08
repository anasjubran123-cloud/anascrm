# CONTENT.md — Convergent Technology corporate site

This file is the **master ledger of placeholders, required assets, and review checklists** for www.convergent.sa. Anything that needs human input — copy, brand asset, written approval, or legal sign-off — is tracked here. Search the codebase for `{{TODO` to find every inline placeholder; each is also recorded below.

The site is **offline during development** (`<meta name="robots" content="noindex, nofollow">` on every page; `public/robots.txt: Disallow: /`). Phase 7 flips both before public launch only after the items below are resolved.

---

## 1. Brand assets — required from CT

These come from the SharePoint **Convergent Technology Full Identity** folder; the SharePoint MCP only returns text content (PDF text, folder listings) so binaries cannot be pushed by Claude. Drop them into the repo paths below on this branch.

### 1.1 Logos (drop into `branding/` and `public/brand/`)

| Asset | SharePoint source | Repo path | Purpose |
|---|---|---|---|
| `CT GROUP.pdf` | CT Group Identity / LOGO | `branding/logos/CT-GROUP.pdf` | Vector master |
| `CT GROUP.png` (color) | CT Group Identity / LOGO | `public/brand/logo-ct-group.png` | Header logo, social cards |
| `CT GROUP Black.png` | CT Group Identity / LOGO | `public/brand/logo-ct-group-black.png` | Light-mode dark variant |
| `CT GROUP White.png` | CT Group Identity / LOGO | `public/brand/logo-ct-group-white.png` | Dark-mode + dark BGs |
| **SVG export from `CT GROUP.ai`** (recommended) | derive | `public/brand/logo-ct-group.svg` | Crisp at any size |
| `logo CT Vertical .png` | CT Group Identity / LOGO | `public/brand/logo-ct-vertical.png` | Square placements |

When the SVG lands, edit `src/components/layout/Logo.astro` to render `<img src="/brand/logo-ct-group.svg" alt="Convergent Technology" />` and remove the typeset CSS fallback. Until then the typeset version mirrors the brand-book lockup.

### 1.2 Cairo fonts (drop into `public/fonts/cairo/`)

| Asset | SharePoint source | Repo path |
|---|---|---|
| `Cairo-Regular.woff2` | CT Group Identity / CT GROUP GUIDE LINE / Fonts | `public/fonts/cairo/Cairo-Regular.woff2` |
| `Cairo-VariableFont_wght.ttf` | CT Group Identity / CT GROUP GUIDE LINE / Fonts | `public/fonts/cairo/Cairo-VariableFont_wght.ttf` |

`@font-face` declarations in `src/styles/tokens.css` reference these exact filenames. Browsers prefer the woff2 over the TTF; the variable TTF gives the full weight axis as a fallback.

The brand kit also contains Optima, Beatrice, Halcom, Cocogoose etc. — those are NOT used on the website. Cairo is the unified family per CT decision (2026-05-08).

### 1.3 Favicon + PWA icons

| Asset | Repo path | Notes |
|---|---|---|
| `favicon.svg` | `public/favicon.svg` | Placeholder ships now (red square + "C"); replace with the official mark when SVG arrives. |
| `apple-touch-icon.png` (180×180) | `public/apple-touch-icon.png` | Required by `BaseLayout.astro` `<link>`. |
| `site.webmanifest` | `public/site.webmanifest` | Already present; update icon entries when real PNGs arrive. |
| `og/default.png` (1200×630) | `public/og/default.png` | Default OG image. Phase 8 covers a programmatic generator option. |

### 1.4 Photography (Phase 8 placeholders → real assets)

The brand book calls out three buckets: **internal shots**, **external shots**, **lifestyle shots**. None are in the repo yet. Recommended placements:

- Home hero supporting image
- About section banner
- Sector cards (one per sector — optional)
- Project case-study covers (one per published case study)

Image-licensing rule: every photograph must be CT-supplied or CT-approved. Stock photography is allowed only with a documented licence on file.

---

## 2. Inline placeholders (search `{{TODO}}`)

These are text-level holes inside files. Replace inline.

### 2.1 About page

- `src/i18n/en.json` → `about.leadershipBody` — `{{TODO: leadership profiles — handover required}}`
- `src/i18n/ar.json` → `about.leadershipBody` — same.

Replacement: short paragraphs introducing the leadership team or a separate `Leadership` section with profile cards (Phase 4 component pattern reuses Card primitive). If CT prefers no leadership section at launch, delete the markup in `pages/{en,ar}/about.astro`.

### 2.2 Projects (case studies)

All three placeholder cards in `src/lib/content.ts` `placeholderProjects` and the matching MDX entries in `src/content/projects/`:

- `placeholder-bank-tier-iii` — banking
- `placeholder-government` — government
- `placeholder-edu` — education

Replace per case study **only after** written disclosure approval (CT brand & legal + named client). Suggested structure per master prompt §8: Client/sector · Challenge · CT scope · Solution · Technologies · Outcome · Photos · Metrics · Approval status.

### 2.3 Careers

- `src/content/careers/placeholder-senior-pm.{en,ar}.md` — replace with the live JD.
- `sampleRoles` array in `src/lib/content.ts` — add or remove roles; the page renders an empty state automatically when the array is empty.

### 2.4 Legal pages

Every legal page (`/legal/privacy`, `/legal/cookies`, `/legal/terms` × EN/AR) carries a draft banner and `{{TODO}}` markers for items requiring legal counsel:

- Lawful basis confirmation (privacy)
- Retention windows for inquiry data and careers data (privacy)
- List of sub-processors (privacy)
- Forum-selection / governing-law clause (terms)
- Cookie / analytics decisions before public launch (cookies)

Owner: CT legal counsel. Phase 7 ships the structural drafts; CT counsel must sign off before robots.txt is flipped to allow indexing.

### 2.5 Partners

`src/content/partners/*.json` — every partner has `"approved": false` and a "Display approval pending" note. Set `"approved": true` only after written confirmation. Tier or authorisation wording must NOT appear without a written confirmation from each partner; the ContactForm + footer / home strip all currently render names only.

---

## 3. Required external decisions

Tracked here so they don't fall through the cracks.

| Item | Decision needed | Phase | Owner | Default if undecided |
|---|---|---|---|---|
| Form vendor | Web3Forms (free) vs Formspree (free) vs Cloudflare Worker (later) | 6 | CT | Web3Forms — fastest to set up, no account on public IP |
| Form access key | Provision and add to `PUBLIC_CONTACT_FORM_ENDPOINT` env | 6 | CT | Form falls back to mailto:info@convergent.sa |
| hCaptcha site key | Provision (free tier) and add to env | 6 | CT | Site ships without captcha; honeypot + min-time still active |
| SPF/DKIM/DMARC | DNS records for the sending domain | 12 | CT IT | Documented in DEPLOY.md as a post-deploy task |
| Cloudflare onboarding | Move DNS to Cloudflare and configure SSL Full (strict) | 12 | CT IT | Site runs on HostGator-only at launch; swap path documented |
| Google Business Profile | Create / claim listing for HQ in Al Khobar | 8 | CT marketing | Listed in DEPLOY.md as a post-launch task |
| Bing Places | Same | 8 | CT marketing | Same |
| Search Console + Bing Webmaster | Verify ownership at launch | 12 | CT marketing | Steps in DEPLOY.md |
| Analytics decision | Cloudflare Web Analytics, Plausible self-host, or none | 8 | CT | Site ships with no analytics; cookie banner notes "no analytics yet" |

---

## 4. Local SEO assets (Phase 8 dependencies)

Compile a single source of truth per the master prompt §17.

- Official names: **Convergent Technology Company** (EN), **شركة التقنية المترابطة** (AR) ✅ confirmed.
- HQ address: `{{TODO: street + building + district + postcode for Al Khobar}}`
- Main phone: `{{TODO}}`
- WhatsApp number: `{{TODO}}`
- Business hours: `{{TODO}}`
- Google Maps URL: `{{TODO}}`
- Geo coordinates: `{{TODO}}`

These feed into the JSON-LD `LocalBusiness` block (Phase 8) and into Google Business Profile / Bing Places setup (Phase 12).

---

## 5. Copy review checklists

Use these as the final pass before launch.

### 5.1 Arabic copy

- [ ] Every page renders with `dir="rtl"` and `lang="ar-SA"`.
- [ ] Mixed bidi (Arabic + English + URLs + numbers + model numbers) renders correctly — sample sentences in About, Projects, Careers.
- [ ] Headlines do not use Latin negative tracking (handled in `global.css`).
- [ ] No untranslated English words in the AR locale (search the AR JSON for ASCII-only strings).
- [ ] Tone matches the brand voice — engineering, restrained, confident.

### 5.2 English copy

- [ ] No invented client names, project values, ISO numbers, certifications, partnership tiers, awards, testimonials, Saudization percentages, headcount, or vendor authorisation levels.
- [ ] Every adjective is defensible.
- [ ] Sentences end with periods, not em-dashes.
- [ ] Capitalisation matches the brand voice (sentence case, not Title Case).

### 5.3 Technical accuracy

- [ ] Capability names match how Convergent's pre-sales describes them in proposals (BoQs, RFQs).
- [ ] Sector names match the SAMA/CITC/Vision-2030 parlance the audience uses.
- [ ] No claim of certifications or partner tiers anywhere in the live copy.

---

## 6. Legal review checklist (CT counsel sign-off)

Each item below blocks the production launch (Phase 12).

- [ ] Privacy notice (EN + AR) — final wording approved.
- [ ] Cookie notice (EN + AR) — final wording approved.
- [ ] Terms of use (EN + AR) — governing law / forum-selection clause reviewed.
- [ ] Retention windows recorded in `SECURITY.md` match the privacy notice.
- [ ] Processors list is complete and accurate.
- [ ] Consent language on the contact form is sufficient under PDPL.
- [ ] Data Subject Request workflow is documented (in `OPERATIONS.md` Phase 11).

---

## 7. Maintenance — keeping this file honest

When you remove an inline `{{TODO}}`, also remove its row above. When you add a new placeholder, add it here in the same change. The launch checklist in Phase 12 fails the launch if any rows above remain unresolved without an explicit waiver from the relevant owner.
