---
id: playbooks/code-review
type: playbook
resource:
  name: code-review
  displayName: "Code Review Process"
  description: "Quality gates and review process for all code changes"
labels:
  setor: engenharia
  owner: val-tech-lead
overview:
  purpose: "Ensure every code change passes through structured quality gates before merge"
steps:
  - "Evidence Gate: git diff non-empty + testes passando"
  - "Anti-Sycophancy Gate: segundo agente revisa criticamente"
  - "Spec Drift Gate: spec original comparada com implementação"
  - "Review by Tech Lead (Val) before merge"
  - "Documentar padrão recorrente em code-review-patterns no ValorBrain"
links: []
---

# Code Review Process

Todo PR passa por 3 gates sequenciais. Primeira falha bloqueia.

## Gate 1: Evidence
- `git diff` non-empty
- Testes passando (`bun test` / `cargo test` / `go test`)
- Sem arquivos gerados/acidentais no diff

## Gate 2: Anti-Sycophancy
- Segundo agente revisa o diff
- Se 3+ reviewers aprovam unanimamente → devil's advocate obrigatório
- Nunca rubber stamp

## Gate 3: Spec Drift
- Termos da issue/task comparados com o diff
- Se task pediu X e diff não menciona X → flag

## Flywheel
Padrões recorrentes de review → `code-review-patterns` no ValorBrain (L1).
