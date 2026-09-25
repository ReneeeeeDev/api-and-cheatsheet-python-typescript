// 07 - Node: módulos ES (import/export), archivos (fs), rutas (path), variables de entorno.
// Extensión .mjs = módulo ES aunque no haya package.json con "type": "module".
// Ejecutar:  node 07_archivos_modulos.mjs

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, appendFileSync, unlinkSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import os from "node:os";

// __dirname no existe en módulos ES; se construye así:
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const carpeta = path.join(__dirname, "salida_07");
if (!existsSync(carpeta)) mkdirSync(carpeta);

// ---------------------------------------------------------------- TEXTO
const rutaTxt = path.join(carpeta, "log.txt");
writeFileSync(rutaTxt, "inicio\n", "utf-8");
appendFileSync(rutaTxt, `${new Date().toISOString()} evento\n`);
console.log(readFileSync(rutaTxt, "utf-8").trim().split("\n"));

// ---------------------------------------------------------------- JSON como "base de datos"
const rutaDb = path.join(carpeta, "db.json");
const leerDb = () => (existsSync(rutaDb) ? JSON.parse(readFileSync(rutaDb, "utf-8")) : { productos: [], nextId: 1 });
const guardarDb = (db) => writeFileSync(rutaDb, JSON.stringify(db, null, 2));

const db = leerDb();
db.productos.push({ id: db.nextId++, nombre: "Mouse", precio: 12.5 });
guardarDb(db);
console.log("productos guardados:", leerDb().productos.length);

// ---------------------------------------------------------------- CSV a mano
const csv = "codigo,nombre,precio\nP01,Mouse,12.5\nP02,Teclado,45";
const [encabezado, ...lineas] = csv.split("\n");
const columnas = encabezado.split(",");
const filas = lineas.map((l) => Object.fromEntries(l.split(",").map((v, i) => [columnas[i], v])));
console.log(filas, filas.reduce((s, f) => s + Number(f.precio), 0));
writeFileSync(path.join(carpeta, "salida.csv"), [columnas.join(","), ...filas.map((f) => Object.values(f).join(","))].join("\n"));

// ---------------------------------------------------------------- VERSIÓN ASÍNCRONA (fs/promises)
await writeFile(path.join(carpeta, "async.txt"), "escrito con await");
console.log(await readFile(path.join(carpeta, "async.txt"), "utf-8"));   // top-level await en .mjs

console.log("archivos:", readdirSync(carpeta));
try { readFileSync(path.join(carpeta, "no_existe.txt")); } catch (e) { console.log("error:", e.code); } // ENOENT

// ---------------------------------------------------------------- PATH, OS, ENTORNO
console.log(path.basename(rutaTxt), path.extname(rutaTxt), path.resolve("."));
console.log(os.platform(), os.cpus().length, "CPUs");
console.log("PORT =", process.env.PORT ?? "(no definido, usar 3000)");
// Definir variable: PowerShell  $env:PORT=4000; node app.js     CMD  set PORT=4000 && node app.js
// Linux/Mac  PORT=4000 node app.js     O con archivo .env:  node --env-file=.env app.js (Node 20.6+)

// ---------------------------------------------------------------- EXPORTAR / IMPORTAR
// utilidades.js:
//   export const IVA = 0.15;
//   export function conIva(p) { return p * (1 + IVA); }
//   export default class Calculadora {}
// otro archivo:
//   import Calculadora, { IVA, conIva } from "./utilidades.js";    ← ¡la extensión .js es obligatoria!
//   import * as utils from "./utilidades.js";
// CommonJS (antiguo, sin "type": "module"):
//   module.exports = { conIva };    const { conIva } = require("./utilidades");

unlinkSync(path.join(carpeta, "async.txt"));
