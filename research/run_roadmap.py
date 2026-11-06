"""Cross-layer baseline / transition / target inventory-gap demonstration.

Three fully materialized snapshots share stable IDs. Assertions specify concrete
inventory changes; no human acceptance or TOGAF governance outcome is inferred.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from eaops.core import load_repository, validate
from eaops.compare import compare_repositories, change_impact
from run_scenarios import _copy_base


def add(root, relative, records):
    path = root / relative
    previous = yaml.safe_load(path.read_text()) if path.exists() else []
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(previous + records, sort_keys=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=".")
    parser.add_argument("--output", default="results/roadmap")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists():
        parser.error("use a new --output directory to preserve previous evidence")
    states = {}
    for state in ("baseline", "transition", "target"):
        root = output / state
        _copy_base(Path(args.base).resolve(), root)
        extra = [
            {"id": "plateau.current", "type": "Plateau", "name": "Reviewed baseline",
             "properties": {"owner": "Enterprise Architecture", "lifecycle": "baseline"}},
            {"id": "plateau.transition", "type": "Plateau", "name": "Parallel platform transition",
             "properties": {"owner": "Enterprise Architecture", "lifecycle": "transition"}},
        ]
        add(root, "model/roadmap.yaml", extra)
        add(root, "relationships/roadmap.yaml", [
            {"id": "rel-gap-current", "type": "Association", "source": "gap.manual-channels", "target": "plateau.current"},
            {"id": "rel-gap-target", "type": "Association", "source": "gap.manual-channels", "target": "plateau.digital-permit-live"},
            {"id": "rel-work-target", "type": "Realization", "source": "work.permit-modernization", "target": "deliverable.target-platform"},
        ])
        if state != "baseline":
            add(root, "model/roadmap.yaml", [{"id": "tech.target-runtime", "type": "Node", "name": "Target platform runtime",
                 "description": "Parallel replacement platform for the reviewed permit service.",
                 "properties": {"owner": "Digital Platforms", "lifecycle": "planned" if state == "transition" else "active"}}])
            add(root, "relationships/roadmap.yaml", [{"id": "rel-target-platform", "type": "Assignment",
                 "source": "tech.target-runtime", "target": "tech.container-platform"}])
        business = yaml.safe_load((root / "model/business.yaml").read_text())
        for obj in business:
            if obj["id"] == "process.assess-case":
                obj["properties"]["owner"] = "Permit Operations" if state != "baseline" else obj["properties"]["owner"]
        (root / "model/business.yaml").write_text(yaml.safe_dump(business, sort_keys=False))
        if state == "target":
            technology = yaml.safe_load((root / "model/technology.yaml").read_text())
            for obj in technology:
                if obj["id"] == "tech.openshift":
                    obj["properties"]["lifecycle"] = "eliminate"
            (root / "model/technology.yaml").write_text(yaml.safe_dump(technology, sort_keys=False))
            implementation = yaml.safe_load((root / "model/implementation.yaml").read_text())
            for obj in implementation:
                if obj["id"] == "gap.manual-channels":
                    obj["properties"]["lifecycle"] = "closed"
            (root / "model/implementation.yaml").write_text(yaml.safe_dump(implementation, sort_keys=False))
            relationships = yaml.safe_load((root / "relationships/relationships.yaml").read_text())
            relationships = [rel for rel in relationships if rel["id"] != "rel-openshift-runtime"]
            (root / "relationships/relationships.yaml").write_text(yaml.safe_dump(relationships, sort_keys=False))
        states[state] = load_repository(root)
        errors = [issue.as_dict() for issue in validate(states[state]) if issue.severity == "error"]
        if errors:
            raise AssertionError({state: errors})
    results = {}
    for source, target in (("baseline", "transition"), ("transition", "target"), ("baseline", "target")):
        delta = compare_repositories(states[source], states[target])
        if source == "baseline":
            assert delta["objects"]["added"] == ["tech.target-runtime"]
            assert delta["relationships"]["added"] == ["rel-target-platform"]
        assert not delta["objects"]["removed"]
        if target == "target":
            assert delta["relationships"]["removed"] == ["rel-openshift-runtime"]
        results[f"{source}-to-{target}"] = {"gap": delta, "review": change_impact(states[source], states[target])}
    (output / "gap-analysis.json").write_text(json.dumps(results, indent=2) + "\n")
    print(output / "gap-analysis.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
