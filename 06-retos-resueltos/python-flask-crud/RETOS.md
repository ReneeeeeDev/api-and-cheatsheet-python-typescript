# Retos resueltos — Flask

Se ejecuta igual que el proyecto original:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py              # http://127.0.0.1:5000
python -m unittest -v      # 12 pruebas (9 originales + 3 de los retos)
```
> Si ya tenías un `instituto.db` del proyecto original, bórralo para que se creen las tablas nuevas.

## Reto 1: materias, notas y promedio calculado en SQL
- **Tablas nuevas** en `init_db()`: `materias(id, nombre, creditos)` y `notas(estudiante_id, materia_id, nota)`, con `UNIQUE(estudiante_id, materia_id)` para que un estudiante no tenga dos notas en la misma materia, y `ON DELETE CASCADE` para que al borrar al estudiante se borren sus notas.
- **Ruta** `GET/POST /estudiantes/<id>/notas` y la plantilla `templates/notas.html` (enlace "Notas" en cada fila del listado).
- **UPSERT:** `INSERT ... ON CONFLICT(estudiante_id, materia_id) DO UPDATE SET nota = excluded.nota`. Si ya existe la nota, la actualiza.
- **Promedios en SQL:** simple `AVG(n.nota)` y ponderado por créditos `SUM(nota * creditos) / SUM(creditos)`. `NULLIF(x, 0)` evita la división para cero.
- `actualizar_promedio()` recalcula la columna `promedio` del estudiante con una subconsulta cada vez que cambia una nota.

## Reto 2: paginación
- `listar(q, pagina)` agrega `LIMIT ? OFFSET ?` con `offset = (pagina - 1) * por_pagina`.
- `contar(q)` hace el `COUNT(*)` con el mismo filtro. Páginas = `ceil(total / por_pagina)`, calculado como `(total + n - 1) // n`.
- La página pedida se ajusta entre 1 y el máximo (`?pagina=99` muestra la última).
- En `index.html`, los enlaces Anterior/Siguiente **conservan la búsqueda** `q`.

## Reto 3: exportar a CSV
- Ruta `GET /exportar?q=...`: usa `csv.writer` sobre un `io.StringIO` (archivo en memoria) y responde con `Response(..., mimetype="text/csv")` y la cabecera `Content-Disposition: attachment` para que el navegador lo descargue.
- El `﻿` inicial (BOM) hace que **Excel** muestre bien las tildes.
- Botón "Exportar CSV" junto al buscador (exporta lo filtrado).
