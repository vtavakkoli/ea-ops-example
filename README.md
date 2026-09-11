# EA-Ops Reference Architecture — Metroville Digital Permit Service

> A complete, fictional Enterprise Architecture-as-Code example showing how EA-Ops models, validates, reviews, governs, and publishes a cross-layer architecture through Git.

[![EA-Ops](https://img.shields.io/badge/EA--Ops-reference%20example-1f6feb)](https://github.com/vtavakkoli/ea-ops)
[![Model](https://img.shields.io/badge/model-ArchiMate%203.2-5c6ac4)](https://github.com/vtavakkoli/ea-ops)
[![Governance](https://img.shields.io/badge/governance-as%20code-2ea44f)](rules/governance.yaml)

## Live interactive architecture portal

**https://vtavakkoli.github.io/ea-ops-example/**

The portal behaves like a lightweight EA repository rather than a static documentation page. It includes:

- a searchable process repository with process documentation and interactive architecture diagrams;
- an event-driven permit journey using ArchiMate `BusinessEvent` and `BusinessProcess` elements;
- distinct visual cues for message, timer and signal events while preserving the semantic `BusinessEvent` type;
- ArchiMate `Representation` elements for human-readable documents such as application PDFs, receipts and decision letters;
- role, application, information and document context for every process;
- data/information, application and technology portfolio views;
- draggable diagram objects with browser-local draft persistence;
- **Auto layout**, **Reset to Git**, **Copy layout YAML** and **Download YAML** controls;
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

Open `site/index.html`, choose a process, drag some objects, then use **Copy layout YAML** or **Download YAML** to persist the refined coordinates in the corresponding view file.

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
