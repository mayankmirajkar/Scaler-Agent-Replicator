"use client";

import { useEffect, useState } from "react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

type Project = {
  id: number;
  name: string;
  description?: string;
  color?: string;
  archived: boolean;
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/projects`)
      .then((r) => r.json())
      .then(setProjects)
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-gray-900">Projects</h2>
      <div className="grid grid-cols-3 gap-4">
        {projects.map((p) => (
          <div
            key={p.id}
            className="rounded-xl border border-gray-200 bg-white p-4 hover:shadow-sm cursor-pointer transition"
          >
            <div className="flex items-center gap-2 mb-2">
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: p.color || "#6a67ce" }}
              />
              <h3 className="text-sm font-semibold text-gray-900">{p.name}</h3>
            </div>
            <p className="text-xs text-gray-500 line-clamp-2">{p.description || "No description"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
