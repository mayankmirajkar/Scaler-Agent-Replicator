import { test, expect } from "@playwright/test";

test.describe("Asana Replica Visual", () => {
  test("Home page pixel diff", async ({ page }) => {
    await page.goto("/");
    // Mask dynamic numbers (task counts etc)
    const masks = await page.locator("span:text-matches('^[0-9]+$')").all();
    await expect(page).toHaveScreenshot("home.png", {
      mask: masks,
      fullPage: true,
      maxDiffPixels: 200,
    });
  });

  test("Projects page", async ({ page }) => {
    await page.goto("/projects");
    await expect(page).toHaveScreenshot("projects.png", { fullPage: true, maxDiffPixels: 200 });
  });

  test("Tasks page", async ({ page }) => {
    await page.goto("/tasks");
    await expect(page).toHaveScreenshot("tasks.png", { fullPage: true, maxDiffPixels: 200 });
  });
});
