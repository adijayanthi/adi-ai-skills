# From requirements to tests

How security requirements become tests that any agent or engineer writes as a
matter of course, and that fail when a guardrail stops holding.

## Verification methods

Every SR names exactly one primary method. Use the `verification` value in the
register.

| `verification` | Use for | What the test does | Gates CI |
|---|---|---|---|
| `surface-absence` | S guardrails | Asserts the capability is absent from the route table, tool definitions, exported API or permission set | Yes |
| `enforcement-rejection` | E guardrails | Submits the violating action through the real entry point and asserts it is rejected, recorded, and that the system state is unchanged | Yes |
| `invariant` | Data-shape guarantees | Asserts a property over an assembled artifact — no secret in a log line, no untrusted source outside its region, byte-identical output for identical inputs | Yes |
| `policy-load` | Policy-as-data | Corrupted, checksum-mismatched and schema-invalid policy each refuse start | Yes |
| `red-team` | Injection and abuse resistance | Plants hostile content, runs the real flow, asserts no disallowed action reached the system | Yes — see below |
| `eval` | Probabilistic components | Measures a classifier, judge or model against a labelled set; reports a rate | No — own cadence |
| `review` | Process controls | A named reviewer signs off; the record is the evidence | No |
| `monitor` | Signals that only real traffic answers | A metric with a threshold and a named response | No |

**Why red-team tests can gate CI even when a model is involved.** Assert on the
system's state, not on the model's behaviour. If the model resists, nothing
happens; if it is fooled, enforcement blocks it. The assertion holds either
way, and a failure means the enforced layer genuinely failed.

**Why evals do not gate CI.** A suite that fails for reasons nobody can act on
teaches the team to ignore red builds. Track probabilistic rates separately,
per model, and never merge results across models.

## Rules for every security test

1. **Name it with the SR id.** Put `[SR-012]` in the test title or a tag the
   test runner reports. This is what the coverage check reads, and what makes
   a failing run say which requirement broke.
2. **A negative case and a positive control.** Assert the violation is
   rejected *and* that the closest legitimate action still succeeds. Without
   the positive control, a guardrail that rejects everything passes.
3. **Enter where an attacker would.** Exercise the real entry point — the
   HTTP route, the tool call, the queue consumer — not the helper behind it.
   Lower seams test your assumptions about the system, not the system.
4. **Assert against real dependencies where their behaviour is the
   constraint.** A mock of a platform API will happily pass while the real one
   does something destructive. Use a disposable real instance where feasible.
5. **Assert the property, not a proxy.** A test that greps for a word, a CSS
   class or a comment as a stand-in for the property will fail later on
   legitimate code and be deleted rather than fixed. Assert the structural
   route instead — for example, that a module imports nothing from the policy
   package, rather than that its source never mentions "policy".
6. **Assert the rule, not the calendar or the release.** Compute dates
   relative to now; assert a version moved forward rather than naming it.
   Anything reading live external data otherwise rots on someone else's
   schedule and fails in the direction that looks like a real defect.
7. **One property, guarded once in an obvious place.** If a property is
   guarded in two places, both are found and updated together — search for
   the other copy before changing either.
8. **Never weaken or delete an SR-tagged test without changing the register**
   in the same change, with the reason.

## Coverage

- Every SR whose `verification` gates CI has at least one test carrying its id.
- Every G has at least one SR, and every E guardrail has at least one
  `enforcement-rejection` SR.
- `scripts/check_coverage.py` reports both and exits non-zero on gaps in the
  gating set. Run it in CI after the test suite.
- An SR that genuinely cannot be tested yet is marked `"status": "known_gap"`
  with the issue that would close it. It is reported, not failed. A register
  that quietly omits what the system fails at proves only what you already
  believe.

## Red-team corpus (systems that read untrusted content)

Plant payloads on **every ingestion surface** in the inventory, including the
user's own message. Each corpus entry states its expected outcome *and the
mechanism that produces it*:

| Outcome | Meaning |
|---|---|
| `suppressed` | The surface never reaches the consumer — strongest, needs no model to be right |
| `unreachable` | The consumer could ask for it and no capability serves it |
| `stripped` | Deterministic normalisation removes it |
| `refused` | It reaches the consumer, which may be persuaded, and the gate rejects the action anyway. Store the action a fully persuaded consumer would submit, so the test submits exactly that |
| `known_gap` | Not stopped today. Recorded with the issue that would stop it |

Payload categories to cover: direct instruction, authority spoofing, urgency
and social engineering, obfuscated or split payloads, indirect (instructs the
system to write an instruction into memory), multi-turn (set up early, exploit
later), provenance forgery (text shaped like a structured signal), concealed
(invisible characters, bidirectional overrides, homoglyphs, hidden styling in
the user's own message), and relayed authority (a plausible forwarded notice a
user might paste in good faith). The last four target mechanisms rather than
general model compliance, and matter most.

**Placeholders, never literals.** `add admin <EMAIL> with password <SECRET>`
tests the defence identically to a real address. When production detections
feed the corpus, sanitise before anything is written.

**Regression is not evaluation.** A corpus of attacks already seen proves you
have not lost ground; it says nothing about novel ones. Schedule periodic
adversarial testing against the current defence as a separate obligation.
