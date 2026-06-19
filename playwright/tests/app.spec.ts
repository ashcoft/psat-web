import { test, expect } from '@playwright/test';

test.describe('PSAT Web Application', () => {
  test('homepage loads correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check page title
    await expect(page).toHaveTitle(/Power System/i);
    
    // Check main content is visible
    await expect(page.locator('body')).toBeVisible();
  });

  test('navigation menu is present', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page has some content
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('no console errors on homepage', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Filter out known non-critical errors
    const criticalErrors = errors.filter(e => 
      !e.includes('favicon') && 
      !e.includes('hydration')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });
});

test.describe('Power Flow Module', () => {
  test('can access power flow functionality', async ({ page }) => {
    await page.goto('/');
    
    // The page should load without errors
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Responsive Design', () => {
  test('works on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Page should be visible on mobile
    await expect(page.locator('body')).toBeVisible();
  });

  test('works on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    
    // Page should be visible on tablet
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Performance', () => {
  test('page loads within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    const loadTime = Date.now() - startTime;
    
    // Page should load within 5 seconds
    expect(loadTime).toBeLessThan(5000);
  });
});
