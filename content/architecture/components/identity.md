---
title: API de Identity
---

El API de Identity gestiona la autenticación, autorización e información de cuentas de usuario.

## Resumen

- **Tipo**: API de Dominio
- **Repositorio**: `xbol-identity-provider`
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-identity.svg
:name: fig-component-identity
:width: 100%

Arquitectura del API de Identity — [Tamaño completo](/diagrams/component-identity.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-identity@4x.png
:name: fig-component-identity-print
:width: 100%

Arquitectura del API de Identity
```

+++

## Servicios de Respaldo

| Rol | Tecnología | Proveedor |
|------|------------|----------|
| Base de Datos | PostgreSQL | AWS RDS |
| Caché | Redis | Contenedor Docker |

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| TBD | Proveedor de Identidad | Federación OAuth/OIDC para autenticación externa |
| Rollbar | Rastreador de Excepciones | Monitoreo de errores y alertas |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de logs y métricas |