# Metroville controlled research scenarios

These scenarios evaluate EA-Ops on controlled architecture changes against the fictional Metroville Digital Permit Service.

Each `CR*.yaml` manifest declares:

- the changed architecture IDs;
- one or more deterministic model mutations;
- the exact expected validation errors, if any.

The runner applies each scenario to a fresh copy of the base architecture. It then compares EA-Ops validation output with the manifest and compares EA-Ops impact analysis with an **independent breadth-first graph traversal implemented in this repository**. The independent oracle does not call `eaops.core.impact`.

For auditability, each scenario also emits a unified `.patch` artifact showing the exact YAML change produced by the manifest.

Run locally after installing EA-Ops:

```bash
python research/run_scenarios.py \
  --base . \
  --scenarios research/scenarios \
  --output results/metroville-scenarios.csv \
  --patch-dir results/patches
```

The canonical CI execution is `.github/workflows/scenario-evaluation.yml`.

## Revision: typed review scope and architecture states

`run_scenarios.py` retains the ten original patches and adds typed, two-hop and change-aware before/after scopes, checked with an independent fixed-point oracle over raw YAML. Seeds and dangling/deleted IDs remain visible. Smaller sets do not establish business-impact accuracy.

`python research/run_roadmap.py --output results/roadmap` materializes baseline, transition and target repositories with Plateau/Gap concepts and a replacement platform. It validates all three and asserts concrete inventory additions/removals. Use a new output directory to preserve earlier evidence. `eaops diff` reports the inventory gap, and `eaops impact TARGET --baseline BASELINE` reports structural review candidates. The demonstration is fictional and has no stakeholder acceptance results.

Preserved outputs are under `research/revision/`. The workflow pins the compatible EA-Ops revision; update that pin deliberately when adopting subsequent changes.

The associated preprint DOI is [10.48550/arXiv.2609.30593](https://doi.org/10.48550/arXiv.2609.30593). Evaluation by the City of Vienna (Wien Digital, MA 01) is planned future work; the current evidence remains the fictional Metroville case and implementation checks.
