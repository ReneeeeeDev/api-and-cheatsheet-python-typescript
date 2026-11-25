// Todas las llamadas HTTP en un solo lugar.
const BASE = "/api/productos";

async function pedir(url, opciones = {}) {
  const res = await fetch(url, { headers: { "Content-Type": "application/json" }, ...opciones });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error((data.errores || [data.error]).join(". "));
  return data;
}

export const api = {
  // RETO 1: filtro por categoría (el backend ya acepta ?categoria=)
  listar: ({ q = "", orden = "id", categoria = "" } = {}) =>
    pedir(`${BASE}?${new URLSearchParams({ q, orden, categoria })}`),
  obtener: (id) => pedir(`${BASE}/${id}`),            // RETO 3: para la página de detalle
  resumen: () => pedir(`${BASE}/resumen`),
  crear: (p) => pedir(BASE, { method: "POST", body: JSON.stringify(p) }),
  actualizar: (id, p) => pedir(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(p) }),
  eliminar: (id) => pedir(`${BASE}/${id}`, { method: "DELETE" }),
};
