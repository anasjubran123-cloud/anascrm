// Single source of truth for site-wide configuration that the Astro config
// itself needs at build time. TypeScript-typed equivalents for runtime are in
// src/config/site.ts.

export const SITE_URL = 'https://www.convergent.sa';
export const SITE_DOMAIN = 'www.convergent.sa';

export const DEFAULT_LOCALE = 'en';
export const LOCALES = /** @type {const} */ (['en', 'ar']);
