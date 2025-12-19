---
title: API de Payments
---

El API de Payments procesa transacciones financieras y mantiene registros de pagos.

## Resumen

- **Tipo**: API de Dominio
- **Repositorio**: `xbol-api-payments`
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-payments.svg
:name: fig-component-payments
:width: 100%

Arquitectura del API de Payments — [Tamaño completo](/diagrams/component-payments.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-payments@4x.png
:name: fig-component-payments-print
:width: 100%

Arquitectura del API de Payments
```

+++

## Servicios de Respaldo

| Rol | Tecnología | Proveedor |
|------|------------|----------|
| Base de Datos | PostgreSQL | AWS RDS |
| Caché | Redis | Contenedor Docker |
| Intermediario de Mensajes | RabbitMQ | Contenedor Docker |

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| TBD | Pasarela de Pagos | Procesamiento de tarjetas de crédito y autorización de pagos |
| Rollbar | Rastreador de Excepciones | Monitoreo de errores y alertas |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de logs y métricas |