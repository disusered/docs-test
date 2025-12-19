---
title: Inventario de Servicios
---

La plataforma comprende los siguientes servicios:

## Servicios Internos

### Gateway APIs

| Componente                  | Ubicación | Tecnología | Propósito                                          |
| --------------------------- | --------- | ---------- | -------------------------------------------------- |
| [](./components/admin-api)  | Nube      | .NET 10    | Punto de entrada para front-ends de administración |
| [](./components/client-api) | Nube      | .NET 10    | Punto de entrada para front-ends de cliente        |

### Domain APIs

| Componente                     | Ubicación | Tecnología | Propósito                                             |
| ------------------------------ | --------- | ---------- | ----------------------------------------------------- |
| [](./components/ticketing)     | Nube      | .NET 10    | Reservas de boletos y gestión de asientos             |
| [](./components/payments)      | Nube      | .NET 10    | Procesamiento de pagos y registros transaccionales    |
| [](./components/identity)      | Nube      | .NET 10    | Autenticación y gestión de usuarios                   |
| [](./components/notifications) | Nube      | .NET 10    | Entrega de correos electrónicos y notificaciones push |

### Front-Ends

| Componente                     | Ubicación         | Tecnología                 | Propósito                           |
| ------------------------------ | ----------------- | -------------------------- | ----------------------------------- |
| [](./components/admin-portal)  | Nube              | Blazor                     | Administración para personal        |
| [](./components/client-web)    | Nube              | React                      | Compra de boletos para clientes     |
| [](./components/client-mobile) | Nube              | React Native (Android/iOS) | Experiencia móvil para clientes     |
| [](./components/handheld)      | Instalación Local | Kotlin (Android)           | Validación de boletos para personal |
| [](./components/bastion)       | Instalación Local | .NET 10                    | Sincronización y validación offline |

## Servicios Externos

### Servicios de Aplicación

| Tipo de Servicio          | Propósito                                                      |
| ------------------------- | -------------------------------------------------------------- |
| Base de Datos             | Almacenamiento persistente para datos de aplicación            |
| Caché                     | Acceso rápido a estado de sesión y datos de lectura frecuente  |
| Intermediario de Mensajes | Procesamiento asíncrono de tareas y distribución de eventos    |
| Proveedor de Correo       | Entrega de correos transaccionales (confirmaciones, recibos)   |
| Proveedor de Push         | Entrega de notificaciones push móviles y web                   |
| Pasarela de Pagos         | Procesamiento de tarjetas de crédito y autorización de pagos   |
| Reserva de Asientos       | Mapas de asientos interactivos y disponibilidad en tiempo real |
| Rastreador de Excepciones | Agregación de errores y alertas                                |
| Servicio de Registro      | Almacenamiento centralizado y búsqueda de registros            |

### Servicios de Infraestructura

| Tipo de Servicio       | Propósito                                              |
| ---------------------- | ------------------------------------------------------ |
| Balanceador de Carga   | Distribución de tráfico y terminación SSL              |
| IP Estática            | Punto de acceso público estable para DNS               |
| CDN                    | Caché perimetral y mitigación de DDoS                  |
| WAF                    | Filtrado de solicitudes y reglas de seguridad          |
| Gestor de Certificados | Aprovisionamiento automatizado de certificados SSL/TLS |
| VPC                    | Aislamiento de red y límites de seguridad              |

## Mapeo de Repositorios

| Componente                     | Repositorio              |
| ------------------------------ | ------------------------ |
| [](./components/admin-api)     | `xbol-api-admin`         |
| [](./components/client-api)    | `xbol-api-client`        |
| [](./components/ticketing)     | `xbol-api-ticketing`     |
| [](./components/payments)      | `xbol-api-payments`      |
| [](./components/identity)      | `xbol-identity-provider` |
| [](./components/notifications) | `xbol-api-notifications` |
| [](./components/admin-portal)  | `xbol-web-admin`         |
| [](./components/client-web)    | `xbol-web-client`        |
| [](./components/client-mobile) | `xbol-app-client`        |
| [](./components/handheld)      | `xbol-app-handheld`      |
| Documentación                  | `xbol-documents`         |
| [](./components/bastion)       | TBD                      |
