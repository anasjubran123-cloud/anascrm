# ADR-009D — Content-Page First Load JS Ceiling Raised to 160 KB

| Field | Value |
|-------|-------|
| **ID** | ADR-009D |
| **Date** | 2026-05-21 |
| **Status** | Accepted |
| **Scope** | All content pages (every route except `/` and `/ar/`) |
| **Related** | [ADR-009C](ADR-009C-cinematic-homepage.md) — homepage hero & budget split |
| **Deciders** | Project lead |

---

## Context

ADR-009C set a ≤ 100 KB First Load JS (gzipped) ceiling for content pages. The
`pnpm build` measurement on 2026-05-21 — taken to fill ADR-009C's homepage
placeholder — revealed three content pages already exceed that ceiling:

| Route | First Load JS (gzipped) | Over the 100 KB ceiling by |
|-------|------------------------|----------------------------|
| `it-infrastructure` | 156 KB | +56 KB |
| `data-centers` | 131 KB | +29 KB |
| `audiovisual` | 129 KB | +29 KB |

The weight is driven by per-page React Three Fiber / Three.js scenes
(`ConvergenceMesh`, `SaudiHubsScene`, `DcServerRackMoment` and related). These
scenes are core to each business unit's page design, not decorative add-ons.

Two paths were considered:

1. **Code-split the R3F scenes** — dynamic-import / lazy-load the Three.js
   scenes below the fold so initial First Load JS drops toward 100 KB.
2. **Raise the content-page ceiling** — accept the measured weight as the new
   ceiling with explicit justification.

---

## Decision

**Raise the content-page First Load JS ceiling to 160 KB** (gzipped).

The highest measured content page is `it-infrastructure` at 156 KB; 160 KB adds
~4 KB headroom. The R3F scenes are intentional, design-critical content for the
business-unit pages, and the bulk of their weight is the shared Three.js
runtime — code-splitting it below the fold yields a worse experience (visible
pop-in, deferred LCP on the scene itself) for a budget number that was set
before these scenes existed.

The 160 KB ceiling is a **build-gate failure threshold**: any content page
crossing 160 KB after this date is a regression to investigate, not a new
normal to absorb.

---

## Consequences

### Positive

- The ceiling now reflects the site's actual design (R3F scenes are core).
- Build gate stays meaningful — 160 KB is a real threshold, not aspirational.
- No code churn; no scene pop-in regression.

### Negative / residual risks

- Content-page Lighthouse Performance may dip below the ≥ 95 target on
  throttled mobile. Re-measure with Lighthouse after launch; if a page misses
  95, that is a separate remediation decision (this ADR governs the JS budget
  only, not the Lighthouse score).
- The 56 KB gap between `it-infrastructure` and the old 100 KB target is large.
  If a fourth page or future feature pushes a route past 160 KB, code-splitting
  R3F should be revisited rather than raising the ceiling again — a third raise
  would mean the budget has stopped constraining anything.

### Follow-ups

- [ ] Update `LAUNCH_LIGHTHOUSE_BASELINE.md` content-page row: First Load JS
      ≤ 160 KB (was ≤ 100 KB).
- [ ] Run Lighthouse on `it-infrastructure`, `data-centers`, `audiovisual`
      after launch; record real Performance scores.
- [ ] Add a CI build-size assertion at 160 KB for content routes and 165 KB
      for the homepage, so regressions fail the build.

---

*Resolves the side-finding logged in ADR-009C's 2026-05-21 measurement section.*
