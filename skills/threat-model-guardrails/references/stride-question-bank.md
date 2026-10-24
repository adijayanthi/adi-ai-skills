# STRIDE question bank

Use STRIDE **per element**: walk each element of the attack-surface inventory
and ask only the categories that apply to its type. Then use the questions
below to find what the specification leaves unanswered. Ask only questions
whose answer would change a threat, a severity or a guardrail.

## Applicability matrix

| Element type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External entity (user, partner system, third-party API) | ✓ | | ✓ | | | |
| Process (service, worker, function, model call, agent) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data store (database, cache, bucket, queue, log, memory) | | ✓ | ✓¹ | ✓ | ✓ | |
| Data flow (request, message, webhook, file transfer, prompt) | | ✓ | | ✓ | ✓ | |
| Trust boundary | Every flow that crosses it gets all of T, I, D, plus S for whoever is on the far side |

¹ Repudiation applies to a data store when it *is* the record — an audit log
or ledger.

## Question format

Every question you ask uses this shape:

```
Q4  [Elevation · A-07 Admin API]
    Can a workspace member change another member's role through the API,
    or only through the admin console?
    Why it matters: the spec lists role changes under "settings" with no
    actor named; if members can do it, T-09 (privilege escalation via
    self-promotion) is High.
    Recommended: (a) owners only, enforced server-side — role changes are
    irreversible in effect, since an escalated account can lock the owner out.
    (a) Owners only → G-06 enforced check, T-09 drops to Low.
    (b) Any member  → T-09 High; needs approval binding and an audit alert.
    (c) Not yet decided → recorded as an assumption, owner: product.
```

## S — Spoofing: is every actor who they claim to be?

- Who are the actors, and how is each authenticated — users, services,
  webhooks, scheduled jobs, operators, support staff?
- How does a callback or webhook prove it came from the claimed sender?
  Signature, shared secret, mutual TLS, IP allowlist, or nothing?
- Can one account act for another — delegation, impersonation by support,
  "log in as"? Who can, and is it recorded?
- What identifies a tenant on each request, and where does that value come
  from — the session, or something the client sends?
- Can content the system reads *look like* it comes from the system or the
  operator — a notice in a fetched page, an email styled as ours?
- **AI:** can text the model reads impersonate the user, the operator or a
  tool result? Is there a channel the model's input cannot forge?

## T — Tampering: can data or code be changed by someone who should not?

- Which inputs reach a query, a command, a template, a file path, a
  deserialiser, an expression evaluator or generated code?
- Which client-supplied values are trusted server-side — prices, ids, roles,
  flags, redirect targets?
- What can a tenant upload or import, what types are accepted, where is it
  stored, and is it ever executed or served from our origin?
- How are dependencies, plugins, models, prompts and build artifacts sourced
  and pinned? Who can change them, and is the change reviewed?
- Are configuration, limits and allowlists code, data or environment? Who can
  edit them, and what happens if they fail to load?
- Can a confirmation or approval be replayed against a changed request?
- **AI:** can content the model reads change what it does next — which tool,
  which target, which value? Can it persist into memory or later turns?

## R — Repudiation: could anyone deny doing what they did?

- Which actions must be attributable, to whom, and for how long?
- Is the audit log append-only, and who can alter or delete it?
- Does each record carry the actor, the target, the decision, the rule or
  policy version in force, and — for AI — which model acted?
- Is the user's own request recorded alongside the action it caused?
- Are operator and support actions recorded the same way as user actions,
  and distinguishably from them?

## I — Information disclosure: can data reach someone who should not see it?

- What personal, financial, credential or confidential data exists, and
  where is each stored, logged, cached, exported and sent?
- Which egress points exist — API responses, logs, analytics, error pages,
  support tooling, emails, exports, model prompts, third parties? What data
  class may cross each?
- Can one tenant's data appear in another tenant's response, cache, search
  index, export, prompt or shared cache prefix?
- Are secrets ever in a URL, a log line, an error message, client storage,
  source control or a model's context?
- What do error and status messages reveal about internals, other users or
  which check fired?
- **AI:** can the model be induced to reveal its instructions, other users'
  data or secrets? Can it publish data outward — a link, an image URL, a
  public page, a webhook?

## D — Denial of service: can availability be exhausted or broken?

- What is unbounded — request size, file size, list length, recursion,
  retries, fan-out, loops, model tokens, spend?
- What happens when each dependency is slow, down, rate-limited or returning
  garbage? Does the system fail open or closed, and is that chosen?
- Can a single action take down the channel needed to undo it?
- Can one tenant degrade others — shared queues, shared quotas, noisy jobs?
- **AI:** can an agent loop, repeat an action, or be steered into repeating
  one? What ceilings stop it, and what happens when one trips?

## E — Elevation of privilege: can anyone gain capability they should not have?

- What roles exist, and which operations does each permit? Is every check
  server-side, on every route, including bulk and export paths?
- Is authorisation checked against the object — this user may act on *this*
  record — and not only against the function?
- Can any path create users, change roles, grant permissions, issue tokens or
  change account recovery? Is that path needed at all?
- What does the system's own service identity have access to, and is that
  the minimum the spec needs?
- Can a compromised tenant system be used as a launch point into ours or
  another tenant's?
- **AI:** what is the full tool surface, and which tools are never needed?
  Which tool arguments select a target, recipient, URL, key or amount — and
  can those values come from content the user did not write?

## Cross-cutting questions

These rarely sit under one letter and are often the most valuable.

- **Non-goals.** What will the system deliberately never do? Is each non-goal
  enforced by the capability being absent, or only by policy?
- **Irreversibility.** For each sink: can we undo it on the user's behalf, by
  what named mechanism, and for how long? What does the underlying platform
  actually restore — verified, not assumed?
- **Confirmation.** Which actions ask the user first, how often will a typical
  user see a prompt, and what tells you they stopped reading?
- **Hostile account holder.** What could a paying customer gain by acting
  against us, against other tenants, or against the platform?
- **Relayed content.** Can a user forward or paste content written by someone
  else — an email, a document, a page — into a request?
- **Break-glass.** What does an operator need to do in an incident (revoke
  access, halt a tenant, rotate keys), and can that path only reduce
  capability?
- **Human-review paths.** If a control can refuse with no override, how does
  a wrongly refused user get unstuck?
- **Out of scope.** What threats are knowingly not defended — the user
  damaging their own data, a breach of their hosting, a compromised provider?
