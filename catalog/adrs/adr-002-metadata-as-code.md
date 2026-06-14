---
id: adr-002-metadata-as-code
type: adr
resource:
  name: adr-002-metadata-as-code
  displayName: "ADR-002: Metadata as Code for Organizational Knowledge"
  description: "Adopt GCP knowledge-catalog concepts (entries, aspects, links, catalog.yaml) for org docs"
labels:
  status: accepted
  date: 2026-06-14
decision:
  context: "Org docs (personas, playbooks, ADRs, client profiles) are unstructured markdown. Agents can't programmatically query relationships. ValorBrain ingests text without structure."
  decision: "Adopt Metadata as Code format: markdown files with YAML frontmatter, organized by type, with catalog.yaml manifest declaring schema. Adapted from GCP knowledge-catalog concepts."
  consequences: "Org graph is queryable. ValorBrain ingestion is structured. Changes are versioned in git. Python reader replaces kcmd."
  status: accepted
links:
  successor_of: []
---

# ADR-002: Metadata as Code for Organizational Knowledge

## Context

Org knowledge scattered across 5 places (Multica issues, ValorBrain docs, Hermes memory, Telegram, human brain). Docs are unstructured — agents must guess relationships from prose.

## Decision

Adopt **Metadata as Code** (adapted from [GCP knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) concepts):

1. **Entry/Aspect/EntryLink data model** — entities with structured metadata and typed relationships
2. **Markdown + YAML frontmatter** — human-readable, git-versionable, agent-parseable
3. **catalog.yaml manifest** — declares entry types, aspect types, link types
4. **Python reader** — replaces kcmd, feeds structured data to ValorBrain

Rejected: GCP Dataplex/BigQuery integration, kcmd TypeScript sync tool, context overlay mode.

## Consequences

- ✅ Org graph is programmatically queryable
- ✅ ValorBrain ingestion is structured (not random text)
- ✅ Changes are auditable via git
- ✅ Agents can resolve relationships without semantic search
- ⚠️ Requires discipline to maintain frontmatter
