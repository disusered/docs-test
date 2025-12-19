---
title: Cliente Móvil
---

La aplicación Cliente Móvil es la aplicación móvil orientada al consumidor para la compra de boletos.

## Resumen

- **Tipo**: Cliente (Aplicación Móvil)
- **Repositorio**: `xbol-app-client`
- **Plataforma**: React Native (iOS y Android)
- **Distribución**: App Store (iOS), Google Play (Android)

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-client-mobile.svg
:name: fig-component-client-mobile
:width: 100%

Arquitectura del Cliente Móvil — [Tamaño completo](/diagrams/component-client-mobile.svg)
```

+++

+++ {"class": "no-web"}

```{image} /diagrams/component-client-mobile@4x.png
:width: 100%
```

+++

## Rol

Proporciona a los clientes:

- Consulta y búsqueda de eventos
- Selección interactiva de asientos
- Compra de boletos y proceso de pago
- Boletos móviles con códigos QR
- Soporte para notificaciones push

## Integración con API

Se comunica exclusivamente con [](./client-api) para todas las operaciones de backend.

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| APNs / FCM | Notificaciones Push | Entrega de notificaciones a dispositivos iOS y Android |
| Rollbar | Reportes de Fallos | Monitoreo de errores y alertas de la aplicación móvil |