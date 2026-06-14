---
id: adr-001-multica-task-store
type: adr
resource:
  name: adr-001-multica-task-store
  displayName: "ADR-001: Multica as Task Store, Hermes as Orchestrator"
  description: "Multica stores tasks/issues/projects. Hermes orchestrates. Daemon autopilot disabled."
labels:
  status: accepted
  date: 2026-06-14
decision:
  context: "Multica has its own daemon with autopilot that tries to orchestrate agents. Hermes also coordinates via crons/herdr. Two coordination layers competing."
  decision: "Multica = task store only (issues, projects, squads, lifecycle). Hermes = orchestrator (reads Multica API, delegates, validates, updates). Daemon heartbeat stays for runtime health, but autopilot disabled."
  consequences: "Single source of truth for task state. Hermes has full context. Daemon no longer makes autonomous assignment decisions."
  status: accepted
links:
  successor_of: []
---

# ADR-001: Multica as Task Store, Hermes as Orchestrator

## Context

Multica has a daemon with autopilot that assigns tasks to agents via runtimes. Hermes also coordinates via crons and herdr. Two layers competing for the same responsibility caused:
- Duplicate work
- Stale runtime IDs (daemon "at capacity" with ghost agents)
- No clear authority on task assignment

## Decision

**Multica = task store.** Issues, projects, squads, lifecycle, assignments — all live in Multica.

**Hermes = orchestrator.** I (default profile) read Multica API, decide priority, delegate via herdr/tmux, validate results with quality gates, and update Multica back.

**Daemon:** Heartbeat for runtime health monitoring stays. Autopilot and auto-assignment disabled.

## Consequences

- ✅ Single source of truth for task state
- ✅ Hermes has full context (ValorBrain + Multica + Telegram)
- ✅ No more ghost runtime IDs
- ⚠️ Hermes is single point of coordination failure (mitigated by crons)
