#!/usr/bin/env python3
"""Security-requirement coverage check.

Reads a threat-model-guardrails register (security-requirements.json) and the
project's test files, and reports:

  - requirements whose verification gates CI but no test carries their id
  - guardrails with no requirement, and E guardrails with no requirement
    whose test would fail if the check stopped running (enforcement-rejection,
    invariant, policy-load or red-team)
  - requirements with neither components nor elements (warning only)
  - ids used in tests that the register does not define (stale tags)
  - references in the register to threats or guardrails that do not exist

Requirements marked "known_gap" are reported, never failed.

Standard library only, so it runs in CI without the skill installed.
Copy it into the project, e.g. scripts/security_coverage.py.

Usage:
  python3 security_coverage.py REGISTER TEST_DIR [TEST_DIR ...]
          [--ext .ts,.js,.py,...] [--report-only] [--json]

Exit status: 0 when nothing in the gating set is uncovered (or --report-only),
1 on gaps, 2 on a register that cannot be read.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

GATING = {"surface-absence", "enforcement-rejection", "invariant", "policy-load", "red-team"}
NON_GATING = {"eval", "review", "monitor"}
# What proves an E guardrail is still running. surface-absence proves an S one.
PROVES_ENFORCEMENT = {"enforcement-rejection", "invariant", "policy-load", "red-team"}
DEFAULT_EXTS = ".ts,.tsx,.js,.jsx,.mjs,.cjs,.py,.go,.rs,.java,.kt,.cs,.rb,.php,.swift,.scala,.ex,.exs"
SR_ID = re.compile(r"\bSR-\d{3,}\b")
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".venv", "__pycache__"}


def load_register(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            register = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read register {path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(register.get("requirements"), list):
        print(f"register {path} has no 'requirements' list", file=sys.stderr)
        sys.exit(2)
    return register


def scan_tests(dirs: list[str], exts: set[str]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for root in dirs:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if os.path.splitext(name)[1] not in exts:
                    continue
                path = os.path.join(dirpath, name)
                try:
                    with open(path, encoding="utf-8", errors="replace") as f:
                        text = f.read()
                except OSError:
                    continue
                for sr in set(SR_ID.findall(text)):
                    found.setdefault(sr, set()).add(os.path.relpath(path))
    return found


def check(register: dict, found: dict[str, set[str]]) -> dict:
    reqs = register["requirements"]
    guardrails = register.get("guardrails", [])
    threats = register.get("threats", [])
    g_ids = {g["id"] for g in guardrails}
    t_ids = {t["id"] for t in threats}
    sr_ids = [r["id"] for r in reqs]

    result = {
        "covered": {},
        "uncovered": [],
        "known_gaps": [],
        "non_gating": [],
        "stale_tags": {},
        "guardrails_without_requirements": [],
        "enforced_without_gating_test": [],
        "unlocatable": [],
        "register_errors": [],
    }

    for dup in sorted({i for i in sr_ids if sr_ids.count(i) > 1}):
        result["register_errors"].append(f"duplicate requirement id {dup}")

    for r in reqs:
        rid, method = r["id"], r.get("verification")
        if method not in GATING | NON_GATING:
            result["register_errors"].append(f"{rid}: unknown verification '{method}'")
        for g in r.get("guardrails", []):
            if guardrails and g not in g_ids:
                result["register_errors"].append(f"{rid}: references undefined guardrail {g}")
        for t in r.get("threats", []):
            if threats and t not in t_ids:
                result["register_errors"].append(f"{rid}: references undefined threat {t}")

        if not r.get("components") and not r.get("elements"):
            result["unlocatable"].append(rid)

        if r.get("status") == "known_gap":
            result["known_gaps"].append({"id": rid, "issue": r.get("issue")})
        elif method in NON_GATING:
            result["non_gating"].append({"id": rid, "verification": method})
        elif rid in found:
            result["covered"][rid] = sorted(found[rid])
        else:
            result["uncovered"].append(rid)

    for sr in sorted(set(found) - set(sr_ids)):
        result["stale_tags"][sr] = sorted(found[sr])

    for g in guardrails:
        mine = [r for r in reqs if g["id"] in r.get("guardrails", [])]
        if not mine:
            result["guardrails_without_requirements"].append(g["id"])
        elif "E" in g.get("strength", []) and not any(
            r.get("verification") in PROVES_ENFORCEMENT for r in mine
        ):
            result["enforced_without_gating_test"].append(g["id"])

    return result


def failed(result: dict) -> bool:
    return any(
        result[k]
        for k in (
            "uncovered",
            "stale_tags",
            "guardrails_without_requirements",
            "enforced_without_gating_test",
            "register_errors",
        )
    )


def print_report(result: dict) -> None:
    def section(title: str, items) -> None:
        if items:
            print(f"\n{title}")
            for item in items:
                print(f"  {item}")

    print(f"Covered: {len(result['covered'])}   Uncovered: {len(result['uncovered'])}   "
          f"Known gaps: {len(result['known_gaps'])}   Non-gating: {len(result['non_gating'])}")
    section("Uncovered requirements (no test carries the id):", result["uncovered"])
    section("Stale tags (used in tests, not in the register):",
            [f"{k}  {', '.join(v)}" for k, v in result["stale_tags"].items()])
    section("Guardrails with no requirement:", result["guardrails_without_requirements"])
    section("Enforced guardrails with no requirement that proves the check runs:",
            result["enforced_without_gating_test"])
    section("Requirements with neither components nor elements (warning):",
            result["unlocatable"])
    section("Register errors:", result["register_errors"])
    section("Known gaps (reported, not failed):",
            [f"{g['id']}  {g['issue'] or 'no issue recorded'}" for g in result["known_gaps"]])
    section("Verified outside CI (eval / review / monitor):",
            [f"{n['id']}  {n['verification']}" for n in result["non_gating"]])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("register")
    parser.add_argument("test_dirs", nargs="+")
    parser.add_argument("--ext", default=DEFAULT_EXTS)
    parser.add_argument("--report-only", action="store_true",
                        help="always exit 0; use on a fresh model before tests exist")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args()

    register = load_register(args.register)
    exts = {e if e.startswith(".") else "." + e for e in args.ext.split(",") if e}
    result = check(register, scan_tests(args.test_dirs, exts))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)

    sys.exit(0 if args.report_only or not failed(result) else 1)


if __name__ == "__main__":
    main()
