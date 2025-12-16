---
title: Client Web
---

The Client Web application is the customer-facing website for ticket purchasing.

## Overview

- **Type**: Client (Web Application)
- **Repository**: `xbol-web-client`
- **Platform**: React (Single Page Application)
- **Deployment**: Docker container via Docker Compose (static files served via CDN)

## Architecture

```{figure} /diagrams/component-client-web.svg
:name: fig-component-client-web
:width: 100%

Client Web Architecture — [Full size](#appendix-client-web)
```

## Role

Provides customers with:

- Event browsing and search
- Interactive seat selection
- Ticket purchasing and checkout
- Order history and ticket management
- Account and notification preferences

## API Integration

Communicates exclusively with [](./client-api) for all backend operations.

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Exception Tracker | Client-side error monitoring |

See [](../index) for service inventory.
