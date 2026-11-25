"""
PLANTILLA MÍNIMA para memorizar: CRUD completo en UN archivo (Flask + SQLite).
Escribirla de memoria en ~20 minutos te da una base para cualquier enunciado.
pip install flask && python flask_un_archivo.py
"""
import sqlite3
from flask import Flask, request, redirect, render_template_string, g

app = Flask(__name__)
DB = "datos.db"

HTML = """
<!doctype html><html lang="es"><head><meta charset="utf-8"><title>CRUD</title>
<style>body{font-family:sans-serif;max-width:800px;margin:auto}td,th{padding:6px;border-bottom:1px solid #ddd}
.error{color:#c00}</style></head><body>
<h1>Items</h1>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="post" action="{{ '/editar/%d' % item.id if item else '/crear' }}">
  <input name="nombre" placeholder="Nombre" value="{{ item.nombre if item else '' }}" required>
  <input name="cantidad" type="number" min="0" value="{{ item.cantidad if item else 0 }}">
  <button>{{ 'Actualizar' if item else 'Crear' }}</button>
</form>
<table><tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th></th></tr>
{% for i in items %}
<tr><td>{{ i.id }}</td><td>{{ i.nombre }}</td><td>{{ i.cantidad }}</td>
<td><a href="/editar/{{ i.id }}">Editar</a>
<form method="post" action="/eliminar/{{ i.id }}" style="display:inline"><button>Eliminar</button></form></td></tr>
{% endfor %}</table></body></html>
"""


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar(_):
    if "db" in g:
        g.db.close()


def validar(f):
    if len(f.get("nombre", "").strip()) < 2:
        return "Nombre muy corto"
    if not f.get("cantidad", "0").isdigit():
        return "Cantidad inválida"
    return None


def pagina(item=None, error=None):
    items = db().execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    return render_template_string(HTML, items=items, item=item, error=error)


@app.get("/")
def index():
    return pagina()


@app.post("/crear")
def crear():
    if err := validar(request.form):
        return pagina(error=err), 400
    db().execute("INSERT INTO items (nombre, cantidad) VALUES (?, ?)",
                 (request.form["nombre"].strip(), int(request.form["cantidad"])))
    db().commit()
    return redirect("/")


@app.route("/editar/<int:id_>", methods=["GET", "POST"])
def editar(id_):
    item = db().execute("SELECT * FROM items WHERE id = ?", (id_,)).fetchone()
    if not item:
        return redirect("/")
    if request.method == "POST":
        if err := validar(request.form):
            return pagina(item, err), 400
        db().execute("UPDATE items SET nombre = ?, cantidad = ? WHERE id = ?",
                     (request.form["nombre"].strip(), int(request.form["cantidad"]), id_))
        db().commit()
        return redirect("/")
    return pagina(item)


@app.post("/eliminar/<int:id_>")
def eliminar(id_):
    db().execute("DELETE FROM items WHERE id = ?", (id_,))
    db().commit()
    return redirect("/")


with app.app_context():
    db().execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "nombre TEXT NOT NULL, cantidad INTEGER NOT NULL DEFAULT 0)")
    db().commit()

if __name__ == "__main__":
    app.run(debug=True)
