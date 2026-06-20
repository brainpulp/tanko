# Tanko — 3D Ditch Cascade & Fill-Time Calculator

Define a set of axis-aligned 3D ditches at different elevations, connect them so
each spills into the next, and compute the fill behaviour: which fills first, how
long each takes to reach spill, and the full event timeline. View the same result
from **Top** (plan), **Side** (elevation), or **3D**.

This is an **analytical model with a 3D visualisation on top** — not a fluid
simulation. The numbers come from exact event math; the animation replays them.

## Run

Open `index.html` in any modern browser. It's a single file; Three.js loads from a
CDN via an import map, so an internet connection is needed on first load.

## How it works

- **`simulate(scene) → { events, perDitch, fillOrder, totals, frames, ... }`** is a
  pure function with no rendering inside it (top of the `<script>` block). The
  renderer and the timeline scrubber only *sample* its output, so every level(t) is
  exact and analytic — linear interpolation between event times, no timestep error.
- Flow is piecewise-constant between events, so the engine advances event-to-event:
  for each filling ditch it computes time-to-spill, takes the minimum, advances all
  volumes, re-routes the newly-spilling ditch's inflow downstream in topological
  order, and repeats.

### Scene format (the source of truth — editable as JSON)

```js
{
  ditches: [{ id, name, x, y, length, width, depth, floorZ }],
  links:   [{ from, to, spillZ?, split? }],   // to: ditch id or "OUT" (waste)
  inflows: [{ to, rate }]                       // rate in L/s
}
```

Lengths in **m**, volumes in **m³**, inflow in **L/s** (1 m³ = 1000 L). Times are
computed in seconds and displayed auto-scaled (s / min / h).

## Model assumptions (v1)

1. Geometry is fixed and numeric — open-top rectangular boxes; rim = `floorZ + depth`.
2. Spill is by **explicit links** at a defined `spillZ` (default = the ditch's rim).
3. **Forward cascade (DAG)** — water flows source → downstream only. No back-flow or
   level equalisation. Loops are out of scope.
4. A spilling ditch is a **pass-through**: at its spill level it holds and passes all
   further inflow downstream at the incoming rate (links have unlimited carry
   capacity in v1).
5. **Rim-overflow / waste:** a ditch with no outgoing outlet fills past its notch to
   the rim, then routes the excess to waste (`OUT`) and is flagged `rim-overflow`.

## Open decisions — how v1 resolves them

- **Branch split** when one ditch feeds several: **even split by default**, with
  optional fixed fractions via `split` on each link (normalised). Priority-by-
  elevation is left for v2.
- **Equalisation / back-flow:** not modelled — v1 is forward-only (a different,
  linear-system solver).
- **Variable inflow over time:** not modelled — constant rate keeps the math exact.
- **Spill = rim vs. notch:** default **rim**; a lower `spillZ` models a weir/notch
  (drawn as a purple lip in the side/3D views).

## Worked example (also an in-page self-test)

- **A**: 10×1×1 m, `floorZ` 0 → cap 10 m³, spills at rim 1.0 m, link `A→B`. Inflow 5 L/s into A.
- **B**: 10×1×1 m, `floorZ` −0.5, link `B→OUT`.
- Result: A reaches spill at **2000 s** (≈33.3 min); B then fills in another 2000 s,
  full at **4000 s** (≈66.7 min). Fill order: **A, then B**.

The engine self-test (bottom-left of the UI) checks this and a few edge cases on load.
