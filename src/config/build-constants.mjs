// Build-time constants consumed by astro.config.mjs (a JS file that loads
// before Astro's runtime can read TS modules) and re-exported by
// src/config/site.ts so app code reads everything from one source.
//
// This file is named build-constants.mjs (not site.mjs) on purpose: the
// path alias "@config/site" used across components and lib code must
// resolve to site.ts unambiguously. Vite's `.mjs`-before-`.ts` resolution
// otherwise causes `import { site } from '@config/site'` to pick the wrong
// module and return `undefined`.

export const SITE_URL = 'https://www.convergent.sa';
export const SITE_DOMAIN = 'www.convergent.sa';

export const DEFAULT_LOCALE = 'en';
export const LOCALES = /** @type {const} */ (['en', 'ar']);
