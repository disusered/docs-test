(page-architecture-deployment)=

# Entorno Operativo

Despliegue de infraestructura mostrando límites de proveedores, decisiones tecnológicas y servicios de respaldo.

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/deployment.svg
:name: fig-deployment
:width: 100%

Diagrama de Despliegue — [Tamaño completo](/diagrams/deployment.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/deployment@4x.png
:name: fig-deployment-print
:width: 100%

Diagrama de Despliegue
```

+++

## Límites de Proveedores

### Cloudflare

| Servicio        | Propósito                                     |
| --------------- | --------------------------------------------- |
| CDN             | Caché perimetral y entrega de contenido       |
| WAF             | Filtrado de solicitudes y reglas de seguridad |
| DDoS Protection | Análisis de tráfico y mitigación de ataques   |

### AWS

| Servicio                   | Propósito                                 |
| -------------------------- | ----------------------------------------- |
| VPC                        | Aislamiento de red y límites de seguridad |
| IP Estática                | Punto de acceso público estable para DNS  |
| Balanceador de Carga (ALB) | Distribución de tráfico y terminación SSL |
| Gestor de Certificados     | Aprovisionamiento automatizado de SSL/TLS |
| RDS (PostgreSQL)           | Servicio de base de datos administrado    |
| CloudWatch                 | Métricas, registros y alarmas             |

### Instalación Local

Los sistemas en instalación local operan dentro de la red local del evento.

| Componente                | Plataforma       | Propósito                                       |
| ------------------------- | ---------------- | ----------------------------------------------- |
| [](./components/bastion)  | .NET 10 (Docker) | Validación offline y sincronización con la nube |
| [](./components/handheld) | Android          | Escaneo de boletos para personal                |

## Plataformas de Cliente

Las aplicaciones cliente se ejecutan en las siguientes plataformas:

| Cliente                        | Plataformas               |
| ------------------------------ | ------------------------- |
| [](./components/client-mobile) | iOS, Android              |
| [](./components/handheld)      | Solo Android              |
| [](./components/admin-portal)  | Web (cualquier navegador) |
| [](./components/client-web)    | Web (cualquier navegador) |

## Servicios de Respaldo

Cada Domain API posee sus propios servicios de respaldo (patrón base-de-datos-por-servicio):

| API                            | Base de Datos | Caché | Intermediario de Mensajes |
| ------------------------------ | ------------- | ----- | ------------------------- |
| [](./components/ticketing)     | PostgreSQL    | Redis | RabbitMQ                  |
| [](./components/payments)      | PostgreSQL    | Redis | RabbitMQ                  |
| [](./components/identity)      | PostgreSQL    | Redis | -                         |
| [](./components/notifications) | PostgreSQL    | -     | RabbitMQ                  |

## Modelo de Despliegue

El despliegue inicial ejecuta los servicios en una única instancia EC2 con Docker Compose:

- **VM Única**: Todos los contenedores de aplicación colocados juntos para simplicidad
- **RDS PostgreSQL**: Cada servicio posee su propia base de datos; las bases de datos pueden migrarse a instancias RDS separadas para escalamiento
- **Redis por Servicio**: Cada servicio ejecuta su propio contenedor Redis, aislado mediante Docker Compose
- **RabbitMQ por Servicio**: Cada servicio ejecuta su propio contenedor RabbitMQ, aislado mediante Docker Compose

Este modelo soporta escalamiento horizontal mediante extracción de servicios a hosts dedicados o promoción de bases de datos a instancias RDS dedicadas.
