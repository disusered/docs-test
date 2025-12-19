---
title: Documentación de APIs
---

## Descripción

Diseñar una API es como diseñar una interfaz de usuario para desarrolladores. Si la nomenclatura es inconsistente o la documentación es vaga, la integración se convierte en una pesadilla.

A continuación, se presenta una guía completa sobre convenciones de nomenclatura y buenas prácticas de documentación, adaptada específicamente a las API RESTful y la especificación Open API (OAS).

## Lineamientos sobre la documentación de nuestras APIs 

La regla de oro de REST es: las URI deben ser sustantivos, no verbos. El "verbo" (la acción) está determinado por el método HTTP (GET, POST, PUT, DELETE).

## Convenciones de nomenclatura de API

### Usar sustantivos en plural no verbos para los recursos

Los recursos suelen existir como una colección. El uso de plurales mantiene la coherencia de la API, tanto si se recupera un solo elemento como una lista.

```
Mala práctica               Buena práctica

GET  /getUsers              GET  /users

GET  /user/123              GET  /users/123

POST /create-user           POST /users
```

### Usar Kebab-case para las URI

En algunos entornos, las URL distinguen entre mayúsculas y minúsculas. Para evitar confusiones, utilicemos letras minúsculas y guiones (formato kebab). También ayudar para la legibilidad.

```
Mala practica               Buena practica

GET /productCategories      GET /product-categories
```

### Manejo de la jerarquía

Podemos utilizar la anidación para mostrar relaciones, pero evitemos anidar a más de dos niveles. Si la anidación es más profunda, la URI se vuelve difícil de manejar.

```
Mala practica     GET /authors/{authorId}/articles/{articleId}/comments

Buena practica    GET /articles/{articleId}/comments
```

### Nomenclatura de procesos

A veces necesitamos realizar un proceso que no se ajusta perfectamente a las operaciones CRUD, como “activar“, “buscar“ o “calcular“. Hay varias maneras de manejar esto.

```
Manejar los procesos como recursos.

Mala práctica                    Buena práctica

POST /transfer-money             POST /transfers

Utilizar parámetros de consulta para filtrar

Mala práctica                    Buena práctica

GET /getActiveUsers              GET /users?status=active

Usar el patron "Controlador" para procesos genericos

Ejemplos

POST /users/123/activate

POST /loans/calculate-interest

POST /orders/{orderId}/cancel

POST /user/{id}/verification-email

POST /reports/{reportId}/export
```

 

### Versionamiento de la API

El uso del control de versiones en las API es importante para la compatibilidad con versiones anteriores, ya que permite introducir cambios como nuevas funciones o mejoras sin afectar a las aplicaciones existentes.

```
Ejemplos

/api/v1/users

/api/v2/users
```

## Convenciones de documentación de API

### Proporcionar un resumen y una descripción clara

Una documentación clara donde se determina con claridad lo requerido y el resultado a esperar, ayuda a entender y escoger que acción y recurso es el que necesita el desarrollador. Cada (punto de conexión) endpoint debe incluir:

* Resumen (1 frase)  
* Descripción (detalles, reglas, ejemplos)  
* Modelo de solicitud  
* Modelo de respuesta  
* Codigo de error.  
* Ejemplos de éxito y de error.

### 

### Agrupación de puntos de conexión

Utilicemos etiquetas para agrupar los recursos de acuerdo a la lógica del dominio.

 

### Documentación de parámetros.

No solo se trata de nombrar el parámetro, sino una breve descripción y en ciertos casos explicar las restricciones en las que puede afectar a la respuesta. Ejemplo el parámetro “límite”.

### Documentar los códigos de estado HTTP más comunes

* `200` \- OK (Success)  
* `201` \- Created (Resource created)  
* `204` \- No content (Successful deletion?)  
* `400` \- Bad request (Client error: validation failed)  
* `401` \- Unauthorized (Authentication required)  
* `403` \- Forbidden (Authenticated, but no permission)  
* `404` \- Not found (Endpoint or resource not found)  
* `409` \- Conflict  
* `422` \- Unprocessable Entity  
* `429` \- Too Many Request (Rate limiting)  
* `500` \- Internal Server Error

 

### Otras consideraciones.

Asegurarnos que nuestros modelos de solicitud y respuesta son claros y consistentes, especificando el tipo de dato de cada una de sus propiedades y si tiene restricciones.

Indicar qué puntos de conexión ocupan autenticación y de qué tipo.

Todo debe estar documentado, pero debe ser de forma sencilla, al usar los lineamientos la nomenclatura de la API por sí sola ya es auto explicativa. De igual manera solo se debe documentar lo necesario, tomando en cuenta es una guía para el desarrollador no una biblia para el.

 

## Referencias 

A continuacion estan las ligas en las que está basado este documento, la mayoría es la ideología a mi entender de cómo deberían aplicarse los lineamientos y la evolución que a tenido en los ultimo años tomando en cuenta lo que si a funcionado o en varios casos, los que son adaptables al cambio o necesidades propias del proyecto.

* [https://devcenter.heroku.com/articles/platform-api-reference](https://devcenter.heroku.com/articles/platform-api-reference)  
* [https://cloud.google.com/apis/design](https://cloud.google.com/apis/design)  
* [https://opensource.zalando.com/restful-api-guidelines/](https://opensource.zalando.com/restful-api-guidelines/)  
* [https://swagger.io/docs/specification/v3\_0/about/](https://swagger.io/docs/specification/v3_0/about/)  
* [https://swagger.io/resources/articles/best-practices-in-api-design/](https://swagger.io/resources/articles/best-practices-in-api-design/)

