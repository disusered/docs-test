---
title:
---

# Introducción

La presente arquitectura tiene como objetivo construir un sistema que gestione el ciclo de vida completo de un ticket. Este sistema será diseñado para cubrir escenarios de venta tradicional de boletos y venta en mercado secundario, garantizando escalabilidad, seguridad, trazabilidad y flexibilidad para distintos tipos de eventos (deportivos, conciertos y espectáculos).

Este sistema consistirá de un conjunto de microservicios, portales y aplicaciones para dispositivos que denominaremos componentes ya que cada uno cumplirá una función específica que formará parte del sistema.

A continuación se detalla la arquitectura y tecnologías que se implementarán para el desarrollo del sistema.

# Arquitectura

La arquitectura del sistema está basada en microservicios con un enfoque de reutilización de software centrado en la integración de componentes independientes y débilmente acoplados con la finalidad de permitir un desarrollo ágil, un mantenimiento más sencillo y proporcionar una mayor escalabilidad.

Por lo que podemos decir que el sistema se basa en una arquitectura moderna, modular y orientada a servicios, permitiendo su evolución y reutilización en distintos mercados y tipos de evento.

- Backend centralizado en APIs REST.
- Frontends especializados por tipo de usuario y dispositivo.
- Base de datos robusta y confiable.
- Motor de precios desacoplado y extensible.

# Tecnologias

Las tecnologías a utilizar para el desarrollo de software son las siguientes y se da una breve justificación de por qué se eligieron.

**_APIs_**

- Tecnologías: PostgreSQL y C\# / .NET 10\.
- Justificación: PostgreSQL es elegido por su robustez transaccional (ACID) y su excelente manejo de datos complejos mediante JSONB, ideal para esquemas de eventos que varían entre sí. C\# / .NET 10 representa la vanguardia en rendimiento. Esta elección asegura el uso de las últimas optimizaciones en el Runtime y soporte para AOT (Ahead Of Time) compilation, lo que reduce los tiempos de respuesta en picos de tráfico masivo.

**_Portal Admin_**

- Tecnologias: Blazor (C\# / .NET 10\) y MudBlazor.
- Justificación: Permite que el equipo de backend desarrolle la herramienta interna usando C\#, compartiendo modelos de datos y lógica de validación, lo que acelera el tiempo de entrega (Time-to-Market)

**Portal Cliente**

- Tecnologias: React, Next.js y Material design.
- Justificación: El SSR (Server Side Rendering) de Next.js es crítico para el SEO (Search Engine Optimization) de los eventos y la velocidad de carga inicial. Material design asegura una estética profesional y limpia.

**Aplicaciones Movil**

- Tecnologias: React Native
- Justificación: Permite una base de código única para iOS y Android, reduciendo tiempos de desarrollo y coherencia visual con el portal de cliente.

**Handhelds**

- Tecnologias: Kotlin
- Justificación: Este ofrece acceso directo al hardware con el máximo rendimiento nativo.

# Gestión de la información

En algunos escenarios algunos de los componentes usarán su propia BD basándonos en el principio de la persistencia políglota. Esto optimiza las diferentes necesidades de datos para su manejo específico del dominio. Se trata de aprovechar las fortalezas únicas de cada componente y a la vez poder gestionar al mismo tiempo la complejidad y la consistencia de los datos. Aun no está del todo definido pero al finalizar el proyecto se podría tener un escenario como el que sigue

- **DB Boletera:** Aquí se centrará la información general del sistema para la gestión y manejo del sistema.
- **DB de Pagos:** Aquí se almacenará toda la información referente a pagos de servicios.
- **DB de ventas (ML):** Aquí se almacena la información relacionada a las ventas, para en un futuro ser la base para la alimentación de IA.
- **BD Parciales:** Tanto el bastión y los handhelds, tendrán que tener una BD parcial para escenarios donde trabajarán en modo offline.

## Protocolos de comunicación

Para mantener la consistencia en la comunicación entre componentes, utilizaremos un bus se servicios que proporciona una estrategia de middleware eficaz para la mensajería entre servicios, políticas de fallos de mensajes y persistencia de entrada/salida. Esto nos permite aprovechar el procesamiento asíncrono y paralelo dentro de uno o varios procesos.

# Estrategia de despliegue

Los componentes se almacenarán en contenedores y se utilizara un orquestador para su implementación, escalado y gestión automatizados.

- **Herramienta para contenedores:** Docker
- **Plataforma de orquestacion:** Kubernetes
- **Entorno de implementación:** Proveedor de nube como Google Cloud o AWS

# Consideraciones de seguridad

La seguridad se implementará en múltiples capas y mecanismos. Algunos serán implementados junto con la estrategia de despliegue, en otros tendremos un servicio que se encarga de la autenticación de los usuarios/servicios por medio de tokens JWT o API KEYs, además de proteger la información sensible utilizando llaves secretas y algoritmos robustos para el cifrado de datos.

# Filosofía de trabajo

Nuestra filosofía está enfocada a entregables, pero siguiendo los principios y buenas prácticas para el desarrollo de software, asegurando así un código limpio, mantenible y escalable. Nos inclinamos a que nuestro trabajo cumpla con los protocolos de calidad e integridad para entregar un producto sólido.

# Diagramas

Los diagramas son una representación inicial del alance del proyecto, donde mostramos la interacción entre los componentes y la lógica de ciertos puntos importantes del sistema.

**Diagramas de arquitectura**

| Diagrama                                 | Propósito                                                          |
| ---------------------------------------- | ------------------------------------------------------------------ |
| [](#page-architecture-context)           | Vista de alto nivel de actores, sistemas y límites arquitectónicos |
| [](#page-architecture-deployment)        | Límites de proveedores y decisiones tecnológicas de despliegue     |
| [Componentes](#page-appendix-components) | Componentes del sistema y sus interacciones                        |

**Diagramas de actividades de compras**

| Diagrama                                | Propósito                                                  |
| --------------------------------------- | ---------------------------------------------------------- |
| [Taquilla](#page-appendix-box-office)   | Flujo de actividades para compras presenciales en taquilla |
| [En linea](#page-appendix-online-sales) | Flujo de actividades para compras a través del portal web  |

**Diagramas de actividades de Bastion**

| Diagrama                                         | Propósito                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------ |
| [Happy Path](#page-appendix-bastion-happy-path)  | Flujo normal de escaneo de boletos con sincronización exitosa al Bastion       |
| [Crash](#page-appendix-bastion-crash)            | Manejo de fallas temporales y permanentes del Bastion, incluyendo recuperación |
| [Replay](#page-appendix-bastion-replay)          | Detección de intentos de clonación de boletos en modos online y offline        |
| [Bottlenecks](#page-appendix-bastion-bottleneck) | Comportamiento ante red lenta y transición automática a modo offline           |

**Diagramas de secuencia de ventas**

| Diagrama                                                 | Propósito                                                                               |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [Venta Inmediata](#page-appendix-sale-payment-immediate) | Flujo de venta general con cobro inmediato y reserva de asientos vía seats.io           |
| [Venta Diferido](#page-appendix-sale-payment-deferred)   | Flujo de venta con pago diferido (ej. Oxxo Pay) y liberación automática por vencimiento |
| [Venta Xolopass](#page-appendix-sale-xolopass)           | Venta de Xolopases no renovados durante preventa, con reserva previa de asientos        |
| [Renovación Xolopass](#page-appendix-renew-xolopass)     | Renovación de Xolopass existente manteniendo asiento reservado                          |
| [Reserva Credito](#page-appendix-reserve-credit)         | Venta a crédito con pagos parciales y manejo de morosidad (inhabilitación/cancelación)  |
| [Reserva Palco](#page-appendix-reserve-suites)           | Reserva y venta de palcos completos con entrega de pases                                |
