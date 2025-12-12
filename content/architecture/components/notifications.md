---
title: Notifications
---

The {term}`Notifications` {term}`Service` delivers messages to users via email and push notifications.

## Overview

- **Type**: {term}`Domain API`
- **Repository**: `xbol-api-notifications`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-notifications.svg
:name: fig-component-notifications
:width: 100%

Notifications API Architecture - [View full size](/diagrams/component-notifications.svg)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Message Broker` | RabbitMQ | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| TBD | Email Provider | Transactional email delivery (confirmations, receipts) |
| TBD | Push Provider | Mobile and web push notification delivery |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
