# Asana Replication Agent

**Fully automated system that replicates Asana’s Home, Projects & Tasks UI + API**
Built with **FastAPI, Next.js, Tailwind, Playwright & an optional LLM agent layer.**

---

## 🔥 What This System Does

This agentic framework can:

### 1. Scrape a live SaaS app (Asana):

* Captures HTML
* Captures full computed CSS properties
* Captures API traffic + request/response bodies

### 2. Reconstruct it:

* Backend:

  * API routes
  * OpenAPI spec (`api.yml`)
  * SQL schema (`schema.sql`)
* Frontend:

  * Pixel-accurate pages in React + Tailwind
  * `/home`
  * `/projects`
  * `/tasks`

### 3. Test it:

* Playwright visual regression
* CSS property assertions
* Dynamic masking for changing numbers

### 4. Run with or without LLMs:

* `USE_LLM=true` → self-improving agent
* `USE_LLM=false` → static fallback, **0 cost**

---

## 🏗 Tech Stack

| Layer        | Tech                                          |
| ------------ | --------------------------------------------- |
| Frontend     | Next.js 14, Tailwind, React Server Components |
| Backend      | FastAPI, SQLAlchemy, SQLite                   |
| Testing      | Playwright (visual + CSS)                     |
| Agent        | Python + TypeScript                           |
| Optional LLM | OpenAI `gpt-4o` or `mini`                     |
| Infra        | Docker-ready, .env powered                    |

---

## 🚀 Setup

### 1. Clone & setup env

```bash
git clone <repo>
cd asana-replication-agent
copy .env.template .env
```

You can leave `USE_LLM=false` (free mode).

---

### 2. Backend — FastAPI

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

Check:

```
http://127.0.0.1:8000/docs
```

---

### 3. Frontend — Next.js

```bash
cd ../frontend
npm install
npm run dev -- --port 3000
```

Check:

```
http://localhost:3000
```

---

### 4. Playwright Tests

```bash
cd frontend
npx playwright install
npx playwright test
```

It runs:

✔ CSS exactness
✔ Pixel-diff screenshots
✔ Dynamic masking for numbers

---

## 🤖 Agent Layer

#### Backend Agent

Generates API schema + SQL structure

```bash
python -m agent.backend_agent
```

Outputs:

```
backend/api.yml
backend/schema.sql
```

#### Frontend Agent

Generates pages from snapshot

```bash
python -m agent.frontend_agent
```

Outputs:

```
frontend/app/page.tsx
```

---

## 🧠 Optional: Real AI Mode

Enable:

```env
USE_LLM=true
```

Set:

```
OPENAI_API_KEY= generated from open-ai-api-keys
ASANA_EMAIL='Scaler@1711'
ASANA_PASSWORD= 'mayank.mirajkar28@gamil.com'
```

Then run:

```bash
npx ts-node agent/playwright_scraper.ts
python -m agent.backend_agent
python -m agent.frontend_agent
```

This:

* Logs into Asana
* Captures live UI + API
* Regenerates code

---

## 🧪 How I Validate Fidelity

| Test Type     | Tool         | Checks                             |
| ------------- | ------------ | ---------------------------------- |
| CSS Assertion | Playwright   | color, border, radius, font weight |
| Visual Diff   | Playwright   | pixel delta < 200                  |
| API Schema    | OpenAPI YAML | routes, params, conditionals       |
| DB Schema     | SQL          | inferred from API usage            |

---

## ⚙️ Notes / Limitations

* Asana login may require solving CAPTCHA manually
* Free mode (USE_LLM=false) uses static mocks (no credits required)
* LLM mode self-improves when API keys are added
* Tested on Node 20 and Python 3.10

---

## 🎯 What This Demonstrates

* Ability to reverse-engineer a SaaS product
* Deep understanding of UI + API interplay
* Automated schema & code generation
* Visual + CSS fidelity testing
* Graceful fallback when no LLM credits
* Production-style architecture

---

## 📩 Contact

If you can run:

```
npm run dev
uvicorn app.main:app
npx playwright test
python -m agent.backend_agent
python -m agent.frontend_agent
```
Then all the project is working perfect.

DEVELOPED BY:-
— **Mayank Mirajkar**
