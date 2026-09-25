"""10 - Servidor web + API JSON SIN instalar nada (solo biblioteca estándar).
Plan de emergencia si en el laboratorio no hay internet para pip install.
Ejecutar:  python 10_servidor_sin_flask.py   →  http://localhost:8000
Probar:    GET  http://localhost:8000/api/tareas
           POST http://localhost:8000/api/tareas   body JSON {"titulo": "Estudiar"}
           DELETE http://localhost:8000/api/tareas/1
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

tareas = [{"id": 1, "titulo": "Repasar SQL", "hecha": False}]
siguiente_id = 2

PAGINA = """<!doctype html><html lang="es"><meta charset="utf-8"><title>Tareas</title>
<body style="font-family:sans-serif;max-width:600px;margin:auto">
<h1>Tareas (servidor sin Flask)</h1>
<form id="f"><input name="titulo" placeholder="Nueva tarea" required><button>Agregar</button></form>
<ul id="lista"></ul>
<script>
async function cargar() {
  const tareas = await (await fetch('/api/tareas')).json();
  lista.innerHTML = '';
  tareas.forEach(t => {
    const li = document.createElement('li');
    li.textContent = t.titulo + ' ';
    const b = document.createElement('button'); b.textContent = 'x';
    b.onclick = async () => { await fetch('/api/tareas/' + t.id, {method: 'DELETE'}); cargar(); };
    li.append(b); lista.append(li);
  });
}
f.onsubmit = async e => {
  e.preventDefault();
  await fetch('/api/tareas', {method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({titulo: f.titulo.value})});
  f.reset(); cargar();
};
cargar();
</script></body></html>"""


class Manejador(BaseHTTPRequestHandler):
    def responder(self, codigo, cuerpo=None, tipo="application/json"):
        datos = b"" if cuerpo is None else (cuerpo if isinstance(cuerpo, bytes) else
                                           json.dumps(cuerpo, ensure_ascii=False).encode())
        self.send_response(codigo)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        if self.path == "/":
            self.responder(200, PAGINA.encode(), "text/html")
        elif self.path == "/api/tareas":
            self.responder(200, tareas)
        else:
            self.responder(404, {"error": "No encontrado"})

    def do_POST(self):
        global siguiente_id
        if self.path != "/api/tareas":
            return self.responder(404, {"error": "No encontrado"})
        largo = int(self.headers.get("Content-Length", 0))
        try:
            datos = json.loads(self.rfile.read(largo) or b"{}")
        except json.JSONDecodeError:
            return self.responder(400, {"error": "JSON inválido"})
        titulo = str(datos.get("titulo", "")).strip()
        if not titulo:
            return self.responder(400, {"error": "El título es obligatorio"})
        tarea = {"id": siguiente_id, "titulo": titulo, "hecha": False}
        siguiente_id += 1
        tareas.append(tarea)
        self.responder(201, tarea)

    def do_DELETE(self):
        partes = self.path.strip("/").split("/")
        if len(partes) == 3 and partes[:2] == ["api", "tareas"] and partes[2].isdigit():
            id_ = int(partes[2])
            antes = len(tareas)
            tareas[:] = [t for t in tareas if t["id"] != id_]
            return self.responder(204 if len(tareas) < antes else 404)
        self.responder(404, {"error": "No encontrado"})


if __name__ == "__main__":
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Servidor en http://localhost:{puerto}  (Ctrl + C para detener)")
    HTTPServer(("", puerto), Manejador).serve_forever()
