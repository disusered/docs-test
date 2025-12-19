---
title: Reglas de React
---

Así como diferentes lenguajes de programación tienen su propia manera de expresar conceptos, React tiene sus modismos o reglas para expresar patrones en un sentido que sea fácil de entender y al mismo tiempo de alta calidad.

Seguir estas reglas pueden ayudar a escribir aplicaciones bien organizadas, seguras y estructuradas en componentes. Estas propiedades hacen que la app sea más resistente a cambios y hace que sea más fácil trabajar con otros desarrolladores, librerías y herramientas.

# 1\. Los Componentes deben ser Puros

Los componentes y hooks de React deben comportarse como funciones puras: al recibir los mismos valores, deben producir el mismo resultado, sin causar efectos secundarios durante el render. La pureza es fundamental para que React pueda renderizar, re-renderizar, comparar y optimizar sin introducir comportamientos inesperados.

## 1.1 Idempotencia del Render

React puede llamar a un componente más de una vez para el mismo estado y los mismos props. Esto no es un error: es el diseño del sistema.

Para ello, un componente debe ser **idempotente**:

_Con los mismos inputs, debe generar exactamente la misma salida._

**Implicaciones prácticas:**

- No producir efectos secundarios durante el render.
- No mutar props, estado ni objetos externos.
- No realizar operaciones que dependan de valores no deterministas (tiempo, random, lecturas externas).
- No leer ni escribir en el DOM directamente.

**No permitido:**

```javascript
function UserCard({ user }) {
  user.visits++; // Mutación
  console.log("Render"); // Efecto secundario
  return (
    <p>
      {user.name} (visits: {visits})
    </p>
  );
}
```

**Correcto:**

```javascript
function UserCard({ user }) {
  const visits = user.visits + 1;
  return (
    <p>
      {user.name} (visits: {visits})
    </p>
  );
}
```

## 1.2 Prohibición de Efectos Secundarios en el Render

Durante el render, React está construyendo la UI. Cualquier acción externa: logs, llamadas a APIs, timers, escritura en variables, manipulación del DOM, quebranta la pureza y puede generar renders inconsistentes.

Los efectos secundarios deben realizarse únicamente dentro de Hooks diseñados para ello (useEffect, useLayoutEffect).

**No permitido:**

```javascript
function Products({ items }) {
  saveToLocalStorage(items); // No permitido
  return <List items={items} />;
}
```

**Correcto:**

```javascript
function Products({ items }) {
  useEffect(() => {
    saveToLocalStorage(items);
  }, [items]);

  return <List items={items} />;
}
```

## 1.3 Inmutabilidad en el Render

Los valores usados para renderizar deben considerarse inmutables dentro del render. Mutarlos puede desincronizar la UI de la memoria interna de React.

**Regla práctica**

- Nunca modificar props.
- Nunca modificar estado directamente.
- Nunca modificar objetos derivados del contexto o de referencias externas.

**No permitido:**

```javascript
function Cart({ cart }) {
  cart.total += 10; // Mutación prohibida
  return <p>{cart.total}</p>;
}
```

**Correcto:**

```javascript
function Cart({ cart }) {
  const total = cart.total + 10;
  return <p>{total}</p>;
}
```

##

## 1.4 Sin Acciones Impredecibles en la Fase de Render

El render debe ser completamente determinado. React puede volver a renderizar:

- Para validar resultados.
- Para ejecutar optimizaciones.
- Por el modo estricto.
- Por reconciliación entre componentes.

Si el render depende de una acción impredecible (ej. `Date.now()`, `Math.random()`, lectura de un servicio), la UI se vuelve inconsistente.

**No permitido:**

```javascript
function Code() {
  const code = Math.random(); // Cambia en cada render
  return <p>{code}</p>;
}
```

**Correcto:**

```javascript
function Code() {
  const [code] = useState(() => Math.random());
  return <p>{code}</p>;
}
```

##

## 1.5 Pureza también aplica a Hooks personalizados

Un custom hook es parte del sistema de render. Si tiene efectos secundarios fuera del contexto de un hook de efectos, viola la pureza.

**No permitido:**

```javascript
function useCounter() {
  analytics.track("counter-used"); // Efecto indebido
  const [value, setValue] = useState(0);
  return { value, setValue };
}
```

**Correcto:**

```javascript
function useCounter() {
  const [value, setValue] = useState(0);

  useEffect(() => {
    analytics.track("counter-used");
  }, []);

  return { value, setValue };
}
```

# 2\. React llama a los Componentes y Hooks

React es quien decide **cuando y cuantas veces** renderiza. Nosotros solo declaramos que queremos mostrar;

React se encarga de la coreografía.

Al entender esto, se evitan errores que, aunque parecen inocentes, rompen por completo la arquitectura reactiva.

## 2.1 Los Componentes no se invocan como funciones normales

Un componente nunca debe ser llamado “a mano”, como si fuera una función utilitaria.

React es el único que puede invocar un componente, porque controla el ciclo de render de principio a fin.

**No permitido:**

```javascript
const result = MyComponent(); // No permitido
```

**Correcto:**

```javascript
<MyComponent /> // React lo llama cuando toca
```

## 2.2 Los Hooks no se “pasan” ni se usan como valores

Un Hook no es un valor transportable: no es una variable, ni un callback, ni una función que se puede guardar para “usar después”.

Los Hooks solo pueden ser llamados desde:

- Un componente de React
- Un Hook personalizado

**No permitido:**

```javascript
const h = useState; // Pasar hooks como valores
const state = someAction(h);
```

**No permitido:**

```javascript
function doSomething(hook) {
  // Recibir hooks como argumentos
  const [v, setV] = hook(); // Esto rompe por completo el orden de los hooks
}
```

**Correcto:**

```javascript
function MyComponent() {
  const [value, setValue] = useState(0); // React controla el ciclo del hook
}
```

## 2.3 React controla el orden, la frecuencia y el contexto

React decide cuantas veces, en qué orden, y en qué momento llamar a los componentes y hooks.

No se debe:

- Alterar el orden dinámicamente
- Esconder un hook dentro de un **_if_**
- Llamar un componente manualmente
- Pasar hooks como valores

**No permitido:** Alterar el orden dinámicamente

```javascript
function Example({ useExtra }) {
  const [a, setA] = useState(0);

  if (useExtra) {
    const [b, setB] = useState(0); // Cambia el orden según la prop
  }

  const [c, setC] = useState(0);
  return <div>{a + c}</div>;
}
```

**Correcto:**

```javascript
function Example({ useExtra }) {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0); // Siempre definido, siempre mismo orden
  const [c, setC] = useState(0);

  return (
    <div>
      {a + c}
      {useExtra && <span>Extra: {b}</span>}
    </div>
  );
}
```

**No permitido:** Esconder un hook dentro de un **_if_**

```javascript
function Wrong() {
  if (Math.random() > 0.5) {
    const [value, setValue] = useState(0); // Hook condicionado
  }
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}
```

**Correcto:**

```javascript
function Right() {
  const [value] = useState(0); // Siempre en el mismo orden
  const [count, setCount] = useState(0);

  const showValue = Math.random() > 0.5;
  return <div>{showValue ? value : count}</div>;
}
```

**No permitido:** Llamar un componente manualmente

```javascript
function App() {
  const profile = UserProfile({ user }); // No permitido
  return <div>{profile}</div>;
}
```

**Correcto:**

```javascript
function App() {
  return (
    <div>
      <UserProfile user={user} /> {/* React lo llama correctamente */}
    </div>
  );
}
```

**No permitido:** Pasar hooks como valores

```javascript
function doSomething(hook) {
  const [value, setValue] = hook(); // Prohibido
}

function App() {
  return doSomething(useState); // Pasar hooks
}
```

**Correcto:**

```javascript
function useCounter() {
  const [value, setValue] = useState(0);
  return { value, setValue };
}

function App() {
  const counter = useCounter(); // Hook llamado en contexto válido
  return <div>{counter.value}</div>;
}
```

# 3\. Reglas de los Hooks

Los Hooks son funciones, pero no son funciones normales.

Son un tipo lógico reutilizable que vive bajo un conjunto muy estricto de reglas.

Romperlas no produce errores evidentes; produce errores silenciosos que hacen que el UI se descomponga por dentro.

## 3.1 Solo se llaman en el nivel superior

No se esconden Hooks en:

- loops
- ifs
- callbacks
- funciones internas
- returns tempranos

React necesita que los Hooks aparezcan en el mismo orden en cada render. Si el orden cambia, todo se desajusta.

**No permitido**

```javascript
function Counter({ active }) {
  if (active) {
    const [count, setCount] = useState(0); // Hook condicionado
  }

  return <div>Hola</div>;
}
```

```javascript
function List({ items }) {
  items.forEach(() => {
    const [flag] = useState(false); // Hook dentro de loop
  });
}
```

```javascript
function App() {
  function inner() {
    const [v] = useState(0); // Hook dentro de función interna
  }
}
```

**Correcto:**

```javascript
function Counter({ active }) {
  const [count, setCount] = useState(0); // Siempre en el tope
  return <div>{active ? count : "Inactivo"}</div>;
}
```

## 3.2 Solo se llaman desde funciones de React

Un Hook no se llama desde cualquier función que se escriba porque sí.

Solo se puede usar dentro de:

- Un Componente de React
- Un Hook personalizado

**No permitido**

```javascript
function doSomething() {
  const [value, setValue] = useState(0); // No es un componente ni un hook
}
```

```javascript
function getData() {
  const [data, setData] = useState(null); // Totalmente fuera del ciclo de React
}
```

**Correcto:**

```javascript
function useThing() {
  const [value, setValue] = useState(0);
  return { value, setValue };
}
```

```javascript
function App() {
  const thing = useThing();
  return <div>{thing.value}</div>;
}
```

## 3.3 Hooks antes de los “early return”

La documentation lo enfatiza:

Si se tiene returns tempranos, los hooks deben ir antes de ellos, nunca después.

**No permitido:**

```javascript
function UserCard({ user }) {
  if (!user) return null;

  const [expanded, setExpanded] = useState(false); // Hook después del return posible
}
```

**Correcto:**

```javascript
function UserCard({ user }) {
  const [expanded, setExpanded] = useState(false); // Siempre al principio
  if (!user) return null;

  return <div>{expanded ? "..." : "..."}</div>;
}
```

# 4. React \- Naming Convention

La claridad de los nombres es la primera defensa contra el caos. Un proyecto compartido se sostiene si todos hablamos el mismo idioma en el código. Estas son las convenciones recomendadas para asegurar consistencia, legibilidad y mantenimiento a largo plazo.

## 4.1\. Componentes (PascalCase)

Los componentes representan unidades visuales y lógicas UI. Su nombre debe reflejarlo.

**Regla**

- Usar **PascalCase** para todos los componentes.

**Ejemplos**

- UserProfile
- LoginForm
- DashboardSidebar

El archivo que contiene un componente debe tener el mismo nombre:

- UserProfile.jsx
- LoginForm.tsx

## 4.2\. Hooks Personalizados (camelCase \+ prefijo “use”)

Los hooks son funciones con un propósito muy particular en React. Su nombre debe hacerlo obvio.

**Regla**

- Siempre iniciar con **use**
- User **camelCase**

**Ejemplos**

- useAuth
- useFetchPosts
- useToggle

## 4.3\. Props (camelCase \+ descriptivas)

Las props cargan información hacia el componente. Su nombre debe explicar su significado.

**Regla**

- Usar **camelCase**
- Evitar abreviaciones crípticas
- Elegir nombres semánticos y claros

**Ejemplos correctos**

- user
- onSubmit
- initialValue

**Ejemplos incorrectos**

- usr
- sub
- v1

## 4.4\. Estado (State) \- Booleanos con prefijos semánticos

Los nombres de estado deben indicar su tipo y propósito.

**Booleanos**  
Usar prefijos como:

- is\*
- has\*
- should\*

**Ejemplos correctos**

- isLoading
- hasError
- shouldRenderFooter

**Otros estados**  
Usar nombres que describan claramente el contenido:

- selectedUserId
- counterValue

## 4.5\. Manejadores de eventos (handle)

Los eventos deben distinguirse como acciones que responden a eventos del usuario o del sistema.

**Regla**

- Prefijo obligatorio: **handle**
- Nombre del evento o acción: en PascalCase después del prefijo

**Ejemplos**

- handleClick
- handleFormSubmit
- handleInputChange

## 4.6\. Archivos de utilidades y funciones helper (camelCase)

Evitar nombres ambiguos. Cada utilidad debe decir claramente qué hace.

**Ejemplos**

- formatDate.js → contiene export function formatDate()
- generateUniqueId.js → contiene export function generateUniqueId()
- parseUserResponse.js → contiene export function parseUserResponse()

## 4.7\. Constantes (UPPER_SNAKE_CASE)

Cuando un valor es constante, usar las mayúsculas.

**Ejemplos**

- API_BASE_URL
- MAX_RETRIES
- DEFAULT_PAGE_SIZE

## 4.8\. Clases CSS (kebab-case)

Las clases CSS o SCSS deben ser simples y legibles.

**Ejemplos**

- page-header
- user-card
- button-primary

## 4.9\. Directorios y módulos

Para carpetas y módulos compartidos.

**Reglas**

- Usar **kebab-case** para carpetas:
  - components/
  - user-profile/
  - hooks/
  - utils/
- Un componente por carpeta cuando tiene archivos auxiliares (estilos, tests, index):
  - UserProfile/
    - UserProfile.tsx
    - UserProfile.css
    - index.ts

## 4.10\. Nombres de Contextos

El nombre del contexto debe dejar claro el dominio y terminar en **Context**.

**Ejemplos**

- AuthContext
- ThemeContext
- SessionContext

**El provider:**

- AuthProvider
- ThemeProvider

## 4.11\. Nombres de Reducers y Actions

Para proyectos con **useReducer** o cualquier arquitectura basada en reducers.

**Reducer**

- userReducer
- cartReducer

**Actions**

- Mayúsculas para los tipos

```javascript
const ADD_TO_CART = "ADD_TO_CART";
const SET_USER = "SET_USER";
```

## 4.12\. Nombres de Tests

Para mantenibilidad.

**Archivos**

- UserProfile.test.tsx
- useAuth.test.ts

**Descripciones (describe, it)**

- Claras y expresivas, no crípticas

# 5. Organización del Proyecto

_(Basada en la arquitectura y convenciones de Next.js)_

La organización del proyecto es un pilar crítico para mantener un código ordenado, comprensible y escalable.

# Estructura de Base del Proyecto

La siguiente estructura ofrece un equilibrio entre simplicidad, escalabilidad y claridad:

```
src/
assets/
components/
context/
hooks/
layouts/
models/
services/
styles/
utils/
app/
layout.tsx
page.tsx
```

# Descripción de Carpetas

## assets/

Archivos estáticos usados por la aplicación, como imágenes, íconos, fuentes o archivos multimedia.  
No debe contener componentes, lógica ni estilos globales.

## components/

Componentes reutilizables y desacoplados del dominio específico de una página.  
Representan piezas UI que pueden aparecer en múltiples secciones de la aplicación.

Ejemplos típicos:

- Button/
- Modal/
- Table/

Cuando un componente requiere archivos adicionales (estilos, pruebas, index), debe declararse dentro de su propia carpeta.

```
components/
Button/
Button.tsx
Button.styles.ts
Button.test.tsx
index.ts
```

## context/

Almacena React Contexts y sus respectivos Providers.  
Se utiliza únicamente para estados globales o compartidos entre múltiples secciones.

**Ejemplos**

- AuthContext/
- ThemeContext/

## hooks/

Hooks personalizados reutilizables en la aplicación.  
Todos deben seguir la convención use\<Nombre\> y cumplir las _Rules of Hooks_.

**Ejemplos**

- useAuth.ts
- useDebounce.ts
- useLocalStorage.ts

## layouts/

Diseños globales que envuelven páginas o grupos de páginas.  
Incluyen estructuras comunes como headers, sidebars o footers.

Contiene **layouts reutilizables** que no están directamente ligados a una ruta específica, pero que pueden ser importados y usados dentro de los `layouts.tsx` de `app/` o en páginas concretas.

**Reglas clave**

1. **No reemplaza los layouts de ruta**

- `app/layout.tsx` y `app/<ruta>/layout.tsx` sigue definiendo los layouts globales o por sección.
- Los layouts en `layouts/` son auxiliares o componibles dentro de estos layouts de rutas.

2. **Nombres claros y PascalCase**

- Cada layout debe estar en su propia carpeta con nombre descriptivo.

3. **Separación de estilos y lógica**

- Estilos específicos del layout van en un archivo de estilos dentro de la carpeta.
- Evitar lógica de negocio dentro del layout.

**Ejemplo de estructura**

```
layouts/
DashboardLayout/
DashboardLayout.tsx
DashboardLayout.styles.ts
index.ts
PublicLayout/
PublicLayout.tsx
PublicLayout.styles.ts
index.ts
```

## models/

Contiene definiciones de tipos, interfaces y DTOs utilizados por la aplicación.  
Este apartado es obligatorio en proyectos _TypeScript_ donde se maneja comunicación con APIs o estructuras de datos complejas.

**Ejemplos**

```
models/
user.dto.ts
auth.dto.ts
product.model.ts
```

**Reglas clave**

- Un archivo por entidad o modelo
- Nombres claros y consistentes para las interfaces: _User, AuthResponse, ProductDetail_
- No incluir lógica en esta carpeta: únicamente estructuras de datos

## app/

Contiene las rutas de la aplicación, usando la filosofía del App Router de Next.js. Cada carpeta dentro de `app/` representa una ruta, y los archivos `page.tsx` representan las pantallas completas de cada ruta.

**Estructura recomendada.**

```
app/
layout.tsx
page.tsx
home/
page.tsx
login/
page.tsx
users/
layout.tsx
page.tsx
[id]/
page.tsx
components/
UserCard.tsx
```

**Reglas clave**

1. **Cada ruta tiene su carpeta**

- El archivo `page.tsx` define la UI principal de la ruta.
- Rutas dinámicas se crean con corchetes **\[params\]**.

2. **Layouts por ruta**

- Se puede tener un `layout.tsx` global y layouts por sección para agrupar varias rutas.
- Los layouts manejan estructura común (headers, sidebars, footers).

3. **Componentes específicos de la página o sección**

- Deben declararse en una subcarpeta `components/` dentro de la ruta correspondiente.
- Ejemplo: `/app/users/components/UserCard.tsx`
- No deben mezclarse con los componentes reutilizables de `src/components/`.

4. **Componentes reutilizables**

- Los componentes que se usan en múltiples rutas deben vivir en `src/components/`.
- Ejemplo: botones, modales, tablas, tarjetas generales.

**Rutas dinámicas con múltiples parámetros**

Además de las rutas dinámicas básicas como `/users/[id]`, Next.js permite manejar escenarios más complejos donde una ruta requiere varios parámetros. Existen dos formas oficiales de lograrlo: múltiples segmentos dinámicos y segmentos tipo catch-all.

1. **Múltiples segmentos dinámicos (parámetros fijos con nombre)**  
   Ideal cuando la URL tiene estructura clara y predecible, por ejemplo:

```
/users/123/orders/55
```

    **Estructura**

```
app/
users/
[userId]/
orders/
[orderId]/
page.tsx
```

    **Uso de parámetros**

```typescript
export default function Page({
  params,
}: {
  params: { userId: string; orderId: string };
}) {
  return <div>{params.userId} — {params.orderId}</div>;
}
```

**Cuándo usarlo**  
Cuando la ruta tiene parámetros bien definidos: userId, postId, productId, etc. Es la opción más clara y mantenible.

2. **Segmentos catch-all para múltiples valores variables**  
   Sirven cuando la URL puede tener una cantidad flexible de partes. Por ejemplo:

```
/products/televisores/samsung/4k
```

**Estructura**

```
app/
products/
[...filters]/
page.tsx
```

**Uso de parámetros**

```typescript
export default function Page({ params }: { params: { filters: string[] } }) {
  console.log(params.filters);
  // ["televisores", "samsung", "4k"]
}
```

**Cuándo usarlo**  
Cuando no se sabe cuántos segmentos habrá, o cuando la ruta representa filtros, categorías o navegación flexible.

## services/

Lógica relacionada con comunicación con APIs, integración con servicios externos o reglas de negocio desacopladas del UI.

**Ejemplos**

- authService.ts
- userService.ts
- productService.ts

**Recomendaciones**

- Servicios deben ser funciones puras (sin dependencias de UI)
- Todas las llamadas HTTP deben vivir aquí, nunca dentro de componentes
- Usar los modelos definidos en `models/` para tipado estricto

## styles/

Estilos globales, temas, variables o archivos base del sistema visual.  
No colocar estilos específicos de componentes en esta carpeta.

## utils/

Funciones puras de utilidad que no dependen de React ni del estado de la aplicación.

**Ejemplos**

- formatDate.ts
- capitalize.ts
- deepClone.ts

# Principios Generales de Organización

## 1\. Un componente por responsabilidad

Si un componente crece demasiado o empieza a mezclar responsabilidades, dividirlo.  
La composición siempre es preferible a los “componentes gigantes”.

##

## 2\. Evitar estructuras de carpetas innecesariamente profundas

La simplicidad es un activo. Evitar rutas como:

```
components/ui/forms/inputs/text/TextInput/
```

Una profundidad moderada acelera la lectura:

```
components/
TextInput/
```

## 3\. Archivos Index moderados, no excesivos

Usar cuando realmente simplifiquen importaciones dentro de un módulo:

**Correcto:**

```
Button/
Button.tsx
index.ts // export { Button }
```

**Incorrecto:**

```
components/
index.ts // export * from todas las carpetas
```

## 4\. Código orientado a propósito, no a conveniencia

Ubicar cada archivo donde realmente pertenece:

- Componente reutilizable → components/
- Componente exclusivo de una página → /pages/\<Page\>/components/
- Hook reutilizable → hooks/
- Hook de dominio específico → _subcarpeta de la página_
- Lógica de negocio o API → services/
- DTOs y modelos → models/
- Ayudas puras → utils/

## 5\. Nota Opcional: Organización por Funcionalidades (Feature Folders)

Aunque **no es el estándar oficial del proyecto**, algunos equipos optan por agrupar módulos completos por funcionalidad.

**Ejemplo**

```
src/
auth/
LoginPage.tsx
useLogin.ts
authService.ts
auth.dto.ts
```

Este estilo puede adoptarse en proyectos grandes; sin embargo, se recomienda mantener la estructura base definida.

# Estilos (styles)

La gestión de estilos en un proyecto React con TypeScript puede organizarse de dos formas principales: **global** y **por componente**. Cada una tiene sus reglas y convenciones.

## 1\. Estilos globales

- Se almacenan en la carpeta `styles/` dentro de `src/` o en la raíz del proyecto.
- Incluyen:
  - Variables de tema (colores, tipografía, espaciados, breakpoints).
  - Estilos base y resets.
  - Configuración de librerías CSS-in-JS si se usa.

```
styles/
global.css    ← resets y estilos globales
theme.ts   ← variables de tema y configuración
stitches.config.ts  ← configuración de CSS-in-JS (opcional)
```

**Reglas clave**

- No colocar estilos de componentes aquí.
- Mantener únicamente reglas globales o compartidas.

## 2\. Estilos específicos de componentes

Existen dos opciones principales para manejar estilos de manera encapsulada:

1. **CSS-in-JS (.styles.ts)**

- Usando librerías como **Stitches, Styled Components** o similares.
- Permite:
  - Tipado completo en TypeScript.
  - Uso de variables de tema.
  - Lógica condicional dentro de estilos.
  - Encapsulación de estilos por componente.

**Ejemplo**

```typescript
// components/Button/Button.styles.ts
import { styled } from "@/styles/stitches.config";
export const ButtonContainer = styled("button", {
  padding: "8px 16px",
  borderRadius: "4px",
  backgroundColor: "$primary",
  color: "$onPrimary",
  "&:hover": {
    backgroundColor: "$primaryDark",
  },
});
```

```typescript
// components/Button/Button.tsx
import { ButtonContainer } from "./Button.styles";
interface ButtonProps {
  label: string;
  onClick?: () => void;
}
export default function Button({ label, onClick }: ButtonProps) {
  return <ButtonContainer onClick={onClick}>{label}</ButtonContainer>;
}
```

2. **CSS Modules (.module.css o .module.scss)**

- Se usan estilos tradicionales, encapsulados automáticamente por Next.js.
- No requiere librerías externas.
- Cada componente importa su propio archivo `.module.css` o `.module.scss`.

**Ejemplo**

```css
/* components/Button/Button.module.scss */
.button {
  padding: 8px 16px;
  border-radius: 4px;
  background-color: blue;
  color: white;
}
```

```typescript
import styles from "./Button.module.scss";

export default function Button({ label }: { label: string }) {
  return <button className={styles.button}>{label}</button>;
}
```

**Reglas clave para estilos de componentes**

1. Mantener los estilos junto al componente (`.styles.ts` o `.module.css`/`.module.scss`).
2. Usar variables y temas definidos en `styles/` para mantener consistencia visual.
3. Evitar lógica de negocio dentro de los archivos de estilo.
4. No colocar estilos globales dentro de los componentes, salvo excepciones justificadas (ej. overrides temporales).

# Lineamientos para el Uso de TypeScript en Proyectos React

# 1\. Modelos y Definiciones de Tipos

## 1.1 Ubicación y organización

Los modelos (DTOs), interfaces y tipos del dominio deben almacenarse en src/models/.

**Ejemplo de estructura**

```
src/
models/
User.ts
Product.ts
AuthResponse.ts
```

## 1.2 Nomenclatura

- Usar **PascalCase** para interfaces y tipos exportados
- Cada modelo debe ir en un archivo propio

**Ejemplo correcto**

```typescript
// src/models/User.ts
export interface User {
  id: number;
  name: string;
  email: string;
}
```

## 1.3 `interface` vs `type`

- _interface:_ estructura de objetos
- _type:_ alias, uniones, combinaciones

**Ejemplo correcto**

```typescript
export interface Product {
  id: number;
  title: string;
}

export type ApiResponse<T> = {
  success: boolean;
  data: T;
};
```

## 1.4 Evitar tipos implícitos

Toda función, constante o módulo exportado debe incluir tipo explícito.

**Incorrecto**

```typescript
export const TAX = 0.16; // Sin tipo explícito
```

**Correcto**

```typescript
export const TAX: number = 0.16;
```

# 2\. Componentes en React con TypeScript

## 2.1 Tipado de props

Declarar explícitamente la estructura de las props.  
**Correcto**

```typescript
interface UserCardProps {
  user: User;
}

export function UserCard({ user }: UserCardProps) {
  return <div>{user.name}</div>;
}
```

## 2.2 Evitar `any`

El tipo _any_ rompe la seguridad de tipos.

**Incorrecto**

```typescript
function save(data: any) {
  /* ... */
}
```

**Incorrecto**

```typescript
function save(data: User): void {
  // ...
}
```

## 2.3 Valores derivados con tipo claro

Cuando el tipo pueda causar confusión, declararlo explícitamente.

```typescript
const total: number = items.reduce((sum, item) => sum + item.price, 0);
```

# 3\. Hooks en React con TypeScript

## 3.1 Tipado en `useState`

Cuando el valor inicial no permite inferencia, tipar explícitamente.

```typescript
const [count, setCount] = useState<number>(0);
```

Ejemplo con tipos completos.

```typescript
const [user, setUser] = useState<User | null>(null);
```

## 3.2 Uso de `useReducer`

Cuando el estado sea complejo, definir tipos para estado y acciones.

```typescript
interface CounterState {
  count: number;
}

type CounterAction = { type: "inc" } | { type: "dec" };

function reducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case "inc":
      return { count: state.count + 1 };
    case "dec":
      return { count: state.count - 1 };
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0 });
```

## 3.3 Hooks personalizados tipados

```typescript
export function useUser(): { user: User | null; load: () => Promise<void> } {
  const [user, setUser] = useState<User | null>(null);

  async function load() {
    const data = await fetchUser();
    setUser(data);
  }

  return { user, load };
}
```

# 4\. Manejo de Eventos y Formularios

## 4.1 Tipos de eventos de React

```typescript
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}
```

## 4.2 Formularios tipados

```typescript
interface LoginForm {
  email: string;
  password: string;
}

function Login() {
  const [form, setForm] = useState<LoginForm>({ email: "", password: "" });

  return (
    <input
      value={form.email}
      onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
        setForm({ ...form, email: e.target.value })
      }
    />
  );
}
```

# 5\. Servicios y Peticiones a la API

## 5.1 Funciones de servicios tipadas

```typescript
export async function getUser(id: number): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}
```

## 5.2 Estructuras genéricas

```typescript
export interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export async function fetchUsers(): Promise<ApiResponse<User[]>> {
  const res = await fetch("/api/users");
  return res.json();
}
```

# 6\. Utilidades y Funciones Auxiliares

## 6.1 Tipado explícito

```typescript
export function formatUser(user: User): string {
  return `${user.name} (${user.id})`;
}
```

## 6.2 Funciones genéricas

```typescript
export function identity<T>(value: T): T {
  return value;
}
```

# 7\. Configuración TypeScript Recomendada

## 7.1 Strict Mode

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

## 7.2 Alias de rutas

```json
{
  "compilerOptions": {
    "baseUrl": "src",
    "paths": {
      "@models/*": ["models/*"],
      "@components/*": ["components/*"]
    }
  }
}
```

**Uso:**

```typescript
import { User } from "@models/User";
```

# 8\. Errores Comunes a Evitar

- Uso injustificado de _any_.
- Props sin tipos definidos.
- Hooks personalizados sin tipos de entrada/salida.
- Duplicación de tipos entre carpetas.
- Uniones demasiado amplias sin propósito.
- Eliminación del _strict mode_.
