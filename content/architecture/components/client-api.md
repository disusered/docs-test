---
title: Client API
---

The Client API is a {term}`Gateway API` that serves as the entry point for customer-facing applications. It manages seat inventory via seats.io and maintains local state for session management.

## Overview

- **Type**: {term}`Gateway API`
- **Repository**: `xbol-api-client`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-client-api.svg
:name: fig-component-client-api
:width: 100%

Client API Architecture - [View full size](/diagrams/component-client-api.svg)
```

## Role

Routes authenticated requests from {term}`Client` applications to Domain APIs:

- {doc}`./ticketing` - Ticket browsing and purchasing
- {doc}`./payments` - Payment processing
- {doc}`./identity` - Authentication and profile
- {doc}`./notifications` - Notification preferences

## Clients Served

- {doc}`./client-web` - Customer web application
- {doc}`./client-mobile` - Customer mobile application

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| seats.io | Seat Reservation | Interactive seating charts and real-time seat availability |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
