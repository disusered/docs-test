---
title: Bastion
---

El Bastion es un servidor en instalación local que habilita la validación de boletos offline cuando la conectividad a la nube no está disponible.

## Resumen

- **Tipo**: API de Dominio (Instalación Local)
- **Repositorio**: TBD
- **Plataforma**: .NET 10 (plantilla de ASP.NET Core API)
- **Despliegue**: Contenedor Docker a través de Docker Compose (en hardware del recinto)

## Arquitectura

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/component-bastion.svg
:name: fig-component-bastion
:width: 100%

Arquitectura del Bastion — [Tamaño completo](/diagrams/component-bastion.svg)
```

+++

+++ {"class": "no-web"}

```{image} /diagrams/component-bastion@4x.png
:width: 100%
```

+++

## Rol

- Proporciona validación de boletos offline para dispositivos [](./handheld)
- Almacena en caché datos de boletos desde [](./admin-api) para acceso offline
- Sincroniza logs de validación a [](./admin-api) cuando se restablece la conectividad

## Servicios de Respaldo

| Rol             | Tecnología | Proveedor         |
| ---------------- | ---------- | ---------------- |
| Base de Datos | PostgreSQL | Contenedor Docker   |
| Caché    | Redis      | Contenedor Docker |

## Proveedores Externos

| Proveedor | Servicio           | Propósito                       |
| -------- | ----------------- | ----------------------------- |
| Rollbar  | Rastreador de Excepciones | Monitoreo de errores y alertas |

## Red

- **LAN**: Atiende dispositivos [](./handheld) a través de red local
- **Internet**: Sincroniza con [](./admin-api) en la nube cuando está disponible

## Arquitectura de Conectividad Recomendada

El Bastion implementa lógica de "almacenar y reenviar" para sobrevivir desconexiones totales. Sin embargo, la infraestructura física debe actuar como filtro multicapa para minimizar la frecuencia de eventos offline.

### Niveles de Conectividad

| Nivel | Tipo | Función | Notas |
|-------|------|---------|-------|
| 1 | Enlace Dedicado / VPN | Tráfico crítico de sincronización | Túnel VPN al VPC en la nube, evita internet público |
| 2 | Internet Público (Fibra) | Wi-Fi de invitados, tráfico de oficina, VPN de respaldo | Susceptible a congestión en días de evento |
| 3 | Celular 5G/LTE | Recuperación ante desastres | Requiere APN privado para evitar saturación de torres |

### Escenarios de Falla

| Escenario | Comportamiento de Red | Rol del Bastion |
|-----------|----------------------|-----------------|
| Operación Normal | Tráfico fluye por Nivel 1 | Sincronización en tiempo real |
| Congestión de Internet | Nivel 1 no afectado (enlace privado) | Sin acción requerida |
| Corte de Fibra (Niveles 1 y 2) | Failover a Nivel 3 (5G) | Modo restringido: prioriza sincronización de ventas sobre logs |
| Apagón Total | Sin conectividad | Modo offline: acepta transacciones localmente, reintenta sincronización periódicamente |

### Requisitos de Infraestructura

- **Diversidad Física**: Entradas de fibra por rutas separadas para prevenir punto único de falla
- **Router SD-WAN**: Balanceo activo/pasivo entre fibra y celular, con priorización de tráfico
- **APN Privado**: SIM con tier de prioridad empresarial para respaldo celular confiable durante eventos masivos
- **Redundancia Eléctrica**: Bastion y router en mismo circuito UPS