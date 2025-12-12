---
title: Identity
---

The {term}`Identity` {term}`Service` manages user authentication, authorization, and account information.

## Overview

- **Type**: {term}`Domain API`
- **Repository**: `xbol-identity-provider`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Architecture

```{figure} /diagrams/component-identity.svg
:name: fig-component-identity
:width: 100%

Identity API Architecture - [View full size](/diagrams/component-identity.svg)
```

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| TBD | Identity Provider | OAuth/OIDC federation for external authentication |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
