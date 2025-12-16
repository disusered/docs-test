---
title: Deployment
---

Infrastructure deployment showing provider boundaries, technology choices, and backing services.

```{figure} /diagrams/deployment.svg
:name: fig-deployment
:width: 100%

Deployment Diagram — [Full size](#appendix-deployment)
```

## Provider Boundaries

### Cloudflare

| Service | Purpose |
|-----------------|---------|
| CDN | Edge caching and content delivery |
| WAF | Request filtering and security rules |
| DDoS Protection | Traffic analysis and attack mitigation |

### AWS

| Service | Purpose |
|---------|---------|
| VPC | Network isolation and security boundaries |
| Static IP | Stable public endpoint for DNS |
| Load Balancer (ALB) | Traffic distribution and SSL termination |
| Certificate Manager | Automated SSL/TLS provisioning |
| RDS (PostgreSQL) | Managed Database service |
| CloudWatch | Metrics, logs, and alarms |

### On-Premise

On-Premise systems operate within the venue's local network.

| Component | Platform | Purpose |
|-------------------|------------------|---------|
| [](./components/bastion) | .NET 10 (Docker) | Offline validation and cloud sync |
| [](./components/handheld) | Android | Staff ticket scanning |

## Client Platforms

Client applications run on the following platforms:

| Client | Platforms |
|--------|-----------|
| [](./components/client-mobile) | iOS, Android |
| [](./components/handheld) | Android only |
| [](./components/admin-portal) | Web (any browser) |
| [](./components/client-web) | Web (any browser) |

## Backing Services

Each Domain API owns its backing services (database-per-service pattern):

| API | Database | Cache | Message Broker |
|-------------|----------|---------------|------------------------|
| [](./components/ticketing) | PostgreSQL | Redis | RabbitMQ |
| [](./components/payments) | PostgreSQL | Redis | RabbitMQ |
| [](./components/identity) | PostgreSQL | Redis | - |
| [](./components/notifications) | PostgreSQL | - | RabbitMQ |

## Deployment Model

Initial deployment runs services on a single EC2 instance with Docker Compose:

- **Single VM**: All application containers co-located for simplicity
- **RDS PostgreSQL**: Each service owns its own database; databases can be migrated to separate RDS instances for scaling
- **Per-Service Redis**: Each service runs its own Redis container, isolated through Docker Compose
- **Per-Service RabbitMQ**: Each service runs its own RabbitMQ container, isolated through Docker Compose

This model supports horizontal scaling by extracting services to dedicated hosts or promoting databases to dedicated RDS instances.
