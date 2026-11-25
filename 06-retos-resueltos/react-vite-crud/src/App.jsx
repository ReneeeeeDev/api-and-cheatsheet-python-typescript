// RETO 3: React Router. App solo define el layout y las rutas.
import { Link, NavLink, Route, Routes } from "react-router-dom";
import Inventario from "./pages/Inventario.jsx";
import DetalleProducto from "./pages/DetalleProducto.jsx";

export default function App() {
  return (
    <>
      <header className="barra">
        <h1><Link to="/" className="logo">Inventario (React)</Link></h1>
        <nav><NavLink to="/" end>Productos</NavLink></nav>
      </header>
      <main className="contenedor">
        <Routes>
          <Route path="/" element={<Inventario />} />
          <Route path="/productos/:id" element={<DetalleProducto />} />
          <Route path="*" element={<section className="panel"><h2>404</h2><p>Página no encontrada. <Link to="/">Volver</Link></p></section>} />
        </Routes>
      </main>
    </>
  );
}
