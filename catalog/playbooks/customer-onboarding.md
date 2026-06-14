---
id: playbooks/customer-onboarding
type: playbook
resource:
  name: customer-onboarding
  displayName: "Customer Onboarding"
  description: "Processo de onboarding de novos clientes — handoff Sales → CS"
labels:
  setor: clientes
  owner: lena-cs-lead
overview:
  purpose: "Garantir que cada novo cliente tenha onboarding estruturado, com expectativas claras e plano de sucesso"
steps:
  - "Sales (Rafa) cria issue no Multica: 'Onboarding: [Cliente]'"
  - "Sales preenche: perfil, necessidades, expectativas, pricing"
  - "CS Lead (Lena) recebe issue e cria plano de onboarding"
  - "CS Specialist (Theo) agenda call de boas-vindas (primeira semana)"
  - "Theo configura acesso, integrações, e treina usuário inicial"
  - "Lena define health score baseline e métricas de sucesso"
  - "Rafa disponível para warm handoff na primeira semana"
  - "Theo documenta caso no ValorBrain (kb-solutions)"
links: []
---

# Customer Onboarding

## Handoff Sales → CS

1. **Rafa cria issue** no Multica com template:
   - Perfil do cliente (tamanho, segmento, stack)
   - Necessidades mapeadas
   - Expectativas de prazo
   - Pricing acordado
   - Pessoas-chave (decisor, usuário principal)

2. **Lena assume** e cria plano:
   - Cronograma de onboarding (semana 1, 2, 4)
   - Métricas de sucesso (definidas com cliente)
   - Health score inicial

3. **Theo executa** na linha de frente:
   - Setup técnico (acessos, integrações)
   - Treinamento inicial
   - Documentação de caso

## Success Criteria

- Cliente usando o produto ativamente em 7 dias
- Primeiro ticket resolvido em 24h
- Health score verde em 30 dias
