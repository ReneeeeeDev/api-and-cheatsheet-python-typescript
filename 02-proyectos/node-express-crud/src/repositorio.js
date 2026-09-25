// Capa de datos: guarda en un archivo JSON (sin instalar base de datos).
// En la prueba puedes reemplazar estas funciones por consultas MySQL (ver README).
import { readFileSync, writeFileSync, existsSync } from "fs";

export function crearRepositorio(ruta) {
  const semilla = {
    nextId: 4,
    productos: [
      { id: 1, nombre: "Mouse inalámbrico", categoria: "Periféricos", precio: 15.5, stock: 20 },
      { id: 2, nombre: "Teclado mecánico", categoria: "Periféricos", precio: 45, stock: 8 },
      { id: 3, nombre: "Monitor 24\"", categoria: "Pantallas", precio: 139.99, stock: 3 },
    ],
  };

  const leer = () => (existsSync(ruta) ? JSON.parse(readFileSync(ruta, "utf-8")) : structuredClone(semilla));
  const escribir = (db) => writeFileSync(ruta, JSON.stringify(db, null, 2));

  return {
    listar({ q = "", categoria = "", orden = "id" } = {}) {
      const texto = q.toLowerCase();
      const lista = leer().productos.filter(
        (p) => p.nombre.toLowerCase().includes(texto) && (!categoria || p.categoria === categoria)
      );
      const comparadores = {
        id: (a, b) => a.id - b.id,
        nombre: (a, b) => a.nombre.localeCompare(b.nombre),
        precio: (a, b) => a.precio - b.precio,
        stock: (a, b) => a.stock - b.stock,
      };
      return lista.sort(comparadores[orden] ?? comparadores.id);
    },
    obtener(id) {
      return leer().productos.find((p) => p.id === id) ?? null;
    },
    crear(datos) {
      const db = leer();
      const nuevo = { id: db.nextId++, ...datos };
      db.productos.push(nuevo);
      escribir(db);
      return nuevo;
    },
    actualizar(id, datos) {
      const db = leer();
      const i = db.productos.findIndex((p) => p.id === id);
      if (i === -1) return null;
      db.productos[i] = { ...db.productos[i], ...datos, id };
      escribir(db);
      return db.productos[i];
    },
    eliminar(id) {
      const db = leer();
      const antes = db.productos.length;
      db.productos = db.productos.filter((p) => p.id !== id);
      if (db.productos.length === antes) return false;
      escribir(db);
      return true;
    },
    resumen() {
      const productos = leer().productos;
      return {
        totalProductos: productos.length,
        unidades: productos.reduce((s, p) => s + p.stock, 0),
        valorInventario: Number(productos.reduce((s, p) => s + p.precio * p.stock, 0).toFixed(2)),
        stockBajo: productos.filter((p) => p.stock < 5).map((p) => p.nombre),
      };
    },
  };
}
