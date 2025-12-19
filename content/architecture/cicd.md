(page-architecture-cicd)=

# CI/CD y Despliegue de Contenedores

Sistema estandarizado de integración y despliegue continuo basado en contenedores Docker, con registro centralizado en AWS ECR.

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/cicd.svg
:name: fig-cicd
:width: 100%

Pipeline de CI/CD — [Tamaño completo](/diagrams/cicd.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/cicd@4x.png
:name: fig-cicd-print
:width: 100%

Pipeline de CI/CD
```

+++

## Estructura de Repositorios

Todos los repositorios de servicios siguen una estructura estandarizada para construcción de contenedores:

| Archivo | Propósito |
| ------- | --------- |
| `Dockerfile` | Definición de imagen de contenedor |
| `docker-compose.yml` | Orquestación local y producción |
| `.dockerignore` | Exclusiones de contexto de build |
| `.github/workflows/` | Definiciones de pipelines CI/CD |

## Pipeline de CI/CD

El pipeline de GitHub Actions ejecuta los siguientes pasos en cada push:

| Etapa | Propósito |
| ----- | --------- |
| Build | Compilación de código y dependencias |
| Test | Ejecución de pruebas automatizadas |
| Push | Publicación de imagen a ECR |

## Mapeo de Entornos

La rama determina el entorno de despliegue y etiqueta de imagen:

| Rama | Entorno | Tag ECR |
| ---- | ------- | ------- |
| `main` | Producción | `latest`, `v{version}` |
| `develop` | Staging | `staging` |
| Feature branches | — | Sin despliegue automático |

## Registro de Contenedores

AWS Elastic Container Registry (ECR) almacena las imágenes de contenedor:

| Configuración | Valor |
| ------------- | ----- |
| Región | Consistente con VPC principal |
| Política de retención | Últimas 10 versiones por servicio |
| Escaneo de vulnerabilidades | Habilitado en push |

## Gestión de Secretos

AWS Secrets Manager proporciona credenciales en tiempo de ejecución:

| Secreto | Uso |
| ------- | --- |
| Credenciales de base de datos | Conexión a RDS PostgreSQL |
| API keys de terceros | seats.io, pasarela de pagos, etc. |
| Certificados | Comunicación inter-servicio |

Los contenedores obtienen secretos al iniciar mediante el SDK de AWS, sin almacenamiento en variables de entorno estáticas.

## Observabilidad

CloudWatch centraliza métricas y registros del pipeline y contenedores:

| Componente | Métricas |
| ---------- | -------- |
| GitHub Actions | Duración de builds, tasa de éxito |
| ECR | Tamaño de imágenes, vulnerabilidades |
| Contenedores | Logs de aplicación, uso de recursos |

## Despliegue

El proceso de despliegue en EC2:

1. GitHub Actions completa build y push a ECR
2. EC2 ejecuta `docker compose pull` para obtener imágenes actualizadas
3. `docker compose up -d` reinicia servicios con nuevas versiones
4. Health checks validan disponibilidad

El balanceador de carga (ALB) dirige tráfico únicamente a contenedores saludables.
