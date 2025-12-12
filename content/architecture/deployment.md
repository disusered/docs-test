---
title: Deployment
---

Infrastructure deployment showing provider boundaries, technology choices, and backing services.

```{figure} /diagrams/deployment.svg
:name: fig-deployment
:width: 100%

Deployment Diagram - [View full size](/diagrams/deployment.svg)
```

## Provider Boundaries

### Cloudflare

| {term}`Service` | Purpose |
|-----------------|---------|
| {term}`CDN` | Edge caching and content delivery |
| {term}`WAF` | Request filtering and security rules |
| DDoS Protection | Traffic analysis and attack mitigation |

### AWS

| Service | Purpose |
|---------|---------|
| {term}`VPC` | Network isolation and security boundaries |
| {term}`Static IP` | Stable public endpoint for DNS |
| {term}`Load Balancer` (ALB) | Traffic distribution and SSL termination |
| Certificate Manager | Automated SSL/TLS provisioning |
| RDS (PostgreSQL) | Managed {term}`Database` service |
| CloudWatch | Metrics, logs, and alarms |

### On-Premise

{term}`On-Premise` systems operate within the venue's local network.

| {term}`Component` | {term}`Platform` | Purpose |
|-------------------|------------------|---------|
| {doc}`./components/bastion` | .NET 10 (Docker) | Offline validation and cloud sync |
| {doc}`./components/handheld` | Android | Staff ticket scanning |

## Client Platforms

{term}`Client` applications run on the following platforms:

| Client | Platforms |
|--------|-----------|
| {doc}`./components/client-mobile` | iOS, Android |
| {doc}`./components/handheld` | Android only |
| {doc}`./components/admin-portal` | Web (any browser) |
| {doc}`./components/client-web` | Web (any browser) |

## Backing Services

Each {term}`Domain API` owns its backing services (database-per-service pattern):

| {term}`API` | Database | {term}`Cache` | {term}`Message Broker` |
|-------------|----------|---------------|------------------------|
| {doc}`./components/ticketing` | PostgreSQL | Redis | RabbitMQ |
| {doc}`./components/payments` | PostgreSQL | Redis | RabbitMQ |
| {doc}`./components/identity` | PostgreSQL | Redis | - |
| {doc}`./components/notifications` | PostgreSQL | - | RabbitMQ |

## Deployment Model

Initial deployment runs services on a single EC2 instance with Docker Compose:

- **Single VM**: All application containers co-located for simplicity
- **RDS PostgreSQL**: Each service owns its own database; databases can be migrated to separate RDS instances for scaling
- **Per-Service Redis**: Each service runs its own Redis container, isolated through Docker Compose
- **Per-Service RabbitMQ**: Each service runs its own RabbitMQ container, isolated through Docker Compose

This model supports horizontal scaling by extracting services to dedicated hosts or promoting databases to dedicated RDS instances.
