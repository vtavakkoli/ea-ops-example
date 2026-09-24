<p align="center"><img src="docs/assets/ea-ops.svg" width="80" height="80" alt="EA Ops connected architecture icon"></p>

# EA-Ops Reference Architecture — Metroville Digital Permit Service

> A complete, fictional Enterprise Architecture-as-Code example showing how EA-Ops models, validates, reviews, governs, and publishes a cross-layer architecture through Git.

[![EA-Ops](https://img.shields.io/badge/EA--Ops-reference%20example-1f6feb)](https://github.com/vtavakkoli/ea-ops)
[![Model](https://img.shields.io/badge/model-ArchiMate%203.2-5c6ac4)](https://github.com/vtavakkoli/ea-ops)
[![Governance](https://img.shields.io/badge/governance-as%20code-2ea44f)](rules/governance.yaml)

## A workspace for everyday architecture

**Python 3.10+ · PyYAML · YAML models · Vanilla JavaScript · SVG · GitHub Actions**

Find the system you need, see who owns it, inspect its dependencies, and bring a clear shortlist to your next architecture review.

| Everyday task | Where to start |
| --- | --- |
| Find a system or its owner | **Catalog**: search names, IDs, descriptions, and owners |
| Prepare a review | Filter by layer, owner, favorites, or high / critical assets |
| Return to your work | Star objects and use **Recently opened** on the overview |
| Share architecture context | Open an object and choose **Copy direct link** |
| Take a shortlist into a meeting | **Export CSV** exports the current catalog filters |
| Check model health | **Review priorities** and **Governance** |
| Inspect connections | **Explore dependencies**, then choose one to three hops |

Press **/** to focus search, type a query, and press **Enter**. The portal runs without a frontend build step or external JavaScript services. Favorites and recent items stay in this browser; reviewed YAML in Git remains the shared source of truth.

[Read the daily workflow guide](docs/daily-workflow.md).

## Live interactive architecture portal

**https://vtavakkoli.github.io/ea-ops-example/**

The portal behaves like a lightweight EA repository rather than a static documentation page. It includes:

- a searchable process repository with process documentation and interactive architecture diagrams;
- semantic ArchiMate-style shapes for Strategy, Business, Application, Technology/Physical, Motivation, and Implementation & Migration elements;
- a dedicated **Notation** page that previews the supported element and relationship vocabulary;
- an event-driven permit journey using ArchiMate `BusinessEvent` and `BusinessProcess` elements;
- distinct visual cues for message, timer and signal events while preserving the semantic `BusinessEvent` type;
- ArchiMate `Representation` elements for human-readable documents such as application PDFs, receipts and decision letters;
- relationship notation for Composition, Aggregation, Assignment, Realization, Serving, Access, Influence, Triggering, Flow, Specialization and Association;
- Access relationship modes (`read`, `write`, `read-write`) and Influence strength metadata;
- role, application, information and document context for every process;
- information, application, technology, strategy, motivation and implementation repository views;
- an architecture explorer for cross-layer navigation;
- draggable diagram objects with immediate relationship rerouting and browser-local draft persistence;
- **Auto layout**, **Reset to Git**, **Zoom**, **Snap grid**, **Copy layout YAML**, **Download YAML**, and **Edit view in GitHub** controls;
- committed `layout.positions` so curated diagrams remain stable across builds;
- model-quality and governance results from the same validation rules used in CI.

The browser is intentionally not the architecture source of truth. Architects can experiment by dragging elements; EA-Ops autosaves the draft locally and exports exact YAML coordinates. Those coordinates are then committed through the normal Git/pull-request workflow.

## Scenario

**Metroville** is a fictional city replacing fragmented permit channels with one secure digital service. Residents submit applications online, authenticate through a digital identity service, upload evidence, pay fees, receive notifications, and track decisions. Case workers process applications in a governed case-management platform while the architecture team manages change through pull requests.

This repository is intentionally separate from the EA-Ops framework. It demonstrates how a normal organization can consume EA-Ops without embedding its architecture inside the framework repository.

## Event-driven permit journey

```text
✉ Permit Request Received
          │
          ▼
Submit Permit Application
          │
          ▼
⌁ Application Registered
          │
          ▼
Assess Permit Case
          │
          ▼
⌁ Assessment Completed
          │
          ▼
◷ Payment Window Opened
          │
          ▼
Collect Permit Fee
          │
          ▼
✉ Payment Confirmation Received
          │
          ▼
Issue Permit Decision
          │
          ▼
✉ Decision Delivered
```

The process view also places responsible roles above the business flow, supporting applications beneath it, and information/documents on their own lane. The layout is stored in `views/process-landscape.yaml`.

## Relationship semantics in the example

The example deliberately exercises more than simple arrows. `Access` relationships carry presentation metadata showing whether behavior reads, writes or reads/writes passive structure, while `Influence` relationships demonstrate strength labels.

```yaml
- id: rel-assess-case-data
  type: Access
  source: process.assess-case
  target: data.permit-case
  properties: {accessType: read-write}

- id: rel-compliance-audit
  type: Influence
  source: driver.compliance
  target: requirement.auditability
  properties: {strength: "++"}
```

The visual notation is generated from these semantics; it is not stored as a separate drawing.

## Cross-layer architecture

```text
Resident
   │
   ▼
Digital Permit Service
   │
   ├── Citizen Portal ── Identity & Access
   │        │
   │        ▼
   │     API Gateway
   │        │
   │        ▼
   ├── Case Management ── Document Management
   │        │
   │        ├── Payment Platform
   │        └── Notification Service
   │
   └── ITSM + Observability
            │
            ▼
      Resilient Platform
```

The same Git repository contains the business, application, information, technology, motivation, and implementation views needed to explain and govern that service.

## EA-Ops operating loop

```text
Architecture change
       │
       ▼
   Pull Request
       │
       ├── metamodel validation
       ├── relationship validation
       ├── governance rules
       └── impact analysis
       │
       ▼
Architecture review / approval
       │
       ▼
      main
       │
       ├── interactive portal
       ├── architecture views
       └── reports
```

**Git handles collaboration and access. EA-Ops handles architecture semantics and governance.**

## Repository map

```text
eaops.yaml
model/
  business.yaml
  application.yaml
  technology.yaml
  motivation.yaml
  implementation.yaml
relationships/
  relationships.yaml
rules/
  governance.yaml
views/
  process-landscape.yaml
  citizen-service.yaml
  platform.yaml
  resilience.yaml
docs/
  index.html
  architecture-report.md
.github/workflows/
  eaops.yml
```

## Try it

```bash
git clone https://github.com/vtavakkoli/ea-ops-example.git
cd ea-ops-example
python -m pip install "git+https://github.com/vtavakkoli/ea-ops.git"
eaops validate .
eaops summary .
eaops impact . --id app.case-management
eaops report . -o architecture-report.md
eaops build . -o site
```

Open `site/index.html`, choose a process, drag some objects, then use **Copy layout YAML** or **Edit view in GitHub** to persist the refined coordinates in the corresponding view file.

## Architecture goals

The example is designed around five measurable architecture outcomes:

- one coherent digital permit journey for residents;
- strong identity, auditability and data-classification controls;
- clear ownership for every critical process and application;
- observable and resilient runtime services;
- change governed through pull requests rather than disconnected documents.

## Important

Metroville and all architecture objects in this repository are fictional. The model is a teaching/reference architecture and is not intended to represent any real city, authority, vendor environment, or production system.

## Related project

EA-Ops framework: https://github.com/vtavakkoli/ea-ops

## License

Apache License 2.0.
