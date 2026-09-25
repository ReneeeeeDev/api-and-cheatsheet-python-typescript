# Cheatsheet React (+ Next.js)

## 1. Crear proyecto

```bash
npm create vite@latest mi-app -- --template react     # o react-ts
cd mi-app
npm install
npm run dev                                            # http://localhost:5173
```

Next.js: `npx create-next-app@latest mi-app` → `npm run dev` (http://localhost:3000).

## 2. Componentes y JSX

```jsx
// Un componente = función que devuelve JSX. Nombre en MAYÚSCULA.
function Saludo({ nombre, edad = 18 }) {       // props con destructuring
  return (
    <div className="card">                        {/* className, no class */}
      <h2>Hola {nombre}</h2>
      {edad >= 18 ? <p>Mayor</p> : <p>Menor</p>}
      {edad > 60 && <span>Jubilado</span>}
    </div>
  );
}

export default function App() {
  return <Saludo nombre="Ana" edad={25} />;
}
```

Reglas JSX: un solo elemento raíz (o `<>...</>`), `className`, `htmlFor`, `onClick` (camelCase), estilos `style={{ color: "red" }}`, etiquetas autocerradas `<img />`.

## 3. useState (estado)

```jsx
import { useState } from "react";

function Contador() {
  const [n, setN] = useState(0);
  return <button onClick={() => setN(n + 1)}>Clicks: {n}</button>;
}

// Estado con arrays: NUNCA mutar (push/splice). Crear uno nuevo.
const [items, setItems] = useState([]);
setItems([...items, nuevo]);                                  // agregar
setItems(items.filter(i => i.id !== id));                     // eliminar
setItems(items.map(i => i.id === id ? { ...i, ...cambios } : i)); // editar

// Estado con objetos
const [form, setForm] = useState({ nombre: "", precio: "" });
setForm({ ...form, nombre: "Mouse" });
```

## 4. Listas y keys

```jsx
<ul>
  {productos.map(p => (
    <li key={p.id}>{p.nombre} - ${p.precio}</li>   // key única obligatoria
  ))}
</ul>
{productos.length === 0 && <p>No hay productos</p>}
```

## 5. Formularios controlados

```jsx
function FormProducto({ onGuardar }) {
  const [form, setForm] = useState({ nombre: "", precio: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.nombre.trim()) return setError("El nombre es obligatorio");
    if (Number(form.precio) <= 0) return setError("Precio inválido");
    onGuardar({ ...form, precio: Number(form.precio) });
    setForm({ nombre: "", precio: "" });
    setError("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="nombre" value={form.nombre} onChange={handleChange} placeholder="Nombre" />
      <input name="precio" type="number" value={form.precio} onChange={handleChange} />
      {error && <p className="error">{error}</p>}
      <button type="submit">Guardar</button>
    </form>
  );
}
```

## 6. useEffect + fetch (consumir API)

```jsx
import { useEffect, useState } from "react";

function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:3000/api/productos")
      .then(r => { if (!r.ok) throw new Error("Error " + r.status); return r.json(); })
      .then(setUsuarios)
      .catch(e => setError(e.message))
      .finally(() => setCargando(false));
  }, []);            // [] = solo al montar. [x] = cada vez que cambia x.

  if (cargando) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;
  return <ul>{usuarios.map(u => <li key={u.id}>{u.nombre}</li>)}</ul>;
}
```

## 7. Comunicación entre componentes

- **Padre → hijo**: props (`<Hijo dato={x} />`).
- **Hijo → padre**: el padre pasa una función (`<Hijo onGuardar={guardar} />`) y el hijo la llama.
- **Estado compartido**: "levantar el estado" al padre común, o `useContext` para cosas globales (usuario logueado, tema).

```jsx
const TemaContext = createContext("light");
<TemaContext.Provider value="dark"><App /></TemaContext.Provider>
const tema = useContext(TemaContext);
```

## 8. Otros hooks útiles

```jsx
const inputRef = useRef(null);  inputRef.current.focus();
const total = useMemo(() => items.reduce((s, i) => s + i.precio, 0), [items]);
```

## 9. Rutas (React Router)

```bash
npm i react-router-dom
```
```jsx
import { BrowserRouter, Routes, Route, Link, useParams, useNavigate } from "react-router-dom";

<BrowserRouter>
  <nav><Link to="/">Inicio</Link> <Link to="/productos">Productos</Link></nav>
  <Routes>
    <Route path="/" element={<Inicio />} />
    <Route path="/productos" element={<Productos />} />
    <Route path="/productos/:id" element={<Detalle />} />
    <Route path="*" element={<p>404</p>} />
  </Routes>
</BrowserRouter>

const { id } = useParams();
const navigate = useNavigate(); navigate("/productos");
```

## 10. Next.js (App Router) — lo mínimo

```
app/
  layout.js          ← layout común
  page.js            ← ruta "/"
  productos/page.js  ← ruta "/productos"
  productos/[id]/page.js ← ruta dinámica
  api/productos/route.js ← endpoint API
```

```jsx
// app/productos/page.js  (Server Component por defecto: puede hacer fetch directo)
export default async function Productos() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users", { cache: "no-store" });
  const data = await res.json();
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Si usas useState/useEffect/onClick → poner arriba del archivo:
"use client";

// app/api/productos/route.js
export async function GET() { return Response.json([{ id: 1 }]); }
export async function POST(req) { const body = await req.json(); return Response.json(body, { status: 201 }); }
```

Deploy en **Vercel**: subir a GitHub → vercel.com → "Add New Project" → importar repo → Deploy. Variables de entorno en Settings → Environment Variables.

## 11. Preguntas teóricas típicas

- **Virtual DOM**: copia en memoria del DOM; React compara (diff) y actualiza solo lo que cambió.
- **Props vs State**: props vienen del padre y son de solo lectura; state es interno y al cambiar re-renderiza.
- **¿Por qué key?**: para que React identifique qué elemento cambió en una lista.
- **SSR vs CSR**: Server Side Rendering (Next genera HTML en servidor, mejor SEO) vs Client Side (React normal, el navegador arma todo).
- **Componente controlado**: input cuyo valor lo maneja el estado de React.

---

# PARTE 2 — AMPLIACIÓN

> Proyecto de referencia: `02-proyectos/react-vite-crud/` y su versión con retos resueltos en `06-retos-resueltos/react-vite-crud/` (custom hook, filtro por categoría y React Router).

## 12. Cómo se ejecuta un proyecto React (y qué es cada archivo)

```bash
npm create vite@latest mi-app -- --template react
cd mi-app
npm install          # descarga dependencias a node_modules
npm run dev          # servidor de desarrollo con recarga en caliente → http://localhost:5173
npm run build        # genera /dist (HTML+JS+CSS optimizados para producción)
npm run preview      # sirve /dist localmente para probar el build
```
```
mi-app/
├── index.html          ← único HTML; tiene <div id="root"> y carga src/main.jsx
├── package.json
├── vite.config.js      ← configuración (plugins, proxy)
├── public/             ← archivos estáticos tal cual (favicon, imágenes)
└── src/
    ├── main.jsx        ← monta <App /> en #root
    ├── App.jsx         ← componente raíz
    ├── components/     ← componentes reutilizables
    ├── pages/          ← pantallas (si usas router)
    ├── hooks/          ← custom hooks (useAlgo)
    ├── services/api.js ← llamadas fetch
    └── index.css
```
React **no** corre con doble clic sobre index.html: necesita `npm run dev` (Vite transforma el JSX).

## 13. Ciclo de vida con useEffect

```jsx
useEffect(() => {
  // se ejecuta DESPUÉS de renderizar
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);        // limpieza: al desmontar o antes de re-ejecutar
}, [dependencia]);

// []            → solo al montar (cargar datos iniciales)
// [a, b]        → al montar y cada vez que cambie a o b
// sin arreglo   → después de CADA render (casi nunca lo quieres)
```
**Error clásico (bucle infinito):** hacer `setX` dentro de un useEffect que depende de `x`, o poner un objeto/función creado en cada render como dependencia.

**Cancelar un fetch** si el componente se desmonta o cambia la búsqueda:
```jsx
useEffect(() => {
  const ctrl = new AbortController();
  fetch(`/api/productos?q=${q}`, { signal: ctrl.signal })
    .then((r) => r.json()).then(setDatos)
    .catch((e) => { if (e.name !== "AbortError") setError(e.message); });
  return () => ctrl.abort();
}, [q]);
```

## 14. Custom hooks (reutilizar lógica)

```jsx
// hooks/useFetch.js
import { useEffect, useState, useCallback } from "react";
export function useFetch(url) {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  const recargar = useCallback(async () => {
    setCargando(true); setError(null);
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setDatos(await r.json());
    } catch (e) { setError(e.message); }
    finally { setCargando(false); }
  }, [url]);

  useEffect(() => { recargar(); }, [recargar]);
  return { datos, cargando, error, recargar };
}

// uso
const { datos: usuarios, cargando, error } = useFetch("https://jsonplaceholder.typicode.com/users");
```
```jsx
// hooks/useLocalStorage.js
export function useLocalStorage(clave, inicial) {
  const [valor, setValor] = useState(() => {
    try { return JSON.parse(localStorage.getItem(clave)) ?? inicial; } catch { return inicial; }
  });
  useEffect(() => { localStorage.setItem(clave, JSON.stringify(valor)); }, [clave, valor]);
  return [valor, setValor];
}
```

## 15. useReducer (estado complejo, estilo Redux)

```jsx
const inicial = { items: [], filtro: "" };
function reducer(estado, accion) {
  switch (accion.tipo) {
    case "agregar":  return { ...estado, items: [...estado.items, accion.item] };
    case "eliminar": return { ...estado, items: estado.items.filter((i) => i.id !== accion.id) };
    case "filtrar":  return { ...estado, filtro: accion.texto };
    default: throw new Error("Acción desconocida: " + accion.tipo);
  }
}
const [estado, dispatch] = useReducer(reducer, inicial);
dispatch({ tipo: "agregar", item: { id: 1, nombre: "Mouse" } });
```

## 16. Context completo (usuario logueado)

```jsx
// context/AuthContext.jsx
import { createContext, useContext, useState } from "react";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const login = async (email, clave) => {
    const r = await fetch("/api/login", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, clave }) });
    if (!r.ok) throw new Error("Credenciales incorrectas");
    setUsuario(await r.json());
  };
  const logout = () => setUsuario(null);
  return <AuthContext.Provider value={{ usuario, login, logout }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);

// main.jsx:  <AuthProvider><App /></AuthProvider>
// cualquier componente:  const { usuario, logout } = useAuth();
```

## 17. Router completo con rutas protegidas

```jsx
import { BrowserRouter, Routes, Route, Link, NavLink, Navigate, Outlet, useParams, useNavigate, useSearchParams } from "react-router-dom";

function RutaProtegida() {
  const { usuario } = useAuth();
  return usuario ? <Outlet /> : <Navigate to="/login" replace />;
}

function Layout() {
  return (<>
    <nav><NavLink to="/">Inicio</NavLink> <NavLink to="/productos">Productos</NavLink></nav>
    <main><Outlet /></main>          {/* aquí se pinta la página hija */}
  </>);
}

<BrowserRouter>
  <Routes>
    <Route element={<Layout />}>
      <Route path="/" element={<Inicio />} />
      <Route path="/login" element={<Login />} />
      <Route element={<RutaProtegida />}>
        <Route path="/productos" element={<Productos />} />
        <Route path="/productos/:id" element={<Detalle />} />
      </Route>
      <Route path="*" element={<NoEncontrado />} />
    </Route>
  </Routes>
</BrowserRouter>

// En Detalle:
const { id } = useParams();
const navigate = useNavigate();                // navigate("/productos") / navigate(-1)
const [params, setParams] = useSearchParams(); // ?q=mouse → params.get("q")
```

## 18. Formularios: validación y varios tipos de input

```jsx
const [form, setForm] = useState({ nombre: "", categoria: "pc", activo: true, nivel: "junior" });
const cambiar = (e) => {
  const { name, value, type, checked } = e.target;
  setForm((f) => ({ ...f, [name]: type === "checkbox" ? checked : value }));   // forma funcional
};

<input name="nombre" value={form.nombre} onChange={cambiar} />
<select name="categoria" value={form.categoria} onChange={cambiar}>
  <option value="pc">PC</option><option value="redes">Redes</option>
</select>
<input type="checkbox" name="activo" checked={form.activo} onChange={cambiar} />
{["junior", "senior"].map((n) => (
  <label key={n}><input type="radio" name="nivel" value={n} checked={form.nivel === n} onChange={cambiar} /> {n}</label>
))}
<textarea name="obs" value={form.obs ?? ""} onChange={cambiar} />
```
Librerías comunes: **react-hook-form** (formularios grandes) y **zod** (esquemas de validación).

## 19. Estilos en React

```jsx
import "./App.css";                                   // CSS global
import estilos from "./Boton.module.css";             // CSS Modules: <button className={estilos.primario}>
<div style={{ backgroundColor: "red", marginTop: 8 }}> // inline (objeto, camelCase)
<li className={`item ${activo ? "activo" : ""}`}>     // clases condicionales
```
Tailwind: `npm i -D tailwindcss @tailwindcss/vite` → plugin en vite.config → `@import "tailwindcss";` en index.css → `<div className="p-4 bg-blue-600 text-white rounded">`.

## 20. Rendimiento y buenas prácticas

- **Keys estables** (id de la BD), nunca el índice si la lista cambia de orden.
- `useMemo` para cálculos costosos; `useCallback` para funciones que pasas a hijos memorizados con `React.memo`.
- No guardes en el estado lo que puedes **calcular** (por ejemplo, el total del carrito se calcula de `items`).
- Levanta el estado solo hasta el ancestro común más cercano.
- Un componente = una responsabilidad. Si pasa de ~150 líneas, divídelo.
- Separa las llamadas HTTP en `services/api.js`.

## 21. Next.js ampliado (App Router)

```bash
npx create-next-app@latest mi-app      # elige App Router, sin src/ si prefieres
npm run dev                             # http://localhost:3000
```
```jsx
// app/layout.js: layout raíz (html, body, nav)
export const metadata = { title: "Mi App" };
export default function RootLayout({ children }) {
  return <html lang="es"><body><nav>...</nav>{children}</body></html>;
}

// app/productos/[id]/page.js: ruta dinámica, Server Component
export default async function Detalle({ params }) {
  const { id } = await params;                               // Next 15: params es una promesa
  const p = await obtenerProducto(id);                       // puede consultar la BD directamente
  if (!p) notFound();
  return <h1>{p.nombre}</h1>;
}

// Server Action: formulario sin API
// app/productos/nuevo/page.js
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
export default function Nuevo() {
  async function crear(formData) {
    "use server";
    await db.producto.create({ data: { nombre: formData.get("nombre") } });
    revalidatePath("/productos");
    redirect("/productos");
  }
  return <form action={crear}><input name="nombre" /><button>Guardar</button></form>;
}
```
Archivos especiales: `page.js` (página), `layout.js`, `loading.js` (mientras carga), `error.js` (errores, debe ser `"use client"`), `not-found.js`, `route.js` (API).

**Server vs Client Components:** por defecto todo es Server (se ejecuta en el servidor, puede leer la BD, no usa hooks). Con `"use client"` se ejecuta en el navegador (useState, onClick, useEffect).

## 22. Preguntas de entrevista React (respuestas cortas)

- **¿Qué provoca un re-render?** Que cambie el estado o las props, o que se re-renderice el padre.
- **¿Por qué no mutar el estado?** React compara referencias: si mutas el mismo array, no detecta el cambio.
- **¿Qué es JSX?** Sintaxis parecida a HTML que se compila a `React.createElement(...)`.
- **Componente controlado vs no controlado:** controlado = valor en el estado (`value` + `onChange`). No controlado = lo maneja el DOM (`useRef`).
- **¿Para qué sirve `key`?** Para identificar elementos de una lista entre renders.
- **Prop drilling:** pasar props por muchos niveles; se soluciona con Context o un gestor de estado (Zustand, Redux).
- **Hooks rules:** solo en el nivel superior del componente (no dentro de if/for) y solo en componentes o custom hooks.
- **SPA:** Single Page Application: una sola página HTML; el JS cambia el contenido sin recargar.
