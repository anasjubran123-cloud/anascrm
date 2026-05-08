# PERFORMANCE.md — Convergent Technology corporate site

## Targets (mobile, throttled)

| Metric | Target | Source |
|---|---|---|
| Lighthouse — Performance | ≥ 95 | Master prompt §16 |
| Lighthouse — Accessibility | ≥ 95 | |
| Lighthouse — Best Practices | ≥ 95 | |
| Lighthouse — SEO | ≥ 95 | |
| LCP | < 2.0 s | Core Web Vitals |
| INP | < 200 ms | |
| CLS | < 0.05 | |
| First-load JS | < 100 KB gzipped per route | |

These are **targets, not claims**. The honesty rule from `SECURITY.md` and the master prompt applies: numbers above are not asserted as met until Lighthouse runs against a deployed build of the site. Phase 12's launch checklist runs the actual measurements.

---

## Architecture choices that drive performance

- **Astro static rendering**, single-file HTML output per route. No SSR cold starts; no client-side router; no hydration unless explicitly requested.
- **Minimal hydration**. The handful of interactive widgets (theme toggle, mobile menu, business-units dropdown, language switcher) are small inline scripts in their respective Astro components — not React islands. They ship as ~3-6 KB of vanilla JS each, post-minification, and are bundled with their owning components rather than as a global runtime.
- **Self-hosted Cairo** with `font-display: swap`. Latin and Arabic both come from a single variable file (`Cairo-VariableFont_wght.ttf`) plus a single `Cairo-Regular.woff2`; users only fetch one woff2 in the common case.
- **Logical CSS properties** throughout, so RTL doesn't ship a second stylesheet.
- **CSS custom properties** in `tokens.css` — Tailwind utilities reference them, so dark-mode and theme swaps don't ship a second theme file.
- **No third-party CSS**. No Tailwind typography plugin (a hand-written `Prose.astro` covers long-form content). No utility CSS framework alongside Tailwind. No icon font.

---

## Image strategy

- Use `<Image>` from `astro:assets` for all content imagery. Astro emits AVIF first, WebP second, and the original format last as a fallback — picked automatically.
- Lazy by default. The single LCP image per page (typically the home hero supporting image, when one ships) is marked `loading="eager"` and given a `fetchpriority="high"` hint.
- Photography for project case studies and sector cards lands in Phase 5/Phase 8 once CT supplies licensed photography (see `CONTENT.md` §1.4).

---

## Font strategy

- One family (Cairo) covers EN + AR, removing a second @font-face fetch.
- Subset later (Phase 8 optimisation): split Latin and Arabic woff2s so the browser only fetches the script it renders. The brand kit's source files don't ship subsets, so we keep this as an optional optimisation rather than a launch-blocking task.
- `font-display: swap` for all weights, so the page never blocks on a font.
- Optional `<link rel="preload" as="font">` for the LCP weight (likely 700 for the H1) — added in Phase 8 once the actual woff2 ships and we know the exact filename hash.

---

## JS budget

| Route | Estimated client JS | Notes |
|---|---|---|
| `/en/`, `/ar/` (home) | ~ 8–12 KB | theme toggle + mobile menu + BU dropdown + lang switcher |
| `/en/contact`, `/ar/contact` | ~ 12–18 KB | adds the form's own validation script + (optional) hCaptcha widget bootstrap |
| All other routes | ~ 6–10 KB | header chrome only |

These numbers are estimates from the source size of the Astro components. Real values land after the first `npm run build`; record them in this file then. Hard fail in CI if a route exceeds 100 KB gzipped.

---

## Caching

- Hashed assets (CSS, JS, fonts, images): `Cache-Control: public, max-age=31536000, immutable` — set in `public/.htaccess`.
- HTML: `no-cache, must-revalidate`. A redeploy is reflected on the next request.
- `robots.txt` and `sitemap.xml`: `max-age=3600`.

When Cloudflare lands, mirror these rules at the edge with Cache Rules (free tier supports this) so HostGator only serves cache-misses.

---

## Compression

- Apache `mod_brotli` first, `mod_deflate` as a fallback. Both shipped in `.htaccess`.
- HostGator's mod_brotli availability varies by plan — verify post-deploy with a `curl -I -H 'Accept-Encoding: br' https://www.convergent.sa/en/` and check the `Content-Encoding` header.

---

## Post-launch monitoring

At launch (HostGator-only):

- Synthetic monitoring via a free uptime check (UptimeRobot / similar, free tier) on `https://www.convergent.sa/en/` and `/ar/`. Configured in `OPERATIONS.md`.
- Manual Lighthouse runs on each major content change.

After Cloudflare onboarding:

- **Cloudflare Web Analytics** (free, no cookies) provides Core Web Vitals from real users.
- Plausible Community / self-hosted Umami is the documented alternative if CT prefers self-hosted analytics.

---

## Known performance work for after launch

Tracked here so they don't get lost.

- [ ] Subset Cairo into Latin+Arabic woff2 pairs and update the `@font-face` block in `tokens.css` to use `unicode-range`.
- [ ] Preload the LCP font weight once known.
- [ ] Generate per-page OG PNGs (the current default OG is an SVG that some social platforms render but not all). A simple script using sharp + satori/resvg can produce these at build time.
- [ ] Add a real photography pipeline once CT supplies images.
- [ ] Run Lighthouse CI in CI; fail the build on regression beyond a tolerance.

---

## Verification

| Check | How | When |
|---|---|---|
| `npm run build` succeeds clean | locally | every change |
| Bundle sizes per route | `du -ah dist/_astro \| sort -h` after build | every change |
| Lighthouse mobile + desktop on Home + Contact + a Capabilities + a Project + 404, both locales | DevTools or `npx lighthouse <url> --view` | pre-launch + after every major change |
| LCP under 2 s | DevTools Performance tab in throttled "Slow 4G" | pre-launch |
| INP under 200 ms | DevTools "Interactions" track | pre-launch + after JS changes |
| CLS under 0.05 | DevTools Web Vitals overlay | pre-launch |
| Real-user Core Web Vitals | Cloudflare Web Analytics (post-onboarding) | continuous |
