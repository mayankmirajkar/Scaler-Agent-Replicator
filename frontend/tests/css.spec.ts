import { test, expect } from "@playwright/test";

test("primary button has correct color and radius", async ({ page }) => {
  await page.goto("/");
  const button = page.getByRole("button", { name: "+ Add task" });
  const color = await button.evaluate((el) =>
    window.getComputedStyle(el).backgroundColor
  );
  const borderRadius = await button.evaluate((el) =>
    window.getComputedStyle(el).borderRadius
  );

  // Tailwind bg-[#1aafd0] should be rgb(26, 175, 208)
  expect(color).toBe("rgb(26, 175, 208)");
  // Tailwind rounded-md -> 0.375rem => 6px (depends on browser, usually 6px)
  expect(borderRadius).toBe("6px");
});

test("sidebar item shape & font", async ({ page }) => {
  await page.goto("/");
  const homeLink = page.getByRole("link", { name: "Home" });
  const styles = await homeLink.evaluate((el) => {
    const cs = window.getComputedStyle(el);
    return {
      fontWeight: cs.fontWeight,
      borderRadius: cs.borderRadius,
      backgroundColor: cs.backgroundColor,
    };
  });

  expect(styles.fontWeight).toBe("600");          // font-semibold
  expect(styles.borderRadius).toBe("12px");       // rounded-xl
  expect(styles.backgroundColor).toBe("rgb(243, 244, 246)"); // bg-gray-100
});
