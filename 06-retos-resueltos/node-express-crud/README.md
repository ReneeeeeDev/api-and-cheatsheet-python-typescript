# Inventario — Node.js + Express (API REST) + JavaScript puro

API REST completa con validación, búsqueda, ordenamiento, resumen (reduce) y un frontend en HTML/CSS/JS sin framework (fetch + DOM). Incluye pruebas unitarias y de integración con el runner nativo de Node.

## Ejecutar
```bash
npm install
npm run dev          # o: npm start
```
- Frontend: http://localhost:3000
- API: http://localhost:3000/api/productos

Los datos se guardan en `db.json` (se crea al primer cambio). Bórralo para volver a los datos iniciales.

## Pruebas
```bash
npm test
```

## Estructura
```
server.js             ← arranca el servidor
src/app.js            ← rutas Express (controlador)
src/validacion.js     ← reglas de negocio / validación
src/repositorio.js    ← acceso a datos (modelo)
public/               ← frontend (index.html, app.js, styles.css)
test/api.test.js      ← pruebas
```
Separar rutas / validación / datos es lo que el evaluador quiere ver (parecido a MVC).

## Endpoints
| Método | Ruta | Respuesta |
|---|---|---|
| GET | /api/productos?q=&orden=precio | 200 lista |
| GET | /api/productos/resumen | 200 totales |
| GET | /api/productos/:id | 200 / 404 |
| POST | /api/productos | 201 / 400 |
| PUT | /api/productos/:id | 200 / 400 / 404 |
| DELETE | /api/productos/:id | 204 / 404 |

## Cambiar a MySQL (si en el lab hay XAMPP)
1. `npm install mysql2`
2. Ejecuta `mysql.sql` en phpMyAdmin.
3. Reemplaza el repositorio por funciones como estas:
```js
import mysql from "mysql2/promise";
const pool = mysql.createPool({ host: "localhost", user: "root", password: "", database: "inventario" });

export const listar = async ({ q = "" }) =>
  (await pool.query("SELECT * FROM productos WHERE nombre LIKE ? ORDER BY id", [`%${q}%`]))[0];
export const obtener = async (id) =>
  (await pool.query("SELECT * FROM productos WHERE id = ?", [id]))[0][0] ?? null;
export const crear = async (d) => {
  const [r] = await pool.query("INSERT INTO productos SET ?", [d]);
  return { id: r.insertId, ...d };
};
export const actualizar = async (id, d) => {
  const [r] = await pool.query("UPDATE productos SET ? WHERE id = ?", [d, id]);
  return r.affectedRows ? obtener(id) : null;
};
export const eliminar = async (id) =>
  (await pool.query("DELETE FROM productos WHERE id = ?", [id]))[0].affectedRows > 0;
```
Y en las rutas usa `async (req, res, next) => { try { ... await ... } catch (e) { next(e) } }`.

## Qué estudiar de este código
- `express.json()`, `express.static()`, `Router`, `router.param`.
- Códigos de estado correctos y mensajes de error en JSON.
- Middleware de 404 y de errores (4 parámetros).
- En el frontend: `fetch`, `FormData`, delegación de eventos, debounce en la búsqueda, escape de HTML contra XSS.

## Reto para practicar
- Agregar un campo `activo` y un endpoint `PATCH /api/productos/:id/estado`.
- Paginación: `?pagina=2&limite=5` usando `slice`.
- Login simple con usuario fijo y un middleware que exija un header `Authorization`.
