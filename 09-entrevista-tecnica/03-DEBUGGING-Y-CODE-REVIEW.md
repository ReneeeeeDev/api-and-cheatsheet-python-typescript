# Debugging y code review: encuentra el error

En muchas entrevistas te muestran código y te preguntan: *"¿qué está mal aquí?"* o *"¿qué le dirías a quien lo escribió?"*. Evalúan si conoces las trampas del lenguaje y si revisas con criterio: corrección, seguridad, rendimiento y legibilidad.

**Cómo practicar:** lee cada fragmento, escribe qué falla, con qué entrada falla y cómo lo corriges. Después abre la respuesta. Si puedes, **ejecuta** el fragmento para comprobarlo.

**Cómo responder en la entrevista:** (1) qué hace mal, (2) un ejemplo de entrada que lo rompe, (3) la corrección, (4) cómo evitarías que vuelva a pasar, por ejemplo con una prueba o una regla del linter.

---

## Python

### 1. La lista que recuerda
```python
def agregar_nota(nota, notas=[]):
    notas.append(nota)
    return notas

print(agregar_nota(8))
print(agregar_nota(9))   # el autor esperaba [9]
```

<details><summary>Respuesta</summary><p>Imprime <code>[8]</code> y luego <code>[8, 9]</code>. El valor por defecto se crea <b>una sola vez</b>, al definir la función, y todas las llamadas comparten la misma lista mutable. Corrección: <code>def agregar_nota(nota, notas=None):</code> y dentro <code>if notas is None: notas = []</code>. Pylint lo detecta (W0102, dangerous-default-value).</p></details>

### 2. Borrar mientras recorres
```python
def quitar_reprobados(notas):
    for n in notas:
        if n < 7:
            notas.remove(n)
    return notas

print(quitar_reprobados([5, 6, 8, 9]))
```

<details><summary>Respuesta</summary><p>Devuelve <code>[6, 8, 9]</code>: el 6 se salva. Al borrar el 5, todos los elementos se corren una posición y el bucle salta el siguiente. Además modifica la lista que recibió, un efecto secundario sorpresa. Corrección: crear una lista nueva, <code>return [n for n in notas if n &gt;= 7]</code>. Regla: nunca modifiques una colección mientras la recorres.</p></details>

### 3. La búsqueda que no encuentra el último
```python
def buscar(lista, x):
    izq, der = 0, len(lista) - 1
    while izq < der:
        medio = (izq + der) // 2
        if lista[medio] == x:
            return medio
        if lista[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1

print(buscar([1, 3, 5], 5))
```

<details><summary>Respuesta</summary><p>Devuelve <code>-1</code>. Cuando <code>izq == der</code> todavía queda un elemento por revisar, pero el bucle termina antes. Es un error <i>off-by-one</i>. Corrección: <code>while izq &lt;= der</code>. Prueba siempre con el primer elemento, el último, uno que no existe y una lista vacía.</p></details>

### 4. El promedio que explota
```python
def promedio(notas):
    return sum(notas) / len(notas)

promedio([])
```

<details><summary>Respuesta</summary><p><code>ZeroDivisionError</code> con una lista vacía. Hay que decidir y documentar qué pasa en ese caso: devolver <code>None</code> o <code>0</code>, o lanzar un <code>ValueError</code> con un mensaje claro. Por ejemplo: <code>if not notas: return None</code>. Es el caso de borde que más se olvida.</p></details>

### 5. Dinero con float
```python
subtotal = 0.1 + 0.2
if subtotal == 0.3:
    print("cobrar 0.30")
print(1.10 * 3)
```

<details><summary>Respuesta</summary><p>No imprime "cobrar" y la multiplicación da <code>3.3000000000000003</code>. Un <code>float</code> es binario y no representa exactamente 0.1. Para dinero usa <code>Decimal("0.10")</code> (construido desde texto) o enteros en centavos; para comparar floats, <code>math.isclose(a, b)</code>. En SQL: <code>DECIMAL(10, 2)</code>, nunca <code>FLOAT</code>.</p></details>

### 6. `is` en vez de `==`
```python
codigo = input("Código: ")       # el usuario escribe LAB-001
if codigo is "LAB-001":
    print("encontrado")
```

<details><summary>Respuesta</summary><p>Casi nunca imprime "encontrado". <code>is</code> compara <b>identidad</b> (si son el mismo objeto en memoria), no igualdad de valor, y el texto leído es un objeto distinto. Python 3.8+ incluso muestra un <code>SyntaxWarning</code>. Usa <code>==</code> para valores; <code>is</code> solo para <code>None</code>, <code>True</code> y <code>False</code>.</p></details>

### 7. La matriz con filas clonadas
```python
tablero = [[0] * 3] * 3
tablero[0][0] = 1
print(tablero)
```

<details><summary>Respuesta</summary><p>Imprime <code>[[1, 0, 0], [1, 0, 0], [1, 0, 0]]</code>: <code>* 3</code> repite <b>la misma lista</b> tres veces, así que las tres filas son una sola. Corrección: <code>[[0] * 3 for _ in range(3)]</code>. Es la misma idea que copia superficial vs profunda (<code>copy.deepcopy</code>).</p></details>

### 8. Horarios comparados como texto
```python
def se_cruzan(ini1, fin1, ini2, fin2):
    return ini1 < fin2 and ini2 < fin1

print(se_cruzan("9:00", "10:00", "9:30", "11:00"))   # se cruzan, ¿verdad?
```

<details><summary>Respuesta</summary><p>Devuelve <code>False</code>. Los textos se comparan carácter por carácter, y <code>"9:00" &lt; "11:00"</code> es falso porque "9" &gt; "1". Comparar horas como texto solo funciona si <b>siempre</b> tienen dos dígitos (<code>09:00</code>). Corrección: validar el formato con <code>^([01]\d|2[0-3]):[0-5]\d$</code> (como en <code>08-guia-desde-cero</code>) o convertir a minutos: <code>h * 60 + m</code>.</p></details>

### 9. Consulta armada con f-string
```python
def buscar_docente(db, nombre):
    sql = f"SELECT * FROM docentes WHERE nombre = '{nombre}'"
    return db.execute(sql).fetchall()

buscar_docente(db, "x' OR '1'='1")
```

<details><summary>Respuesta</summary><p><b>Inyección SQL</b>: con esa entrada la consulta queda <code>WHERE nombre = 'x' OR '1'='1'</code> y devuelve todos los registros. Con otras entradas un atacante puede leer otras tablas o borrar datos. Corrección: consulta parametrizada, <code>db.execute("SELECT * FROM docentes WHERE nombre = ?", (nombre,))</code>. Nunca concatenes entrada del usuario en SQL. Es el número 1 que revisan en un code review.</p></details>

### 10. El reporte que hace 1 001 consultas
```python
labs = db.execute("SELECT id, nombre FROM laboratorios").fetchall()
reporte = []
for lab in labs:
    total = db.execute("SELECT COUNT(*) FROM reservas WHERE laboratorio_id = ?",
                       (lab["id"],)).fetchone()[0]
    reporte.append((lab["nombre"], total))
```

<details><summary>Respuesta</summary><p>Funciona, pero es el problema <b>N+1</b>: una consulta para la lista y una más por cada laboratorio. Con 1 000 laboratorios son 1 001 viajes a la base de datos. Corrección, una sola consulta: <code>SELECT l.nombre, COUNT(r.id) FROM laboratorios l LEFT JOIN reservas r ON r.laboratorio_id = l.id GROUP BY l.id</code>. El <code>LEFT JOIN</code> conserva los laboratorios con 0 reservas. Los ORMs esconden este problema; se soluciona con <code>joinedload</code> o <code>include</code>.</p></details>

---

## JavaScript

### 11. Igualdad con conversión
```js
function validarCantidad(cantidad) {
  if (cantidad == "") return "La cantidad es obligatoria";
  return "OK";
}
console.log(validarCantidad(0));
```

<details><summary>Respuesta</summary><p>Devuelve "La cantidad es obligatoria". Con <code>==</code>, JS convierte los tipos: <code>0 == ""</code> es <code>true</code> (también <code>"0" == false</code> y <code>null == undefined</code>). Usa siempre <code>===</code>. Para validar: <code>if (cantidad === "" || cantidad === null || Number.isNaN(Number(cantidad)))</code>. ESLint lo exige con la regla <code>eqeqeq</code>.</p></details>

### 12. `sort` que ordena mal
```js
const edades = [10, 9, 1, 100];
console.log(edades.sort());
```

<details><summary>Respuesta</summary><p>Imprime <code>[1, 10, 100, 9]</code>: sin comparador, <code>sort</code> convierte todo a texto y ordena alfabéticamente. Corrección: <code>edades.sort((a, b) =&gt; a - b)</code>. Ojo: <code>sort</code> también <b>modifica</b> el arreglo original; si no quieres eso, usa <code>[...edades].sort(...)</code> o <code>toSorted</code>.</p></details>

### 13. `forEach` con `async`
```js
async function guardarTodas(reservas) {
  reservas.forEach(async (r) => {
    await db.guardar(r);
  });
  console.log("Todas guardadas");
}
```

<details><summary>Respuesta</summary><p>"Todas guardadas" se imprime <b>antes</b> de guardar, y los errores de <code>guardar</code> se pierden: <code>forEach</code> no espera promesas. Corrección en serie: <code>for (const r of reservas) await db.guardar(r);</code>. En paralelo: <code>await Promise.all(reservas.map((r) =&gt; db.guardar(r)));</code>.</p></details>

### 14. El `await` que falta
```js
async function saludar(email) {
  const usuario = buscarUsuario(email);   // buscarUsuario es async
  if (!usuario) return "No existe";
  return `Hola ${usuario.nombre}`;
}
```

<details><summary>Respuesta</summary><p>Siempre devuelve "Hola undefined". Sin <code>await</code>, <code>usuario</code> es una <code>Promise</code>, que siempre es <i>truthy</i>, y una promesa no tiene <code>.nombre</code>. Corrección: <code>const usuario = await buscarUsuario(email);</code>. TypeScript o la regla de ESLint <code>no-floating-promises</code> lo detectan.</p></details>

### 15. `var` en un bucle
```js
for (var i = 1; i <= 3; i++) {
  setTimeout(() => console.log("Turno", i), 100);
}
```

<details><summary>Respuesta</summary><p>Imprime "Turno 4" tres veces. <code>var</code> tiene alcance de función, así que las tres funciones comparten la misma <code>i</code>, y cuando se ejecutan el bucle ya terminó con <code>i = 4</code>. Corrección: <code>let i</code>, que crea una variable nueva en cada vuelta. En Python pasa lo mismo con <code>[lambda: i for i in range(3)]</code>; se corrige con <code>lambda i=i: i</code>.</p></details>

---

## Ejercicio de code review

Te piden revisar este pull request. **Antes de ver la respuesta, encuentra al menos 8 problemas** y ordénalos por gravedad.

```python
import sqlite3
from flask import Flask, request

app = Flask(__name__)
app.secret_key = "123"

@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    db = sqlite3.connect("app.db")
    if request.method == "POST":
        docente = request.form["docente"]
        lab = request.form["lab"]
        fecha = request.form["fecha"]
        ini = request.form["ini"]
        fin = request.form["fin"]
        db.execute(f"INSERT INTO reservas VALUES (null, {lab}, '{docente}', '{fecha}', '{ini}', '{fin}')")
        db.commit()
    filas = db.execute("SELECT * FROM reservas").fetchall()
    html = ""
    for f in filas:
        lab = db.execute(f"SELECT nombre FROM laboratorios WHERE id = {f[1]}").fetchone()
        html += f"<li>{f[2]} - {lab[0]} - {f[3]} {f[4]}-{f[5]}</li>"
    return "<ul>" + html + "</ul>"
```

<details><summary>Respuesta (12 problemas, del más grave al menos grave)</summary>
<ol>
<li><b>Inyección SQL</b> en el INSERT y en el SELECT del bucle (f-strings). Usar parámetros <code>?</code>.</li>
<li><b>XSS</b>: <code>docente</code> se inserta en el HTML sin escapar; un nombre como <code>&lt;script&gt;…&lt;/script&gt;</code> se ejecuta en el navegador de cada visitante. Usar plantillas Jinja, que escapan por defecto, o <code>markupsafe.escape</code>.</li>
<li><b>Clave secreta débil y escrita en el código</b> (<code>"123"</code>). Leerla de una variable de entorno: <code>os.environ["SECRET_KEY"]</code>.</li>
<li><b>Sin validación</b>: campos vacíos, formato de fecha y hora, <code>fin &gt; ini</code>, que el laboratorio exista y no esté en mantenimiento.</li>
<li><b>No revisa choques de horario</b>: es la regla de negocio principal (<code>ini1 &lt; fin2 AND ini2 &lt; fin1</code>).</li>
<li><b>Sin CSRF</b> en un formulario POST (Flask-WTF o un token propio).</li>
<li><code>request.form["x"]</code> lanza <code>KeyError</code> → error 400 genérico si falta un campo; mejor <code>request.form.get("x", "").strip()</code> con un mensaje de error claro.</li>
<li><b>La conexión nunca se cierra</b>: se pierde en cada petición. Usar <code>g</code> + <code>teardown_appcontext</code> o <code>with</code>.</li>
<li><b>N+1</b>: una consulta por cada reserva para traer el nombre del laboratorio. Usar <code>JOIN</code>.</li>
<li>Después del POST no hay <b>redirect</b> (patrón Post/Redirect/Get): al recargar la página se duplica la reserva.</li>
<li><code>INSERT</code> sin nombres de columnas, <code>SELECT *</code> e índices mágicos (<code>f[1]</code>, <code>f[2]</code>) se rompen si cambia la tabla. Nombrar las columnas y usar <code>row_factory = sqlite3.Row</code>.</li>
<li>Sin pruebas, sin paginación y sin separación de responsabilidades: la ruta valida, guarda y genera HTML. Separar en <code>validaciones.py</code>, <code>db.py</code> y plantillas, como en <code>08-guia-desde-cero</code>.</li>
</ol>
<p><b>Cómo comunicarlo:</b> empieza por lo bueno ("la ruta es corta y se entiende"), separa lo que <b>bloquea</b> el merge (1–5) de las <b>sugerencias</b> (10–12) y propone la corrección en lugar de solo señalar el problema.</p>
</details>

---

## Checklist para revisar código (úsala también con tu propio código)

| Área | Pregunta |
|---|---|
| Corrección | ¿Hace lo que dice el requisito? ¿Funciona con vacíos, nulos, bordes y errores de red o de base de datos? |
| Seguridad | ¿Consultas parametrizadas? ¿Salida escapada? ¿Secretos fuera del código? ¿Se valida en el servidor? ¿Se revisa quién puede hacer qué? |
| Rendimiento | ¿Consultas dentro de bucles (N+1)? ¿Bucles anidados innecesarios? ¿Falta paginación o índices? |
| Legibilidad | ¿Nombres claros? ¿Funciones cortas con una sola tarea? ¿Código duplicado? ¿Números mágicos? |
| Errores | ¿Se manejan las excepciones? ¿Los mensajes ayudan al usuario sin exponer detalles internos? |
| Pruebas | ¿Hay pruebas de las reglas de negocio? ¿Cubren los casos de borde? |
