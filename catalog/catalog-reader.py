#!/usr/bin/env python3
"""
catalog-reader.py — Lightweight Metadata as Code reader for Valor Digital.
Replaces GCP's kcmd. Walks catalog/ directory, parses YAML frontmatter,
builds in-memory graph of entries + links, and can output:
  - JSON graph (for ValorBrain ingestion)
  - Org chart (text tree)
  - Validation report (missing required aspects, broken links)

Usage:
  python3 catalog-reader.py --tree           # Print org chart
  python3 catalog-reader.py --json           # JSON graph for ValorBrain
  python3 catalog-reader.py --validate       # Validate catalog integrity
  python3 catalog-reader.py --query <id>     # Show entry details
  python3 catalog-reader.py --ingest         # Ingest into ValorBrain API
"""

import os
import sys
import re
import json
import argparse
import yaml
import requests
from pathlib import Path
from collections import defaultdict

CATALOG_DIR = Path(__file__).parent
CATALOG_YAML = CATALOG_DIR / "catalog.yaml"


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse markdown file with YAML frontmatter. Returns (metadata, body)."""
    text = filepath.read_text(encoding="utf-8")
    
    # Match frontmatter between --- markers
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    
    try:
        meta = yaml.safe_load(match.group(1))
        if meta is None:
            meta = {}
    except yaml.YAMLError as e:
        print(f"⚠️  YAML parse error in {filepath.name}: {e}", file=sys.stderr)
        return {}, text
    
    return meta, match.group(2)


def load_catalog() -> tuple[dict, list[dict]]:
    """Load catalog.yaml manifest and all entries from the directory tree."""
    manifest = {}
    if CATALOG_YAML.exists():
        with open(CATALOG_YAML) as f:
            manifest = yaml.safe_load(f) or {}
    
    entries = []
    md_files = sorted(CATALOG_DIR.rglob("*.md"))
    
    for fp in md_files:
        meta, body = parse_frontmatter(fp)
        if not meta or "id" not in meta:
            continue
        
        meta["_path"] = str(fp.relative_to(CATALOG_DIR))
        meta["_body"] = body.strip()
        meta["_filename"] = fp.name
        entries.append(meta)
    
    return manifest, entries


def build_graph(entries: list[dict]) -> dict:
    """Build adjacency lists from entry links."""
    entry_ids = {e["id"] for e in entries}
    graph = defaultdict(lambda: defaultdict(list))
    
    for entry in entries:
        eid = entry["id"]
        links = entry.get("links", {})
        
        # Handle links that are list instead of dict (malformed)
        if isinstance(links, list):
            continue
        
        for link_type, link_list in links.items():
            if not isinstance(link_list, list):
                link_list = [link_list]
            
            for link in link_list:
                if isinstance(link, dict):
                    target = link.get("target", "")
                    if target:
                        graph[eid][link_type].append(target)
    
    return dict(graph)


def print_org_tree(entries: list[dict], graph: dict):
    """Print the org chart as a tree based on reports_to links."""
    # Build reverse map: who reports to whom (manager → [directs])
    reports_to_map = defaultdict(list)
    roots = []
    all_personas = set()
    
    for entry in entries:
        if entry.get("type") != "persona":
            continue
        
        eid = entry["id"]
        all_personas.add(eid)
        managers = graph.get(eid, {}).get("reports_to", [])
        
        if managers:
            for m in managers:
                reports_to_map[m].append(eid)
        else:
            roots.append(eid)
    
    # Find roots: personas that are targets of reports_to but don't report to anyone in the catalog
    # OR personas with no reports_to at all
    all_targets = set()
    for directs in reports_to_map.values():
        all_targets.update(directs)
    
    everyone_with_manager = set()
    for directs in reports_to_map.values():
        everyone_with_manager.update(directs)
    
    # Roots are managers who don't report to anyone in our catalog
    managers_set = set(reports_to_map.keys())
    for m in managers_set:
        if m not in everyone_with_manager:
            roots.append(m)
    
    # Also include personas with no reports_to and no directs (lone wolves)
    for entry in entries:
        if entry.get("type") != "persona":
            continue
        eid = entry["id"]
        if eid not in everyone_with_manager and eid not in managers_set:
            roots.append(eid)
    
    # Deduplicate roots while preserving order
    seen = set()
    deduped_roots = []
    for r in roots:
        if r not in seen:
            seen.add(r)
            deduped_roots.append(r)
    
    def get_display(eid):
        for e in entries:
            if e["id"] == eid:
                res = e.get("resource", {})
                name = res.get("displayName", eid)
                title = e.get("labels", {}).get("nivel", "")
                return f"{name}" + (f" ({title})" if title else "")
        return eid
    
    def print_tree(eid, indent=0, is_last=True):
        prefix = "    " * indent + ("└── " if is_last else "├── ") if indent > 0 else ""
        print(f"{prefix}{get_display(eid)}")
        
        children = sorted(reports_to_map.get(eid, []))
        for i, child in enumerate(children):
            print_tree(child, indent + 1, i == len(children) - 1)
    
    print("\n🌳 Valor Digital — Organograma\n")
    for root in deduped_roots:
        print_tree(root)


def print_json(entries: list[dict], graph: dict, manifest: dict):
    """Output the full catalog as JSON for ValorBrain ingestion."""
    output = {
        "manifest": {
            "scope": manifest.get("scope", ""),
            "entry_types": list(manifest.get("entryTypes", {}).keys()),
            "link_types": list(manifest.get("linkTypes", {}).keys()),
        },
        "entries": [],
        "links": graph,
        "stats": {
            "total_entries": len(entries),
            "by_type": {},
        }
    }
    
    for entry in entries:
        clean = {k: v for k, v in entry.items() if not k.startswith("_")}
        clean["_path"] = entry["_path"]
        output["entries"].append(clean)
        etype = entry.get("type", "unknown")
        output["stats"]["by_type"][etype] = output["stats"]["by_type"].get(etype, 0) + 1
    
    print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


def validate(entries: list[dict], graph: dict, manifest: dict) -> bool:
    """Validate catalog integrity. Returns True if all checks pass."""
    errors = []
    warnings = []
    entry_ids = {e["id"] for e in entries}
    
    # Check required aspects per type
    entry_types = manifest.get("entryTypes", {})
    
    for entry in entries:
        eid = entry["id"]
        etype = entry.get("type")
        
        if not etype:
            errors.append(f"{eid}: missing 'type'")
            continue
        
        # Check required aspects
        type_def = entry_types.get(etype, {})
        required = type_def.get("requiredAspects", [])
        
        for req in required:
            if req not in entry and req not in entry.get("labels", {}):
                # Check nested
                found = False
                for key in [req, req.replace("-", "_")]:
                    if key in entry:
                        found = True
                        break
                if not found:
                    # Check if it's in the body (overview)
                    if req == "overview" and entry.get("_body"):
                        found = True
                    elif req in ["identity", "responsibilities", "decision", "contacts"]:
                        if any(k in entry for k in [req, req.replace("-","_")]):
                            found = True
                    
                    if not found:
                        warnings.append(f"{eid}: missing required aspect '{req}' for type '{etype}'")
        
        # Check link targets exist
        links = entry.get("links", {})
        if isinstance(links, list):
            links = {}
        for link_type, link_list in links.items():
            if not isinstance(link_list, list):
                link_list = [link_list]
            for link in link_list:
                if isinstance(link, dict):
                    target = link.get("target", "")
                    if target and target not in entry_ids:
                        warnings.append(f"{eid}: link '{link_type}' → '{target}' (target not in catalog)")
    
    # Check for duplicate IDs
    id_counts = defaultdict(int)
    for e in entries:
        id_counts[e["id"]] += 1
    for eid, count in id_counts.items():
        if count > 1:
            errors.append(f"Duplicate ID: '{eid}' ({count} files)")
    
    # Report
    if errors:
        print(f"\n❌ {len(errors)} ERROR(S):")
        for e in errors:
            print(f"  ✗ {e}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  • {w}")
    
    if not errors and not warnings:
        print("\n✅ Catalog is clean — no errors, no warnings.")
    
    print(f"\nStats: {len(entries)} entries")
    by_type = defaultdict(int)
    for e in entries:
        by_type[e.get("type", "unknown")] += 1
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")
    
    return len(errors) == 0


def query_entry(entries: list[dict], graph: dict, entry_id: str):
    """Show details for a specific entry."""
    entry = None
    for e in entries:
        if e["id"] == entry_id:
            entry = e
            break
    
    if not entry:
        print(f"Entry '{entry_id}' not found.")
        return
    
    print(f"\n{'='*60}")
    res = entry.get("resource", {})
    print(f"  {res.get('displayName', entry_id)}")
    print(f"  ID: {entry['id']}")
    print(f"  Type: {entry.get('type', '?')}")
    if entry.get("labels"):
        labels = entry["labels"]
        print(f"  Labels: {', '.join(f'{k}={v}' for k,v in labels.items())}")
    print(f"  File: {entry.get('_path', '?')}")
    print(f"{'='*60}")
    
    # Identity
    ident = entry.get("identity", {})
    if ident:
        print(f"\n  Nome: {ident.get('nome', '?')}")
        print(f"  Apelido: {ident.get('apelido', '?')}")
        print(f"  Personalidade: {ident.get('personalidade', '?')}")
        print(f"  Tom: {ident.get('tom', '?')}")
    
    # Links
    links = graph.get(entry_id, {})
    if links:
        print(f"\n  Links:")
        for ltype, targets in links.items():
            for t in targets:
                # Find display name
                display = t
                for e in entries:
                    if e["id"] == t:
                        display = e.get("resource", {}).get("displayName", t)
                        break
                print(f"    {ltype} → {display} ({t})")
    
    # Body
    body = entry.get("_body", "")
    if body:
        print(f"\n{body[:500]}")
        if len(body) > 500:
            print("...")


def ingest_to_valorbrain(entries: list[dict], manifest: dict):
    """Ingest all catalog entries into ValorBrain as structured documents."""
    import os
    
    vb_url = os.environ.get("VB_URL", "http://localhost:7438")
    vb_token = os.environ.get("VB_TOKEN", "")
    vb_tenant = os.environ.get("VB_TENANT", "3ceeb048-754c-4910-a798-112ae867e9a4")
    
    if not vb_token:
        print("❌ VB_TOKEN not set. Export VB_TOKEN=<token> first.")
        sys.exit(1)
    
    headers = {
        "Authorization": f"Bearer {vb_token}",
        "X-Tenant-ID": vb_tenant,
        "Content-Type": "application/json",
    }
    
    collection = "org-catalog"
    success = 0
    failed = 0
    
    for entry in entries:
        eid = entry["id"]
        res = entry.get("resource", {})
        title = res.get("displayName", eid)
        
        # Build body from frontmatter + markdown
        meta_clean = {k: v for k, v in entry.items() if not k.startswith("_")}
        body_yaml = yaml.dump(meta_clean, allow_unicode=True, default_flow_style=False)
        body = f"```yaml\n{body_yaml}\n```\n\n{entry.get('_body', '')}"
        
        payload = {
            "collection": collection,
            "path": f"org-catalog/{entry.get('type','unknown')}/{eid}",
            "title": f"[{entry.get('type','?').upper()}] {title}",
            "content": body,
        }
        
        try:
            r = requests.post(f"{vb_url}/documents", headers=headers, json=payload, timeout=30)
            data = r.json()
            action = data.get("action", data.get("status", "?"))
            print(f"  {'✅' if r.status_code < 400 else '❌'} {eid}: {action}")
            if r.status_code < 400:
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ {eid}: {e}")
            failed += 1
    
    print(f"\n📊 Ingested: {success} success, {failed} failed")
    print(f"   Collection: {collection}")
    print(f"   Tenant: {vb_tenant}")


def main():
    parser = argparse.ArgumentParser(description="Valor Digital Catalog Reader")
    parser.add_argument("--tree", action="store_true", help="Print org chart tree")
    parser.add_argument("--json", action="store_true", help="Output JSON graph")
    parser.add_argument("--validate", action="store_true", help="Validate catalog")
    parser.add_argument("--query", type=str, help="Query specific entry")
    parser.add_argument("--ingest", action="store_true", help="Ingest into ValorBrain")
    
    args = parser.parse_args()
    
    manifest, entries = load_catalog()
    graph = build_graph(entries)
    
    if args.tree:
        print_org_tree(entries, graph)
    elif args.json:
        print_json(entries, graph, manifest)
    elif args.validate:
        validate(entries, graph, manifest)
    elif args.query:
        query_entry(entries, graph, args.query)
    elif args.ingest:
        ingest_to_valorbrain(entries, manifest)
    else:
        # Default: summary
        print(f"\n📊 Valor Digital Catalog — {len(entries)} entries\n")
        by_type = defaultdict(int)
        for e in entries:
            by_type[e.get("type", "unknown")] += 1
        for t, c in sorted(by_type.items()):
            print(f"  {t:15s} {c}")
        print(f"\n  Use --tree, --json, --validate, --query <id>, or --ingest")


if __name__ == "__main__":
    main()
