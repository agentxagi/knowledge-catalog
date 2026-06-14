---
id: playbooks/billing
type: playbook
resource:
  name: billing
  displayName: "Billing & Finance Process"
  description: "Processo mensal de faturamento, cobrança, e relatório financeiro"
labels:
  setor: operacoes
  owner: tav-ops
overview:
  purpose: "Garantir que receita entre, despesas sejam controladas, e o CEO tenha visibilidade financeira"
steps:
  - "Tav gera fatura mensal para cada cliente ativo"
  - "Tav envia fatura via canal acordado (email, WhatsApp)"
  - "Tav monitora pagamento (prazo: 7 dias úteis)"
  - "Se inadimplente → Tav envia lembrete + escalado para Lena se >15 dias"
  - "Tav paga APIs (ZAI, OpenRouter, Cloudflare, domínios)"
  - "Tav compila relatório mensal: receita, despesas, margem, projeção"
  - "Tav grava unit-economics no ValorBrain"
links: []
---

# Billing & Finance Process

## Ciclo Mensal

**Dia 1-5:** Faturamento
- Gerar faturas para todos os clientes ativos
- Enviar via canal preferido do cliente

**Dia 6-15:** Cobrança
- Monitorar pagamentos
- Lembrete amigável no dia 10 se não pago

**Dia 16+:** Escalação
- Inadimplência >15 dias → Lena (CS) interage
- Inadimplência >30 dias → Rafa (Sales) renegocia

**Dia 25:** Fechamento
- Pagar contas (APIs, infra, domínios)
- Compilar relatório financeiro
- Enviar ao CEO

## Relatório Mensal (formato)

```
Receita: R$ X
  Cliente A: R$ Y
  Cliente B: R$ Z
Despesas: R$ W
  APIs: R$
  Infra: R$
Margem: R$ (Receita - Despesas)
MRR: R$
Projeção próximo mês: R$
```
