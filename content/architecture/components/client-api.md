---
title: Client API
---

The Client API is a Gateway API that serves as the entry point for customer-facing applications.

## Overview

- **Type**: Gateway API
- **Repository**: `xbol-api-client`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-client-api.svg
:name: fig-component-client-api
:width: 100%

Client API Architecture — [Full size](#appendix-client-api)
```

## Role

Routes authenticated requests from Client applications to Domain APIs:

- [](./ticketing) - Ticket browsing and purchasing
- [](./payments) - Payment processing
- [](./identity) - Authentication and profile
- [](./notifications) - Notification preferences

## Clients Served

- [](./client-web) - Customer web application
- [](./client-mobile) - Customer mobile application

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| Database | PostgreSQL | AWS RDS |
| Cache | Redis | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Exception Tracker | Error monitoring and alerting |
| AWS CloudWatch | Logging | Centralized log aggregation and metrics |

See [](../index) for service inventory.
