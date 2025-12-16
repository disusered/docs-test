---
title: Notifications
---

The Notifications Service delivers messages to users via email and push notifications.

## Overview

- **Type**: Domain API
- **Repository**: `xbol-api-notifications`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-notifications.svg
:name: fig-component-notifications
:width: 100%

Notifications API Architecture — [Full size](#appendix-notifications)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| Database | PostgreSQL | AWS RDS |
| Message Broker | RabbitMQ | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Mailchimp | Email Provider | Transactional email delivery (confirmations, receipts) |
| TBD | Push Provider | Mobile and web push notification delivery |
| Rollbar | Exception Tracker | Error monitoring and alerting |
| AWS CloudWatch | Logging | Centralized log aggregation and metrics |

See [](../index) for service inventory.
