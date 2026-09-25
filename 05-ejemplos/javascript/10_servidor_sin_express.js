// 10 - Servidor web + API REST SIN Express (solo módulo http de Node).
// Plan de emergencia si no hay internet para npm install. También sirve para entender qué hace Express por dentro.
// Ejecutar:  node 10_servidor_sin_express.js   →  http://localhost:8001
const http = require("http");

let tareas = [{ id: 1, titulo: "Repasar SQL", hecha: false }];
let nextId = 2;

const PAGINA = `<!doctype html><html lang="es"><meta charset="utf-8"><title>Tareas</title>
<body style="font-family:sans-serif;max-width:600px;margin:auto">
<h1>Tareas (Node sin Express)</h1>
<form id="f"><input name="titulo" required><button>Agregar</button></form><ul id="lista"></ul>
<script>
async function cargar() {
  const ts = await (await fetch('/api/tareas')).json();
  lista.innerHTML = '';
  for (const t of ts) {
    const li = document.createElement('li');
    const chk = document.createElement('input'); chk.type = 'checkbox'; chk.checked = t.hecha;
    chk.onchange = async () => { await fetch('/api/tareas/' + t.id, {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({hecha: chk.checked})}); };
    const del = document.createElement('button'); del.textContent = 'x';
    del.onclick = async () => { await fetch('/api/tareas/' + t.id, {method:'DELETE'}); cargar(); };
    li.append(chk, ' ' + t.titulo + ' ', del); lista.append(li);
  }
}
f.onsubmit = async e => { e.preventDefault();
  await fetch('/api/tareas', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({titulo: f.titulo.value})});
  f.reset(); cargar(); };
cargar();
</script></body></html>`;

function enviarJSON(res, codigo, datos) {
  res.writeHead(codigo, { "Content-Type": "application/json; charset=utf-8" });
  res.end(datos === undefined ? "" : JSON.stringify(datos));
}

function leerCuerpo(req) {
  return new Promise((resolve, reject) => {
    let cuerpo = "";
    req.on("data", (trozo) => (cuerpo += trozo));
    req.on("end", () => { try { resolve(cuerpo ? JSON.parse(cuerpo) : {}); } catch (e) { reject(e); } });
  });
}

const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const partes = url.pathname.split("/").filter(Boolean);        // "/api/tareas/2" → ["api","tareas","2"]
  console.log(req.method, url.pathname);

  try {
    if (req.method === "GET" && url.pathname === "/") {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      return res.end(PAGINA);
    }
    if (partes[0] !== "api" || partes[1] !== "tareas") return enviarJSON(res, 404, { error: "No encontrado" });
    const id = partes[2] ? Number(partes[2]) : null;

    if (req.method === "GET" && !id) {
      const q = (url.searchParams.get("q") || "").toLowerCase();
      return enviarJSON(res, 200, tareas.filter((t) => t.titulo.toLowerCase().includes(q)));
    }
    if (req.method === "POST" && !id) {
      const { titulo } = await leerCuerpo(req);
      if (!titulo?.trim()) return enviarJSON(res, 400, { error: "El título es obligatorio" });
      const tarea = { id: nextId++, titulo: titulo.trim(), hecha: false };
      tareas.push(tarea);
      return enviarJSON(res, 201, tarea);
    }
    const tarea = tareas.find((t) => t.id === id);
    if (!tarea) return enviarJSON(res, 404, { error: "Tarea no encontrada" });
    if (req.method === "PUT") {
      Object.assign(tarea, await leerCuerpo(req), { id });
      return enviarJSON(res, 200, tarea);
    }
    if (req.method === "DELETE") {
      tareas = tareas.filter((t) => t.id !== id);
      return enviarJSON(res, 204);
    }
    enviarJSON(res, 405, { error: "Método no permitido" });
  } catch (e) {
    enviarJSON(res, 400, { error: "JSON inválido" });
  }
});

const PUERTO = process.env.PORT || 8001;
servidor.listen(PUERTO, () => console.log(`Servidor en http://localhost:${PUERTO}`));
