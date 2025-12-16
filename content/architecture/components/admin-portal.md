---
title: Admin Portal
---

The Admin Portal is the staff-facing web application for platform administration.

## Overview

- **Type**: Client (Web Application)
- **Repository**: `xbol-web-admin`
- **Platform**: Blazor Server (.NET 10)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-admin-portal.svg
:name: fig-component-admin-portal
:width: 100%

Admin Portal Architecture — [Full size](#appendix-admin-portal)
```

## Role

Provides staff with tools to:

- Manage events and seating configurations
- Process box office sales
- View transaction history and issue refunds
- Manage users and permissions
- Configure notification templates

## API Integration

Communicates exclusively with [](./admin-api) for all backend operations.

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Exception Tracker | Error monitoring in browser and server |

See [](../index) for service inventory.
