---
title: API de Administración
---

El API de Administración es un Gateway API que sirve como punto de entrada para aplicaciones dirigidas al personal.

## Descripción General

- **Tipo**: Gateway API
- **Repositorio**: `xbol-api-admin`
- **Plataforma**: .NET 10 (plantilla ASP.NET Core API)
- **Despliegue**: Contenedor Docker mediante Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-admin-api.svg
:name: fig-component-admin-api
:width: 100%

Arquitectura del API de Administración — [Tamaño completo](/diagrams/component-admin-api.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-admin-api@4x.png
:name: fig-component-admin-api-print
:width: 100%

Arquitectura del API de Administración
```

+++

## Función

Enruta solicitudes autenticadas desde [](./admin-portal) hacia los Domain APIs:

- [](./ticketing) - Gestión de eventos y asientos
- [](./payments) - Historial de transacciones y reembolsos
- [](./identity) - Gestión de usuarios y roles
- [](./notifications) - Configuración de notificaciones

## Servicios de Respaldo

| Función      | Tecnología | Proveedor         |
|--------------|------------|-------------------|
| Base de Datos| PostgreSQL | AWS RDS           |
| Caché        | Redis      | Contenedor Docker |

## Proveedores Externos

| Proveedor      | Servicio              | Propósito                                       |
|----------------|----------------------|------------------------------------------------|
| Rollbar        | Rastreador de Excepciones | Monitoreo de errores y alertas            |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de registros y métricas |