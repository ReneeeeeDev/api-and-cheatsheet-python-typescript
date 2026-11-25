# Retos resueltos — Node + Express

Se ejecuta igual que el original:
```bash
npm install
npm run dev        # http://localhost:3000   (usuario: admin / clave: admin123)
npm test           # 12 pruebas
```
> Borra `db.json` si existía del proyecto original. Credenciales configurables: `APP_USER` y `APP_PASS` (variables de entorno).

## Reto 1: campo `activo` + `PATCH /api/productos/:id/estado`
- `src/repositorio.js`: los productos tienen `activo`. `listar()` acepta `?activo=true|false`, y `resumen()` cuenta los inactivos.
- `src/app.js`: `router.patch("/:id/estado", ...)` valida que `activo` sea **booleano** (`typeof activo !== "boolean"` responde 400), devuelve 404 si no existe y 200 con el producto actualizado.
- **¿Por qué PATCH y no PUT?** PUT reemplaza el recurso completo; PATCH modifica una parte. Cambiar solo el estado es una modificación parcial.
- Frontend: columna Estado, botón Activar/Desactivar y filtro Todos/Activos/Inactivos.

```bash
curl -X PATCH http://localhost:3000/api/productos/1/estado -H "Content-Type: application/json" -H "Authorization: Bearer TU_TOKEN" -d "{\"activo\":false}"
```

## Reto 2: paginación `?pagina=2&limite=5`
- Si llega `pagina`, la respuesta es `{ datos, pagina, limite, total, paginas }`; si no, el arreglo simple de siempre (así no se rompe el frontend de React).
- `limite` entre 1 y 50; la página se ajusta entre 1 y `paginas`. Se calcula con `slice((pagina - 1) * limite, pagina * limite)`.
- Frontend: botones Anterior/Siguiente, y "Página X de Y". Al cambiar un filtro se vuelve a la página 1.

## Reto 3: login + middleware de autorización
- `POST /api/login` con `{usuario, clave}` genera un token (`crypto.randomUUID()`) guardado en un `Set` en memoria. `POST /api/logout` lo elimina.
- Middleware `requiereAuth`: lee `Authorization: Bearer <token>`. Si el token no es válido responde **401** y la petición no llega al manejador.
- Se aplica **solo a las rutas que modifican** datos: `router.post("/", requiereAuth, manejador)`. Los GET siguen siendo públicos.
- Frontend: formulario de login, token en `sessionStorage`, la función `pedir()` añade la cabecera a todas las peticiones y, si recibe 401, cierra la sesión.
- **En producción** se usaría: usuarios en BD con contraseña hasheada (bcrypt), **JWT** con expiración y HTTPS (ver cheatsheet 02, sección 17).

```bash
curl -X POST http://localhost:3000/api/login -H "Content-Type: application/json" -d "{\"usuario\":\"admin\",\"clave\":\"admin123\"}"
# → {"token":"...","usuario":"admin"}
curl -X DELETE http://localhost:3000/api/productos/3 -H "Authorization: Bearer EL_TOKEN"
```

> El proyecto `06-retos-resueltos/react-vite-crud` usa el backend **original** (`02-proyectos/node-express-crud`), que no pide login.
