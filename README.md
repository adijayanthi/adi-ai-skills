# adi-ai-skills

Agent skills in the open [Agent Skills](https://agentskills.io/specification)
format. They work in Claude Code, OpenAI Codex, and any other harness that
reads `SKILL.md`.

## Skills

| Skill | What it does |
|---|---|
| [threat-model-guardrails](skills/threat-model-guardrails/) | Turns a product or feature specification into an attack-surface inventory, a STRIDE threat model, a guardrail catalogue and testable security requirements. Cross-checks OWASP Top 10, CWE Top 25 and the OWASP LLM and Agentic Top 10s, asks the team what the spec leaves out, and makes the requirements bind whoever writes the tests |

## Installing a skill

Clone the repository, then copy or symlink the skill's folder into your
harness's skills directory. Keep the folder name unchanged; the spec requires
it to match the skill's `name`.

```bash
git clone https://github.com/adijayanthi/adi-ai-skills.git
```

| Harness | Project-level | User-level |
|---|---|---|
| Claude Code | `.claude/skills/<skill>/` | `~/.claude/skills/<skill>/` |
| OpenAI Codex | `.agents/skills/<skill>/` | `~/.agents/skills/<skill>/` |
| Other harnesses | The harness's documented skills path | |

For example, to make it available in every Claude Code project:

```bash
cp -r adi-ai-skills/skills/threat-model-guardrails ~/.claude/skills/
```

Each skill's own README covers how to use it.

## Licence

[Apache License 2.0](LICENSE). Each skill folder carries its own copy, so a
skill copied on its own keeps its licence.
