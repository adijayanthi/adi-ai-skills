# threat-model-guardrails

An agent skill that turns a specification into a threat model, a guardrail
catalogue and testable security requirements — and makes those requirements
bind whoever writes the tests next.

Give it any Markdown spec: a product specification, a PRD, a feature or
enhancement document. It inventories the attack surface, runs STRIDE per
element, cross-checks OWASP Top 10:2025, the CWE Top 25 (2025), the OWASP API
Top 10 and — for AI or agent features — the OWASP LLM and Agentic Top 10s,
then asks the team batched questions where the spec is silent. Answers flow
into:

| Output | Purpose |
|---|---|
| `THREAT-MODEL.md` | Attack surface, threats with "why it is real here", what is explicitly not defended, assumptions |
| `GUARDRAILS.md` | Each control with its strength (structural, enforced, advisory), enforcement point and failure mode |
| `SECURITY-REQUIREMENTS.md` + `security-requirements.json` | Testable "shall" statements traced to guardrails and threats; the JSON is what tools and agents read |
| A block for `AGENTS.md` / `CLAUDE.md` | Makes test-writing agents cover the requirements for the files they touch |
| `security_coverage.py` | CI check that every gating requirement has a test carrying its id |

It runs in **full** mode for a new product and **delta** mode for a feature
against an existing model, continuing the numbering.

## Layout

```
threat-model-guardrails/
├── SKILL.md                         the workflow and the yardstick
├── references/
│   ├── stride-question-bank.md      STRIDE-per-element matrix and questions
│   ├── catalogues.md                OWASP / CWE / LLM / Agentic, with spec triggers
│   ├── guardrail-patterns.md        29 guardrail patterns with their tests
│   └── test-traceability.md         verification methods, test rules, red-team corpus
├── assets/                          output templates, register example, agent snippet
└── scripts/check_coverage.py        stdlib-only coverage check
```

## Installing

The skill follows the [Agent Skills](https://agentskills.io/specification)
format: a directory with `SKILL.md` carrying `name` and `description`
frontmatter, plus optional `references/`, `assets/` and `scripts/`. Copy or
symlink the directory — the directory name must stay `threat-model-guardrails`.

| Harness | Project-level | User-level |
|---|---|---|
| Claude Code | `.claude/skills/threat-model-guardrails/` | `~/.claude/skills/threat-model-guardrails/` |
| OpenAI Codex | `.agents/skills/threat-model-guardrails/` | `~/.agents/skills/threat-model-guardrails/` |
| Other Agent Skills harnesses | Per the harness's documented skills path | |

Portability notes:

- Only `name` and `description` are relied on. `metadata` is part of the
  open specification; harnesses that do not read it ignore it.
- The body uses no harness-specific tool names. Where a harness has a
  structured question tool, the skill says to use it; otherwise it asks in
  plain text.
- For a harness without skill support, paste `SKILL.md` into its system or
  project instructions and keep the other files beside the repository; the
  links are relative.
- Codex reads an optional `agents/openai.yaml` for display metadata and
  invocation policy. None is shipped; add one if you publish to that surface.

Validate the frontmatter with the reference validator:

```bash
skills-ref validate ./threat-model-guardrails
```

## Using it

> Threat-model `docs/SPEC.md`.

> Here's the spec for the new bulk-import feature — what does it add to our
> threat model?

The skill reads, asks one batch of questions with a recommended answer for
each, waits, and then writes the artifacts. Run the coverage check once tests
exist:

```bash
python3 scripts/security_coverage.py docs/security/security-requirements.json tests
```

Use `--report-only` on a fresh model, when every requirement is expected to be
uncovered.

## Provenance

Distilled from the guardrail specification of an agentic SaaS product, where
the threat assessment was woven into the specification rather than written as
a separate STRIDE exercise. The enforcement-strength model, the assignment
rule, irreversibility tiering, provenance and argument-sink checks, bounded
lifetime for untrusted content, policy-as-data with fail-closed loading, and
the "every rule has a rejection test" coverage rule all come from that work;
STRIDE and the public catalogues are the scaffolding added to make it
repeatable on any specification.

## Licence

[Apache License 2.0](LICENSE.txt). Use it, change it and share it, including commercially. Keep the licence and copyright notice, and mark files you change.
