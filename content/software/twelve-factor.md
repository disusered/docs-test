---
title: Metodología 12 Factor App
---

[12 factor app](https://12factor.net/) es una metodología utilizada en software entregado como servicio (_software-as-a-service_ o _web apps_). A nivel de arquitectura, establecemos un contrato limpio con el sistema operativo, maximizando la portabilidad entre ambientes de ejecución. En lugar de depender de configuraciones manuales, utilizamos formatos declarativos para automatizar el setup del entorno (dockerfile por ejemplo), lo que reduce la barrera de entrada para nuevos desarrolladores.

Son adecuados para el despliegue en plataformas en la nube, eliminando la necesidad de servidores y administración de sistemas tradicionales. Minimizan la divergencia entre los ambientes de producción y desarrollo, permitiendo el despliegue e integración continua (CI/CD). Por último, estas aplicaciones pueden escalar sin cambios significativos en las herramientas, arquitectura o prácticas de desarrollo.

## Procesamiento asíncrono / en segundo plano

Delegar tareas de larga duración o no críticas a tareas en segundo plano, colas de mensajes o procesos de trabajo. Evita solicitudes que puedan bloquear el sistema y mejora la capacidad de respuesta al mantener la aplicación con capacidad de respuesta incluso bajo una carga elevada.

## Seguridad e integridad de los datos

La seguridad y la integridad de los datos son cruciales para proteger contra el acceso no autorizado, mantener la confianza de los usuarios/clientes, garantizar la precisión en la toma de decisiones y cumplir con las normativas. Garantizan que el software sea fiable y esté disponible para los usuarios.

## Validación y depuración de entradas

Nunca debemos confiar en los datos enviados por el usuario/cliente. Siempre debemos validar los tipos, longitudes y formatos en el punto de entrada (Controlador).

Siempre debemos tener presente prevenir ataques de inyección SQL y garantizar la consistencia de los datos. Aunque el Frontend valide la entrada, el Backend debe validarla nuevamente, ya que las solicitudes pueden ser falsificadas (mediante cURL o Postman).

Esto evita que datos corruptos ingresen a la base de datos, lo que suele provocar fallos en otras partes del sistema posteriormente.

## Autenticación y autorización

Una gestión de identidades adecuada a los servicios y recursos del sistema garantiza que solo los usuarios y roles autorizados accedan a las operaciones confidenciales.

Dando como beneficio flujos de usuario seguros, menos errores de acceso, permitiendo una escalabilidad en la gestión de usuarios, menor riesgo de seguridad, cumplimiento normativo.

## Principio de privilegio mínimo

Los servicios y los usuarios de la base de datos solo deben tener los permisos esenciales para realizar su función. Debemos estar preparados para la contención de daños y aumentar la resiliencia del sistema.

Por ejemplo, si un atacante compromete un servicio, no debería tener acceso a la base de datos para eliminar tablas o si un desarrollador escribe accidentalmente un comando malicioso, la capa de permisos lo bloquea.

## Encriptación

El cifrado de datos en tránsito y en reposo es necesario para proteger la información confidencial (datos personales, credenciales, etc) para evitar su exposición. Hay que asegurarnos que la información esté protegida contra accesos no autorizados, incluso si el dispositivo es perdido o robado.

## Gestión de dependencias / aplicación de parches

Mantener las dependencias actualizadas y auditar las vulnerabilidades, ayudan a reducir riesgos de seguridad; los paquetes obsoletos son un vector de ataque común.

También mejora la eficiencia de los desarrolladores al permitir acceso a nuevas funciones y un mejor rendimiento gracias a las dependencias actualizadas.

## Gestión de secretos

La gestión de secretos busca mantener la información confidencial, como claves de API y contraseñas, estrictamente fuera del código fuente. Almacenar estos datos en archivos dentro del proyecto, como `appsettings.json` aumenta el riesgo de que sean expuestos accidentalmente en el repositorio.

En el entorno de desarrollo local utilizamos la herramienta [Secret Manager de .NET](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-10.0&tabs=linux#secret-manager), la cual almacena las credenciales en el perfil del usuario local en lugar del directorio del proyecto. En producción, la configuración se inyecta mediante variables de entorno.

## La limitación de velocidad y la regulación del ancho de banda (Rate Limiting / Throttling)

Esto ofrece ventajas como la protección contra ataques como DDoS y botnets, la garantía de una asignación equitativa de recursos entre los usuarios y la mejora de la estabilidad y el rendimiento del sistema al prevenir la sobrecarga del servidor. También ayudan a gestionar los costes al controlar el consumo de recursos y garantizar gastos predecibles procedentes de servicios externos.
