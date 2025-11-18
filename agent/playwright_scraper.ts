// agent/playwright_scraper.ts
import { chromium, Page } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";
import * as dotenv from "dotenv";

dotenv.config();

const ASANA_EMAIL = process.env.ASANA_EMAIL!;
const ASANA_PASSWORD = process.env.ASANA_PASSWORD!;

type PageName = "home" | "projects" | "tasks";

async function loginToAsana(page: Page) {
  // 1) Go to login page
  await page.goto("https://app.asana.com/-/login", { waitUntil: "domcontentloaded" });

  // --- EMAIL STEP ---
  const emailInput = page.locator('input[type="email"], input[name="email"]');
  await emailInput.waitFor({ state: "visible", timeout: 30000 });
  await emailInput.fill(ASANA_EMAIL);

  // Prefer clicking the visible "Continue" button
  const continueButton = page.getByRole("button", { name: /continue/i });

  if (await continueButton.isVisible().catch(() => false)) {
    await continueButton.click();
  } else {
    // Fallback: press Enter
    await emailInput.press("Enter");
  }

  // Do NOT wait for networkidle here – Asana never really goes idle.
  // Instead wait until password field appears.
  const passwordInput = page.locator('input[type="password"], input[name="password"]');
  await passwordInput.waitFor({ state: "visible", timeout: 30000 });

  // --- PASSWORD STEP ---
  await passwordInput.fill(ASANA_PASSWORD);

  // Try to click a "Log in" / "Login" button
  const loginButton = page.getByRole("button", { name: /log in|login/i });

  if (await loginButton.isVisible().catch(() => false)) {
    await loginButton.click();
  } else {
    // Fallback: press Enter in password field
    await passwordInput.press("Enter");
  }

  // Now wait until we are on the main app URL (or give up after 60s)
  try {
    await page.waitForURL(/app\.asana\.com\/0\//, { timeout: 60000 });
  } catch {
    // If it doesn't match, we still continue – you'll see in debug if something is off
  }
}

async function capturePage(name: PageName, url: string) {
  const browser = await chromium.launch({
    headless: false,   // keep visible while debugging; change to true later
    slowMo: 300,       // slow down actions so you can see what's happening
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  const networkLogs: any[] = [];

  context.on("requestfinished", async (request) => {
    const response = await request.response();
    const reqUrl = request.url();
    const method = request.method();
    const headers = request.headers();
    let body: any = null;
    try {
      body = await response?.json();
    } catch {
      body = null;
    }
    networkLogs.push({
      url: reqUrl,
      method,
      status: response?.status(),
      headers,
      body,
    });
  });

  // Login once
  await loginToAsana(page);

  // Navigate to desired page
  await page.goto(url, { waitUntil: "domcontentloaded" });
  // Give Asana a few seconds to render content
  await page.waitForTimeout(5000);

  const html = await page.content();
  const computedStyles = await page.evaluate(() => {
    const elements = Array.from(document.querySelectorAll("*")).slice(0, 300);
    return elements.map((el, idx) => {
      const cs = window.getComputedStyle(el as Element);
      return {
        index: idx,
        tag: (el as Element).tagName,
        className: (el as HTMLElement).className,
        styles: {
          color: cs.color,
          backgroundColor: cs.backgroundColor,
          fontSize: cs.fontSize,
          fontWeight: cs.fontWeight,
          borderRadius: cs.borderRadius,
        },
      };
    });
  });

  const outDir = path.join(__dirname, "output");
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  fs.writeFileSync(
    path.join(outDir, `${name}.json`),
    JSON.stringify({ html, computedStyles, networkLogs }, null, 2)
  );

  await browser.close();
}

(async () => {
  await capturePage("home", "https://app.asana.com/0/home");
  await capturePage("projects", "https://app.asana.com/0/projects");
  await capturePage("tasks", "https://app.asana.com/0/my_tasks");
})();
