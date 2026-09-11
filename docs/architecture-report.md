# Metroville Digital Permit Service — Architecture Report

## Executive Summary

- Quality score: **100/100**
- Architecture objects: **56**
- Relationships: **73**
- Business processes: **6**
- Data / business objects: **6**
- Applications: **9**
- Ownership coverage: **100.0%**
- Documentation coverage: **100.0%**
- Validation: **0 errors**, **0 warnings**

## Process Repository

| Process | Owner | Criticality | Lifecycle | Supporting applications | Data used |
|---|---|---|---|---:|---:|
| Assess Permit Case | Service Operations | critical | active | 1 | 2 |
| Collect Permit Fee | Finance Services | high | active | 1 | 1 |
| Govern Service Change | Enterprise Architecture | high | active | 1 | 0 |
| Issue Permit Decision | Service Operations | critical | active | 2 | 1 |
| Manage Digital Service Incident | IT Operations | critical | active | 2 | 1 |
| Submit Permit Application | Digital Services | critical | active | 2 | 2 |

## Data & Information Repository

| Information object | Type | Owner | Classification | Process usage |
|---|---|---|---|---:|
| Architecture & Service Audit Event | DataObject | Security Governance | restricted | 1 |
| Citizen Profile | DataObject | Data Governance | confidential | 1 |
| Payment Receipt | BusinessObject | Finance Services | internal | 1 |
| Permit Application | BusinessObject | Service Operations | confidential | 2 |
| Permit Case Record | DataObject | Service Data Owner | confidential | 1 |
| Permit Decision | BusinessObject | Service Operations | confidential | 1 |

## Application Portfolio

| Application | Owner | Lifecycle | Tier | Processes supported |
|---|---|---|---|---:|
| API Gateway | Integration Platform | strategic | tier-1 | 0 |
| Citizen Service Portal | Digital Platforms | strategic | tier-1 | 1 |
| Digital Identity & Access | Identity & Security | strategic | tier-1 | 0 |
| Document Management | Enterprise Content | strategic | tier-1 | 0 |
| IT Service Management | IT Operations | strategic | tier-1 | 2 |
| Notification Service | Digital Platforms | strategic | tier-2 | 1 |
| Observability Platform | Platform Engineering | strategic | tier-1 | 1 |
| Payment Platform | Finance Technology | strategic | tier-1 | 1 |
| Permit Case Management | Business Applications | strategic | tier-1 | 2 |

## Catalog by Type

| Type | Count |
|---|---:|
| ApplicationComponent | 9 |
| ApplicationService | 2 |
| Assessment | 1 |
| BusinessActor | 2 |
| BusinessObject | 3 |
| BusinessProcess | 6 |
| BusinessRole | 3 |
| BusinessService | 1 |
| Capability | 4 |
| Constraint | 1 |
| DataObject | 3 |
| Deliverable | 2 |
| Driver | 2 |
| Gap | 1 |
| Goal | 2 |
| Node | 2 |
| Plateau | 1 |
| Requirement | 2 |
| Stakeholder | 2 |
| SystemSoftware | 1 |
| TechnologyService | 4 |
| ValueStream | 1 |
| WorkPackage | 1 |

## Validation Findings

| Severity | Rule | Object | Finding |
|---|---|---|---|
| pass | MODEL_VALID | — | No validation findings |

## Governance Statement

`main` represents the approved architecture. Proposed changes are reviewed as pull requests, validated by EA-Ops, and published as an interactive repository portal.

The HTML portal provides process drill-down diagrams, information-asset views, application and technology context, relationship navigation, global exploration, and governance results from the same source model.
