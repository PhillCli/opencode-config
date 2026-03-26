---
name: diagrams
description: Create readable cloud/infrastructure architecture diagrams using Python diagrams (mingrammer/diagrams, Graphviz). Use whenever user asks for infra/cloud topology visuals, architecture maps, GCP/AWS/Azure resource overviews, network/data-flow diagrams, or wants to improve existing infrastructure diagram readability/reviewability. Prefer this skill even when user says only "diagram" if the target is cloud resources and relationships. Do NOT use for Mermaid/PlantUML-specific requests.
---

# Diagrams (Python) — Infrastructure Diagram Quality Rules

Use this skill to generate reviewer-friendly infrastructure diagrams with `diagrams~=0.25.1`.

Primary objective: readable architecture review artifacts, not maximum detail density.

## Non-negotiable defaults

- Direction: `LR`.
- Routing: `splines="ortho"` (rectilinear edges).
- Do not use `splines="spline"` unless user explicitly asks for curved routing.
- No decorative legends.
- No ambiguous cluster or node names.

## Required L1/L2/L3 split

Unless user explicitly requests otherwise, produce 3 views:

1. **L1 Context**
   - External actors/systems, cloud projects/accounts, core platform blocks.
   - Exclude IAM internals, backup internals, per-bucket detail.

2. **L2 Runtime flow**
   - Request/data path only: ingress -> runtime -> db/queue/storage -> egress.
   - Exclude deploy identity chains and governance wiring.

3. **L3 Operations/state**
   - Storage state, backups/snapshots, IAM bindings relevant to operations, monitoring.
   - Exclude user request narrative.

If any view gets crowded, split further (e.g. `l3a-storage-backup`, `l3b-iam-monitoring`).

## Naming taxonomy (strict)

### Forbidden labels (unless that is exact product name)

- `Edge`
- `Deploy identities`
- `Runtime services`
- `Service` (alone)
- `Identity` (alone)

### Preferred labels

- Use exact provider/service names where known (`Cloud NAT`, `Pub/Sub`, `Secret Manager`, `Compute Engine`).
- For generic components, include type suffix (`Auth API`, `App VM`, `Backup Bucket`).
- Keep labels short (1-3 words).

## Edge style policy

- Use one edge style by default (solid).
- Introduce dashed/dotted only when there is clear semantic need.
- If using 2+ edge styles, explain semantics in README (not giant in-diagram legend).
- Keep edge labels minimal (`req`, `sql`, `events`, `snap`, `dump`) only if needed for comprehension.

## Graphviz profile (recommended)

```python
graph_attr = {
    "rankdir": "LR",
    "splines": "ortho",
    "nodesep": "0.55",
    "ranksep": "0.95",
    "pad": "0.25",
    "newrank": "true",
    "remincross": "true",
    "concentrate": "false",
    "fontname": "Helvetica",
    "fontsize": "12",
}

node_attr = {
    "fontname": "Helvetica",
    "fontsize": "10",
}

edge_attr = {
    "fontname": "Helvetica",
    "fontsize": "9",
    "color": "#3a3a3a",
}
```

Only deviate when requested by user.

## Complexity budget

Per diagram target:

- <= 14 nodes
- <= 18 edges
- <= 5 edge labels
- cluster nesting depth <= 2

If above budget, split the diagram rather than compressing with visual tricks.

## Cluster rules

Cluster only by meaningful boundaries:

- project/account
- network boundary (VPC/VNet)
- data domain (runtime vs backup)

Avoid clusters that restate obvious grouping without review value.

## Hub and fan-out control

- Avoid blank hub nodes in L1.
- In L2/L3, use hub node only when one source fans to >=4 similar targets.
- If hub introduced, keep it unlabeled and local; do not let it create long crossing arcs.

## Output and portability

Produce:

- `.py` source for each view
- `.png` for review (canonical)
- `.svg` optional/secondary
- `README.md` (assumptions + include/exclude per level + any edge semantics)

Important: `diagrams` SVG often references absolute local icon paths (`xlink:href=/home/...`).
If SVG portability is needed, call out limitation clearly and keep PNG as primary review artifact.

## Pre-delivery quality gate (must pass)

1. All edges are orthogonal (no smooth curves).
2. Reading direction is obvious left->right.
3. No ambiguous labels from forbidden list.
4. L1 excludes low-level internals.
5. L2 shows one coherent runtime path.
6. L3 focuses on state/ops, not user request flow.
7. No avoidable crossing lines remain.
8. No giant legend panel consuming diagram area.
9. Clusters are semantic, not decorative.
10. PNG renders all cloud icons.
11. If SVG generated, limitations documented.

If any item fails, revise before final output.

## Anti-patterns

- One mega-diagram mixing abstraction levels.
- Curved edges in LR infra diagrams.
- Legend as separate large cluster with sample arrows.
- Synthetic labels not tied to real architecture terminology.
- Forcing all concerns into exactly 3 files when split would be clearer.
