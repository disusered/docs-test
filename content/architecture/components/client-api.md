---
title: API de Cliente
---

El API de Cliente es un Gateway API que sirve como punto de entrada para las aplicaciones orientadas al consumidor.

## Resumen

- **Tipo**: Gateway API
- **Repositorio**: `xbol-api-client`
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-client-api.svg
:name: fig-component-client-api
:width: 100%

Arquitectura del API de Cliente — [Tamaño completo](/diagrams/component-client-api.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-client-api@4x.png
:name: fig-component-client-api-print
:width: 100%

Arquitectura del API de Cliente
```

+++

## Rol

Enruta solicitudes autenticadas desde aplicaciones de Cliente hacia APIs de Dominio:

- [](./ticketing) - Consulta y compra de boletos
- [](./payments) - Procesamiento de pagos
- [](./identity) - Autenticación y perfil
- [](./notifications) - Preferencias de notificaciones

## Clientes Atendidos

- [](./client-web) - Aplicación web para clientes
- [](./client-mobile) - Aplicación móvil para clientes

## Servicios de Respaldo

| Rol | Tecnología | Proveedor |
|------|------------|----------|
| Base de Datos | PostgreSQL | AWS RDS |
| Caché | Redis | Contenedor Docker |

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| Rollbar | Rastreador de Excepciones | Monitoreo de errores y alertas |
| AWS CloudWatch | Servicio de Registro | Agregación centralizada de logs y métricas |