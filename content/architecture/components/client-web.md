---
title: Client Web
---

The Client Web application is the customer-facing website for ticket purchasing.

## Overview

- **Type**: {term}`Client` (Web Application)
- **Repository**: `xbol-web-client`
- **Platform**: React (Single Page Application)
- **Deployment**: Docker container via Docker Compose (static files served via CDN)

## Build & Deployment

```{figure} /diagrams/component-client-web.svg
:name: fig-component-client-web
:width: 100%

Client Web Build & Deployment Pipeline - [View full size](/diagrams/component-client-web.svg)
```

## Role

Provides customers with:

- Event browsing and search
- Interactive seat selection
- Ticket purchasing and checkout
- Order history and ticket management
- Account and notification preferences

## API Integration

Communicates exclusively with {doc}`./client-api` for all backend operations.

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
