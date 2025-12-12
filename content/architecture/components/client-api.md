---
title: Client API
---

The Client API is a {term}`Gateway API` that serves as the entry point for customer-facing applications.

## Overview

- **Type**: {term}`Gateway API`
- **Repository**: `xbol-api-client`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Role

Routes authenticated requests from {term}`Client` applications to Domain APIs:

- {doc}`./ticketing` - Ticket browsing and purchasing
- {doc}`./payments` - Payment processing
- {doc}`./identity` - Authentication and profile
- {doc}`./notifications` - Notification preferences

## Clients Served

- {doc}`./client-web` - Customer web application
- {doc}`./client-mobile` - Customer mobile application

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |

## External Providers

None directly - orchestrates calls to Domain APIs which connect to external providers.

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
