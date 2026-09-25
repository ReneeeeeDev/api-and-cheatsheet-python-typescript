// Pruebas con el runner nativo de Node (sin instalar Jest). Ejecutar: npm test
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { crearApp } from "../src/app.js";
import { crearRepositorio } from "../src/repositorio.js";
import { validarProducto } from "../src/validacion.js";

let server, base, dir;

before(async () => {
  dir = mkdtempSync(join(tmpdir(), "crud-"));
  const app = crearApp(crearRepositorio(join(dir, "test.json")));
  await new Promise((ok) => (server = app.listen(0, ok)));   // puerto libre aleatorio
  base = `http://localhost:${server.address().port}/api/productos`;
});
after(() => { server.close(); rmSync(dir, { recursive: true, force: true }); });

const json = (method, body) => ({ method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

// ---- Unitarias
test("validación: datos correctos", () => {
  const r = validarProducto({ nombre: "Laptop", categoria: "PC", precio: "500.555", stock: "2" });
  assert.deepEqual(r.errores, []);
  assert.equal(r.datos.precio, 500.56);
});

test("validación: datos incorrectos", () => {
  const r = validarProducto({ nombre: "a", precio: -1, stock: 1.5 });
  assert.equal(r.errores.length, 4);
});

// ---- Integración (API real)
test("GET lista los productos", async () => {
  const res = await fetch(base);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).length, 3);
});

test("GET busca y ordena", async () => {
  const data = await (await fetch(`${base}?q=o&orden=precio`)).json();
  const precios = data.map((p) => p.precio);
  assert.deepEqual(precios, [...precios].sort((a, b) => a - b));
});

test("POST crea y responde 201", async () => {
  const res = await fetch(base, json("POST", { nombre: "Parlantes", categoria: "Audio", precio: 25, stock: 4 }));
  assert.equal(res.status, 201);
  const p = await res.json();
  assert.equal(p.id, 4);
  assert.equal((await (await fetch(`${base}/resumen`)).json()).stockBajo.includes("Parlantes"), true);
});

test("POST inválido responde 400", async () => {
  const res = await fetch(base, json("POST", { nombre: "" }));
  assert.equal(res.status, 400);
  assert.ok((await res.json()).errores.length > 0);
});

test("PUT actualiza parcialmente", async () => {
  const res = await fetch(`${base}/1`, json("PUT", { stock: 99 }));
  const p = await res.json();
  assert.equal(p.stock, 99);
  assert.equal(p.nombre, "Mouse inalámbrico");
});

test("DELETE elimina y luego 404", async () => {
  assert.equal((await fetch(`${base}/2`, { method: "DELETE" })).status, 204);
  assert.equal((await fetch(`${base}/2`)).status, 404);
  assert.equal((await fetch(`${base}/abc`)).status, 400);
});
