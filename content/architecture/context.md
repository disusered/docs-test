---
title: Context
---

High-level view showing actors, system boundaries, and how users interact with the platform.

```{figure} /diagrams/context.svg
:name: fig-context
:width: 100%

System Context Diagram — [Full size](#appendix-context)
```

## Network Flow

All traffic enters through public domain names that resolve to Static IP addresses within the VPC. Requests pass through network services (CDN, WAF, Load Balancer) before reaching their destination:

1. **Web Clients**: Browser requests route to [](./components/admin-portal) or [](./components/client-web), which then make API calls
2. **Mobile Clients**: Native apps connect directly to Gateway APIs through the same network path
3. **On-Premise**: [](./components/handheld) devices connect to local [](./components/bastion) for offline operation; Bastion syncs with cloud via internet

## Authentication Flow

Gateway APIs ([](./components/admin-api), [](./components/client-api)) authenticate requests through [](./components/identity), which verifies credentials against the Identity Provider. Gateway APIs then forward authenticated requests to Domain APIs.

Domain APIs validate JWT tokens or API keys issued by Identity API but do not call Identity API directly on every request. This prevents creating a dependency bottleneck while maintaining security.

## Actors

| Actor       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| Customer    | Purchases tickets via web or mobile                             |
| Admin Staff | Manages Platform configuration                          |
| Box Office  | Sells tickets on-site via [](./components/admin-portal)      |
| Gate Staff  | Validates tickets using [](./components/handheld) devices    |

## Infrastructure

| Component | Location | Purpose                      |
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
| [](./components/admin-portal)        | Cloud    | Staff web interface      |
| [](./components/client-web)          | Cloud    | Customer ticket purchasing |

### Mobile Clients

| System                                  | Location   | Purpose             |
| --------------------------------------- | ---------- | ------------------- |
| [](./components/client-mobile)       | Cloud      | Customer mobile app |
| [](./components/handheld)            | On-Premise | QR code scanning    |

### Gateway APIs

| System                                  | Location | Purpose                        |
| --------------------------------------- | -------- | ------------------------------ |
| [](./components/admin-api)           | Cloud    | Gateway for staff operations   |
| [](./components/client-api)          | Cloud    | Gateway for customer operations |

### Domain APIs

| System                                  | Location | Purpose                            |
| --------------------------------------- | -------- | ---------------------------------- |
| [](./components/ticketing)           | Cloud    | Seat reservations                  |
| [](./components/payments)            | Cloud    | Transaction processing             |
| [](./components/identity)            | Cloud    | Authentication and user management |
| [](./components/notifications)       | Cloud    | Email and push delivery            |

### On-Premise

| System                                  | Location   | Purpose                     |
| --------------------------------------- | ---------- | --------------------------- |
| [](./components/bastion)             | On-Premise | Offline validation and sync |

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
