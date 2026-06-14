---
id: playbooks/deploy
type: playbook
resource:
  name: deploy
  displayName: "Deploy Process"
  description: "Processo de deploy para serviços da Valor Digital"
labels:
  setor: engenharia
  owner: iris-devops
overview:
  purpose: "Padronizar deploys com rollback rápido e zero downtime"
steps:
  - "Iris verifica health check do serviço atual (baseline)"
  - "Iris pull + build na máquina alvo"
  - "Iris deploy (systemctl restart ou blue-green)"
  - "Iris verifica health check pós-deploy"
  - "Se falhar → rollback imediato (binary anterior)"
  - "Iris documenta deploy no ValorBrain (deploy-log)"
  - "Se incidente → cria postmortem em 24h"
links: []
---

# Deploy Process

## Pré-deploy
- Health check do serviço atual (baseline de comportamento)
- Backup do binário atual (rollback rápido)
- Comunicar no canal apropriado antes de deploys disruptivos

## Deploy
- `systemctl restart` para serviços systemd
- Blue-green quando disponível
- Verificar health check em até 30s pós-deploy

## Rollback
- Se health check falha após 30s → restaurar binário anterior
- Se erro em produção → rollback primeiro, investigar depois

## Pós-deploy
- Documentar: versão, mudanças, hora
- Postmortem em 24h se incidente ocorreu

## Serviços Críticos
- ValorBrain (:7438) — pode ter downtime curto
- Multica (:8091) — pode ter downtime curto
- SaaS (:3000) — zero downtime ideal (PPR/standalone)
- VPS (nginx) — zero downtime obrigatório
