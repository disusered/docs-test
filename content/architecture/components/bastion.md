---
title: Bastion
---

The Bastion is an On-Premise server enabling offline ticket validation when cloud connectivity is unavailable.

## Overview

- **Type**: Domain API (On-Premise)
- **Repository**: TBD
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose (on venue hardware)

## Role

- Provides offline ticket validation for [](./handheld) devices
- Caches ticket data from cloud for offline access
- Syncs validation logs to cloud when connectivity resumes

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| Database | SQLite | Local file |
| Cache | In-memory | Application |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Exception Tracker | Error monitoring and alerting |

## Network

- **LAN**: Serves [](./handheld) devices over local network
- **Internet**: Syncs with cloud Gateway APIs when available

See [](../index) for service inventory.
