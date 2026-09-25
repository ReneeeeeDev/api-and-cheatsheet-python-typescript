# Guía 2 — Construir desde cero con Node.js + Express

**App:** Sistema de reserva de laboratorios (el simulacro).
**Stack:** Express (servidor), EJS (vistas HTML en el servidor), SQLite con `better-sqlite3` (BD en un archivo, sin instalar un servidor de BD).
**Tiempo objetivo:** 2 h 15 min. Cada paso termina con **✅ Verifica** y **💾 Commit**.

> La carpeta `solucionario/reservas-express` tiene el proyecto terminado. Todo el código de esta guía sale de ahí, así que si algo no te funciona, compara tu archivo con el del solucionario.

## Mapa de pasos

| Paso | Qué haces | Min | Acumulado |
|---|---|---|---|
| 0 | Verificar herramientas | 3 | 0:03 |
| 1 | Leer y diseñar (tablas y rutas) | 10 | 0:13 |
| 2 | Crear el proyecto y las carpetas | 10 | 0:23 |
| 3 | Base de datos | 10 | 0:33 |
| 4 | Reglas de negocio (validaciones) | 15 | 0:48 |
| 5 | App base + vistas EJS + CSS | 15 | 1:03 |
| 6 | CRUD de laboratorios | 25 | 1:28 |
| 7 | Reservas + filtros | 25 | 1:53 |
| 8 | Reporte | 7 | 2:00 |
| 9 | API JSON | 7 | 2:07 |
| 10 | Pruebas automáticas | 8 | 2:15 |
| 11 | README + GitHub | 10 | 2:25 |

---

## Paso 0 — Verificar herramientas (3 min)

```bash
node -v        # 18 o mayor (ideal 20 o 22)
npm -v
git --version
```

---

## Paso 1 — Leer y diseñar (10 min)

**Tablas:**
```
laboratorios                         reservas
------------                         --------
id (PK)                              id (PK)
codigo (único)       1 ───────── N   laboratorio_id (FK → laboratorios.id)
nombre                               docente
piso                                 fecha        (AAAA-MM-DD)
capacidad (> 0)                      hora_inicio  (HH:MM)
estado (disponible|mantenimiento)    hora_fin     (HH:MM)
                                     motivo
```

**Rutas:**

| Método | URL | Archivo | Qué hace |
|---|---|---|---|
| GET | `/` | app.js | Panel con totales |
| GET | `/laboratorios` (`?editar=ID`) | routes/laboratorios.js | Listado + formulario |
| POST | `/laboratorios` | routes/laboratorios.js | Crear |
| POST | `/laboratorios/:id` | routes/laboratorios.js | Actualizar |
| POST | `/laboratorios/:id/eliminar` | routes/laboratorios.js | Eliminar |
| GET | `/reservas` (`?fecha=&lab=`) | routes/reservas.js | Listado filtrado + formulario |
| POST | `/reservas` | routes/reservas.js | Crear reserva |
| POST | `/reservas/:id/eliminar` | routes/reservas.js | Cancelar |
| GET | `/reporte` | routes/reporte.js | Reservas y horas por laboratorio |
| GET/POST | `/api/laboratorios` | routes/api.js | API JSON |
| GET | `/api/reservas` | routes/api.js | API JSON |

**Regla clave:** dos reservas del mismo laboratorio y el mismo día chocan si `inicio_nueva < fin_existente` **y** `inicio_existente < fin_nueva`.

---

## Paso 2 — Crear el proyecto y las carpetas (10 min)

### 2.1 Inicializar e instalar

```bash
cd Desktop
mkdir reservas-express
cd reservas-express
npm init -y
npm install express ejs better-sqlite3
```

- **express**: el servidor web.
- **ejs**: plantillas HTML con `<%= %>` para insertar datos.
- **better-sqlite3**: SQLite con una API **síncrona** (sin `async/await`), así el código queda más corto y claro.

> **Si `better-sqlite3` falla al instalar** (error de compilación o `node-gyp`) y tienes Node 22.5 o mayor, usa el SQLite que ya trae Node. Mira el **Plan B** al final de la guía.

### 2.2 Editar `package.json`

Reemplaza su contenido por este (las versiones pueden variar; deja las que instaló npm):

```json
{
  "name": "reservas-express",
  "version": "1.0.0",
  "description": "Sistema de reserva de laboratorios con Express, EJS y SQLite",
  "type": "module",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "node --watch src/server.js",
    "test": "node --test"
  },
  "dependencies": {
    "better-sqlite3": "^13.0.3",
    "ejs": "^6.0.1",
    "express": "^5.2.1"
  }
}
```

- `"type": "module"` permite usar `import`/`export` en lugar de `require`.
- `npm run dev` usa `node --watch`, que reinicia el servidor al guardar (no hace falta instalar nodemon).
- `npm test` ejecuta las pruebas con el runner que trae Node.

### 2.3 Estructura de carpetas

```bash
mkdir src
mkdir src\db              # Linux/Mac: mkdir -p src/db src/routes views/partials public/css test
mkdir src\routes
mkdir views
mkdir views\partials
mkdir public
mkdir public\css
mkdir test
```

Estructura final:

```
reservas-express/
├── node_modules/            ← dependencias (NO se sube a Git)
├── package.json             ← nombre, scripts y dependencias
├── README.md
├── .gitignore
├── src/                     ← código del servidor
│   ├── server.js            ← punto de entrada: crea la BD y arranca el servidor
│   ├── app.js               ← configura Express: vistas, middlewares, rutas
│   ├── validaciones.js      ← reglas de negocio
│   ├── db/
│   │   ├── conexion.js      ← conexión y datos iniciales
│   │   └── schema.sql       ← tablas
│   └── routes/              ← un archivo por módulo (controladores)
│       ├── laboratorios.js
│       ├── reservas.js
│       ├── reporte.js
│       └── api.js
├── views/                   ← plantillas EJS (HTML generado en el servidor)
│   ├── partials/
│   │   ├── cabecera.ejs     ← <head>, menú y mensajes
│   │   └── pie.ejs
│   ├── inicio.ejs
│   ├── laboratorios.ejs
│   ├── reservas.ejs
│   └── reporte.ejs
├── public/                  ← archivos estáticos (se sirven tal cual)
│   └── css/styles.css
└── test/
    └── app.test.js
```

**¿Por qué `server.js` y `app.js` separados?** `app.js` solo **construye** la aplicación y recibe la BD por parámetro, y `server.js` la **arranca**. Así, en las pruebas creamos la app con una BD en memoria sin tocar la real. Eso se llama **inyección de dependencias**, y es un buen punto para mencionarlo al evaluador.

**¿Por qué un archivo por módulo en `routes/`?** Cada archivo exporta una función que recibe `db` y devuelve un `Router`. En `app.js` se monta con un prefijo, `app.use("/laboratorios", ...)`, así que dentro del router las rutas son relativas (`"/"`, `"/:id"`).

### 2.4 Git

`.gitignore`:

```text
node_modules/
*.db
.vscode/
```

```bash
git init
git config user.name "Tu Nombre"
git config user.email "tu@correo.com"
git add .
git commit -m "chore: estructura inicial del proyecto Express"
```

✅ **Verifica:** `git status` no muestra `node_modules`.

---

## Paso 3 — Base de datos (10 min)

### 3.1 `src/db/schema.sql`

```sql
-- Esquema de la base de datos (SQLite).
-- "IF NOT EXISTS" permite ejecutarlo cada vez que arranca la app sin borrar datos.

CREATE TABLE IF NOT EXISTS laboratorios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT    NOT NULL UNIQUE,
    nombre      TEXT    NOT NULL,
    piso        INTEGER NOT NULL CHECK (piso >= 0),
    capacidad   INTEGER NOT NULL CHECK (capacidad > 0),
    estado      TEXT    NOT NULL DEFAULT 'disponible'
                CHECK (estado IN ('disponible', 'mantenimiento'))
);

CREATE TABLE IF NOT EXISTS reservas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratorio_id  INTEGER NOT NULL REFERENCES laboratorios(id),
    docente         TEXT    NOT NULL,
    fecha           TEXT    NOT NULL,          -- formato AAAA-MM-DD
    hora_inicio     TEXT    NOT NULL,          -- formato HH:MM
    hora_fin        TEXT    NOT NULL,
    motivo          TEXT,
    CHECK (hora_fin > hora_inicio)
);
```

### 3.2 `src/db/conexion.js`

```js
// Conexión a SQLite con better-sqlite3 (API síncrona: fácil de leer, sin async/await).
import Database from "better-sqlite3";
import { readFileSync } from "fs";

export function crearDb(ruta = "reservas.db") {
  const db = new Database(ruta);
  db.pragma("foreign_keys = ON");                 // SQLite no activa las FK por defecto

  // Ejecuta el esquema (ruta relativa a ESTE archivo, funciona en Windows y Linux)
  const esquema = readFileSync(new URL("./schema.sql", import.meta.url), "utf-8");
  db.exec(esquema);

  // Datos de ejemplo si la tabla está vacía
  const { total } = db.prepare("SELECT COUNT(*) AS total FROM laboratorios").get();
  if (total === 0) {
    const insertar = db.prepare(
      "INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)"
    );
    insertar.run("LAB-001", "Laboratorio de Redes", 1, 25, "disponible");
    insertar.run("LAB-002", "Laboratorio de Software", 2, 30, "disponible");
    insertar.run("LAB-003", "Laboratorio Multimedia", 2, 20, "mantenimiento");
  }
  return db;
}
```

**API de better-sqlite3, en resumen:**
```js
db.prepare(sql).get(...params)   // una fila (objeto) o undefined
db.prepare(sql).all(...params)   // arreglo de filas
db.prepare(sql).run(...params)   // INSERT/UPDATE/DELETE → { changes, lastInsertRowid }
db.exec(sql)                     // ejecutar varias sentencias sin parámetros
```
Siempre con `?` y los valores aparte, **nunca** concatenando texto del usuario (SQL Injection).

`new URL("./schema.sql", import.meta.url)` construye la ruta relativa **a este archivo**, así funciona sin importar desde qué carpeta ejecutes `node`.

✅ **Verifica:**
```bash
node -e "import('./src/db/conexion.js').then(m => console.log(m.crearDb(':memory:').prepare('SELECT codigo, estado FROM laboratorios').all()))"
```
Debe mostrar los 3 laboratorios. `:memory:` crea una BD temporal en memoria que no deja archivo.

💾 `git add . ; git commit -m "feat: esquema de base de datos y conexión"`

---

## Paso 4 — Reglas de negocio (15 min)

### `src/validaciones.js`

```js
// Reglas de negocio. Cada función recibe la conexión (db) y los datos del formulario
// y devuelve un arreglo de mensajes de error (arreglo vacío = todo correcto).

export const ESTADOS = ["disponible", "mantenimiento"];
const PATRON_HORA = /^([01]\d|2[0-3]):[0-5]\d$/;     // 00:00 a 23:59
const PATRON_FECHA = /^\d{4}-\d{2}-\d{2}$/;          // 2026-09-25

// Dos horarios [ini, fin) se cruzan si uno empieza antes de que termine el otro.
// Las horas "HH:MM" se pueden comparar como texto.
export const seCruzan = (ini1, fin1, ini2, fin2) => ini1 < fin2 && ini2 < fin1;

const esEntero = (valor, minimo) => /^\d+$/.test(String(valor ?? "").trim()) && Number(valor) >= minimo;

export function validarLaboratorio(db, datos, idActual = 0) {
  const errores = [];
  const codigo = String(datos.codigo ?? "").trim().toUpperCase();
  const nombre = String(datos.nombre ?? "").trim();

  if (!codigo) {
    errores.push("El código es obligatorio.");
  } else if (db.prepare("SELECT 1 FROM laboratorios WHERE codigo = ? AND id <> ?").get(codigo, idActual)) {
    errores.push(`Ya existe un laboratorio con el código ${codigo}.`);
  }
  if (nombre.length < 3) errores.push("El nombre debe tener al menos 3 caracteres.");
  if (!esEntero(datos.piso, 0)) errores.push("El piso debe ser un número entero (0 o mayor).");
  if (!esEntero(datos.capacidad, 1)) errores.push("La capacidad debe ser un número entero mayor a 0.");
  if (!ESTADOS.includes(datos.estado ?? "disponible"))
    errores.push("El estado debe ser 'disponible' o 'mantenimiento'.");
  return errores;
}

// Devuelve la reserva que se cruza con el horario pedido, o undefined.
export function buscarChoque(db, laboratorioId, fecha, horaInicio, horaFin) {
  return db.prepare(
    `SELECT * FROM reservas
     WHERE laboratorio_id = ? AND fecha = ?
       AND hora_inicio < ? AND ? < hora_fin`
  ).get(laboratorioId, fecha, horaFin, horaInicio);
}

export function validarReserva(db, datos) {
  const errores = [];
  const docente = String(datos.docente ?? "").trim();
  const fecha = String(datos.fecha ?? "");
  const inicio = String(datos.hora_inicio ?? "");
  const fin = String(datos.hora_fin ?? "");
  const lab = db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(Number(datos.laboratorio_id) || 0);

  if (docente.length < 3) errores.push("El nombre del docente es obligatorio (mínimo 3 caracteres).");
  if (!lab) errores.push("Seleccione un laboratorio válido.");
  else if (lab.estado === "mantenimiento")
    errores.push(`${lab.nombre} está en mantenimiento y no se puede reservar.`);
  if (!PATRON_FECHA.test(fecha)) errores.push("La fecha es obligatoria.");
  if (!PATRON_HORA.test(inicio) || !PATRON_HORA.test(fin))
    errores.push("Las horas de inicio y fin son obligatorias (HH:MM).");
  else if (fin <= inicio) errores.push("La hora de fin debe ser mayor que la hora de inicio.");

  // Solo buscamos choques si lo anterior está bien
  if (errores.length === 0) {
    const choque = buscarChoque(db, lab.id, fecha, inicio, fin);
    if (choque)
      errores.push(`Horario ocupado: ${choque.hora_inicio}-${choque.hora_fin} reservado por ${choque.docente}.`);
  }
  return errores;
}
```

**Por qué funciona la consulta de choque:**

| Existente | Nueva | ¿Choca? | Por qué |
|---|---|---|---|
| 08:00–10:00 | 09:00–11:00 | Sí | 08:00 < 11:00 y 09:00 < 10:00 |
| 08:00–12:00 | 09:00–10:00 | Sí | la nueva queda dentro |
| 08:00–10:00 | 10:00–12:00 | No | 10:00 < 10:00 es falso (contiguas) |
| 08:00–10:00 | 07:00–08:00 | No | 08:00 < 08:00 es falso |

✅ **Verifica:**
```bash
node -e "import('./src/validaciones.js').then(m => console.log(m.seCruzan('08:00','10:00','09:00','11:00'), m.seCruzan('08:00','10:00','10:00','12:00')))"
```
Debe imprimir `true false`.

💾 `git add . ; git commit -m "feat: validaciones y regla de choque de horarios"`

---

## Paso 5 — App base, vistas y estilos (15 min)

### 5.1 `src/app.js` (versión inicial, sin rutas de módulos todavía)

```js
import express from "express";
import { fileURLToPath } from "url";
// (aquí se agregan las rutas de los pasos 6 a 9)

// Recibe la BD por parámetro: así las pruebas pueden usar una BD en memoria.
export function crearApp(db) {
  const app = express();

  // Configuración de vistas EJS (carpeta /views en la raíz del proyecto)
  app.set("view engine", "ejs");
  app.set("views", fileURLToPath(new URL("../views", import.meta.url)));

  // Middlewares
  app.use(express.urlencoded({ extended: false }));   // lee formularios HTML (req.body)
  app.use(express.json());                            // lee JSON (para la API)
  app.use(express.static(fileURLToPath(new URL("../public", import.meta.url))));

  // Mensajes después de redirigir: /laboratorios?ok=Guardado  o  ?error=...
  app.use((req, res, next) => {
    res.locals.ok = req.query.ok || "";
    res.locals.error = req.query.error || "";
    res.locals.errores = [];
    next();
  });

  app.get("/", (req, res) => {
    const contar = (sql) => db.prepare(sql).get().total;
    res.render("inicio", {
      totales: {
        laboratorios: contar("SELECT COUNT(*) AS total FROM laboratorios"),
        disponibles: contar("SELECT COUNT(*) AS total FROM laboratorios WHERE estado = 'disponible'"),
        reservas: contar("SELECT COUNT(*) AS total FROM reservas"),
      },
    });
  });

  // (aquí se agregan las rutas de los pasos 6 a 9)

  // 404 y errores (siempre al final)
  app.use((req, res) => res.status(404).send("Página no encontrada"));
  app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send("Error interno del servidor");
  });

  return app;
}
```

**Orden de los middlewares (importa mucho):**
1. `express.urlencoded` y `express.json` leen el cuerpo de la petición y lo dejan en `req.body`. Sin ellos, `req.body` es `undefined`.
2. `express.static` sirve `public/`, así que `/css/styles.css` corresponde a `public/css/styles.css`.
3. El middleware propio copia `?ok=` y `?error=` de la URL a `res.locals`, y todo lo que está en `res.locals` está disponible en **todas** las vistas.
4. Las rutas.
5. **Al final** van el 404 y el manejador de errores (el que tiene 4 parámetros).

### 5.2 `src/server.js`

```js
// Punto de entrada: crea la BD, crea la app y levanta el servidor.
import { crearDb } from "./db/conexion.js";
import { crearApp } from "./app.js";

const PUERTO = process.env.PORT || 3000;
const db = crearDb("reservas.db");
const app = crearApp(db);

app.listen(PUERTO, () => {
  console.log(`Servidor listo en http://localhost:${PUERTO}`);
});
```

### 5.3 `views/partials/cabecera.ejs`

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><%= titulo %> | Laboratorios ISTE</title>
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <header class="barra">
    <a class="logo" href="/">Reservas de Laboratorios</a>
    <nav>
      <a href="/laboratorios">Laboratorios</a>
      <a href="/reservas">Reservas</a>
      <a href="/reporte">Reporte</a>
    </nav>
  </header>

  <main class="contenedor">
    <%# Mensajes que llegan por la URL después de redirigir (?ok=... / ?error=...) %>
    <% if (ok) { %><div class="alerta ok"><%= ok %></div><% } %>
    <% if (error) { %><div class="alerta error"><%= error %></div><% } %>

    <%# Errores de validación al volver a mostrar un formulario %>
    <% if (errores.length) { %>
      <div class="alerta error">
        <strong>Revise los datos:</strong>
        <ul><% errores.forEach(e => { %><li><%= e %></li><% }) %></ul>
      </div>
    <% } %>
```

### 5.4 `views/partials/pie.ejs`

```html
  </main>
</body>
</html>
```

### 5.5 `views/inicio.ejs`

```html
<%- include("partials/cabecera", { titulo: "Inicio" }) %>

<h1>Panel principal</h1>
<div class="tarjetas">
  <div class="tarjeta"><span>Laboratorios</span><strong><%= totales.laboratorios %></strong></div>
  <div class="tarjeta"><span>Disponibles</span><strong><%= totales.disponibles %></strong></div>
  <div class="tarjeta"><span>Reservas</span><strong><%= totales.reservas %></strong></div>
</div>
<p class="acciones">
  <a class="btn" href="/reservas">Nueva reserva</a>
  <a class="btn sec" href="/laboratorios">Gestionar laboratorios</a>
</p>

<%- include("partials/pie") %>
```

**EJS en 4 líneas:**
- `<%= valor %>` imprime **escapando HTML**, lo que evita XSS. Úsalo siempre para datos.
- `<%- include(...) %>` imprime **sin escapar**. Úsalo solo para incluir otras plantillas.
- `<% código JS %>` ejecuta código sin imprimir (if, forEach).
- `<%# comentario %>`.

### 5.6 `public/css/styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }

:root {
  --primario: #0a5bd6;
  --peligro: #dc2626;
  --gris: #64748b;
  --borde: #e5e7eb;
  --fondo: #f1f5f9;
}

body { margin: 0; font-family: system-ui, sans-serif; background: var(--fondo); color: #1f2937; }

/* Barra superior */
.barra { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;
         gap: 12px; padding: 12px 24px; background: var(--primario); }
.barra a { color: #fff; text-decoration: none; }
.barra nav { display: flex; gap: 16px; }
.logo { font-weight: 700; }

.contenedor { max-width: 1000px; margin: 24px auto; padding: 0 16px; display: grid; gap: 16px; }
.panel { background: #fff; border-radius: 10px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.panel h2 { margin-top: 0; font-size: 18px; }

/* Formularios */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
label { display: grid; gap: 4px; font-size: 14px; }
input, select { width: 100%; padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; }
.filtros { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; margin-bottom: 12px; }
.filtros label { min-width: 160px; }

/* Botones */
button, .btn { display: inline-block; padding: 8px 14px; border: 0; border-radius: 6px; cursor: pointer;
               background: var(--primario); color: #fff; text-decoration: none; font-size: 14px; }
.btn.sec { background: var(--gris); }
.peligro { background: var(--peligro); }
.acciones { display: flex; gap: 8px; align-items: center; margin-top: 12px; }
td.acciones { margin: 0; }
.acciones form { margin: 0; }

/* Tablas */
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; border-bottom: 1px solid var(--borde); text-align: left; }
thead { background: #f8fafc; }
.estado { padding: 2px 8px; border-radius: 999px; font-size: 12px; }
.estado.disponible { background: #dcfce7; color: #166534; }
.estado.mantenimiento { background: #fee2e2; color: #991b1b; }

/* Mensajes */
.alerta { padding: 10px 14px; border-radius: 8px; }
.alerta ul { margin: 6px 0 0; }
.alerta.ok { background: #dcfce7; color: #166534; }
.alerta.error { background: #fee2e2; color: #991b1b; }

/* Tarjetas del inicio */
.tarjetas { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.tarjeta { background: #fff; border-radius: 10px; padding: 16px; display: grid; gap: 4px; }
.tarjeta span { color: var(--gris); font-size: 13px; }
.tarjeta strong { font-size: 28px; }

/* Celular: la tabla se desplaza horizontalmente */
@media (max-width: 700px) {
  .panel { overflow-x: auto; }
}
```

### ▶ Ejecutar

```bash
npm run dev
```
Abre **http://localhost:3000**.

✅ **Verifica:** ves el panel con **3 laboratorios, 2 disponibles, 0 reservas**, y se creó `reservas.db`. El menú todavía da "Página no encontrada".

💾 `git add . ; git commit -m "feat: app base con vistas EJS y estilos"`

---

## Paso 6 — CRUD de laboratorios (25 min)

### 6.1 `src/routes/laboratorios.js`

```js
// Rutas del CRUD de laboratorios. Montadas en /laboratorios (ver app.js).
import { Router } from "express";
import { validarLaboratorio } from "../validaciones.js";

// Limpia y convierte los datos del formulario al orden de las columnas.
export const datosLaboratorio = (b) => [
  String(b.codigo).trim().toUpperCase(),
  String(b.nombre).trim(),
  Number(b.piso),
  Number(b.capacidad),
  b.estado || "disponible",
];

export default function laboratoriosRouter(db) {
  const router = Router();

  const mostrar = (res, form = {}, errores = [], status = 200) => {
    const labs = db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all();
    res.status(status).render("laboratorios", { labs, form, errores });
  };

  // GET /laboratorios            → listado + formulario vacío
  // GET /laboratorios?editar=2   → listado + formulario con el laboratorio 2
  router.get("/", (req, res) => {
    const editarId = Number(req.query.editar);
    if (editarId) {
      const lab = db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(editarId);
      if (!lab) return res.redirect("/laboratorios?error=" + encodeURIComponent("Laboratorio no encontrado."));
      return mostrar(res, lab);
    }
    mostrar(res);
  });

  // POST /laboratorios → crear
  router.post("/", (req, res) => {
    const errores = validarLaboratorio(db, req.body);
    if (errores.length) return mostrar(res, req.body, errores, 400);
    db.prepare("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)")
      .run(...datosLaboratorio(req.body));
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio creado correctamente."));
  });

  // POST /laboratorios/:id → actualizar
  router.post("/:id", (req, res) => {
    const id = Number(req.params.id);
    const errores = validarLaboratorio(db, req.body, id);
    if (errores.length) return mostrar(res, { ...req.body, id }, errores, 400);
    db.prepare("UPDATE laboratorios SET codigo = ?, nombre = ?, piso = ?, capacidad = ?, estado = ? WHERE id = ?")
      .run(...datosLaboratorio(req.body), id);
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio actualizado."));
  });

  // POST /laboratorios/:id/eliminar → eliminar (si no tiene reservas)
  router.post("/:id/eliminar", (req, res) => {
    const id = Number(req.params.id);
    if (db.prepare("SELECT 1 FROM reservas WHERE laboratorio_id = ?").get(id)) {
      return res.redirect("/laboratorios?error=" +
        encodeURIComponent("No se puede eliminar: el laboratorio tiene reservas registradas."));
    }
    db.prepare("DELETE FROM laboratorios WHERE id = ?").run(id);
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio eliminado."));
  });

  return router;
}
```

### 6.2 Conectar la ruta en `src/app.js`

Arriba, junto a los otros `import`:
```js
import laboratoriosRouter from "./routes/laboratorios.js";
```
Dentro de `crearApp`, donde está el comentario de las rutas (**antes** del 404):
```js
app.use("/laboratorios", laboratoriosRouter(db));
```

**Flujo POST → Redirect → GET:**
```
Formulario ──POST /laboratorios──► router.post("/")
                                      │
                ┌── ¿hay errores? ────┤
                ▼ sí                  ▼ no
   res.status(400).render(...)     INSERT
   con los datos escritos          res.redirect("/laboratorios?ok=...")
   y la lista de errores           → el navegador hace GET; si refresca, NO duplica
```

- `req.body`: datos del formulario (siempre texto). `req.params.id`: el `:id` de la URL. `req.query.editar`: el `?editar=` de la URL.
- `encodeURIComponent` codifica espacios y tildes para poder ponerlos en la URL.
- `.run(...datosLaboratorio(req.body))`: el `...` (spread) pasa cada elemento del arreglo como un parámetro.

### 6.3 `views/laboratorios.ejs`

```html
<%- include("partials/cabecera", { titulo: "Laboratorios" }) %>

<section class="panel">
  <%# Si form.id existe estamos editando; si no, creando %>
  <h2><%= form.id ? `Editar laboratorio ${form.codigo}` : "Nuevo laboratorio" %></h2>
  <form method="post" action="<%= form.id ? `/laboratorios/${form.id}` : '/laboratorios' %>">
    <div class="grid">
      <label>Código
        <input name="codigo" value="<%= form.codigo ?? '' %>" placeholder="LAB-004" required>
      </label>
      <label>Nombre
        <input name="nombre" value="<%= form.nombre ?? '' %>" required minlength="3">
      </label>
      <label>Piso
        <input name="piso" type="number" min="0" value="<%= form.piso ?? '' %>" required>
      </label>
      <label>Capacidad
        <input name="capacidad" type="number" min="1" value="<%= form.capacidad ?? '' %>" required>
      </label>
      <label>Estado
        <select name="estado">
          <% ["disponible", "mantenimiento"].forEach(e => { %>
            <option value="<%= e %>" <%= form.estado === e ? "selected" : "" %>><%= e %></option>
          <% }) %>
        </select>
      </label>
    </div>
    <div class="acciones">
      <button type="submit">Guardar</button>
      <% if (form.id) { %><a class="btn sec" href="/laboratorios">Cancelar</a><% } %>
    </div>
  </form>
</section>

<section class="panel">
  <h2>Listado</h2>
  <table>
    <thead>
      <tr><th>Código</th><th>Nombre</th><th>Piso</th><th>Capacidad</th><th>Estado</th><th>Acciones</th></tr>
    </thead>
    <tbody>
      <% if (labs.length === 0) { %>
        <tr><td colspan="6">No hay laboratorios registrados.</td></tr>
      <% } %>
      <% labs.forEach(lab => { %>
        <tr>
          <td><%= lab.codigo %></td>
          <td><%= lab.nombre %></td>
          <td><%= lab.piso %></td>
          <td><%= lab.capacidad %></td>
          <td><span class="estado <%= lab.estado %>"><%= lab.estado %></span></td>
          <td class="acciones">
            <a class="btn sec" href="/laboratorios?editar=<%= lab.id %>">Editar</a>
            <form method="post" action="/laboratorios/<%= lab.id %>/eliminar"
                  onsubmit="return confirm('¿Eliminar <%= lab.codigo %>?')">
              <button class="peligro">Eliminar</button>
            </form>
          </td>
        </tr>
      <% }) %>
    </tbody>
  </table>
</section>

<%- include("partials/pie") %>
```

- `form.codigo ?? ''` usa un texto vacío si el valor es `undefined` o `null`, para que no aparezca "undefined" en el input.
- Eliminar se hace con un `<form method="post">`, nunca con un enlace GET.

✅ **Verifica** en http://localhost:3000/laboratorios:

| Prueba | Resultado esperado |
|---|---|
| Crear `lab-004`, "Lab Hardware", piso 1, capacidad 20 | Aparece como **LAB-004** con el mensaje verde |
| Crear con código `LAB-001` | Error "Ya existe..." y los datos se conservan |
| Editar y guardar | Se actualiza |
| Eliminar LAB-004 | Desaparece |

💾 `git add . ; git commit -m "feat: CRUD de laboratorios"`

---

## Paso 7 — Reservas y filtros (25 min)

### 7.1 `src/routes/reservas.js`

```js
// Rutas de reservas. Montadas en /reservas (ver app.js).
import { Router } from "express";
import { validarReserva } from "../validaciones.js";

export default function reservasRouter(db) {
  const router = Router();

  const mostrar = (req, res, form = {}, errores = [], status = 200) => {
    const filtro = { fecha: req.query.fecha || "", lab: req.query.lab || "" };

    let sql = `SELECT r.*, l.codigo, l.nombre AS laboratorio
               FROM reservas r
               JOIN laboratorios l ON l.id = r.laboratorio_id
               WHERE 1 = 1`;
    const params = [];
    if (filtro.fecha) { sql += " AND r.fecha = ?"; params.push(filtro.fecha); }
    if (filtro.lab) { sql += " AND r.laboratorio_id = ?"; params.push(Number(filtro.lab)); }
    sql += " ORDER BY r.fecha, r.hora_inicio";

    res.status(status).render("reservas", {
      reservas: db.prepare(sql).all(...params),
      labs: db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all(),
      form, errores, filtro,
    });
  };

  router.get("/", (req, res) => mostrar(req, res));

  router.post("/", (req, res) => {
    const b = req.body;
    const errores = validarReserva(db, b);
    if (errores.length) return mostrar(req, res, b, errores, 400);
    db.prepare(`INSERT INTO reservas (laboratorio_id, docente, fecha, hora_inicio, hora_fin, motivo)
                VALUES (?, ?, ?, ?, ?, ?)`)
      .run(Number(b.laboratorio_id), b.docente.trim(), b.fecha, b.hora_inicio, b.hora_fin, (b.motivo || "").trim());
    res.redirect("/reservas?ok=" + encodeURIComponent("Reserva registrada."));
  });

  router.post("/:id/eliminar", (req, res) => {
    db.prepare("DELETE FROM reservas WHERE id = ?").run(Number(req.params.id));
    res.redirect("/reservas?ok=" + encodeURIComponent("Reserva cancelada."));
  });

  return router;
}
```

- **JOIN** trae el nombre del laboratorio junto a cada reserva.
- **Filtros dinámicos**: `WHERE 1 = 1` permite añadir `AND ...` solo cuando el filtro tiene valor, y los valores van en `params`.

### 7.2 Conectar en `src/app.js`

```js
import reservasRouter from "./routes/reservas.js";
// ...
app.use("/reservas", reservasRouter(db));
```

### 7.3 `views/reservas.ejs`

```html
<%- include("partials/cabecera", { titulo: "Reservas" }) %>

<section class="panel">
  <h2>Nueva reserva</h2>
  <form method="post" action="/reservas">
    <div class="grid">
      <label>Docente
        <input name="docente" value="<%= form.docente ?? '' %>" required>
      </label>
      <label>Laboratorio
        <select name="laboratorio_id" required>
          <option value="">-- Seleccione --</option>
          <% labs.forEach(lab => { %>
            <option value="<%= lab.id %>"
                    <%= String(form.laboratorio_id) === String(lab.id) ? "selected" : "" %>
                    <%= lab.estado === "mantenimiento" ? "disabled" : "" %>>
              <%= lab.codigo %> - <%= lab.nombre %><%= lab.estado === "mantenimiento" ? " (mantenimiento)" : "" %>
            </option>
          <% }) %>
        </select>
      </label>
      <label>Fecha
        <input name="fecha" type="date" value="<%= form.fecha ?? '' %>" required>
      </label>
      <label>Hora inicio
        <input name="hora_inicio" type="time" value="<%= form.hora_inicio ?? '' %>" required>
      </label>
      <label>Hora fin
        <input name="hora_fin" type="time" value="<%= form.hora_fin ?? '' %>" required>
      </label>
      <label>Motivo
        <input name="motivo" value="<%= form.motivo ?? '' %>">
      </label>
    </div>
    <div class="acciones"><button type="submit">Reservar</button></div>
  </form>
</section>

<section class="panel">
  <h2>Reservas registradas</h2>
  <%# Filtros: formulario GET → los valores viajan en la URL (?fecha=...&lab=...) %>
  <form method="get" class="filtros">
    <label>Fecha <input name="fecha" type="date" value="<%= filtro.fecha %>"></label>
    <label>Laboratorio
      <select name="lab">
        <option value="">Todos</option>
        <% labs.forEach(lab => { %>
          <option value="<%= lab.id %>" <%= filtro.lab === String(lab.id) ? "selected" : "" %>><%= lab.codigo %></option>
        <% }) %>
      </select>
    </label>
    <button type="submit">Filtrar</button>
    <a class="btn sec" href="/reservas">Limpiar</a>
  </form>

  <table>
    <thead>
      <tr><th>Fecha</th><th>Horario</th><th>Laboratorio</th><th>Docente</th><th>Motivo</th><th></th></tr>
    </thead>
    <tbody>
      <% if (reservas.length === 0) { %>
        <tr><td colspan="6">No hay reservas.</td></tr>
      <% } %>
      <% reservas.forEach(r => { %>
        <tr>
          <td><%= r.fecha %></td>
          <td><%= r.hora_inicio %> - <%= r.hora_fin %></td>
          <td><%= r.codigo %> - <%= r.laboratorio %></td>
          <td><%= r.docente %></td>
          <td><%= r.motivo || "" %></td>
          <td>
            <form method="post" action="/reservas/<%= r.id %>/eliminar"
                  onsubmit="return confirm('¿Cancelar esta reserva?')">
              <button class="peligro">Cancelar</button>
            </form>
          </td>
        </tr>
      <% }) %>
    </tbody>
  </table>
</section>

<%- include("partials/pie") %>
```

- `String(form.laboratorio_id) === String(lab.id)`: el formulario envía `"2"` (texto) y la BD devuelve `2` (número). Con `===` no son iguales si no conviertes.
- `disabled` en mantenimiento es solo una ayuda visual. La regla real está en `validarReserva`.

✅ **Verifica** (mismo laboratorio y fecha):

| Reserva | Esperado |
|---|---|
| LAB-002, 08:00–10:00 | ✔ Registrada |
| LAB-002, 09:00–11:00 | ✘ "Horario ocupado..." |
| LAB-002, 10:00–12:00 | ✔ (contigua) |
| LAB-001, 08:00–10:00 | ✔ (otro laboratorio) |
| Fin antes que inicio | ✘ |
| Filtrar por fecha / laboratorio | Solo aparecen las que coinciden |
| Eliminar LAB-002 | ✘ "tiene reservas registradas" |

💾 `git add . ; git commit -m "feat: reservas con validación de choques y filtros"`

---

## Paso 8 — Reporte (7 min)

### 8.1 `src/routes/reporte.js`

```js
// Reporte de uso. Montado en /reporte (ver app.js).
import { Router } from "express";

const SQL_REPORTE = `
SELECT l.codigo, l.nombre,
       COUNT(r.id) AS total_reservas,
       ROUND(COALESCE(SUM(
           (strftime('%s', r.hora_fin) - strftime('%s', r.hora_inicio)) / 3600.0
       ), 0), 1) AS horas
FROM laboratorios l
LEFT JOIN reservas r ON r.laboratorio_id = l.id
GROUP BY l.id
ORDER BY horas DESC, l.codigo`;

export default function reporteRouter(db) {
  const router = Router();
  router.get("/", (req, res) => res.render("reporte", { filas: db.prepare(SQL_REPORTE).all() }));
  return router;
}
```

- **LEFT JOIN** incluye laboratorios sin reservas. `COALESCE(x, 0)` convierte NULL en 0.
- `strftime('%s', hora)` pasa la hora a segundos, y al dividir para 3600 obtienes horas.
- En MySQL: `SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fin, r.hora_inicio)) / 3600)`.

### 8.2 Conectar en `src/app.js`

```js
import reporteRouter from "./routes/reporte.js";
// ...
app.use("/reporte", reporteRouter(db));
```

### 8.3 `views/reporte.ejs`

```html
<%- include("partials/cabecera", { titulo: "Reporte" }) %>

<section class="panel">
  <h2>Uso de laboratorios</h2>
  <table>
    <thead><tr><th>Código</th><th>Laboratorio</th><th>Reservas</th><th>Horas reservadas</th></tr></thead>
    <tbody>
      <% filas.forEach(f => { %>
        <tr>
          <td><%= f.codigo %></td>
          <td><%= f.nombre %></td>
          <td><%= f.total_reservas %></td>
          <td><%= f.horas %></td>
        </tr>
      <% }) %>
    </tbody>
  </table>
</section>

<%- include("partials/pie") %>
```

✅ **Verifica:** una reserva de 08:00 a 10:00 muestra 1 reserva y 2 horas.

💾 `git add . ; git commit -m "feat: reporte de uso por laboratorio"`

---

## Paso 9 — API REST en JSON (7 min)

### 9.1 `src/routes/api.js`

```js
// API REST en JSON. Montada en /api (ver app.js).
import { Router } from "express";
import { validarLaboratorio } from "../validaciones.js";
import { datosLaboratorio } from "./laboratorios.js";

export default function apiRouter(db) {
  const router = Router();

  // GET /api/laboratorios
  router.get("/laboratorios", (req, res) => {
    res.json(db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all());
  });

  // POST /api/laboratorios   body: {"codigo":"LAB-010","nombre":"...","piso":1,"capacidad":20}
  router.post("/laboratorios", (req, res) => {
    const datos = { estado: "disponible", ...(req.body || {}) };
    const errores = validarLaboratorio(db, datos);
    if (errores.length) return res.status(400).json({ errores });
    const r = db.prepare("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)")
      .run(...datosLaboratorio(datos));
    res.status(201).json(db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(r.lastInsertRowid));
  });

  // GET /api/reservas?fecha=2026-09-25
  router.get("/reservas", (req, res) => {
    let sql = "SELECT r.*, l.codigo FROM reservas r JOIN laboratorios l ON l.id = r.laboratorio_id";
    const params = [];
    if (req.query.fecha) { sql += " WHERE r.fecha = ?"; params.push(req.query.fecha); }
    res.json(db.prepare(sql + " ORDER BY r.fecha, r.hora_inicio").all(...params));
  });

  return router;
}
```

### 9.2 Conectar en `src/app.js`

```js
import apiRouter from "./routes/api.js";
// ...
app.use("/api", apiRouter(db));
```

### 9.3 Así queda la parte de rutas de app.js (compara con la tuya)

Arriba del archivo:

```js
import laboratoriosRouter from "./routes/laboratorios.js";
import reservasRouter from "./routes/reservas.js";
import reporteRouter from "./routes/reporte.js";
import apiRouter from "./routes/api.js";
```

Dentro de `crearApp`, antes del 404:

```js
  app.use("/laboratorios", laboratoriosRouter(db));
  app.use("/reservas", reservasRouter(db));
  app.use("/reporte", reporteRouter(db));
  app.use("/api", apiRouter(db));
```

✅ **Verifica:**
- Navegador: http://localhost:3000/api/laboratorios
- PowerShell:
  ```powershell
  Invoke-RestMethod -Method Post -Uri http://localhost:3000/api/laboratorios -ContentType "application/json" -Body '{"codigo":"LAB-050","nombre":"Lab API","piso":1,"capacidad":12}'
  ```
- CMD / Git Bash:
  ```bash
  curl -X POST http://localhost:3000/api/laboratorios -H "Content-Type: application/json" -d "{\"codigo\":\"LAB-051\",\"nombre\":\"Lab API\",\"piso\":1,\"capacidad\":12}"
  ```
  Esperado: **201** con el laboratorio creado. Si envías `{}`, la respuesta es **400** con los errores.

💾 `git add . ; git commit -m "feat: API JSON de laboratorios y reservas"`

---

## Paso 10 — Pruebas automáticas (8 min)

### `test/app.test.js`

```js
// Pruebas con el runner nativo de Node. Ejecutar:  npm test
import { test, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import { crearDb } from "../src/db/conexion.js";
import { crearApp } from "../src/app.js";
import { seCruzan } from "../src/validaciones.js";

let servidor, base;

// Antes de cada prueba: BD nueva en memoria + servidor en un puerto libre
beforeEach(async () => {
  const app = crearApp(crearDb(":memory:"));
  await new Promise((listo) => (servidor = app.listen(0, listo)));
  base = `http://localhost:${servidor.address().port}`;
});
afterEach(() => servidor.close());

// Envía un formulario como lo haría el navegador (sin seguir la redirección)
const enviar = (ruta, datos) =>
  fetch(base + ruta, { method: "POST", body: new URLSearchParams(datos), redirect: "manual" });

const reservar = (inicio, fin, lab = 2, fecha = "2026-09-25") =>
  enviar("/reservas", { docente: "Ing. Ruiz", laboratorio_id: lab, fecha, hora_inicio: inicio, hora_fin: fin });

// ---- Unitarias
test("seCruzan detecta horarios que se superponen", () => {
  assert.equal(seCruzan("08:00", "10:00", "09:00", "11:00"), true);
  assert.equal(seCruzan("08:00", "12:00", "09:00", "10:00"), true);
});

test("seCruzan acepta horarios contiguos", () => {
  assert.equal(seCruzan("08:00", "10:00", "10:00", "12:00"), false);
});

// ---- Integración
test("todas las páginas cargan", async () => {
  for (const ruta of ["/", "/laboratorios", "/reservas", "/reporte", "/laboratorios?editar=1"]) {
    assert.equal((await fetch(base + ruta)).status, 200, ruta);
  }
});

test("crear laboratorio", async () => {
  const r = await enviar("/laboratorios", { codigo: "lab-010", nombre: "Lab IA", piso: 3, capacidad: 15, estado: "disponible" });
  assert.equal(r.status, 302);
  assert.match(await (await fetch(base + "/laboratorios")).text(), /LAB-010/);
});

test("laboratorio inválido o duplicado", async () => {
  const r = await enviar("/laboratorios", { codigo: "LAB-001", nombre: "X", piso: -1, capacidad: 0, estado: "otro" });
  assert.equal(r.status, 400);
  const html = await r.text();
  assert.match(html, /Ya existe/);
  assert.match(html, /capacidad/);
});

test("editar laboratorio", async () => {
  const r = await enviar("/laboratorios/1", { codigo: "LAB-001", nombre: "Redes Renovado", piso: 1, capacidad: 40, estado: "disponible" });
  assert.equal(r.status, 302);
  assert.match(await (await fetch(base + "/laboratorios")).text(), /Redes Renovado/);
});

test("reserva válida", async () => {
  assert.equal((await reservar("08:00", "10:00")).status, 302);
});

test("reserva que choca es rechazada", async () => {
  await reservar("08:00", "10:00");
  const r = await reservar("09:00", "11:00");
  assert.equal(r.status, 400);
  assert.match(await r.text(), /Horario ocupado/);
});

test("reservas contiguas y en otro día son aceptadas", async () => {
  await reservar("08:00", "10:00");
  assert.equal((await reservar("10:00", "12:00")).status, 302);
  assert.equal((await reservar("08:00", "10:00", 2, "2026-09-26")).status, 302);
});

test("hora fin menor que inicio", async () => {
  assert.equal((await reservar("10:00", "09:00")).status, 400);
});

test("laboratorio en mantenimiento", async () => {
  assert.equal((await reservar("08:00", "09:00", 3)).status, 400);
});

test("no elimina laboratorio con reservas", async () => {
  await reservar("08:00", "10:00");
  await enviar("/laboratorios/2/eliminar", {});
  assert.equal((await (await fetch(base + "/api/laboratorios")).json()).length, 3);
  await enviar("/laboratorios/1/eliminar", {});          // este no tiene reservas
  assert.equal((await (await fetch(base + "/api/laboratorios")).json()).length, 2);
});

test("filtro y reporte", async () => {
  await reservar("08:00", "10:30");
  await reservar("08:00", "09:00", 2, "2026-09-26");
  assert.equal((await (await fetch(base + "/api/reservas?fecha=2026-09-26")).json()).length, 1);
  assert.match(await (await fetch(base + "/reporte")).text(), /3\.5/);
});

test("API crear laboratorio", async () => {
  const r = await fetch(base + "/api/laboratorios", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ codigo: "LAB-020", nombre: "Lab Móvil", piso: 1, capacidad: 10 }),
  });
  assert.equal(r.status, 201);
  assert.equal((await r.json()).codigo, "LAB-020");
  const vacio = await fetch(base + "/api/laboratorios", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: "{}",
  });
  assert.equal(vacio.status, 400);
});
```

- `crearDb(":memory:")` da a cada prueba una BD nueva y vacía.
- `app.listen(0)` usa un puerto libre al azar, así que no choca con tu servidor en el 3000.
- `redirect: "manual"` permite comprobar que la respuesta es un **302** en lugar de seguir la redirección.
- `new URLSearchParams(datos)` envía los datos igual que un formulario HTML.

```bash
npm test
```

✅ **Verifica:** `# pass 14` y `# fail 0`.

💾 `git add . ; git commit -m "test: pruebas unitarias y de integración"`

---

## Paso 11 — README y GitHub (10 min)

### `README.md`

````markdown
# Sistema de Reserva de Laboratorios (Express)

Aplicación web para registrar laboratorios y gestionar sus reservas, evitando choques de horario.

## Funcionalidades
- CRUD de laboratorios (código único, piso, capacidad, estado).
- Reservas con validaciones: horario válido, laboratorio disponible y **sin cruces de horario**.
- Listado de reservas con filtros por fecha y laboratorio.
- Reporte de reservas y horas por laboratorio.
- API REST: `GET/POST /api/laboratorios`, `GET /api/reservas?fecha=AAAA-MM-DD`.

## Tecnologías
Node.js, Express, EJS, SQLite (better-sqlite3), HTML/CSS.

## Instalación y ejecución
```bash
npm install
npm run dev
```
Abrir http://localhost:3000. La base de datos `reservas.db` se crea automáticamente con 3 laboratorios de ejemplo.

## Pruebas
```bash
npm test
```

## Estructura
```
src/server.js          Punto de entrada
src/app.js             Configuración de Express
src/db/                Conexión y esquema SQL
src/validaciones.js    Reglas de negocio
src/routes/            Rutas (controladores) por módulo
views/                 Vistas EJS
public/css/            Estilos
test/                  Pruebas automáticas
```
````

```bash
git add . ; git commit -m "docs: README con instrucciones"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/reservas-express.git
git push -u origin main
```

---

## Paso 12 — Revisión final

- [ ] Borra `reservas.db`, ejecuta `npm run dev` y confirma que todo se crea solo.
- [ ] Recorre todas las pantallas y envía formularios vacíos: ningún error 500.
- [ ] Revisa los casos de choque de la tabla del Paso 7.
- [ ] README y último commit hechos.

## Errores comunes y solución

| Error | Causa | Solución |
|---|---|---|
| `Cannot use import statement outside a module` | Falta `"type": "module"` | Agrégalo en `package.json` |
| `ERR_MODULE_NOT_FOUND ... routes/laboratorios` | En ES Modules la extensión es obligatoria | Escribe `"./routes/laboratorios.js"` con `.js` |
| `req.body` es `undefined` | Falta `express.urlencoded` / `express.json`, o están **después** de las rutas | Ponlos antes de los `app.use` de rutas |
| `Failed to lookup view "laboratorios"` | La vista no está en `views/` o el nombre no coincide | Revisa `app.set("views", ...)` y el nombre del archivo |
| `x is not defined` dentro de un .ejs | No pasaste esa variable en `res.render(...)` | Pásala o usa `res.locals` |
| La página siempre da 404 | El 404 está **antes** de las rutas | El `app.use` del 404 va al final |
| `EADDRINUSE: 3000` | Ya hay un servidor corriendo | Ciérralo o usa `PORT=3001`. En PowerShell: `$env:PORT=3001; npm run dev` |
| `SqliteError: no such table` | La BD quedó vieja o a medias | Detén el servidor y borra `reservas.db` |
| `SqliteError: UNIQUE constraint failed` | Faltó validar el duplicado | Revisa `validarLaboratorio` |

## Plan B: sin `better-sqlite3` (usando el SQLite que trae Node 22.5+)

Si `npm install better-sqlite3` falla, cambia **solo** estas 3 líneas en `src/db/conexion.js` y todo lo demás funciona igual (lo probé con las mismas 14 pruebas):

```js
import { DatabaseSync } from "node:sqlite";          // en lugar de: import Database from "better-sqlite3";
const db = new DatabaseSync(ruta);                   // en lugar de: new Database(ruta)
db.exec("PRAGMA foreign_keys = ON");                 // en lugar de: db.pragma("foreign_keys = ON")
```
Y quita `better-sqlite3` de `package.json`. En algunas versiones Node muestra un aviso "ExperimentalWarning"; es normal.

## Plan C: MySQL (si te lo exigen o hay XAMPP)

`npm install mysql2`, y en `conexion.js`:
```js
import mysql from "mysql2/promise";
export const pool = mysql.createPool({ host: "localhost", user: "root", password: "", database: "reservas" });
// consultas:  const [filas] = await pool.query("SELECT * FROM laboratorios WHERE id = ?", [id]);
//             const [r] = await pool.query("INSERT INTO ... VALUES (?, ?)", [a, b]);  r.insertId
```
Con MySQL todo es asíncrono, así que las rutas pasan a ser `async (req, res, next) => { try { ... await ... } catch (e) { next(e); } }` y las validaciones también llevan `await`. En `schema.sql` usa `INT AUTO_INCREMENT PRIMARY KEY`, `VARCHAR`, `DATE` y `TIME`.

## Cómo explicarle tu proyecto al evaluador (30 segundos)

> "Separé `server.js`, que arranca el servidor, de `app.js`, que construye la aplicación recibiendo la BD por parámetro. Eso me permite probarla con una base en memoria. Las rutas están organizadas por módulo con `express.Router`, las reglas de negocio en `validaciones.js` y las vistas en EJS con parciales para la cabecera. Uso consultas parametrizadas contra SQL Injection y `<%= %>` para escapar HTML contra XSS. Valido todo en el servidor. El choque de horarios lo resuelvo con la condición de intervalos superpuestos en SQL, y aplico POST-Redirect-GET."
