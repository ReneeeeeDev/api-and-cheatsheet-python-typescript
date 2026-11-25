# Mi práctica

Aquí van **mis intentos**, separados de las soluciones del kit. La idea es escribir el código yo y comparar con el solucionario solo cuando algo no funcione.

## reservas-flask: avance de `08-guia-desde-cero/GUIA-1-FLASK.md`

| Paso | Estado | Archivos |
|---|---|---|
| 0–2. Herramientas, diseño y estructura | ✅ | `.gitignore` |
| 3. Base de datos | ✅ | `schema.sql`, `db.py` |
| 4. Reglas de negocio | ✅ | `validaciones.py` |
| 5. App base, plantilla y estilos | ⬜ siguiente | `app.py`, `templates/base.html`, `templates/inicio.html`, `static/css/styles.css` |
| 6. CRUD de laboratorios | ⬜ | rutas + `templates/laboratorios.html` |
| 7. Reservas y filtros | ⬜ | rutas + `templates/reservas.html` |
| 8. Reporte | ⬜ | ruta + `templates/reporte.html` |
| 9. API REST en JSON | ⬜ | rutas `/api/...` |
| 10. Pruebas automáticas | ⬜ | `tests/test_app.py` |
| 11–12. README y revisión final | ⬜ | `README.md` |

**Error encontrado y corregido:** en `schema.sql` decía `CREATE TABLE IF NOT EXIST` (sin la S final), un error de sintaxis que impedía arrancar la app. Lección: ejecutar el esquema apenas se escribe, por ejemplo con `python -c "import sqlite3; sqlite3.connect(':memory:').executescript(open('schema.sql').read())"`.

### Continuar

```bash
cd mi-practica/reservas-flask
python -m venv venv
venv\Scripts\activate            # Linux/Mac: source venv/bin/activate
pip install flask pytest
# seguir la guía desde el Paso 5
```

Comparar con la solución: `08-guia-desde-cero/solucionario/reservas-flask/`. En VS Code, clic derecho sobre un archivo → *Select for Compare*, y luego sobre el otro → *Compare with Selected*.

## Ideas para más práctica

- Rehacer `reservas-flask` desde cero en 3 horas, cronometrado (como en la prueba real).
- Hacer la misma app con Express (`GUIA-2-EXPRESS.md`) en `mi-practica/reservas-express/`.
