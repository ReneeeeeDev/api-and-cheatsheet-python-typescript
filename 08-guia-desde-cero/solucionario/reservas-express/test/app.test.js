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
