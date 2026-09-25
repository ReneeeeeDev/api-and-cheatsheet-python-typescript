# Cheatsheet HTML + CSS

## 1. Plantilla base HTML5 (escríbela de memoria)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header><nav>...</nav></header>
  <main>
    <section>...</section>
  </main>
  <footer>© 2026</footer>
  <script src="app.js"></script>
</body>
</html>
```

Etiquetas semánticas: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`. Mejoran SEO y accesibilidad.

## 2. Formulario completo con validación HTML

```html
<form id="form" action="/guardar" method="POST">
  <label for="nombre">Nombre</label>
  <input id="nombre" name="nombre" type="text" required minlength="3" maxlength="100">

  <label for="email">Email</label>
  <input id="email" name="email" type="email" required>

  <label for="cedula">Cédula</label>
  <input id="cedula" name="cedula" pattern="[0-9]{10}" title="10 dígitos" required>

  <label for="edad">Edad</label>
  <input id="edad" name="edad" type="number" min="0" max="120">

  <label for="fecha">Fecha</label>
  <input id="fecha" name="fecha" type="date">

  <label for="carrera">Carrera</label>
  <select id="carrera" name="carrera" required>
    <option value="">-- Seleccione --</option>
    <option value="1">Software</option>
  </select>

  <fieldset>
    <legend>Jornada</legend>
    <label><input type="radio" name="jornada" value="matutina" checked> Matutina</label>
    <label><input type="radio" name="jornada" value="nocturna"> Nocturna</label>
  </fieldset>

  <label><input type="checkbox" name="acepta" required> Acepto términos</label>
  <textarea name="obs" rows="3"></textarea>
  <button type="submit">Guardar</button>
</form>
```

## 3. Tabla

```html
<table>
  <thead><tr><th>ID</th><th>Nombre</th><th>Acciones</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>Ana</td><td><button>Editar</button><button>Eliminar</button></td></tr>
  </tbody>
</table>
```

## 4. CSS esencial

```css
*, *::before, *::after { box-sizing: border-box; }   /* SIEMPRE */
:root { --primario: #0a5bd6; --texto: #1f2937; }      /* variables */
body { margin: 0; font-family: system-ui, sans-serif; color: var(--texto); }

/* Selectores */
.clase {}  #id {}  div p {} /* descendiente */  div > p {} /* hijo directo */
a:hover {}  li:nth-child(odd) {}  input:focus {}  input:invalid {}
[type="email"] {}

/* Box model: contenido + padding + border + margin */
.card { padding: 16px; border: 1px solid #ddd; border-radius: 8px; margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,.08); }
```

## 5. Flexbox (una dimensión)

```css
.fila {
  display: flex;
  justify-content: space-between;   /* eje principal: flex-start|center|space-between|space-around */
  align-items: center;              /* eje cruzado */
  gap: 12px;
  flex-wrap: wrap;
}
.fila > .item { flex: 1; }          /* crecer para ocupar espacio */
.centrar-todo { display: flex; justify-content: center; align-items: center; min-height: 100vh; }
```

## 6. Grid (dos dimensiones)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));   /* responsive sin media queries */
  gap: 16px;
}
.layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-areas: "aside main";
}
```

## 7. Responsive

```css
/* Mobile first */
.contenedor { width: 100%; padding: 0 16px; }
@media (min-width: 768px) {
  .contenedor { max-width: 960px; margin: 0 auto; }
}
img { max-width: 100%; height: auto; }
```

## 8. Estilos rápidos para que tu CRUD se vea profesional

```css
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: left; }
thead { background: #f3f4f6; }
button { padding: 8px 14px; border: 0; border-radius: 6px; cursor: pointer;
         background: var(--primario); color: #fff; }
button.peligro { background: #dc2626; }
input, select { width: 100%; padding: 8px; border: 1px solid #d1d5db; border-radius: 6px; }
.error { color: #dc2626; }
.exito { color: #16a34a; }
```

Si hay internet, Bootstrap en 1 línea (ahorra tiempo):
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- clases: container, row, col-md-6, btn btn-primary, table table-striped, form-control, alert alert-danger -->
```

## 9. Teoría rápida

- **Especificidad**: inline > #id > .clase/:hover/[atr] > etiqueta. `!important` gana todo (evitarlo).
- **position**: `static` (normal), `relative` (se mueve respecto a sí mismo), `absolute` (respecto al padre posicionado), `fixed` (respecto a la ventana), `sticky`.
- **display**: `block` (ocupa toda la fila), `inline` (en línea, sin ancho/alto), `inline-block`, `flex`, `grid`, `none`.
- **em vs rem**: em relativo al padre, rem relativo al `html`.
- **Accesibilidad**: `alt` en imágenes, `label` asociado a cada input, contraste suficiente.

---

# PARTE 2 — AMPLIACIÓN

> Práctica completa en `05-ejemplos/web-dom/index.html` (formulario validado, tabla, filtros, localStorage).

## 10. Cómo ver y probar HTML/CSS

- **Doble clic** en el `.html`: se abre en el navegador (file://). Suficiente para HTML/CSS/JS simple.
- **Live Server** (VS Code): clic derecho → *Open with Live Server*. Recarga al guardar y sirve en http://127.0.0.1:5500.
- **Servidor rápido:** `python -m http.server 8000` o `npx serve` en la carpeta.
- **F12 (DevTools):** Elements (ver/editar CSS en vivo), Console, Network, y el icono de móvil (📱) para probar el responsive.

## 11. HTML semántico y accesible: estructura de una página completa

```html
<body>
  <a href="#contenido" class="saltar">Saltar al contenido</a>
  <header>
    <nav aria-label="Principal">
      <ul><li><a href="/" aria-current="page">Inicio</a></li><li><a href="/cursos">Cursos</a></li></ul>
    </nav>
  </header>
  <main id="contenido">
    <h1>Un solo h1 por página</h1>
    <section aria-labelledby="t-cursos">
      <h2 id="t-cursos">Cursos</h2>
      <article>
        <h3>Programación I</h3>
        <p>...</p>
        <figure><img src="aula.jpg" alt="Estudiantes en el laboratorio" width="400" height="300" loading="lazy">
          <figcaption>Laboratorio 002</figcaption></figure>
      </article>
    </section>
    <aside>Contenido relacionado</aside>
  </main>
  <footer><address>Ambato, Ecuador</address></footer>
</body>
```
- Jerarquía de títulos sin saltos (h1 → h2 → h3).
- `alt` descriptivo en imágenes informativas, `alt=""` en decorativas.
- `<button>` para acciones y `<a>` para navegar. Nunca `<div onclick>`.
- Cada input con su `<label for>`. Errores asociados con `aria-describedby`.
- Contraste mínimo 4.5:1 en texto normal.

## 12. Tipos de input y validación nativa

```html
<input type="text" required minlength="3" maxlength="50" pattern="[A-Za-zÁÉÍÓÚáéíóúñÑ ]+">
<input type="email" required>        <input type="url">          <input type="tel" pattern="09[0-9]{8}">
<input type="number" min="0" max="10" step="0.01">              <input type="range" min="0" max="100">
<input type="date" min="2026-01-01">  <input type="time">          <input type="datetime-local">
<input type="password" autocomplete="new-password">             <input type="file" accept=".pdf,image/*" multiple>
<input type="color">  <input type="search">  <input type="checkbox">  <input type="radio">  <input type="hidden">
<select multiple size="3">...</select>   <textarea rows="4"></textarea>
<datalist id="ciudades"><option value="Ambato"><option value="Quito"></datalist> <input list="ciudades">
```
Estilizar según validez: `input:invalid`, `input:valid`, `input:user-invalid` (solo después de que el usuario interactúa), `:focus-visible`, `:disabled`, `:checked`, `:placeholder-shown`.

Validación personalizada con JS:
```js
input.setCustomValidity(cedulaValida(input.value) ? "" : "Cédula inválida");
form.reportValidity();
```

## 13. Flexbox a fondo

```css
.contenedor {
  display: flex;
  flex-direction: row;          /* row | column | row-reverse | column-reverse */
  flex-wrap: wrap;              /* permite varias líneas */
  justify-content: space-between; /* EJE PRINCIPAL: flex-start | center | flex-end | space-between | space-around | space-evenly */
  align-items: center;          /* EJE CRUZADO: stretch | flex-start | center | flex-end | baseline */
  align-content: flex-start;    /* reparte las líneas cuando hay wrap */
  gap: 16px 8px;                /* fila columna */
}
.item { flex: 1 1 200px; }      /* grow shrink basis: crece, se encoge, base 200px */
.item-fijo { flex: 0 0 250px; } /* no crece ni se encoge */
.item-especial { align-self: flex-end; order: -1; }
.empujar-derecha { margin-left: auto; }   /* truco: empuja al extremo */
```
Patrones: barra de navegación (logo a la izquierda, menú a la derecha con `margin-left: auto`), footer al fondo (`body{display:flex;flex-direction:column;min-height:100vh} main{flex:1}`), tarjetas que se envuelven (`flex-wrap`).

## 14. Grid a fondo

```css
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "aside  main"
    "footer footer";
  min-height: 100vh;
  gap: 16px;
}
header { grid-area: header; } aside { grid-area: aside; } main { grid-area: main; } footer { grid-area: footer; }

@media (max-width: 768px) {
  .layout { grid-template-columns: 1fr; grid-template-areas: "header" "main" "aside" "footer"; }
}

.galeria { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
.destacado { grid-column: span 2; grid-row: span 2; }
.centrado { display: grid; place-items: center; }     /* centrar en 1 línea */
```
**¿Flex o Grid?** Flex para una dimensión (una fila o una columna de elementos). Grid para dos dimensiones (layout de página, galerías).

## 15. Responsive completo

```css
/* Mobile first: estilos base para celular, luego se amplía */
.menu { display: none; }
@media (min-width: 576px)  { /* celulares grandes */ }
@media (min-width: 768px)  { .menu { display: flex; } /* tablets */ }
@media (min-width: 1024px) { /* laptops */ }
@media (prefers-color-scheme: dark) { :root { --fondo: #111; --texto: #eee; } }
@media print { nav, button { display: none; } }

h1 { font-size: clamp(1.5rem, 4vw, 2.5rem); }         /* tamaño fluido con mínimo y máximo */
.contenedor { width: min(100% - 32px, 1100px); margin-inline: auto; }
img, video { max-width: 100%; height: auto; }
.tabla-scroll { overflow-x: auto; }                    /* tablas anchas en celular */
```
Unidades: `px` fijo, `%` relativo al padre, `rem` relativo al html (16px por defecto), `em` relativo al elemento, `vw/vh` relativos a la ventana, `fr` fracción en grid, `ch` ancho de un carácter.

## 16. Transiciones, animaciones y efectos

```css
.boton { transition: background-color .2s ease, transform .2s; }
.boton:hover { background-color: #0847a8; transform: translateY(-2px); }
.boton:active { transform: scale(.98); }

@keyframes aparecer { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.tarjeta { animation: aparecer .3s ease-out both; }

@keyframes girar { to { transform: rotate(360deg); } }
.spinner { width: 24px; height: 24px; border: 3px solid #ddd; border-top-color: #0a5bd6; border-radius: 50%; animation: girar 1s linear infinite; }

@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
```

## 17. Componentes CSS listos para usar

```css
/* Modal */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,.5); display: grid; place-items: center; }
.modal > div { background: #fff; padding: 24px; border-radius: 12px; width: min(90%, 480px); }
/* o con HTML nativo: <dialog id="d">...</dialog>  →  d.showModal() / d.close() */

/* Badge */
.badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; background: #dcfce7; color: #166534; }

/* Barra de navegación sticky */
.nav { position: sticky; top: 0; z-index: 10; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.1); }

/* Truncar texto */
.truncar { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Tabla cebra */
tbody tr:nth-child(even) { background: #f8fafc; }
tbody tr:hover { background: #eef2ff; }
```

## 18. Bootstrap 5 en 5 minutos (si hay internet, ahorra mucho tiempo)

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<nav class="navbar navbar-expand-lg navbar-dark bg-primary"><div class="container">
  <a class="navbar-brand" href="#">ISTE</a></div></nav>
<div class="container my-4">
  <div class="row g-3">
    <div class="col-md-4"><div class="card"><div class="card-body">
      <h5 class="card-title">Título</h5><p class="card-text">Texto</p>
      <a href="#" class="btn btn-primary">Ir</a></div></div></div>
  </div>
  <form class="row g-3 mt-2">
    <div class="col-md-6"><label class="form-label">Nombre</label><input class="form-control" required></div>
    <div class="col-md-6"><label class="form-label">Carrera</label><select class="form-select"><option>Software</option></select></div>
    <div class="col-12"><button class="btn btn-success">Guardar</button></div>
  </form>
  <div class="alert alert-danger mt-3">Error</div>
  <table class="table table-striped table-hover mt-3"><thead class="table-dark"><tr><th>#</th><th>Nombre</th></tr></thead></table>
</div>
```
Grid de Bootstrap: 12 columnas; `col-md-6` = media fila desde tablets. Espaciado: `m-3`, `mt-2`, `p-4`, `px-2`, `gap-2`. Utilidades: `d-flex justify-content-between align-items-center`, `text-center`, `fw-bold`, `text-danger`, `w-100`.

## 19. Preguntas de entrevista HTML/CSS

- **¿Qué es el DOM?** Representación en árbol del documento HTML que JavaScript puede leer y modificar.
- **Block vs inline vs inline-block:** block ocupa toda la fila y acepta width/height. Inline fluye con el texto y no acepta width/height. Inline-block fluye con el texto pero acepta dimensiones.
- **`box-sizing: border-box`:** el width incluye padding y borde (más predecible).
- **Margin collapse:** los márgenes verticales de bloques adyacentes se fusionan (queda el mayor).
- **`position: absolute`** se posiciona respecto al ancestro más cercano con `position` distinto de static.
- **`display: none` vs `visibility: hidden`:** el primero quita el elemento del flujo; el segundo lo oculta pero conserva su espacio.
- **Pseudo-clase vs pseudo-elemento:** `:hover` (estado) vs `::before` (contenido generado).
- **SEO básico:** title y meta description, un h1, HTML semántico, alt en imágenes, URLs amigables, velocidad de carga y diseño responsive.
