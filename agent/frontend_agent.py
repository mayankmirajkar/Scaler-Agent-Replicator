# D:\Scaler-Agent-Replicator\agent\frontend_agent.py
import json
from pathlib import Path
from .config import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # in case lib isn't installed when use_llm=False

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = Path(__file__).with_name("output")
FRONTEND_APP = ROOT / "frontend" / "app"

def load_page_snapshot(name: str):
    p = OUTPUT_DIR / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError(
            f"{p} not found. Run the scraper first: "
            f"`npx ts-node agent/playwright_scraper.ts`"
        )
    with p.open(encoding="utf-8") as f:
        return json.load(f)

def generate_home_page_llm():
    if not settings.openai_api_key or OpenAI is None:
        raise RuntimeError("LLM disabled or openai not installed")

    client = OpenAI(api_key=settings.openai_api_key)
    snapshot = load_page_snapshot("home")
    html = snapshot["html"]
    styles = snapshot["computedStyles"]

    prompt = f"""
You are a senior front-end engineer.

Given the following HTML snapshot and partial computed styles from Asana's Home page, generate a React Server Component for Next.js (app router) using Tailwind CSS.

Constraints:
- Mimic layout, spacing, and typography as closely as possible.
- Use Asana-like brand colors: #3be8b0, #1aafd0, #6a67ce, #ffb900, #fc636b.
- Do not hard-code dynamic counts; read them from GET /home API at NEXT_PUBLIC_BACKEND_URL + "/home".
- Component file: app/page.tsx.

HTML (truncated):
{html[:15000]}

Sample computed styles:
{styles[:50]}
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )

    code = resp.output[0].content[0].text
    (FRONTEND_APP / "page.tsx").write_text(code, encoding="utf-8")

def generate_home_page_mock():
    # Just write the static Next.js Home file we designed earlier.
    content = """\
"use client";

import { useEffect, useState } from "react";

type Task = {
  id: number;
  name: string;
  status: string;
};

type Project = {
  id: number;
  name: string;
};

type HomeResponse = {
  widgets: {
    total_tasks: number;
    completed_tasks: number;
    overdue_tasks: number;
    this_week_completed: number;
  };
  recent_projects: Project[];
  my_tasks: Task[];
};

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function HomePage() {
  const [data, setData] = useState<HomeResponse | null>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/home`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => {});
  }, []);

  const widgets = data?.widgets;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-gray-900">Home</h2>
      </div>
      <div className="grid grid-cols-4 gap-4">
        <WidgetCard label="Total tasks" value={widgets?.total_tasks ?? 0} accent="#1aafd0" />
        <WidgetCard label="Completed" value={widgets?.completed_tasks ?? 0} accent="#3be8b0" />
        <WidgetCard label="Overdue" value={widgets?.overdue_tasks ?? 0} accent="#fc636b" />
        <WidgetCard label="Completed this week" value={widgets?.this_week_completed ?? 0} accent="#ffb900" />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <Panel title="Recent projects">
          <ul className="space-y-1">
            {data?.recent_projects?.length ? (
              data.recent_projects.map((p) => (
                <li key={p.id} className="flex items-center justify-between">
                  <span className="text-sm text-gray-800">{p.name}</span>
                </li>
              ))
            ) : (
              <p className="text-sm text-gray-500">No projects yet.</p>
            )}
          </ul>
        </Panel>
        <Panel title="My tasks">
          <ul className="space-y-1">
            {data?.my_tasks?.length ? (
              data.my_tasks.map((t) => (
                <li key={t.id} className="flex items-center justify-between">
                  <span className="text-sm text-gray-800">{t.name}</span>
                  <span className="text-xs rounded-full px-2 py-0.5 bg-gray-100 text-gray-600">
                    {t.status}
                  </span>
                </li>
              ))
            ) : (
              <p className="text-sm text-gray-500">No tasks yet.</p>
            )}
          </ul>
        </Panel>
      </div>
    </div>
  );
}

function WidgetCard({ label, value, accent }: { label: string; value: number; accent: string }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white px-4 py-3 flex flex-col gap-1">
      <span className="text-xs uppercase tracking-wide text-gray-500">{label}</span>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-semibold text-gray-900">{value}</span>
        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: accent }} />
      </div>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
      </div>
      {children}
    </div>
  );
}
"""
    (FRONTEND_APP / "page.tsx").write_text(content, encoding="utf-8")

def main():
    if settings.use_llm:
        generate_home_page_llm()
    else:
        print("[frontend_agent] USE_LLM=false → writing mock Home page without API calls")
        generate_home_page_mock()

if __name__ == "__main__":
    main()
