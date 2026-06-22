#!/usr/bin/env python3
"""Render a diagram spec into a single self-contained, interactive HTML file.

Renderers:
  mermaid  -> structure diagrams (flow/sequence/state/class/ER/gantt/mindmap...)
  vega     -> Vega-Lite data charts (line/bar/scatter/area/histogram/...)

Output is one .html file with pan/zoom/hover interactivity baked in. Libraries
load from a CDN by default; pass --offline to inline them (requires network at
build time).

Usage:
  render.py --type mermaid --in spec.mmd  --out diagram.html [--title T] [--offline]
  render.py --type vega    --in spec.json --out chart.html   [--title T] [--offline]
"""

import argparse
import html
import json
import sys
import urllib.request

# Pinned versions so output is reproducible.
MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"
PANZOOM_URL = "https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"
VEGA_URL = "https://cdn.jsdelivr.net/npm/vega@5"
VEGALITE_URL = "https://cdn.jsdelivr.net/npm/vega-lite@5"
VEGAEMBED_URL = "https://cdn.jsdelivr.net/npm/vega-embed@6"


def _script_tag(url, offline):
    """Return a <script> tag, inlining the source when offline is requested."""
    if not offline:
        return f'<script src="{url}"></script>'
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            src = resp.read().decode("utf-8")
        return f"<script>\n{src}\n</script>"
    except Exception as e:  # noqa: BLE001 - fall back to CDN, never hard-fail
        sys.stderr.write(
            f"warning: could not inline {url} ({e}); falling back to CDN link\n"
        )
        return f'<script src="{url}"></script>'


def render_mermaid(spec, title, offline):
    mermaid_js = _script_tag(MERMAID_URL, offline)
    panzoom_js = _script_tag(PANZOOM_URL, offline)
    esc_spec = html.escape(spec)
    esc_title = html.escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc_title}</title>
<style>
  :root {{ color-scheme: light dark; }}
  html, body {{ margin: 0; height: 100%; font-family: system-ui, sans-serif; }}
  header {{ padding: 8px 14px; font-size: 14px; opacity: .75;
            border-bottom: 1px solid rgba(128,128,128,.3); }}
  #wrap {{ position: absolute; top: 38px; left: 0; right: 0; bottom: 0; }}
  #diagram {{ width: 100%; height: 100%; }}
  #hint {{ position: fixed; bottom: 10px; right: 14px; font-size: 12px;
           opacity: .55; user-select: none; }}
</style>
{mermaid_js}
{panzoom_js}
</head>
<body>
<header>{esc_title}</header>
<div id="wrap"><div id="diagram" class="mermaid">{esc_spec}</div></div>
<div id="hint">drag to pan &middot; scroll to zoom &middot; double-click to reset</div>
<script>
  mermaid.initialize({{ startOnLoad: false, securityLevel: "loose" }});
  (async () => {{
    const el = document.getElementById("diagram");
    const {{ svg }} = await mermaid.render("g", el.textContent.trim());
    el.innerHTML = svg;
    const svgEl = el.querySelector("svg");
    svgEl.setAttribute("width", "100%");
    svgEl.setAttribute("height", "100%");
    svgEl.style.maxWidth = "none";
    const pz = svgPanZoom(svgEl, {{
      zoomEnabled: true, controlIconsEnabled: false, fit: true, center: true,
      minZoom: 0.2, maxZoom: 20,
    }});
    svgEl.addEventListener("dblclick", () => {{ pz.reset(); }});
    window.addEventListener("resize", () => {{ pz.resize(); pz.fit(); pz.center(); }});
  }})();
</script>
</body>
</html>
"""


def render_vega(spec_json, title, offline):
    vega_js = _script_tag(VEGA_URL, offline)
    vegalite_js = _script_tag(VEGALITE_URL, offline)
    vegaembed_js = _script_tag(VEGAEMBED_URL, offline)
    esc_title = html.escape(title)
    # Embed the spec as JSON so quoting is safe.
    spec_blob = json.dumps(spec_json)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc_title}</title>
<style>
  :root {{ color-scheme: light dark; }}
  html, body {{ margin: 0; font-family: system-ui, sans-serif; }}
  header {{ padding: 8px 14px; font-size: 14px; opacity: .75;
            border-bottom: 1px solid rgba(128,128,128,.3); }}
  #chart {{ padding: 16px; }}
</style>
{vega_js}
{vegalite_js}
{vegaembed_js}
</head>
<body>
<header>{esc_title}</header>
<div id="chart"></div>
<script>
  const spec = {spec_blob};
  vegaEmbed("#chart", spec, {{ actions: true, tooltip: true }})
    .catch(err => {{
      document.getElementById("chart").textContent = "Vega-Lite error: " + err;
    }});
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Render a diagram spec to interactive HTML.")
    ap.add_argument("--type", required=True, choices=["mermaid", "vega"])
    ap.add_argument("--in", dest="infile", required=True, help="path to the spec file")
    ap.add_argument("--out", dest="outfile", required=True, help="path to write .html")
    ap.add_argument("--title", default="Diagram")
    ap.add_argument("--offline", action="store_true",
                    help="inline libraries (needs network at build time)")
    args = ap.parse_args()

    with open(args.infile, "r", encoding="utf-8") as f:
        spec = f.read()

    if args.type == "mermaid":
        out = render_mermaid(spec, args.title, args.offline)
    else:
        try:
            spec_json = json.loads(spec)
        except json.JSONDecodeError as e:
            sys.exit(f"error: --type vega expects valid JSON in {args.infile}: {e}")
        out = render_vega(spec_json, args.title, args.offline)

    with open(args.outfile, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {args.outfile}")


if __name__ == "__main__":
    main()
