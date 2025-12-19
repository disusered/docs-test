---
title: Portal de Administración
---

El Portal de Administración es la aplicación web orientada al personal para la administración de la plataforma.

## Resumen

- **Tipo**: Cliente (Aplicación Web)
- **Repositorio**: `xbol-web-admin`
- **Plataforma**: Blazor WebAssembly (.NET 10)
- **Despliegue**: Contenedor Docker a través de Docker Compose

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-admin-portal.svg
:name: fig-component-admin-portal
:width: 100%

Arquitectura del Portal de Administración — [Tamaño completo](/diagrams/component-admin-portal.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-admin-portal@4x.png
:name: fig-component-admin-portal-print
:width: 100%

Arquitectura del Portal de Administración
```

+++

## Rol

Proporciona al personal herramientas para:

- Gestionar eventos y reservación de asientos
- Procesar ventas y creditos de taquilla
- Consultar historial de transacciones y emitir reembolsos

## Integración con API

Se comunica exclusivamente con [](./admin-api) para todas las operaciones de backend.

## Proveedores Externos

| Proveedor | Servicio                  | Propósito                                    |
| --------- | ------------------------- | -------------------------------------------- |
| Rollbar   | Rastreador de Excepciones | Monitoreo de errores en navegador y servidor |

