---
title: Bastion
---

The {term}`Bastion` is an {term}`On-Premise` server enabling offline ticket validation when cloud connectivity is unavailable.

## Overview

- **Type**: {term}`Domain API` ({term}`On-Premise`)
- **Repository**: TBD
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose (on venue hardware)

## Role

- Provides offline ticket validation for {doc}`./handheld` devices
- Caches ticket data from cloud for offline access
- Syncs validation logs to cloud when connectivity resumes

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | SQLite | Local file |
| {term}`Cache` | In-memory | Application |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| Rollbar | Exception Tracker | Error monitoring and alerting |

## Network

- **LAN**: Serves {doc}`./handheld` devices over local network
- **Internet**: Syncs with cloud Gateway APIs when available

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
