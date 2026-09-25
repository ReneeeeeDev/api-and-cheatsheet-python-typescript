// Validación separada para poder probarla sola (prueba unitaria).
export function validarProducto(body, { parcial = false } = {}) {
  const errores = [];
  const datos = {};

  if (!parcial || body.nombre !== undefined) {
    const nombre = String(body.nombre ?? "").trim();
    if (nombre.length < 3) errores.push("El nombre debe tener al menos 3 caracteres");
    else datos.nombre = nombre;
  }
  if (!parcial || body.categoria !== undefined) {
    const categoria = String(body.categoria ?? "").trim();
    if (!categoria) errores.push("La categoría es obligatoria");
    else datos.categoria = categoria;
  }
  if (!parcial || body.precio !== undefined) {
    const precio = Number(body.precio);
    if (body.precio === "" || body.precio == null || Number.isNaN(precio) || precio <= 0)
      errores.push("El precio debe ser un número mayor a 0");
    else datos.precio = Math.round(precio * 100) / 100;
  }
  if (!parcial || body.stock !== undefined) {
    const stock = Number(body.stock ?? 0);
    if (!Number.isInteger(stock) || stock < 0) errores.push("El stock debe ser un entero >= 0");
    else datos.stock = stock;
  }
  return { errores, datos };
}
