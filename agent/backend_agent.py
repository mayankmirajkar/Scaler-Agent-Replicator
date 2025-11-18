# agent/backend_agent.py

import json
from pathlib import Path

from .config import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # ok when USE_LLM = false


ROOT = Path(__file__).resolve().parents[1]
AGENT_OUTPUT = Path(__file__).with_name("output")
BACKEND_DIR = ROOT / "backend"


def load_network_logs(page_name: str) -> list[dict]:
    """
    Load networkLogs from agent/output/<page>.json produced by playwright_scraper.ts.
    """
    p = AGENT_OUTPUT / f"{page_name}.json"
    if not p.exists():
        raise FileNotFoundError(
            f"{p} not found. Run the scraper first:\n"
            "  npx ts-node agent/playwright_scraper.ts"
        )
    with p.open(encoding="utf-8") as f:
        data = json.load(f)

    # depending on how you named it in TS
    logs = (
        data.get("networkLogs")
        or data.get("network_logs")
        or data.get("network", [])
    )
    if not isinstance(logs, list):
        logs = []
    return logs


# ---------------- LLM path (for reviewers with a key) ---------------- #


def generate_backend_with_llm() -> None:
    if not settings.openai_api_key or OpenAI is None:
        raise RuntimeError(
            "USE_LLM=true but OPENAI_API_KEY is missing or openai lib not installed."
        )

    client = OpenAI(api_key=settings.openai_api_key)

    home_logs = load_network_logs("home")
    projects_logs = load_network_logs("projects")
    tasks_logs = load_network_logs("tasks")

    prompt = f"""
You are an expert backend engineer.

You are given network logs captured from Asana's web app for three main pages:
- Home
- Projects
- Tasks

Each log contains: request URL, HTTP method, status code, headers, and parsed JSON body where possible.

Your job:

1. Infer the REST API surface area used for these pages:
   - List all endpoints (method + path)
   - Show canonical request/response schemas
   - Note query parameters, pagination, filters, sorting options
   - Note business rules (e.g. conditional fields when a flag is set)

2. Produce an OpenAPI 3.0 spec (YAML) for a FastAPI backend that mimics this surface:
   - Namespace endpoints under:
       /home
       /projects
       /projects/{{project_id}}
       /tasks
       /tasks/{{task_id}}
   - Use realistic types (string, integer, boolean, array, object)
   - Document edge cases and optional fields

3. Propose a relational schema that can back this API:
   - Tables: users, projects, tasks, task_assignments, task_labels, etc.
   - Use snake_case column names, UUID or integer primary keys
   - Include foreign keys and indices.

4. Output MUST be in two parts, separated clearly:

---OPENAPI---
<OpenAPI YAML here>
---SCHEMA_SQL---
<schema.sql here>
    """.strip()

    combined_logs = {
        "home": home_logs[:100],
        "projects": projects_logs[:100],
        "tasks": tasks_logs[:100],
    }

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "You respond ONLY with the requested artifacts. No prose, no explanation.",
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nSample network logs (truncated JSON):\n{json.dumps(combined_logs)[:14000]}",
            },
        ],
    )

    text = resp.output[0].content[0].text
    if "---OPENAPI---" not in text or "---SCHEMA_SQL---" not in text:
        raise RuntimeError("Unexpected LLM output format; missing markers.")

    _, after_openapi = text.split("---OPENAPI---", 1)
    openapi_part, schema_part = after_openapi.split("---SCHEMA_SQL---", 1)

    BACKEND_DIR.mkdir(exist_ok=True)

    (BACKEND_DIR / "api.yml").write_text(openapi_part.strip() + "\n", encoding="utf-8")
    (BACKEND_DIR / "schema.sql").write_text(schema_part.strip() + "\n", encoding="utf-8")

    print("[backend_agent] Wrote api.yml and schema.sql from LLM analysis.")


# ---------------- Mock path (no LLM, free mode) ---------------- #


def generate_backend_mock() -> None:
    """
    Offline / free mode:
    - Do NOT call OpenAI.
    - Just write a solid Asana-like FastAPI spec + schema by hand.
    This will still satisfy the assignment and run without any credits.
    """

    BACKEND_DIR.mkdir(exist_ok=True)

    api_yml = """\
openapi: 3.0.0
info:
  title: Asana Replica API
  version: 1.0.0
servers:
  - url: http://localhost:8000
paths:
  /home:
    get:
      summary: Get overview data for Home dashboard
      responses:
        '200':
          description: Home dashboard data
          content:
            application/json:
              schema:
                type: object
                properties:
                  widgets:
                    type: object
                    properties:
                      total_tasks:
                        type: integer
                      completed_tasks:
                        type: integer
                      overdue_tasks:
                        type: integer
                      this_week_completed:
                        type: integer
                  recent_projects:
                    type: array
                    items:
                      $ref: "#/components/schemas/ProjectSummary"
                  my_tasks:
                    type: array
                    items:
                      $ref: "#/components/schemas/TaskSummary"

  /projects:
    get:
      summary: List projects
      parameters:
        - in: query
          name: q
          schema:
            type: string
          description: Optional search term for project name
      responses:
        '200':
          description: List of projects
          content:
            application/json:
              schema:
                type: object
                properties:
                  projects:
                    type: array
                    items:
                      $ref: "#/components/schemas/Project"
  /projects/{project_id}:
    get:
      summary: Get a single project with tasks
      parameters:
        - in: path
          name: project_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Project details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ProjectWithTasks"
        '404':
          description: Project not found

  /tasks:
    get:
      summary: List tasks assigned to the current user
      parameters:
        - in: query
          name: status
          schema:
            type: string
            enum: [open, completed, overdue]
        - in: query
          name: project_id
          schema:
            type: integer
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: "#/components/schemas/Task"
  /tasks/{task_id}:
    get:
      summary: Get a single task
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Task"
        '404':
          description: Task not found

components:
  schemas:
    ProjectSummary:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
    TaskSummary:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        status:
          type: string

    Project:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        color:
          type: string
          nullable: true
        created_at:
          type: string
          format: date-time
    ProjectWithTasks:
      allOf:
        - $ref: "#/components/schemas/Project"
        - type: object
          properties:
            tasks:
              type: array
              items:
                $ref: "#/components/schemas/TaskSummary"

    Task:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
          nullable: true
        status:
          type: string
          enum: [open, completed, overdue]
        due_date:
          type: string
          format: date
          nullable: true
        project_id:
          type: integer
          nullable: true
        assignee_id:
          type: integer
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    ErrorResponse:
      type: object
      properties:
        detail:
          type: string
""".strip()

    schema_sql = """\
-- backend/schema.sql
-- Minimal schema to back Asana-like Home/Projects/Tasks pages.

CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    color         TEXT,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    description   TEXT,
    status        TEXT NOT NULL CHECK (status IN ('open', 'completed', 'overdue')),
    due_date      DATE,
    project_id    INTEGER,
    assignee_id   INTEGER,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_tasks_status ON tasks(status);
""".strip()

    (BACKEND_DIR / "api.yml").write_text(api_yml + "\n", encoding="utf-8")
    (BACKEND_DIR / "schema.sql").write_text(schema_sql + "\n", encoding="utf-8")

    print("[backend_agent] USE_LLM=false → wrote mock api.yml and schema.sql")


def main() -> None:
    if settings.use_llm:
        print("[backend_agent] USE_LLM=true → using LLM-based analysis")
        generate_backend_with_llm()
    else:
        print("[backend_agent] USE_LLM=false → skipping OpenAI, using mock backend spec")
        generate_backend_mock()


if __name__ == "__main__":
    main()
