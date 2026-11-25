import { useEffect, useState } from "react";
import { useProductos } from "../hooks/useProductos.js";
import ProductoForm from "../components/ProductoForm.jsx";
import ProductoTabla from "../components/ProductoTabla.jsx";
import Resumen from "../components/Resumen.jsx";

export default function Inventario() {
  // Toda la lógica de datos viene del custom hook (RETO 2)
  const { productos, resumen, categorias, filtros, cambiarFiltro, cargando, error, guardar, eliminar } = useProductos();
  const [editando, setEditando] = useState(null);
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    if (!mensaje) return;
    const t = setTimeout(() => setMensaje(""), 2500);
    return () => clearTimeout(t);
  }, [mensaje]);

  async function onGuardar(datos) {
    await guardar(datos, editando?.id);
    setMensaje(editando ? "Producto actualizado" : "Producto creado");
    setEditando(null);
  }

  async function onEliminar(p) {
    if (!confirm(`¿Eliminar "${p.nombre}"?`)) return;
    await eliminar(p.id);
    setMensaje("Producto eliminado");
    if (editando?.id === p.id) setEditando(null);
  }

  return (
    <>
      {error && <div className="alerta error">{error}</div>}
      {mensaje && <div className="alerta ok">{mensaje}</div>}
      <Resumen datos={resumen} />

      <section className="panel">
        <h2>{editando ? `Editar #${editando.id}` : "Nuevo producto"}</h2>
        <ProductoForm key={editando?.id ?? "nuevo"} inicial={editando} categorias={categorias}
                      onGuardar={onGuardar} onCancelar={() => setEditando(null)} />
      </section>

      <section className="panel">
        <div className="filtros">
          <input value={filtros.q} onChange={(e) => cambiarFiltro("q", e.target.value)} placeholder="Buscar..." />
          {/* RETO 1: filtro por categoría generado a partir de los productos */}
          <select value={filtros.categoria} onChange={(e) => cambiarFiltro("categoria", e.target.value)} aria-label="Categoría">
            <option value="">Todas las categorías</option>
            {categorias.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={filtros.orden} onChange={(e) => cambiarFiltro("orden", e.target.value)} aria-label="Orden">
            <option value="id">Orden: ID</option>
            <option value="nombre">Nombre</option>
            <option value="precio">Precio</option>
            <option value="stock">Stock</option>
          </select>
        </div>
        {cargando ? <p>Cargando...</p> : <ProductoTabla productos={productos} onEditar={setEditando} onEliminar={onEliminar} />}
      </section>
    </>
  );
}
