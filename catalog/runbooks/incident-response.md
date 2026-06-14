---
id: runbooks/incident-response
type: runbook
resource:
  name: incident-response
  displayName: "Incident Response Runbook"
  description: "Procedimento operacional para incidentes de produção"
labels:
  setor: engenharia
  owner: iris-devops
overview:
  purpose: "Minimizar MTTR e garantir comunicação clara durante incidentes"
steps:
  - "Detectar (alerta, monitor, ou relato de cliente)"
  - "Confirmar severidade (P0=down total, P1=degradação, P2=minor)"
  - "Comunicar (P0/P1 → acordar Hermes/COO, notificar Lena se cliente impactado)"
  - "Isolar causa (logs, metrics, reproduzir)"
  - "Mitigar (rollback, restart, hotfix, ou workaround)"
  - "Resolver"
  - "Postmortem em 24h (sem dedo apontado, foco em causa raiz)"
  - "Documentar aprendizado no ValorBrain (postmortems collection)"
links: []
---

# Incident Response Runbook

## Severidade

| Nível | Definição | Resposta |
|-------|-----------|----------|
| **P0** | Serviço down, cliente impactado | Acordar Hermes + Lena imediatamente |
| **P1** | Degração significativa | Hermes investiga, Lena notifica cliente |
| **P2** | Minor, não impacta cliente | Iris resolve, documenta |

## Ordem de Prioridade

1. **Restaurar serviço** (rollback > restart > hotfix)
2. **Comunicar** (cliente, CEO, stakeholders)
3. **Investigar** (logs, metrics, reproduzir)
4. **Prevenir** (fix permanente, runbook update)

## Postmortem Template

```markdown
## [Data] — [Título do Incidente]

**Severidade:** P0/P1/P2
**Duração:** Xh Ym
**Impacto:** [clientes afetados, funcionalidade]

### Timeline
- HH:MM — Detecção
- HH:MM — Confirmação
- HH:MM — Mitigação
- HH:MM — Resolução

### Causa Raiz
[O que realmente aconteceu, não sintoma]

### O que funcionou
[Ações que ajudaram]

### O que falhou
[Ações que não ajudaram ou atrasaram]

### Action Items
- [ ] Fix permanente
- [ ] Alerta/monitoring novo
- [ ] Runbook update
```
