# Architecture Decision Records

Records for significant architectural decisions made on the Convergent Technology Company website project.

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-001](ADR-001-stack.md) | Astro static site with Tailwind and React islands | Accepted | 2026-05 |
| [ADR-002](ADR-002-bilingual-routing.md) | Prefix-default-locale bilingual routing `/en` + `/ar` | Accepted | 2026-05 |
| [ADR-003](ADR-003-form-endpoint.md) | Web3Forms / Formspree free tier + hCaptcha with Cloudflare Worker swap path | Accepted | 2026-05 |
| [ADR-004](ADR-004-security-headers.md) | Apache `.htaccess` for all security headers (no Cloudflare at launch) | Accepted | 2026-05 |
| [ADR-005](ADR-005-fonts.md) | Cairo self-hosted subset for EN + AR unified typeface | Accepted | 2026-05 |
| [ADR-006](ADR-006-no-cms.md) | MDX content collections, no headless CMS | Accepted | 2026-05 |
| [ADR-007](ADR-007-analytics.md) | No analytics at launch; Cloudflare Analytics / Plausible deferred | Accepted | 2026-05 |
| [ADR-008](ADR-008-partner-logos.md) | Partner logos displayed without tier claims; written approvals pre-launch gate | Accepted | 2026-05 |
| [ADR-009C](ADR-009C-cinematic-homepage.md) | Cinematic homepage hero; per-route performance budget split | Accepted | 2026-05-21 |
| ADR-009D | Content pages over the 100 KB First Load JS ceiling — remediation | Proposed | 2026-05-21 |

## Format

Each ADR follows the structure: **Context → Decision → Consequences**. Superseded ADRs are marked `Superseded by ADR-XXX` and kept for history.
