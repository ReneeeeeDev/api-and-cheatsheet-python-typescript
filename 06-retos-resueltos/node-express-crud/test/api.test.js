// Pruebas (incluye los 3 retos). Ejecutar: npm test
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { crearApp } from "../src/app.js";
import { crearRepositorio } from "../src/repositorio.js";
import { validarProducto } from "../src/validacion.js";

let server, base, dir, token;

before(async () => {
  dir = mkdtempSync(join(tmpdir(), "crud-"));
  const app = crearApp(crearRepositorio(join(dir, "test.json")));
  await new Promise((ok) => (server = app.listen(0, ok)));
  base = `http://localhost:${server.address().port}/api`;
});
after(() => { server.close(); rmSync(dir, { recursive: true, force: true }); });

// Helper: petición JSON con el token si existe
const pedir = (metodo, ruta, body, conToken = true) => fetch(base + ruta, {
  method: metodo,
  headers: { "Content-Type": "application/json", ...(conToken && token ? { Authorization: `Bearer ${token}` } : {}) },
  body: body === undefined ? undefined : JSON.stringify(body),
});

// ---- Unitarias
test("validación: datos correctos", () => {
  const r = validarProducto({ nombre: "Laptop", categoria: "PC", precio: "500.555", stock: "2" });
  assert.deepEqual(r.errores, []);
  assert.equal(r.datos.precio, 500.56);
});

test("validación: datos incorrectos", () => {
  assert.equal(validarProducto({ nombre: "a", precio: -1, stock: 1.5 }).errores.length, 4);
});

// ---- RETO 3: login y middleware
test("sin token no se puede crear (401)", async () => {
  const res = await pedir("POST", "/productos", { nombre: "X", categoria: "Y", precio: 1, stock: 1 }, false);
  assert.equal(res.status, 401);
});

test("login incorrecto 401, correcto devuelve token", async () => {
  assert.equal((await pedir("POST", "/login", { usuario: "admin", clave: "mala" }, false)).status, 401);
  const res = await pedir("POST", "/login", { usuario: "admin", clave: "admin123" }, false);
  assert.equal(res.status, 200);
  token = (await res.json()).token;
  assert.ok(token.length > 10);
});

test("token inventado es rechazado", async () => {
  const res = await fetch(base + "/productos/1", { method: "DELETE", headers: { Authorization: "Bearer inventado" } });
  assert.equal(res.status, 401);
});

// ---- CRUD con token
test("GET es público y lista 3", async () => {
  const res = await pedir("GET", "/productos", undefined, false);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).length, 3);
});

test("POST crea (201) con activo=true", async () => {
  const res = await pedir("POST", "/productos", { nombre: "Parlantes", categoria: "Audio", precio: 25, stock: 4 });
  assert.equal(res.status, 201);
  const p = await res.json();
  assert.equal(p.id, 4);
  assert.equal(p.activo, true);
});

test("POST inválido 400", async () => {
  assert.equal((await pedir("POST", "/productos", { nombre: "" })).status, 400);
});

test("PUT actualiza parcialmente", async () => {
  const p = await (await pedir("PUT", "/productos/1", { stock: 99 })).json();
  assert.equal(p.stock, 99);
  assert.equal(p.nombre, "Mouse inalámbrico");
});

// ---- RETO 1: activo + PATCH
test("PATCH estado cambia activo y valida booleano", async () => {
  const r1 = await pedir("PATCH", "/productos/2/estado", { activo: false });
  assert.equal(r1.status, 200);
  assert.equal((await r1.json()).activo, false);
  assert.equal((await pedir("PATCH", "/productos/2/estado", { activo: "no" })).status, 400);
  assert.equal((await pedir("PATCH", "/productos/999/estado", { activo: true })).status, 404);
  const inactivos = await (await pedir("GET", "/productos?activo=false")).json();
  assert.deepEqual(inactivos.map((p) => p.id).sort(), [2, 3]);
  const activos = await (await pedir("GET", "/productos?activo=true")).json();
  assert.deepEqual(activos.map((p) => p.id).sort(), [1, 4]);
});

// ---- RETO 2: paginación
test("paginación devuelve metadatos y corta la lista", async () => {
  const r = await (await pedir("GET", "/productos?pagina=2&limite=3")).json();
  assert.deepEqual({ pagina: r.pagina, limite: r.limite, total: r.total, paginas: r.paginas }, { pagina: 2, limite: 3, total: 4, paginas: 2 });
  assert.equal(r.datos.length, 1);
  const fuera = await (await pedir("GET", "/productos?pagina=50&limite=3")).json();
  assert.equal(fuera.pagina, 2);                          // se ajusta a la última
});

test("DELETE con token y luego 404; logout invalida el token", async () => {
  assert.equal((await pedir("DELETE", "/productos/2")).status, 204);
  assert.equal((await pedir("GET", "/productos/2")).status, 404);
  assert.equal((await pedir("POST", "/logout")).status, 204);
  assert.equal((await pedir("DELETE", "/productos/1")).status, 401);
});
