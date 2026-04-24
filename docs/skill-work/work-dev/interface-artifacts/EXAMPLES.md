# Interface Artifact Examples

These examples show how interface artifacts help the operator inspect or navigate a surface without becoming canonical truth.

## A. Strategy notebook visualizer

**Intent**  
Help the operator see how major strategy-notebook surfaces relate before deciding what to open, inspect, or revise.

**Inputs**  

- `docs/skill-work/work-strategy/strategy-notebook/`
- generated fixture data and graph-like structure

**Generated artifact**  

- static HTML visualizer
- generated fixture JSON

**Inspection path**  

- serve locally
- inspect in browser
- optionally use Workbench for screenshot and bounded inspection notes

**Receipt**  

- optional Workbench receipt for UI/runtime behavior
- strategy trace only if a command also writes notebook files

**Operator decision**  

- inspect further
- revise
- keep as a derived orientation surface

**Why it is not Record truth**  
It helps the operator understand notebook structure and paths. It does not compose strategy judgment, validate geopolitical claims, or update the Record.

See [../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md](../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md).

## B. Gate-review cockpit mockup

**Intent**  
Preview a more inspectable review surface before deciding whether it should become a scripted dashboard or a real work-dev tool.

**Inputs**  

- `users/grace-mar/recursion-gate.md`
- existing review dashboard concepts
- optional candidate summary rows or derived JSON prepared in WORK

**Generated artifact**  

- HTML or React cockpit mockup
- comparison view of pending, approved, or processed states

**Inspection path**  

- view in browser or local preview
- use Workbench if behavior or layout matters

**Receipt**  

- interface-artifact metadata
- optional Workbench receipt

**Operator decision**  

- discard
- revise
- convert to scripted dashboard
- implement as a work-dev tool

**Why it is not Record truth**  
It summarizes and previews review flow. It does not replace `recursion-gate.md`, does not approve candidates, and does not gain merge authority by looking more polished.

## C. Self-library map

**Intent**  
Give the operator a navigable map of library clusters, reading lanes, or thematic seams before deciding whether to refine scripts or browse the underlying sources directly.

**Inputs**  

- `users/grace-mar/self-library.md`
- existing library index or derived library outputs

**Generated artifact**  

- SVG map
- HTML visualizer
- Markdown dashboard variant

**Inspection path**  

- inspect the generated view directly
- use Workbench when interaction or rendering behavior matters

**Receipt**  

- interface-artifact metadata
- optional Workbench receipt

**Operator decision**  

- keep as derived artifact
- revise the map
- convert to scripted dashboard

**Why it is not Record truth**  
The map is a navigational and comparative aid. Canonical library truth still lives in the underlying library files and governed update paths, not in the generated map.

## Pattern summary

Across all three examples:

- the artifact helps the operator inspect or navigate
- the artifact is WORK-only and derived
- the artifact may be inspected through Workbench
- the artifact may suggest a real next move
- the artifact cannot silently become Record truth, gate authority, or external proof
