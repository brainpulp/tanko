---
name: diagram
description: >-
  Render diagrams and charts to a single self-contained, interactive HTML file
  (pan / zoom / hover) that opens in any browser with no server or build step.
  Use when the user wants to visualize a flowchart, architecture, sequence /
  state / ER diagram, mind map, Gantt, or a data chart (line / bar / scatter /
  time series), or asks to "draw", "diagram", "chart", "graph", or "visualize"
  something. Supports Mermaid (structure diagrams) and Vega-Lite (data charts).
---

# Diagram

Produce **interactive, self-contained HTML diagrams**. The output is a single
`.html` file the user opens in a browser. No server, no bundler. Interactivity
(pan, zoom, hover tooltips) is built in.

## When to use which renderer

| User wants | Use | Spec format |
|---|---|---|
| Flowchart, architecture, sequence, state, class, ER, mind map, Gantt, git graph | **mermaid** | Mermaid text |
| Line / bar / scatter / area / histogram, time series, data-driven dashboards | **vega** | Vega-Lite JSON |

If unsure, default to **mermaid** for "boxes and arrows" and **vega** for
"numbers / data".

## Workflow

1. Decide the renderer from the table above.
2. Write the diagram spec to a temp file:
   - Mermaid → `*.mmd` (plain Mermaid syntax, no surrounding ```` ```mermaid ````).
   - Vega-Lite → `*.json` (a valid Vega-Lite spec).
3. Render it:
   ```bash
   python3 .claude/skills/diagram/render.py \
     --type mermaid \
     --in /tmp/spec.mmd \
     --out /tmp/diagram.html \
     --title "My Diagram"
   ```
4. Tell the user the path and offer to open it / send it. In a remote session,
   use SendUserFile to deliver the `.html` so they can open it locally.

## Interactivity included

- **Mermaid**: rendered SVG is wrapped with pan/zoom (drag to pan, scroll to
  zoom, double-click to reset). Node `title` text shows as a native tooltip on
  hover — add it in Mermaid with `click NodeId callback "tooltip text"` or via a
  node label.
- **Vega-Lite**: Vega-Embed provides tooltips, and interval/point selections you
  add in the spec (e.g. `"params":[{"name":"grid","select":"interval","bind":"scales"}]`)
  give drag-zoom and pan for free.

## Online vs offline

By default libraries load from a CDN (smallest file, needs internet when
opened). For a fully offline file, pass `--offline` and the renderer will inline
the libraries it can fetch at build time. If the build environment has no
network, fall back to CDN mode and tell the user the file needs internet on
first open.

## Notes

- Keep one diagram per file; for a multi-panel view, use a Vega-Lite
  `vconcat`/`hconcat` or multiple Mermaid subgraphs.
- Validate Mermaid syntax mentally before rendering; the most common failure is
  unescaped special characters in labels — wrap labels in `"` quotes.
- This skill is project-agnostic: it does not touch the host app (e.g. the
  Three.js scene in this repo). It only writes the HTML file you ask for.
