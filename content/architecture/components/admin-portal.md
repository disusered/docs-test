---
title: Admin Portal
---

The Admin Portal is the staff-facing web application for platform administration.

## Overview

- **Type**: {term}`Client` (Web Application)
- **Repository**: `xbol-web-admin`
- **Platform**: Blazor Server (.NET 10)
- **Deployment**: Docker container via Docker Compose

## Build & Deployment

```{figure} /diagrams/component-admin-portal.svg
:name: fig-component-admin-portal
:width: 100%

Admin Portal Build & Deployment Pipeline - [View full size](/diagrams/component-admin-portal.svg)
```

## Role

Provides staff with tools to:

- Manage events and seating configurations
- Process box office sales
- View transaction history and issue refunds
- Manage users and permissions
- Configure notification templates

## API Integration

Communicates exclusively with {doc}`./admin-api` for all backend operations.

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
