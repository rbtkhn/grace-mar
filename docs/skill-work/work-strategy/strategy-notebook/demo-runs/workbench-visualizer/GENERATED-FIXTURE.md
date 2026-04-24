# Generated fixture (strategy notebook visualizer)

`strategy-notebook-visualizer.fixture.json` is a **derived** artifact. It is **not** SELF, EVIDENCE, or a gate merge. The HTML map **does not** assert strategic truth; it only reflects **tree structure and paths** the generator found.

- **`knot-index.yaml`** and **strategy-notebook** docs remain the source of truth for knots and intent.
- Built-in **wrapper fields** in the JSON (`recordAuthority: none`, `gateEffect: none`, `truthScope`, `generatedAt`, etc.) label scope; the static page may ignore them and only use `nodes` and `edges`.

## Regenerate

From the repository root:

```bash
python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py
```

## Drift check (CI / before commit)

```bash
python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py --check
```

Exit `0` if the on-disk file matches a fresh in-memory build (normalized JSON), `1` if missing, parse error, or differ. **`generatedAt` is not treated as structural drift:** `--check` compares the built graph to the file while reusing the file’s `generatedAt` so two runs in a row are not a false positive.

## PyYAML

If PyYAML is missing, the generator **warns** and skips `knot-index` / `knot-connections`–driven nodes and edges; baseline nodes and directory discovery still run.

## ID conventions (selection)

- **Baseline** nodes use fixed `id` values (e.g. `knot-index`, `graph-schema`, `strategy-state-iran`). Dynamic segments use stable prefixes: `expert-…`, `mind-…`, `watch-…`, `strategy-state-iran-…` (or `ssi-…` where used), and **`knot-<slug>`** from the repo-relative path (kebab from path segments, see the script).
