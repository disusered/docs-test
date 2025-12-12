---
title: Payments
---

The {term}`Payments` {term}`Service` processes financial transactions and maintains payment records.

## Overview

- **Type**: {term}`Domain API`
- **Repository**: `xbol-api-payments`
- **Platform**: .NET 10 (ASP.NET Core API template)
- **Deployment**: Docker container via Docker Compose

## Backing Services

| Role | Technology | Provider |
|------|------------|----------|
| {term}`Database` | PostgreSQL | AWS RDS |
| {term}`Cache` | Redis | Docker container |
| {term}`Message Broker` | RabbitMQ | Docker container |

## External Providers

| Provider | Service | Purpose |
|----------|---------|---------|
| TBD | Payment Gateway | Credit card processing and payment authorization |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
