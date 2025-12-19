---
title: Estándares Generales de Código en .NET
---

# Convenciones de Nombres

La consistencia en los nombres reduce la carga cognitiva. Seguimos las pautas estándar de Microsoft .NET con una rigurosidad específica aplicada a los patrones Async y API.

**Estándares Generales de C\#**

- **PascalCase:** Usar para _Class_, _Record_, _Struct_, _Method_, _Property_ y _Enum_.
- **camelCase:** Usar para _localVariable_, _methodParameter_ y _private \_field_.
- **Interfaces:** Deben comenzar con una I mayúscula.

# Código Limpio

Mantener la base de código limpia ayuda en las revisiones de código y reduce los _merge conflicts_.

**Configurar Auto Formato al guardar:**

_Tools \-\> Options \-\> Text Editor \-\> Code Cleanup \-\> Select Profile 1_

**Modificadores de Acceso Explícitos**

No confíes en los modificadores de acceso por defecto. Sé explícito para evitar la exposición accidental de lógica interna.

**Mal:**

```{code} csharp
class UserService // Defaults to internal
{
    string _connectionString; // Defaults to private
}
```

**Bien:**

```{code} csharp
public class UserService
{
    private readonly string _connectionString;
}
```

**Uso de Var**

Usa _var_ solo cuando el tipo sea explícitamente obvio desde el lado derecho de la asignación. Si el tipo no es obvio, decláralo explícitamente.

**Mal:**

```{code} csharp
var result = _service.GetData(); // Cual es el resultado? Un int? Una lista? Un usuario?
```

**Bien:**

```{code} csharp
var user = new User(); // Obvio
List<User> users = _service.GetData(); // Explicito
```

# Backend (Web API)

# Arquitectura de Controladores

El Controlador es la "Puerta de Entrada" de tu backend. Su única responsabilidad es recibir una solicitud, validar el protocolo (HTTP), delegar el trabajo a un servicio y devolver la respuesta HTTP apropiada.

## El Principio del "Controlador Delgado" (_Thin Controller_)

**Regla:** Los controladores no deben contener Lógica de Negocio ni lógica de Acceso a Datos.

- **Por qué:** Poner lógica en los controladores hace imposible realizar pruebas unitarias de esa lógica sin levantar un contexto HTTP. También viola el Principio de Responsabilidad Única.
- **Implementación:** Inyectar un Servicio para manejar el procesamiento real.

**Mal (Controlador Robusto):**

```{code} csharp
[HttpPost]
public async Task<IActionResult> CreateUser(UserDto dto)
{
    // LOGICA EN CONTROLLADOR - EVITAR ESTO
    if (string.IsNullOrEmpty(dto.Email)) return BadRequest();

    var user = new UserEntity { Email = dto.Email };
    _dbContext.Users.Add(user); // Acceso directo a BD
    await _dbContext.SaveChangesAsync();

    return Ok(user);
}
```

**Bien (Controlador Delgado):**

```{code} csharp
[HttpPost]
public async Task<ActionResult<UserDto>> CreateUser(UserDto dto)
{
    // Delegar a la capa de servicios
    var result = await _userService.CreateUserAsync(dto);

    // Mapear resultado a un estatus HTTP
    return CreatedAtAction(nameof(GetUser), new { id = result.Id }, result);
}
```

## Valores de Retorno Tipados (_ActionResult\<T\>_)

Dado que nuestro Cliente Blazor está en una solución separada, confiamos en OpenAPI (Swagger) para generar nuestro código de cliente.

**Regla:** Usa siempre ActionResult\<T\> en lugar de _IActionResult_.

- **Por qué:** _IActionResult_ oculta el tipo de retorno. Swagger no puede ver qué objeto se devuelve, por lo que genera un _System.Object_ genérico en el cliente Blazor. _ActionResult\<UserDto\>_ le dice a Swagger exactamente cuál es el esquema, permitiendo al generador crear una clase _UserDto_ tipada en el proyecto cliente.

**Mal (Oculta el Esquema):**

```{code} csharp
public async Task<IActionResult> GetProduct(int id) { ... }
```

**Bien (Expone el Esquema):**

```{code} csharp
[ProducesResponseType(StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<ActionResult<ProductDto>> GetProduct(int id) { ... }
```

# Acceso a Datos y Mejores Prácticas de LINQ

En una Web API, LINQ no es solo una forma de filtrar listas; es un Generador de SQL.

Cada línea de código LINQ que escribes contra un DbSet se traduce en un comando SQL enviado a la base de datos.

## La Regla de Oro: Proyectar siempre a DTOs

Nunca devuelvas una Entidad de Entity Framework (por ejemplo, _UserEntity_) directamente desde un servicio o controlador. Siempre proyéctala a un Objeto de Transferencia de Datos (DTO) dentro de la consulta misma.

**¿Por qué?**

- **Seguridad:** Las entidades a menudo contienen datos sensibles (Hashes de contraseñas, Flags Internos) que nunca deben salir del servidor.
- **Rendimiento:** `SELECT *` obtiene todas las columnas. Las proyecciones obtienen solo las columnas que necesitas.
- **Serialización:** Las entidades a menudo tienen referencias circulares (Usuario \-\> Pedidos \-\> Usuario) que bloquean los serializadores JSON.

**Mal (Materializando Entidades):**

```{code} csharp
// Obtiene TODAS las columnas (Password, InternalId, etc.) from DB
// Obtiene TODOS los registros en memoria antes de filtrar
var users = await _context.Users.ToListAsync();
return users.Select(u => new UserDto { Name = u.Name });
```

**Bien (Proyectando a DTO):**

```{code} csharp
// Genera SQL: SELECT Name, Email FROM Users WHERE IsActive = 1
var users = await _context.Users
    .Where(u => u.IsActive)
    .Select(u => new UserDto
    {
        Name = u.Name,
        Email = u.Email
    })
    .ToListAsync(); // La materialización sucede al ÚLTIMO
return users;
```

## IQueryable vs. IEnumerable

Entender la diferencia entre estas interfaces es vital para el rendimiento.

- **`IQueryable`**: Representa una consulta que **aún no se ha ejecutado**. Los filtros aplicados aquí se convierten en cláusulas `WHERE` de SQL.
- **`IEnumerable`**: Representa datos ya en memoria. Los filtros aplicados aquí se ejecutan en la CPU del servidor web, no en la base de datos.

**La Trampa de la "Materialización Prematura":** Llamar a _.ToList()_ o _.AsEnumerable()_ demasiado pronto detiene la generación de SQL y carga todo en la memoria.

**Mal:**

```{code} csharp
// 1. Ejecuta SQL: SELECT * FROM Products
var allProducts = _context.Products.ToList();
// 2. Filtra 100,000 registros en memoria del servidor Web
var expensiveProducts = allProducts.Where(p => p.Price > 1000).ToList();
```

**Bien:**

```{code} csharp
// 1. Builds Query definition (No SQL sent yet)
var query = _context.Products.AsQueryable();
// 2. Appends SQL WHERE clause
query = query.Where(p => p.Price > 1000);
// 3. Executes SQL: SELECT * FROM Products WHERE Price > 1000
var expensiveProducts = await query.ToListAsync();
```

## El Problema N+1

El problema "N+1" ocurre cuando obtienes una lista de elementos (1 consulta) y luego iteras sobre ellos para obtener datos relacionados (N consultas).

**Mal (Consultas en Bucle):**

```{code} csharp
// Consulta 1: Obtener 100 ordenes
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    // Consulta 2...101: Viaje de vuelta a la BD por cada orden
    var customer = _context.Customers.Find(order.CustomerId);
    order.CustomerName = customer.Name;
}
```

**Bien (Carga Anticipada / Eager Loading):** Usa _.Include()_ para obtener datos relacionados en una sola consulta JOIN optimizada.

```{code} csharp
// Query 1: SELECT * FROM Orders LEFT JOIN Customers ...
var orders = await _context.Orders
    .Include(o => o.Customer)
    .ToListAsync();
```

**Mejor (Proyección \- Recomendado):** Si usas _.Select()_, EF Core crea automáticamente el JOIN eficiente sin necesidad de _.Include()._

```{code} csharp
var dtos = await _context.Orders
    .Select(o => new OrderDto
    {
        OrderId = o.Id,
        CustomerName = o.Customer.Name // EF crea el JOIN automaticamente aquí
    })
    .ToListAsync();
```

## No-Tracking para Operaciones de Lectura

Por defecto, Entity Framework "rastrea" cada objeto que obtiene para poder detectar cambios para actualizaciones. Esto tiene una sobrecarga significativa.

Para solicitudes API GET donde solo estás devolviendo datos y no modificándolos, desactiva esto.

**Regla:** Usa _.AsNoTracking()_ para todas las consultas de solo lectura.

```{code} csharp
// Faster, uses less memory
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.Category == "Tech")
    .ToListAsync();
```

## Ejecución Asíncrona

Nunca bloquees el hilo en una Web API. Usar _.Result_ o _.Wait()_ puede causar agotamiento del _thread pool_ y bloqueos (_deadlocks_).

**Mal:**

```{code} csharp
var users = _context.Users.ToList(); // Synchronous - blocks the thread
```

**Bien:**

```{code} csharp
var users = await _context.Users.ToListAsync(); // Asynchronous - frees thread while waiting for DB
```

# Programación Defensiva de API

La programación defensiva en el backend trata de asegurar la estabilidad y seguridad independientemente de la entrada que se reciba. **Nunca confíes en los datos enviados desde el cliente**.

## Cláusulas de Defensa (_Guard Clauses_)

Falla rápido. Si un método recibe argumentos inválidos, debe fallar inmediatamente (o devolver un error) en lugar de intentar procesar datos parciales.

- **Uso:** Verifica nulos y cadenas vacías en la parte superior de tus métodos de Servicio o Controlador.
- **C\# Moderno:** Usa el estático ArgumentNullException.ThrowIfNull(...) disponible en .NET 6+.

**Mal ("Camino Feliz" Anidado):**

```{code} csharp
public async Task UpdateUserAsync(int id, UserDto dto)
{
    if (dto != null)
    {
        var user = await _repo.GetAsync(id);
        if (user != null)
        {
            // Lógica de actualización...
        }
    }
}
```

**Bien (Cláusulas de Defensa / "Retorno Temprano"):**

```{code} csharp
public async Task UpdateUserAsync(int id, UserDto dto)
{
    // 1. Defiende contra mal input inmediatamente
    ArgumentNullException.ThrowIfNull(dto);

    // 2. Defiende contra datos faltantes
    var user = await _repo.GetAsync(id);
    if (user == null)
    {
        throw new EntityNotFoundException("User", id);
    }
    // 3. Happy Path (No necesita identación)
    user.Update(dto);
    await _repo.SaveAsync();
}
```

## FluentValidation (Reglas de Negocio)

Atributos como _\[Required\]_ son geniales para comprobaciones básicas, pero para reglas de negocio complejas (por ejemplo, "EndDate debe ser posterior a StartDate"), usa **FluentValidation**.

- **Por qué:** Separa la lógica de validación de tus DTOs, manteniendo tus clases limpias.
- **Estrategia Compartida:** Si pones estos validadores en una biblioteca .Shared (si es posible), Blazor también puede ejecutarlos. Si no, actúan como guardián en el API.

**Implementación:**

```{code} csharp
public class CreateOrderValidator : AbstractValidator<CreateOrderDto>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.CustomerName).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Items).NotEmpty().WithMessage("Order must have at least one item.");
        RuleFor(x => x.Total).GreaterThan(0);
    }
}
```

## Protección contra Agotamiento de Recursos (Paginación)

Una de las formas más fáciles de bloquear una API es solicitar "Todos los Datos".

- **Regla:** Nunca expongas un método que devuelva List\<T\> sin parámetros Skip y Take.
- **Límite Defensivo:** Si el cliente solicita PageSize=10,000, la API debe ignorarlo y limitarlo a un tope seguro (por ejemplo, 50 o 100).

**Mal (Consulta Sin Límites):**

```{code} csharp
[HttpGet]
public async Task<List<Product>> GetAll(int pageSize)
{
    // DANGER: Client can send pageSize=1000000 and crash the server memory
    return await _db.Products.Take(pageSize).ToListAsync();
}
```

**Bien (Consulta Limitada):**

```{code} csharp
[HttpGet]
public async Task<List<Product>> GetAll(int pageSize = 10)
{
    // Defensive Cap
    const int MaxPageSize = 50;
    if (pageSize > MaxPageSize) pageSize = MaxPageSize;
    return await _db.Products.Take(pageSize).ToListAsync();
}
```

##

##

## Sanitización de Entradas

Incluso si válidas los datos, debes sanitizarlos antes de almacenarlos para prevenir problemas de formato o ataques básicos de inyección.

- **Recorte de Cadenas (Trimming):** Los usuarios a menudo copian y pegan texto con espacios en blanco al principio o al final.
- **Codificación HTML:** Si tu aplicación permite texto enriquecido, debes sanitizar las etiquetas HTML para prevenir XSS (Cross-Site Scripting) cuando esos datos se rendericen más tarde en Blazor.

**Ejemplo (Middleware de Recorte o lógica en DTO):**

```{code} csharp
public async Task CreateUser(UserDto dto)
{
    // Always trim string inputs
    dto.Email = dto.Email?.Trim().ToLower();
    dto.Name = dto.Name?.Trim();

    // ... process
}
```

## Limitación de Tasa (_Rate Limiting_)

Protege tu API de bucles agresivos (por ejemplo, un componente Blazor que llama accidentalmente a la API dentro de _OnAfterRender_ creando efectivamente un bucle infinito).

**Implementación (Middleware Integrado en .NET 7+):** En Program.cs, añade un limitador global.

```{code} csharp
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Request.Headers.Host.ToString(),
            factory: partition => new FixedWindowRateLimiterOptions
            {
                AutoReplenishment = true,
                PermitLimit = 100, // Max 100 requests...
                Window = TimeSpan.FromMinutes(1) // ...per minute
            }));
});
```

# Manejo de Excepciones

En este enfoque, el Servicio lanza excepciones personalizadas, y un Middleware Global las captura y las convierte en respuestas HTTP. Esto mantiene el Controlador más limpio pero utiliza excepciones para el flujo de control.

## La Lógica del Servicio

```{code} csharp
public async Task<UserDto> GetUserAsync(int id)
{
    var user = await _repo.GetByIdAsync(id);

    if (user == null)
    {
        // Throw a custom exception defined in your Core layer
        throw new EntityNotFoundException($"User {id} was not found.");
    }
    return user.ToDto();
}
```

## El Middleware (Registrado en Program.cs)

Este middleware se sitúa en el pipeline del API. Si captura una _`EntityNotFoundException`_, devuelve automáticamente un _`404 Not Found`_.

## El Controlador (Extremadamente Delgado)

```{code} csharp
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetUser(int id)
{
    // If this fails, the middleware catches the exception.
    // The Controller assumes success if line 2 is reached.
    var user = await _userService.GetUserAsync(id);
    return Ok(user);
}
```

## Implementación de la estrategia de Manejo Global de Excepciones

### Excepción Personalizada

Esta clase típicamente vive en tu proyecto _`Core/Domain`_ (o proyecto _`Shared`_). No debe depender de bibliotecas de ASP.NET Core.

```{code} csharp
// In MyProject.Core/Exceptions/EntityNotFoundException.cs
public class EntityNotFoundException : Exception
{
    public EntityNotFoundException(string message)
        : base(message)
    {
    }
    public EntityNotFoundException(string name, object key)
        : base($"Entity '{name}' ({key}) was not found.")
    {
    }
}
```

### El Middleware

Esta clase vive en tu proyecto de API. Su trabajo es envolver cada solicitud HTTP en un bloque _`try/catch`_.

```{code} csharp
// In MyProject.Api/Middleware/ExceptionHandlingMiddleware.cs
using System.NET;
using System.Text.Json;
using MyProject.Core.Exceptions; // Reference your core exceptions

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            // Continue down the pipeline
            await _next(context);
        }
        catch (Exception ex)
        {
            // Catch any exception thrown by Controller or Service
            await HandleExceptionAsync(context, ex);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        var response = new ErrorResponse();
        switch (exception)
        {
            case EntityNotFoundException:
                // Map custom Not Found exception to 404
                context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                response.Message = exception.Message;
                break;
            case ValidationException ex:
                // (Example) Map validation errors to 400
                context.Response.StatusCode = (int)HttpStatusCode.BadRequest;
                response.Message = ex.Message;
                break;
            default:
                // Unhandled errors -> 500 Internal Server Error
                _logger.LogError(exception, "An unhandled exception occurred.");
                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                response.Message = "Internal Server Error. Please contact support.";
                break;
        }
        var result = JsonSerializer.Serialize(response);
        await context.Response.WriteAsync(result);
    }
}
// Simple DTO for the error response
public class ErrorResponse
{
    public string Message { get; set; } = string.Empty;

```

### Registro (Program.cs)

Debes registrar el middleware en tu punto de entrada de la API. El orden es crítico. Debe registrarse **antes** de _`MapControllers()`_ para que envuelva la ejecución del controlador.

```{code} csharp
// Program.cs
var app = builder.Build();
// ... other middleware (Swagger, CORS, etc.)

// 1. Register the Exception Middleware
app.UseMiddleware<ExceptionHandlingMiddleware>();

// 2. Then Map Controllers
app.MapControllers();

app.Run();
```

## Cómo Funciona el Flujo

1. **Cliente:** Solicita _`GET /api/users/99`._
2. **Controlador:** Llama a _`_userService.GetUser(99)`_.
3. **Servicio:** Revisa la BD, no encuentra nada. Lanza _`new`_ `EntityNotFoundException("User 99 not found")`.
4. **Controlador:** La ejecución se aborta inmediatamente (no se alcanza la instrucción _`return`_).
5. **Middleware:** El bloque _`catch`_ intercepta la excepción.
6. **Middleware:** Ve que es _`EntityNotFoundException`_. Establece el Estado a _`404`_. Escribe JSON _`{ "message": "User 99 not found" }`_.
7. **Cliente:** Recibe una respuesta _`404`_ estricta.

---

# El Contrato

# Atributos OpenAPI (Swagger)

Por defecto, Swagger solo genera documentación mínima. Debemos usar decoradores para decirle explícitamente al generador qué hace nuestra API para que el cliente Blazor sepa cómo manejarlo.

## Códigos de Estado Obligatorios

- **Regla:** Cada acción del controlador debe definir todos los posibles caminos de retorno HTTP usando _\[ProducesResponseType\]_.
- **Por qué:** Si no documentas un _404_, el cliente generado podría lanzar una excepción genérica en lugar de una _NotFoundException_ específica o un resultado _null_.
- **El Truco Genérico:** Usa _typeof(void)_ o _typeof(ProblemDetails)_ para estados de error.

**Mal (Contrato Incompleto):**

```{code} csharp
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetUser(int id)
{
    // Swagger thinks this ONLY returns 200 OK.
    // If it returns 404, the Blazor client might crash.
    var user = await _service.GetAsync(id);
    return user ?? NotFound();
}
```

**Bien (Contrato Listo para el Cliente):**

```{code} csharp
[HttpGet("{id}")]
[ProducesResponseType(StatusCodes.Status200OK)] // Logic infers type from ActionResult<T>
[ProducesResponseType(StatusCodes.Status404NotFound)] // Client knows to expect 404
[ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status500InternalServerError)]
public async Task<ActionResult<UserDto>> GetUser(int id) { ... }
```

## Documentación Legible por Humanos (_\[SwaggerOperation\]_)

Nombres de métodos como _GetUserAsync_ a menudo no son suficientes. Usa anotaciones para describir la intención y las reglas de negocio.

- **Requisito:** Habilitar anotaciones en _Program.cs_: _builder.Services.AddSwaggerGen(opts \=\> opts.EnableAnnotations());_

**Uso:**

```{code} csharp
[HttpPost]
[SwaggerOperation(
    Summary = "Creates a new User",
    Description = "Requires Admin privileges. The email must be unique."
)]
public async Task<IActionResult> CreateUser(...) { ... }
```

# Esquema y Serialización

## Enums como Cadenas (Crítico)

Por defecto, C\# serializa los Enums como Enteros (0, 1, 2).

- **Problema:** Si agregas un nuevo valor de enum en medio de la lista en la API, todos los enteros existentes se desplazan, rompiendo silenciosamente la lógica de datos del Cliente Blazor.
- **Solución:** Serializa siempre los Enums como Cadenas ("_Active_", "_Suspended_").

**Implementación (Program.cs):**

```{code} csharp
// In your API Program.cs
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        // Global setting: Send "Active" instead of 1
        options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
    });
```

## Nulabilidad y el Atributo _\[Required\]_

El Generador de Clientes (NSwag/AutoRest) necesita saber si una propiedad puede ser nula para generar el código Typescript/C\# correcto (por ejemplo, _string_ vs _string?_).

- **Regla:** Marca explícitamente los campos DTO no anulables con _\[Required\]_.

**Mal (DTO Ambiguo):**

```{code} csharp
public class CreateProductDto
{
    public string Name { get; set; } // Is this required? API assumes yes, Client assumes no.
    public string? Description { get; set; }
}
```

**Bien (DTO Estricto):**

```{code} csharp
public class CreateProductDto
{
    [Required] // Tells Swagger: "This field will NEVER be missing"
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; } // Nullable in Swagger schema
}
```

# Versionado y Evolución de API

Dado que el Cliente Blazor y la Web API están en repositorios separados, probablemente se desplegarán en momentos diferentes.

No puedes simplemente cambiar la firma de un endpoint; debes evolucionarlo.

##

## Versionado por Ruta de URL

Estandarizamos en **Versionado por Ruta de URL** porque es el más explícito y fácil de depurar (puedes ver la versión en la pestaña de red del navegador).

- **Regla:** Todos los Controladores deben incluir un segmento de versión en su ruta.
- **Implementación:** Usa el paquete _Microsoft.As.NETCore.Mvc.Versioning_.

**Mal (Sin versión):**

```{code} csharp
[Route("api/[controller]")] // api/users
public class UsersController : ControllerBase
```

**Bien (Versionado):**

```{code} csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")] // api/v1/users
public class UsersController : ControllerBase
```

## Manejo de Cambios Disruptivos (_Breaking Changes_)

Un "Cambio Disruptivo" es cualquier cambio que cause que el cliente Blazor existente falle (por ejemplo, renombrar una propiedad, eliminar un parámetro, cambiar un tipo de dato).

**El Protocolo:**

- **Nunca Modifiques V1:** Si necesitas renombrar campos o cambiar la lógica drásticamente, **no** toques el controlador V1.
- **Crea V2:** Crea _UsersControllerV2_, enrútalo a _api/v2/users_, e implementa la nueva lógica allí.
- **Depreca V1:** Agrega el atributo _\[Obsolete\]_ al endpoint antiguo. Esto señala al Generador de Clientes que este método debe marcarse como obsoleto en el código generado.

**Backend (Marcando Deprecación/Obsolescencia):**

```{code} csharp
[HttpGet("{id}")]
[Obsolete("Use v2 endpoint which returns full User details including Roles.")]
public async Task<ActionResult<UserDto>> GetUser(int id) { ... }
```

**Frontend (Resultado del Cliente Generado):** El cliente generado probablemente producirá una advertencia (CS0618) en el registro de compilación de Blazor si intentas usarlo, alertando al desarrollador para que actualice: _Warning: 'IUserClient.GetUserAsync(int)' is obsolete: 'Use v2 endpoint...'_

## Swagger y Versionado

Cuando uses versionado, probablemente tendrás múltiples documentos Swagger (por ejemplo, _/swagger/v1/swagger.json_ y _/swagger/v2/swagger.json_).

- **Regla de Generación de Clientes:** El script de generación de Blazor debe ser configurable para apuntar a una versión específica.
- **Verificación de Seguridad:** Durante un periodo de transición, el Cliente podría usar v2 para la "Característica de Usuario" pero aún usar v1 para la "Característica de Producto". Esto es perfectamente aceptable y es el beneficio principal del versionado.

---

# Frontend (Blazor)

# Programación Defensiva de UI

En Blazor, si ocurre una excepción no controlada durante el renderizado (por ejemplo, una Referencia Nula), el circuito entero se bloquea, requiriendo que el usuario recargue la página.

La programación defensiva aquí trata de proteger el "Árbol de Renderizado".

## El Patrón de UI de "Tres Estados"

Nunca asumas que los datos están listos inmediatamente. Cada página que obtiene datos debe manejar tres estados distintos: **Cargando** (_Loading_), **Error** y **Datos** (_Data_).

**Mal (Asumiendo Éxito):**

```{code} csharp
@page "/products"
@inject IProductClient Client
<h1>@_products.Count Products</h1> @foreach (var p in _products)
{
    <p>@p.Name</p>
}
@code {
    private List<ProductDto> _products; // Defaults to null
    protected override async Task OnInitializedAsync()
    {
        _products = await Client.GetProductsAsync();
    }
}
```

**Bien (Tres Estados Defensivo):**

```{code} csharp
@page "/products"
@inject IProductClient Client
@if (_isLoading)
{
    <div class="spinner">Loading...</div>
}
else if (_errorMessage != null)
{
    <div class="alert alert-danger">@_errorMessage</div>
}
else if (_products != null)
{
    <h1>@_products.Count Products</h1>
    @foreach (var p in _products)
    {
        <p>@p.Name</p>
    }
}
@code {
    private ICollection<ProductDto>? _products;
    private bool _isLoading = true;
    private string? _errorMessage;
    protected override async Task OnInitializedAsync()
    {
        try
        {
            _products = await Client.GetProductsAsync();
        }
        catch (Exception ex)
        {
            _errorMessage = "Unable to load products. Please try again later.";
            // Log ex to external logging service (e.g. AppInsights)
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

## Límites de Error Globales (_Error Boundaries_)

Incluso con código defensivo, los componentes fallan. Usa el componente _\<ErrorBoundary\>_ (disponible en .NET 6+) para contener el fallo en una sección específica de la página, en lugar de matar toda la aplicación.

**Implementación (MainLayout.razor):**

```{code} csharp
<div class="main-content">
    <ErrorBoundary>
        <ChildContent>
            @Body
        </ChildContent>
        <ErrorContent>
            <div class="crash-message">
                Something went wrong in this section. <a href="/">Return Home</a>
            </div>
        </ErrorContent>
    </ErrorBoundary>
</div>
```

# Integración de API y Resiliencia

Dado que la API está en una solución separada (y probablemente en un servidor separado), los fallos de red **ocurrirán**.

## Clientes Tipados y Polly

No uses _HttpClient_ sin procesar. Usa los Clientes Tipados generados por NSwag/AutoRest (por ejemplo, _IUserClient_) y envuélvelos con políticas de **Polly** para resiliencia.

**Mejor Práctica:** Implementa "Manejo de Fallas Transitorias" (Reintentos) en Program.cs.

```{code} csharp
// Program.cs (Blazor Client)
// 1. Register the Generated Client
builder.Services.AddHttpClient<IProductClient, ProductClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["ApiBaseUrl"]);
})
// 2. Add Polly Retry Policy
.AddTransientHttpErrorPolicy(policy =>
    policy.WaitAndRetryAsync(3, retryAttempt =>
        TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)) // Backoff: 2s, 4s, 8s
    )
);
```

##

## Manejo de Respuestas "Void" de la API

Cuando una API devuelve _204 No Content_ o _200 OK (void)_, el cliente generado usualmente devuelve _Task_.

- **Regla:** Siempre haz await a estas llamadas dentro de un try/catch. Los errores de red lanzan excepciones, no devuelven "false".

# Mejores Prácticas de Componentes y Ciclo de Vida

## OnInitialized vs. OnParametersSet

- _OnInitializedAsync_: Se ejecuta **una vez** cuando el componente se crea. Úsalo para obtener datos iniciales.
- _OnParametersSetAsync_: Se ejecuta **cada vez** que el padre pasa nuevos parámetros.
  - \*Advertencia**\*:** Si obtienes datos aquí, asegúrate de no desencadenar un bucle infinito de renderizado.

## LINQ en Blazor (Conciencia de Memoria)

A diferencia del Backend, LINQ en Blazor se ejecuta en la CPU del navegador del usuario (WebAssembly).

- **Regla:** Evita LINQ complejo (Groups, Joins) dentro de la lógica de Renderizado (sintaxis Razor).
- **Mejor Práctica:** Realiza cálculos complejos en el bloque `@code` o en un `ViewModel`, y almacena el resultado en una variable.

**Mal (Calcula en cada frame de renderizado):**

```{code} csharp
<p>Total Active: @MyList.Where(x => x.IsActive).Sum(x => x.Price)</p>
```

**Bien (Calculado una vez):**

```{code} csharp
<p>Total Active: @_totalActivePrice</p>
@code {
    private decimal _totalActivePrice;

    protected override void OnParametersSet()
    {
        _totalActivePrice = MyList.Where(x => x.IsActive).Sum(x => x.Price);
    }
}
```

## Componentes Desechables (_Disposable_)

Si un componente se suscribe a un evento (evento C\#) o a un temporizador (Timer), **debe** implementar _IDisposable_ para desvincularse cuando el usuario navega fuera. No hacerlo causa "Componentes Fantasma" que se ejecutan en segundo plano y fugan memoria.

```{code} csharp
@implements IDisposable
@code {
    protected override void OnInitialized()
    {
        StateService.OnChange += StateHasChanged;
    }
    public void Dispose()
    {
        // CRITICAL: Unsubscribe to prevent memory leak
        StateService.OnChange -= StateHasChanged;
    }
}
```

# Estrategias de Gestión de Estado

Evita dispersar la lógica de datos dentro de componentes individuales. En su lugar, usa un enfoque escalonado para la gestión del estado basado en la vida útil y el alcance de los datos.

## Nivel 1: URL como la Fuente Única de la Verdad

El estado más robusto es la URL. Si un usuario copia la URL y la envía a un colega, deberían ver la vista exacta (filtros, número de página, pestaña activa).

- **Regla:** Si afecta la navegación o el filtrado, ponlo en los Query Strings de la URL.
- **Implementación:** Usa _\[SupplyParameterFromQuery\]_ (disponible en .NET 6+).

**Mal (Perdido al Refrescar):**

```{code} csharp
// Clicking "Refresh" resets the filter because it's only in memory
private string _searchTerm = "";
```

**Bien (Marcadores/Bookmarks funcionan):**

```{code} csharp
[SupplyParameterFromQuery(Name = "q")]
public string? SearchTerm { get; set; }
protected override async Task OnParametersSetAsync()
{
    // Automatically triggers when URL changes
    await LoadDataAsync(SearchTerm);
}
```

## Nivel 2: Contenedor de Estado En-Memoria (El Patrón de Servicio)

Para datos compartidos a través de múltiples componentes (por ejemplo, un Carrito de Compras, Perfil de Usuario, o Pasos de un Asistente), usa un **_Scoped Service_**.

**El Patrón:**

1. Crear una clase C\# (_CartState_).
2. Registrarla como _Scoped_ en DI (Inyección de Dependencias).
3. Usar un evento _Action_ de C\# para notificar a los componentes cuando los datos cambien.

**El Contenedor de Estado:**

```{code} csharp
public class CartState
{
    // The Data
    public List<ProductDto> Items { get; private set; } = new();
    // The Notification
    public event Action? OnChange;
    public void AddItem(ProductDto item)
    {
        Items.Add(item);
        NotifyStateChanged();
    }
    private void NotifyStateChanged() => OnChange?.Invoke();
}
```

**El Componente (Escuchando Cambios):**

```{code} csharp
@inject CartState Cart
@implements IDisposable
<p>Items in cart: @Cart.Items.Count</p>
@code {
    protected override void OnInitialized()
    {
        // Subscribe to updates
        Cart.OnChange += StateHasChanged;
    }
    public void Dispose()
    {
        // CRITICAL: Unsubscribe to prevent memory leaks
        Cart.OnChange -= StateHasChanged;
    }
}
```

## Nivel 3: Persistencia (Sobreviviendo al Refresco)

El estado en memoria (Nivel 2\) se borra si el usuario presiona F5. Para datos críticos que deben sobrevivir a un refresh (Tokens de Auth, Preferencia de Tema, Formularios en progreso), usa Almacenamiento del Navegador.

- _localStorage_: Persiste incluso después de cerrar el navegador.
- _sessionStorage_: Persiste solo mientras la pestaña está abierta.

**Recomendación:** Usa una librería como _Blazored.LocalStorage_ para manejar la serialización/deserialización automáticamente.

```{code} csharp
public async Task SaveThemeAsync(string theme)
{
    await _localStorage.SetItemAsync("theme", theme);
}
```

## La Trampa "Estática" (Advertencia de Blazor Server)

Si alguna vez alojas esta aplicación como Blazor Server (o migras a ella):

- **Regla:** NUNCA uses variables static para mantener estado del usuario.
- **Por qué:** En Blazor Server, las variables static se comparten entre TODOS los usuarios conectados a esa instancia del servidor. El Usuario A vería los datos del Usuario B.
- **Solución:** Usa siempre Inyección de Dependencias (servicios Scoped).

# Estilizado y Arquitectura CSS

Evitamos el problema de la "Hoja de Estilos de Solo Agregar" (donde site.css crece a 5,000 líneas). En su lugar, usamos un enfoque híbrido de Variables CSS para consistencia y Aislamiento de CSS para modularidad.

## Aislamiento de CSS (Estilos Scoped)

Blazor proporciona un mecanismo integrado para limitar el alcance (scope) de CSS a un componente específico. Este es nuestro estándar por defecto para diseño y comportamiento específico de componentes.

- **Nombramiento de Archivos:** Crea un archivo .css con exactamente el mismo nombre que el componente.
  - Counter.razor \-\> Counter.razor.css
- **Cómo funciona:** Blazor reescribe tus selectores en tiempo de compilación (por ejemplo, .card se convierte en .card\[b-3x9d1\]) para que solo apliquen a ese componente.

**Mal (Contaminación Global):**

```css
/* In site.css */
.card {
  background: red;
} /* accidentally turns ALL cards red */
```

**Bien (Aislado):**

```css
/* In ProductCard.razor.css */
.card {
  background: red;
} /* Only affects ProductCard.razor */
```

##

## El Combinador ::deep

Un error común con el Aislamiento de CSS es que no aplica a **Componentes Hijos** renderizados dentro del padre.

- **Problema:** Quieres estilizar un _\<InputText\>_ estándar dentro de tu _LoginForm.razor_, pero el aislamiento ignora el HTML del componente hijo.
- **Solución:** Usa el combinador ::deep.

```css
/* LoginForm.razor.css */
/* Applies to HTML elements in LoginForm */
.login-box {
  border: 1px solid #ccc;
}
/* Applies to Child Components (like Blazor InputText) inside .login-box */
::deep input.form-control {
  background-color: #f0f0f0;
}
```

## Arquitectura Global (Temas)

No uses códigos hex hardcodeados (_\#3498db_) dentro de archivos aislados. Si la marca cambia, tendrás que editar 50 archivos.

**Regla:** Usa Propiedades Personalizadas CSS (Variables) para todos los tokens de diseño (Colores, Espaciado, Fuentes). Defínelos en app.css (o root.css).

**Definición (app.css):**

```css
:root {
  --primary-color: #007bff;
  --spacing-md: 1rem;
  --font-heading: "Roboto", sans-serif;
}
```

**Uso (Component.razor.css):**

```css
.submit-btn {
  background-color: var(--primary-color); /* Safe */
  padding: var(--spacing-md);
}
```

## Clases Condicionales

Evita lógica C\# compleja dentro de la cadena del atributo _class_. Hace que el marcado Razor sea ilegible.

**Mal (Cadena Spaghetti):**

```{code} csharp
<div class="alert @(IsError ? "alert-danger" : (IsWarning ? "alert-warning" : "alert-info"))">
```

**Bien (Método Helper o Propiedad):** Mueve la lógica al bloque `@code`.

```{code} csharp
<div class="alert @AlertClass"> ... </div>
@code {
    private string AlertClass => IsError ? "alert-danger"
                               : IsWarning ? "alert-warning"
                               : "alert-info";
}
```

## Estilos en Línea (Inline Styles)

- **Regla:** Evita los atributos style="..." por completo.
- **Por qué:** Violan los hashes de la Política de Seguridad de Contenido (CSP) en entornos estrictos y no pueden ser reutilizados.
- **Excepción:** Valores dinámicos que cambian cada frame (por ejemplo, el ancho de una barra de progreso o coordenadas de arrastrar y soltar).

```{code} csharp
<div class="progress-bar" style="width: @(PercentComplete)%"></div>
```

## ¿Qué va en site.css (o app.css)?

Piensa en este archivo como tu **Sistema de Diseño**. Define el "Vocabulario" de tu sitio. Generalmente debe contener definiciones, no implementaciones.

#### **A. Propiedades Personalizadas CSS (Variables) \[CRÍTICO\]**

Define todos tus colores, fuentes y espaciado aquí. Rara vez deberías ver un código hex (por ejemplo, \#ff0000) en un archivo de componente.

```css
:root {
  /* Brand Colors */
  --primary: #007bff;
  --secondary: #6c757d;
  --danger: #dc3545;

  /* Spacing Scale */
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;

  /* Typography */
  --font-main: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  --font-code: "Consolas", monospace;
}
```

#### **B. Restablecimiento (Resets) y Normalización de CSS**

Reglas que aseguran que los navegadores rendericen los elementos de manera consistente.

```css
* {
  box-sizing: border-box; /* Essential for layout math */
}
body {
  margin: 0;
  font-family: var(--font-main);
  color: var(--text-dark);
}
```

#### **C. Valores Predeterminados de Tipografía**

Encabezados, párrafos y estilos de enlaces. Estos deben ser consistentes en toda la aplicación.

```css
h1,
h2,
h3,
h4,
h5,
h6 {
  margin-top: 0;
  margin-bottom: var(--space-md);
  font-weight: 600;
}
a {
  color: var(--primary);
  text-decoration: none;
}
```

#### **D. Clases de Utilidad**

Clases pequeñas de propósito único que no justifican un componente (a menos que uses Tailwind/Bootstrap, en cuyo caso estas se te proporcionan).

```css
.text-center {
  text-align: center;
}
.d-flex {
  display: flex;
}
.cursor-pointer {
  cursor: pointer;
}
.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
```

## ¿Qué va en Component.razor.css?

Piensa en esto como la **Implementación**. Estos estilos son "Scoped" (Aislados), lo que significa que Blazor les agrega un ID único para que no puedan afectar a otros componentes.

#### **A. Diseño Interno (Layout)**

Cómo se organizan los elementos dentro de este componente específico.

```css
/* UserProfile.razor.css */
.profile-card {
  display: flex; /* Flexbox specific to this card's layout */
  flex-direction: column;
  gap: var(--space-md); /* Using the global variable */
}
```

#### **B. Dimensiones Específicas**

Si un componente necesita una restricción específica de altura o ancho.

```css
/* Sidebar.razor.css */
.sidebar-container {
  width: 250px;
  height: 100vh;
}
```

#### **C. Estados Específicos del Componente**

Estilos que cambian según la lógica de C\# específica de este componente.

```css
/* TodoItem.razor.css */
.is-completed {
  text-decoration: line-through;
  color: var(--secondary);
  opacity: 0.7;
}
```

#### **D. El Combinador ::deep**

Estilos para Componentes Hijos que se renderizan dentro de este componente. El aislamiento de Blazor no penetra en los componentes hijos por defecto; debes forzarlo.

```css
/* LoginForm.razor.css */
/* Targets the InputText Blazor component rendered inside this form */
::deep .form-control {
  border: 2px solid var(--primary);
}
```

### **Lista de Verificación Resumida**

| Tipo de Regla                        | Ubicación del Archivo | ¿Por qué?                                                                                                                                                                |
| :----------------------------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Colores / Códigos Hex**            | site.css (Variables)  | Cambiar el color de la marca lo cambia en todas partes instantáneamente.                                                                                                 |
| **Familias de Fuentes**              | site.css              | Consistencia a través de las páginas.                                                                                                                                    |
| **Sistemas Grid / Flex**             | site.css (o Librería) | La estructura principal del diseño de página usualmente abarca toda la aplicación.                                                                                       |
| **Anchos Específicos de Componente** | Component.razor.css   | Una "UserCard" sabe qué tan ancha debe ser; el sitio global no.                                                                                                          |
| **Efectos Hover**                    | Component.razor.css   | La lógica de interacción usualmente pertenece al componente.                                                                                                             |
| **Z-Index (Capas)**                  | site.css              | **Excepción:** Las guerras de Z-index ocurren cuando los componentes gestionan sus propias capas. Define Z-indexes globales (Modal vs Tooltip) en variables de site.css. |

###

###

###

###

### **Escenario de Ejemplo**

**El Objetivo:** Crear una "Tarjeta de Producto" (Product Card).

**1\. site.css (La configuración):**

```css
:root {
  --card-bg: #ffffff;
  --border-radius: 8px;
  --shadow-soft: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

**2\. ProductCard.razor.css (La implementación):**

```css
.card {
  /* Use the variables */
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-soft);

  /* Layout specific to this component */
  padding: 1rem;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px); /* Interaction logic lives here */
}

/* Image is specific to this card */
.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
```

Esta separación asegura que si quieres cambiar el estilo de "sombra suave" en toda la aplicación, editas site.css.

Pero si quieres cambiar cómo se comporta la Tarjeta de Producto al pasar el mouse (hover), editas ProductCard.razor.css.

# Creación y Reutilización de Componentes

Seguimos la filosofía de Diseño Atómico. No construyas "Componentes de Página" (Monolitos). Divide la UI en pequeños bloques de Lego reutilizables.

## Granularidad (Átomos, Moléculas, Organismos)

- **Átomos:** Unidades más pequeñas. Botones, Entradas, Etiquetas. (por ejemplo, _\<PrimaryButton\>_).
- **Moléculas:** Grupos de átomos. Caja de Búsqueda (Input \+ Button), Campo de Formulario (Label \+ Input \+ Error Msg).
- **Organismos:** Secciones complejas. Barra de navegación, Barra lateral, Cuadrícula de productos.

**Regla:** La lógica "Inteligente" (llamadas API) usualmente vive en **Páginas** u **Organismos**. La lógica "Tonta" (renderizar datos, emitir clics) vive en **Átomos** y **Moléculas**.

## Componentes con Plantilla (_RenderFragment_)

La herramienta más poderosa para reutilización es RenderFragment. Permite a un componente actuar como un "Envoltorio" o "Diseño" sin saber qué hay dentro de él.

**Escenario:** Quieres un componente Card, pero a veces contiene un Gráfico, a veces una Tabla.

**Bien (Envoltorio Reutilizable):**

```{code} csharp
<div class="card shadow-sm">
    <div class="card-header">@Title</div>
    <div class="card-body">
        @ChildContent </div>
</div>
@code {
    [Parameter] public string Title { get; set; }
    [Parameter] public RenderFragment ChildContent { get; set; }
}
```

**Uso:**

```{code} csharp
<Card Title="Sales Report">
    <Chart Data="_salesData" />
</Card>
```

## Componentes Genéricos (`@typeparam`)

Si te encuentras copiando y pegando una Cuadrícula o Lista porque "Esta muestra Usuarios" y "Esa muestra Productos", usa **Genéricos**.

**Escenario:** Una Tabla Ordenable que funciona para CUALQUIER tipo de dato.

```{code} csharp
@typeparam TItem
<table class="table">
    <thead>
        <tr>@HeaderContent</tr>
    </thead>
    <tbody>
        @foreach (var item in Items)
        {
            <tr>@RowTemplate(item)</tr>
        }
    </tbody>
</table>
@code {
    [Parameter] public IEnumerable<TItem> Items { get; set; }
    [Parameter] public RenderFragment HeaderContent { get; set; }
    [Parameter] public RenderFragment<TItem> RowTemplate { get; set; }
}
```

**Uso:**

```{code} csharp
<SortableTable Items="_users" Context="user">
    <HeaderContent>
        <th>Name</th>
        <th>Email</th>
    </HeaderContent>
    <RowTemplate>
        <td>@user.Name</td>
        <td>@user.Email</td>
    </RowTemplate>
</SortableTable>
```

## Parámetros y _\[EditorRequired\]_

Los desarrolladores a menudo olvidan pasar los parámetros requeridos, causando errores en tiempo de ejecución.

Usa _\[EditorRequired\]_ para convertir estos en Advertencias en Tiempo de Compilación.

**Mal:**

```{code} csharp
[Parameter] public string Label { get; set; } // If null, UI looks broken
```

**Bien:**

```{code} csharp
[EditorRequired] // Compiler warns if <MyInput> is missing the Label attribute
[Parameter] public string Label { get; set; }
```

## EventCallbacks (Comunicación Hacia Arriba)

Los componentes hijos nunca deben modificar datos directamente. Deben notificar al padre.

- **Regla:** Usa siempre _EventCallback\<T\>_ en lugar de _Action\<T\>_ para eventos de componentes.
- **Por qué:** _EventCallback_ desencadena automáticamente _StateHasChanged()_ en el componente padre, asegurando que la UI se actualice inmediatamente.

```{code} csharp
// Child Component
[Parameter] public EventCallback<int> OnDeleted { get; set; }
private async Task HandleClick()
{
    await OnDeleted.InvokeAsync(ItemId); // Parent refreshes automatically
}
```

## Inmutabilidad de Parámetros

**Regla Estricta:** Nunca escribas en una propiedad _\[Parameter\]_ desde dentro del componente.

- Los parámetros fluyen Hacia Abajo (Padre a Hijo).
- Los eventos fluyen Hacia Arriba (Hijo a Padre).
- Si un hijo cambia su propio parámetro, será sobrescrito la próxima vez que el padre se renderice.

---

# Seguridad y Operaciones

# CORS (Cross-Origin Resource Sharing)

Debido a que tu Cliente Blazor y Web API se ejecutan en diferentes dominios (o puertos), el navegador bloqueará las solicitudes por defecto.

Debes permitir explícitamente que el cliente Blazor hable con la API.

## Políticas de Origen Estricto

**Regla:** Nunca uses _.AllowAnyOrigin()_ en Producción. Abre tu API para ser llamada por sitios web maliciosos que alojan scripts dirigidos a tus usuarios.

**Mal (Comodín \- Inseguro):**

```{code} csharp
app.UseCors(x => x
    .AllowAnyMethod()
    .AllowAnyHeader()
    .AllowAnyOrigin()); // DANGER: Anyone can embed your API
```

**Bien (Impulsado por Configuración):** Lee la URL permitida desde _appsettings.json_ para que puedas cambiarla por entorno (Localhost vs. Dominio de Producción).

```{code} csharp
// In Program.cs (API Project)
var allowedOrigins = builder.Configuration.GetSection("AllowedOrigins").Get<string[]>();
builder.Services.AddCors(options =>
{
    options.AddPolicy("BlazorClientPolicy", policy =>
    {
        policy.WithOrigins(allowedOrigins) // Only allow YOUR Blazor app
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});
// ... later in the pipeline
app.UseCors("BlazorClientPolicy");
```

```json
// appsettings.json
{
  "AllowedOrigins": ["https://localhost:7001", "https://my-blazor-app.com"]
}
```

## Encabezados Expuestos

Si tu API usa encabezados personalizados para Paginación (por ejemplo, _X-Pagination_) o Versionado, debes "Exponerlos" explícitamente en CORS, o el cliente Blazor los leerá como nulos.

```{code} csharp
policy.WithOrigins(...)
    .WithExposedHeaders("X-Pagination", "X-Version");
```

# Configuración del Entorno

Gestionar la configuración en una solución desacoplada requiere entender que **La Configuración del Cliente es Pública** y **La Configuración del Servidor es Privada**.

## La Configuración "Pública" de Blazor

**Advertencia de Seguridad Crítica:** appsettings.json en un proyecto Blazor WebAssembly se descarga al navegador del usuario.

- **Regla:** NUNCA pongas secretos (Claves API, Cadenas de Conexión, Contraseñas) en el appsettings.json de Blazor.
- **Uso:** Solo almacena información pública, como la URL Base de la API o Feature Flags.

**Blazor wwwroot/appsettings.json:**

```json
{
  "ApiBaseUrl": "https://localhost:5001",
  "Features": {
    "EnableDarkTheme": true
  }
}
```

## Configuración del Backend (API)

La API se ejecuta en el servidor, por lo que **puede** guardar secretos.

- **Desarrollo:** Usa **User Secrets** (Click derecho en Proyecto \-\> Manage User Secrets) para almacenar cadenas de conexión a BD. No los confirmes en Git.
- **Producción:** Usa Variables de Entorno (Azure App Service / AWS / variables de entorno Docker) para inyectar cadenas de conexión.

**Mal (Secretos Confirmados):**

```json
// appsettings.json
"ConnectionStrings": {
    "Default": "Server=...;Password=SuperSecret123;" // DANGER: Committed to Git
}
```

**Bien (Reemplazo de Token):**

```json
// appsettings.json
"ConnectionStrings": {
    "Default": "Wait for Environment Variable"
}
```

---

# Control de Versiones y Colaboración

# Pautas de Commits Convencionales

Nos adherimos a la especificación de **Conventional Commits**. Esto proporciona un historial estructurado que permite la generación automatizada de Changelogs (Registros de Cambios) y Versionado Semántico (SemVer).

## Estructura del Mensaje

Cada mensaje de commit debe seguir este formato:

```
<type>(<scope>): <description>
[optional body]
[optional footer(s)]
```

- **Type:** ¿Qué tipo de cambio es este?
- **Scope:** (Opcional) ¿Qué proyecto o módulo está afectado?
- **Description:** Resumen corto en modo imperativo (por ejemplo, "add" no "added").

## Tipos Permitidos

| Tipo         | Impacto SemVer | Descripción                                                                   |
| :----------- | :------------- | :---------------------------------------------------------------------------- |
| **feat**     | MINOR          | Una nueva característica (por ejemplo, agregar una barra de búsqueda).        |
| **fix**      | PATCH          | Una corrección de errores (por ejemplo, arreglar un fallo al iniciar sesión). |
| **docs**     | Ninguno        | Cambios solo de documentación (README, anotaciones Swagger).                  |
| **style**    | Ninguno        | Formato, puntos y comas faltantes (sin cambios de código).                    |
| **refactor** | Ninguno        | Un cambio de código que ni arregla un error ni agrega una característica.     |
| **perf**     | Ninguno        | Un cambio de código que mejora el rendimiento.                                |
| **test**     | Ninguno        | Agregar pruebas faltantes o corregir pruebas existentes.                      |
| **chore**    | Ninguno        | Mantenimiento (actualizar paquetes NuGet, .gitignore).                        |
| **ci**       | Ninguno        | Cambios en la tubería de CI/CD (GitHub Actions, Azure DevOps).                |

**Ejemplos:**

- feat(client): add skeleton loader to product list
- fix(api): correct validation logic for email field
- chore(shared): update fluentvalidation package

## Manejo de Cambios Disruptivos (_Breaking Changes_)

Un Cambio Disruptivo es cualquier cosa que causaría que la aplicación consumidora (Blazor) fallara si no se actualizara simultáneamente.

Regla: DEBES indicar los cambios disruptivos explícitamente para desencadenar un salto de versión MAYOR.

**Sintaxis 1: El "\!" (Preferido)**

Agrega un signo de exclamación después del tipo/ámbito.

```
feat(api)!: change user id from int to guid
```

**Sintaxis 2: El Pie de Página**

Agrega BREAKING CHANGE: en el pie de página.

```
feat(api): change user id from int to guid
BREAKING CHANGE: The 'id' field in UserDto is now a Guid string instead of an Integer.
```

# El "Por Qué" Importa (El Cuerpo)

Para commits complejos, la línea de asunto no es suficiente. Usa el cuerpo para explicar **por qué** se hizo el cambio, no solo **qué** cambió.

**Mal:**

```
fix(client): update list logic
```

**Bien:**

```
fix(client): prevent infinite render loop in product list
The OnParametersSetAsync method was modifying a parameter directly,
which triggered a re-render. Moved logic to a private field to fix.
```
