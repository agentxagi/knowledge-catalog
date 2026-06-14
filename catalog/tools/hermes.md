---
id: tool-hermes
type: tool
resource:
  name: hermes
  displayName: "Hermes Agent"
  description: "AI agent platform by Nous Research — the operational engine of Valor Digital"
labels:
  layer: orchestrator
  host: WSL2
  status: production
overview:
  purpose: "Coordinator, investigator, fixer. Hermes reads the org catalog, coordinates agents, validates work, reports to CEO."
  profiles: "default (COO), dev, cs, financeiro, vendas. More profiles pending (tech-lead, devops, sdr, cs-lead, growth-lead)."
  transport: "Telegram + Discord. Cron scheduling. herdr CLI for tmux delegation."
  memory: "Persistent memory (MEMORY.md, USER.md). Session search via SQLite FTS5."
links:
  depends_on: [{target: tool-valorbrain}, {target: tool-multica}]
---

# Hermes Agent

The operational brain. Runs on WSL2 (DESKGUSI9). Communicates via Telegram (#operator-ai with MoltGus) and Discord.

## Crons

- **Health Ping (30m)** — Quick smoke test. Silent if nothing changed.
- **System Audit (2h)** — Deep analysis. Always share findings.

## herdr Integration

Delegates coding tasks to tmux sessions via herdr CLI. Fluxo: `herdr agent send` + `herdr pane send-keys <pane> Enter` (duas cmds, sempre).
