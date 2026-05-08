import { SITE_URL, SITE_DOMAIN, DEFAULT_LOCALE, LOCALES } from './site.mjs';

export type Locale = (typeof LOCALES)[number];

export interface SiteConfig {
  url: string;
  domain: string;
  defaultLocale: Locale;
  locales: readonly Locale[];
  // Lead routing
  contactEmail: string;
  // Legal entities (English + Arabic) used in JSON-LD and footer
  legalNameEn: string;
  legalNameAr: string;
  // HQ
  hq: {
    city: string;
    country: string;
    countryCode: string;
  };
}

export const site: SiteConfig = {
  url: SITE_URL,
  domain: SITE_DOMAIN,
  defaultLocale: DEFAULT_LOCALE as Locale,
  locales: LOCALES as readonly Locale[],
  contactEmail: 'info@convergent.sa',
  legalNameEn: 'Convergent Technology Company',
  legalNameAr: 'شركة التقنية المترابطة',
  hq: {
    city: 'Al Khobar',
    country: 'Kingdom of Saudi Arabia',
    countryCode: 'SA',
  },
};
