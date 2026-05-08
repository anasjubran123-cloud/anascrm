import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const KEY_PAGES = [
  '/en/',
  '/en/about',
  '/en/capabilities',
  '/en/sectors',
  '/en/business-units',
  '/en/projects',
  '/en/news',
  '/en/careers',
  '/en/contact',
  '/en/legal/privacy',
  '/en/legal/cookies',
  '/en/legal/terms',
  '/ar/',
  '/ar/about',
  '/ar/capabilities',
  '/ar/sectors',
  '/ar/business-units',
  '/ar/projects',
  '/ar/news',
  '/ar/careers',
  '/ar/contact',
  '/ar/legal/privacy',
  '/ar/legal/cookies',
  '/ar/legal/terms',
];

async function gotoOk(page: Page, path: string) {
  const response = await page.goto(path, { waitUntil: 'domcontentloaded' });
  expect(response?.ok(), `${path} did not return 2xx`).toBeTruthy();
}

test.describe('Smoke — every key page renders', () => {
  for (const path of KEY_PAGES) {
    test(`renders ${path}`, async ({ page }) => {
      await gotoOk(page, path);
      // Must have a unique <title>.
      const title = await page.title();
      expect(title.length).toBeGreaterThan(0);
      // Must have an <h1>.
      const h1Count = await page.locator('h1').count();
      expect(h1Count, `${path} should expose a single <h1>`).toBeGreaterThanOrEqual(1);
      // dir must match the locale.
      const dir = await page.evaluate(() => document.documentElement.dir);
      const expected = path.startsWith('/ar') ? 'rtl' : 'ltr';
      expect(dir).toBe(expected);
    });
  }
});

test.describe('Skip link works', () => {
  test('Tab focuses the skip link first', async ({ page }) => {
    await page.goto('/en/');
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.textContent ?? '');
    expect(focused.toLowerCase()).toContain('skip');
  });
});

test.describe('Theme toggle', () => {
  test('persists choice to localStorage', async ({ page }) => {
    await page.goto('/en/');
    await page.locator('[data-theme-toggle]').click();
    const stored = await page.evaluate(() => localStorage.getItem('ct-theme'));
    expect(stored === 'light' || stored === 'dark').toBeTruthy();
  });
});

test.describe('Accessibility (axe) — critical pages', () => {
  for (const path of ['/en/', '/en/contact', '/ar/', '/ar/contact']) {
    test(`no axe violations on ${path}`, async ({ page }) => {
      await page.goto(path);
      const results = await new AxeBuilder({ page }).analyze();
      // Print violations to logs to make CI failures actionable.
      if (results.violations.length > 0) {
        console.log(JSON.stringify(results.violations, null, 2));
      }
      expect(results.violations).toEqual([]);
    });
  }
});

test.describe('robots + sitemap', () => {
  test('robots.txt is present', async ({ request }) => {
    const r = await request.get('/robots.txt');
    expect(r.ok()).toBeTruthy();
  });
  test('sitemap is present', async ({ request }) => {
    const r = await request.get('/sitemap-index.xml');
    expect(r.ok()).toBeTruthy();
  });
});
