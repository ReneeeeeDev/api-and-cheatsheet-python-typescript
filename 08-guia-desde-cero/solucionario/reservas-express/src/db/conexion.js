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
