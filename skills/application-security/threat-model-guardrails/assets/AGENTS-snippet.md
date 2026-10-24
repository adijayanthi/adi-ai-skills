<!--
Append this block to the project's agent instruction file (AGENTS.md,
CLAUDE.md, or equivalent). Adjust the paths to where the artifacts were
written. It is harness-neutral on purpose: any agent that reads the file
follows it.
-->

## Security requirements

This project's threat model, guardrails and security requirements live in
`docs/security/`. **`docs/security/security-requirements.json` is
authoritative.**

When you write or change code or tests:

1. Find every requirement whose `components` globs match the files you are
   touching. Those requirements bind your change.
2. For each one, make sure a test exists that carries the requirement id in
   its title — for example `it("[SR-012] rejects a cross-tenant export", …)` —
   and asserts **both** the rejection and a positive control (the closest
   legitimate action still succeeds).
3. Test through the real entry point (route, tool call, queue consumer), not
   the helper behind it. Assert the system's resulting state, not which
   function was called.
4. Structural guardrails (`verification: surface-absence`) are tested by
   asserting the capability is absent. Do not add the capability to make a
   feature work — raise it instead; it is a threat-model change.
5. Never weaken, skip or delete a test tagged with an SR id without updating
   the register in the same change and stating why.
6. A change that adds an entry point, a privileged or irreversible operation,
   a data store, an integration or an AI capability needs a delta threat
   model before it is built.
7. Run the coverage check and include its result when you report the work:

   ```bash
   python3 scripts/security_coverage.py docs/security/security-requirements.json tests
   ```
