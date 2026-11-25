# Retos resueltos — React

Usa el backend **original** (sin login):
```bash
# Terminal 1
cd 02-proyectos/node-express-crud
npm install
npm run dev
# Terminal 2
cd 06-retos-resueltos/react-vite-crud
npm install          # instala también react-router-dom
npm run dev          # http://localhost:5173
```

## Reto 1: filtro por categoría
- `api.listar({ q, orden, categoria })` envía `?categoria=`; el backend ya filtraba por ese campo.
- Las categorías se calculan en el hook a partir de **todos** los productos, con `[...new Set(todos.map(p => p.categoria))]` ordenado con `localeCompare`, para que el `<select>` no pierda opciones al filtrar.
- Bonus: el formulario sugiere las categorías existentes con un `<datalist>`.

## Reto 2: custom hook `useProductos()` (`src/hooks/useProductos.js`)
- Encapsula el estado (`productos`, `resumen`, `categorias`, `filtros`, `cargando`, `error`) y las acciones (`cambiarFiltro`, `guardar`, `eliminar`, `recargar`).
- La página `Inventario.jsx` queda solo con la UI: `const { productos, guardar, ... } = useProductos();`.
- Los hooks personalizados **empiezan con "use"** y pueden usar otros hooks (useState, useEffect, useCallback).
- `useCallback(cargar, [filtros])` + `useEffect` con `setTimeout`/`clearTimeout` hace el debounce de la búsqueda.

## Reto 3: React Router con detalle `/productos/:id`
- `main.jsx` envuelve la app en `<BrowserRouter>`.
- `App.jsx` define `<Routes>`: `/` → `Inventario`, `/productos/:id` → `DetalleProducto`, `*` → 404.
- `ProductoTabla` convierte el nombre en `<Link to={`/productos/${p.id}`}>` (navega sin recargar la página).
- `DetalleProducto` usa `useParams()` para leer el id, `useNavigate()` para "Atrás" (`navigate(-1)`), y cancela la actualización del estado si el componente se desmonta (variable `activo` en la limpieza del `useEffect`).
- `NavLink` agrega la clase `active` al enlace de la ruta actual.

Estructura final:
```
src/
├── main.jsx               BrowserRouter
├── App.jsx                layout + Routes
├── api.js                 fetch centralizado
├── hooks/useProductos.js  custom hook
├── pages/Inventario.jsx   página principal
├── pages/DetalleProducto.jsx
└── components/            ProductoForm, ProductoTabla, Resumen
```
