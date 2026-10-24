# Threat model — {{system or feature name}}

| | |
|---|---|
| Specification | {{path or link, with version or commit}} |
| Mode | Full / Delta against {{previous model version}} |
| Model version | {{n}} — {{date}} |
| Owners | {{product owner}}, {{engineering owner}} |

## 1. Governing principle

> {{One sentence the whole defence rests on. Example: "Capability restriction
> beats hygiene — every dangerous operation is pushed toward impossible and
> away from discouraged."}}

## 2. Attack surface

### 2.1 Elements

| ID | Type | Element | Trust zone | Source |
|---|---|---|---|---|
| A-01 | External entity | {{Tenant user, via web app}} | Untrusted | Stated §{{n}} |
| A-02 | Data flow | {{Inbound payment webhook}} | Crosses TB-1 | Stated §{{n}} |
| A-03 | Process | {{Invoice renderer}} | Internal | Inferred from §{{n}} — {{why}} |
| A-04 | Data store | {{Tenant documents bucket}} | Internal | Unknown — see Q3 |
| TB-1 | Trust boundary | {{Internet ↔ API gateway}} | | |

### 2.2 Assets

| Asset | Why an attacker wants it | Held in |
|---|---|---|
| {{Stored API credentials for tenants' accounts}} | {{Admin-equivalent access to many tenants}} | A-04 |

### 2.3 Actors

| Actor | Capability assumed |
|---|---|
| Anonymous internet | Can reach every public entry point |
| Legitimate tenant acting against us | Authenticated; may supply hostile input deliberately |
| Tenant relaying content they did not write | Authenticated; input partly authored by a third party |
| Another tenant | Authenticated in their own scope |
| Operator / support staff | {{what access}} |
| Compromised dependency | {{which}} |

### 2.4 Entry points and sinks

| Entry point | Elements | Reaches sinks |
|---|---|---|
| {{POST /webhooks/payments}} | A-02 → A-03 | {{marks invoice paid}} |

| Sink | Reversible? | Restore mechanism |
|---|---|---|
| {{Send invoice email}} | No | — |
| {{Edit draft invoice}} | Yes | {{Version history, restore by id}} |

### 2.5 AI components (omit if none)

| Component | Reads (trust type) | Can call | Remembers |
|---|---|---|---|

## 3. Threats

| ID | Threat | STRIDE | Elements | Actor | Why it is real here | Catalogue | Impact | Likelihood | Status |
|---|---|---|---|---|---|---|---|---|---|
| T-01 | {{Webhook forged to mark invoices paid}} | S, T | A-02 | Anonymous | {{§4.2 accepts webhooks with no stated signature check}} | A07:2025, CWE-306 | High — {{revenue loss}} | High — {{public URL}} | In scope |

Keep "why it is real here" specific enough that it could not be pasted into
another project's model. Status is one of: *in scope*, *out of scope*
(reason), *accepted* (by whom), *proposed-accept* (awaiting an owner with
authority), or *conditional on Qn*.

## 4. Explicitly not defended

| Not defended | Why |
|---|---|
| {{A tenant damaging their own data through legitimate requests}} | {{They own it; our obligation is visibility and reversibility}} |

## 5. Assumptions and open questions

| ID | Assumption (recommended answer) | Affects | Owner | Resolve by |
|---|---|---|---|---|
| AS-01 | {{Only owners can change roles}} | T-09 | {{product}} | {{before build of §n}} |

## 6. Catalogue coverage

Entries checked and found not applicable, so a reader can see they were
considered.

| Catalogue entry | Not applicable because |
|---|---|
| CWE-787 | {{No native code in scope}} |

## 7. Change log

| Version | Date | Change |
|---|---|---|
| 1 | {{date}} | Initial model |
