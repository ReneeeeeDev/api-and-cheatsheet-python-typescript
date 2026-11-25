// PLANTILLA MÍNIMA para memorizar: API CRUD + página HTML en UN archivo (Express).
// npm init -y && npm i express && node express_un_archivo.js
const express = require("express");
const app = express();
app.use(express.json());

let items = [{ id: 1, nombre: "Ejemplo", cantidad: 5 }];
let nextId = 2;

function validar(b) {
  if (!b.nombre || String(b.nombre).trim().length < 2) return "Nombre muy corto";
  if (!Number.isInteger(Number(b.cantidad)) || Number(b.cantidad) < 0) return "Cantidad inválida";
  return null;
}

app.get("/api/items", (req, res) => res.json(items));

app.post("/api/items", (req, res) => {
  const err = validar(req.body);
  if (err) return res.status(400).json({ error: err });
  const item = { id: nextId++, nombre: req.body.nombre.trim(), cantidad: Number(req.body.cantidad) };
  items.push(item);
  res.status(201).json(item);
});

app.put("/api/items/:id", (req, res) => {
  const item = items.find((i) => i.id === Number(req.params.id));
  if (!item) return res.status(404).json({ error: "No encontrado" });
  const err = validar(req.body);
  if (err) return res.status(400).json({ error: err });
  Object.assign(item, { nombre: req.body.nombre.trim(), cantidad: Number(req.body.cantidad) });
  res.json(item);
});

app.delete("/api/items/:id", (req, res) => {
  const antes = items.length;
  items = items.filter((i) => i.id !== Number(req.params.id));
  res.status(items.length < antes ? 204 : 404).end();
});

// Frontend mínimo embebido
app.get("/", (req, res) => res.send(`<!doctype html><html lang="es"><meta charset="utf-8"><title>CRUD</title>
<body style="font-family:sans-serif;max-width:700px;margin:auto">
<h1>Items</h1>
<form id="f"><input type="hidden" name="id"><input name="nombre" placeholder="Nombre" required>
<input name="cantidad" type="number" min="0" value="0"><button>Guardar</button></form>
<p id="error" style="color:#c00"></p><ul id="lista"></ul>
<script>
const f = document.getElementById("f");
async function cargar() {
  const items = await (await fetch("/api/items")).json();
  lista.innerHTML = "";
  for (const i of items) {
    const li = document.createElement("li");
    li.textContent = i.nombre + " (" + i.cantidad + ") ";
    const ed = document.createElement("button"); ed.textContent = "Editar";
    ed.onclick = () => { f.id.value = i.id; f.nombre.value = i.nombre; f.cantidad.value = i.cantidad; };
    const del = document.createElement("button"); del.textContent = "Eliminar";
    del.onclick = async () => { await fetch("/api/items/" + i.id, { method: "DELETE" }); cargar(); };
    li.append(ed, del); lista.append(li);
  }
}
f.onsubmit = async (e) => {
  e.preventDefault();
  const d = Object.fromEntries(new FormData(f));
  const res = await fetch(d.id ? "/api/items/" + d.id : "/api/items", {
    method: d.id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) });
  error.textContent = res.ok ? "" : (await res.json()).error;
  if (res.ok) { f.reset(); f.id.value = ""; cargar(); }
};
cargar();
</script></body></html>`));

app.listen(3000, () => console.log("http://localhost:3000"));
