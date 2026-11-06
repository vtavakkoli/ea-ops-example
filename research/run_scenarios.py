from __future__ import annotations

import argparse
from collections import deque
import csv
import difflib
from pathlib import Path
import shutil
import tempfile

import yaml

from eaops.core import impact, load_repository, validate
from eaops.compare import change_impact


BASE_ITEMS = ("eaops.yaml", "model", "relationships", "views", "rules")


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save(path: Path, data) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _copy_base(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in BASE_ITEMS:
        src = source / name
        dst = target / name
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.exists():
            shutil.copy2(src, dst)


def _find(items: list[dict], oid: str) -> dict:
    try:
        return next(item for item in items if item.get("id") == oid)
    except StopIteration as exc:
        raise KeyError(f"ID not found: {oid}") from exc


def _apply(root: Path, operation: dict, before: dict[Path, str]) -> None:
    path = root / operation["file"]
    if path not in before:
        before[path] = path.read_text(encoding="utf-8") if path.exists() else ""
    data = _load(path) if path.exists() else []
    kind = operation["op"]

    if kind == "set_property":
        item = _find(data, operation["id"])
        item.setdefault("properties", {})[operation["property"]] = operation["value"]
    elif kind == "remove_property":
        item = _find(data, operation["id"])
        item.setdefault("properties", {}).pop(operation["property"], None)
    elif kind == "set_field":
        _find(data, operation["id"])[operation["field"]] = operation["value"]
    elif kind == "remove_item":
        data = [item for item in data if item.get("id") != operation["id"]]
    elif kind == "add_item":
        if any(item.get("id") == operation["item"].get("id") for item in data):
            raise ValueError(f"Duplicate add_item ID: {operation['item'].get('id')}")
        data.append(operation["item"])
    else:
        raise ValueError(f"Unsupported operation: {kind}")
    _save(path, data)


def _documents(folder: Path) -> list[dict]:
    result = []
    if not folder.exists():
        return result
    for path in sorted(list(folder.rglob("*.yaml")) + list(folder.rglob("*.yml"))):
        data = _load(path)
        if isinstance(data, list):
            result.extend(item for item in data if isinstance(item, dict))
        elif isinstance(data, dict):
            result.append(data)
    return result


def independent_impact(root: Path, changed_ids: set[str]) -> set[str]:
    adjacency: dict[str, set[str]] = {}
    for rel in _documents(root / "relationships"):
        source, target = rel.get("source"), rel.get("target")
        if not source or not target:
            continue
        adjacency.setdefault(source, set()).add(target)
        adjacency.setdefault(target, set()).add(source)

    impacted = set(changed_ids)
    queue = deque(changed_ids)
    while queue:
        current = queue.popleft()
        for neighbor in adjacency.get(current, set()):
            if neighbor not in impacted:
                impacted.add(neighbor)
                queue.append(neighbor)
    return impacted


def independent_dependency(root: Path, seeds: set[str], max_depth: int | None = None) -> set[str]:
    """Fixed-point scan over raw YAML, independent of the product's adjacency BFS.

    The propagation policy is shared by specification, not by imported code.
    Agreement checks that policy's implementation, not real business impact.
    """
    found = set(seeds)
    rels = _documents(root / "relationships")
    waves = 0
    while True:
        if max_depth is not None and waves >= max_depth:
            return found
        previous = set(found)
        for rel in rels:
            s, t, kind = rel.get("source"), rel.get("target"), rel.get("type")
            if not s or not t:
                continue
            if kind in ("Serving", "Realization", "Assignment", "Triggering", "Flow") and s in previous:
                found.add(t)
            if kind in ("Composition", "Aggregation") and t in previous:
                found.add(s)
            if kind == "Access":
                properties = rel.get("properties") or {}
                access = str(properties.get("accessType") or properties.get("access") or "access").lower()
                if access in ("readwrite", "read/write"):
                    access = "read-write"
                if access in ("read", "read-write", "access") and t in previous:
                    found.add(s)
                if access in ("write", "read-write", "access") and s in previous:
                    found.add(t)
        if found == previous:
            return found
        waves += 1


def independent_review(base: Path, target: Path, operations: list[dict]) -> set[str]:
    local, seeds = set(), set()
    for operation in operations:
        if operation["file"].startswith("relationships/"):
            rid = operation.get("id", (operation.get("item") or {}).get("id"))
            for root in (base, target):
                for rel in _documents(root / "relationships"):
                    if rel.get("id") == rid:
                        seeds.update(x for x in (rel.get("source"), rel.get("target")) if x)
        elif operation["file"].startswith("model/"):
            oid = operation.get("id", (operation.get("item") or {}).get("id"))
            if operation["op"] == "set_property" and operation.get("property") == "owner":
                local.add(oid)
            else:
                seeds.add(oid)
    return independent_dependency(base, seeds) | independent_dependency(target, seeds) | local


def _patch(before: dict[Path, str], root: Path) -> str:
    chunks = []
    for path in sorted(before, key=lambda p: str(p)):
        old = before[path].splitlines(keepends=True)
        new = path.read_text(encoding="utf-8").splitlines(keepends=True) if path.exists() else []
        rel = path.relative_to(root).as_posix()
        chunks.extend(
            difflib.unified_diff(
                old,
                new,
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
            )
        )
    return "".join(chunks)


def run_scenario(base: Path, scenario_path: Path, patch_dir: Path) -> dict:
    spec = _load(scenario_path)
    with tempfile.TemporaryDirectory(prefix="eaops-scenario-") as tmp:
        root = Path(tmp)
        _copy_base(base, root)
        before: dict[Path, str] = {}
        for operation in spec.get("operations", []):
            _apply(root, operation, before)

        repo = load_repository(root)
        actual_issues = validate(repo)
        actual_errors = sorted(
            (issue.code, issue.object_id or "")
            for issue in actual_issues
            if issue.severity == "error"
        )
        expected_errors = sorted(
            (item["code"], item.get("object_id", ""))
            for item in spec.get("expected_errors", [])
        )
        validation_exact = actual_errors == expected_errors

        changed = set(spec.get("changed_ids", []))
        actual_impact = set(impact(repo, changed)["impacted"])
        oracle_impact = independent_impact(root, changed)
        impact_exact = actual_impact == oracle_impact
        review = change_impact(load_repository(base), repo)
        expected_review = independent_review(base, root, spec.get("operations", []))
        review_exact = set(review["impacted"]) == expected_review
        typed_current = impact(repo, changed, profile="dependency")
        bounded = impact(repo, changed, profile="dependency", max_depth=2)
        typed_exact = set(typed_current["impacted"]) == independent_dependency(root, changed)
        bounded_exact = set(bounded["impacted"]) == independent_dependency(root, changed, max_depth=2)

        patch_dir.mkdir(parents=True, exist_ok=True)
        (patch_dir / f"{spec['id']}.patch").write_text(_patch(before, root), encoding="utf-8")

        return {
            "scenario": spec["id"],
            "description": spec["description"],
            "changed_ids": ";".join(sorted(changed)),
            "expected_errors": ";".join(f"{c}:{o}" for c, o in expected_errors),
            "actual_errors": ";".join(f"{c}:{o}" for c, o in actual_errors),
            "validation_exact": str(validation_exact).lower(),
            "impact_size": len(actual_impact),
            "impact_exact": str(impact_exact).lower(),
            "typed_current_size": len(typed_current["impacted"]),
            "typed_two_hop_size": len(bounded["impacted"]),
            "review_scope_size": len(review["impacted"]),
            "review_scope_ids": ";".join(review["impacted"]),
            "review_exact": str(review_exact).lower(),
            "typed_exact": str(typed_exact and bounded_exact).lower(),
            "overall_pass": str(validation_exact and impact_exact and review_exact and typed_exact and bounded_exact).lower(),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run controlled Metroville EA-Ops research scenarios.")
    parser.add_argument("--base", default=".")
    parser.add_argument("--scenarios", default="research/scenarios")
    parser.add_argument("--output", default="results/metroville-scenarios.csv")
    parser.add_argument("--patch-dir", default="results/patches")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    scenario_dir = Path(args.scenarios).resolve()
    patch_dir = Path(args.patch_dir).resolve()
    rows = [
        run_scenario(base, scenario_path, patch_dir)
        for scenario_path in sorted(scenario_dir.glob("CR*.yaml"))
    ]
    if not rows:
        raise SystemExit("No CR*.yaml scenarios found")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    failed = [row["scenario"] for row in rows if row["overall_pass"] != "true"]
    print(output)
    if failed:
        raise SystemExit("Scenario failures: " + ", ".join(failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
