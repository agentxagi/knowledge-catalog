---
id: tool-valorbrain
type: tool
resource:
  name: valorbrain
  displayName: "ValorBrain"
  description: "Institutional memory OS — vector search, document store, cross-agent knowledge"
labels:
  layer: L0-L2
  port: "7438"
  status: production
overview:
  purpose: "Knowledge OS for the Valor Digital ecosystem. Stores, searches, and retrieves institutional memory across all agents."
  api: "REST :7438. POST /documents (create/update), GET /documents/:id, GET /documents?pattern=*, POST /search, POST /retrieve"
  client_mode: ":7440 — LLM-less client, same PostgreSQL DB, tenant header required"
  multi_tenant: "Tenant VD = 3ceeb048-754c-4910-a798-112ae867e9a4"
  auth: "Bearer token (vb_admin_unlimited_*, vb_agent_*, vb_*)"
links:
  depends_on: []
---

# ValorBrain

Engine: TypeScript, PostgreSQL backend. Hybrid search (keyword + semantic). Embedding via Jina v3 (:7997), Reranker (:8096).

## Classification

- **L0** — Canônico (constituição da empresa: ORG.md, ADRs, pricing, ICP)
- **L1** — Operacional (estado atual, runbooks, patterns semi-estáveis)
- **L2** — Efêmero (logs, tickets, health checks)

## Flywheel

L2 → padrões extraídos → L1 → melhores práticas provadas → L0
