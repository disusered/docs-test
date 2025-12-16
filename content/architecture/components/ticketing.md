---
title: Ticketing
---

The Ticketing Service calculates dynamic pricing for events based on demand, inventory, and business rules.

## Overview

- **Type**: Domain API
- **Repository**: `xbol-api-ticketing`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-ticketing.svg
:name: fig-component-ticketing
:width: 100%

Ticketing API Architecture — [Full size](#appendix-ticketing)
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
| seats.io | Seat Inventory | Event seating configuration and real-time availability |
| Rollbar | Exception Tracker | Error monitoring and alerting |
| AWS CloudWatch | Logging | Centralized log aggregation and metrics |

See [](../index) for service inventory.
