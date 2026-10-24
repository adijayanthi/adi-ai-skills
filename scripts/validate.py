#!/usr/bin/env python3
"""Check the repository's skills against its layout and publishing rules.

  skills/<domain>/<skill>/SKILL.md     a published skill
  skills/in-progress/<skill>/SKILL.md  beta: public, not in a plugin
  skills/deprecated/<skill>/SKILL.md   retired: kept for reference

Every skill must have valid Agent Skills frontmatter, a name matching its
folder and unique across the repository (harnesses install skills flat, by
name), a licence, and a LICENSE.txt. A published skill must also declare its
domain in metadata, be listed in its domain's README, the root README, and the
domain's plugin in .claude-plugin/marketplace.json. Every listed plugin path
must exist.

Standard library only. Exit status 1 on any problem.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
LIFECYCLE = {"in-progress", "deprecated"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    block = text[4:].split("\n---", 1)[0]
    fields, section = {}, None
    for line in block.splitlines():
        top = re.match(r"^([a-zA-Z-]+):\s*(.*)$", line)
        nested = re.match(r"^\s+([a-zA-Z-]+):\s*(.*)$", line)
        if top:
            key, value = top.groups()
            section = key if value == "" else None
            fields[key] = value.strip().strip('"') if value else {}
        elif nested and section:
            fields[section][nested.group(1)] = nested.group(2).strip().strip('"')
    return fields


def main() -> int:
    problems: list[str] = []
    seen: dict[str, Path] = {}
    published: dict[str, list[str]] = {}

    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    plugins = {p["name"]: p for p in marketplace["plugins"]}
    root_readme = (ROOT / "README.md").read_text()

    for skill_md in sorted(SKILLS.glob("*/*/SKILL.md")):
        folder = skill_md.parent
        bucket = folder.parent.name
        rel = folder.relative_to(ROOT).as_posix()
        fm = frontmatter(skill_md.read_text())
        name = fm.get("name", "")
        description = fm.get("description", "")

        if not NAME.fullmatch(name) or len(name) > 64:
            problems.append(f"{rel}: name '{name}' is not 1-64 lowercase letters, digits and single hyphens")
        if name != folder.name:
            problems.append(f"{rel}: name '{name}' does not match its folder")
        if not 0 < len(description) <= 1024:
            problems.append(f"{rel}: description must be 1-1024 characters, is {len(description)}")
        if not fm.get("license"):
            problems.append(f"{rel}: no license field")
        if not (folder / "LICENSE.txt").exists():
            problems.append(f"{rel}: no LICENSE.txt")
        if name in seen:
            problems.append(f"{rel}: name '{name}' already used by {seen[name].relative_to(ROOT)}")
        seen[name] = folder

        if bucket in LIFECYCLE:
            continue

        metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        if metadata.get("domain") != bucket:
            problems.append(f"{rel}: metadata.domain must be '{bucket}'")
        domain_readme = folder.parent / "README.md"
        if not domain_readme.exists() or f"./{name}/" not in domain_readme.read_text():
            problems.append(f"{rel}: not listed in skills/{bucket}/README.md")
        if f"skills/{bucket}/{name}" not in root_readme:
            problems.append(f"{rel}: not listed in the root README")
        published.setdefault(bucket, []).append(f"./{rel}")

    for domain, paths in published.items():
        plugin = plugins.get(domain)
        if not plugin:
            problems.append(f"marketplace: no plugin named '{domain}' for skills/{domain}/")
            continue
        for path in paths:
            if path not in plugin.get("skills", []):
                problems.append(f"marketplace: plugin '{domain}' does not list {path}")

    for plugin in plugins.values():
        for path in plugin.get("skills", []):
            if not (ROOT / path / "SKILL.md").exists():
                problems.append(f"marketplace: plugin '{plugin['name']}' lists {path}, which has no SKILL.md")
            elif Path(path).parts[1] in LIFECYCLE:
                problems.append(f"marketplace: plugin '{plugin['name']}' lists a {Path(path).parts[1]} skill, {path}")

    if problems:
        print("\n".join(problems))
        return 1
    count = sum(len(p) for p in published.values())
    print(f"ok: {len(seen)} skills, {count} published across {len(published)} domains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
