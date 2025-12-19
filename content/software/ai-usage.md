---
title: Política de Uso de Asistentes de IA
---

# Política de Uso Seguro de Asistentes de IA en el Ciclo de Desarrollo de Software

## 1\. Objetivo

Establecer los lineamientos técnicos y de seguridad para el uso de herramientas de Inteligencia Artificial Generativa (Copilot, ChatGPT, etc.) en las fases de codificación, testing, documentación y despliegue de software, mitigando riesgos de fuga de propiedad intelectual y vulnerabilidades de seguridad.

## 2\. Principio Rector: "Copiloto, no Piloto"

La IA debe tratarse como un **programador junior no confiable**: puede escribir código rápido, pero carece de contexto de negocio y conciencia de seguridad. Todo output de la IA debe ser revisado, probado y validado por un desarrollador humano antes de cualquier _commit_.

## 3\. Gestión Estricta de Datos Sensibles y Propiedad Intelectual

El riesgo más crítico es la filtración de datos confidenciales hacia los modelos de entrenamiento públicos de los proveedores de IA. Se establecen las siguientes prohibiciones absolutas:

### 3.1. Sanitización de Prompts (Regla de Cero Secretos)

Antes de enviar cualquier fragmento de código o consulta a una IA, el desarrollador debe asegurar que **NO** contenga:

- **Credenciales:** API Keys, Tokens (JWT, OAuth), contraseñas de bases de datos o llaves privadas SSH/PGP.
- **Infraestructura:** Direcciones IP internas, nombres de servidores de producción o rutas de archivos críticos.
- **Configuraciones:** Contenido de archivos .env, config.js o settings.py sin ofuscar.

**Acción Requerida:** Si necesitas que la IA analice una función que usa una API Key, reemplazarla por un placeholder genérico (ej. "YOUR_API_KEY_HERE") antes de pegarla en el chat.

### 3.2. Protección de Datos del Cliente (PII)

Está estrictamente prohibido utilizar datos reales de clientes para generar ejemplos o probar lógica con la IA.

- **Prohibido:** Copiar un JSON, CSV o volcado SQL de producción que contenga nombres, correos, teléfonos, tarjetas de crédito o IDs gubernamentales.
- **Permitido:** Utilizar estructuras de datos vacías o generar datos ficticios (_mock data_) usando librerías como Faker o generados con la misma IA bajo instrucciones explícitas de anonimato.

### 3.3. Contaminación de Contexto

Evitar pegar la lógica de negocio "Core" (el algoritmo secreto que diferencia a la empresa) en chats públicos. Si se requiere ayuda con esa lógica, se debe abstraer el problema matemático o algorítmico y presentarlo de forma aislada, sin revelar cómo se integra en el producto final.

## 4\. Riesgos Críticos al Codificar con IA

El código generado por IA es sintácticamente correcto, pero frecuentemente inseguro o legalmente problemático.

### 4.1. Alucinación de Paquetes (Software Supply Chain Attacks)

La IA puede sugerir la importación de librerías o paquetes que **no existen** o que tienen nombres similares a los populares.

- **Riesgo:** Atacantes crean paquetes maliciosos con esos nombres sugeridos comúnmente por la IA.
- **Mitigación:** Verificar siempre en el repositorio oficial (NPM, PyPI, Maven, NuGet) que la librería existe, es popular, tiene mantenimiento activo y una licencia compatible.

### 4.2. Vulnerabilidades de Seguridad Introducidas

La IA se entrena con código de internet, el cual a menudo es inseguro. Tiende a reintroducir vulnerabilidades clásicas:

- **Inyección SQL:** Sugerir consultas concatenadas en lugar de parametrizadas.
- **XSS (Cross-Site Scripting):** No escapar inputs de usuario en el frontend.
- **Criptografía débil:** Sugerir algoritmos obsoletos (MD5, SHA1) para hashing.
- **Mitigación:** Todo código generado debe pasar por herramientas de análisis estático (SAST) y revisión de pares (Code Review).

### 4.3. Licenciamiento y Derechos de Autor

La IA puede reproducir fragmentos de código protegidos por licencias restrictivas (ej. GPL) sin avisar.

- **Riesgo:** Contaminar el código propietario de la empresa con licencias que obligan a liberar el código fuente (Copyleft).
- **Mitigación:** No solicitar a la IA que reproduzca funciones complejas de software conocido. Usar la IA para lógica genérica, no para copiar funcionalidades específicas de competidores.

## 5\. Protocolo de Desarrollo (Workflow)

Para integrar código de IA en el repositorio oficial, se deben seguir estos pasos:

1. **Aislamiento:** Entender el problema y solicitar a la IA una solución aislada.
2. **Revisión Humana:** Leer el código línea por línea. Si no entiendes qué hace una línea, **bórrala**.
3. **Refactorización:** Renombrar variables para seguir la guía de estilo de la empresa y optimizar la lógica.
4. **Testing Obligatorio:** Escribir Tests Unitarios (Unit Tests) que validen la función, incluyendo casos borde (nulls, listas vacías, caracteres especiales).
5. **Pull Request (PR):** Indicar en el PR si el código base fue generado por IA para que los revisores presten especial atención a posibles huecos de seguridad.

## 6\. Casos de Uso: Permitido vs. Prohibido

| ✅ Permitido (Luz Verde)                                                           | ⛔ Prohibido (Luz Roja)                                                                                              |
| :--------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Boilerplate:** Generar estructuras básicas de clases, interfaces o HTML/CSS.     | **Lógica Core:** Subir el código fuente completo de la aplicación.                                                   |
| **Unit Tests:** Pedirle que genere casos de prueba para una función dada.          | **Debug con Datos Reales:** Pegar logs de error que contienen datos de clientes o secretos.                          |
| **Regex:** Generar o explicar Expresiones Regulares complejas.                     | **Configuración de Seguridad:** Pedirle que genere reglas de Firewall o configuraciones de IAM sin revisión experta. |
| **Refactorización:** "Optimiza esta función para reducir complejidad ciclomática". | **Ofuscación:** Usar la IA para desofuscar código de terceros o ingeniería inversa ilegal.                           |
| **Documentación:** Generar docstrings o comentarios Javadoc/Swagger.               | **Generación de Credenciales:** Usar la IA para generar contraseñas o claves/llaves "seguras".                       |

## 7\. Responsabilidad Final

El uso de herramientas de IA no exime al desarrollador de responsabilidad. Si un bug crítico o una vulnerabilidad llega a producción, la responsabilidad es de quien hizo el _commit_, independientemente de si el código lo escribió un humano o una máquina.

**_"Si no lo puedes explicar, no lo subas."_**
