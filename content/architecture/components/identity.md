---
title: Identity
---

The Identity Service manages user authentication, authorization, and account information.

## Overview

- **Type**: Domain API
- **Repository**: `xbol-identity-provider`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-identity.svg
:name: fig-component-identity
:width: 100%

Identity API Architecture — [Full size](#appendix-identity)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| Database | PostgreSQL | AWS RDS |
| Cache | Redis | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| TBD | Identity Provider | OAuth/OIDC federation for external authentication |
| Rollbar | Exception Tracker | Error monitoring and alerting |
| AWS CloudWatch | Logging | Centralized log aggregation and metrics |

See [](../index) for service inventory.
