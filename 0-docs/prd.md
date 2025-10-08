Here’s a **very detailed PRD (Product Requirements Document)** for your “Browser-Extension + MCP for Teams Planner” project. You can adapt, cut, or expand as needed. I’ll label sections clearly.

---

## 1. Title & Authors

* **Product name (tentative):** PlannerAgent
* **Document version:** 1.0
* **Date:** [today’s date]
* **Author:** [Your name / team]
* **Stakeholders:** You (developer), users / clients, possibly future maintainers

---

## 2. Purpose & Scope

**Purpose:**
Provide an AI-driven integration between a user’s browser session (Teams/Planner UI) and an AI agent via MCP, enabling reading, creating, updating, and deleting tasks in Microsoft Planner within Teams, using a browser extension + MCP server bridge.

**Scope (in scope):**

* Browser extension (Chrome / Chromium) that runs on Teams / Planner web UI
* MCP server / tool provider that maps Planner operations to extension APIs
* AI agent (Cursor or similar) integration via MCP
* Core CRUD operations on Planner tasks & plans
* Authentication piggybacked via browser session (assuming user already logged in)

**Out of scope (for this 3-4 month MVP):**

* Full support for attachments, comments, file uploads
* Support for mobile / Teams desktop app
* Multi-tenant or enterprise administration features
* High fault tolerance, load balancing, clustering
* Long-term UI change resilience

---

## 3. Stakeholders & Users

* **Primary user (you / your team):** wants to ask “Create a task …” etc.
* **Secondary user (if shared):** other users in your organization, testers
* **Developer / maintainer:** you or collaborators
* **Viewer:** minimal documentation / support user

---

## 4. Use Cases / User Stories

1. *As a user*, I can ask the AI “List all tasks in Plan X” and see their titles, due dates, statuses.
2. *As a user*, I can ask “Create a new task in Plan X with title / due date / assignee / description.”
3. *As a user*, I can ask “Update task Y’s due date to Z” or “Mark task Y complete.”
4. *As a user*, I can ask “Delete task Y.”
5. *As a user*, I can verify the action in the actual Planner UI.
6. *As a developer*, I can debug errors (seeing logs, extension console).
7. *As a user*, I don’t need to re-login — uses my existing browser session.

---

## 5. Functional Requirements

Each requirement has an ID for traceability.

| ID    | Feature                | Description                                                                  | Inputs / Outputs                                                 | Constraints / Notes                                  |
| ----- | ---------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| FR-1  | Detect Planner context | Extension runs only on Teams / Planner web pages                             | URL match, DOM detection                                         | Manifest host permissions needed                     |
| FR-2  | Get list of plans      | Fetch plans visible to the user                                              | (none) → list of plan IDs, names                                 | Use internal API or wrap DOM / network calls         |
| FR-3  | Get tasks in plan      | Return tasks in a plan (with status, due date, assignees)                    | planId → list of task objects                                    | Might need pagination                                |
| FR-4  | Create task            | Create a new task in a plan / bucket                                         | planId, title, dueDate, assignee, description → task ID / status | Validate inputs; support minimal fields              |
| FR-5  | Update task            | Modify fields, e.g. due date, status, title, assignee                        | taskId, field changes → status                                   | Partial update allowed                               |
| FR-6  | Delete task            | Remove a task                                                                | taskId → confirmation / status                                   | Confirm or require safe deletion                     |
| FR-7  | Error reporting        | Return structured errors                                                     | tool call → error message / code                                 | Provide extension + server error passback            |
| FR-8  | MCP tool interface     | MCP server provides “tools” matching operations (getTasks, createTask, etc.) | MCP tool call → extension invocation → result                    | Use JSON RPC or messaging                            |
| FR-9  | Extension ↔ MCP comms  | Bridge from MCP server to extension and back                                 | messages / transports                                            | Could be WebSocket, local HTTP, or browser messaging |
| FR-10 | Session / auth reuse   | Use the browser’s logged-in session for Planner, not separate login          | None → reuse browser cookies / tokens                            | Must handle token expiration / UI redirection        |
| FR-11 | Safety / confirmation  | For destructive ops (delete), require confirmation (optionally)              | taskId → user confirmation / passback                            | Optional “dry run / preview” mode                    |
| FR-12 | Logging / debug        | Log operations, errors at extension and server                               | timestamp, op, inputs, results                                   | Store to console or local log buffer                 |

---

## 6. Non-Functional Requirements

* **Performance:** Actions must complete within ~3 seconds typically.
* **Reliability:** For 3-4 month lifespan, tolerable occasional breaks but not constant failure.
* **Security / Privacy:** All operations run locally in browser where user is logged in; no external leaking of credentials.
* **Maintainability:** Code should be modular; easy to patch selectors or extension logic.
* **Compatibility:** Chrome / Chromium browsers; manifest v3 extension architecture.
* **Usability:** The AI agent interface should feel seamless; the user gives natural language commands.
* **Observability:** Errors surfaced clearly to user or developer (logs, error messages).

---

## 7. Architecture & System Design

* **Browser extension layer:**

  * Content scripts running on Teams / Planner pages
  * Background script for messaging, command routing
  * Hooks into DOM or intercept network calls
  * Exposes commands (createTask, etc.) via `chrome.runtime.onMessage` or similar

* **MCP server / tool provider layer:**

  * Defines a set of MCP tools (getPlans, getTasks, createTask, updateTask, deleteTask)
  * On tool invocation, it sends a message to the extension (via transport)
  * Waits / receives the response, packages result or error back to agent

* **Transport / communication link:**

  * WebSocket or `chrome.runtime.connect` / message ports
  * May require a local HTTP or WebSocket bridge if extension background ↔ external server

* **AI agent client (Cursor or other):**

  * Uses MCP to call tools
  * The AI “thinking” layer chooses tools based on user prompt

* **Error / fallback path:**

  * If extension fails, MCP server returns meaningful error
  * Potential fallback: prompt user to manually intervene

Diagram (simplified):

```
User prompt → AI → MCP client → MCP server → extension API → browser UI / network → extension returns → MCP server → AI → result
```

---

## 8. Data & State

* **Plan / task objects:** ID, name, description, due date, status, assignees, bucket ID
* **Session state:** which plan is active, last used bucket, mapping of task IDs
* **Error states / logs** stored locally (memory / console)
* **No persistent database** required for MVP

---

## 9. Assumptions & Constraints

* User is already logged into Microsoft Teams / Planner in the browser.
* Planner UI is stable enough for 3-4 months.
* Permissions and CORS allow extension to intercept or wrap calls.
* The extension can access necessary APIs or DOM to perform operations.
* Only one browser instance / profile in use.
* Minimal concurrency / low scale (few operations per session).

---

## 10. Risks & Mitigations

| Risk                                            | Mitigation                                                        |
| ----------------------------------------------- | ----------------------------------------------------------------- |
| UI changes break selectors / network endpoints  | Keep a small selector map, easy to patch; fallback error handling |
| Request failures / network issues               | Retry logic, error back to user / agent                           |
| Permission / security limitations by browser    | Scope extension permissions tightly; test manifest v3 constraints |
| Race conditions (e.g. UI not loaded yet)        | Use wait / retry loops, checks for DOM ready                      |
| Unexpected Planner API changes (Microsoft side) | Monitor changes; limit features to stable ones                    |
| Browser session logout / token expiry           | Detect redirects to login and prompt user to reauthenticate       |

---

## 11. Milestones & Timeline

| Phase                                            | Duration | Deliverables                                        |
| ------------------------------------------------ | -------- | --------------------------------------------------- |
| Phase 1: Setup & scaffolding                     | 1 week   | Extension skeleton + MCP server stub                |
| Phase 2: Read operations (list plans, get tasks) | 1 week   | getPlans + getTasks tool working                    |
| Phase 3: Create / Update operations              | 1 week   | createTask, updateTask, basic fields                |
| Phase 4: Delete / safety / error handling        | 1 week   | deleteTask, confirmation, error reporting           |
| Phase 5: Integration & testing                   | 1 week   | Connect with AI agent, end-to-end tests             |
| Phase 6: Polish & bug fix                        | 1 week   | Logging, minor adjustments, packaging               |
| Total                                            | ~6 weeks | MVP ready within 1.5 months, buffer time for issues |

---

## 12. Success Criteria / Acceptance Tests

* Given a user asks “Create a task in Plan X …”, task appears in Planner UI with correct fields.
* Asking “List tasks in Plan X” returns correct current tasks.
* Asking “Update task Y status to done” changes it in UI.
* Asking “Delete task Y” removes it (or gives confirmation).
* System handles errors gracefully (e.g. invalid plan, missing permission) with clear messages.
* Performance: most operations under ~3s.
* Minimal crashes, extension does not break basic browser behavior.

---

## 13. Future & Extensions

* Support comments, attachments, file upload
* Support multiple users / multi-tenant
* Add UI preview before applying changes
* Add rollback / undo capabilities
* Add support for mobile / Teams desktop app
* Transition to Graph API / full backend integration

---

If you like, I can convert this PRD into a clean markdown or share a downloadable template you can use right away. Do you want me to send that?
