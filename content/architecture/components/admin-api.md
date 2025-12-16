---
title: Admin API
---

The Admin API is a Gateway API that serves as the entry point for staff-facing applications.

## Overview

- **Type**: Gateway API
- **Repository**: `xbol-api-admin`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-admin-api.svg
:name: fig-component-admin-api
:width: 100%

Admin API Architecture — [Full size](#appendix-admin-api)
```

## Role

Routes authenticated requests from [](./admin-portal) to Domain APIs:

- [](./ticketing) - Event and seat management
- [](./payments) - Transaction history and refunds
- [](./identity) - User and role management
- [](./notifications) - Notification configuration

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
