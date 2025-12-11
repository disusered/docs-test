---
title: Overview
---

## Architecture Diagrams

| Diagram                 | Level      | Purpose                                            |
| ----------------------- | ---------- | -------------------------------------------------- |
| {doc}`./context`        | C4 Level 1 | High-level view of actors, systems, and boundaries |
| {doc}`./cloud`          | C4 Level 2 | Cloud services with backing service dependencies   |
| {doc}`./onprem`         | C4 Level 2 | On-premise infrastructure for offline resilience   |
| {doc}`./messaging`      | C4 Dynamic | Multi-channel messaging and async data flows       |
| {doc}`./infrastructure` | C4 Level 2 | AWS infrastructure, compute, and scaling path      |

## Architecture Principles

### 1. Gateway API

Client API and Admin API are the primary entry points for front-end applications. These gateway APIs handle authentication and orchestrate calls to domain APIs (Ticketing, Payments, Notifications, Identity). Domain APIs are not directly consumed by front-ends under normal operation, though they remain independently accessible for internal tooling or future integrations.

### 2. Database Per Service

Each API owns its backing services (database, cache, message broker). Even when sharing physical infrastructure, services are logically isolated.

### 3. Offline Resilience

The bastion system enables ticket validation when cloud connectivity is unavailable. Staff scan QR codes on tickets or devices using handhelds connected to the bastion locally. Validation works offline; data syncs with cloud when connectivity resumes. Web and mobile client apps require internet connectivity.

### 4. Multi-Channel Messaging

Services send notifications via email and push notifications through a dedicated Notifications API. Additional channels (SMS, etc.) can be added as needed.

### 5. Structured Logging

All processes use structured logging. Logs are written to local text files and persisted to a logging service for long-term storage. IT teams can configure additional sinks as needed.

### 6. Infrastructure Simplicity

Initial deployment runs all services on a single VM with Docker Compose. Cloud-managed networking handles load balancing, SSL termination, CDN, WAF, and static IP allocation. DNS is managed by external domain registrar.

## Service Inventory

### Internal Services

#### Gateway APIs

| Service    | Location | Tech    | Purpose                             |
| ---------- | -------- | ------- | ----------------------------------- |
| Admin API  | Cloud    | .NET 10 | Entry point for admin front-ends    |
| Client API | Cloud    | .NET 10 | Entry point for customer front-ends |

#### Domain APIs

| Service           | Location | Tech    | Purpose                                 |
| ----------------- | -------- | ------- | --------------------------------------- |
| Ticketing API     | Cloud    | .NET 10 | Ticket reservations and seat management |
| Payments API      | Cloud    | .NET 10 | Payment processing and transaction logs |
| Identity API      | Cloud    | .NET 10 | Authentication and user management      |
| Notifications API | Cloud    | .NET 10 | Email and push notification delivery    |

#### Front-Ends

| Service           | Location   | Tech                       | Purpose                     |
| ----------------- | ---------- | -------------------------- | --------------------------- |
| Admin Portal      | Cloud      | Blazor                     | Staff administration        |
| Client Web App    | Cloud      | React                      | Customer ticket purchasing  |
| Client Mobile App | Cloud      | React Native (Android/iOS) | Customer mobile experience  |
| Handheld App      | On-premise | React Native (Android)     | Staff ticket validation     |
| Bastion           | On-premise | .NET 10                    | Offline sync and validation |

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

| Service           | Repository               |
| ----------------- | ------------------------ |
| Admin API         | `xbol-api-admin`         |
| Client API        | `xbol-api-client`        |
| Ticketing API     | `xbol-api-ticketing`     |
| Payments API      | `xbol-api-payments`      |
| Identity API      | `xbol-identity-provider` |
| Notifications API | `xbol-api-notifications` |
| Admin Portal      | `xbol-web-admin`         |
| Client Web App    | `xbol-web-client`        |
| Client Mobile App | `xbol-app-client`        |
| Handheld App      | `xbol-app-handheld`      |
| Documentation     | `xbol-documents`         |
| Bastion           | TBD                      |

## Device Types

See {doc}`./context` for device connectivity.
