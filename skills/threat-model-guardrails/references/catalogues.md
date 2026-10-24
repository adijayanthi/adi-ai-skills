# Catalogues to cross-check against

Editions verified 2026-10. Before relying on a list, check whether a newer
edition exists; if you have web access, prefer the official page. Cite the
edition with each ID in the threat model (for example `A01:2025`, `CWE-862`,
`LLM06:2025`, `ASI02`).

Use the **spec trigger** column to decide relevance. A catalogue entry with no
matching element in the inventory is recorded as *not applicable* — never
listed as a threat just because it is on a list.

## OWASP Top 10:2025 (web applications)

Source: <https://owasp.org/Top10/2025/>

| ID | Name | STRIDE | Spec trigger |
|---|---|---|---|
| A01 | Broken Access Control (includes SSRF) | E, I | Roles, tenants, per-object ids in URLs, admin functions, outbound fetches of user-supplied URLs |
| A02 | Security Misconfiguration | I, E | New infrastructure, default settings, feature flags, CORS, headers, debug modes |
| A03 | Software Supply Chain Failures | T | Third-party packages, plugins, extensions, models, build pipeline, auto-update |
| A04 | Cryptographic Failures | I | Secrets, tokens, personal data at rest or in transit, key management |
| A05 | Injection | T, E | Any input reaching SQL, shell, templates, LDAP, expression languages, HTML output, or a model prompt |
| A06 | Insecure Design | all | Missing abuse cases, trust assumptions, business-logic flows (refunds, invites, quotas) |
| A07 | Authentication Failures | S | Login, sessions, password reset, MFA, API keys, magic links, SSO |
| A08 | Software or Data Integrity Failures | T | Deserialisation, signed updates, webhooks, CI artifacts, unsigned imports |
| A09 | Security Logging and Alerting Failures | R | Audit requirements, incident response, alerting, retention |
| A10 | Mishandling of Exceptional Conditions | D, I | Error paths, timeouts, partial failures, dependency outages, fail-open defaults |

## CWE Top 25 Most Dangerous Software Weaknesses (2025)

Source: <https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html>.
Formerly the "CWE/SANS Top 25"; now published by MITRE with CISA. The
memory-safety entries (marked †) apply only to components written in
memory-unsafe languages or native extensions — say so rather than listing
them against a managed-runtime service.

| Rank | CWE | Name | STRIDE | Spec trigger |
|---|---|---|---|---|
| 1 | 79 | Cross-site Scripting | T, I | User content rendered in a browser, rich text, previews, emails |
| 2 | 89 | SQL Injection | T, I | Search, filters, sorting, reporting, raw queries |
| 3 | 352 | Cross-Site Request Forgery | S, T | Cookie sessions with state-changing requests |
| 4 | 862 | Missing Authorization | E | Any new route, handler, job or export |
| 5 | 787 | Out-of-bounds Write † | T, E | Native code, parsers, codecs |
| 6 | 22 | Path Traversal | I, T | File names, archives, downloads, storage keys from input |
| 7 | 416 | Use After Free † | T, E | Native code |
| 8 | 125 | Out-of-bounds Read † | I | Native code, parsers |
| 9 | 78 | OS Command Injection | T, E | Shelling out, conversions, CLI wrappers |
| 10 | 94 | Code Injection | T, E | `eval`, templates, plugins, generated or model-written code that runs |
| 11 | 120 | Classic Buffer Overflow † | T, E | Native code |
| 12 | 434 | Unrestricted Upload of Dangerous File Type | T, E | Uploads, imports, attachments, avatars |
| 13 | 476 | NULL Pointer Dereference † | D | Native code |
| 14 | 121 | Stack-based Buffer Overflow † | T, E | Native code |
| 15 | 502 | Deserialization of Untrusted Data | T, E | Pickled/serialised objects, session blobs, queue payloads |
| 16 | 122 | Heap-based Buffer Overflow † | T, E | Native code |
| 17 | 863 | Incorrect Authorization | E | Complex role rules, delegation, sharing |
| 18 | 20 | Improper Input Validation | T | Every entry point |
| 19 | 284 | Improper Access Control | E | Any access decision |
| 20 | 200 | Exposure of Sensitive Information | I | Errors, logs, exports, APIs returning whole objects |
| 21 | 306 | Missing Authentication for Critical Function | S, E | Internal endpoints, admin tools, webhooks, health/debug routes |
| 22 | 918 | Server-Side Request Forgery | E, I | Fetching user-supplied URLs, webhooks, previews, importers |
| 23 | 77 | Command Injection | T, E | Any command built from input |
| 24 | 639 | Authorization Bypass Through User-Controlled Key | E | Ids in URLs or bodies selecting another user's object |
| 25 | 770 | Allocation of Resources Without Limits | D | Uploads, batch jobs, loops, model calls, fan-out |

## OWASP API Security Top 10 (2023)

Source: <https://api-security.owasp.org/editions/2023/en/0x11-t10>. Use when
the spec exposes an API, including one consumed only by your own frontend.

| ID | Name | Spec trigger |
|---|---|---|
| API1 | Broken Object Level Authorization | Object ids in requests |
| API2 | Broken Authentication | Tokens, keys, sessions |
| API3 | Broken Object Property Level Authorization | Mass assignment, whole-object responses |
| API4 | Unrestricted Resource Consumption | Pagination, batch, upload, expensive operations |
| API5 | Broken Function Level Authorization | Admin and internal routes alongside user routes |
| API6 | Unrestricted Access to Sensitive Business Flows | Sign-up, purchase, invite, referral, voting |
| API7 | Server Side Request Forgery | URL parameters fetched server-side |
| API8 | Security Misconfiguration | CORS, verbose errors, default credentials |
| API9 | Improper Inventory Management | Old versions, undocumented or debug endpoints |
| API10 | Unsafe Consumption of APIs | Trusting third-party API responses |

## OWASP Top 10 for LLM Applications (2025)

Source: <https://genai.owasp.org/llm-top-10/>. Use when any model reads input
or produces output that affects the system.

| ID | Name | Spec trigger | Strongest pattern |
|---|---|---|---|
| LLM01 | Prompt Injection | Model reads user input, documents, web pages, email, tool results | Trust typing, ingress pre-flight, argument provenance at sinks |
| LLM02 | Sensitive Information Disclosure | Model sees personal data, secrets, other tenants' data | Keep it out of context structurally; egress allowlists |
| LLM03 | Supply Chain | Third-party models, fine-tunes, prompts, plugins | Pinned model chain with declared capabilities |
| LLM04 | Data and Model Poisoning | Training, fine-tuning, RAG ingestion, memory | Untrusted label survives storage; provenance |
| LLM05 | Improper Output Handling | Model output rendered, executed, queried or sent | Treat output as untrusted input to the next sink |
| LLM06 | Excessive Agency | Tools that write, delete, pay, send or configure | Capability absence; enforced gate; irreversibility tiers |
| LLM07 | System Prompt Leakage | Secrets or rules in the prompt | Nothing in the prompt is a secret or an enforcement point |
| LLM08 | Vector and Embedding Weaknesses | RAG, shared vector stores | Per-tenant indexes; retrieved text is untrusted |
| LLM09 | Misinformation | Advice users act on | Proposals must cite structured signals; show provenance |
| LLM10 | Unbounded Consumption | Long contexts, loops, retries, spend | Ceilings that halt; per-tenant metering |

## OWASP Top 10 for Agentic Applications (2026)

Published December 2025 by the OWASP GenAI Security Project. Use when a model
plans, calls tools, holds memory, or talks to other agents. It extends the LLM
list; it does not replace it.

| ID | Name | Spec trigger | Strongest pattern |
|---|---|---|---|
| ASI01 | Agent Goal Hijack | Agent reads content it did not author | Plan-then-execute; re-plan as a visible event |
| ASI02 | Tool Misuse and Exploitation | Any tool with side effects | Operation allowlist; rate ceilings; argument provenance |
| ASI03 | Identity and Privilege Abuse | Agent acts with a user's or service's credentials | Opaque handles; least-privilege identity; scope binding |
| ASI04 | Agentic Supply Chain Vulnerabilities | External tools, MCP servers, schemas, prompts | Curated allowlist; descriptions never drive selection |
| ASI05 | Unexpected Code Execution | Agent writes or triggers code | No execution capability, or isolated sandbox with no credentials |
| ASI06 | Memory and Context Poisoning | Persistent memory, long sessions, summaries | Memory reloaded as untrusted; bounded content lifetime |
| ASI07 | Insecure Inter-Agent Communication | Multi-agent, delegation, sub-agents | Typed, schema-constrained messages; no free-text authority |
| ASI08 | Cascading Failures | Chained tools, retries, dependencies | Halt on ceiling; fail-closed defaults; circuit breakers |
| ASI09 | Human-Agent Trust Exploitation | Users approve or act on agent output | Confirmation is rare and bound; show content, not verdicts |
| ASI10 | Rogue Agents | Long-running or autonomous agents | Kill switch; behavioural monitoring; policy the agent cannot read or write |
