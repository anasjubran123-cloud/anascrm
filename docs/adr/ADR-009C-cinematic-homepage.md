# ADR-009C — Cinematic Homepage Hero; Per-Route Performance Budget Split

| Field | Value |
|-------|-------|
| **ID** | ADR-009C |
| **Date** | 2026-05-21 |
| **Status** | Accepted |
| **Scope** | `/` (homepage) only — all other routes unaffected |
| **Supersedes** | ADR-009A (restrained global aesthetic), ADR-009B (uniform Lighthouse 95+ target) |
| **Deciders** | Project lead |

---

## Context

STAGE_4_DESIGN_SPEC v1.2 specified a uniform restrained brand posture across every route — measured typography, generous whitespace, no decorative motion on any page. Lighthouse ≥ 95 Performance was set as a single global floor.

During Phase 9C, a cinematic homepage hero was introduced (plain HTML5 `<video>` + scroll listener, ~3 KB, no R3F / Three.js) to create a premium first impression for the mother-company landing page. The component existed in code before this decision was consciously documented, creating a "drift" state where code and spec contradicted each other.

Existing R3F scenes on the homepage (`ConvergenceMesh`, `SaudiHubsScene`, `DcServerRackMoment`) already pushed the homepage's First Load JS beyond the 100 KB gzipped target set for content pages. A single global budget was no longer defensible.

---

## Decision

**Adopt** the cinematic homepage hero as a **progressive enhancement** that activates only when all four conditions are met at runtime:

1. `prefers-reduced-motion` is not set (`matchMedia('(prefers-reduced-motion: reduce)').matches === false`)
2. Viewport width ≥ 768 px (tablet + desktop only)
3. `requestIdleCallback` is available (signals the browser is not under pressure)
4. A `HEAD` request to the video file URL returns HTTP 200 (avoids broken-video fallback)

The **SSR dark-gradient** is canonical and ships in the initial HTML. The video layer is painted over it via JS after all four gates pass. Removing the JS leaves a fully functional, accessible, brand-correct page.

**Hero video hard caps:**

| Constraint | Limit |
|------------|-------|
| File size (encoded) | ≤ 4 MB |
| Duration | ≤ 12 s (seamless loop) |
| Max resolution | 1080p |
| Formats required | H.264 MP4 (primary) + WebM/AV1 (alternate) |
| Poster frame | Required — loaded ahead of video |
| Autoplay | Muted, `playsinline`, `loop` only |

**Decorative video is forbidden on all routes except `/` and `/ar/`.**

---

## Performance budget split

The homepage is decoupled from content pages to reflect their genuinely different design intent.

| Metric | Homepage (`/`, `/ar/`) | Content pages (all other routes) |
|--------|------------------------|----------------------------------|
| LCP (mobile, throttled 4G) | ≤ 3.2 s | ≤ 2.5 s |
| CLS | ≤ 0.05 | ≤ 0.05 |
| INP | ≤ 200 ms | ≤ 200 ms |
| Total Blocking Time | ≤ 350 ms | ≤ 200 ms |
| First Load JS (gzipped) | ≤ **165 KB** (measured 160 KB, 2026-05-21 + 5 KB headroom) | ≤ 160 KB — see ADR-009D |
| Lighthouse Performance | ≥ 88 | ≥ 95 |
| Lighthouse A11y / BP / SEO | ≥ 95 | ≥ 95 |

### Measurement — 2026-05-21 (`pnpm build`, Next.js production site)

The production site routes `/` → `/[lang]` via a language-redirect middleware:

| Route | First Load JS (gzipped) | Notes |
|-------|------------------------|-------|
| `/` (literal) | 103 KB | Language-redirect entry; 135 B route-specific |
| `/[lang]` (renders `/en`, `/ar` — the real homepage) | **160 KB** | 6.1 KB route-specific + 103 KB shared + R3F + cinematic-hero scaffold |

**160 KB** is what visitors actually load on the homepage. The homepage ceiling
is **ratified at 165 KB** — the measured 160 KB plus 5 KB headroom to absorb
minor dependency drift. A regression past 165 KB is a build-gate failure.

### Side-finding — content pages over the 100 KB ceiling

The same build revealed three content pages already exceed the ≤ 100 KB
content-page budget this ADR sets:

| Route | First Load JS (gzipped) | Over budget by |
|-------|------------------------|----------------|
| `it-infrastructure` | 156 KB | +56 KB |
| `data-centers` | 131 KB | +31 KB |
| `audiovisual` | 129 KB | +29 KB |

This is the "open a separate issue" path the follow-up checklist anticipated.
It is **out of scope for ADR-009C** (which governs `/` only) and is resolved in
[ADR-009D](ADR-009D-content-page-budget.md), which raises the content-page
ceiling to **160 KB**.

---

## Consequences

### Positive

- The homepage makes a premium cinematic first impression on capable devices / connections.
- Users on low-powered devices, save-data connections, or with `prefers-reduced-motion` receive a pixel-perfect SSR fallback — no layout shift, no broken video, no accessibility regression.
- The four-gate capability check makes the enhancement self-disabling in hostile conditions without any developer intervention.
- The brand posture split is now documented: cinematic homepage, restrained everywhere else.

### Negative / residual risks

- Homepage Lighthouse Performance floor drops from ≥ 95 to ≥ 88. This is intentional and bounded; if the real score falls below 88, revisit scene complexity.
- The homepage Lighthouse Performance floor drops from ≥ 95 to ≥ 88; if the real score falls below 88 after video integration, revisit scene complexity.
- Video asset production (encode, optimize, poster) is the client's responsibility; until the asset exists, the hero renders as the SSR gradient.
- H.264 + WebM dual-encode increases CDN storage by ~8 MB per video (4 MB × 2 formats).

### Follow-ups

- [x] Run `pnpm build`, measure homepage First Load JS gzipped — **160 KB, 2026-05-21**. Recorded above and in `LAUNCH_LIGHTHOUSE_BASELINE.md`.
- [x] Ratify the homepage First Load JS ceiling — **165 KB** (measured 160 KB + 5 KB headroom).
- [x] Write ADR-009D for the three content pages over the 100 KB ceiling — Accepted, ceiling raised to 160 KB.
- [ ] Encode hero video: H.264 MP4 + WebM/AV1, ≤4 MB each, 12s loop, poster JPEG. Verify file size before deploying.
- [ ] Run Lighthouse on the homepage after video integration: confirm score ≥ 88 Performance, ≥ 95 A11y/BP/SEO.
- [ ] Mark Arabic cinematic i18n keys (`AR-REVIEW-PENDING-PHASE9C`) as reviewed once native-speaker review is complete.
- [ ] Sync `.claude/worktrees/blissful-raman-852120/` copies of `STAGE_4_DESIGN_SPEC.md` and `LAUNCH_LIGHTHOUSE_BASELINE.md` to canonical OneDrive copies if diverged.

---

## How to run the budget measurement

```bash
# In the Astro project root:
npm run build          # or pnpm build
# Astro prints per-route bundle sizes at the end of the build output.
# Look for the line starting with "/" (homepage route) — record the JS size in KB (gzipped).

# Alternatively, use the bundle visualiser if configured:
npm run build -- --reporter html
# Open dist/_astro/ in a local server and check the visualiser.
```

---

*This ADR was drafted to resolve a drift between Phase 9C code (cinematic hero in place) and the v1.2 spec (uniform restrained posture). The commit that introduced the hero should reference this ADR.*
