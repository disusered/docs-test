---
title: Ticketing
---

The {term}`Ticketing` {term}`Service` manages ticket inventory, seat reservations, and purchase transactions.

## Overview

- **Type**: {term}`Domain API`
- **Repository**: `xbol-api-ticketing`
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
| seats.io | Seat Reservation | Interactive seating charts and real-time availability |

## Detailed Documentation

Coming soon.

See {doc}`../index` for service inventory.
