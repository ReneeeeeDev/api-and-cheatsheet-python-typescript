# CRUD de Estudiantes — Python + Flask + SQLite

Aplicación web completa: listar, buscar, crear, editar y eliminar estudiantes, con relación a carreras (JOIN), validación de cédula ecuatoriana, mensajes flash, API REST JSON y pruebas automáticas.

## Ejecutar

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000. La base `instituto.db` se crea sola con datos de ejemplo.

## Pruebas
```bash
python -m unittest -v
```

## API
| Método | Ruta | Descripción |
|---|---|---|
| GET | /api/estudiantes?q=texto | Listar / buscar |
| GET | /api/estudiantes/1 | Obtener uno |
| POST | /api/estudiantes | Crear (JSON) |
| PUT | /api/estudiantes/1 | Actualizar |
| DELETE | /api/estudiantes/1 | Eliminar |

Ejemplo:
```bash
curl -X POST http://127.0.0.1:5000/api/estudiantes -H "Content-Type: application/json" -d "{\"cedula\":\"1804432126\",\"nombre\":\"Maria Diaz\",\"email\":\"m@mail.com\",\"carrera_id\":1,\"promedio\":8.5}"
```

## Qué estudiar de este código
1. `get_db()` / `close_db()`: una conexión por petición.
2. Consultas **parametrizadas** con `?` (evita SQL Injection).
3. `JOIN` entre estudiantes y carreras, y `LEFT JOIN + GROUP BY` para el resumen.
4. `validar()`: validación en servidor (nunca confiar solo en el HTML).
5. `cedula_valida()`: algoritmo módulo 10 (pregunta clásica en Ecuador).
6. Patrón POST → redirect → GET (evita reenviar el formulario al refrescar).
7. Herencia de plantillas Jinja (`base.html` + `{% block %}`).
8. Códigos HTTP correctos: 200, 201, 204, 400, 404.

## Reto para practicar (hazlo tú, 30–45 min)
- Agregar una tabla `materias` y `notas`, y una pantalla que muestre las notas de un estudiante con su promedio calculado en SQL.
- Paginar el listado (`LIMIT ? OFFSET ?`).
- Exportar el listado a CSV (`/exportar` con el módulo `csv` y `Response`).
