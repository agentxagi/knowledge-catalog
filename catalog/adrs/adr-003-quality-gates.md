---
id: adr-003-quality-gates
type: adr
resource:
  name: adr-003-quality-gates
  displayName: "ADR-003: Quality Gates — Evidence, Anti-Sycophancy, Spec Drift"
  description: "Three quality gates adapted from Loki Mode RARV concept, implemented as Hermes logic"
labels:
  status: accepted
  date: 2026-06-14
decision:
  context: "Agents report 'done' without evidence. Reviews rubber-stamp. Specs drift from implementation."
  decision: "Three quality gates as Hermes coordinator logic: Evidence (git diff + tests), Anti-sycophancy (devil's advocate review), Spec drift (task terms vs result)."
  consequences: "False 'done' reports caught. Token-efficient (early gate blocks save review tokens). Agents held accountable."
  status: accepted
links:
  successor_of: []
---

# ADR-003: Quality Gates

## Context

Agents say "terminei" but produced nothing. Reviews approve everything. Implementation diverges from spec silently.

## Decision

Three quality gates, adapted from Loki Mode RARV concept (concepts only, zero BUSL code):

1. **Evidence Gate** — git diff non-empty + tests passing. Blocks before wasting review tokens.
2. **Anti-Sycophancy** — second agent reviews critically. If 3 reviewers approve unanimously, devil's advocate runs.
3. **Spec Drift** — compares task description terms with result. Catches "asked for X, got Y."

Gates run sequentially. First failure blocks. Gate logic is Hermes reasoning, not bash script.

## Consequences

- ✅ False completions caught early
- ✅ Token-efficient (evidence gate blocks before review)
- ✅ Specs respected
- ⚠️ Slower throughput (trade-off for quality)
