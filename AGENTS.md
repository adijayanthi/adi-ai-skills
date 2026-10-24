# Working in this repository

A collection of agent skills in the open [Agent Skills](https://agentskills.io/specification)
format, organised by security domain. Read this before adding or changing a
skill.

## Layout

```
skills/
├── <domain>/            a published security domain, e.g. application-security
│   ├── README.md        lists every skill in the domain
│   └── <skill>/         one skill; folder name = the skill's `name`
│       ├── SKILL.md     required
│       ├── LICENSE.txt  required, a copy of the root LICENSE
│       ├── README.md    how to install and use it
│       ├── CHANGELOG.md
│       ├── agents/openai.yaml   optional Codex display metadata
│       ├── references/  loaded on demand
│       ├── assets/      templates and examples
│       └── scripts/     executable helpers, standard library only where possible
├── in-progress/<skill>/ beta: public, excluded from plugins
└── deprecated/<skill>/  retired: kept for reference, excluded from plugins
```

Two levels only: domain, then skill. Harnesses install skills flat, by name,
so deeper nesting buys nothing and makes paths longer. A cross-cutting
concern belongs in a skill's description, not in a sub-folder.

## Domains

Create a domain folder when its first skill lands, not before. Use these
names, so the set stays consistent:

| Folder | Covers |
|---|---|
| `application-security` | Secure design, threat modelling, security requirements, secure code review, dependency and supply-chain risk in the codebase |
| `ai-security` | Risks specific to models and agents: prompt-injection testing, model red-teaming, agent permission design |
| `cloud-security` | Cloud configuration, infrastructure-as-code review, cloud identity and network posture |
| `identity-and-access` | Authentication, authorisation models, IAM policy review |
| `security-operations` | Detection engineering, incident response, threat hunting, log analysis |
| `offensive-security` | Authorised penetration testing and red-team methodology |
| `governance-risk-compliance` | Control mapping, risk registers, policy, audit evidence |

A skill that spans domains goes where its primary output is used.
`threat-model-guardrails` sits in `application-security`, although it has AI
checks, because its output is a product's security requirements.

## Adding a skill

1. Start it in `skills/in-progress/<name>/` if it is not ready for general use.
2. `name` is lowercase letters, digits and single hyphens, at most 64
   characters, matches the folder, and is unique across the whole
   repository.
3. Frontmatter: `name`, `description` (what it does *and* when to use it, at
   most 1024 characters), `license: Apache-2.0`, and `metadata` with
   `version` and `domain`.
4. Keep `SKILL.md` under 500 lines and about 5,000 tokens. Move detail into
   `references/`, linked one level deep.
5. Use no harness-specific tool names in the body. Say "if the harness offers
   a structured question tool…", not a product's tool name.
6. To publish, move it into its domain folder, then add it to:
   - the domain README;
   - the root README's skills table;
   - the domain's plugin in `.claude-plugin/marketplace.json`, creating the
     plugin (named after the domain) if it is the domain's first skill.
7. Bump the skill's `metadata.version` and `CHANGELOG.md` for every published
   change, and the marketplace `metadata.version` for every release.
8. Run both checks before committing:

   ```bash
   python3 scripts/validate.py
   claude plugin validate .
   ```

## Content rules

- Skills here are published. Never include a client's, employer's or private
  project's names, data or code. Distil the method; leave the product behind.
- Cite external catalogues (OWASP, CWE, MITRE) with their edition, and verify
  them against the official source before changing a reference table.
- Commit subjects are plain imperative sentences; do not start one with `#`.
