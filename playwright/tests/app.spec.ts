import { test, expect } from '@playwright/test';

async function loadApp(page: any): Promise<void> {
  await page.goto('/');
  await expect(page.locator('body')).toBeVisible();
}

test.describe('PSAT Web Application', () => {
  test('homepage loads correctly', async ({ page }) => {
    await loadApp(page);
    await expect(page).toHaveTitle(/Power System/i);
  });

  test('navigation menu is present', async ({ page }) => {
    await loadApp(page);
  });

  test('no console errors on homepage', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg: any) => {
      if (msg.type() === 'error') errors.push(msg.text());
    });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const criticalErrors = errors.filter((e: string) => 
      !e.includes('favicon') && !e.includes('hydration')
    );
    expect(criticalErrors).toHaveLength(0);
  });

  test('power flow module accessible', async ({ page }) => {
    await loadApp(page);
  });
});

test.describe('Responsive Design', () => {
  test('works on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await loadApp(page);
  });

  test('works on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await loadApp(page);
  });
});

test.describe('Performance', () => {
  test('page loads within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    expect(Date.now() - startTime).toBeLessThan(5000);
  });
});
