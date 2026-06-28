# Tanko — Request Tracker

Always include a **Done** list at the end of every response.

## Rules
- No initials anywhere (chamber IDs, labels, panel cards, results table, events)
- Full chamber names everywhere (default "Chamber N" when adding)
- Every response ends with a status list of all requests

---

## Request Log

### Session 1
- [x] Draggable depth/level markers on chamber walls with trigger actions
- [x] Both sidebars collapsible and resizable via drag-splitter
- [x] Opening names show full chamber names (not IDs/initials)
- [x] Level marker cards show full chamber names
- [x] Color picker for chambers and markers
- [x] Pump add button fixed (creates directly, no two-click workflow needed)
- [x] Water surface more realistic: canvas ripple texture + UV animation + high metalness
- [x] Fix mirrored wall labels (all faces now use unflipped texture)

### Session 2
- [x] Save everything (markers, pumps, etc.) — auto-saved to localStorage on every change
- [x] Presets as a dropdown (replaced 5 buttons with a single select)
- [x] Fix blank active tool button (CSS specificity fix: `#tools button.active` now visible)
- [x] Marker add button shows a warning when there are no chambers
- [x] No initials: chamber IDs now c1/c2/c3 (not A/B/C); default names "Chamber N"
- [x] No initials in right panel: results table, overflow warning, events, charts all use chamber names
- [x] No initials in chamber sidebar cards (shows name or ID)
- [x] Always-on status list in every Claude response (this file)
