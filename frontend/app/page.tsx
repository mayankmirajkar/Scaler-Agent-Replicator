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
