---
title: Payments
---

The Payments Service processes financial transactions and maintains payment records.

## Overview

- **Type**: Domain API
- **Repository**: `xbol-api-payments`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-payments.svg
:name: fig-component-payments
:width: 100%

Payments API Architecture — [Full size](#appendix-payments)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| Database | PostgreSQL | AWS RDS |
| Cache | Redis | Docker container |
| Message Broker | RabbitMQ | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| TBD | Payment Gateway | Credit card processing and payment authorization |
| Rollbar | Exception Tracker | Error monitoring and alerting |
| AWS CloudWatch | Logging | Centralized log aggregation and metrics |

See [](../index) for service inventory.
