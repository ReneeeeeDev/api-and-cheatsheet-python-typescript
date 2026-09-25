import { useCallback, useEffect, useState } from "react";
import { api } from "./api.js";
import ProductoForm from "./components/ProductoForm.jsx";
import ProductoTabla from "./components/ProductoTabla.jsx";
import Resumen from "./components/Resumen.jsx";

export default function App() {
  const [productos, setProductos] = useState([]);
  const [resumen, setResumen] = useState(null);
  const [editando, setEditando] = useState(null);     // producto seleccionado o null
  const [busqueda, setBusqueda] = useState("");
  const [orden, setOrden] = useState("id");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");

  const cargar = useCallback(async () => {
    try {
      setError("");
      const [lista, res] = await Promise.all([api.listar(busqueda, orden), api.resumen()]);
      setProductos(lista);
      setResumen(res);
    } catch (e) {
      setError("No se pudo conectar con la API. ¿Está corriendo el backend en el puerto 3000?");
    } finally {
      setCargando(false);
    }
  }, [busqueda, orden]);

  // Recarga cuando cambia la búsqueda u orden (con debounce de 300 ms)
  useEffect(() => {
    const t = setTimeout(cargar, 300);
    return () => clearTimeout(t);            // limpieza: cancela si el usuario sigue escribiendo
  }, [cargar]);

  // El mensaje de éxito desaparece solo
  useEffect(() => {
    if (!mensaje) return;
    const t = setTimeout(() => setMensaje(""), 2500);
    return () => clearTimeout(t);
  }, [mensaje]);

  async function guardar(datos) {
    if (editando) {
      await api.actualizar(editando.id, datos);
      setMensaje("Producto actualizado");
    } else {
      await api.crear(datos);
      setMensaje("Producto creado");
    }
    setEditando(null);
    cargar();
  }

  async function eliminar(p) {
    if (!confirm(`¿Eliminar "${p.nombre}"?`)) return;
    await api.eliminar(p.id);
    setMensaje("Producto eliminado");
    if (editando?.id === p.id) setEditando(null);
    cargar();
  }

  return (
    <>
      <header className="barra"><h1>Inventario (React)</h1></header>
      <main className="contenedor">
        {error && <div className="alerta error">{error}</div>}
        {mensaje && <div className="alerta ok">{mensaje}</div>}

        <Resumen datos={resumen} />

        <section className="panel">
          <h2>{editando ? `Editar #${editando.id}` : "Nuevo producto"}</h2>
          {/* key fuerza a reiniciar el formulario al cambiar de producto */}
          <ProductoForm
            key={editando?.id ?? "nuevo"}
            inicial={editando}
            onGuardar={guardar}
            onCancelar={() => setEditando(null)}
          />
        </section>

        <section className="panel">
          <div className="filtros">
            <input value={busqueda} onChange={(e) => setBusqueda(e.target.value)} placeholder="Buscar..." />
            <select value={orden} onChange={(e) => setOrden(e.target.value)}>
              <option value="id">Orden: ID</option>
              <option value="nombre">Nombre</option>
              <option value="precio">Precio</option>
              <option value="stock">Stock</option>
            </select>
          </div>
          {cargando ? <p>Cargando...</p> : (
            <ProductoTabla productos={productos} onEditar={setEditando} onEliminar={eliminar} />
          )}
        </section>
      </main>
    </>
  );
}
