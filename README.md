# Tanko — 3D Chamber Flow Simulator

Define axis-aligned 3D **chambers** at different elevations, connect them with
**openings** (holes in shared walls), **tubes** (pipes between any two chambers),
**inflows** and **drains**, then watch the water move. Build and edit the whole
scene directly in the 3D view, or as JSON. View from **Top** (plan), **Side**
(elevation), or **3D**.

This is a **rate-based hydraulic model** — flow through every connection follows the
orifice/weir equation, so sizes and valves actually change how fast things fill.

## Run

Open `index.html` in any modern browser. It's a single file; Three.js loads from a
CDN via an import map, so an internet connection is needed on first load.

## Editing in the 3D view

A toolbar sits top-left. In **Select** mode, drag the handles:

- **rim** (blue ▲) / **floor** (amber ▼) — raise/lower a chamber's top or bottom (side/3D)
- **move** (green ◆) / **size** (purple ■) — reposition / resize the footprint (top/3D)
- **walls** (grey bars) — drag a single border; it **snaps** to neighbouring walls and
  **won't overlap** another chamber
- **openings** — drag the bottom & top edges (side) and width (top); drag to slide it
  along the wall
- **tubes** — drag either endpoint's height; click the **valve** to open/close
- **inflows / drains** — drag to reposition; click the valve to open/close

The other toolbar buttons (**+Chamber, +Opening, +Tube, +Inflow, +Drain, Delete**)
let you add and remove everything by clicking in the scene.

## Hydraulic model

One flow primitive is used everywhere — the orifice/weir discharge

```
Q = ∫ Cd · w · √(2·g·head) dz   over the wetted aperture     (Cd ≈ 0.6, g = 9.81)
```

- **Openings** are rectangular apertures `[zBot, zTop]` of a given `width` in a shared
  wall. Drag the top **above the wall crest** → it behaves as a **cascade/weir** over
  `zBot`; keep it **below** → a **submerged window**. The regime switches itself.
- **Automatic spilling:** wherever two chambers' walls touch, water spills over the
  **lower shared rim** toward the lower side, at a rate proportional to the shared
  length. No setup — it's derived from geometry.
- **Loss to the wild:** wall segments with no neighbour overflow at the chamber's own
  rim and that fluid is **lost** (tracked separately from intentional drains).
- **Tubes** are round pipes (by `diameter`) between any two chambers, adjacent or not;
  flow is bidirectional and equalises levels. A low-attached tube acts as communicating
  vessels.
- **Drains** are round outlets to outside at an elevation `z`. **Inflows** are sources
  (L/s). Both have an open/closed **valve**.

The solver integrates volumes over small adaptive steps with flux limiting (no
overshoot), so mass is conserved: `inflow = stored + drained + lost`.

### Scene format (the source of truth — editable as JSON)

```js
{
  chambers: [{ id, name, x, y, length, width, depth, floorZ }],
  openings: [{ a, b, zBot, zTop, width }],            // a,b adjacent chamber ids
  tubes:    [{ from, to, fromZ, toZ, diameter, open }],
  inflows:  [{ to, rate, open }],                      // rate in L/s
  drains:   [{ from, z, diameter, open }]
}
```

Lengths in **m**, volumes in **m³**, inflow in **L/s** (1 m³ = 1000 L). Times are in
seconds, displayed auto-scaled (s / min / h). Legacy scenes using `ditches` /
`links` / `conduits` are migrated automatically on load.

## Self-test

The engine self-test (bottom-left of the UI) checks mass conservation across the
presets, automatic adjacency, valve behaviour, and orifice discharge on load.
