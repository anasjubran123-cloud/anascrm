# Brand Guideline — Extract

Source: `Convergent Technology Full Identity / CT Group Identity / CT GROUP GUIDE LINE / Convergant GuideLine.pdf` (Version 0.1, Oct 2025).

Pulled via the SharePoint MCP on 2026-05-08 from
`https://covergtech-my.sharepoint.com/personal/anjubran_convergent_sa/Documents/Desktop/Convergent Technology Full Identity/`.

This file records what was extracted so future contributors do not have to re-derive it.

## Wordmark

- "**Convergent**" set as the primary wordmark.
- "**T e c h n o l o g y**" letter-spaced beneath, centred.
- Lockups: Horizontal, Vertical (long), Vertical Short, plus Arabic version.
- Co-branding rules: equal optical size; vertical or horizontal stroke equal to logo clear space; partner placement per principal/equal/sub-brand rules in the guideline.
- Minimum sizes: 100 px digital (preferred), 50 px digital absolute floor; 20 mm print floor, 80 mm preferred.
- Clear space: equal to the height of the wordmark.

## Primary colour — CT GROUP

| Token | Hex | RGB | CMYK |
|---|---|---|---|
| ROSO red (primary) | `#D00F18` | 208 / 15 / 24 | 12 / 100 / 100 / 3 |

Mono variants documented: black on white, white on black.

## Sub-brands and accent system

The brand uses a flexible accent palette per sub-brand. The mother brand (CT GROUP) carries the primary red; each business unit takes its own accent layered on top of the master neutrals.

Sub-brands recognised in the guideline:

- Convergent **Data Center**
- Convergent **IT Infrastructure**
- Convergent **Audiovisual**
- Convergent **Landscape**
- Convergent **Events** (corporate/event-collateral track, not a website business unit)

Per-sub-brand accent hexes are not declared in the master document; they live in each sub-brand's own guideline (CT DATA CENTRE, CT IT INFUSTRACTURE, CT AUDIOVISUAL, CT LANDSCAPE, CT EVENTS folders). The mother website only renders link-out cards to the four business-unit subdomains, so for v1 we use the master red and a neutral system.

## Typography

- **English typeface** declared in guideline: **Optima** (paid / proprietary). Optima cannot be self-hosted on the website without a paid Linotype/Monotype web licence, so per the project cost-control rule we do **not** ship Optima.
- **Replacement (per CT instruction this session, 2026-05-08):** use **Cairo** as the unified family for both English and Arabic. Cairo is a Google Font (Open Font License), supports Latin and Arabic, and self-hosts cleanly. Single family also keeps cross-lingual rhythm consistent.
- Body / supporting reference: the original .ai package report listed Cairo, Optima, Beatrice Deck, Quicksand, EB Garamond, Almarai Light, Adobe Arabic, 29LT Zarid Sans — recorded for reference only; not used in production.

## Voice / themes

- Tagline: **"Where Systems Sync."**
- Editorial header: **"A Gateway to Tomorrow."**
- Design metaphor: "modern architectural gateway — strong, grounded, sharply futuristic; a company built on solid technological foundations."
- Pattern motif: minimal line-art inspired by hightech/blueprint plans. Used sparingly; not as decoration.
- Iconography: mixed round/sharp edges per context. No emoji.

## Photography

Three buckets called out: Internal shots, External shots, Lifestyle shots. No reference frames pulled yet; required as part of the content handover (logged in `CONTENT.md` once Phase 5 lands).

## Logo files in source folder (`CT Group Identity / LOGO`)

Identified but not yet copied into the repo (SharePoint MCP returns text content only, not binary):

- `CT GROUP.ai` (Adobe Illustrator master)
- `CT GROUP.pdf`
- `CT GROUP.jpg`
- `CT GROUP Black.pdf` / `.png`
- `CT GROUP White.pdf` / `.png`
- `logo CT Vertical .ai` / `.pdf` / `.png`
- `logo CT Vertical Black.pdf` / `.png`
- `logo CT Vertical white.pdf` / `.png`

**No SVG variant exists in the source.** For crisp web rendering we want one. Recommended path: export an SVG from `CT GROUP.ai` and push it (and at least the colour, black, and white PNGs) to `/branding/` on this branch.

## Additional source notes

- The guideline references `convergenttec.com` and `convergenttic.com` in mockups. Final canonical domain is **`www.convergent.sa`** per CT decision this session — these mockup URLs are ignored.
- A "Sand (RGB)" spot colour appears in the .ai file's package report, but is not specified as a brand colour in the guideline body. Treated as a layout/print accent, not a web token.

## What this drives in code

- `src/styles/tokens.css` carries `--ct-red: #D00F18` as the primary brand colour.
- The entire type system runs on **Cairo** (self-hosted woff2 subset), with system fallback chains for both Latin and Arabic.
- The `<Logo>` component renders a typeset CSS wordmark matching the guideline's structure ("Convergent" + letter-spaced "T e c h n o l o g y") as the v1 fallback. When the SVG/PNG arrives in `/branding/`, the component swaps to `<img>` with one line.
- Sub-brand accent hexes stay placeholder until the per-unit guidelines are pulled.
