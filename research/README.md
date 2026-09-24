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
