# TESTING.md — Convergent Technology corporate site

What we test, how to run it locally, and what CI runs.

## Local commands

```bash
npm install                # one-time
npm run dev                # http://localhost:4321 — try /en and /ar
npm run build              # static output in dist/
npm run preview            # serve dist/ locally (used by Playwright)
npm run typecheck          # astro check (TypeScript strict)
npm run lint               # ESLint over .astro / .ts / .tsx / .js / .mjs / .cjs
npm run format             # rewrite with Prettier (Astro + Tailwind plugins)
npm run format:check       # Prettier without rewriting (CI gate)
npm test                   # Playwright smoke + axe over /en/ + /ar/ pages
```

The Astro registry blocks in some sandboxed environments returned 403 on the first install attempt; if `npm install` errors with `E403` from `registry.npmjs.org`, run install on a network with full registry access (your laptop / a CI runner) and commit `package-lock.json`.

## Browser matrix

| | Why |
|---|---|
| Chromium 120+ desktop | Default Lighthouse / Web Vitals reference. |
| Chromium mobile (Pixel 7 emulation) | iPhone SE width covers 375 px; Pixel 7 emulates ~412 px and Android quirks. |
| Safari 17+ | Manual smoke each release (we don't run a Safari Playwright project — adds runtime). |
| Firefox 120+ | Manual smoke each release. |
| Edge | Inherits Chromium. |

If you add a Playwright project for Safari/Firefox, expect the build matrix to roughly double in CI minutes.

## What `npm test` covers

`tests/smoke.spec.ts`:

1. **Page-level smoke** — every public page in EN and AR returns 2xx, has a unique `<title>`, has at least one `<h1>`, and the `<html dir>` matches the locale.
2. **Skip-to-content** — Tab from the freshly-loaded page focuses the skip link first.
3. **Theme toggle** — clicking it persists the choice to `localStorage`.
4. **Accessibility (axe)** — `/en/`, `/en/contact`, `/ar/`, `/ar/contact` must produce zero axe violations. axe rules are a subset of WCAG 2.2 AA — this catches a meaningful slice of regressions but does not replace manual a11y review.
5. **`robots.txt` and `sitemap-index.xml`** — both reachable on the preview server.

## RTL and bidi checks (manual)

Run through these on every PR that touches layout, components, or copy:

- [ ] `/ar/...` renders with `dir="rtl"` and Arabic typography.
- [ ] No hardcoded `left:` / `right:` (use logical properties — `inset-inline-start`, `inset-inline-end`, `padding-inline`, `margin-inline`).
- [ ] Mixed bidi (Arabic + English + URLs + numbers + model numbers) renders without breakage on About, Projects, Careers.
- [ ] Mobile menu opens to the correct side in RTL.
- [ ] Business Units dropdown's chevron rotates the right way in RTL.

## Forms test (manual)

- [ ] Submit a real test lead from `/en/contact`. Confirm it lands at `info@convergent.sa`.
- [ ] Submit from `/ar/contact`. Confirm Arabic message body renders correctly in the inbox.
- [ ] Empty submit triggers inline error states (name, email, message all flagged).
- [ ] Honeypot test: open DevTools, fill the hidden `company_url` field with text, then submit a valid form — submission is silently dropped.
- [ ] Min-time-to-submit: programmatically submit within 1 second of load — submission is dropped.
- [ ] hCaptcha (if `PUBLIC_HCAPTCHA_SITE_KEY` is set) blocks submission until solved.

## WCAG 2.2 AA checklist

Run through these before each release. The new 2.2 criteria are highlighted.

- [ ] Skip-to-content link works keyboard-only.
- [ ] Visible focus rings on every interactive element (`:focus-visible` is set in `global.css`).
- [ ] **2.2 — Focus not obscured (minimum):** focused element is never hidden behind sticky header.
- [ ] **2.2 — Target size (minimum):** every interactive target is ≥ 24×24 CSS px (44×44 preferred). Buttons/inputs are 40–44 px tall by default.
- [ ] **2.2 — Consistent help:** Contact link is in the header on every page, in the same spot.
- [ ] **2.2 — Redundant entry avoided:** the contact form does not ask the user to repeat data.
- [ ] **2.2 — Accessible authentication:** no logins on the public site; if added, no cognitive function tests beyond simple username/password.
- [ ] Heading hierarchy is not broken (only one `<h1>` per page; `<h2>` follows `<h1>`).
- [ ] Form labels are explicit (`<label for>`).
- [ ] Errors are announced via `aria-describedby` and `role="status"`.
- [ ] Decorative images use `alt=""`.
- [ ] Body text contrast ≥ 4.5:1; large text ≥ 3:1.
- [ ] `prefers-reduced-motion` respected (animations zeroed out via `tokens.css`).

Run `npx pa11y https://staging.convergent.sa/en/` for an automated audit before launch (Phase 11).

## Performance checks (manual, pre-launch)

See `PERFORMANCE.md` §"Verification".

## Deployment checks (manual, post-launch)

See `SECURITY.md` §6 and `DEPLOY.md` (Phase 12).

## CI

`.github/workflows/ci.yml` runs:

1. **build** — install, typecheck, lint (informative), format check (informative), build, audit (informative).
2. **e2e** — install Playwright browsers, build, run `npm test` against the preview server, upload the Playwright report on failure.

Lint, format, and audit start as `continue-on-error: true` to avoid blocking the first PR while the team converges on rules. Flip them to required after a clean PR or two.

CI does not depend on any paid-tier secret. The form vendor and hCaptcha keys are not needed for CI to pass — the smoke test covers the form skeleton without submitting.
