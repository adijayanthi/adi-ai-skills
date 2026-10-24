# Security requirements — {{system or feature name}}

The human-readable view of `security-requirements.json`. **The JSON register
is authoritative**; tooling and agents read it, and this document is kept in
step with it in the same change.

Every test that verifies a requirement carries its id — for example
`[SR-001]` — in the test title, so a failing run names the broken requirement
and `scripts/security_coverage.py` can report what is uncovered.

## Requirements

### SR-001 — {{Short title}}

| | |
|---|---|
| Statement | The system **shall** {{reject a payment webhook whose signature does not verify against the tenant's signing secret, and leave the invoice unchanged}}. |
| Guardrails | G-01 |
| Threats | T-01 |
| Verification | `enforcement-rejection` |
| Components | `{{src/webhooks/**}}` |
| Status | open / covered / known_gap ({{issue}}) |

**Acceptance criteria**

- Negative: {{a webhook with a missing or wrong signature returns 401, writes
  a Suspicious audit row with rule G-01, and the invoice status is unchanged}}.
- Positive control: {{a correctly signed webhook marks the invoice paid}}.

## Traceability

| SR | G | T | Verification | Tests |
|---|---|---|---|---|
| SR-001 | G-01 | T-01 | enforcement-rejection | {{filled in by the coverage check}} |
