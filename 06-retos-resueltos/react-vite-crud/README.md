# Inventario — React + Vite (frontend que consume la API Node)

Frontend en React con componentes, `useState`, `useEffect` (con limpieza y debounce), formulario controlado con validación, manejo de carga/errores y una capa `api.js` que centraliza los `fetch`.

## Ejecutar (necesitas 2 terminales)
```bash
# Terminal 1: backend
cd ../node-express-crud
npm install
npm run dev              # http://localhost:3000

# Terminal 2: frontend
cd react-vite-crud
npm install
npm run dev              # http://localhost:5173
```
`vite.config.js` tiene un **proxy**: las llamadas a `/api` se envían al backend en el puerto 3000.

## Estructura
```
src/main.jsx                    ← punto de entrada
src/App.jsx                     ← estado principal y lógica
src/api.js                      ← llamadas HTTP
src/components/ProductoForm.jsx ← formulario controlado (crear/editar)
src/components/ProductoTabla.jsx← listado con key
src/components/Resumen.jsx      ← tarjetas de totales
```

## Conceptos que demuestra
- **Levantar el estado**: `App` guarda `productos` y `editando`; los hijos reciben datos y funciones por props.
- **Hijo → padre**: `onGuardar`, `onEditar`, `onEliminar`.
- **`key` para reiniciar un componente**: `<ProductoForm key={editando?.id ?? "nuevo"} />`.
- **`useEffect` con cleanup**: el `return () => clearTimeout(t)` cancela búsquedas mientras escribes.
- **Estados de UI**: cargando, error, mensaje de éxito, botón deshabilitado al enviar.
- **Inmutabilidad**: `setForm({ ...form, [name]: value })`.

## Build para producción / Vercel
```bash
npm run build        # genera dist/
```
En Vercel: importar el repo → Framework "Vite" → Deploy (el backend tendría que estar desplegado aparte y cambiar `BASE` en `api.js`).

## Reto para practicar
- Agregar filtro por categoría con un `<select>` generado a partir de los productos.
- Separar la lógica en un custom hook `useProductos()`.
- Agregar React Router con una página `/productos/:id` de detalle.
