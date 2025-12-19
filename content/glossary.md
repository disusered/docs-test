---
title: Glosario
label: glossary
---

# Glosario

Este glosario proporciona definiciones para términos clave utilizados a lo largo de la documentación de XBOL.

ACID
: Acrónimo de _Atomicity, Consistency, Isolation, Durability_. Propiedades que garantizan que las transacciones en la base de datos se procesen de manera confiable, asegurando la integridad de los datos ante fallos.

Actors / Actores
: Usuarios o sistemas externos que interactúan con la plataforma XBOL, incluyendo clientes, personal administrativo, taquilla, personal de acceso y portadores de boletos.

AOT Compilation / Compilación Anticipada
: Proceso de compilar el código de alto nivel a código máquina nativo antes de la ejecución, en lugar de hacerlo en tiempo de ejecución (JIT). Mejora significativamente el tiempo de arranque de los servicios.

AOP / Programación Orientada a Aspectos
: _Aspect-Oriented Programming_. Paradigma que permite separar funcionalidades transversales (logging, seguridad, transacciones) del código de negocio principal mediante interceptores y atributos.

APNs
: _Apple Push Notification service_. Servicio de Apple para enviar notificaciones push a dispositivos iOS y macOS.

API
: _Application Programming Interface_. Conjunto de protocolos y herramientas para construir aplicaciones de software.

Asynchronous / Asíncrono
: Modelo de ejecución donde las operaciones no bloquean el hilo principal mientras esperan respuesta, permitiendo procesamiento concurrente y mejor utilización de recursos.

API Key / Clave de API
: Código único o token pasado a una API para identificar al usuario o aplicación que realiza la llamada. Se utiliza para controlar el acceso y rastrear el uso.

Authentication / Autenticación
: Proceso de verificar la identidad de un usuario, dispositivo o sistema antes de otorgar acceso.

Authentication Flow / Flujo de Autenticación
: Secuencia de pasos mediante la cual un sistema verifica la identidad de un usuario y otorga acceso a recursos protegidos.

AWS
: _Amazon Web Services_. Plataforma de servicios en la nube que proporciona infraestructura de computación, almacenamiento y redes. Proveedor principal de XBOL.

Auto Scaling / Escalamiento Automático
: Servicio de AWS que ajusta automáticamente la cantidad de instancias EC2 en función de la demanda, agregando capacidad durante picos de tráfico y reduciéndola cuando disminuye la carga.

Backend
: Capa de acceso a datos y lógica de negocio de la arquitectura. Se refiere a los servicios que se ejecutan en el servidor, invisibles para el usuario final.

Background Worker / Worker en Segundo Plano
: Proceso que ejecuta tareas asíncronas o programadas (background jobs) sin intervención directa del usuario.

Backing Services / Servicios de Respaldo
: Infraestructura de soporte necesaria para operar un servicio (Base de datos, caché, message broker).

Bastion
: Servidor en instalación local que habilita la validación de boletos sin conexión cuando la conectividad a la nube no está disponible.

C#
: Lenguaje de programación desarrollado por Microsoft. Lenguaje principal para los servicios backend de XBOL.

Cache / Caché
: Almacén de datos de alta velocidad que mantiene datos de acceso frecuente en memoria para recuperación rápida.

Centralized Aggregation / Agregación Centralizada
: Recopilación y consolidación de registros y métricas de múltiples fuentes en una ubicación central.

Client / Cliente
: Aplicación con la que los usuarios finales interactúan directamente (navegador web, aplicación móvil, handheld).

Cloud / Nube
: Infraestructura de computación remota que proporciona recursos bajo demanda a través de internet.

CI/CD
: _Continuous Integration / Continuous Deployment_. Práctica de automatizar la integración de código, pruebas y despliegue para entregar cambios de manera frecuente y confiable.

Cloudflare
: Plataforma de servicios de red y seguridad que proporciona CDN, protección DDoS y WAF.

Component / Componente
: Unidad desplegable dentro del sistema XBOL, tal como una API, aplicación web o servicio.

Container / Contenedor
: Unidad de software empaquetada que incluye código y dependencias para ejecutarse de manera consistente en diferentes entornos.

CTE / Expresión de Tabla Común
: _Common Table Expression_. Conjunto de resultados temporal con nombre definido dentro de una consulta SQL, que simplifica consultas complejas y permite recursividad.

curl
: Herramienta de línea de comandos para transferir datos mediante URLs. Comúnmente utilizada para probar APIs HTTP.

Database / Base de Datos
: Almacenamiento persistente (PostgreSQL vía RDS) donde los servicios guardan datos de aplicación.

DDD / Diseño Guiado por el Dominio
: _Domain-Driven Design_. Enfoque de desarrollo de software que centra el diseño en el modelo del dominio de negocio, utilizando un lenguaje ubicuo compartido entre desarrolladores y expertos del dominio.

Debugging / Depuración
: Proceso de identificar, analizar y corregir errores o comportamientos inesperados en el código.

DNS
: _Domain Name System_. Servicio que traduce nombres de dominio legibles por humanos a direcciones IP numéricas.

Docker
: Plataforma de contenedorización que permite empaquetar, distribuir y ejecutar aplicaciones en contenedores aislados.

Dockerfile
: Archivo de texto que contiene instrucciones para construir una imagen de contenedor Docker. Define el sistema base, dependencias, código fuente y comandos de ejecución.

Domain API / API de Dominio
: Servicio responsable de una capacidad de negocio específica (ticketing, pagos, identidad, notificaciones).

EC2
: _Elastic Compute Cloud_. Servicio de AWS que proporciona capacidad de cómputo redimensionable mediante máquinas virtuales.

ECR
: _Elastic Container Registry_. Servicio administrado de AWS para almacenar, gestionar y desplegar imágenes de contenedores Docker. Integrado con IAM para control de acceso y escaneo de vulnerabilidades.

Edge Caching / Caché Perimetral
: Técnica que almacena copias de contenido en servidores distribuidos geográficamente cerca de los usuarios finales.

Encryption / Cifrado
: Proceso de convertir datos en un formato ilegible mediante algoritmos criptográficos para proteger información sensible.

Exceptions / Excepciones
: Errores o condiciones anómalas que ocurren durante la ejecución del software, capturadas para análisis.

FCM
: _Firebase Cloud Messaging_. Servicio de Google para enviar notificaciones push a dispositivos Android, iOS y web.

Front-End / Interfaz de Usuario
: Aplicación o interfaz visual que se ejecuta en el navegador o dispositivo del cliente.

Gateway API / API de Gateway
: Punto de entrada que enruta solicitudes a servicios internos, gestionando autenticación y orquestación.

GitHub Actions
: Plataforma de CI/CD integrada en GitHub que permite automatizar flujos de trabajo de construcción, pruebas y despliegue mediante archivos YAML en el repositorio.

Horizontal Scaling / Escalamiento Horizontal
: Técnica de escalabilidad que agrega más instancias de servidores o servicios para distribuir la carga.

Identity / Identidad
: Servicio que gestiona autenticación de usuarios, autorización e información de cuentas.

Instance / Instancia
: Servidor virtual o recurso de computación individual en la nube que ejecuta cargas de trabajo específicas.

JSONB
: Formato de almacenamiento binario para datos JSON en PostgreSQL. Permite almacenar datos semi-estructurados con capacidad de indexación.

JWT
: _JSON Web Token_. Estándar abierto para transmitir información de manera segura entre partes como objeto JSON.

Kotlin
: Lenguaje de programación moderno utilizado para el desarrollo de componentes nativos en Android.

Load Balancer / Balanceador de Carga
: Distribuye tráfico entrante a través de múltiples servidores para confiabilidad y rendimiento.

Material Design / MudBlazor
: Sistema de diseño y biblioteca de componentes para .NET que proporcionan la guía visual para las aplicaciones administrativas.

Message Broker / Intermediario de Mensajes
: Software que habilita comunicación asíncrona entre servicios mediante enrutamiento de mensajes a través de colas.

Metrics / Métricas
: Mediciones cuantitativas del rendimiento y comportamiento del sistema.

Microservice / Microservicio
: Estilo arquitectónico donde la aplicación se estructura como una colección de servicios pequeños y autónomos.

Middleware
: Software que actúa como puente entre una solicitud y la lógica principal (ej. logging, autenticación).

Mobile OS / Sistema Operativo Móvil
: Plataformas de software base para dispositivos móviles (iOS y Android).

Network Isolation / Aislamiento de Red
: Separación lógica de redes para prevenir acceso no autorizado.

Next.js
: Framework web basado en React que habilita renderizado del lado del servidor (SSR) y optimización SEO.

Notifications / Notificaciones
: Servicio que entrega mensajes a usuarios mediante correo electrónico u otros canales.

OAuth
: _Open Authorization_. Protocolo estándar de autorización que permite a aplicaciones de terceros acceder a recursos de un usuario sin exponer sus credenciales, mediante tokens de acceso delegados.

On-Premise / Instalación Local
: Hardware y software ubicado en la instalación física del evento en lugar de en la nube.

Orchestration / Orquestación
: Coordinación automatizada de múltiples servicios para ejecutar un flujo de trabajo complejo.

Payments / Pagos
: Servicio que procesa transacciones financieras y mantiene registros de pagos.

PII / Información de Identificación Personal
: _Personally Identifiable Information_. Cualquier dato que pueda identificar a un individuo específico, como nombre, correo electrónico, número de teléfono, dirección o documento de identidad. Requiere protección especial bajo regulaciones de privacidad.

Platform / Plataforma
: Objetivo de despliegue para una aplicación cliente (iOS, Android, navegador web).

Polling
: Técnica donde el cliente consulta periódicamente al servidor para verificar cambios de estado, en lugar de recibir notificaciones push. Utilizada en colas virtuales para actualizar la posición del usuario.

PostgreSQL
: Sistema de gestión de bases de datos relacional de código abierto.

Push Notifications / Notificaciones Push
: Mensajes enviados directamente a dispositivos sin solicitud activa del usuario.

RabbitMQ
: Intermediario de mensajes que implementa el protocolo AMQP, usado para comunicación asíncrona.

RDS
: _Relational Database Service_. Servicio administrado de base de datos de AWS.

RDS Proxy
: Servicio de AWS que gestiona un pool de conexiones a bases de datos RDS, reduciendo la sobrecarga de conexiones y mejorando la escalabilidad de aplicaciones con alta concurrencia.

React
: Biblioteca de JavaScript para construir interfaces de usuario interactivas.

React Native
: Framework para construir aplicaciones móviles nativas usando React.

Redis
: Almacén de datos en memoria utilizado como caché de alta velocidad.

Roles
: Conjunto de permisos y privilegios asignados a usuarios o servicios.

RPS
: _Requests Per Second_. Métrica que mide la cantidad de solicitudes que un servicio puede procesar por segundo. Utilizada para evaluar capacidad y establecer límites de throttling.

Rollbar
: Servicio de monitoreo de errores en tiempo real.

SEO
: _Search Engine Optimization_. Prácticas para asegurar que el contenido público sea indexable por buscadores.

Service / Servicio
: Proceso en ejecución que realiza trabajo (API o worker).

SMS
: _Short Message Service_. Servicio de envío de mensajes de texto a móviles.

SSL
: _Secure Sockets Layer_. Protocolo criptográfico para comunicaciones seguras.

SSL Termination / Terminación SSL
: Proceso donde el balanceador de carga descifra el tráfico SSL antes de pasarlo a los servidores internos.

SQL
: _Structured Query Language_. Lenguaje estándar para gestionar y consultar bases de datos relacionales.

SSR / Renderizado del Lado del Servidor
: Técnica donde el HTML se genera en el servidor antes de enviarse al navegador.

Static IP / IP Estática
: Dirección IP pública fija que proporciona un punto de entrada estable.

Stateless
: Patrón de arquitectura donde los servicios no almacenan estado de sesión entre solicitudes. Permite escalamiento horizontal al agregar instancias sin compartir memoria.

Structured Logging / Registro Estructurado
: Práctica de registrar eventos del sistema en formato estructurado (JSON).

Template / Plantilla
: Estructura base de código preconfigurada para estandarizar el desarrollo.

Ticketing / Boletería
: Servicio que gestiona inventario de boletos, reservas y compras.

Throttling
: Técnica de control de caudal que limita la cantidad de solicitudes aceptadas en un periodo de tiempo para proteger servicios críticos de sobrecarga.

Token
: Credencial digital que representa autenticación o autorización.

VM / Máquina Virtual
: Emulación de un sistema computacional (ej. instancias EC2).

VPC
: _Virtual Private Cloud_. Entorno de red aislado dentro de la nube pública.

WAF
: _Web Application Firewall_. Filtra tráfico malicioso hacia las aplicaciones web.

XBOL
: Sistema principal documentado en esta referencia técnica.

XBOL System
: Solución completa que incluye software, bases de datos e integraciones.
