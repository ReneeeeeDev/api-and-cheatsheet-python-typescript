// Todas las llamadas HTTP en un solo lugar (fácil de cambiar la URL o agregar tokens).
const BASE = "/api/productos";

async function pedir(url, opciones = {}) {
  const res = await fetch(url, { headers: { "Content-Type": "application/json" }, ...opciones });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error((data.errores || [data.error]).join(". "));
  return data;
}

export const api = {
  listar: (q = "", orden = "id") => pedir(`${BASE}?${new URLSearchParams({ q, orden })}`),
  resumen: () => pedir(`${BASE}/resumen`),
  crear: (p) => pedir(BASE, { method: "POST", body: JSON.stringify(p) }),
  actualizar: (id, p) => pedir(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(p) }),
  eliminar: (id) => pedir(`${BASE}/${id}`, { method: "DELETE" }),
};
