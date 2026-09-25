# Banco de preguntas de entrevista (con respuestas cortas)

Para después de la prueba práctica, o si te piden explicar tu código. Respuestas de 20–40 segundos: **concepto + ejemplo concreto**.

---

## 1. Sobre ti y el puesto (prepara TU versión)

**¿Por qué quieres trabajar en el ISTE?**
> "Me atrae desarrollar sistemas que usan estudiantes y docentes todos los días: matrículas, laboratorios, notas. El stack del puesto (PHP, Python, JavaScript, SQL, WordPress) coincide con lo que he trabajado, y en un entorno educativo puedo seguir aprendiendo y aportar rápido."

**Háblame de un proyecto del que estés orgulloso.**
> Usa **STAR**: Situación (contexto) → Tarea (tu responsabilidad) → Acción (qué hiciste tú, con tecnologías concretas) → Resultado (medible: "redujo de 2 días a 2 horas", "lo usan 200 estudiantes").

**¿Cuál es tu mayor debilidad?**
> Una real, pequeña y en mejora: "A veces quería entregar rápido y omitía las pruebas. Ahora escribo pruebas de las reglas críticas antes de dar algo por terminado."

**¿Cómo aprendes una tecnología nueva?**
> "Documentación oficial, un proyecto pequeño de práctica, y después aplicarlo en algo real. Por ejemplo, aprendí React haciendo un CRUD que consumía mi propia API."

**¿Qué haces si no sabes resolver algo?**
> "Primero lo investigo con un tiempo límite (documentación, errores, Stack Overflow). Si en ~30–60 minutos no avanzo, pregunto con contexto: qué intenté y qué error obtuve."

**¿Cómo manejas un desacuerdo técnico con un compañero?**
> "Con datos: comparamos las opciones por criterios (tiempo, mantenimiento, rendimiento), probamos si hace falta y, si no hay acuerdo, decide el líder técnico y yo me alineo."

**¿Trabajo bajo presión / plazos cortos?**
> "Priorizo lo que da valor primero (lo mínimo funcional), comunico riesgos temprano y no sacrifico lo básico: control de versiones y probar antes de entregar."

**¿Dónde te ves en 3 años?**
> "Como desarrollador semi-senior del equipo, dominando los sistemas de la institución y ayudando a los nuevos."

**Pretensión salarial** (dice "a convenir"): investiga un rango para Ambato y para un junior. Una respuesta posible: "Estoy abierto a la escala de la institución para el cargo; para mí pesan también el aprendizaje y la estabilidad."

**Preguntas para hacerles al final (demuestran interés):**
- ¿Qué sistemas mantiene actualmente la Unidad de TI y con qué tecnologías?
- ¿Cómo es el flujo de trabajo: control de versiones, revisiones de código, despliegues?
- ¿Cuál sería mi primer proyecto o responsabilidad?
- ¿Cómo está conformado el equipo?

---

## 2. Programación general

| Pregunta | Respuesta corta |
|---|---|
| ¿Compilado vs interpretado? | El compilado se traduce a código máquina o bytecode antes de ejecutarse (Java, C#); el interpretado se ejecuta línea por línea (Python, JS; en la práctica usan JIT). |
| ¿Tipado estático vs dinámico? | Estático: el tipo se revisa al compilar (Java, C#, TS). Dinámico: se revisa al ejecutar (Python, JS, PHP). |
| ¿Paso por valor vs referencia? | Por valor se copia el dato; por referencia se pasa la dirección y los cambios afectan al original. En Python y JS los objetos se pasan por "referencia compartida". |
| ¿Qué es la recursión? | Una función que se llama a sí misma con un caso base que la detiene. Ejemplo: factorial o recorrer carpetas. |
| ¿Stack vs heap? | Stack: memoria de llamadas y variables locales, rápida y limitada. Heap: objetos dinámicos, la gestiona el garbage collector. |
| ¿Qué es un algoritmo? ¿Big O? | Pasos finitos para resolver un problema. Big O mide cómo crece el tiempo o la memoria con n: O(1), O(log n), O(n), O(n log n), O(n²). |
| ¿Array vs lista enlazada? | Array: acceso por índice O(1), insertar en medio O(n). Lista enlazada: insertar O(1) si tienes el nodo, acceso O(n). |
| ¿Pila vs cola? | Pila LIFO (deshacer, llamadas). Cola FIFO (atención de turnos, tareas). |
| ¿Hash table? | Estructura clave→valor con acceso promedio O(1): dict, Map, HashMap. |
| ¿Síncrono vs asíncrono? | Síncrono bloquea hasta terminar; asíncrono continúa y recibe el resultado después (callbacks, promesas, async/await). |
| ¿Qué es una expresión regular? | Un patrón para buscar o validar texto: `^\d{10}$` valida 10 dígitos. |
| ¿Mutable vs inmutable? | Mutable se puede modificar (lista); inmutable no (string, tupla). La inmutabilidad evita efectos secundarios. |

## 3. POO

| Pregunta | Respuesta |
|---|---|
| 4 pilares | **Encapsulamiento** (ocultar estado, exponer métodos), **Abstracción** (mostrar lo esencial), **Herencia** (reutilizar de una clase padre), **Polimorfismo** (misma interfaz, distinto comportamiento). |
| ¿Clase vs objeto? | La clase es el molde; el objeto es una instancia concreta. |
| ¿Interfaz vs clase abstracta? | Interfaz: solo un contrato, se pueden implementar varias. Abstracta: puede tener estado y código, se hereda una sola. |
| ¿Sobrecarga vs sobrescritura? | Sobrecarga: mismo nombre y distintos parámetros. Sobrescritura: la subclase redefine un método del padre. |
| ¿Composición vs herencia? | Composición: "tiene un" (Carrito tiene Productos). Herencia: "es un" (Docente es Empleado). Se prefiere la composición porque acopla menos. |
| ¿Qué es un constructor? | Método que inicializa el objeto al crearlo. |
| ¿`static`? | Pertenece a la clase y no a la instancia (contador compartido, métodos utilitarios). |
| SOLID | **S**: una responsabilidad por clase. **O**: abierta a extensión, cerrada a modificación. **L**: una subclase puede reemplazar a su padre. **I**: interfaces pequeñas. **D**: depender de abstracciones, no de implementaciones concretas. |
| Ejemplo de Open/Closed | Agregar `Tesis extends Material` sin tocar `prestar()` (ver `06-retos-resueltos/java-consola-poo`). |
| Patrones de diseño que conoces | **Singleton** (una instancia: conexión), **Factory** (crear objetos según tipo), **Repository/DAO** (acceso a datos), **MVC**, **Observer** (eventos), **Strategy** (algoritmos intercambiables). |

## 4. Bases de datos

| Pregunta | Respuesta |
|---|---|
| ¿PK vs FK? | La PK identifica cada fila (única, no nula); la FK referencia la PK de otra tabla y garantiza la integridad referencial. |
| ¿INNER vs LEFT JOIN? | INNER devuelve solo las coincidencias; LEFT devuelve todas las filas de la izquierda (con NULL si no hay match). |
| ¿WHERE vs HAVING? | WHERE filtra filas antes de agrupar; HAVING filtra grupos después del GROUP BY. |
| ¿DELETE vs TRUNCATE vs DROP? | Borra filas (se puede filtrar y revertir) / vacía la tabla completa (rápido) / elimina la tabla. |
| Normalización | Organizar para evitar redundancia: 1FN valores atómicos, 2FN sin dependencias parciales, 3FN sin dependencias transitivas. |
| ¿Índice? | Estructura que acelera búsquedas (como el índice de un libro); hace más lentas las escrituras. |
| ACID | Atomicidad (todo o nada), Consistencia (reglas válidas), Aislamiento (transacciones que no se interfieren), Durabilidad (lo confirmado persiste). |
| ¿Transacción? | Grupo de operaciones que se confirma (COMMIT) o se deshace (ROLLBACK) en bloque. Ejemplo: una transferencia bancaria. |
| SQL Injection | Meter SQL malicioso en un input (`' OR '1'='1`). Se previene con **consultas parametrizadas**, nunca concatenando. |
| ¿Vista? | Consulta guardada que se usa como tabla. |
| ¿Procedimiento almacenado vs función? | El procedimiento ejecuta acciones (puede no devolver valor, se llama con CALL); la función devuelve un valor y se usa dentro de un SELECT. |
| ¿Trigger? | Código que se ejecuta automáticamente ante INSERT, UPDATE o DELETE (ej. descontar stock). |
| ¿SQL vs NoSQL? | SQL: tablas con esquema, relaciones, ACID (notas, pagos). NoSQL: documentos o clave-valor flexibles y escalables (logs, catálogos). |
| ¿ORM? | Mapea tablas a clases (SQLAlchemy, Eloquent, Entity Framework, Hibernate, Prisma). Ventaja: productividad; desventaja: menos control y posibles consultas ineficientes (problema N+1). |
| ¿Cómo optimizas una consulta lenta? | `EXPLAIN`, índices en las columnas de WHERE y JOIN, evitar `SELECT *`, paginar, evitar funciones sobre columnas indexadas en el WHERE. |

## 5. Web y APIs

| Pregunta | Respuesta |
|---|---|
| ¿Qué pasa al escribir una URL? | DNS → IP → conexión TCP/TLS → petición HTTP → el servidor procesa → respuesta HTML → el navegador descarga CSS/JS y renderiza. |
| Métodos HTTP | GET (leer), POST (crear), PUT (reemplazar), PATCH (modificar parcialmente), DELETE (eliminar). |
| Códigos HTTP | 200 OK, 201 Created, 204 No Content, 301/302 redirección, 400 Bad Request, 401 no autenticado, 403 prohibido, 404 no encontrado, 409 conflicto, 422 validación, 500 error del servidor. |
| ¿REST? | Estilo de API: recursos identificados por URL, verbos HTTP, sin estado y representaciones en JSON. |
| ¿Idempotente? | Repetir la petición deja el mismo resultado: GET, PUT y DELETE sí; POST no. |
| ¿Cookie vs sesión vs JWT? | La cookie guarda datos en el navegador. La sesión guarda los datos en el servidor y el navegador solo tiene un id en una cookie. El JWT es un token firmado que el cliente envía y el servidor verifica sin guardar estado. |
| ¿Autenticación vs autorización? | Quién eres (login) vs qué puedes hacer (roles y permisos). |
| ¿CORS? | Regla del navegador que bloquea peticiones a otro origen, salvo que el servidor lo permita con cabeceras `Access-Control-Allow-*`. |
| ¿Cómo guardas contraseñas? | Con hash lento y sal: bcrypt o argon2 (`password_hash`, `generate_password_hash`). Nunca en texto plano ni con MD5. |
| XSS | Inyectar JavaScript en una página. Se previene escapando la salida (`htmlspecialchars`, `{{ }}` de Jinja, `textContent`) y con Content-Security-Policy. |
| CSRF | Un sitio malicioso hace que tu navegador envíe peticiones a otro sitio con tu sesión. Se previene con tokens CSRF y cookies SameSite. |
| ¿HTTP vs HTTPS? | HTTPS cifra la comunicación con TLS: protege contraseñas y datos. |
| ¿Frontend vs backend vs full stack? | Navegador (UI) / servidor (lógica y BD) / ambos. |
| ¿SSR vs CSR vs SSG? | El servidor genera el HTML / el navegador lo arma con JS / se genera en el build (estático). |
| ¿MVC? | Modelo (datos y reglas), Vista (presentación), Controlador (recibe la petición, coordina y responde). |
| ¿Qué es un middleware? | Función que se ejecuta entre la petición y la respuesta (logs, autenticación, parseo de JSON, errores). |
| ¿Qué es un webhook? | El servidor A llama a una URL tuya cuando ocurre un evento (pago aprobado). |
| ¿GraphQL vs REST? | GraphQL: un endpoint donde el cliente pide exactamente los campos que necesita. REST: varios endpoints por recurso. |

## 6. JavaScript / React / Node

| Pregunta | Respuesta |
|---|---|
| `var` / `let` / `const` | `var`: ámbito de función con hoisting (evitar). `let`: bloque, reasignable. `const`: bloque, no reasignable (pero el objeto sí puede mutar). |
| `==` vs `===` | `==` convierte los tipos antes de comparar; `===` compara valor y tipo. Usa siempre `===`. |
| ¿Closure? | Una función que recuerda las variables del ámbito donde se creó (contador privado, debounce). |
| ¿Event loop? | JS tiene un solo hilo; las tareas asíncronas se encolan y se ejecutan cuando la pila está vacía. Las microtareas (promesas) van antes que las macrotareas (timers). |
| ¿Promesa? | Objeto que representa un valor futuro: pending → fulfilled/rejected. Se usa con `.then` o `await`. |
| `null` vs `undefined` | `undefined`: no asignado. `null`: vacío intencional. |
| ¿Hoisting? | Las declaraciones se "elevan": las funciones completas, `var` sin valor, y `let`/`const` quedan en la zona muerta temporal. |
| `map` vs `forEach` | `map` devuelve un nuevo array; `forEach` solo recorre. |
| ¿Qué es Node? | Entorno para ejecutar JS fuera del navegador (motor V8 + APIs de sistema). Es bueno para I/O concurrente. |
| ¿npm? `package.json`? | Gestor de paquetes. `package.json` lista las dependencias y los scripts; `package-lock.json` fija las versiones exactas. |
| React: estado vs props | El estado es interno y mutable con su setter; las props vienen del padre y son de solo lectura. |
| ¿Virtual DOM? | Copia en memoria; React calcula las diferencias y actualiza solo lo que cambió en el DOM real. |
| `useEffect` | Efectos secundarios después del render (fetch, timers); el array de dependencias controla cuándo se ejecuta, y la función de retorno limpia. |
| ¿Por qué `key`? | Identifica los elementos de una lista para que React sepa cuál cambió. |
| ¿Custom hook? | Función `useAlgo` que encapsula lógica reutilizable con otros hooks. |
| ¿Context? | Comparte datos globales (usuario, tema) sin pasar props por muchos niveles. |

## 7. Python / PHP

| Pregunta | Respuesta |
|---|---|
| ¿Lista vs tupla vs set vs dict? | Mutable ordenada / inmutable / sin duplicados / clave→valor. |
| ¿List comprehension? | `[x*2 for x in lista if x > 0]`: crea listas de forma concisa. |
| ¿`*args`, `**kwargs`? | Argumentos posicionales variables (tupla) y con nombre (diccionario). |
| ¿Decorador? | Función que envuelve a otra para añadir comportamiento (`@app.route`, `@login_requerido`). |
| ¿Entorno virtual? | Aísla las dependencias de cada proyecto (`python -m venv venv`). |
| ¿Flask vs Django? | Flask es minimalista y tú eliges las piezas. Django trae ORM, admin y auth incluidos. |
| ¿GIL? | En CPython solo un hilo ejecuta bytecode a la vez; para CPU se usan procesos, para I/O sirven hilos o async. |
| PHP: `include` vs `require` | Si falla, `require` detiene la ejecución e `include` solo avisa. `_once` evita incluir dos veces. |
| PHP: `==` vs `===` | Igual que en JS: `===` compara también el tipo. |
| PHP: `$_GET`/`$_POST`/`$_SESSION` | Parámetros de la URL / cuerpo del formulario / datos de sesión en el servidor. |
| PHP: ¿PDO vs mysqli? | PDO sirve para varias bases de datos y tiene parámetros con nombre; mysqli es solo para MySQL. |
| ¿Laravel? | Framework MVC de PHP: Eloquent ORM, Blade, migraciones, Artisan. |

## 8. Git, metodologías y buenas prácticas

| Pregunta | Respuesta |
|---|---|
| ¿merge vs rebase? | Merge une historias con un commit de unión; rebase reescribe tus commits encima de otra rama (historial lineal). No hagas rebase de ramas compartidas. |
| ¿Conflicto? ¿Cómo lo resuelves? | Dos cambios en las mismas líneas. Editas el archivo dejando lo correcto, quitas las marcas `<<<<<<<` y haces `add` + `commit`. |
| ¿Pull Request? | Solicitud para integrar una rama, con revisión de código. |
| ¿Qué es un buen commit? | Pequeño, con un solo propósito y un mensaje en imperativo (`feat: agregar filtro por fecha`). |
| Scrum | Sprints de 1–4 semanas. Roles: Product Owner, Scrum Master y equipo. Eventos: planning, daily, review y retrospectiva. Artefactos: product backlog, sprint backlog e incremento. |
| Kanban | Tablero (Por hacer / En progreso / Hecho) con límite de trabajo en curso. |
| ¿Historia de usuario? | "Como **docente** quiero **reservar un laboratorio** para **dar mi clase práctica**", con criterios de aceptación. |
| CI/CD | Integración continua (pruebas automáticas en cada push) y entrega o despliegue continuo. |
| Clean code | Nombres claros, funciones cortas con una tarea, sin duplicación (DRY), manejo de errores y pruebas. |
| ¿Code review? | Otro desarrollador revisa tu código antes de integrarlo: encuentra errores y comparte conocimiento. |
| ¿Deuda técnica? | Atajos que ahorran tiempo hoy y cuestan mantenimiento mañana. |

## 9. Preguntas "de situación" (piensa en voz alta)

- **"El sistema de matrículas está lento el primer día de inscripciones."** Revisaría los logs y el monitoreo, identificaría las consultas lentas (EXPLAIN), agregaría índices, caché de datos estáticos, paginación y, si hace falta, escalaría recursos. Comunicaría el estado a los usuarios.
- **"Encuentras un bug en producción un viernes a las 17h."** Evaluar el impacto; si es crítico, hotfix mínimo probado o revertir al último despliegue estable. Documentar e informar. El arreglo de fondo va con calma.
- **"Te piden una función con un plazo imposible."** Proponer un alcance mínimo (MVP) para la fecha y el resto en una segunda entrega; hacer visibles los riesgos.
- **"Un docente reporta que 'no funciona el sistema'."** Hacer preguntas concretas: qué intentaba hacer, qué mensaje vio, desde qué navegador, pedir una captura. Reproducir el problema y luego corregir.
- **"¿Cómo diseñarías el sistema de reservas de laboratorios?"** Tablas (laboratorios, reservas con FK), regla de choque (`ini1 < fin2 AND ini2 < fin1`), validaciones en el servidor, roles (docente reserva, admin gestiona), API REST y un reporte de uso. Ya lo tienes implementado en el simulacro.
