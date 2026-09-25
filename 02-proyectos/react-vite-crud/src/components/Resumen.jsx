export default function Resumen({ datos }) {
  if (!datos) return null;
  const tarjetas = [
    ["Productos", datos.totalProductos],
    ["Unidades", datos.unidades],
    ["Valor inventario", `$${datos.valorInventario.toFixed(2)}`],
    ["Stock bajo", datos.stockBajo.length],
  ];
  return (
    <section className="tarjetas">
      {tarjetas.map(([titulo, valor]) => (
        <div className="tarjeta" key={titulo}>
          <span>{titulo}</span>
          <strong>{valor}</strong>
        </div>
      ))}
    </section>
  );
}
