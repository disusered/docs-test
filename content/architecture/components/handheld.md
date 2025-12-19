---
title: Cliente Handheld
---

El Cliente Handheld es la aplicación móvil orientada al personal para la validación de boletos en las puertas del recinto.

## Resumen

- **Tipo**: Cliente (Aplicación Móvil)
- **Repositorio**: `xbol-app-handheld`
- **Plataforma**: Kotlin (Android)
- **Distribución**: APK de instalación directa (no disponible en tiendas de aplicaciones)

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-handheld.svg
:name: fig-component-handheld
:width: 100%

Arquitectura del Cliente Handheld — [Tamaño completo](/diagrams/component-handheld.svg)
```

+++

+++ {"class": "no-web"}

```{image} /diagrams/component-handheld@4x.png
:width: 100%
```

+++

## Rol

Proporciona al personal de puertas:

- Escaneo de códigos QR para validación de boletos
- Validación offline mediante conexión a [](./bastion)
- Registro de entradas y estadísticas

## Modo de Red

### Modo Online

Se conecta a [](./admin-api) a través de internet para validación en tiempo real.

### Modo Offline

Se conecta a [](./bastion) local a través de LAN cuando internet no está disponible. Los datos de validación se sincronizan a la nube cuando se restablece la conectividad.

## Proveedores Externos

| Proveedor | Servicio | Propósito |
|----------|---------|---------|
| Rollbar | Reportes de Fallos | Monitoreo de errores y alertas de la aplicación móvil |