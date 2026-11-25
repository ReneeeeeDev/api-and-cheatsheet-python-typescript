# Simulacro de prueba práctica (3 horas)

Hazlo cronometrado, como si fuera mañana. Usa el lenguaje que domines (Python/Flask, Node/Express, PHP o Java). No mires los proyectos de `02-proyectos` salvo que te quedes atascado más de 15 minutos (y anótalo: eso es lo que debes repasar).

---

## Enunciado: "Sistema de reserva de laboratorios"

El Instituto necesita un sistema web para que los docentes reserven laboratorios de cómputo.

### Requisitos funcionales
1. **Laboratorios** (CRUD completo): código (único, ej. `LAB-002`), nombre, piso, capacidad (entero > 0), estado (`disponible` / `mantenimiento`).
2. **Reservas**: docente (nombre), laboratorio, fecha, hora inicio, hora fin, motivo.
   - No se puede reservar un laboratorio en `mantenimiento`.
   - La hora fin debe ser mayor que la hora inicio.
   - **No puede haber dos reservas del mismo laboratorio que se crucen en fecha y horario.**
3. **Listado de reservas** con filtro por fecha y por laboratorio, mostrando el nombre del laboratorio (JOIN).
4. **Reporte**: número de reservas y horas totales reservadas por laboratorio.
5. **API REST** en JSON para laboratorios (al menos GET y POST).

### Requisitos técnicos
- Base de datos relacional (MySQL o SQLite) con clave foránea.
- Validaciones en el servidor con mensajes claros.
- Interfaz HTML/CSS usable (formularios con `label`, tabla, mensajes de éxito/error).
- Repositorio Git con al menos 5 commits con mensajes descriptivos.
- `README.md` con instrucciones de instalación y ejecución.
- **Extra**: pruebas unitarias de la validación de choque de horarios; diseño responsive; despliegue.

---

## Plan de tiempo sugerido

| Minuto | Actividad |
|---|---|
| 0–15 | Leer todo, dibujar las 2 tablas, decidir rutas. `git init` + primer commit. |
| 15–45 | Crear BD + CRUD de laboratorios (listar y crear primero). Commit. |
| 45–60 | Editar/eliminar laboratorios + API JSON. Commit. |
| 60–110 | Reservas: formulario, validaciones y **choque de horarios**. Commit. |
| 110–135 | Listado con filtros + reporte. Commit. |
| 135–160 | Estilos, mensajes, README. Commit. |
| 160–180 | Probar todo como usuario, corregir, commit final. |

**Regla de oro:** a los 90 minutos debes tener algo que funcione de punta a punta, aunque sea feo.

---

## Pista clave: detectar choque de horarios

Dos intervalos `[inicio1, fin1)` y `[inicio2, fin2)` se cruzan si:
```
inicio1 < fin2  AND  inicio2 < fin1
```
En SQL:
```sql
SELECT COUNT(*) FROM reservas
WHERE laboratorio_id = ? AND fecha = ?
  AND hora_inicio < ?      -- fin de la nueva
  AND ? < hora_fin         -- inicio de la nueva
  AND id <> ?;             -- al editar, excluir la propia reserva (usa 0 al crear)
```
Las horas en formato `HH:MM` ("08:00", "14:30") se pueden comparar como texto correctamente.

## Esquema sugerido
```sql
CREATE TABLE laboratorios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(80) NOT NULL,
  piso INTEGER NOT NULL,
  capacidad INTEGER NOT NULL CHECK (capacidad > 0),
  estado VARCHAR(20) NOT NULL DEFAULT 'disponible'
);
CREATE TABLE reservas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  laboratorio_id INTEGER NOT NULL REFERENCES laboratorios(id),
  docente VARCHAR(100) NOT NULL,
  fecha DATE NOT NULL,
  hora_inicio CHAR(5) NOT NULL,
  hora_fin CHAR(5) NOT NULL,
  motivo VARCHAR(200)
);
```

Reporte de horas (SQLite):
```sql
SELECT l.nombre, COUNT(r.id) AS reservas,
  ROUND(COALESCE(SUM((strftime('%s', r.hora_fin) - strftime('%s', r.hora_inicio)) / 3600.0), 0), 1) AS horas
FROM laboratorios l LEFT JOIN reservas r ON r.laboratorio_id = l.id
GROUP BY l.id;
```
MySQL: `SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fin, r.hora_inicio)) / 3600)`.

---

## Rúbrica (así te pueden evaluar)

| Criterio | Peso | Qué se mira |
|---|---|---|
| Funcionalidad | 35 % | CRUD completo, reservas, filtros, reporte funcionan |
| Reglas de negocio | 20 % | Validaciones, choque de horarios, mantenimiento |
| Base de datos | 15 % | Modelo correcto, FK, consultas con JOIN/GROUP BY |
| Calidad de código | 15 % | Nombres claros, organización en archivos, sin código repetido |
| Git y documentación | 10 % | Commits frecuentes y descriptivos, README |
| Interfaz | 5 % | Usable, mensajes claros, responsive |

## Autoevaluación al terminar
- [ ] ¿Se puede crear, ver, editar y borrar laboratorios?
- [ ] ¿Rechaza una reserva que se cruza (ej. 08:00–10:00 vs 09:00–11:00)?
- [ ] ¿Acepta reservas contiguas (08:00–10:00 y 10:00–12:00)?
- [ ] ¿Rechaza hora fin <= hora inicio?
- [ ] ¿Rechaza laboratorios en mantenimiento?
- [ ] ¿Qué pasa si envío el formulario vacío?
- [ ] ¿Qué pasa si elimino un laboratorio que tiene reservas? (decide: impedirlo con un mensaje)
- [ ] ¿El README permite a otra persona ejecutarlo en 2 minutos?

## Otros enunciados posibles para practicar (mismo esqueleto)
1. **Inventario de equipos** del instituto con préstamos a estudiantes (no prestar si ya está prestado).
2. **Registro de asistencia** a un evento: inscripción con cédula válida, cupo máximo, reporte de asistentes.
3. **Matrículas**: estudiantes, materias, matrícula (máximo 7 materias, sin repetir), reporte de créditos.
4. **Mesa de ayuda (tickets de soporte TI)**: crear ticket, asignar técnico, cambiar estado (abierto → en proceso → cerrado), reporte por estado. Muy acorde a la Unidad de TI.
5. Consumir una API pública (`https://jsonplaceholder.typicode.com/users`) y mostrarla en una tabla con buscador en React.
