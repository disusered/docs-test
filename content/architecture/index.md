---
title: Principios Arquitectónicos
---

## Gateway API

Los componentes [](./components/client-api) y [](./components/admin-api) constituyen los puntos de entrada principales para las aplicaciones front-end. Estos componentes son Gateway APIs que gestionan la autenticación y orquestan las llamadas hacia los Domain APIs ([](./components/ticketing), [](./components/payments), [](./components/notifications), [](./components/identity)). Los Domain APIs no son consumidos directamente por los front-ends durante operación normal, aunque permanecen independientemente accesibles para herramientas internas o integraciones futuras.

## Base de Datos por Servicio

Cada API posee sus propios servicios de respaldo (Base de Datos, Caché, Intermediario de Mensajes). Incluso cuando comparten infraestructura física, los servicios están lógicamente aislados.

## Resiliencia Sin Conexión

El sistema [](./components/bastion) habilita la validación de boletos cuando la conectividad a la nube no está disponible. El personal escanea códigos QR en boletos o dispositivos utilizando [](./components/handheld) conectados localmente al bastion. La validación opera sin conexión; los datos se sincronizan con la nube cuando la conectividad se restablece. Las aplicaciones web y móviles de cliente requieren conectividad a internet.

## Mensajería Multicanal

Los servicios envían notificaciones mediante correo electrónico y notificaciones push a través de un componente dedicado [](./components/notifications). Canales adicionales (SMS, etc.) pueden agregarse según sea necesario.

## Registro Estructurado

Todos los procesos utilizan registro estructurado (structured logging). Los registros se escriben a archivos de texto locales y se persisten a un servicio de registro para almacenamiento a largo plazo. Los equipos de TI pueden configurar destinos adicionales según sea necesario.

## Simplicidad de Infraestructura

El despliegue inicial ejecuta todos los servicios en una única VM con Docker Compose. La gestión de red en la nube maneja el Balanceador de Carga, terminación SSL, CDN, WAF y asignación de IP estática. El DNS es administrado por un registrador de dominio externo.
