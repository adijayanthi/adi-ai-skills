# Guardrails — {{system or feature name}}

Companion to `THREAT-MODEL.md`. Every guardrail carries an ID; every ID has at
least one security requirement in `SECURITY-REQUIREMENTS.md` and at least one
test asserting rejection.

## 1. Enforcement strengths

| Strength | Mechanism | Failure mode |
|---|---|---|
| **S — Structural** | The capability does not exist | Cannot fail |
| **E — Enforced** | Code validates every relevant action and rejects violations | Fails closed |
| **A — Advisory** | Documentation, copy, prompts, training | Fails open |

**Assignment rule.** A guardrail may be advisory-only if and only if its
worst-case failure is a poor experience. Otherwise it is S or E.

## 2. Enforcement points

| Point | Controls | Deterministic? |
|---|---|---|
| Structural | What capabilities exist at all | Yes |
| Ingress | What enters a sensitive consumer, and with what label | {{Normalisation yes; classifiers no}} |
| Egress | Every outbound action and data flow | Yes |
| At rest | What is stored, encrypted, retained | Yes |
| Operational | Monitoring, review, incident response | No |

## 3. Catalogue

### G-01 — {{Name}} · {{S / E / A / S+E}}

| | |
|---|---|
| Mitigates | T-01, T-04 |
| Pattern | {{P10 Argument provenance at intent-requiring sinks}} |
| Enforcement point | {{Egress — the action gate}} |
| Deterministic | {{Yes / No — and what part is probabilistic}} |
| Fails | {{Closed — a policy load failure refuses start}} |
| Requirements | SR-001, SR-002 |

**Mechanism.** {{What the code does, where it lives. Name the location, not
the intent.}}

**Residual risk.** {{What still gets through, and what bounds it.}}

**User message.** {{What the user sees when this fires, in plain language,
with the alternative offered.}}

## 4. Coverage

| Threat | Guardrails | Strongest | Status |
|---|---|---|---|
| T-01 | G-01, G-04 | E | Covered |
| T-07 | G-09 | A | **Accepted** by {{owner}} — worst case is {{poor experience}} |

## 5. Deterministic and probabilistic

| Property | Strength | Why |
|---|---|---|
| {{No secret ever reaches a log line}} | Deterministic | {{Opaque handles; no function returns a secret}} |
| {{The classifier flags hostile content}} | Probabilistic | {{Reduces volume; never eliminates}} |

No tuning moves a row from probabilistic to deterministic — only moving the
mechanism into code does.

## 6. Failure modes by component

| Component | When unavailable | Why |
|---|---|---|
| {{Input judge}} | {{Fail open if deterministic stage found nothing; closed otherwise}} | {{Never an enforcement point}} |

## 7. Policy data

| File | Holds | Changed by | Reviewed by |
|---|---|---|---|
| {{policy/action-tiers.json}} | {{Tier per action, restore mechanism}} | {{PR}} | {{owner}} |

Load failure, checksum mismatch or schema violation refuses start. Every audit
entry records the policy version. Commercial limits do not live here.

## 8. Violation response

| Class | Examples | Response |
|---|---|---|
| Expected | {{Action outside the allowlist}} | Logged, explained, no alert |
| Suspicious | {{Untrusted value at an intent sink}} | Logged, low alert, aggregated per scope |
| Critical | {{Scope mismatch; secret egress; ceiling breach; policy load failure}} | Halt, immediate alert, no further action until reviewed |

## 9. Decisions

| Decision | Reasoning | Date | Decided by |
|---|---|---|---|
