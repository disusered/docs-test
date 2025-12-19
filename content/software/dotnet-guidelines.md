---
title: Lineamientos de desarrollo de software .NET
---

## Descripción

Esta es una recopilación de lineamientos para el desarrollo de backend, organizada por categorías. Estas directrices son independientes del lenguaje de programación y se centran en el impacto en la arquitectura del desarrollo, las operaciones y la dinámica del equipo en las decisiones de código con el propósito de que la retroalimentación se centre en la salud del sistema a largo plazo, en lugar de en preferencias personales.

## Lineamientos

## Diseño y estructura de la arquitectura

Esta categoría se centra en cómo encajan los componentes. Los errores en esta área son los más costosos de corregir posteriormente.

A continuación se muestra la jerarquía de la arquitectura de software y el enfoque de cada una de ellas.

**Arquitectura de software** (Infraestructura y responsabilidades) →  
**Diseño de software** (Modularidad y colaboración) →  
**Patrones de diseño** (Ayudan a implementar la arquitectura definida aplicando modelos establecidos) →  
**Principios del desarrollo de software** (Son guías para la generación del código) →  
**Buenas prácticas** (Son nuestras herramientas para el día a día, para mantener los lineamientos ya definidos para generar un código limpio).

### Separación de responsabilidades

El código debe estar dividido en distintas capas con una responsabilidad específica, como por ejemplo la capa de la lógica de negocio y la capa de acceso a la información.

Al mantener las responsabilidades separadas, cada parte del sistema tiene una única responsabilidad y puede evolucionar de forma independiente. Esto reduce el acoplamiento y aumenta la cohesión.

Ejemplo de una separación de responsabilidades a nivel lógico.

```{code} sh
:caption: Estructura visual

MySolution
└── MyProject.csproj
    ├── Controllers (UI)
    ├── Services (Logic)
    └── Repositories (Data)
```

```{code} csharp
:caption: Como nota adicional cabe mencionar que a pesar de estar en el mismo proyecto el controlador no tiene interacción directa con la capa de datos, la interaccion se da por medio del servicio.

// 1. Capa de datos (Repository) - Gestion de la base de datos
public class UserRepository
{
    public User GetById(int id)
    {
        // Aqui va la logica de comunicacion con la BD
        return new User { Id = id, Name = "Alice" };
    }
}

// 2. Capa de negocio (Service) - Gestiona las reglas
public class UserService
{
    private readonly UserRepository _repo;

    public UserService()
    {
        _repo = new UserRepository();
    }

    public string GetUserStatus(int id)
    {
        var user = _repo.GetById(id);

        // Regla de negocio: Solo Alice esta activa
        if (user.Name == "Alice") return "Active";
        return "Inactive";
    }
}

// 3. Capa de presentacion (UI) - Gestiona la interaccion con el usuario
public class UserController
{
    public void ShowUser(int id)
    {
        var service = new UserService();
        Console.WriteLine($"User Status: {service.GetUserStatus(id)}");
    }
}
```

Ejemplo de separación de responsabilidades a nivel físico.

```
MySolution.sln
 ├── MyProject.Web (UI)      -> Enfocado en la interfaz de usuario
 ├── MyProject.Core (Logic)  -> Enfocado en la logica del negocio/sistema
 └── MyProject.Infra (Data)  -> Enfocado en la comunicacion con la fuente de datos
```

### Arquitectura modular

Al segmentar las funcionalidades en módulos o componentes apropiadamente delimitados, promueve la reusabilidad y claridad dentro del sistema.

La finalidad es que estos módulos pueden ser reemplazados, mejorados o que puedan ser reusados en otros proyectos o sistemas. Un ejemplo puede ser la funcionalidad de cobros por X banco, este módulo debería ser reusable en otros proyectos o sistemas.

Aquí nos enfocaremos al paradigma AOP (Programación Orientada a Aspectos), donde separaremos módulos enfocados a logs, seguridad, transacciones, etc; de la lógica de negocios. Esto reduce el código repetitivo y facilita el mantenimiento y a la comprensión del sistema.

```{code} shell
:caption: Un ejemplo de un proyecto de presentación cuando la codificación está en base a modulos o componentes.

PuntoDeVenta.csproj
 ├── Modules
 │    ├── Sales (Ventas) <- Modulo de ventas
 │    │    ├── Controllers
 │    │    ├── Services
 │    │    ├── Data (DbContext propio)
 │    │    └── Contracts (Interfaces públicas)
 │    │
 │    └── Inventory (Inventario) <- Modulo de invetario
 │         ├── Controllers
 │         ├── Services (Internal)
 │         └── Data
 └── Shared <- Componentes de uso comun (listas, formas, etc)
```

#### Ejemplo en base a microservicios / micromonolitos

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/microservices.svg
:name: fig-microservices
:width: 100%

Diagrama de microservicios / micromonolitos — [Tamaño completo](/diagrams/microservices.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/microservices@4x.png
:name: fig-microservices-print
:width: 100%

Diagrama de microservicios
```
+++

#### Ejemplo basado en DDD (Domain driven design)

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/ddd.svg
:name: fig-ddd
:width: 100%

Diagrama de DDD — [Tamaño completo](/diagrams/ddd.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/ddd@4x.png
:name: fig-ddd-print
:width: 100%

Diagrama de DDD
```
+++

### Implementar patrones de diseño

Estos son guías de sobre cómo se diseñan las clases, las interfaces y los módulos, ayudan a crear sistemas que son mantenibles (SOLID), fomentar la simplicidad para evitar la complejidad innecesaria (KISS) y desanima la optimización prematura o la implementación de funciones antes de que sean necesarias (YAGNI).

Como los ejemplos previamente mencionados estos solo están basados en principios de programación, los cuales son fundamentales para que los patrones de diseño funcionen, los siguientes patrones por si solo muestran cómo estos principios son aplicados, pero a una jerarquía más alta.

El patrón de repositorio, la finalidad de este patrón es separar la lógica del acceso a datos con la lógica del dominio.

El patrón de estrategias, la finalidad de este patrón es poder separar varios procesos, acciones o servicios que tienen su propia lógica y reglas pero una misma funcionalidad, el ejemplo más común son las formas de pago, donde tienes una estrategia para cada tipo de pago.

Un ejemplo más complejo podría ser el State Management que usa varios patrones (command, observer, singleton and facade, entre otros) y la razón de esto es por es usado para mantener la coherencia de los datos, compartir datos entre componentes, manejar la interacción del usuario y facilitar el escalado.

Esto ayuda a tener menos bichos, deuda técnica ya que estos ayudan a que los desarrolladores tomen mejores decisiones y de forma natural diseñen con mayor criterio.

### Convención sobre configuración

La idea es utilizar valores predeterminados adecuados para minimizar la necesidad de configuración explícita. Esto ayuda a la consistencia entre servicios.

Reduce el código repetitivo y la fatiga de toma de decisiones; los desarrolladores solo necesitan especificar cuándo se desvían del estándar.

Este lineamiento explica la importancia de estos, ya que por ejemplo al tener ya definidos, el nombre de las carpetas, su estructura, los patrones de nomenclatura, etc. Reduce el esfuerzo, la duplicidad e incrementa la consistencia a través de todo nuestro proyecto.

El enfoque de este lineamiento es…

- Reducir código, evitar la configuración excesiva.
- El desarrollador puede cambiar de proyecto y saber dónde está todo.
- Clases, controladores, rutas y ciertas configuraciones ya están automatizadas o predefinidas y no hay necesidad de preocuparse por ello.
- Los valores/configuraciones default evitan errores manuales

```{code} csharp
:caption: Algunos ejemplos basados en C#

// Antes de CoC necesitabamos configurar cada ruta de manera individual

endpoints.MapControllerRoute(
  name: "GetProducts",
  pattern: "api/products/get",
  defaults: new { controller = "Products", action = "Get" }
);

// Despues de CoC, el Framework (ASP.NET) automaticamente mapea la ruta /Products/Get si seguimos la siguiente convencion

public class ProductsController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => ...
}

/*****************************************************************************/

// Antes de CoC teniamos de mapear de forma manual y especifica el nombre de la tablas  y sus relaciones

modelBuilder.Entity<Product>().ToTable("Product");
modelBuilder.Entity<Product>()
    .Property(p => p.Id)
    .HasColumnName("Id");

// Despues de CoC en EF automaticamente detecta el nombre de la tabla, su llave primaria y llaves foraneas. Solo debemos hacer configuraciones cuando es necesario (el cual deberia ser minimo y en una cituacion mus especifica)

public class Product
    {
        public int Id { get; set; } // Primary Key by convention
        public string Name { get; set; }
        public decimal Price { get; set; }
        public DateTime CreatedDate { get; set; }
    }

/*****************************************************************************/

// Otro ejemplo donde ejemplifica el valor de este lineamiento es el siguiente, Al utilizar una clase base evita el codigo repetitivo, utiliza un estandar que la mayoria de los desarrolladores conoce

 public class ProductRepository : GenericRepository<Product>
 {
     public ProductRepository(DbContext dbContext) : base(dbContext)
     {
     }
 }
```

## Calidad y mantenibilidad del código

Debemos garantizar que el código sea legible por humanos, no solo ejecutable por máquinas.

### _Prácticas de código limpio_

El código debe ser legible, comprensible y mantenible. Un código limpio es la base de cualquier sistema estable; un código desordenado acumula deuda técnica.

Esta práctica ayuda a comprender el funcionamiento del código; y por tanto reduce la posibilidad de cometer errores. Esto ayuda a que un código heredado sea más fácil de actualizar, transformar y ampliar.

#### Ejemplos de código limpio

```{code} csharp
:caption: Nombres claros y expresivos

// Lo malo: codigo ilegible.

var x = Get();
var y = x.Count();

// Lo bueno: Codigo legible

List<Invoice> pendingInvoices = GetPendingInvoices();
int quantityOfPendingInvoices = pendingInvoices.Count();

```

```{code} csharp
:caption: Funciones pequeñas y con responsabilidad única

// Lo malo: el codigo hace muchas cosas

public void ProcessOrder(Order order)
{
    if (order.Total <= 0) throw new Exception("Invalid");
    order.Status = "Processed";
    _repository.Save(order);
    _logger.Log("Order processed");
}

// Lo bueno: separa en funciones pequeñas y especificas

public void ProcessOrder(Order order)
{
    Validate(order);
    MarkAsProcessed(order);
    Save(order);
}

private void Validate(Order order)
{
    if (order.Total <= 0)
    {
        throw new InvalidOperationException(
"Order total must be greater than zero.");
    }
}

private void MarkAsProcessed(Order order)
{
    order.Status = "Processed"; <-- // Aqui deberiamos utilizar una constante.
}

private void Save(Order order)
{
    _repository.Save(order);
    _logger.Log("Order processed"); <-- // Deberiamos de indicar el nivel de log
}
```

```{code} csharp
:caption: Evitar valores magicos y centralizar sus valores para su mejor mantenimiento

// Lo malo, valores magicos

if (age > 65)
{
     discount = 0.20;
     displayMessage = "Senior discount";
}

// Lo bueno, valores constantes

const int SENIOR_AGE_THRESHOLD = 65;
const double SENIOR_DISCOUNT_RATE = 0.20;const string SENIOR_DISCOUNT_MESSAGE = "Senior discount";

if (age > SENIOR_AGE_THRESHOLD)
{
 discount = SENIOR_DISCOUNT_RATE;
 displayMessage = SENIOR_DISCOUNT_MESSAGE;
}
```

```{code} csharp
:caption: Uso correcto de excepciones, no debemos ocultar los errores, debemos mostrarlos o logearlos para poderlos resolver.

// Lo malo
if (costumer == null)
{
 return null;
}

// Lo bueno
if (costumer == null)
{
 throw new ArgumentNullException(nameof(customer));
}
```

```{code} csharp
:caption: Codigo defensivo, en algunas ocaciones no debemos generar errores, debemos estar listos para algunos escenarios que pueden desde un inicio ser manejados

// Lo malo, no aplicar la ley de Murphy.

public decimal CalculateTotal(Order order)
{
 return order.Items.Sum(x => x.Price);
}

// Lo bueno, aplicando programacion defensiva en base a la ley de Murphy

public decimal CalculateTotal(Order order)
{
 if (order?.Items == null || !order.Items.Any())
 {
  return 0.0;
 }

 return order.Items.Sum(x => x.Price);
}
```

```{code} csharp
:caption: Evitar el anidamiento profundo

// Lo malo, demaciados ifs

if (user != null)
{
    if (user.Address != null)
    {
        if (user.Address.City != null)
        {
            Send(user.Address.City);
        }
    }
}

// Lo bueno, simplicar la expresion

if (user?.Address?.City is null)
    return;

Send(user.Address.City);
```

```{code} csharp
:caption: Debemos comentar el codigo solo cuando agrega valor

// Lo malo, el codigo es intuitivo por lo cual no necesita un comentario// Asginar los valores iniciales para el recorrido de la tabla
int columnIndex = 0;
int rowIndex = 0;

// Lo bueno, se explica que se esta validando y por que.
// Regla de negocio: todos los usuario premium deben tener un descuento mayor a 10%
if (user.IsPremium && user.Discount < 10)
{
 throw new InvalidOperationException("Invalid premium discount.");
}
```

```{code} csharp
:caption: Simplificar el codigo (sin abusar)

// Lo malo, en ciertos casos aunque el codigo este estructurado y legible, es posible simplificarlo

var result = new List<User>();
foreach (var u in users)
{
    if (u.IsActive)
    {
        result.Add(u);
    }
}

// Lo bueno, simplicar el codigo con el uso de LINQ
var activeUsers = users.Where(u => u.IsActive).ToList();
```

### _Nombres, formato y estilo coherentes_

Al adoptar un estilo uniforme en todo el código mejora la legibilidad y reduce la carga cognitiva ya que ayuda a que los desarrolladores puedan analizar y revisar el código rápidamente.

Al haber menos discrepancias de estilo hace que la revisión del código sea más amena y precisa.

```{code} csharp
:caption: Ejemplos de nomenclatura. Para mayor informacion: [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/)

// Para las clases, interfaces y enums usamos PascalCase

public class UserManager {}
public interface IRepository {}
public enum OrderStatus {}

// Para los metodos y funciones tambien usamos PascalCase

public void GetData() {}
public void CalculateTotal() {}

// Para las variables y paremetros usamos camelCase

int customerCount;
string emailAddress;

// Para los campos privados usamos camelCase precedidos por guiones bajos.

private int _orderCount:
private readonly ILogger _logger;

// Para constantes usamos SnakeCase en mayusculas

private const int MAX_VALUE = 999;

// Debemos evitar abbreviaturas

int quantity; // No usar qty
int address; // No usar addr

// Para la documentacion de cambios usaremos mensajes semanticos

// El formato es el siguiente y el titulo no debe pasar de los 80 caracteres, pero en situaciones muy excepcionales que no pase de los 120
// <tipo> (opcional:<alcance>): <descripcion>

// Para la documentacion de cambios hacia main y simplificar todos los comenatarios usaremos el formato siguiente haciendo un squash commit
// <tipo> (optional:<alcance>): <descripcion>
// [optional cuerpo]

// El alcance es opcional pero recomendamos agregarlo siempre que sea posible.

feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.

// *** Tipos y cuando  usarlos *** //
// feat: (nueva funcion para el usuario, no una nueva funcion para el script de compilacion)
// fix: (correccion de error para el usuario, no una correccion para un script de compliacion)
// docs: (cambios en la documentacion)
// style: (formato, omision de punto y coma, etc.; sin cambios en el codigo de produccion)
// refactor: (optimizacion del codigo de produccion, utilizando el principio de boy scout)
// test: (añadir pruebas, optimizar pruebas; no son cambios en el codigo de produccion)
// chore: (actualizar tareas rutinarias, actualizacion de dependencias, etc.)
```

```{code} csharp
:caption: Ejemplos de formato

// El separador de codigo va en una linea nueva, como el siguiente codigo lo muestra la llave esta en la siguiente linea.

public void Execute()
{
    Console.WriteLine("Running");
}

// Usar identacion (4 espacios)

if (condition)
{
    Console.WriteLine("Invalid");
}

// Usar lineas en blanco para separar la logica en secciones

public void Register(User user)
{
    Validate(user);

    _repository.Save(user);

    _logger.Log("User registered");
}

// Para una linea muy larga de codigo, podemos hacerla mas legible al romperla en multiples lineas cuando es posible

var users = await db.Users.Include(u => u.Orders).ToListAsync();

var users = await db.Users
    .Include(u => u.Orders)
    .ToListAsync();

// La estructura de archivo, debe tener el siguiente orden, esto ayuda a evitar utilizar regiones para seccionar el código. A continuación se enumera el orden.

// Using statements, Namespace, Class, Fields, Constructors, Properties, Methods (public first, then private)

using System;

namespace CleanCodeDemo
{
    public class UserManager
    {
        private readonly IUserRepository _repository;

        public UserManager(IUserRepository repository)
        {
            _repository = repository;
        }

        public User GetUser(int id)
        {
            return _repository.GetById(id);
        }
    }
}
```

```{code} csharp
:caption: Ejemplos de guias de estilo

// Utilizar el tipo de dato explicito procurando la claridad de codigo.

List<Order> items = Get();List<User> active = GetActiveUsers();

// Utilizar var cuando el tipo de dato es obvio

var user = new User();
var customers = new List<Customer>();

// Siempre usar llaves para las condiciones y bucles aunque solo sea una linea

if (items.Any())
{
 return items;
}

// Codificar el codigo para el retorno temprano

// Ejemplo antes

if (user != null)
{
    if (user.IsActive)
    {
        Process(user);
    }
}

// Al enfocarnos en el retorno temprano reducimos codigo anidado.

if (user == null || !user.IsActive)
    return;

Process(user);

// Evitar una lista larga de parametros, (no mas de 4)

public void Create(string name, string lastname, string email, int age, string city, bool active)

public void Create(CreateUserRequest request)

// Un archivo por clase

// El codigo y los commits seran en ingles
```

### _Evitar malas prácticas y código muerto_

Al identificar y eliminar las malas prácticas como son la lógica duplicada, funciones extensas, código sin usar por mencionar unas ayuda a la eficiencia y rapidez del desarrollo, ayuda a tener menos mantenimiento, menor riesgo de regresión, mejor arquitectura.

El código muerto (código inusitado, inalcanzable o comentado) genera más carga de mantenimiento y en otras ocasiones puede conducir a suposiciones falsas y errores. Hay que recordar que el código comentado no es documentación.

Hay que tener en cuenta, que también exagerar en las buenas prácticas puede ser contraproducente, ya que puede complicar la complejidad del código, la optimización constante del código no siempre trae valor al producto (costo \- beneficio), en muchas casos crea mini clases que podrían estar encapsuladas en una clase o en un solo archivo.

Las pruebas son importantes pero también exagerar en las pruebas reduce la velocidad de las liberaciones y por tanto va en contra de la programación ágil.

Las buenas prácticas nos sugieren que hacer en ciertos escenarios, pero debemos entender cuándo y cómo usarlas. Cuando el escenario es muy trivial pueden ser ignorados tanto una buena práctica como las pruebas, o cuando estas pueden causar conflictos, ejemplo de un DRY, puede generar acoplamiento no deseado, o probar algo trivial y realizar las pruebas completas de regresiones para cambios de texto no son beneficiosos.

## Rendimiento y escalabilidad

El rendimiento se centra en la velocidad y la capacidad de respuesta de un sistema en un momento dado, mientras que la escalabilidad se refiere a su capacidad para gestionar cargas de usuarios o volúmenes de datos crecientes sin que se produzca una degradación. La importancia en el rendimiento garantiza una buena experiencia de usuario y en la escalabilidad permite asegurar que el sistema pueda crecer y adaptarse a las demandas futuras sin necesidad de una revisión completa.

### _Optimizar el acceso a la base de datos_

Debemos implementar consultas eficientes y minimizar la recuperación innecesaria de datos, las consultas mal optimizadas degradan el rendimiento y aumentan los costos. Esto da como resultado tiempos de respuesta más rápidos, menor consumo de recursos permitiendo la escalabilidad, rentabilidad y capacidad de crecimiento.

```{code} csharp
:caption: En codigo de backend estas son algunas recomendaciones para la optimizacion a la BD // Evitar consultas N+1

// Codigo que genera demaciadas llamadas a la BD
var users = await db.Users.ToListAsync();

foreach (var user in users)
{
    user.Orders = await db.Orders
        .Where(o => o.UserId == user.Id)
        .ToListAsync();
}

// Codigo simplificado que regresa el mismo resultado con una sola llamada

var users = await db.Users
    .Include(u => u.Orders)
    .ToListAsync();

// Usar batch inserts tambien reduce el numero de llamadas a la BD

foreach (var item in items)
{
    await db.Items.AddAsync(item);
    await db.SaveChangesAsync();
}

// Mejor

await db.Items.AddRangeAsync(items);
await db.SaveChangesAsync();
```

```{code} csharp
:caption: Evitar el buffet de datos... solo debemos consultar la informacion necesaria

// Evitar esto
var products = await db.Products.ToListAsync();

// Cambiarlo por esto
var products = await db.Products
    .Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    })
    .ToListAsync();
```

:::{note}
Este también es un claro ejemplo de exageración de buenas practicas, pero he lo puesto para fines de ejemplo. La recomendación para este lineamiento es cuando hacemos uniones a diferentes tablas y solo necesitamos la información de unos cuantos campos
:::

Al usar `AsNoTracking()` el query es mas rápido y reduce el uso de memoria (entre un 40% y 50%), ya que no tiene que estar pendiente a cambios en la información.

Al utilizar los métodos async evita el bloqueo de los hijos que consultan la BD.

```{code} csharp
:caption: Usar AsNoTracking() cuando solo estamos consultando la informacion. Y usar async siempre en las consultas.
var customers = await db.Customers
    .AsNoTracking()
    .ToListAsync();
```

Es recomendable usar una consulta TSQL cuando el query es muy complejo y/o largo, las consultas de los reportes ya que estos pueden impactar al rendimiento de la BD.

```{code} csharp
:caption: Para escenarios complejos usar TSQL directamente
var users = await connection.QueryAsync<User>(
    "SELECT Id, Name FROM Users WHERE IsActive = 1");
```

```{code} sql
:caption: Optimizacion de consultas de TSQL

// Cuando sea necesario evitar seleccionar todos los campos (reduce el I/O), este es recomendable para consultas largas

SELECT OrderId, TotalAmount, CreatedAt
FROM Orders
WHERE CustomerId = @id;
```

En columnas que son utilizadas constantemente en los `WHERE`, `JOIN` y `ORDER BY`. Esto ayuda a evitar el escaneo completo de las tablas, sobrecargar el procesamiento y evita timeouts por carga

```{code} sql
:caption: Utilizar indices cuando es necesario
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
```

```{code} sql
:caption: Utlizar indices de cobertura para evitar la sobre indexacion. Esto ayuda a evitar busquedas innecesarias e incrementa el rendimiento.
CREATE INDEX IX_Orders_CustomerId_Amount
ON Orders (CustomerId)
INCLUDE (OrderId, Amount, CreatedAt);
```

Ayuda a evitar tener logs inmensos, reduciendo así el uso del espacio en disco. Aumenta el rendimiento del query y simplifica la lógica.

```{code} sql
:caption: Evitar consultas que generen mutiples transacciones.
// Este query realiza demasiadas transacciones
DECLARE order_cursor CURSOR FOR
SELECT Id FROM Orders

OPEN order_cursor;
FETCH NEXT FROM order_cursor...
 // SET order to status pending if the status is processed
...

// Este query hace lo mismo en una consulta mas simple.

UPDATE Orders
SET Status = 'Processed'
WHERE Status = 'Pending';
```

Ayuda a la legibilidad de la consulta ya que puedes seccionar la consulta en pequeños bloques. También ayudar a minimizar el mundo de datos, ya que vas filtrando la información antes de las uniones. Es eficiente cuando necesitas utilizar consultas por jerarquía o que necesitan recursividad. Es recomendado para su uso en la paginación.

Al utilizar CTE generamos un mejor plan de ejecución, evitar tener subqueries duplicados, el motor de BD optimiza cada bloque de manera independiente, reduce el uso de memoria, es mas rápido que los bucles, cursores y mas eficiente que las tablas temporales en la mayoría de los casos.

```{code} sql
:caption: Utilizar CTE
// Este es un ejemplo de prefiltrado antes del joinWITH FilteredOrders AS (
    SELECT OrderId, CustomerId, ProductId, Total
    FROM Orders
    WHERE CreatedAt >= DATEADD(day, -7, GETDATE())
)
SELECT fo.OrderId, fo.Total, c.Name
FROM FilteredOrders fo
JOIN Customers c ON fo.CustomerId = c.CustomerId
JOIN Products p ON fo.ProductId = p.ProductId
WHERE p.Category = 'Electronics';

// Estos son unos ejemplos para la segmentacion y la paginacion
WITH OrderedOrders AS (
    SELECT
        OrderId, Total, CreatedAt,
        ROW_NUMBER() OVER (ORDER BY OrderId) AS RowNum
    FROM Orders
)
SELECT OrderId, Total, CreatedAt
FROM OrderedOrders
WHERE RowNum BETWEEN @Skip AND @Skip + @Take - 1;

// o se puede escribir WHERE RowNum BETWEEN @Offset AND @Offset + @PageSize - 1;
```

```{code} sql
:caption: Este es un ejemplo para la recursividad
WITH CategoryHierarchy AS (
    SELECT Id, ParentId, 0 AS Level
    FROM Categories
    WHERE ParentId IS NULL

    UNION ALL

    SELECT c.Id, c.ParentId, ch.Level + 1
    FROM Categories c
    JOIN CategoryHierarchy ch ON c.ParentId = ch.Id
)
SELECT * FROM CategoryHierarchy;
```

```{code} sql
:caption: Este es un ejemplo que evita query duplicados o demasiadas subconsultas logica repetida y quera un plan de ejecucion lento y el CTE resuelve todo eso
SELECT
    (SELECT AVG(Price) FROM Products WHERE CategoryId = p.CategoryId) AS AvgPrice,
    (SELECT COUNT(*) FROM Products WHERE CategoryId = p.CategoryId) AS TotalCount
FROM Products p;

WITH CategoryStats AS (
    SELECT
        CategoryId,
        AVG(Price) AS AvgPrice,
        COUNT(*) AS TotalCount
    FROM Products
    GROUP BY CategoryId
)
SELECT
    p.Name,
    c.AvgPrice,
    c.TotalCount
FROM Products p
JOIN CategoryStats c ON p.CategoryId = c.CategoryId;
```

Evitar el casteo/formateo en la consulta, esto debe hacerse en el backend si es para la lógica de negocios o en el frontend si es estático.

```{code} sql
/* SQL (Malo)*/
SELECT
    Id,
    CASE
        WHEN Status = 1 AND Amount > 100 THEN 'HIGH'
        WHEN Status = 1 AND Amount <= 100 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS RiskLevel,
    UPPER(CustomerName) AS CustomerUpper
FROM Orders
WHERE YEAR(OrderDate) = @year;

/* SQL y Backend (Bueno) */
SELECT Id, Status, Amount, CustomerName, OrderDate
FROM Orders
WHERE OrderDate >= @startDate AND OrderDate < @endDate;

public string GetRiskLevel(Order o)
{
    if (o.Status == 1 && o.Amount > 100) return "HIGH";
    if (o.Status == 1) return "MEDIUM";
    return "LOW";
}
```

```{code} sql
:caption: Los casteos se pueden hacer en la capa de presentacion
/* SQL (Malo) */
WITH RecentOrders AS (
    SELECT
        CAST(OrderDate AS VARCHAR(10)) AS DateString,
        CAST(Total AS DECIMAL(10,2)) AS TotalFormatted,
        CustomerId
    FROM Orders
    WHERE YEAR(OrderDate) = YEAR(GETDATE())
)
SELECT * FROM RecentOrders;
```

Estos es para mantener el principio de la responsabilidad única

- **Base de datos**: Guarda y extrae información
- **Backend**: reglas de negocio, trasformación de datos
- **Frontend**: Formato y presentación

Es común castear la fecha de creación, pero algunas buenas practicas indican que este campo puede ser utilizado como un indice de cobertura por lo cual es una de las razones de la observación anterior

```{code} sql
:caption: NUNCA castear o converting columnas indexadas
SELECT *
FROM Users
WHERE CAST(CreatedAt AS DATE) = '2025-01-01'; // Esto evitar utilizar la columna indexada
```

### _Usar almacenamiento en caché_

Al almacenar la información que tiene un uso frecuente en una capa de acceso más rápido (memoria, almacenamiento en memoria) reduce la latencia y la carga en las bases de datos generando respuestas más rápidas a solicitudes repetidas o comunes permitiendo gestionar una mayor carga con menores costos de infraestructura.

Se recomienda usar caché en los siguientes escenarios:

- La información rara vez cambia
- Se consulta con frecuencia
- Su plan de ejecución es pesado o complejo

Se recomienda NO usar caché en los siguientes escenarios:

- La información es dinámica o sufre cambios constantemente
- Son casos muy específicos (de usuario, cliente, etc) que necesitan información altamente personalizada
- Cuando las BD / Tablas son demasiado pesadas
- Cuando es para sistemas de tiempo real (transacciones de banco)

```{code} csharp
:caption: Podemos usar MemCache para applicaciones de una sola instancia (no distribuida)
public async Task<List<Product>> GetProducts()
{
    if (_cache.TryGetValue("products", out List<Product> cached))
        return cached;

    var products = await db.Products.ToListAsync();

    _cache.Set("products", products, TimeSpan.FromMinutes(10));

    return products;
}
```

```{code} csharp
:caption: Podemos usar cache distribuido (Redis) para microservicios o sistemas escalables
public async Task<Product?> GetProduct(int id)
{
    var key = $"product-{id}";
    var cached = await _cache.GetStringAsync(key);

    if (cached != null)
        return JsonSerializer.Deserialize<Product>(cached);

    var product = await db.Products.FindAsync(id);

    if (product != null)
        await _cache.SetStringAsync(
            key,
            JsonSerializer.Serialize(product),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
            });

    return product;
}
```

O podemos usar el patron Cache Aside (Recomendado)

+++ {"tags": ["no-pdf"]}

```{figure} /diagrams/cache-aside.svg
:name: fig-cache-aside
:width: 100%

Diagrama de patron Cache Aside — [Tamaño completo](/diagrams/cache-aside.svg)
```

+++

+++ {"class": "no-web"}

```{figure} /diagrams/cache-aside@4x.png
:name: fig-cache-aside-print
:width: 100%

Diagrama de patron Cache Aside
```
+++

En código se vería así:

```{code} csharp
public async Task<Product?> GetProductAsync(int id)
{
    string key = $"product:{id}";

    // 1. Try get from cache
    var cached = await _cache.GetStringAsync(key);
    if (cached != null)
        return JsonSerializer.Deserialize<Product>(cached);

    // 2. Cache miss → Load from DB
    var product = await _db.Products
                          .AsNoTracking()
                          .FirstOrDefaultAsync(p => p.Id == id);

    if (product == null)
        return null;

    // 3. Save to cache for next reads
    var data = JsonSerializer.Serialize(product);

    await _cache.SetStringAsync(
        key,
        data,
        new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
        });

    // 4. Return result
    return product;
}
```
