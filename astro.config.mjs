// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

import { SITE_URL, LOCALES, DEFAULT_LOCALE } from './src/config/build-constants.mjs';

export default defineConfig({
  site: SITE_URL,
  output: 'static',
  trailingSlash: 'never',
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
  i18n: {
    defaultLocale: DEFAULT_LOCALE,
    locales: LOCALES,
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false,
    },
  },
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    mdx(),
    sitemap({
      i18n: {
        defaultLocale: DEFAULT_LOCALE,
        locales: {
          en: 'en-SA',
          ar: 'ar-SA',
        },
      },
      // Exclude the dev playground from the sitemap.
      filter: (page) => !page.includes('/dev/'),
    }),
  ],
  vite: {
    build: {
      sourcemap: false,
    },
    ssr: {
      noExternal: [],
    },
    server: {
      // Hosts permitted to reach the dev server. A leading dot is a
      // suffix-match wildcard (e.g. .trycloudflare.com matches any
      // foo.trycloudflare.com). LAN IPs and localhost are always allowed.
      // We list the common preview/tunnel domains so testing the dev
      // server from a phone via Cloudflare quick-tunnels or ngrok works
      // out of the box. This block has no effect on production builds.
      allowedHosts: [
        '.trycloudflare.com',
        '.ngrok-free.app',
        '.ngrok.app',
        '.ngrok.io',
        '.localhost',
        'localhost',
      ],
    },
    preview: {
      allowedHosts: [
        '.trycloudflare.com',
        '.ngrok-free.app',
        '.ngrok.app',
        '.ngrok.io',
        '.localhost',
        'localhost',
      ],
    },
  },
});
