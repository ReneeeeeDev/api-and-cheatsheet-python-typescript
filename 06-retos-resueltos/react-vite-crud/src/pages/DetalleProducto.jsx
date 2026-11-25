// RETO 3: página de detalle en /productos/:id
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api.js";

export default function DetalleProducto() {
  const { id } = useParams();                 // lee el :id de la URL
  const navigate = useNavigate();
  const [producto, setProducto] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let activo = true;                        // evita actualizar el estado si el usuario ya salió de la página
    setProducto(null); setError("");
    api.obtener(id)
      .then((p) => activo && setProducto(p))
      .catch((e) => activo && setError(e.message));
    return () => { activo = false; };
  }, [id]);

  if (error) return <section className="panel"><h2>Error</h2><p>{error}</p><Link to="/">Volver</Link></section>;
  if (!producto) return <p>Cargando...</p>;

  const valor = producto.precio * producto.stock;
  return (
    <section className="panel detalle">
      <h2>{producto.nombre}</h2>
      <dl>
        <dt>ID</dt><dd>{producto.id}</dd>
        <dt>Categoría</dt><dd>{producto.categoria}</dd>
        <dt>Precio</dt><dd>${producto.precio.toFixed(2)}</dd>
        <dt>Stock</dt><dd className={producto.stock < 5 ? "bajo" : ""}>{producto.stock}{producto.stock < 5 && " (stock bajo)"}</dd>
        <dt>Valor en inventario</dt><dd>${valor.toFixed(2)}</dd>
      </dl>
      <div className="acciones">
        <button className="sec" onClick={() => navigate(-1)}>← Atrás</button>
        <Link className="btn" to={`/productos/${Number(id) + 1}`}>Siguiente →</Link>
      </div>
    </section>
  );
}
