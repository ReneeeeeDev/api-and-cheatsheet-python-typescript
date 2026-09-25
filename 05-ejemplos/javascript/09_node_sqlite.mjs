// 09 - Base de datos SQLite SIN instalar paquetes (módulo node:sqlite, Node 22.5 o superior).
// Ejecutar:  node 09_node_sqlite.mjs
// (En Node 22.5–22.12 puede requerir:  node --experimental-sqlite 09_node_sqlite.mjs)
// Con better-sqlite3 (npm i better-sqlite3) la API es casi idéntica: new Database(ruta).

import { DatabaseSync } from "node:sqlite";

const db = new DatabaseSync(":memory:");          // o "archivo.db" para guardar en disco
db.exec("PRAGMA foreign_keys = ON");
db.exec(`
  CREATE TABLE categorias (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE);
  CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio > 0),
    stock INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER REFERENCES categorias(id)
  );
`);

// Sentencias preparadas con ? (seguras contra SQL Injection)
const insCat = db.prepare("INSERT INTO categorias (nombre) VALUES (?)");
const perifericos = insCat.run("Periféricos").lastInsertRowid;
const pantallas = insCat.run("Pantallas").lastInsertRowid;

const insProd = db.prepare("INSERT INTO productos (nombre, precio, stock, categoria_id) VALUES (?, ?, ?, ?)");
insProd.run("Mouse", 15.5, 20, perifericos);
insProd.run("Teclado", 45, 8, perifericos);
insProd.run("Monitor", 139.99, 3, pantallas);

console.log("Todos:", db.prepare("SELECT * FROM productos").all());
console.log("Uno:", db.prepare("SELECT * FROM productos WHERE id = ?").get(2));
console.log("No existe:", db.prepare("SELECT * FROM productos WHERE id = ?").get(99));   // undefined

const r = db.prepare("UPDATE productos SET stock = stock - ? WHERE id = ?").run(5, 1);
console.log("Filas actualizadas:", r.changes);

console.log("Resumen por categoría:", db.prepare(`
  SELECT c.nombre, COUNT(p.id) AS productos, SUM(p.precio * p.stock) AS valor
  FROM categorias c LEFT JOIN productos p ON p.categoria_id = c.id
  GROUP BY c.id ORDER BY valor DESC`).all());

try {
  insProd.run("Gratis", 0, 1, perifericos);
} catch (e) {
  console.log("Error esperado (CHECK):", e.message);
}

// Transacción manual
db.exec("BEGIN");
try {
  db.prepare("UPDATE productos SET stock = stock - 1 WHERE id = ?").run(3);
  db.prepare("INSERT INTO productos (nombre, precio) VALUES (?, ?)").run("X", -1);   // falla
  db.exec("COMMIT");
} catch {
  db.exec("ROLLBACK");
  console.log("Rollback: stock del monitor sigue en", db.prepare("SELECT stock FROM productos WHERE id = 3").get().stock);
}
db.close();
