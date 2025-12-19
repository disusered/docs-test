---
title: Precios dinámicos
---

# Descripción

El presente documento describe alternativas y consideraciones clave para la implementación de un **modelo de precios dinámicos** en la venta de boletos para un estadio de fútbol, con proyección a otros tipos de eventos (conciertos, espectáculos) y a su reutilización en otros estadios o recintos.

Se analizan dos enfoques estratégicos:

1. **Uso de soluciones existentes** (APIs, SDKs, plataformas especializadas).
2. **Desarrollo de un motor propio de precios dinámicos**.

Para cada alternativa se describen ventajas, desventajas, tiempos estimados, riesgos, y el impacto en el negocio, así como consideraciones especiales como cortesías y promociones.

# Metas

1. Maximizar ingresos totales, no solo el volumen de ventas.
2. Optimizar la ocupación del establecimiento.
3. Vender antes y mejor, ajustando precios según el momento.
4. Reducir inventario no vendido cerca del evento.
5. Adaptarse a diferentes mercados y recintos sin redefinir toda la estrategia.

La solución debe ser flexible, escalable, configurable por evento y recinto enfocado a usuarios de áreas como ventas, marketing y gerencia.

# Comparativas

Para tomar una decisión informada, hemos analizado dos caminos: adquirir una solución de terceros o desarrollar un motor propio.

**_Solución de terceros_**

| Ventajas                                       | Desventajas                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------- |
| Implementación en semanas o pocos meses        | Comisiones por boleto y/o licencias mensuales                    |
| IA entrenada con millones de eventos globales  | No tenemos control total sobre por qué el precio cambios         |
| El proveedor se encarga de las actualizaciones | Si el proveedor sube precios o falla, el negocio se detiene      |
| Menos carga para nuestro equipo de desarrollo  | Dificultad para adaptar reglas muy específicas del negocio local |

#### [**QCue**](https://onlocationexp.com/tip) **(Líder en Deportes/Eventos)**

Ofrecen Ticketing Intelligence / dynamic pricing para equipos y estadios. Se centran en maximizar ingresos por asiento con reglas específicas para el fan fairness. Es el estándar en la industria deportiva de EE.UU. (usado por muchos equipos de la MLB y NBA). Se integra con las boleteras grandes.

- **Enfoque:** Volumen y Rentabilidad.
- **Costo:** **Alto / Bajo Cotización.** No publican precios, pero operan bajo un modelo de **Licencia Anual \+ % del "Lift"** (porcentaje del ingreso _extra_ que generaron). Estamos hablando de miles de dólares al año.
- **Integración:** Tienen una API robusta que se conecta a tu inventario. Su algoritmo analiza ventas históricas, clima, desempeño del equipo/artista y ventas secundarias (mercado de reventa).

[**Pricemoov**](https://pricemoov.com/platform) **(Plataformas de precios dinámicos)**

Es una solución rápida para fijar precios inteligentes y liberar todo tu potencial de ingresos. Combina un software de fijación de precios muy fácil de usar para probar y controlar los precios en toda la organización y los canales y una tecnología de ciencia de datos ágil que analiza continuamente todos los datos relevantes para ayudar en la toma de decisiones y ahorrar tiempo en el análisis.

- **Enfoque:** Pricing avanzado para varios sectores.
- **Costo:** **Alto / Bajo Cotización.** Un estimado de 2,000 dlls al mes \+ posibles cargos extras.
- **Integración:** Tienen una API que se alimenta en tiempo real sobre los precios del mercado.

#### [**Digonex**](https://www.digonex.com/) **(Enfoque en Atracciones y Cultura)**

Sus algoritmos de precios fueron desarrollados por un equipo de economistas con doctorados, estos realizan el trabajo de recopilar datos, analizar patrones y determinar el precio óptimo.

- **Enfoque:** Rentabilidad equilibrada (Fairness). Sus algoritmos son conocidos por ser menos agresivos que los de las aerolíneas.
- **Costo:** **Cotización personalizada.** Generalmente tarifa fija mensual. Su precio depende del tamaño del establecimiento, su uso, metas, requiere un contacto directo con su agente de ventas.
- **Integración:** API REST, actuando como un motor externo.

Otras opciones a considerar [PROS](https://pros.com/industries/services/), [Zilliant](https://zilliant.com) y [DynamO Pricing](https://www.dynamopricing.com/).

- **Enfoque:** PROS se enfoca en predecir la disposición a pagar, Zillant se enfoca en optimizar el precio del producto e incrementar ventas y DynamO Pricing se enfoca en la venta rápida del producto.
- **Costo:** PROS es una suscripción anual, pero suele requerir proyectos de implementación largos y costosos. Zilliant es ligeramente menor a PROS debido a una implementación más ágil y DynamO Pricing suele tener un costo debido a que se basan en un porcentaje sobre el “lift” (incremento de las ventas) o sobre los boletos que se vendieron con un precio optimizado.
- **Integración:** Todos se integran por medio de un API REST con la posibilidad de necesitar algún trabajo extra para una completa integración.

**_Desarrollo propio_**

| Ventajas                                                             | Desventajas                                                                        |
| :------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| El algoritmo es un activo del negocio, vendible a otros estadios     | Requiere una inversión inicial de tiempo mayor                                     |
| Ajuste fino para cortesías, promociones locales y reglas específicas | Se requerirá de un equipo de desarrollo para mantener y evolucionar la herramienta |
| Eliminación de comisiones por transacciones a terceros               | Requiere investigación y pruebas para calibrar el modelo                           |
| La información nunca sale de nuestros servidores                     |                                                                                    |

Aquí hay que tener en cuenta que el motor inicial no usa Inteligencia Artificial, sino que se implementaran reglas deterministas que el usuario final configura. Será transparente y fácil de auditar.

- **Enfoque:** El motor debe poder tener tres enfoques: Rentabilidad (el precio máximo que el cliente está dispuesto a pagar), Volumen (llenar el lugar para que aumentar el consumo secundario) y el Mixto (llenar el lugar lo más posible a un precio optimizado).
- **Integración:** La integración se basará en poder implementar variables de comportamiento para que nos regresen un valor que afectará el precio base.  
  Para la rentabilidad se usan las variables: histórico de precios, precios de la competencia y atributos del evento, como el artista, clima y día de la semana. Para el volumen se usan las variables como: días restantes para el evento, capacidad total vs vendidos, tasa diaria de venta. Para el mixto serían todas las anteriores más implementar el precio más bajo y el más alto (para evitar saltos de precios desmesurados) y otras reglas de la venta justa, más la recomendación de que se requiera la validación humana para tener un comportamiento más esperado.

# Implementaciones

A continuación se presentan los planes de tiempos estimados para la implementación de precios dinámicos.

## Solución de terceros (3 a 5 Meses)

- Mes 1: Selección de proveedor y firma de contrato.
- Mes 2: Desarrollo de conectores API (Middleware en .NET) para enviar inventario y recibir precios.
- Mes 3: Pruebas de integración en ambiente Staging y configuración de reglas de negocio.
- Mes 4: Despliegue productivo (“Go Live”).

Riesgos: Rapidez de comunicación con el proveedor, necesidad de alimentar a la herramienta, si realmente podemos configurar los comportamientos deseados, implementaciones adicionales.

## Desarrollo propio (4 a 6 meses)

- Mes 1-2: Diseño de arquitectura y lógica de negocio (algoritmo o algoritmos para calcular los precios dinámicos).
- Mes 3-4: Desarrollo de motor de reglas y panel de administración.
- Mes 5: Simulación: El motor se utiliza en un escenario real, pero no cambia precios, solo se guardan los resultados. (Corroborar que el motor se comportó de la forma esperada).
- Mes 6: Go live con Reglas.

Riegos: La implementación gradual de módulos de Machine Learning no están contemplados para este desarrollo, pero sí en el diseño de arquitectura para que estos puedan ser alimentados. Debemos tener en cuenta que estos algoritmos tienden a evolucionar, por lo que requerirá trabajo de mantenimiento y desarrollo.

**CONCLUSIÓN**

Considerando la visión de expandir este sistema a otros estadios y edificaciones, la recomendación es optar por crear nuestro propio motor de precios dinámicos por las siguientes razones:

- Al replicar el modelo en otros estadios, el costo es cero. Con un proveedor externo pagaremos licencias/servicios por cada réplica.
- Creamos un motor específico para nuestro plan de trabajo que se alimenta de datos locales, creando así un motor más personalizado para cada estadio al momento de implementar la IA.
- Se tendrá el control total del comportamiento de los algoritmos, pudiendo adaptar reglas locales y no globales.

**ANEXO**

Ejemplo de un algoritmo base para el cálculo dinámico de precios.

Variables clave:

- Capacidad total
- Precio base justo
- Precio mínimo / máximo
- Ritmo de ventas
- Tiempo al evento
- Tipo de evento
- Pronostico clima en el dia del evento
- Optimismo
- Historial de eventos similares (Se usará en la fase 2\)

El algoritmo no es magia; es un **motor de decisiones** que evalúa el contexto del evento en tiempo real y ajusta el precio para encontrar el equilibrio perfecto entre oferta y demanda.

La idea es que el algoritmo pueda funcionar con el “input” del personal de ventas, marketing o gerencia que conozcan el mercado y saben cómo se debería reaccionar en la venta

Imaginemos el cálculo como una fórmula sencilla:

1. **Precio Calculado** \= Precio Base (**Tipo de Evento**)
2. **\+** Un extra si se vende muy rápido (**Ritmo de Ventas**)
3. **\+** Un extra si quedan pocos lugares (**Capacidad**)
4. **\+/-** Ajuste por urgencia de fecha (**Tiempo**)
5. **\+/-** Ajuste por contexto (**Clima** \+ **Historial**)
6. \+/- Ajuste por intuición (**Optimismo \+ Seat Score**)
7. **Resultado Final** \= El precio calculado, pero **SIEMPRE** dentro de los límites (Mínimo y Máximo).

## Ejemplo de Escenario Real

_Faltan 2 días para el partido (Tiempo), se pronostica lluvia (Clima), pero es contra el clásico rival (Tipo de evento) y quedan pocos asientos (Capacidad)._

- **El Algoritmo dice:** "La lluvia bajaría el precio, PERO la escasez y la importancia del rival pesan más. **Decisión:** Mantener el precio alto, pero no subirlo más.". 

El proceso se divide en 5 fases lógicas:

### 1\. El Punto de Partida (La Base)

Todo cálculo comienza con un valor ancla para asegurar que el precio sea razonable desde el inicio.

- **Variable: Precio Base Justo**
  - _Lógica:_ Es el precio "estándar" que cobraremos en condiciones normales.
- **Variable: Tipo de Evento**
  - _Lógica:_ Aplica un multiplicador inicial. ¿Es una final de campeonato o un partido amistoso?
  - _Ejemplo:_ Si es un evento "Premium", el precio base arranca un 20% más alto.

### 2\. El Termómetro de Demanda (Ajuste en Tiempo Real)

Aquí es donde el algoritmo "siente" el mercado. Si la gente compra rápido, el valor sube; si compra lento, se ajusta para incentivar.

- **Variable: Ritmo de Ventas (Velocidad)**
  - _Lógica:_ ¿Cuántos boletos se vendieron en la última hora?
  - _Acción:_ Si la velocidad es alta (ej. \>100 boletos/hora), el precio sube ligeramente para capturar ese alto interés. Si es baja, el precio se mantiene o baja suavemente.
- **Variable: Capacidad Total vs. Ocupación Actual**
  - _Lógica:_ La escasez genera valor.
  - _Acción:_
    - Queda mucho espacio (0-50% ocupado) \-\> Precio relajado.
    - Quedan pocos lugares (90% ocupado) \-\> Precio agresivo (Premium).

### 3\. El Factor Contexto (Variables Externas)

El algoritmo mira "hacia afuera" para anticipar cambios en la decisión de compra del usuario.

- **Variable: Tiempo al Evento**
  - _Lógica:_ La urgencia cambia el valor.
  - _Acción:_ Generalmente, el precio sube a medida que se acerca la fecha (curva de urgencia). Sin embargo, si faltan 24 horas y hay mucho espacio, el algoritmo puede lanzar ofertas de último minuto.
- **Variable: Pronóstico del Clima**
  - _Lógica:_ El clima afecta la disposición a asistir (especialmente en eventos al aire libre).
  - _Acción:_
    - _Sol/Buen clima:_ Aumenta la probabilidad de asistencia \-\> Sube el precio ligeramente.
    - _Lluvia pronosticada:_ Baja la demanda espontánea \-\> El precio se ajusta a la baja para convencer a los indecisos.
- **Variable: Historial de Eventos Similares (Machine Learning)**
  - _Lógica:_ "La historia se repite".
  - _Acción:_ El sistema mira qué pasó la última vez con un evento igual (mismo rival, mismo día de la semana). Si históricamente ese evento vende todo 3 días antes, el algoritmo subirá los precios antes de lo normal.

### 4\. Factor de Intuicion (Variables Internas)

Podemos incluir variables que simulan el ánimo o la estrategia del momento, técnicamente no es “suerte” sino variables de gestión que permitan inclinar el algoritmo sin romperlo.

- **Variable: Optimismo**
  - _Logica_: “La variable humana”
  - _Acción_: Empodera al equipo comercial. El algoritmo hace el cálculo duro, pero el humano define la actitud de venta.
    - Modo "Conservador" (±3%): "Queremos ir a lo seguro, priorizamos llenar el lugar sobre la ganancia." El algoritmo suprime las subidas bruscas de precio.
    - Modo "Neutro" (±5%): El algoritmo sigue su lógica matemática estándar.
    - Modo "Tiburón" (±8%): "Me siento con suerte/optimista". El equipo de ventas percibe un hype en la calle que los datos aún no ven. Le dicen al algoritmo: "Sé agresivo, sube los precios más rápido ante el menor signo de demanda".
- **Variable: Seat Score**
  - _Logica_: “Calidad de la ubicación”
  - _Acción_: No todas las secciones son iguales. Pasillo vs centro, Sobra vs Sol. Esto permitirá hacer micro ajustes de precio en base al nivel de granularidad del inventario, permitiendo calcular en base al nivel, zona, fila o asiento dependiendo el ajuste indicado.

### 5\. Los Límites de Seguridad (Protección de Marca)

Para evitar precios ridículos o devaluación de la marca, establecemos barreras inquebrantables.

- **Variables: Precio Mínimo / Precio Máximo**
  - _Regla:_ Sin importar qué tan alta sea la demanda, el precio nunca superará el Máximo (para no enojar a los fans). Sin importar qué tan baja sea la venta, nunca bajará del Mínimo (para no regalar el producto).
