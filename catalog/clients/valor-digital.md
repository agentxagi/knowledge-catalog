---
id: client-valor-digital
type: client
resource:
  name: valor-digital
  displayName: "Valor Digital (Produto Próprio)"
  description: "Produto interno — ValorBrain, valorcode, SaaS, infra"
labels:
  status: produto-proprio
  prioridade: maxima
overview:
  produto: "ValorBrain (memory OS) + valorcode (agentic editor) + SaaS"
  stack: "TypeScript, PostgreSQL 18, Next.js standalone, K3s, Cloudflare"
  url_saas: "valorbrain.valor.digital"
  url_api: ":7438"
  workspace_multica: "gustavo-b6b0e758"
contacts:
  tech_lead: val-tech-lead
  devops: iris-devops
links:
  client_of: [{target: val-tech-lead}]
---

# Valor Digital (Produto Próprio)

Não é um cliente externo — é o produto da empresa. Prioridade máxima.

## Produtos

### ValorBrain
Memory OS. Vector search + document store. REST API :7438.
- Engine: TypeScript, PostgreSQL backend
- Hybrid search (keyword + semantic)
- Multi-tenant (tenant VD = 3ceeb048)
- SaaS: valorbrain.valor.digital (Next.js standalone)

### valorcode
Agentic editor. Fork/rebrand do jcode.
- Client-mode LLM-less no :7440
- Whitelabel via BRAND.toml
- Binário: /root/.local/bin/valorcode

### Infraestrutura
- WSL2 (DESKGUSI9): heavy lifting
- VPS (100.71.216.11): always-on
- Cloudflare tunnels: DNS, proxy, TLS
- Tailscale: rede privada
