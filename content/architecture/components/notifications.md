---
title: API de Notifications
---

El API de Notifications entrega mensajes a usuarios a través de correo electrónico y notificaciones push.

## Resumen

- **Tipo**: API de Dominio
- **Repositorio**: `xbol-api-notifications`
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-notifications.svg
:name: fig-component-notifications
:width: 100%

Arquitectura del API de Notifications — [Tamaño completo](/diagrams/component-notifications.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-notifications@4x.png
:name: fig-component-notifications-print
:width: 100%

Arquitectura del API de Notifications
```

+++

## Servicios de Respaldo

| Rol | Tecnología | Proveedor |
|------|------------|----------|
| Base de Datos | PostgreSQL | AWS RDS |
| Intermediario de Mensajes | RabbitMQ | Contenedor Docker |

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| Mailchimp | Proveedor de Email | Entrega de correos transaccionales (confirmaciones, recibos) |
| TBD | Proveedor Push | Entrega de notificaciones push móviles y web |
| Rollbar | Rastreador de Excepciones | Monitoreo de errores y alertas |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de logs y métricas |