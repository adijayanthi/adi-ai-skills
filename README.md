# adi-ai-skills

Application security and cybersecurity skills for AI coding agents, in the
open [Agent Skills](https://agentskills.io/specification) format. They work in
Claude Code, OpenAI Codex, and any other harness that reads `SKILL.md`.

Skills are grouped by security domain, and each domain installs as one
plugin.

## Skills

| Domain | Skill | What it does |
|---|---|---|
| [Application security](skills/application-security/) | [threat-model-guardrails](skills/application-security/threat-model-guardrails/) | Turns a product or feature specification into an attack-surface inventory, a STRIDE threat model, a guardrail catalogue and testable security requirements. Cross-checks OWASP Top 10, CWE Top 25 and the OWASP LLM and Agentic Top 10s, asks the team what the spec leaves out, and makes the requirements bind whoever writes the tests |

More domains (AI security, cloud security, identity and access, security
operations, offensive security, governance, risk and compliance) are added as
their first skill is published. See [AGENTS.md](AGENTS.md) for the layout.

## Installing

### Claude Code: as a plugin (updates itself)

Install a whole domain:

```text
/plugin install application-security --marketplace adijayanthi/adi-ai-skills
```

Or add the marketplace once, then install domains from it:

```text
/plugin marketplace add adijayanthi/adi-ai-skills
/plugin install application-security@adi-ai-skills
```

### Any harness: copy a single skill

Clone the repository, then copy or symlink the skill's folder into your
harness's skills directory. Keep the folder name unchanged; the Agent Skills
spec requires it to match the skill's `name`.

```bash
git clone https://github.com/adijayanthi/adi-ai-skills.git
```

| Harness | Project-level | User-level |
|---|---|---|
| Claude Code | `.claude/skills/<skill>/` | `~/.claude/skills/<skill>/` |
| OpenAI Codex | `.agents/skills/<skill>/` | `~/.agents/skills/<skill>/` |
| Other harnesses | The harness's documented skills path | |

For example, for every Codex project:

```bash
cp -r adi-ai-skills/skills/application-security/threat-model-guardrails ~/.agents/skills/
```

Each skill's own README covers how to use it.

## Licence

[Apache License 2.0](LICENSE). Each skill folder carries its own copy, so a
skill copied on its own keeps its licence.
