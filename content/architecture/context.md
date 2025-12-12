---
title: Context
---

High-level view showing actors, system boundaries, and how users interact with the platform.

```{figure} /diagrams/context.svg
:name: fig-context
:width: 100%

System Context Diagram - [View full size](/diagrams/context.svg)
```

## Network Flow

All traffic enters through public domain names that resolve to {term}`Static IP` addresses within the {term}`VPC`. Requests pass through network services ({term}`CDN`, {term}`WAF`, {term}`Load Balancer`) before reaching their destination:

1. **Web Clients**: Browser requests route to {doc}`./components/admin-portal` or {doc}`./components/client-web`, which then make {term}`API` calls
2. **Mobile Clients**: Native apps connect directly to Gateway APIs through the same network path
3. **{term}`On-Premise`**: {doc}`./components/handheld` devices connect to local {doc}`./components/bastion` for offline operation; Bastion syncs with cloud via internet

## Authentication Flow

Gateway APIs ({doc}`./components/admin-api`, {doc}`./components/client-api`) authenticate requests through {doc}`./components/identity`, which verifies credentials against the Identity Provider. Gateway APIs then forward authenticated requests to Domain APIs.

Domain APIs validate JWT tokens or API keys issued by Identity API but do not call Identity API directly on every request. This prevents creating a dependency bottleneck while maintaining security.

## Actors

| Actor       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| Customer    | Purchases tickets via web or mobile                             |
| Admin Staff | Manages {term}`Platform` configuration                          |
| Box Office  | Sells tickets on-site via {doc}`./components/admin-portal`      |
| Gate Staff  | Validates tickets using {doc}`./components/handheld` devices    |

## Infrastructure

| {term}`Component` | Location | Purpose                      |
| ----------------- | -------- | ---------------------------- |
| Domain Name       | External | DNS resolution               |
| Static IP         | Cloud    | Fixed VPC entry point        |
| CDN               | Cloud    | Content delivery and caching |
| WAF               | Cloud    | Web application firewall     |
| Load Balancer     | Cloud    | Traffic distribution         |

## Systems

### Web Clients

| System                                  | Location | Purpose                  |
| --------------------------------------- | -------- | ------------------------ |
| {doc}`./components/admin-portal`        | Cloud    | Staff web interface      |
| {doc}`./components/client-web`          | Cloud    | Customer ticket purchasing |

### Mobile Clients

| System                                  | Location   | Purpose             |
| --------------------------------------- | ---------- | ------------------- |
| {doc}`./components/client-mobile`       | Cloud      | Customer mobile app |
| {doc}`./components/handheld`            | On-Premise | QR code scanning    |

### Gateway APIs

| System                                  | Location | Purpose                        |
| --------------------------------------- | -------- | ------------------------------ |
| {doc}`./components/admin-api`           | Cloud    | Gateway for staff operations   |
| {doc}`./components/client-api`          | Cloud    | Gateway for customer operations |

### Domain APIs

| System                                  | Location | Purpose                            |
| --------------------------------------- | -------- | ---------------------------------- |
| {doc}`./components/ticketing`           | Cloud    | Seat reservations                  |
| {doc}`./components/payments`            | Cloud    | Transaction processing             |
| {doc}`./components/identity`            | Cloud    | Authentication and user management |
| {doc}`./components/notifications`       | Cloud    | Email and push delivery            |

### On-Premise

| System                                  | Location   | Purpose                     |
| --------------------------------------- | ---------- | --------------------------- |
| {doc}`./components/bastion`             | On-Premise | Offline validation and sync |

## External Services

| Service           | Purpose                       |
| ----------------- | ----------------------------- |
| Payment Gateway   | Transaction processing        |
| Seat Reservation  | Seat mapping and availability |
| Email Provider    | Transactional email delivery  |
| Push Provider     | Mobile push notifications     |
| Identity Provider | OAuth/OIDC authentication     |
| Exception Tracker | Error monitoring and alerting |
| Logging Service   | Centralized log aggregation   |
