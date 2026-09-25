# Cheatsheet Python (para prueba práctica)

## 1. Sintaxis esencial

```python
# Variables y tipos
nombre = "Ana"          # str
edad = 25               # int
nota = 8.5              # float
activo = True           # bool
nada = None

# f-strings (lo más usado)
print(f"Hola {nombre}, tienes {edad} años y nota {nota:.2f}")

# Conversión
int("10"), float("3.5"), str(10), bool(0)   # 10, 3.5, "10", False

# Entrada por consola
n = int(input("Número: "))
```

## 2. Estructuras de control

```python
if edad >= 18 and activo:
    print("Mayor")
elif edad >= 12:
    print("Adolescente")
else:
    print("Niño")

for i in range(5):          # 0..4
    print(i)
for i in range(10, 0, -2):  # 10,8,6,4,2
    print(i)
for i, valor in enumerate(["a", "b"]):
    print(i, valor)

while n > 0:
    n -= 1

# Operador ternario
estado = "Aprobado" if nota >= 7 else "Reprobado"
```

## 3. Listas, diccionarios, sets, tuplas

```python
nums = [5, 3, 8, 1]
nums.append(10); nums.insert(0, 99); nums.remove(3); nums.pop()
nums.sort(); nums.sort(reverse=True)
ordenada = sorted(nums)
len(nums), sum(nums), max(nums), min(nums)
nums[0], nums[-1], nums[1:3], nums[::-1]   # primero, último, slice, invertida

# List comprehension (MUY útil)
pares = [x for x in nums if x % 2 == 0]
cuadrados = [x ** 2 for x in range(1, 6)]

# Diccionarios
persona = {"nombre": "Ana", "edad": 25}
persona["email"] = "ana@mail.com"
persona.get("telefono", "N/A")       # valor por defecto, no da error
for k, v in persona.items():
    print(k, v)
"nombre" in persona                   # True

# Lista de diccionarios (típico en CRUD)
estudiantes = [
    {"nombre": "Ana", "nota": 9},
    {"nombre": "Luis", "nota": 6},
]
aprobados = [e for e in estudiantes if e["nota"] >= 7]
ordenados = sorted(estudiantes, key=lambda e: e["nota"], reverse=True)
promedio = sum(e["nota"] for e in estudiantes) / len(estudiantes)

# Sets (sin repetidos)
unicos = set([1, 2, 2, 3])            # {1,2,3}
a & b, a | b, a - b                    # intersección, unión, diferencia

# Contar ocurrencias
from collections import Counter
Counter("banana")                      # {'a':3,'n':2,'b':1}
```

## 4. Strings

```python
s = "  Hola Mundo  "
s.strip(), s.lower(), s.upper(), s.title()
s.replace("Hola", "Chao")
s.split()              # ['Hola', 'Mundo']
"-".join(["a", "b"])   # "a-b"
s.startswith("Ho"), s.endswith("do"), "Mundo" in s
s.isdigit(), s.isalpha(), s.isalnum()
s[::-1]                # invertir
s.count("o"), s.find("M")
```

## 5. Funciones

```python
def saludar(nombre, saludo="Hola"):
    """Docstring: describe la función."""
    return f"{saludo}, {nombre}"

def sumar_todo(*args):          # cantidad variable de argumentos
    return sum(args)

cuadrado = lambda x: x * x

# Manejo de errores
try:
    x = int(input())
except ValueError:
    print("No es un número")
finally:
    print("Siempre se ejecuta")

# Lanzar error propio
if edad < 0:
    raise ValueError("La edad no puede ser negativa")
```

## 6. POO (clases)

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def presentarse(self):
        return f"Soy {self.nombre}"

    def __str__(self):                # cómo se imprime
        return f"Persona({self.nombre}, {self.edad})"

class Estudiante(Persona):            # herencia
    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self.carrera = carrera

    def presentarse(self):            # polimorfismo (sobrescritura)
        return f"{super().presentarse()} y estudio {self.carrera}"

e = Estudiante("Ana", 20, "Software")
print(e.presentarse())

# Dataclass (atajo moderno)
from dataclasses import dataclass
@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0
```

Los 4 pilares de POO (te lo pueden preguntar):
- **Encapsulamiento**: ocultar datos internos (`self._privado`, getters/setters, `@property`).
- **Herencia**: una clase hija reutiliza una padre (`class B(A)`).
- **Polimorfismo**: mismo método, distinto comportamiento según la clase.
- **Abstracción**: exponer solo lo necesario (`from abc import ABC, abstractmethod`).

## 7. Archivos y JSON

```python
import json

with open("datos.txt", "w", encoding="utf-8") as f:
    f.write("Hola\n")
with open("datos.txt", encoding="utf-8") as f:
    for linea in f:
        print(linea.strip())

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(estudiantes, f, ensure_ascii=False, indent=2)
with open("datos.json", encoding="utf-8") as f:
    datos = json.load(f)

# CSV
import csv
with open("datos.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["nombre"])
```

## 8. Base de datos con sqlite3 (viene con Python, sin instalar nada)

```python
import sqlite3

con = sqlite3.connect("app.db")
con.row_factory = sqlite3.Row           # permite fila["columna"]
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER DEFAULT 0
)""")

# SIEMPRE parámetros con ? (evita SQL Injection)
cur.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            ("Mouse", 12.5, 10))
con.commit()
nuevo_id = cur.lastrowid

filas = cur.execute("SELECT * FROM productos WHERE precio > ?", (5,)).fetchall()
for f in filas:
    print(f["id"], f["nombre"])

uno = cur.execute("SELECT * FROM productos WHERE id = ?", (1,)).fetchone()
cur.execute("UPDATE productos SET stock = ? WHERE id = ?", (20, 1))
cur.execute("DELETE FROM productos WHERE id = ?", (1,))
con.commit()
con.close()
```

### Con MySQL (si en el lab hay XAMPP)
```bash
pip install mysql-connector-python
```
```python
import mysql.connector
con = mysql.connector.connect(host="localhost", user="root", password="", database="tienda")
cur = con.cursor(dictionary=True)
cur.execute("SELECT * FROM productos WHERE id = %s", (1,))   # ojo: %s, no ?
print(cur.fetchone())
con.commit()
```

## 9. Flask (web/API rápida)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
pip install flask
python app.py
```

```python
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.get("/")
def inicio():
    return render_template("index.html", titulo="Inicio")

@app.get("/api/productos")
def listar():
    return jsonify([{"id": 1, "nombre": "Mouse"}])

@app.post("/api/productos")
def crear():
    data = request.get_json()
    if not data or not data.get("nombre"):
        return jsonify({"error": "nombre es obligatorio"}), 400
    return jsonify({"id": 2, **data}), 201

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        return redirect(url_for("inicio"))
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)       # http://127.0.0.1:5000
```

Plantilla Jinja2 (`templates/index.html`):
```html
<h1>{{ titulo }}</h1>
{% for p in productos %}
  <p>{{ p.nombre }} - ${{ "%.2f"|format(p.precio) }}</p>
{% else %}
  <p>No hay productos</p>
{% endfor %}
{% if error %}<div class="error">{{ error }}</div>{% endif %}
```

Códigos HTTP a recordar: **200** OK, **201** creado, **204** sin contenido, **400** petición inválida, **401** no autenticado, **403** prohibido, **404** no encontrado, **500** error del servidor.

## 10. Testing en Python

```python
# test_calculos.py  → ejecutar: python -m unittest -v
import unittest
from calculos import sumar

class TestCalculos(unittest.TestCase):
    def test_sumar(self):
        self.assertEqual(sumar(2, 3), 5)

    def test_error(self):
        with self.assertRaises(ValueError):
            sumar("a", 1)

if __name__ == "__main__":
    unittest.main()
```

Con pytest (`pip install pytest`, luego `pytest -v`):
```python
def test_sumar():
    assert sumar(2, 3) == 5
```

## 11. Comandos útiles

```bash
python --version
pip install -r requirements.txt
pip freeze > requirements.txt
python -m http.server 8000     # servidor estático rápido
```

---

# PARTE 2 — AMPLIACIÓN

> Ejemplos ejecutables de todo esto en `05-ejemplos/python/` (01 a 10).

## 12. Dónde y cómo se ejecuta Python

| Forma | Cómo | Cuándo |
|---|---|---|
| Archivo | `python archivo.py` | Siempre en la prueba |
| Consola interactiva (REPL) | `python` → escribir código → `exit()` | Probar una línea rápida |
| Módulo | `python -m unittest`, `python -m venv venv`, `python -m http.server` | Herramientas incluidas |
| VS Code | Botón ▶ arriba a la derecha, o `F5` para depurar | Cómodo; revisa el intérprete (abajo a la derecha) |
| Con argumentos | `python app.py 8080` → `import sys; sys.argv[1]` | Parametrizar |

**Estructura típica de un script:**
```python
"""Descripción del programa."""
import sys                     # 1. imports de la biblioteca estándar
import requests                # 2. imports de terceros
from mi_modulo import util     # 3. imports propios

CONSTANTE = 10                 # 4. constantes en MAYÚSCULAS

def main():                    # 5. funciones
    ...

if __name__ == "__main__":     # 6. punto de entrada: solo corre al ejecutar el archivo, no al importarlo
    main()
```

## 13. Convenciones (PEP 8), lo que el evaluador nota

- `snake_case` para variables y funciones, `PascalCase` para clases, `MAYUSCULAS` para constantes.
- 4 espacios de sangría (nunca tabs mezclados). Máximo ~100 caracteres por línea.
- Nombres descriptivos: `total_ventas`, no `tv`. Funciones con verbo: `calcular_promedio()`.
- Docstrings en funciones públicas. Comentarios que expliquen el **por qué**, no el qué.
- `if lista:` en lugar de `if len(lista) > 0:`, y `if x is None:` en lugar de `== None`.

## 14. Comprehensions avanzadas y generadores

```python
# Anidada (aplanar matriz)
plana = [x for fila in [[1, 2], [3, 4]] for x in fila]          # [1, 2, 3, 4]
# Con condición y transformación
nombres = [e["nombre"].upper() for e in estudiantes if e["nota"] >= 7]
# Diccionario invertido
invertido = {v: k for k, v in {"a": 1, "b": 2}.items()}          # {1: 'a', 2: 'b'}
# Generador: no crea la lista en memoria (paréntesis)
total = sum(x * x for x in range(1_000_000))

def leer_grande(ruta):          # función generadora: yield
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            yield linea.strip()
```

## 15. Módulos útiles de la biblioteca estándar (sin instalar)

| Módulo | Para qué | Ejemplo |
|---|---|---|
| `os`, `pathlib` | Archivos y rutas | `Path("datos").mkdir(exist_ok=True)` |
| `sys` | Argumentos, salir | `sys.argv`, `sys.exit(1)` |
| `json`, `csv` | Formatos | `json.dumps(obj, ensure_ascii=False)` |
| `sqlite3` | Base de datos | ver sección 8 |
| `datetime` | Fechas | `datetime.now().strftime("%d/%m/%Y")` |
| `re` | Expresiones regulares | `re.fullmatch(r"\d{10}", cedula)` |
| `collections` | Counter, defaultdict, deque | `Counter(lista).most_common(3)` |
| `itertools` | Combinaciones | `combinations([1,2,3], 2)`, `groupby`, `chain` |
| `functools` | lru_cache, reduce, partial | `@lru_cache` |
| `math`, `random`, `statistics` | Números | `statistics.mean(notas)`, `median`, `stdev` |
| `decimal` | Dinero exacto | `Decimal("0.1") + Decimal("0.2")` |
| `unittest` | Pruebas | ver sección 10 |
| `http.server` | Servidor web | `python -m http.server 8000` |
| `urllib.request` | Peticiones HTTP sin requests | `urlopen(url).read()` |
| `hashlib`, `secrets` | Hash y tokens | `hashlib.sha256(b"x").hexdigest()`, `secrets.token_hex(16)` |
| `logging` | Logs | `logging.basicConfig(level=logging.INFO)` |

## 16. Consumir APIs con requests

```bash
pip install requests
```
```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/users", params={"_limit": 3}, timeout=5)
r.raise_for_status()                    # lanza error si 4xx/5xx
usuarios = r.json()
print([u["name"] for u in usuarios])

r = requests.post("http://localhost:5000/api/estudiantes",
                  json={"nombre": "Ana", "cedula": "1710034065"}, timeout=5)
print(r.status_code, r.json())

requests.put(url, json={...}); requests.delete(url)
requests.get(url, headers={"Authorization": "Bearer TOKEN"})
```

## 17. Flask ampliado

### Blueprints (organizar rutas en varios archivos)
```python
# rutas/productos.py
from flask import Blueprint, jsonify
bp = Blueprint("productos", __name__, url_prefix="/productos")

@bp.get("/")
def listar():
    return jsonify([])

# app.py
from rutas.productos import bp as productos_bp
app.register_blueprint(productos_bp)
```

### Login con sesión y contraseña con hash
```python
from functools import wraps
from flask import session, redirect, url_for, request, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash   # viene con Flask

# Al registrar:  hash = generate_password_hash("Clave123")  → guardar en la BD
# Al ingresar:
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = get_db().execute("SELECT * FROM usuarios WHERE email = ?",
                                   (request.form["email"],)).fetchone()
        if usuario and check_password_hash(usuario["clave_hash"], request.form["clave"]):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            return redirect(url_for("inicio"))
        flash("Credenciales incorrectas", "error")
    return render_template("login.html")

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura

@app.get("/panel")
@login_requerido
def panel():
    return f"Hola {session['nombre']}"
```
En plantillas: `{% if session.usuario_id %} Hola {{ session.nombre }} {% endif %}`.

### Paginación
```python
@app.get("/productos")
def productos():
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = 10
    total = get_db().execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    filas = get_db().execute("SELECT * FROM productos ORDER BY id LIMIT ? OFFSET ?",
                             (por_pagina, (pagina - 1) * por_pagina)).fetchall()
    paginas = (total + por_pagina - 1) // por_pagina        # división hacia arriba
    return render_template("productos.html", filas=filas, pagina=pagina, paginas=paginas)
```
```html
{% if pagina > 1 %}<a href="?pagina={{ pagina - 1 }}">Anterior</a>{% endif %}
Página {{ pagina }} de {{ paginas }}
{% if pagina < paginas %}<a href="?pagina={{ pagina + 1 }}">Siguiente</a>{% endif %}
```

### Exportar CSV / descargar
```python
import csv, io
from flask import Response

@app.get("/exportar")
def exportar():
    salida = io.StringIO()
    w = csv.writer(salida)
    w.writerow(["id", "nombre"])
    for f in get_db().execute("SELECT id, nombre FROM productos"):
        w.writerow([f["id"], f["nombre"]])
    return Response("﻿" + salida.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=productos.csv"})
```

### Subir archivos
```python
from werkzeug.utils import secure_filename
@app.post("/subir")
def subir():
    archivo = request.files.get("foto")          # <form enctype="multipart/form-data">
    if not archivo or not archivo.filename.lower().endswith((".png", ".jpg")):
        return "Archivo inválido", 400
    archivo.save(os.path.join("static/uploads", secure_filename(archivo.filename)))
    return "OK"
```

### Manejo de errores y CORS
```python
@app.errorhandler(404)
def no_encontrado(e):
    return render_template("404.html"), 404

# CORS (si un frontend React en otro puerto consume tu API)
# pip install flask-cors
from flask_cors import CORS
CORS(app)
```

### Jinja2 en 10 líneas
```html
{{ variable }}  {{ variable|upper }}  {{ lista|length }}  {{ precio|round(2) }}  {{ texto|default("—") }}
{{ "%.2f"|format(precio) }}   {{ fecha.strftime("%d/%m/%Y") }}
{% if cond %}...{% elif otra %}...{% else %}...{% endif %}
{% for x in lista %} {{ loop.index }} {{ x }} {% else %} vacío {% endfor %}
{% extends "base.html" %}  {% block contenido %}{% endblock %}  {% include "parcial.html" %}
{% set total = items|sum(attribute="precio") %}
{{ url_for('editar', id=5) }}   {{ url_for('static', filename='css/app.css') }}
{# comentario #}
```
Jinja **escapa HTML automáticamente** (protege de XSS). `{{ html|safe }}` desactiva el escape; úsalo solo con contenido tuyo.

## 18. SQLAlchemy / Flask-SQLAlchemy (ORM), por si lo piden

```bash
pip install flask-sqlalchemy
```
```python
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"   # MySQL: "mysql+pymysql://root:@localhost/tienda"
db = SQLAlchemy(app)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    productos = db.relationship("Producto", backref="categoria")

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))

with app.app_context():
    db.create_all()

# CRUD
p = Producto(nombre="Mouse", precio=10); db.session.add(p); db.session.commit()
Producto.query.all(); db.session.get(Producto, 1); Producto.query.filter_by(nombre="Mouse").first()
Producto.query.filter(Producto.precio > 5).order_by(Producto.nombre).all()
p.precio = 12; db.session.commit()
db.session.delete(p); db.session.commit()
```
**ORM vs SQL directo:** el ORM mapea tablas a clases, evita escribir SQL y es portable entre bases. El SQL directo da más control y es más transparente. En una prueba de 3 horas, `sqlite3` directo es lo más rápido de montar.

## 19. Django en 1 minuto (por si preguntan la diferencia)

```bash
pip install django
django-admin startproject sitio .
python manage.py startapp inventario
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser
python manage.py runserver                 # http://127.0.0.1:8000/admin
```
Django trae ORM, panel de administración, autenticación y formularios incluidos ("baterías incluidas"). Flask es minimalista: tú eliges cada pieza. Patrón de Django: **MVT** (Model–View–Template).

## 20. Pruebas ampliadas

```python
import unittest
from unittest.mock import patch

class TestCalculos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):        # una vez para toda la clase
        cls.datos = [1, 2, 3]

    def setUp(self):            # antes de CADA prueba
        self.lista = []

    def test_iguales(self):
        self.assertEqual(sum(self.datos), 6)
        self.assertAlmostEqual(0.1 + 0.2, 0.3)       # floats
        self.assertIn(2, self.datos)
        self.assertTrue(all(x > 0 for x in self.datos))
        self.assertIsNone(None)

    def test_excepcion(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

    def test_con_subcasos(self):
        for entrada, esperado in [(2, True), (3, False)]:
            with self.subTest(entrada=entrada):
                self.assertEqual(entrada % 2 == 0, esperado)

    @patch("random.randint", return_value=4)          # simular (mock) una dependencia
    def test_mock(self, _):
        import random
        self.assertEqual(random.randint(1, 6), 4)
```
Comandos: `python -m unittest -v`, `python -m unittest discover tests`, `python -m unittest test_modulo.TestClase.test_metodo`.

## 21. Errores frecuentes en Python y cómo leerlos

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>      ← archivo y línea donde ocurrió
    print(usuario["email"])
KeyError: 'email'                          ← TIPO de error: mensaje   ← ¡lee esto primero!
```
| Error | Causa típica |
|---|---|
| `IndentationError: expected an indented block` | Falta sangría después de `:` |
| `SyntaxError: invalid syntax` | Falta `:` en if/def/for, paréntesis sin cerrar, `=` en vez de `==` |
| `TypeError: can only concatenate str (not "int") to str` | `"Edad: " + 5` → usa f-string |
| `TypeError: 'NoneType' object is not subscriptable` | `fetchone()` devolvió None (no existe el registro) |
| `UnboundLocalError` | Asignas una variable global dentro de una función sin `global` |
| `RecursionError` | Recursión sin caso base |
| `sqlite3.ProgrammingError: Incorrect number of bindings` | Cantidad de `?` distinta a la de valores. Ojo: `(x)` no es tupla, usa `(x,)` |
| `jinja2.exceptions.UndefinedError` | Variable no pasada a `render_template` |
