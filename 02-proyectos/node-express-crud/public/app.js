// Frontend en JavaScript puro (sin framework): fetch + DOM.
const API = "/api/productos";
const $ = (sel) => document.querySelector(sel);
const form = $("#form");
let temporizador;

const dinero = (n) => `$${Number(n).toFixed(2)}`;

// Escapa texto para evitar XSS al usar innerHTML
const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function aviso(msg, tipo = "ok") {
  const t = $("#toast");
  t.textContent = msg;
  t.className = `toast ${tipo}`;
  t.hidden = false;
  clearTimeout(temporizador);
  temporizador = setTimeout(() => (t.hidden = true), 2500);
}

async function pedir(url, opciones = {}) {
  const res = await fetch(url, { headers: { "Content-Type": "application/json" }, ...opciones });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

async function cargar() {
  const params = new URLSearchParams({ q: $("#buscar").value, orden: $("#orden").value });
  const [productos, resumen] = await Promise.all([pedir(`${API}?${params}`), pedir(`${API}/resumen`)]);

  $("#tabla").innerHTML = productos.length
    ? productos.map((p) => `
      <tr class="${p.stock < 5 ? "bajo" : ""}">
        <td>${p.id}</td><td>${esc(p.nombre)}</td><td>${esc(p.categoria)}</td>
        <td>${dinero(p.precio)}</td><td>${p.stock}</td>
        <td class="acciones">
          <button class="sec" data-editar="${p.id}">Editar</button>
          <button class="peligro" data-eliminar="${p.id}">Eliminar</button>
        </td>
      </tr>`).join("")
    : `<tr><td colspan="6">Sin resultados</td></tr>`;

  $("#resumen").innerHTML = `
    <div class="tarjeta"><span>Productos</span><strong>${resumen.totalProductos}</strong></div>
    <div class="tarjeta"><span>Unidades</span><strong>${resumen.unidades}</strong></div>
    <div class="tarjeta"><span>Valor inventario</span><strong>${dinero(resumen.valorInventario)}</strong></div>
    <div class="tarjeta"><span>Stock bajo</span><strong>${resumen.stockBajo.length}</strong></div>`;

  const categorias = [...new Set(productos.map((p) => p.categoria))];
  $("#categorias").innerHTML = categorias.map((c) => `<option value="${esc(c)}">`).join("");
}

function limpiarForm() {
  form.reset();
  form.id.value = "";
  $("#titulo-form").textContent = "Nuevo producto";
  $("#cancelar").hidden = true;
  $("#errores").innerHTML = "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const datos = Object.fromEntries(new FormData(form));
  const id = datos.id;
  delete datos.id;
  try {
    await pedir(id ? `${API}/${id}` : API, { method: id ? "PUT" : "POST", body: JSON.stringify(datos) });
    aviso(id ? "Producto actualizado" : "Producto creado");
    limpiarForm();
    cargar();
  } catch (err) {
    $("#errores").innerHTML = (err.errores || [err.error || "Error"]).map((m) => `<li>${esc(m)}</li>`).join("");
  }
});

// Delegación de eventos: un solo listener para todos los botones de la tabla
$("#tabla").addEventListener("click", async (e) => {
  const { editar, eliminar } = e.target.dataset;
  if (editar) {
    const p = await pedir(`${API}/${editar}`);
    for (const campo of ["id", "nombre", "categoria", "precio", "stock"]) form[campo].value = p[campo];
    $("#titulo-form").textContent = `Editar #${p.id}`;
    $("#cancelar").hidden = false;
    form.nombre.focus();
  }
  if (eliminar && confirm("¿Eliminar este producto?")) {
    await pedir(`${API}/${eliminar}`, { method: "DELETE" });
    aviso("Producto eliminado", "error");
    cargar();
  }
});

$("#cancelar").addEventListener("click", limpiarForm);
$("#orden").addEventListener("change", cargar);
// Debounce: espera 300ms después de teclear antes de buscar
let espera;
$("#buscar").addEventListener("input", () => { clearTimeout(espera); espera = setTimeout(cargar, 300); });

cargar();
