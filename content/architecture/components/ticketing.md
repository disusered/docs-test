---
title: Ticketing
---

The {term}`Ticketing` {term}`Service` calculates dynamic pricing for events based on demand, inventory, and business rules.

## Overview

- **Type**: {term}`Domain API`
- **Repository**: `xbol-api-ticketing`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-ticketing.svg
:name: fig-component-ticketing
:width: 100%

Ticketing API Architecture - [View full size](/diagrams/component-ticketing.svg)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |
| {term}`Message Broker` | RabbitMQ | Docker container |

## External Providers

None - pricing calculations are internal. Seat inventory is managed by Gateway APIs via seats.io.

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
