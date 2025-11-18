"use client";

import { useEffect, useState } from "react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

type Task = {
  id: number;
  name: string;
  status: string;
  label?: string;
  project_id: number;
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [labelFilter, setLabelFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const loadTasks = () => {
    const params = new URLSearchParams();
    if (labelFilter.trim() !== "") params.set("label", labelFilter);
    if (statusFilter.trim() !== "") params.set("status", statusFilter);
    fetch(`${BACKEND_URL}/tasks?` + params.toString())
      .then((r) => r.json())
      .then(setTasks)
      .catch(() => {});
  };

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-gray-900">My tasks</h2>

      <div className="flex gap-3 items-end">
        <div className="flex flex-col">
          <label className="text-xs text-gray-500 mb-1">Label</label>
          <input
            value={labelFilter}
            onChange={(e) => setLabelFilter(e.target.value)}
            className="border rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#1aafd0]"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-xs text-gray-500 mb-1">Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#1aafd0]"
          >
            <option value="">All</option>
            <option value="not_started">Not started</option>
            <option value="in_progress">In progress</option>
            <option value="complete">Complete</option>
          </select>
        </div>
        <button
          onClick={loadTasks}
          className="rounded-md px-3 py-1 text-sm bg-[#1aafd0] text-white hover:bg-[#6a67ce]"
        >
          Apply
        </button>
      </div>

      <table className="w-full text-sm border-separate border-spacing-y-1">
        <thead>
          <tr className="text-xs text-gray-500">
            <th className="text-left px-2 py-1">Task</th>
            <th className="text-left px-2 py-1">Status</th>
            <th className="text-left px-2 py-1">Label</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((t) => (
            <tr
              key={t.id}
              className="bg-white hover:bg-gray-50 rounded-lg shadow-[0_0_0_1px_rgba(0,0,0,0.03)]"
            >
              <td className="px-2 py-2">{t.name}</td>
              <td className="px-2 py-2">
                <span className="text-xs rounded-full px-2 py-0.5 bg-gray-100 text-gray-600">
                  {t.status}
                </span>
              </td>
              <td className="px-2 py-2 text-xs text-gray-500">{t.label || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
