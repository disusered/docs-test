---
title: Admin API
---

The Admin API is a {term}`Gateway API` that serves as the entry point for staff-facing applications. It manages seat inventory and event configuration via seats.io, and maintains local state for administrative workflows.

## Overview

- **Type**: {term}`Gateway API`
- **Repository**: `xbol-api-admin`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-admin-api.svg
:name: fig-component-admin-api
:width: 100%

Admin API Architecture - [View full size](/diagrams/component-admin-api.svg)
```

## Role

Routes authenticated requests from {doc}`./admin-portal` to Domain APIs:

- {doc}`./ticketing` - Event and seat management
- {doc}`./payments` - Transaction history and refunds
- {doc}`./identity` - User and role management
- {doc}`./notifications` - Notification configuration

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| seats.io | Seat Reservation | Event seating configuration and seat inventory management |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
