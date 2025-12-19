(page-architecture-context)=

# Contexto del Sistema

Vista de alto nivel que muestra actores, límites del sistema y cómo los usuarios interactúan con la plataforma.

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/context.svg
:name: fig-context
:width: 100%

Diagrama de Contexto del Sistema — [Tamaño completo](/diagrams/context.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/context@4x.png
:name: fig-context-print
:width: 100%

Diagrama de Contexto del Sistema
```

+++

## Flujo de Red

Todo el tráfico ingresa a través de nombres de dominio públicos que resuelven a direcciones IP estáticas dentro del VPC. Las solicitudes pasan por servicios de red (CDN, WAF, Load Balancer) antes de alcanzar su destino:

1. **Clientes Web**: Las solicitudes del navegador se enrutan a [](./components/admin-portal) o [](./components/client-web), que luego realizan llamadas a las APIs
2. **Clientes Móviles**: Las aplicaciones nativas se conectan directamente a los Gateway APIs a través de la misma ruta de red
3. **Instalación Local**: Los dispositivos [](./components/handheld) se conectan al [](./components/bastion) local para operación offline; el Bastion se sincroniza con la nube vía internet

## Flujo de Autenticación

Los Gateway APIs ([](./components/admin-api), [](./components/client-api)) autentican solicitudes a través de [](./components/identity), que verifica credenciales contra el Identity Provider. Los Gateway APIs luego reenvían solicitudes autenticadas a los Domain APIs.

Los Domain APIs validan tokens JWT emitidos por el Identity API pero no llaman directamente al Identity API en cada solicitud. Esto previene la creación de un cuello de botella de dependencia mientras se mantiene la seguridad.

## Actores

| Actor              | Descripción                                                        |
| ------------------ | ------------------------------------------------------------------ |
| Cliente            | Compra boletos mediante web o móvil                                |
| Administradores    | Gestiona la configuración de la plataforma                         |
| Taquilla           | Vende boletos en sitio mediante [](./components/admin-portal)      |
| Personal de Acceso | Valida boletos usando dispositivos [](./components/handheld)       |
| Portador de Boleto | Presenta boletos para escaneo en puntos de acceso                  |

## Infraestructura

| Componente           | Ubicación | Propósito                         |
| -------------------- | --------- | --------------------------------- |
| Nombre de Dominio    | Externo   | Resolución DNS                    |
| IP Estática          | Nube      | Punto de entrada fijo al VPC      |
| CDN                  | Nube      | Entrega de contenido y caché      |
| WAF                  | Nube      | Firewall de aplicaciones web      |
| Balanceador de Carga | Nube      | Distribución de tráfico           |

## Sistemas

### Clientes Web

| Sistema                       | Ubicación | Propósito                       |
| ----------------------------- | --------- | ------------------------------- |
| [](./components/admin-portal) | Nube      | Interfaz web para personal      |
| [](./components/client-web)   | Nube      | Compra de boletos para clientes |

### Clientes Móviles

| Sistema                        | Ubicación         | Propósito                      |
| ------------------------------ | ----------------- | ------------------------------ |
| [](./components/client-mobile) | Nube              | Aplicación móvil para clientes |
| [](./components/handheld)      | Instalación Local | Escaneo de códigos QR          |

### Gateway APIs

| Sistema                     | Ubicación | Propósito                              |
| --------------------------- | --------- | -------------------------------------- |
| [](./components/admin-api)  | Nube      | Gateway para operaciones de personal   |
| [](./components/client-api) | Nube      | Gateway para operaciones de clientes   |

### Domain APIs

| Sistema                        | Ubicación | Propósito                                 |
| ------------------------------ | --------- | ----------------------------------------- |
| [](./components/ticketing)     | Nube      | Reservas de asientos                      |
| [](./components/payments)      | Nube      | Procesamiento de transacciones            |
| [](./components/identity)      | Nube      | Autenticación y gestión de usuarios       |
| [](./components/notifications) | Nube      | Entrega de correos y notificaciones push  |

### Instalación Local

| Sistema                  | Ubicación         | Propósito                           |
| ------------------------ | ----------------- | ----------------------------------- |
| [](./components/bastion) | Instalación Local | Validación offline y sincronización |

## Servicios Externos

| Servicio                  | Propósito                                   |
| ------------------------- | ------------------------------------------- |
| Pasarela de Pagos         | Procesamiento de transacciones              |
| Reserva de Asientos       | Mapeo de asientos y disponibilidad          |
| Proveedor de Correo       | Entrega de correos transaccionales          |
| Proveedor de Push         | Notificaciones push móviles                 |
| Proveedor de Identidad    | Autenticación OAuth/OIDC                    |
| Rastreador de Excepciones | Monitoreo de errores y alertas              |
| Servicio de Registro      | Agregación centralizada de registros        |
