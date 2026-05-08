import en from '../i18n/en.json';
import ar from '../i18n/ar.json';
import { LOCALES, DEFAULT_LOCALE } from '../config/site.mjs';
import type { Locale } from '../config/site';

type Dictionary = typeof en;

const dictionaries: Record<Locale, Dictionary> = {
  en,
  ar: ar as Dictionary,
};

const directions: Record<Locale, 'ltr' | 'rtl'> = {
  en: 'ltr',
  ar: 'rtl',
};

const htmlLangCodes: Record<Locale, string> = {
  en: 'en-SA',
  ar: 'ar-SA',
};

export function isLocale(value: string | undefined): value is Locale {
  return typeof value === 'string' && (LOCALES as readonly string[]).includes(value);
}

export function dirFor(locale: Locale): 'ltr' | 'rtl' {
  return directions[locale];
}

export function htmlLangFor(locale: Locale): string {
  return htmlLangCodes[locale];
}

export function dictFor(locale: Locale): Dictionary {
  return dictionaries[locale];
}

export function defaultLocale(): Locale {
  return DEFAULT_LOCALE as Locale;
}

export function otherLocale(locale: Locale): Locale {
  return locale === 'en' ? 'ar' : 'en';
}

// Build a locale-prefixed path. Always returns paths without trailing slash
// (matches astro.config.mjs trailingSlash: 'never').
export function localizedPath(locale: Locale, path = '/'): string {
  const trimmed = path.replace(/^\/+|\/+$/g, '');
  if (trimmed.length === 0) {
    return `/${locale}`;
  }
  return `/${locale}/${trimmed}`;
}
