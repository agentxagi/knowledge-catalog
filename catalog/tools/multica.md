---
id: tool-multica
type: tool
resource:
  name: multica
  displayName: "Multica / ValorCollab"
  description: "AI-native task management — issues, projects, squads, agents"
labels:
  layer: task-store
  port: "8091"
  status: production
overview:
  purpose: "Task store for Valor Digital. Issues, projects, squads, lifecycle. NOT an orchestrator (see ADR-001)."
  api: "REST :8091. X-Workspace-Id header. PUT for updates (PATCH returns 405)."
  agents: "PM, Builder, Reviewer, QA, Hermes (registered but daemon autopilot disabled)"
  workspaces: "7 total — Valor Digital, Climoo, ValorCollab, Gustavo Ops, Mar de Vinhos, Rivia Outline, Teste"
  auth: "Bearer PAT"
links:
  depends_on: [{target: tool-valorbrain}]
---

# Multica / ValorCollab

Source: `/mnt/data/multica-opt` (fork of Paperclip/Multica)
Binary: `/opt/multica/server/bin/server` + `/usr/local/bin/multica` (CLI)
Systemd: multica-backend, multica-daemon, multica-web

## Important Quirks

- **PUT not PATCH** — PATCH returns 405 for issue updates
- **Auto-subissues disabled** (commit 07ec1658) — no more auto-decompose of markdown lists
- **Status values**: todo, in_progress, in_review, done, cancelled
- **Project status**: planned, in_progress, paused, completed, cancelled
