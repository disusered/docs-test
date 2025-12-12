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

All traffic enters through public domain names that resolve to static IP addresses within the {term}`VPC`. Requests pass through network services ({term}`CDN`, {term}`WAF`, {term}`Load Balancer`) before reaching their destination:

1. **Web Clients**: Browser requests route to Admin Portal or Client Web, which then make API calls
2. **Mobile Clients**: Native apps connect directly to {term}`Gateway API`s through the same network path
3. **On-Premise**: Handheld devices connect to local {term}`Bastion` for offline operation; Bastion syncs with cloud via internet

## Authentication Flow

Gateway APIs (Admin API, Client API) authenticate requests through Identity API, which verifies credentials against the Identity Provider. Gateway APIs then forward authenticated requests to {term}`Domain API`s.

Domain APIs validate JWT tokens or API keys issued by Identity API but do not call Identity API directly on every request. This prevents creating a dependency bottleneck while maintaining security.

## Actors

| Actor       | Description                            |
| ----------- | -------------------------------------- |
| Customer    | Purchases tickets via web or mobile    |
| Admin Staff | Manages platform configuration         |
| Box Office  | Sells tickets on-site via Admin Portal |
| Gate Staff  | Validates tickets using handhelds      |

## Infrastructure

| Component     | Location | Purpose                      |
| ------------- | -------- | ---------------------------- |
| Domain Name   | External | DNS resolution               |
| Static IP     | Cloud    | Fixed VPC entry point        |
| CDN           | Cloud    | Content delivery and caching |
| WAF           | Cloud    | Web application firewall     |
| Load Balancer | Cloud    | Traffic distribution         |

## Systems

### Web Clients

| System       | Location | Purpose                            |
| ------------ | -------- | ---------------------------------- |
| Admin Portal | Cloud    | Staff web interface       |
| Client Web   | Cloud    | Customer ticket purchasing |

### Mobile Clients

| System        | Location   | Purpose                           |
| ------------- | ---------- | --------------------------------- |
| Client Mobile | Cloud      | Customer mobile app |
| Handheld App  | On-premise | QR code scanning    |

### Gateway APIs

| System     | Location | Purpose                       |
| ---------- | -------- | ----------------------------- |
| Admin API  | Cloud    | Gateway for staff operations  |
| Client API | Cloud    | Gateway for customer operations|

### Domain APIs

| System        | Location | Purpose                            |
| ------------- | -------- | ---------------------------------- |
| Ticketing     | Cloud    | Seat reservations                  |
| Payments      | Cloud    | Transaction processing             |
| Identity      | Cloud    | Authentication and user management |
| Notifications | Cloud    | Email and push delivery            |

### On-Premise

| System  | Location   | Purpose                     |
| ------- | ---------- | --------------------------- |
| Bastion | On-premise | Offline validation and sync |

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
