---
title: Cliente Web
---

La aplicación Cliente Web es el sitio web orientado al consumidor para la compra de boletos.

## Resumen

- **Tipo**: Cliente (Aplicación Web)
- **Repositorio**: `xbol-web-client`
- **Plataforma**: React (Aplicación de Página Única)
- **Despliegue**: Contenedor Docker a través de Docker Compose (archivos estáticos servidos vía CDN)

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-client-web.svg
:name: fig-component-client-web
:width: 100%

Arquitectura del Cliente Web — [Tamaño completo](/diagrams/component-client-web.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/component-client-web@4x.png
:name: fig-component-client-web-print
:width: 100%

Arquitectura del Cliente Web
```

+++

## Rol

Proporciona a los clientes:

- Consulta y búsqueda de eventos
- Selección interactiva de asientos
- Compra de boletos y proceso de pago
- Historial de pedidos y gestión de boletos
- Preferencias de cuenta y notificaciones

## Integración con API

Se comunica exclusivamente con [](./client-api) para todas las operaciones de backend.

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| Rollbar | Rastreador de Excepciones | Monitoreo de errores del lado del cliente |