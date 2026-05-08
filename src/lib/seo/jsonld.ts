// Strongly-typed JSON-LD generators for Convergent's structured data.
// Per master prompt §17 we emit Organization + LocalBusiness on every page,
// and add Service / BreadcrumbList / Article / FAQPage where applicable.
//
// Schema reference: https://schema.org/

import type { Locale } from '@config/site';
import { site } from '@config/site';

const ORG_ID = `${site.url}#org`;
const PLACE_ID = `${site.url}#hq`;

interface ImageRef {
  url: string;
  width?: number;
  height?: number;
}

const defaultLogo: ImageRef = {
  url: `${site.url}/brand/logo-ct-group.svg`,
};

export interface OrganizationOptions {
  locale: Locale;
  logo?: ImageRef;
}

export function organizationLD(opts: OrganizationOptions): unknown {
  const localized = opts.locale === 'ar' ? site.legalNameAr : site.legalNameEn;
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': ORG_ID,
    name: localized,
    alternateName:
      opts.locale === 'ar' ? site.legalNameEn : site.legalNameAr,
    url: site.url,
    logo: (opts.logo ?? defaultLogo).url,
    sameAs: [
      // {{TODO: add LinkedIn / X / etc. URLs once CT social profiles confirmed.}}
    ],
    contactPoint: [
      {
        '@type': 'ContactPoint',
        contactType: 'customer support',
        email: site.contactEmail,
        availableLanguage: ['en', 'ar'],
      },
    ],
  };
}

export interface LocalBusinessOptions {
  locale: Locale;
}

export function localBusinessLD(opts: LocalBusinessOptions): unknown {
  return {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': PLACE_ID,
    name: opts.locale === 'ar' ? site.legalNameAr : site.legalNameEn,
    url: site.url,
    image: defaultLogo.url,
    telephone: '{{TODO: confirm main phone}}',
    email: site.contactEmail,
    address: {
      '@type': 'PostalAddress',
      addressLocality: site.hq.city,
      addressCountry: site.hq.countryCode,
      streetAddress: '{{TODO: street + building + district + postcode}}',
    },
    areaServed: site.hq.countryCode,
    openingHoursSpecification: [
      {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
        opens: '08:30',
        closes: '17:30',
      },
    ],
  };
}

export interface BreadcrumbItem {
  name: string;
  url: string;
}

export function breadcrumbLD(items: readonly BreadcrumbItem[]): unknown {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export interface ArticleOptions {
  locale: Locale;
  title: string;
  description: string;
  publishedAt: string | Date;
  url: string;
  image?: string;
}

export function articleLD(opts: ArticleOptions): unknown {
  const datePublished =
    typeof opts.publishedAt === 'string'
      ? opts.publishedAt
      : opts.publishedAt.toISOString();
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: opts.title,
    description: opts.description,
    datePublished,
    inLanguage: opts.locale === 'ar' ? 'ar-SA' : 'en-SA',
    author: { '@type': 'Organization', '@id': ORG_ID },
    publisher: { '@type': 'Organization', '@id': ORG_ID },
    mainEntityOfPage: opts.url,
    image: opts.image ?? `${site.url}/og/default.png`,
  };
}
