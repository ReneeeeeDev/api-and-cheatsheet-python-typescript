# Cheatsheet JavaScript + Node.js + Express

## 1. JavaScript moderno (ES6+)

```js
// Variables: usa const por defecto, let si cambia. Nunca var.
const nombre = "Ana";
let edad = 25;

// Template strings
console.log(`Hola ${nombre}, tienes ${edad} años`);

// Comparación: SIEMPRE === (estricto)
"5" == 5   // true  (mal)
"5" === 5  // false (bien)

// Conversión
Number("10"), parseInt("10px"), parseFloat("3.5"), String(10), Boolean(0)
Number.isNaN(Number("abc"))   // true

// Funciones
function sumar(a, b = 0) { return a + b; }
const restar = (a, b) => a - b;          // arrow function
const cuadrado = x => x * x;

// Ternario, nullish y optional chaining
const estado = nota >= 7 ? "Aprobado" : "Reprobado";
const tel = persona.telefono ?? "N/A";     // si es null/undefined
const ciudad = persona?.direccion?.ciudad; // no revienta si no existe
```

## 2. Arrays (lo más preguntado)

```js
const nums = [5, 3, 8, 1];
nums.push(10); nums.pop(); nums.unshift(0); nums.shift();
nums.includes(3); nums.indexOf(8); nums.length;
nums.slice(1, 3);            // copia parcial
nums.splice(1, 1);           // elimina 1 elemento en índice 1 (modifica)
[...nums].reverse();         // copia invertida
[...nums].sort((a, b) => a - b);   // ¡sort sin función ordena como texto!

// Métodos funcionales (dominar estos 5)
const dobles   = nums.map(n => n * 2);
const pares    = nums.filter(n => n % 2 === 0);
const total    = nums.reduce((acc, n) => acc + n, 0);
const primero  = nums.find(n => n > 4);
const idx      = nums.findIndex(n => n > 4);
nums.some(n => n > 7);  nums.every(n => n > 0);
nums.forEach((n, i) => console.log(i, n));

// Array de objetos (típico CRUD)
const estudiantes = [
  { id: 1, nombre: "Ana", nota: 9 },
  { id: 2, nombre: "Luis", nota: 6 },
];
const aprobados = estudiantes.filter(e => e.nota >= 7);
const nombres = estudiantes.map(e => e.nombre);
const promedio = estudiantes.reduce((s, e) => s + e.nota, 0) / estudiantes.length;
const ordenados = [...estudiantes].sort((a, b) => b.nota - a.nota);
// "Actualizar" sin mutar:
const actualizados = estudiantes.map(e => e.id === 2 ? { ...e, nota: 7 } : e);
// "Eliminar" sin mutar:
const sinLuis = estudiantes.filter(e => e.id !== 2);

// Agrupar
const porEstado = estudiantes.reduce((acc, e) => {
  const k = e.nota >= 7 ? "aprobados" : "reprobados";
  (acc[k] ||= []).push(e);
  return acc;
}, {});
```

## 3. Objetos, destructuring, spread

```js
const persona = { nombre: "Ana", edad: 25 };
const { nombre, edad } = persona;               // destructuring
const [a, b, ...resto] = [1, 2, 3, 4];
const copia = { ...persona, email: "a@m.com" }; // spread
Object.keys(persona); Object.values(persona); Object.entries(persona);
JSON.stringify(persona);  JSON.parse('{"a":1}');
```

## 4. Strings

```js
const s = "  Hola Mundo  ";
s.trim(); s.toLowerCase(); s.toUpperCase();
s.split(" "); ["a","b"].join("-");
s.includes("Mundo"); s.startsWith("Ho"); s.replaceAll("o", "0");
s.split("").reverse().join("");   // invertir
s.padStart(5, "0");               // "00042"
```

## 5. Clases

```js
class Persona {
  #secreto = "privado";            // campo privado real
  constructor(nombre, edad) { this.nombre = nombre; this.edad = edad; }
  presentarse() { return `Soy ${this.nombre}`; }
  static crear(obj) { return new Persona(obj.nombre, obj.edad); }
}
class Estudiante extends Persona {
  constructor(nombre, edad, carrera) { super(nombre, edad); this.carrera = carrera; }
  presentarse() { return `${super.presentarse()} y estudio ${this.carrera}`; }
}
```

## 6. Asincronía (clave para APIs)

```js
// Promesas con async/await
async function cargarUsuarios() {
  try {
    const res = await fetch("https://jsonplaceholder.typicode.com/users");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Error:", err.message);
  }
}

// POST con fetch
await fetch("/api/productos", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre: "Mouse", precio: 12.5 }),
});

// Varias en paralelo
const [u, p] = await Promise.all([fetch("/api/u"), fetch("/api/p")]);
```

## 7. DOM (JavaScript en el navegador, sin framework)

```js
const form = document.querySelector("#form");
const lista = document.getElementById("lista");

form.addEventListener("submit", (e) => {
  e.preventDefault();                            // evita recargar la página
  const nombre = form.nombre.value.trim();
  if (!nombre) return alert("Nombre obligatorio");
  const li = document.createElement("li");
  li.textContent = nombre;                       // textContent evita XSS
  lista.appendChild(li);
  form.reset();
});

elemento.classList.add("activo"); elemento.classList.toggle("oculto");
elemento.style.display = "none";
lista.innerHTML = items.map(i => `<li>${i}</li>`).join("");
```

## 8. Node.js básico

```bash
node -v && npm -v
npm init -y                     # crea package.json
npm install express             # dependencia
npm install -D nodemon          # dependencia de desarrollo
node index.js
npx nodemon index.js            # reinicia al guardar
```

En `package.json` agrega `"type": "module"` para usar `import` en lugar de `require`.

```js
// CommonJS                         // ES Modules
const fs = require("fs");           import fs from "fs";
module.exports = { sumar };         export function sumar() {}
                                    export default app;

// Leer / escribir archivos
import { readFileSync, writeFileSync, existsSync } from "fs";
const datos = JSON.parse(readFileSync("db.json", "utf-8"));
writeFileSync("db.json", JSON.stringify(datos, null, 2));
```

## 9. Express: API REST completa (memorizar esta estructura)

```js
import express from "express";
const app = express();
app.use(express.json());                    // lee JSON del body
app.use(express.urlencoded({ extended: true })); // lee formularios HTML
app.use(express.static("public"));          // sirve HTML/CSS/JS de /public

let productos = [{ id: 1, nombre: "Mouse", precio: 12.5 }];
let nextId = 2;

// LISTAR (con búsqueda opcional ?q=)
app.get("/api/productos", (req, res) => {
  const q = (req.query.q || "").toLowerCase();
  res.json(productos.filter(p => p.nombre.toLowerCase().includes(q)));
});

// OBTENER UNO
app.get("/api/productos/:id", (req, res) => {
  const p = productos.find(p => p.id === Number(req.params.id));
  if (!p) return res.status(404).json({ error: "No encontrado" });
  res.json(p);
});

// CREAR
app.post("/api/productos", (req, res) => {
  const { nombre, precio } = req.body;
  if (!nombre || precio == null || isNaN(precio) || precio < 0)
    return res.status(400).json({ error: "Datos inválidos" });
  const nuevo = { id: nextId++, nombre, precio: Number(precio) };
  productos.push(nuevo);
  res.status(201).json(nuevo);
});

// ACTUALIZAR
app.put("/api/productos/:id", (req, res) => {
  const i = productos.findIndex(p => p.id === Number(req.params.id));
  if (i === -1) return res.status(404).json({ error: "No encontrado" });
  productos[i] = { ...productos[i], ...req.body, id: productos[i].id };
  res.json(productos[i]);
});

// ELIMINAR
app.delete("/api/productos/:id", (req, res) => {
  const antes = productos.length;
  productos = productos.filter(p => p.id !== Number(req.params.id));
  if (productos.length === antes) return res.status(404).json({ error: "No encontrado" });
  res.status(204).end();
});

// Middleware de errores (al final)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: "Error interno" });
});

app.listen(3000, () => console.log("http://localhost:3000"));
```

Si el frontend está en otro puerto (React en 5173): `npm i cors` y `app.use(cors())`.

## 10. Express + MySQL (si hay XAMPP en el lab)

```bash
npm install mysql2
```
```js
import mysql from "mysql2/promise";
const pool = mysql.createPool({ host: "localhost", user: "root", password: "", database: "tienda" });

app.get("/api/productos", async (req, res, next) => {
  try {
    const [rows] = await pool.query("SELECT * FROM productos ORDER BY id DESC");
    res.json(rows);
  } catch (e) { next(e); }
});

app.post("/api/productos", async (req, res, next) => {
  try {
    const { nombre, precio } = req.body;
    const [r] = await pool.query("INSERT INTO productos (nombre, precio) VALUES (?, ?)", [nombre, precio]);
    res.status(201).json({ id: r.insertId, nombre, precio });
  } catch (e) { next(e); }
});
// UPDATE: pool.query("UPDATE productos SET nombre=?, precio=? WHERE id=?", [n, p, id]) → r.affectedRows
// DELETE: pool.query("DELETE FROM productos WHERE id=?", [id])
```

## 11. Testing en Node (sin instalar nada, Node 18+)

```js
// suma.test.js → ejecutar: node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { sumar } from "./suma.js";

test("suma dos números", () => {
  assert.equal(sumar(2, 3), 5);
});
test("lanza error", () => {
  assert.throws(() => sumar("a", 1));
});
```

Con Jest (`npm i -D jest`): `expect(sumar(2,3)).toBe(5)`; con Vitest es igual.

## 12. TypeScript en 1 minuto

```ts
let edad: number = 25;
let nombres: string[] = ["Ana"];
interface Producto { id: number; nombre: string; precio: number; stock?: number; }
type Estado = "activo" | "inactivo";
function total(items: Producto[]): number {
  return items.reduce((s, p) => s + p.precio, 0);
}
```
`npx tsc --init` crea tsconfig; `npx tsc` compila a JS.

---

# PARTE 2 — AMPLIACIÓN

> Ejemplos ejecutables en `05-ejemplos/javascript/` (01 a 10) y `05-ejemplos/web-dom/index.html`.

## 13. Dónde se ejecuta JavaScript

| Entorno | Cómo | Tiene | No tiene |
|---|---|---|---|
| **Navegador** | `<script src="app.js"></script>`, o F12 → Console | `document`, `window`, `localStorage`, `fetch`, `alert` | `fs`, `process`, `require` |
| **Node.js** | `node archivo.js` | `fs`, `path`, `process`, `http`, `fetch` (18+) | `document`, `window` |
| **REPL de Node** | `node` → escribir → `.exit` | Probar rápido | |

**Scripts en HTML:**
```html
<script src="app.js" defer></script>        <!-- defer: espera a que el HTML cargue -->
<script type="module" src="main.js"></script>  <!-- permite import/export en el navegador -->
```
Los módulos (`type="module"`) **no funcionan con doble clic** (file://): usa Live Server o `npx serve`.

## 14. Hoisting, scope y var/let/const

```js
console.log(a);   // undefined (var se "eleva" sin valor)
var a = 1;
console.log(b);   // ReferenceError (let/const: "zona muerta temporal")
let b = 2;

for (var i = 0; i < 3; i++) setTimeout(() => console.log(i));   // 3 3 3 (una sola variable compartida)
for (let j = 0; j < 3; j++) setTimeout(() => console.log(j));   // 0 1 2 (una variable por vuelta)

const arr = [1];
arr.push(2);       // ✔ const impide REASIGNAR, no MODIFICAR el contenido
// arr = [];       // ✘ TypeError
```

## 15. DOM completo

```js
// Seleccionar
document.getElementById("id");
document.querySelector(".clase");          // el primero
document.querySelectorAll("li");           // NodeList (tiene forEach)
elemento.closest("tr");                    // ancestro más cercano
form.elements.nombre / form.nombre         // campos de un formulario por su name

// Leer / modificar
el.textContent = "texto seguro";           // no interpreta HTML (evita XSS)
el.innerHTML = "<b>html</b>";              // interpreta HTML (¡cuidado con datos del usuario!)
input.value; checkbox.checked; select.value;
el.setAttribute("data-id", 5); el.dataset.id;   // atributos data-*
el.classList.add("activo"); .remove(); .toggle(); .contains();
el.style.display = "none";
el.hidden = true;

// Crear / insertar / eliminar
const li = document.createElement("li");
li.textContent = "Nuevo";
lista.append(li); lista.prepend(li); el.before(otro); el.after(otro);
el.remove();
lista.replaceChildren();                    // vaciar

// Eventos
boton.addEventListener("click", (e) => { e.target; e.currentTarget; });
form.addEventListener("submit", (e) => { e.preventDefault(); /* ... */ });
input.addEventListener("input", ...);      // cada tecla
select.addEventListener("change", ...);    // al cambiar
document.addEventListener("DOMContentLoaded", iniciar);
window.addEventListener("keydown", (e) => { if (e.key === "Escape") cerrar(); });

// Delegación: un listener en el padre para muchos hijos (incluso los creados después)
tabla.addEventListener("click", (e) => {
  const boton = e.target.closest("button[data-accion]");
  if (!boton) return;
  const { accion, id } = boton.dataset;
});

// Leer todo un formulario
const datos = Object.fromEntries(new FormData(form));   // { nombre: "...", edad: "..." } (todo texto)
form.reset();
```

## 16. Almacenamiento en el navegador

```js
localStorage.setItem("clave", JSON.stringify(objeto));   // persiste al cerrar el navegador
const obj = JSON.parse(localStorage.getItem("clave") ?? "null");
localStorage.removeItem("clave"); localStorage.clear();
sessionStorage   // igual, pero se borra al cerrar la pestaña
// Solo guarda TEXTO (por eso JSON). ~5 MB. No guardes contraseñas ni tokens sensibles.
```

## 17. Express ampliado

### Estructura profesional
```
src/
  server.js            → app.listen
  app.js               → middlewares + rutas
  routes/productos.js  → express.Router
  controllers/         → funciones (req, res)
  services/ o models/  → lógica y acceso a datos
  middlewares/         → auth, errores, validación
```

### Router + controlador
```js
// routes/productos.js
import { Router } from "express";
import * as ctrl from "../controllers/productos.js";
const r = Router();
r.get("/", ctrl.listar);
r.get("/:id", ctrl.obtener);
r.post("/", ctrl.crear);
r.put("/:id", ctrl.actualizar);
r.delete("/:id", ctrl.eliminar);
export default r;

// app.js
app.use("/api/productos", productosRouter);
```

### Middlewares propios
```js
// Logger
app.use((req, res, next) => {
  const inicio = Date.now();
  res.on("finish", () => console.log(`${req.method} ${req.originalUrl} ${res.statusCode} ${Date.now() - inicio}ms`));
  next();
});

// Autenticación simple por token
const requiereToken = (req, res, next) => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (token !== process.env.API_TOKEN) return res.status(401).json({ error: "No autorizado" });
  next();
};
app.use("/api/admin", requiereToken, adminRouter);

// Validación reutilizable
const validar = (reglas) => (req, res, next) => {
  const errores = reglas.map((r) => r(req.body)).filter(Boolean);
  if (errores.length) return res.status(400).json({ errores });
  next();
};
const nombreObligatorio = (b) => (!b.nombre?.trim() ? "nombre es obligatorio" : null);
router.post("/", validar([nombreObligatorio]), ctrl.crear);

// Rutas async: en Express 5 los errores de promesas llegan solos al manejador de errores.
// En Express 4 envuelve:  const asyncH = (fn) => (req, res, next) => fn(req, res, next).catch(next);
```

### Sesiones y login (vistas server-side)
```bash
npm i express-session bcrypt
```
```js
import session from "express-session";
import bcrypt from "bcrypt";
app.use(session({ secret: "cambia-esto", resave: false, saveUninitialized: false }));

app.post("/login", async (req, res) => {
  const u = db.prepare("SELECT * FROM usuarios WHERE email = ?").get(req.body.email);
  if (!u || !(await bcrypt.compare(req.body.clave, u.clave_hash)))
    return res.status(401).render("login", { error: "Credenciales incorrectas" });
  req.session.usuario = { id: u.id, nombre: u.nombre };
  res.redirect("/");
});
app.post("/logout", (req, res) => req.session.destroy(() => res.redirect("/login")));
const autenticado = (req, res, next) => (req.session.usuario ? next() : res.redirect("/login"));
// Registrar: const hash = await bcrypt.hash(clave, 10);
```

### JWT (APIs sin sesión)
```bash
npm i jsonwebtoken
```
```js
import jwt from "jsonwebtoken";
const token = jwt.sign({ id: u.id, rol: u.rol }, process.env.JWT_SECRET, { expiresIn: "2h" });
// El cliente lo envía en cada petición:  Authorization: Bearer <token>
const payload = jwt.verify(token, process.env.JWT_SECRET);   // lanza error si es inválido o expiró
```

### Paginación, ordenamiento y filtros en la API
```js
router.get("/", (req, res) => {
  const pagina = Math.max(1, Number(req.query.pagina) || 1);
  const limite = Math.min(50, Number(req.query.limite) || 10);
  const columnasPermitidas = ["nombre", "precio", "id"];                    // ¡nunca metas req.query directo en ORDER BY!
  const orden = columnasPermitidas.includes(req.query.orden) ? req.query.orden : "id";
  const total = db.prepare("SELECT COUNT(*) AS n FROM productos").get().n;
  const datos = db.prepare(`SELECT * FROM productos ORDER BY ${orden} LIMIT ? OFFSET ?`).all(limite, (pagina - 1) * limite);
  res.json({ datos, pagina, limite, total, paginas: Math.ceil(total / limite) });
});
```

### Vistas con EJS (server-side rendering)
```js
app.set("view engine", "ejs");            // npm i ejs; las vistas van en /views
res.render("productos", { productos, titulo: "Lista" });
```
```html
<%= variable %>          <!-- escapa HTML (seguro) -->
<%- include("partials/header") %>   <!-- sin escapar: solo para incluir plantillas -->
<% if (productos.length) { %> ... <% } else { %> Vacío <% } %>
<% productos.forEach(p => { %> <li><%= p.nombre %></li> <% }) %>
```

### Variables de entorno con .env
```bash
# .env   (agrégalo a .gitignore)
PORT=3000
JWT_SECRET=supersecreto
```
```js
// Node 20.6+:  node --env-file=.env src/server.js    (sin instalar dotenv)
// Alternativa:  npm i dotenv  →  import "dotenv/config";
const PORT = process.env.PORT ?? 3000;
```

### Seguridad básica
```bash
npm i helmet express-rate-limit
```
```js
import helmet from "helmet";
import rateLimit from "express-rate-limit";
app.use(helmet());                                       // cabeceras de seguridad
app.use("/login", rateLimit({ windowMs: 15 * 60 * 1000, max: 10 }));   // anti fuerza bruta
app.disable("x-powered-by");
```

## 18. Mongoose (MongoDB), por si preguntan NoSQL

```js
import mongoose from "mongoose";
await mongoose.connect("mongodb://127.0.0.1:27017/tienda");
const Producto = mongoose.model("Producto", new mongoose.Schema({
  nombre: { type: String, required: true }, precio: { type: Number, min: 0 }, tags: [String],
}, { timestamps: true }));
await Producto.create({ nombre: "Mouse", precio: 10 });
await Producto.find({ precio: { $gt: 5 } }).sort({ nombre: 1 }).limit(10);
await Producto.findByIdAndUpdate(id, { precio: 12 }, { new: true });
await Producto.findByIdAndDelete(id);
```
**SQL vs NoSQL:** SQL usa tablas con esquema fijo, relaciones y transacciones ACID (notas, pagos, inventario). NoSQL (MongoDB) usa documentos JSON flexibles y escala horizontalmente (logs, catálogos variables).

## 19. Pruebas con Jest y Supertest (lo más común en empresas)

```bash
npm i -D jest supertest
# package.json:  "test": "node --experimental-vm-modules node_modules/jest/bin/jest.js"  (si usas ES modules)
```
```js
import request from "supertest";
import { crearApp } from "../src/app.js";
const app = crearApp(crearDb(":memory:"));

describe("API productos", () => {
  test("GET /api/productos devuelve 200", async () => {
    const res = await request(app).get("/api/productos");
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });
  test("POST inválido devuelve 400", async () => {
    const res = await request(app).post("/api/productos").send({});
    expect(res.status).toBe(400);
  });
});
// Matchers: toBe, toEqual (objetos), toContain, toHaveLength, toThrow, toBeNull, toBeGreaterThan
```

## 20. Errores de Node/Express frecuentes

| Error | Causa |
|---|---|
| `Cannot set headers after they are sent to the client` | Respondiste dos veces: falta `return` antes de `res.status(...).json()` |
| `req.body is undefined` | Falta `app.use(express.json())` o `express.urlencoded()` |
| `Cannot GET /ruta` | La ruta no existe con ese método, o el prefijo de `app.use` no coincide |
| `ERR_REQUIRE_ESM` / `Cannot use import statement` | Mezcla de CommonJS y ES Modules: revisa `"type": "module"` |
| `CORS policy: No 'Access-Control-Allow-Origin'` | El frontend está en otro origen: `npm i cors` y `app.use(cors())` |
| `UnhandledPromiseRejection` | Falta `await` o `try/catch` en una función async |
| `EADDRINUSE` | Puerto ocupado |
