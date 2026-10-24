# Changelog

## 1.1.0 — 2026-10-24

From the first independent run against a real product specification, compared
with that product's hand-written guardrail specification.

- **Learned trust.** Step 1 inventories values the system learns from the
  other party (discovered endpoints, headers, redirects, callback parameters)
  and where they are later trusted. When code exists, entry points, sinks and
  learned values are traced to it. New pattern **P30**: bind learned endpoints
  to the origin and scheme the user named. The run missed a real
  credential-redirection gap of exactly this shape, because the spec never
  mentioned the discovery step.
- **Three mandatory AI checks** in step 2: control-flow integrity, the lethal
  trifecta (in-policy exfiltration), and text-to-text harm. Also
  **subtraction**: does the task need each untrusted source, and does the
  product's scope force broad reading? The run missed plan-then-execute,
  in-policy exfiltration through publishing, and request-driven scope.
- **Delta against a model you cannot see.** When a spec cites guardrail IDs
  or documents that were not provided: ask for them first, otherwise use a
  non-colliding prefix and a mapping table.
- **Questions beyond the cap** become *assumed without asking*, listed with
  the round.
- **`proposed-accept`** status when no owner with authority is available.
- **Before code exists**, requirements carry `elements` (`A-nn`) instead of
  `components`.
- **Coverage check:** an E guardrail is proven by any of
  `enforcement-rejection`, `invariant`, `policy-load` or `red-team`, not only
  a rejection. Requirements with neither components nor elements are flagged.
- **Red-team corpus** has a fixed location and an example
  (`assets/redteam-corpus.example.json`), and is kept out of test directories.
- **Register schema** adds `title`, `elements`, `conditionalOn` and
  `acceptedBy`.
- `agents/openai.yaml` for Codex display metadata.

## 1.0.0 — 2026-10-24

First release.
