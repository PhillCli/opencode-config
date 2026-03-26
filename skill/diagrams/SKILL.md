---
name: diagrams
description: Create readable cloud/infrastructure architecture diagrams using Python diagrams (mingrammer/diagrams, Graphviz). Use whenever user asks for infra/cloud topology visuals, architecture maps, GCP/AWS/Azure resource overviews, network/data-flow diagrams, or wants to improve existing infrastructure diagram readability/reviewability. Prefer this skill even when user says only "diagram" if the target is cloud resources and relationships. Do NOT use for Mermaid/PlantUML-specific requests.
---

# Diagrams (Python) — Infrastructure Diagram Taste Guide

Use this skill to generate **human-reviewable** infrastructure diagrams with `diagrams~=0.25.1`.

Primary goal: optimize for reviewer comprehension, not “show everything in one picture”.

## Default Deliverable: L1/L2/L3 Set

Unless user explicitly asks for a single view, produce three diagrams:

1. **L1 — Context/Boundaries**
   - Projects/accounts, trust boundaries, internet/external systems, major platform blocks.
   - No internal implementation detail.

2. **L2 — Runtime/Data Flow**
   - Request/data path from ingress to app/services to databases/queues.
   - Only components participating in runtime behavior.

3. **L3 — State/Operations**
   - Buckets/storage, backups/snapshots, IAM/service accounts, monitoring/alerts, deployment identities.
   - Focus on operational ownership and lifecycle.

If all three become dense, split further (e.g., L3a storage-backup, L3b IAM-observability).

## Layout Rules (taste baseline)

- Prefer **left-to-right** (`direction="LR"`) unless user asks otherwise.
- Keep one dominant reading direction per diagram.
- Max cluster nesting depth: **2**.
- Use short node labels (1–3 words). Move long details into caption/notes.
- Keep edge labels minimal and meaningful (protocol, intent, or data class).
- Add a small legend if edge styles/colors have semantics.
- Prefer multiple crisp diagrams over one crowded diagram.

## Edge/Noise Control Rules

When edges become noisy:

1. Collapse repetitive nodes into grouped arrays/lists.
2. Route fan-out/fan-in through a neutral hub node (`Node("", shape="plaintext", width="0", height="0")`) when needed.
3. Consider merged edges with Graphviz concentrators:
   - `graph_attr["concentrate"] = "true"`
   - `graph_attr["splines"] = "spline"`
   - Works best with default `dot` layout engine.
4. Use `minlen` and selective `constraint="false"` only to improve readability.

Important nuance: diagrams’ default edge routing tends to orthogonal style; merged-edge behavior requires `splines="spline"`.

## Visual Semantics

Use consistent edge semantics:

- **solid**: primary runtime/data path
- **dashed**: control/deploy/management path
- **dotted**: backup/replication/async path

Use color sparingly. If color used, reserve it for category semantics and keep a legend.

## Cluster Semantics

Cluster by boundaries reviewers care about:

- Cloud project/account/subscription
- Network boundary (VPC/VNet)
- Data domain (runtime vs backup)
- Identity/control plane (IAM/deploy)

Avoid decorative clustering that adds boxes but no meaning.

## Recommended Diagram Defaults

```python
from diagrams import Diagram

graph_attr = {
    "pad": "0.3",
    "nodesep": "0.45",
    "ranksep": "0.75",
    "fontsize": "18",
    "fontname": "Inter",
    "splines": "ortho",  # switch to "spline" when using concentrate
}

node_attr = {
    "fontsize": "13",
    "fontname": "Inter",
}

edge_attr = {
    "fontsize": "11",
    "fontname": "Inter",
}

with Diagram(
    "Infra L1 Context",
    show=False,
    direction="LR",
    outformat=["png", "svg"],
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    ...
```

## Output Contract

When implementing, produce:

- Source code (`.py`) for each diagram
- Rendered `png` + `svg` for each diagram
- Brief `README.md` or notes section with:
  - assumptions
  - legend semantics
  - what each level includes/excludes

Suggested naming:

- `l1-context.{py,png,svg}`
- `l2-runtime-flow.{py,png,svg}`
- `l3-ops-state.{py,png,svg}`

## Quality Gate (must pass)

Before finishing, verify:

1. Can reviewer explain system in <60 seconds from L1?
2. Can reviewer trace request/data path from left to right in L2?
3. Can reviewer locate backups, IAM identities, and monitoring in L3?
4. Are there avoidable crossing edges still present?
5. Any label too long for quick scan?
6. Any cluster without semantic value?
7. Is there a clear legend when non-default edge semantics are used?

If 2+ checks fail, revise layout/scope split before finalizing.

## Anti-Patterns

- Single “everything diagram” with mixed abstraction levels.
- Long prose labels inside node names.
- Unlabeled edge styles/colors.
- Mixing runtime flow with backup/IAM details in same view unless tiny system.
- Excessive nested clusters.
