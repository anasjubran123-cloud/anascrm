/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        // Map Tailwind colour utilities onto CSS custom properties defined in
        // src/styles/tokens.css. Do not hard-code hex values here — tokens.css
        // is the single source of truth for brand colour, and dark-mode swaps
        // happen there.
        brand: {
          DEFAULT: 'rgb(var(--ct-brand) / <alpha-value>)',
          contrast: 'rgb(var(--ct-brand-contrast) / <alpha-value>)',
        },
        surface: {
          0: 'rgb(var(--ct-surface-0) / <alpha-value>)',
          1: 'rgb(var(--ct-surface-1) / <alpha-value>)',
          2: 'rgb(var(--ct-surface-2) / <alpha-value>)',
        },
        ink: {
          0: 'rgb(var(--ct-ink-0) / <alpha-value>)',
          1: 'rgb(var(--ct-ink-1) / <alpha-value>)',
          2: 'rgb(var(--ct-ink-2) / <alpha-value>)',
          muted: 'rgb(var(--ct-ink-muted) / <alpha-value>)',
        },
        line: {
          DEFAULT: 'rgb(var(--ct-line) / <alpha-value>)',
          strong: 'rgb(var(--ct-line-strong) / <alpha-value>)',
        },
      },
      fontFamily: {
        sans: ['var(--ct-font-sans)'],
        display: ['var(--ct-font-display)'],
        mono: ['var(--ct-font-mono)'],
      },
      maxWidth: {
        prose: '68ch',
        wide: '88rem',
      },
      screens: {
        xs: '375px',
      },
    },
  },
  plugins: [],
};
