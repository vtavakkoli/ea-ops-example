# Metroville Digital Permit Service — Architecture Brief

> **Reference architecture:** fictional smart-city digital permit service  
> **Governance model:** EA-Ops / Git-native architecture operations  
> **Metamodel:** ArchiMate 3.2 starter profile

## Executive summary

Metroville's reference architecture shows how a public digital service can be modeled and governed from one Git repository. The business journey, applications, information assets, platform services, architecture drivers, requirements and modernization work package share stable IDs and explicit relationships. Pull requests are the architecture change mechanism; deterministic EA-Ops rules are the architecture gate.

The current model contains **56 architecture objects**, **74 explicit relationships**, **3 curated architecture views**, and **8 governance rules**. All modeled objects include an accountable owner and a description, allowing the repository to be used as both a machine-readable graph and a human-readable architecture catalog.

## Architecture health

| Measure | Reference value |
| --- | ---: |
| Architecture objects | 56 |
| Relationships | 74 |
| Views | 3 |
| Governance rules | 8 |
| Ownership coverage | 100% |
| Description coverage | 100% |
| Critical processes with modeled support | 100% |

## Business architecture

The resident journey is represented as a value stream and a sequence of governed business processes:

**Submit Permit Application → Assess Permit Case → Collect Permit Fee → Issue Permit Decision**

The architecture also models two operational processes that keep the service sustainable: **Manage Digital Service Incident** and **Govern Service Change**. Four strategic capabilities anchor the design: digital public service delivery, case management, secure digital identity, and operational resilience.

## Application and information architecture

The target service is intentionally modular. A Citizen Service Portal and Permit Case Management system realize the Digital Permit Service. Identity, API management, documents, payments, notifications, ITSM and observability are modeled as separate application components with explicit ownership and lifecycle metadata.

Three governed data objects demonstrate information accountability: Citizen Profile, Permit Case Record, and Architecture & Service Audit Event. Each includes a data owner and classification so data governance can be validated in CI rather than left as prose.

## Technology architecture

The reference runtime separates application concerns from reusable platform services. Managed container runtime, database, event messaging, and monitoring services support the application layer. Nodes and system software remain visible so impact analysis can traverse from a technology change to affected applications and then to critical business processes.

## Motivation and controls

The model explains *why* the architecture exists. Digital-first service delivery and regulatory accountability influence measurable goals and requirements. End-to-end auditability, high availability, and controlled data residency are first-class architecture objects linked to the implementation rather than isolated statements in a document.

## Change governance

EA-Ops treats a pull request as an architecture change request:

1. edit YAML architecture facts;
2. open a pull request;
3. run metamodel and relationship validation;
4. run organization governance rules;
5. review impact and ownership;
6. approve and merge;
7. regenerate architecture reports and the browser.

This approach deliberately reuses Git for identity, access, history, review and approvals while EA-Ops focuses on architecture semantics.

## Example impact question

A change to `app.case-management` can be traversed through its relationships to identify the processes it supports, data it touches, integrations around it, technology services beneath it, and related service objectives. This is the practical value of keeping architecture relationships in the same version-controlled graph as the objects themselves.

## Governance rules demonstrated

The example includes rules requiring:

- process ownership, lifecycle and criticality;
- application ownership, lifecycle and service tier;
- an incoming `Serving` relationship for every critical process;
- data ownership and information classification;
- technology-service ownership and lifecycle;
- business-service ownership;
- requirement ownership and priority;
- work-package ownership and lifecycle.

## Disclaimer

Metroville is fictional. The example exists to demonstrate EA-Ops concepts and does not describe the architecture of any real municipality or organization.
