export default function ProductoTabla({ productos, onEditar, onEliminar }) {
  if (productos.length === 0) return <p>No hay productos.</p>;

  return (
    <table>
      <thead>
        <tr><th>ID</th><th>Nombre</th><th>Categoría</th><th>Precio</th><th>Stock</th><th></th></tr>
      </thead>
      <tbody>
        {productos.map((p) => (
          <tr key={p.id}>
            <td>{p.id}</td>
            <td>{p.nombre}</td>
            <td>{p.categoria}</td>
            <td>${p.precio.toFixed(2)}</td>
            <td className={p.stock < 5 ? "bajo" : ""}>{p.stock}</td>
            <td className="acciones">
              <button className="sec" onClick={() => onEditar(p)}>Editar</button>
              <button className="peligro" onClick={() => onEliminar(p)}>Eliminar</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
