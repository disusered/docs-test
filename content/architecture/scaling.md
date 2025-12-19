---
title: Escalabilidad
---

(page-architecture-scaling)=

# Escalabilidad

Estrategia de escalamiento para soportar alta demanda en eventos masivos, protegiendo los componentes críticos del sistema.

## Contexto

La plataforma se desarrolla para un estadio con capacidad de aproximadamente 25,000 asientos, utilizado por un equipo profesional de futbol y para conciertos y otros eventos.

Se ha manifestado preocupación por la capacidad para soportar escenarios de alta demanda—como preventas de partidos con figuras internacionales (ej. amistosos de selección nacional)—donde plataformas de terceros han reportado millones de solicitudes y fallas bajo presión.

El enfoque de escalabilidad no se basa en un número arbitrario de "usuarios concurrentes", sino en métricas concretas:

- Usuarios en fila de espera
- Intentos de compra por segundo
- Capacidad máxima de base de datos y proveedores externos

## Principios de Diseño

| Principio | Implementación |
| --------- | -------------- |
| APIs Stateless | Escalamiento horizontal en EC2 con Auto Scaling |
| Protección de cuellos de botella | Throttling y cola virtual para DB, seats.io y pasarela |
| Separación de responsabilidades | Operaciones secundarias procesadas vía WolverineFX |
| Defensa perimetral | Cloudflare WAF para filtrar tráfico malicioso |

## Cuellos de Botella y Mitigación

### Base de Datos (PostgreSQL/RDS)

| Riesgo | Mitigación |
| ------ | ---------- |
| Conexiones simultáneas | RDS Proxy |
| Bloqueos en tablas críticas | Diseño de índices, tablas delgadas |
| Lecturas intensivas | Caché agresivo con Redis |

### Proveedor de Asientos (seats.io)

| Riesgo | Mitigación |
| ------ | ---------- |
| Límites de RPS | Minimizar llamadas redundantes |
| Latencia de render | Cachear elementos estáticos |

### Pasarela de Pagos

| Riesgo | Mitigación |
| ------ | ---------- |
| Límite de transacciones concurrentes | Reintentos controlados |
| Latencia por intento | Separación orden/pago confirmado |

### APIs Propias

| Riesgo | Mitigación |
| ------ | ---------- |
| Código síncrono bloqueante | APIs 100% async/await |
| Operaciones pesadas en endpoints | Separación de responsabilidades |
| Falta de caché | Redis para lecturas frecuentes |

## Throttling

Control de caudal implementado en Cloudflare WAF mediante reglas rate-based que bloquean IPs que exceden umbrales en endpoints críticos:

- Login
- Inicio de checkout
- Confirmación de compra

## Cola Virtual

Para eventos de altísima demanda, la cola virtual ordena y dosifica el acceso al checkout.

### Comportamiento

1. Usuario solicita compra para evento con cola habilitada
2. Si hay capacidad disponible → acceso directo (`status=ready`)
3. Si no hay capacidad → asignación de turno (`status=waiting`)
4. Frontend consulta estado periódicamente (polling)
5. Sistema promueve usuarios cuando se libera capacidad
6. Token de cola requerido para iniciar checkout

### Endpoints

| Método | Endpoint | Propósito |
| ------ | -------- | --------- |
| POST | `/events/{eventId}/queue` | Entrar a cola o acceso directo |
| GET | `/events/{eventId}/queue/{queueToken}` | Consultar estado (waiting/ready/expired) |

### Implementación

- Almacén de estado: Redis (ElastiCache)
- Servicio: `QueueService` dentro de [](./components/ticketing)
- Habilitación: Por evento mediante flag `Events.QueueEnabled`

## Procesos Asíncronos

WolverineFX procesa tareas no críticas en segundo plano:

| Tarea | Prioridad |
| ----- | --------- |
| Confirmación de compra (correo) | Diferida |
| Actualización de puntos de lealtad | Diferida |
| Generación de comprobantes/facturas | Diferida |
| Integraciones con backoffice | Diferida |

## Plan de Implementación

### Fase 1 — Arquitectura Base

- APIs stateless en EC2 con Auto Scaling y ALB
- PostgreSQL en RDS con RDS Proxy
- Caché Redis para lecturas
- Integración con seats.io
- WolverineFX para procesos asíncronos
- Reglas básicas de WAF

### Fase 2 — Endurecimiento

- Ajuste de reglas de throttling en WAF
- Pruebas de carga para medir transacciones por segundo
- Validación de capacidad en checkout concurrente

### Fase 3 — Cola Virtual

- Implementación con Redis y endpoints descritos
- Habilitación solo para eventos marcados como alta demanda
- Refinamiento de UX en pantalla de espera
