---
title: API de Ticketing
---

El API de Ticketing calcula precios dinámicos para eventos basándose en demanda, inventario y reglas de negocio.

## Resumen

- **Tipo**: API de Dominio
- **Repositorio**: `xbol-api-ticketing`
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-ticketing.svg
:name: fig-component-ticketing
:width: 100%

Arquitectura del API de Ticketing — [Tamaño completo](/diagrams/component-ticketing.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-ticketing@4x.png
:name: fig-component-ticketing-print
:width: 100%

Arquitectura del API de Ticketing
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
| seats.io | Inventario de Asientos | Configuración de asientos de eventos y disponibilidad en tiempo real |
| Rollbar | Rastreador de Excepciones | Monitoreo de errores y alertas |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de logs y métricas |