---
title: Overview
---

## Architecture Diagrams

| Diagram          | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| [](./context)    | High-level view of actors, systems, and boundaries |
| [](./deployment) | Provider boundaries and technology choices         |

## Architecture Principles

### 1. Gateway API

[](./components/client-api) and [](./components/admin-api) are the primary entry points for front-end applications. These Gateway APIs handle authentication and orchestrate calls to Domain APIs ([](./components/ticketing), [](./components/payments), [](./components/notifications), [](./components/identity)). Domain APIs are not directly consumed by front-ends under normal operation, though they remain independently accessible for internal tooling or future integrations.

### 2. Database Per Service

Each API owns its backing services (Database, Cache, Message Broker). Even when sharing physical infrastructure, services are logically isolated.

### 3. Offline Resilience

The [](./components/bastion) system enables ticket validation when cloud connectivity is unavailable. Staff scan QR codes on tickets or devices using [](./components/handheld) connected to the bastion locally. Validation works offline; data syncs with cloud when connectivity resumes. Web and mobile Client apps require internet connectivity.

### 4. Multi-Channel Messaging

Services send notifications via email and push notifications through a dedicated [](./components/notifications). Additional channels (SMS, etc.) can be added as needed.

### 5. Structured Logging

All processes use structured logging. Logs are written to local text files and persisted to a logging service for long-term storage. IT teams can configure additional sinks as needed.

### 6. Infrastructure Simplicity

Initial deployment runs all services on a single VM with Docker Compose. Cloud-managed networking handles Load Balancer, SSL termination, CDN, WAF, and Static IP allocation. DNS is managed by external domain registrar.

## Service Inventory

The platform comprises the following services:

### Internal Services

#### Gateway APIs

| Component                   | Location | Tech    | Purpose                             |
| --------------------------- | -------- | ------- | ----------------------------------- |
| [](./components/admin-api)  | Cloud    | .NET 10 | Entry point for admin front-ends    |
| [](./components/client-api) | Cloud    | .NET 10 | Entry point for customer front-ends |

#### Domain APIs

| Component                      | Location | Tech    | Purpose                                 |
| ------------------------------ | -------- | ------- | --------------------------------------- |
| [](./components/ticketing)     | Cloud    | .NET 10 | Ticket reservations and seat management |
| [](./components/payments)      | Cloud    | .NET 10 | Payment processing and transaction logs |
| [](./components/identity)      | Cloud    | .NET 10 | Authentication and user management      |
| [](./components/notifications) | Cloud    | .NET 10 | Email and push notification delivery    |

#### Front-Ends

| Component                      | Location   | Tech                       | Purpose                     |
| ------------------------------ | ---------- | -------------------------- | --------------------------- |
| [](./components/admin-portal)  | Cloud      | Blazor                     | Staff administration        |
| [](./components/client-web)    | Cloud      | React                      | Customer ticket purchasing  |
| [](./components/client-mobile) | Cloud      | React Native (Android/iOS) | Customer mobile experience  |
| [](./components/handheld)      | On-Premise | React Native (Android)     | Staff ticket validation     |
| [](./components/bastion)       | On-Premise | .NET 10                    | Offline sync and validation |

### External Services

#### Application Services

| Service Type      | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| Database          | Persistent storage for application data                |
| Cache             | Fast access to session state and frequently-read data  |
| Message Broker    | Asynchronous task processing and event distribution    |
| Email Provider    | Transactional email delivery (confirmations, receipts) |
| Push Provider     | Mobile and web push notification delivery              |
| Payment Gateway   | Credit card processing and payment authorization       |
| Seat Reservation  | Interactive seating charts and real-time availability  |
| Exception Tracker | Error aggregation and alerting                         |
| Logging Service   | Centralized log storage and search                     |

#### Infrastructure Services

| Service Type        | Purpose                                    |
| ------------------- | ------------------------------------------ |
| Load Balancer       | Traffic distribution and SSL termination   |
| Static IP           | Stable public endpoint for DNS             |
| CDN                 | Edge caching and DDoS mitigation           |
| WAF                 | Request filtering and security rules       |
| Certificate Manager | Automated SSL/TLS certificate provisioning |
| VPC                 | Network isolation and security boundaries  |

## Repository Mapping

| Component                      | Repository               |
| ------------------------------ | ------------------------ |
| [](./components/admin-api)     | `xbol-api-admin`         |
| [](./components/client-api)    | `xbol-api-client`        |
| [](./components/ticketing)     | `xbol-api-ticketing`     |
| [](./components/payments)      | `xbol-api-payments`      |
| [](./components/identity)      | `xbol-identity-provider` |
| [](./components/notifications) | `xbol-api-notifications` |
| [](./components/admin-portal)  | `xbol-web-admin`         |
| [](./components/client-web)    | `xbol-web-client`        |
| [](./components/client-mobile) | `xbol-app-client`        |
| [](./components/handheld)      | `xbol-app-handheld`      |
| Documentation                  | `xbol-documents`         |
| [](./components/bastion)       | TBD                      |

## Device Types

See [](./context) for device connectivity.
