---
title: Glossary
label: glossary
---

# Glossary

This glossary provides definitions for key terms used throughout the XBOL documentation. Terms can be referenced from other documents using the `{term}` role.

:::{glossary}
API
: Application Programming Interface. A set of protocols and tools for building software applications.

Bastion
: An on-premise server enabling offline ticket validation when cloud connectivity is unavailable.

CDN
: Content Delivery Network. Caches and serves static content from edge locations near users.

Domain API
: A service responsible for a specific business capability (ticketing, payments, identity, notifications).

Gateway API
: An entry point that routes requests to internal services, handling authentication and orchestration.

Identity
: The service managing user authentication, authorization, and account information.

Load Balancer
: Distributes incoming traffic across multiple servers for reliability and performance.

Message Broker
: Software that enables asynchronous communication between services by routing messages through queues.

Notifications
: The service delivering messages to users via email and push notifications.

On-Premise
: Hardware and software located at the physical venue rather than in cloud data centers.

Payments
: The service processing financial transactions and maintaining payment records.

Static IP
: A fixed public IP address that provides a stable entry point for DNS resolution.

Ticketing
: The service managing ticket inventory, seat reservations, and purchase transactions.

VPC
: Virtual Private Cloud. An isolated network environment within cloud infrastructure.

WAF
: Web Application Firewall. Filters malicious traffic and enforces security rules.

XBOL
: The primary system documented in this technical reference. See architecture section for detailed specifications.

XBOL System
: The complete XBOL solution including all software components, databases, and integrations.
:::

---

:::{tip}
To add new terms, use this format inside the glossary directive:

```
TermName
: Definition of the term.
```

Reference terms in other documents using `` {term}`XBOL` ``.
:::
