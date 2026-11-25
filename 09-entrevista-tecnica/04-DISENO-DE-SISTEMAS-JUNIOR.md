# Diseño de sistemas para perfiles junior y semi-senior

A un junior no le piden diseñar Netflix. Le piden algo como *"¿cómo harías un sistema de reservas?"* para ver si sabe **modelar datos, diseñar una API, pensar en las reglas de negocio y en lo que puede fallar**. Si además mencionas cómo escalarlo, sumas puntos.

---

## 1. Método en 5 pasos (30–40 minutos)

| Paso | Tiempo | Qué haces |
|---|---|---|
| **1. Requisitos** | 5 min | Requisitos funcionales (qué hace) y no funcionales (cuántos usuarios, tiempo de respuesta, disponibilidad). **Pregunta**, no asumas. |
| **2. Entidades y tablas** | 8 min | Sustantivos → tablas. Relaciones (1:N, N:M), claves, restricciones (`UNIQUE`, `CHECK`, `FOREIGN KEY`). |
| **3. API** | 7 min | Endpoints REST: verbo + recurso + códigos de respuesta. |
| **4. Flujo y reglas** | 8 min | Recorre un caso de uso completo: validaciones, permisos, errores y concurrencia. |
| **5. Mejorar y escalar** | 5 min | Índices, caché, paginación, colas, réplicas, monitoreo. Solo lo que haga falta según el paso 1. |

Dibuja mientras hablas: cajas para cliente → API → base de datos, y tablas con sus columnas.

---

## 2. Ejemplo resuelto: sistema de reservas de laboratorios

*(Lo tienes implementado en `08-guia-desde-cero/` y en `04-simulacro/`.)*

**1. Requisitos.** Los docentes reservan un laboratorio por fecha y franja horaria; no puede haber choques; un laboratorio en mantenimiento no se reserva; hay un reporte de uso. Escala: ~50 laboratorios y ~500 docentes. Basta con un servidor y una base de datos relacional.

**2. Modelo de datos**

```sql
CREATE TABLE docentes (
  id      INTEGER PRIMARY KEY,
  nombre  TEXT NOT NULL,
  email   TEXT NOT NULL UNIQUE
);
CREATE TABLE laboratorios (
  id         INTEGER PRIMARY KEY,
  codigo     TEXT NOT NULL UNIQUE,
  nombre     TEXT NOT NULL,
  capacidad  INTEGER NOT NULL CHECK (capacidad > 0),
  estado     TEXT NOT NULL DEFAULT 'disponible' CHECK (estado IN ('disponible', 'mantenimiento'))
);
CREATE TABLE reservas (
  id              INTEGER PRIMARY KEY,
  laboratorio_id  INTEGER NOT NULL REFERENCES laboratorios(id),
  docente_id      INTEGER NOT NULL REFERENCES docentes(id),
  fecha           DATE NOT NULL,
  hora_inicio     TIME NOT NULL,
  hora_fin        TIME NOT NULL,
  CHECK (hora_fin > hora_inicio)
);
CREATE INDEX idx_reservas_lab_fecha ON reservas (laboratorio_id, fecha);   -- acelera la búsqueda de choques
```

**3. API**

| Método y ruta | Qué hace | Respuestas |
|---|---|---|
| `GET /api/laboratorios?estado=disponible` | Listar (con filtro) | 200 |
| `POST /api/laboratorios` | Crear | 201, 400 (validación), 409 (código repetido) |
| `PUT /api/laboratorios/{id}` | Actualizar | 200, 404 |
| `DELETE /api/laboratorios/{id}` | Eliminar | 204, 404, 409 (tiene reservas) |
| `GET /api/reservas?fecha=2026-09-25&lab=3` | Listar las reservas de un día | 200 |
| `POST /api/reservas` | Reservar | 201, 400, **409 (choque de horario)** |
| `GET /api/reportes/uso?desde=…&hasta=…` | Horas reservadas por laboratorio | 200 |

**4. Regla clave y concurrencia.** Dos reservas chocan si `inicio1 < fin2 AND inicio2 < fin1`, en el mismo laboratorio y la misma fecha. ¿Qué pasa si dos docentes reservan la misma franja **al mismo tiempo**? Ambos consultan, ninguno ve choque y los dos insertan. Soluciones: hacer la verificación y el insert en **una transacción** con bloqueo (`SELECT … FOR UPDATE` en MySQL o PostgreSQL; `BEGIN IMMEDIATE` en SQLite), o una restricción en la base de datos (en PostgreSQL, `EXCLUDE USING gist` sobre rangos de tiempo). Mencionar este caso es lo que más diferencia una buena respuesta.

**5. Mejoras.** Autenticación y roles (el docente reserva, el administrador gestiona laboratorios), notificaciones por correo en segundo plano, auditoría (quién creó o canceló), paginación en los listados y respaldos de la base de datos.

---

## 3. Otros ejercicios para practicar (con puntos clave)

### Acortador de URLs (tipo bit.ly)
- Tabla `enlaces(id, codigo UNIQUE, url_original, creado_en, clics)`.
- Código corto: el `id` convertido a **base62** (`0-9a-zA-Z`); 7 caracteres dan 62⁷ ≈ 3,5 billones de códigos.
- `POST /api/enlaces` → `{codigo}`; `GET /{codigo}` → redirección **301** (permanente; el navegador la guarda en caché) o **302** (temporal; permite contar cada clic).
- Hay muchas más lecturas que escrituras, así que conviene una **caché** (Redis) de código → URL. Los clics pueden contarse de forma asíncrona.
- Seguridad: validar la URL, limitar la frecuencia de creación (*rate limiting*) y bloquear dominios maliciosos.

### Sistema de notas y matrículas
- Tablas: `estudiantes`, `materias`, `periodos`, `matriculas(estudiante_id, materia_id, periodo_id, UNIQUE(…))` (la relación N:M) y `calificaciones(matricula_id, parcial, nota CHECK (nota BETWEEN 0 AND 10))`.
- Reglas: cupo máximo por materia, prerrequisitos (¡es el problema 23 de `algoritmos/`!) y periodo abierto o cerrado.
- Permisos: el estudiante ve solo sus notas, el docente edita las de sus materias y secretaría gestiona las matrículas.
- Primer día de matrículas, cuando todos entran a la vez: colas, caché del catálogo de materias, índices y pruebas de carga.

### Envío de notificaciones (correo o WhatsApp)
- No envíes el correo dentro de la petición HTTP, porque es lento y puede fallar. Guarda un **trabajo en una cola** (Redis/RQ, Celery, BullMQ o RabbitMQ) y que un *worker* lo procese.
- Reintentos con espera creciente (*exponential backoff*) y una cola de "fallidos" para revisar a mano.
- **Idempotencia**: si el worker reintenta, no debe enviar el mismo correo dos veces. Guarda el estado (`pendiente`, `enviado`, `fallido`).

### API de inventario para varias sucursales
- `productos`, `sucursales` y `stock(producto_id, sucursal_id, cantidad CHECK (cantidad >= 0))`.
- Venta concurrente del último producto: `UPDATE stock SET cantidad = cantidad - 1 WHERE … AND cantidad >= 1` y revisar las filas afectadas (operación atómica).
- Historial de movimientos en lugar de solo un número: `movimientos(tipo, cantidad, fecha, usuario)`.

---

## 4. Conceptos que debes poder explicar en 30 segundos

| Concepto | Explicación corta |
|---|---|
| **REST** | Recursos con URL (`/reservas/5`), verbos HTTP (GET leer, POST crear, PUT/PATCH actualizar, DELETE borrar), sin estado entre peticiones y respuestas en JSON. |
| **Códigos HTTP** | 200 OK, 201 creado, 204 sin contenido, 400 datos inválidos, 401 sin autenticar, 403 sin permiso, 404 no existe, 409 conflicto, 422 validación, 500 error del servidor. |
| **Normalización** | No repetir datos: cada hecho en un solo lugar (1FN valores atómicos; 2FN y 3FN sin dependencias parciales ni transitivas). A veces se desnormaliza a propósito para leer más rápido. |
| **Índice** | Estructura (normalmente un árbol B) que acelera las búsquedas por una columna a cambio de más espacio y escrituras más lentas. Se ponen en columnas de `WHERE`, `JOIN` y `ORDER BY`. |
| **Transacción y ACID** | Atomicidad (todo o nada), Consistencia (respeta las reglas), Aislamiento (las transacciones no se pisan), Durabilidad (lo confirmado no se pierde). |
| **Sesión vs JWT** | Sesión: el servidor guarda el estado y el cliente solo un ID en una cookie; es fácil de revocar. JWT: un token firmado con los datos dentro; no necesita estado, pero es difícil de revocar antes de que expire. |
| **Hash de contraseñas** | bcrypt o argon2: lentos y con sal. Nunca MD5, SHA-1 ni texto plano. |
| **Caché** | Guardar resultados costosos más cerca (memoria o Redis). Lo difícil es **invalidarla** cuando cambian los datos. Estrategias: TTL, o borrar la entrada al escribir. |
| **Escalado vertical vs horizontal** | Vertical: un servidor más grande (simple, pero con techo). Horizontal: más servidores detrás de un **balanceador de carga**; exige que la app no guarde estado en memoria. |
| **Réplicas de lectura** | Copias de la base de datos que solo atienden lecturas. Alivian al servidor principal; puede haber un pequeño retraso en los datos. |
| **Cola de mensajes** | Desacopla el trabajo lento o que puede fallar (correos, reportes, pagos) del flujo de la petición. |
| **CDN** | Sirve archivos estáticos (imágenes, JS, CSS) desde servidores cercanos al usuario. |
| **Logs y monitoreo** | Logs estructurados, métricas (latencia, errores) y alertas. "Si no lo mides, no sabes si está caído". |
| **Rate limiting** | Limitar las peticiones por usuario o IP (por ejemplo, 100 por minuto). Protege contra abuso y ataques de fuerza bruta. |

---

## 5. OWASP Top 10 en una tabla (seguridad que todo dev debe conocer)

| Riesgo | Ejemplo | Prevención |
|---|---|---|
| Control de acceso roto | `GET /api/notas/15` devuelve las notas de otro estudiante | Verificar en **cada** endpoint que el recurso pertenece al usuario |
| Fallas criptográficas | Contraseñas en MD5, sitio sin HTTPS | bcrypt o argon2, TLS en todo el sitio |
| Inyección | SQL armado con texto del usuario | Consultas parametrizadas o un ORM |
| Diseño inseguro | Recuperar la contraseña con "pregunta secreta" | Modelado de amenazas desde el diseño |
| Configuración incorrecta | `debug=True` en producción, contraseñas por defecto | Configuración por entorno, *hardening* |
| Componentes vulnerables | Dependencias viejas con fallas conocidas | `npm audit`, `pip-audit`, Dependabot |
| Fallas de autenticación | Login sin límite de intentos | Rate limiting, MFA, sesiones que expiran |
| Fallas de integridad | Instalar paquetes sin verificar su origen | Lockfiles, firmas, CI confiable |
| Falta de logs y monitoreo | Nadie se entera de un ataque | Registrar los eventos de seguridad y configurar alertas |
| SSRF | El servidor descarga la URL que le pasa el usuario (incluidas las internas) | Lista de dominios permitidos y bloquear IPs internas |

---

## 6. Preguntas para practicar en voz alta

1. ¿Cómo diseñarías la base de datos de una biblioteca, con préstamos, multas y reservas de libros?
2. Tu API tarda 3 segundos en responder. ¿Cómo encuentras la causa?
3. ¿Cómo evitas que dos personas compren el último asiento de un bus?
4. ¿Qué cambiarías en tu proyecto si mañana tuviera 100 veces más usuarios?
5. ¿Cómo diseñarías la paginación de un listado de 1 millón de registros? (`LIMIT/OFFSET` o paginación por cursor: `WHERE id > último_id`)
6. ¿Dónde guardarías los archivos que suben los usuarios? (No en la base de datos: en almacenamiento de objetos como S3 o Azure Blob, y en la base solo la ruta)
7. ¿Cómo desplegarías tu proyecto Flask o Express? (Variables de entorno, servidor WSGI o PM2, proxy inverso, HTTPS, logs y CI/CD; ver `01-cheatsheets/12-dart-flutter-wordpress-cloud.md`)
