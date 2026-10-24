# Guardrail patterns

A library of guardrail shapes, each with the problem it solves, its strength,
and the test that proves it. Choose from these before inventing new ones, and
name the pattern in the guardrail entry so readers recognise it.

Patterns are grouped by where they act. Those marked **AI** apply when a model
reads input or calls tools; the rest apply to any system.

---

## Capability

### P1 — Capability absence · S
**Problem:** a dangerous operation is reachable, so every defence of it can be
argued around.
**Mechanism:** the endpoint, tool, route or code path does not exist. Non-goals
are enforced this way — *a non-goal defended only by policy is not a
non-goal.*
**Test:** assert absence from the surface — the route table, the tool
definitions, the exported API. There is no runtime path to exercise.
**Use first for:** user and permission management, account recovery changes,
code execution, anything the spec lists as out of scope.

### P2 — Operation allowlist · S + E
**Problem:** a generic capability ("make any API call") lets callers reach
operations nobody designed for.
**Mechanism:** the surface *is* the allowlist — one named operation per
intended action. Additionally validate the operation against policy data, so
one can be disabled without a deploy.
**Test:** surface test for the structural half; a disabled operation is
rejected for the enforced half.

### P3 — Curated allowlist for third-party components · E
**Problem:** installing or calling a third-party package, plugin, extension or
tool imports its risk.
**Mechanism:** a vetted list, matched by exact identifier, with vetting
criteria evaluated before entry rather than at use. Third-party descriptions
may explain, never select.
**Test:** an identifier outside the list is rejected; a description that names
a different component does not change what is chosen.

---

## Authorisation and action control

### P4 — Single choke point with an unforgeable approval · E
**Problem:** checks scattered across handlers drift, and one is eventually
missed.
**Mechanism:** every privileged write goes through one gate. The write
function requires an approval value that only the gate can construct — a
branded type, a capability token, a module-private constructor — so "forgot to
check" is a compile or runtime error rather than a bypass.
**Test:** each write without an approval is impossible to call or is rejected;
each rule in the gate has a rejection test.

### P5 — Scope binding · E
**Problem:** an action meant for one tenant, account or resource executes
against another.
**Mechanism:** every action carries its scope identifier; the gate verifies it
matches the session's authorised scope *and* that the credential resolves to
the same scope. A mismatch is never normal operation: reject, halt, alert.
**Test:** an action against B carrying A's session is rejected and halts.
Include bulk, export and background-job paths, which are where this is missed.

### P6 — Irreversibility tiering · E
**Problem:** confirmation applied by blast radius trains users to click
through, so the dangerous prompt is approved too.
**Mechanism:** an explicit table classifies every action as *reversible* —
execute, report plainly, offer a specific undo — or *irreversible* — confirm
first. A reversible classification is valid only with a **named restore
mechanism**. Partially reversible (state restores, consequences do not) is
treated as irreversible. Verify what the underlying platform actually restores
rather than assuming it.
**Test:** a reversible action executes and leaves a usable restore point; an
irreversible one without confirmation is rejected; every table row names a
mechanism or is tier 2.

### P7 — Confirmation bound to the exact action · E
**Problem:** a generic "yes" is replayed against a different or modified
action.
**Mechanism:** the confirmation token references the operation, target and a
hash of the proposed change. It cannot authorise anything else or be reused.
**Monitor:** confirmations per user per period, time-to-confirm (a cluster
under two seconds means nobody read it), and undo/complaint rate. A tripped
signal names an action to re-tier, not a threshold to raise.
**Test:** a token replayed against a modified proposal is rejected.

### P8 — Destructive-action floor · E
**Problem:** confirmation is treated as permission to destroy anything.
**Mechanism:** a short list of actions refused unconditionally — deleting what
the system did not create, unpublishing live content, writing outside owned
regions, changes that break the channel needed to undo them. Independent of
tier: a confirmation does not unlock it.
**Test:** each refused action is rejected *with* a valid confirmation.

### P9 — Proposal provenance · E · AI
**Problem:** a system that suggests actions can be talked into suggesting the
attacker's.
**Mechanism:** every system-initiated proposal carries a reference to the
structured signal that produced it — a version string, a database record, a
status code, a diff. Rejected when the reference is absent, unresolvable, or
resolves to untrusted free text. The system may *discuss* what it read; it
cannot *propose* acting on it.
**Test:** a proposal with absent, unresolvable and untrusted-derived
provenance is each rejected.

### P10 — Argument provenance at intent-requiring sinks · E · AI
**Problem:** the confused deputy. The action is permitted, so authorisation
passes, but the user never asked for *that target*.
**Mechanism:** label every argument by origin — `user` (traceable to the
user's own request), `system` (our structured state), `untrusted` (read from
content). Declare which arguments are **sinks requiring intent**: targets of
destructive actions, identifiers of what to install or remove, settings keys
and values, URLs, recipients, amounts. Reject `untrusted` at those sinks.
Match `system` labels by **signal kind and value**, never value alone — an
attacker who controls one field's value would otherwise label any argument it
happens to equal. An empty kind list means only the user's own words may fill
the sink.
**Test:** the same permitted action is accepted with a user-named target and
rejected when the target's value came from read content.

### P11 — Plan-then-execute · E · AI
**Problem:** content read mid-task redirects the action sequence.
**Mechanism:** commit the action sequence before reading untrusted data.
Content read afterwards can only fail to match the plan. A genuine mismatch
surfaces as a **visible re-plan the user sees**, never a silent change of
course. Redirection is an event, not a branch.
**Test:** an injected instruction read mid-task adds no action to the
committed plan.

### P12 — Rate and volume ceilings · E
**Problem:** a runaway or hijacked loop multiplies damage before anyone
notices.
**Mechanism:** per-session and per-scope ceilings on writes, sensitive
operations and total actions, held in policy data. Exceeding one halts and
alerts. A legitimate workflow that would exceed a ceiling gets its own,
derived ceiling — not a raised global one.
**Test:** exceeding each ceiling halts.

### P13 — Break-glass path that can only reduce capability · E
**Problem:** in an incident the operator needs to act where normal checks are
wrong (halted scopes, ceilings, user confirmation).
**Mechanism:** a separate path hard-coded to capability-reducing operations
only — revoke, halt, rotate. Audited before it acts, with a required reason
and an operator attribution. No user- or model-reachable route to it.
**Test:** the path cannot perform any capability-adding operation.

---

## Ingress — what enters

### P14 — Closed-world source inventory · S
**Problem:** new inputs arrive without anyone deciding how far to trust them.
**Mechanism:** every source that may reach a sensitive consumer (a model's
context, a template, a query) is listed with a trust type. Anything not listed
does not enter. Adding one is a reviewed change. Keep the inventory as data so
invariants are testable.
**Test:** every source has a trust type; no unlisted source appears in an
assembled input.

### P15 — Trust labels at the narrowest field · E
**Problem:** a combined response (rendered HTML, a whole object) mixes trusted
and untrusted fields, laundering the taint before any policy sees it.
**Mechanism:** fetch raw fields rather than rendered output, and label per
field. Labels are permanent: no path downgrades untrusted content, because the
downgrade decision becomes the target.
**Test:** an untrusted field nested in a trusted object keeps its label.

### P16 — Suppression by default · S/E
**Problem:** the highest-risk inputs — fields writable by people who are not
the user (comments, form submissions, file metadata, third-party
descriptions) — are read when nothing needed them.
**Mechanism:** excluded by default; admitted only when the committed plan
names them, decided by code rather than at read time.
**Test:** a suppressed source is absent under every request shape that does
not name it.

### P17 — Decide versus transform · E · AI
**Problem:** flagged content must be handled without killing legitimate work.
**Mechanism:** content read *to decide* degrades to schema-constrained typed
fields. Content read *to transform* passes through with flagged spans excised.
If excision leaves it unusable, stop and say so. A free-text summary of
hostile input is not extraction — it is a transformation of hostile input.
**Test:** a flagged decision-path read yields typed fields and no free text.

### P18 — Two-stage input pre-flight · S + E · AI
**Problem:** the user's own request may carry content they did not write —
concealed text, relayed phishing.
**Mechanism:** Stage 1, deterministic normalisation: strip zero-width and
invisible characters, bidirectional overrides, homoglyphs, invisible styling,
hidden markup; record what was hidden. The consumer only ever receives
normalised text — a structural guarantee. Stage 2, a probabilistic judge
returning a **schema-constrained verdict** only, so a hijacked judge can at
worst under-report. The judge is never an enforcement point. Input mechanics
(paste, typing speed) are not trust signals.
**Test:** each concealment technique is stripped; a non-schema verdict is a
failure, not parsed.

### P19 — Consent ceiling · E
**Problem:** a hostile account holder approves their own flagged input.
**Mechanism:** consent decides whether to proceed with the request. It never
authorises flagged content as instruction and never widens what the system
may do. The flagged span is discarded on approval. Show the user *the content*
that was found, never which rule fired.
**Test:** approval on a flagged request proceeds with the span still
discarded; a refuse-regardless verdict is not overridable.

### P20 — Bounded lifetime for untrusted content · S · AI
**Problem:** untrusted content read once persists in history or memory and
keeps steering later turns.
**Mechanism:** untrusted content enters in one structural position (for
example, tool results only) and is cleared when the turn that used it ends —
by structure, not by scanning. It never occupies a cached or shared prefix.
Memory is reloaded tagged untrusted, so it can shape conversation but never
authorise an action.
**Test:** after a turn completes, none of its untrusted content remains in
history; a payload written into memory cannot authorise the action it asks
for.

---

## Egress and data

### P21 — Opaque handles instead of secrets · S + E
**Problem:** secrets leak into logs, prompts, support messages or client code.
**Mechanism:** callers receive an opaque handle; one narrow module resolves it
to the secret, lends it to a callback and zeroes it after. No function returns
a secret. Additionally scan outbound logs and messages for secret-shaped
content as defence in depth.
**Test:** a secret-shaped value reaching each egress point is blocked; no
export returns plaintext.

### P22 — Egress data-class allowlist · E
**Problem:** data reaches a destination it was never meant for.
**Mechanism:** for each egress point — API responses, logs, analytics, support
tooling, emails, exports, model context, third parties — list what data
classes are permitted and what are forbidden.
**Test:** each forbidden class at each egress point is rejected.

### P23 — Sanitise before persisting · E
**Problem:** "we sanitise logs" hardens into a guarantee nobody verified.
**Mechanism:** sanitise in memory at detection, before any write. A typed
boundary (a branded `Sanitized` value) makes every persistence path require
it. Deterministic redaction for shaped identifiers; probabilistic for
free-form personal data, documented as fallible. **Uncertain sanitisation
fails closed to metadata only.**
**Test:** a persistence path cannot accept an unsanitised string; uncertain
input stores metadata and no text.

### P24 — Per-tenant isolation of caches and indexes · S
**Problem:** a shared cache, prefix or vector index carries one tenant's data
into another's response.
**Mechanism:** scope keys per tenant by construction. A shared prefix across
tenants is a guardrail violation, not an optimisation.
**Test:** two tenants' assembled inputs share no tenant-specific bytes.

### P30 — Bind learned endpoints to what the user named · E
**Problem:** the system learns an address from the other party (a discovered
API root, a header, a redirect, a callback parameter) and later sends
credentials or trust there. A misconfigured or compromised party then
redirects authenticated traffic, often downgrading it to plain http.
**Mechanism:** a learned endpoint must share the origin and scheme of the
address the user supplied. Check it when it is learned and again at use,
because rows stored before the check exist. Refuse rather than rewrite: a
rewritten guess can succeed against the wrong thing.
**Test:** a learned endpoint on another origin, or on http, is refused and
nothing is stored or sent.

---

## Policy and operations

### P25 — Policy as versioned, checksummed data; fail closed on load · E
**Problem:** a service running without its rules is more dangerous than one
that is down.
**Mechanism:** allowlists, tier tables, sinks and ceilings live in structured
data, schema-validated and checksummed at startup. Load failure, checksum
mismatch or a rule that can never match refuses start. Every audit entry
records the policy version. Policy changes are reviewed and audited. The
system's own runtime (and any model) cannot read or write it.
**Test:** corrupted, mismatched and invalid policy each refuse start.

### P26 — Violation response classes · E
**Problem:** every rejection treated the same either floods alerts or hides
attacks.
**Mechanism:** *Expected* (normal limits — logged, explained, no alert);
*Suspicious* (possible attack — logged, low alert, **aggregated per scope**,
since repeats matter more than singles); *Critical* (scope mismatch, secret
egress, ceiling breach, policy failure — halt, alert immediately, no further
action until reviewed). Every rejection records time, actor, scope, rule,
attempted operation and target, policy version, decision, message shown and —
for AI — which model proposed it.
**Test:** each class produces its response; a Critical halts.

### P27 — Declared fail modes per component · E
**Problem:** a dependency outage quietly turns a control off.
**Mechanism:** for each component that can be unavailable or return garbage,
state fail open or fail closed and why. They may legitimately differ — a
filter that is never an enforcement point may fail open, while a sanitiser
guarding disk must fail closed. Document the asymmetry where both live.
**Test:** each component's failure produces its declared behaviour.

### P28 — Dependency capability declarations · E · AI
**Problem:** swapping a model or dependency silently removes a security
property it provided.
**Mechanism:** each model or dependency declares its relevant capabilities as
documented, undocumented or absent; the code declares what it requires; only
*documented* satisfies a requirement, checked at startup. Record which model
served each action.
**Test:** a chain containing a model lacking a required capability refuses
start.

### P29 — Human release path for hard refusals · operational
**Problem:** a control that refuses with no override strands a legitimate user
on a false positive.
**Mechanism:** a reviewed path for a human to release a block. A release lifts
the block; it never replays the refused action automatically.
**Test:** a release lets the user resubmit; it does not execute the original.

---

## User messaging (part of every guardrail)

- Plain language. No rule IDs, tiers or internal vocabulary.
- Say what was not done, and why, in terms of the user's own system.
- Offer what can be done instead. A refusal without an alternative is a dead
  end.
- Never imply the user is at fault when an attack is detected — they are the
  target.
- Show the content that was found, never which check found it.
- Status and error text never reveal which stage, rule or dependency failed.
- A message that says something happened ("the team has been alerted") must
  trace to code that makes it happen.
