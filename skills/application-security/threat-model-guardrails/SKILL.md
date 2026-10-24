---
name: threat-model-guardrails
description: Turns a product, feature or enhancement specification (any Markdown spec or PRD) into an attack-surface inventory, a STRIDE threat model, a guardrail catalogue with enforcement strengths, and testable security requirements that test-writing agents must cover. Cross-checks against OWASP Top 10, CWE Top 25 and, for AI or agent features, the OWASP LLM and Agentic Top 10s. Asks the product team batched clarifying questions where the spec is silent. Use when someone shares a spec and asks for a threat model, attack surface, abuse cases, guardrails, security requirements or security test cases, or before building a feature that adds an entry point, a privilege, a data store, an integration or an AI capability.
license: Apache-2.0
metadata:
  version: "1.1.0"
  domain: "application-security"
  spec-format: "agentskills.io"
---

# Threat model and guardrails from a specification

Reads a specification, finds what it does not say, asks, and produces four
linked artifacts. Every line of the output traces in one chain:

```
A-nn  attack-surface element   (what exists)
 └─ T-nn  threat               (what can go wrong there, and why it is real here)
     └─ G-nn  guardrail        (what prevents it, and how strongly)
         └─ SR-nnn  requirement (a testable "shall" statement)
             └─ test           (named with the SR id, asserting rejection)
```

A threat with no guardrail is an accepted risk and must say so. A guardrail
with no requirement is an intention. A requirement with no test will quietly
stop being true.

## The yardstick

These are the judgements the whole skill applies. They are what separates a
threat model that shapes the product from one that is filed and forgotten.

1. **Capability restriction beats hygiene.** A capability that does not exist
   cannot be misused however the request is phrased. For every threat, ask
   first whether the capability is needed at all.
2. **Every guardrail declares a strength** — and the strength is a property of
   *where the control lives*, not how carefully it is written:

   | Strength | Mechanism | Failure mode |
   |---|---|---|
   | **S — Structural** | The capability, endpoint, tool or code path does not exist | Cannot fail; nothing to bypass |
   | **E — Enforced** | Our code validates every relevant action and rejects violations regardless of caller intent | Fails closed: a bug blocks a legitimate action |
   | **A — Advisory** | Documentation, UI copy, training, a prompt instruction, a warning | Fails open under pressure; guarantees nothing |

3. **The assignment rule.** A guardrail may be advisory-only *if and only if*
   its worst-case failure is a poor experience. If the worst case is a breach,
   data loss, a broken customer system, or an action nobody authorised, it must
   be S or E. Advisory supplements; it never substitutes.
4. **Say what is not defended.** An explicit out-of-scope list prevents false
   confidence and stops the model being read as a promise.
5. **Deterministic and probabilistic are never blurred.** Any claimed
   guarantee states which it rests on. A classifier, a model, a heuristic or a
   human reviewer reduces volume; only code that runs on every request
   guarantees. Nothing moves up that line by being tuned.
6. **Tier by irreversibility, not blast radius.** Confirmation belongs where
   the system cannot undo the action. A "reversible" claim is valid only if it
   names the restore mechanism. Confirmation is a last resort: users trained
   by frequent prompts approve the dangerous one too.
7. **Permitted is not wanted.** An authorisation check asks whether an action
   is allowed, not whether the user intended it. Where values that select a
   target, recipient, URL, key or amount can come from data the user did not
   author, the requirement must bind them to the user's own input
   (the confused-deputy test).
8. **Fail closed by default; argue every fail-open.** Each component that can
   be unavailable records what happens then, and why.
9. **Policy is versioned data, and loads or the service does not start.**
   Limits, allowlists and tier tables live in reviewed, checksummed data; every
   audit entry records the policy version in force.
10. **Every guardrail has at least one test asserting rejection, and every gap
    is written down.** A known gap recorded with its owner is honest; a gap
    discovered later is a breach.

The full pattern library behind these is in
[references/guardrail-patterns.md](references/guardrail-patterns.md).

## Modes

- **Full** — a new product or a first threat model. Produce all artifacts.
- **Delta** — a feature or enhancement against an existing model. Use this
  whenever `docs/security/security-requirements.json` (or the location the
  user names) already exists. Analyse only what the feature adds or changes,
  continue the existing numbering, and never renumber or reuse an ID.
- **Delta against a model you cannot see.** If the spec cites threat or
  guardrail IDs, or a security document that was not provided, it already has
  a model. Ask for that document before anything else. If it cannot be
  supplied, run in full mode with a prefix that cannot collide (for example
  `TM-G-nn`), and map every ID the spec cites to yours in a table, so the two
  numberings are never confused.

State the mode and the output location before starting. Default location is
`docs/security/`; follow the project's convention if it has one.

## Workflow

### 1. Read and decompose

Read the whole specification and any linked documents it treats as
authoritative. In delta mode, read the existing threat model and register
first. Then build the **attack-surface inventory**:

- **Elements**, each typed as *external entity*, *process*, *data store*,
  *data flow* or *trust boundary* — the STRIDE-per-element types.
- **Assets** — what an attacker wants: credentials, personal data, money
  movement, admin capability, other tenants' data, availability, reputation.
- **Actors** — including the legitimate user acting against you, a user
  relaying content they did not write, an operator or insider, a compromised
  dependency, and another tenant.
- **Entry points** — every place input arrives, including webhooks, file
  uploads, imports, email, third-party callbacks, scheduled jobs and content
  fetched from elsewhere.
- **Sinks** — every privileged or irreversible operation: writes, deletes,
  payments, permission changes, outbound messages, publication, code
  execution, configuration changes.
- **AI components**, if any — what each model reads, which of that is
  untrusted, which tools it can call, what it remembers.
- **Learned trust** — values the system learns from the other party and
  later relies on: endpoints from discovery or response headers, redirect
  targets, callback parameters, keys or settings fetched from the far side.
  For each, note where it is later trusted, such as credentials sent to it,
  links rendered from it, or code run because of it. Specs rarely mention
  these, and they are where implementations quietly widen the attack surface.

When code exists, trace each entry point, sink and learned value to the code
that implements it. A spec describes intent, and the gap that matters is often
something the implementation learned that the spec never mentions.

Mark every fact **stated** (cite the spec section), **inferred** (say from
what) or **unknown**. Unknowns become questions in step 3; inferences become
questions when a wrong inference would change a threat's severity.

### 2. Analyse

Run STRIDE per element using the applicability matrix and question bank in
[references/stride-question-bank.md](references/stride-question-bank.md).
Then cross-check the inventory against the catalogues in
[references/catalogues.md](references/catalogues.md), using their *spec
triggers* — a mention of file upload, templating, redirects, deserialisation,
outbound fetches, tool-calling models and so on.

For every AI component that reads untrusted content, three checks are
mandatory, because each names a harm that authorisation checks cannot see:

- **Control-flow integrity.** If it can also act, how is content read
  mid-task prevented from adding, removing or redirecting an action? Examples
  are a plan committed before the read, or a separate context with no tools.
  If nothing prevents it, that is a threat.
- **The lethal trifecta.** Does it combine private data, untrusted content and
  a way to communicate externally? Publishing to the public web, sending
  email, setting a link or calling a webhook all count. If all three are
  present, in-policy exfiltration is a threat, since no policy that permits
  the action can block it.
- **Text-to-text harm.** Can injected content make its *output* misleading
  ("no action needed", a fabricated recommendation) when a person acts on that
  output? No action passes a gate, so record it, and record what bounds it.

Also apply **subtraction**: for each untrusted source, ask whether the task
needs it at all, and whether the product's scope forces broad reading before
acting (open-ended "look at everything and fix it" requests). Narrowing scope
is often the strongest ingress control available.

Every candidate threat must be **grounded**: tied to an element and to a
reason it is real *in this system*. A catalogue entry with no element in the
inventory is noted as not applicable, not listed as a threat. Threats that
depend on an unanswered question are held as *conditional on Qn*.

### 3. Ask

Ask the product or development team the questions whose answers change the
model. Rules:

- **Batch them.** One round of up to twelve, ordered by how much the answer
  moves severity or design. Never drip one question at a time.
- **Beyond the cap**, questions whose answer would not change a threat's
  severity or a guardrail's strength become assumptions directly. List them
  under the round as *assumed without asking*, with the recommended answer,
  so the team can still overturn them.
- **Never ask what the spec already answers.** Quote it instead.
- Each question carries its STRIDE tag and element ID, **why it matters**, a
  **recommended answer** with the reason, and **what changes** under each
  answer. A question without a recommendation pushes analysis back onto the
  person asked.
- Prefer decisions over facts the team would have to research. Where a fact
  can be checked directly — reading code, probing an API, reading vendor
  documentation — check it rather than asking.
- If the harness offers a structured multiple-choice question tool, use it for
  questions with discrete answers; otherwise ask in plain text with lettered
  options.
- **Stop and wait for answers.** Do not draft the threat model in the same
  turn as the questions.
- At most three rounds. After that, or when told to proceed, record every
  open question as an **assumption** with the recommended answer, an owner
  and the threats it affects, and continue.

If an answer reframes the question, the framing was wrong: rebuild the
affected part of the inventory rather than forcing the answer into it.

### 4. Write the threat model

Use [assets/THREAT-MODEL.template.md](assets/THREAT-MODEL.template.md). Each
threat carries: ID, title, STRIDE category, affected elements, actor, **why it
is real here** (one concrete sentence tied to the spec), catalogue references
(OWASP / CWE / LLM / ASI IDs), impact and likelihood (High/Medium/Low, with
the reason), and status — *in scope*, *out of scope* with the reason, or
*accepted* with the owner who accepted it. When no one with authority is
available, use *proposed-accept*: a threat is not accepted until someone with
the authority to accept it says so, and every proposed-accept threat is
listed in the summary.

Include the **governing principle** the system's defence rests on, in one
sentence. Every later guardrail should be explainable from it.

### 5. Derive the guardrails

Use [assets/GUARDRAILS.template.md](assets/GUARDRAILS.template.md) and the
patterns in [references/guardrail-patterns.md](references/guardrail-patterns.md).
Each guardrail carries: ID, the threats it mitigates, **strength** (S, E, A or
a combination), mechanism, **enforcement point** (structural absence, ingress,
egress, at rest, or operational), **failure behaviour** (open or closed, and
why), deterministic or probabilistic, and residual risk.

Then check coverage:

- Every in-scope threat whose worst case is worse than a poor experience has at
  least one S or E guardrail. If not, either add one or move the threat to
  *accepted* with an owner — never leave it covered only by A.
- Prefer S wherever the capability is genuinely never needed.
- Any guardrail that relies on a user reading a prompt is marked as such, with
  how its effectiveness will be monitored.
- Commercial or plan limits are not safety controls. Keep them out of the
  guardrail catalogue and its policy data, so nobody reads a safety ceiling as
  negotiable.

In delta mode, also list **existing guardrails the feature presses** — any
limit, tier or exclusion a legitimate use of the new feature would trip — and
resolve each explicitly rather than letting the first incident decide.

### 6. Write the security requirements

Use [assets/SECURITY-REQUIREMENTS.template.md](assets/SECURITY-REQUIREMENTS.template.md).
Each requirement is one observable "shall" statement, traced to guardrails and
threats, with:

- **Verification method** — one of the methods in
  [references/test-traceability.md](references/test-traceability.md).
  Structural guardrails are verified by asserting absence; enforced ones by
  submitting the violating action and asserting rejection.
- **Acceptance criteria** — the negative case (the violation is rejected and
  recorded) *and* a positive control (the legitimate action still succeeds),
  so over-blocking is caught as well as under-blocking.
- **Components** — the code paths or modules it applies to, as globs, so a
  test-writing agent can find which requirements bind the file it is
  touching. Before code exists, put the element IDs (`A-nn`) in `elements`,
  leave `components` empty, and fill in the globs when the code lands. A
  requirement with neither cannot be found by anyone writing tests.

Write the machine-readable register alongside the document, in the shape of
[assets/security-requirements.example.json](assets/security-requirements.example.json).
The register, not the prose, is what tooling and other agents read.

### 7. Hand off to testing

Make the requirements bind the agents and people who write tests, in any
harness:

1. Copy [scripts/check_coverage.py](scripts/check_coverage.py) into the project
   (for example `scripts/security_coverage.py`) so CI can run it without the
   skill installed.
2. Append the block in [assets/AGENTS-snippet.md](assets/AGENTS-snippet.md) to
   the project's agent instruction file — `AGENTS.md`, `CLAUDE.md`, or
   whichever the project's harnesses read. Ask before editing it.
3. If the system reads untrusted content into a model, scaffold the red-team
   corpus described in
   [references/test-traceability.md](references/test-traceability.md) at
   `docs/security/redteam-corpus.json`, in the shape of
   [assets/redteam-corpus.example.json](assets/redteam-corpus.example.json).
   Every entry states its expected outcome and the mechanism that produces
   it. Keep the corpus out of test directories: it cites SR ids but is not a
   test, and the coverage check would count it as one.
4. Run the coverage check and report uncovered requirements. They are
   expected on a fresh model; report them as the test backlog, not as a
   failure.

### 8. Self-review before presenting

- Every T has a "why real here" a reader could not paste into another project.
- Every in-scope T is covered by S/E, or is accepted with an owner.
- No guarantee rests on an A control, a classifier, or a model's compliance.
- Every "reversible" claim names its restore mechanism.
- Every AI component that reads untrusted content has a control-flow
  integrity answer, a lethal-trifecta assessment and a text-to-text harm
  entry.
- Every learned value that is later trusted has a guardrail binding it.
- Every component with a failure mode states open or closed.
- Every SR has a negative case and a positive control.
- Out-of-scope and assumptions lists are present and non-empty, or explicitly
  "none".
- No user-facing string in the spec asserts that something happened (*"we've
  alerted the team"*) unless a requirement makes the code do it. Copy review
  checks wording, not truth.
- IDs are stable, unique, and continue the existing sequence in delta mode.

Present a short summary: counts per artifact, the highest-severity threats,
any threat accepted rather than mitigated, and the open assumptions. Then
point to the files.

## Writing rules

- Cite the spec section for every stated fact. Do not invent product facts.
- Concrete over generic: *"a webhook URL is supplied by the tenant and fetched
  by the worker"*, not *"SSRF may be possible"*.
- Name the control's location, not its intent: *"the export handler rejects
  an account id that is not the session's"*, not *"ensure tenants are
  isolated"*.
- Keep user-facing messaging requirements in the guardrails document: plain
  language, no rule IDs, never imply the user is at fault, say what was not
  done and offer what can be done instead.
- When a decision is the team's to make, record it as a decision with the
  reasoning, so later readers know it was a choice and not an oversight.
