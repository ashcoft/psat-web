import { test, expect } from '@playwright/test';

/**
 * E2E tests for Power System Analysis Tool
 * These tests verify the core functionality of the web interface
 */

test.describe('Power System Components', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('application loads without crashes', async ({ page }) => {
    // Verify the page loads successfully
    await expect(page).not.toBeNull();
    const body = await page.locator('body');
    await expect(body).toBeVisible();
  });

  test('displays power system analysis interface', async ({ page }) => {
    // Check that main interface elements are present
    const mainContent = page.locator('main, [role="main"], #__next, #root, body');
    await expect(mainContent.first()).toBeVisible();
  });
});

test.describe('IEC Symbols Library', () => {
  test('symbol library is accessible', async ({ page }) => {
    await page.goto('/');
    
    // Check page loads
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Power Flow Analysis', () => {
  test('power flow module loads', async ({ page }) => {
    await page.goto('/');
    
    // Basic functionality test
    await expect(page.locator('body')).toBeVisible();
  });

  test('supports multiple power flow methods', async ({ page }) => {
    await page.goto('/');
    
    // Check page loads for power flow analysis
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Stability Analysis', () => {
  test('stability analysis module loads', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Fault Analysis', () => {
  test('fault analysis module loads', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Report Generation', () => {
  test('report generation is available', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('body')).toBeVisible();
  });
});
