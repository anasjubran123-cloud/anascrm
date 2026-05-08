# Convergent Technology — Corporate Website

Mother-company website for **Convergent Technology Company / شركة التقنية المترابطة**, deployed at **www.convergent.sa**. Static, bilingual (Arabic + English), built with Astro and Tailwind, served from HostGator. Cloudflare in front of HostGator is planned but not yet provisioned.

This repository ships the **mother site only**. Each business unit (AV, IT, Data Centers, Landscape) lives on its own subdomain and will be built separately. The mother site renders link-out cards to those subdomains via a single source of truth in `src/config/business-units.ts`.

## Status

This is **Phase 1 — Scaffold** of a multi-phase build (see `/root/.claude/plans/so-we-will-go-noble-valiant.md`). The site is intentionally **offline during development** — no public exposure until design and content are signed off:

- `<meta name="robots" content="noindex, nofollow">` on every page
- `public/robots.txt` returns `Disallow: /`
- Phase 7 flips both for production launch

## Stack

| | |
|---|---|
| Framework | Astro 5 (static output, MDX content collections) |
| Styling | Tailwind CSS 3 + CSS custom-property design tokens (`src/styles/tokens.css`) |
| Type safety | TypeScript strict (`astro check`) |
| i18n routing | Astro `i18n` config with `/en/...` and `/ar/...` mirrors, `prefixDefaultLocale: true` |
| Typography | Cairo (unified EN + AR), self-hosted, OFL — see `branding/BRAND_GUIDELINE_EXTRACT.md` |
| Brand colour | ROSO red `#D00F18` (CT GROUP), tokenised in `src/styles/tokens.css` |
| Hosting | HostGator shared, behind Cloudflare (later) |

Versions are pinned via `package-lock.json` after the first install. Refer to `package.json` for the declared ranges.

## Local development

```bash
nvm use 22         # or any Node ≥ 20
npm install
npm run dev        # http://localhost:4321 — try /en and /ar
npm run build      # static output in dist/
npm run preview    # serve dist/ locally
npm run typecheck  # astro check
```

## Repository layout

```
.
├── astro.config.mjs            # Astro + integrations + i18n routing
├── tailwind.config.cjs         # Tailwind utilities mapped to tokens.css vars
├── tsconfig.json               # Strict TS, path aliases (@components, @lib, etc.)
├── branding/
│   └── BRAND_GUIDELINE_EXTRACT.md  # Provenance + extracted brand decisions
├── public/
│   └── robots.txt              # Currently Disallow: / (dev posture)
└── src/
    ├── components/layout/      # Logo, Header, Footer (Phase 1 baseline)
    ├── config/
    │   ├── site.mjs            # Site URL/locales (consumed by astro.config)
    │   ├── site.ts             # Typed site config (incl. info@convergent.sa)
    │   └── business-units.ts   # Single source for AV/IT/DC/Landscape links
    ├── content/                # MDX collections (capabilities, projects, news, careers, partners)
    ├── i18n/                   # en.json, ar.json — flat string dictionaries
    ├── layouts/
    │   └── BaseLayout.astro    # lang/dir/hreflang/canonical/OG, theme bootstrap
    ├── lib/
    │   └── i18n.ts             # Locale helpers (dirFor, htmlLangFor, localizedPath, …)
    ├── pages/
    │   ├── index.astro         # Locale redirect
    │   ├── 404.astro
    │   ├── en/index.astro      # Phase 1 home (hero only)
    │   └── ar/index.astro      # Mirror
    └── styles/
        ├── tokens.css          # Single source of truth for colour, type, motion
        └── global.css          # Tailwind imports + base resets + skip-link
```

## Brand

The brand palette, typography, and wordmark structure are extracted from the official guideline (`Convergant GuideLine.pdf` v0.1, Oct 2025) — full notes in `branding/BRAND_GUIDELINE_EXTRACT.md`.

The Phase 1 logo is a CSS typeset wordmark that mirrors the guideline's "Convergent / T E C H N O L O G Y" lockup, sized to brand minimums. Once the official logo binaries land in `branding/` (PNG, PDF, ideally an SVG exported from `CT GROUP.ai`), the `<Logo>` component in `src/components/layout/Logo.astro` swaps to render the file directly.

## i18n

- Routes mirror under `/en/...` and `/ar/...`. The `/` root redirects to `/en` (default locale, see `src/config/site.mjs`).
- `<html lang="ar-SA" dir="rtl">` for Arabic, `<html lang="en-SA" dir="ltr">` for English.
- `hreflang` pairs and `x-default` are emitted by `BaseLayout.astro`.
- All strings live in `src/i18n/{en,ar}.json`. Components consume them via `dictFor(locale)` from `src/lib/i18n.ts`.

## Phases (gates)

| Phase | Scope | State |
|---|---|---|
| 0 | Audit & plan | done |
| 1 | Astro + Tailwind scaffold, bilingual routing skeleton, base layout, tokens | **current** |
| 2 | Design system (full tokens, dark mode, primitives) | next |
| 3 | Header / Footer / mobile menu / language switcher / theme toggle / a11y baseline | |
| 4 | Core pages EN + AR | |
| 5 | Content collections + `CONTENT.md` | |
| 6 | Forms (info@convergent.sa via free vendor, hCaptcha, honeypot) | |
| 7 | Security hardening (.htaccess, CSP, headers, security.txt, legal drafts) | |
| 8 | SEO + performance | |
| 9 | Tests + CI | |
| 10 | Migration & redirects (only if existing URLs need preserving) | |
| 11 | HostGator staging + review | |
| 12 | Launch package | |

Each phase ends at a gate. The full plan is at `/root/.claude/plans/so-we-will-go-noble-valiant.md`.

## What this site is **not**

- It is **not** the AV, IT, Data Center, or Landscape subsidiary website. Each lives separately on its own subdomain. This codebase only links to them.
- It is **not** running on WordPress / PHP / a database. Architecture is intentionally static.
- It is **not** publicly indexed during development. Search-engine visibility is gated to Phase 7+.

## Decisions on file

Recorded in `branding/BRAND_GUIDELINE_EXTRACT.md` and the plan file. Highlights:

- Canonical domain: `www.convergent.sa` (apex 301 → www, configured in `.htaccess` Phase 7).
- Lead routing: `info@convergent.sa`.
- Cloudflare: not at launch; site Cloudflare-ready, swap path documented in Phase 12.
- Optima (paid) replaced by Cairo (free, OFL) per CT instruction (2026-05-08).
- Partner logos: included without tier claims; written approvals are a launch-checklist item.
- Case studies: dummy placeholders for now; real disclosure after written approval.
