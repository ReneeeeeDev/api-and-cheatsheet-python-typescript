// Frontend en JavaScript puro con los 3 retos: login con token, activar/desactivar y paginación.
const API = "/api/productos";
const $ = (sel) => document.querySelector(sel);
const form = $("#form");
let pagina = 1;
const LIMITE = 5;
let temporizador;

// ------------------------------------------------------------ SESIÓN (RETO 3)
// sessionStorage: el token dura mientras la pestaña esté abierta
const leerToken = () => { try { return sessionStorage.getItem("token"); } catch { return null; } };
const guardarToken = (t) => { try { t ? sessionStorage.setItem("token", t) : sessionStorage.removeItem("token"); } catch {} };

function pintarSesion() {
  const logueado = Boolean(leerToken());
  $("#panel-login").hidden = logueado;
  $("#panel-form").hidden = !logueado;
  $("#sesion").innerHTML = logueado ? `admin · <button class="sec" id="salir">Salir</button>` : "Invitado (solo lectura)";
  if (logueado) $("#salir").onclick = salir;
}

$("#form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const { token } = await pedir("/api/login", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(e.target))) });
    guardarToken(token);
    e.target.reset();
    $("#error-login").textContent = "";
    pintarSesion(); cargar();
  } catch (err) {
    $("#error-login").textContent = err.error || "Error";
  }
});

async function salir() {
  await pedir("/api/logout", { method: "POST" }).catch(() => {});
  guardarToken(null);
  pintarSesion(); cargar();
}

// ------------------------------------------------------------ UTILIDADES
const dinero = (n) => `$${Number(n).toFixed(2)}`;
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function aviso(msg, tipo = "ok") {
  const t = $("#toast");
  t.textContent = msg; t.className = `toast ${tipo}`; t.hidden = false;
  clearTimeout(temporizador);
  temporizador = setTimeout(() => (t.hidden = true), 2500);
}

// Todas las peticiones pasan por aquí: agrega el token y maneja 401
async function pedir(url, opciones = {}) {
  const token = leerToken();
  const res = await fetch(url, {
    ...opciones,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
  });
  if (res.status === 401 && token) { guardarToken(null); pintarSesion(); }
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

// ------------------------------------------------------------ LISTADO (RETO 1 y 2)
async function cargar() {
  const params = new URLSearchParams({
    q: $("#buscar").value, orden: $("#orden").value, activo: $("#filtro-activo").value, pagina, limite: LIMITE,
  });
  const [resp, resumen] = await Promise.all([pedir(`${API}?${params}`), pedir(`${API}/resumen`)]);
  pagina = resp.pagina;
  const logueado = Boolean(leerToken());

  $("#tabla").innerHTML = resp.datos.length
    ? resp.datos.map((p) => `
      <tr class="${p.activo === false ? "inactivo" : ""}">
        <td>${p.id}</td><td>${esc(p.nombre)}</td><td>${esc(p.categoria)}</td>
        <td>${dinero(p.precio)}</td><td>${p.stock}</td>
        <td><span class="estado ${p.activo === false ? "off" : "on"}">${p.activo === false ? "Inactivo" : "Activo"}</span></td>
        <td class="acciones">${logueado ? `
          <button class="sec" data-estado="${p.id}" data-activo="${p.activo !== false}">${p.activo === false ? "Activar" : "Desactivar"}</button>
          <button class="sec" data-editar="${p.id}">Editar</button>
          <button class="peligro" data-eliminar="${p.id}">Eliminar</button>` : ""}
        </td>
      </tr>`).join("")
    : `<tr><td colspan="7">Sin resultados</td></tr>`;

  $("#info-pagina").textContent = `Página ${resp.pagina} de ${resp.paginas} (${resp.total} productos)`;
  $("#anterior").disabled = resp.pagina <= 1;
  $("#siguiente").disabled = resp.pagina >= resp.paginas;

  $("#resumen").innerHTML = `
    <div class="tarjeta"><span>Productos</span><strong>${resumen.totalProductos}</strong></div>
    <div class="tarjeta"><span>Unidades</span><strong>${resumen.unidades}</strong></div>
    <div class="tarjeta"><span>Valor inventario</span><strong>${dinero(resumen.valorInventario)}</strong></div>
    <div class="tarjeta"><span>Inactivos</span><strong>${resumen.inactivos}</strong></div>`;
}

function limpiarForm() {
  form.reset(); form.id.value = "";
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
    limpiarForm(); cargar();
  } catch (err) {
    $("#errores").innerHTML = (err.errores || [err.error || "Error"]).map((m) => `<li>${esc(m)}</li>`).join("");
  }
});

$("#tabla").addEventListener("click", async (e) => {
  const { editar, eliminar, estado, activo } = e.target.dataset;
  try {
    if (estado) {
      await pedir(`${API}/${estado}/estado`, { method: "PATCH", body: JSON.stringify({ activo: activo !== "true" }) });
      aviso(activo === "true" ? "Producto desactivado" : "Producto activado");
      cargar();
    }
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
  } catch (err) {
    aviso(err.error || "Error", "error");
  }
});

$("#anterior").addEventListener("click", () => { pagina--; cargar(); });
$("#siguiente").addEventListener("click", () => { pagina++; cargar(); });
$("#cancelar").addEventListener("click", limpiarForm);
$("#orden").addEventListener("change", () => { pagina = 1; cargar(); });
$("#filtro-activo").addEventListener("change", () => { pagina = 1; cargar(); });
let espera;
$("#buscar").addEventListener("input", () => { clearTimeout(espera); espera = setTimeout(() => { pagina = 1; cargar(); }, 300); });

pintarSesion();
cargar();
