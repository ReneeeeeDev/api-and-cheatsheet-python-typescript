# Cheatsheet SQL (MySQL / SQLite / SQL Server)

Practica con: `sqlite3 practica.db` (o en https://sqliteonline.com / phpMyAdmin de XAMPP).
Hay un script listo en `03-logica/sql/practica.sql` con tablas y datos para probar todo esto.

## 1. Crear base y tablas (DDL)

```sql
CREATE DATABASE instituto;          -- MySQL
USE instituto;

CREATE TABLE carreras (
  id INT AUTO_INCREMENT PRIMARY KEY,         -- SQLite: INTEGER PRIMARY KEY AUTOINCREMENT
  nombre VARCHAR(100) NOT NULL UNIQUE        -- SQL Server: id INT IDENTITY(1,1) PRIMARY KEY
);

CREATE TABLE estudiantes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cedula CHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(120),
  fecha_nacimiento DATE,
  carrera_id INT,
  activo BOOLEAN DEFAULT TRUE,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (carrera_id) REFERENCES carreras(id)
);

CREATE TABLE notas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  estudiante_id INT NOT NULL,
  materia VARCHAR(80) NOT NULL,
  nota DECIMAL(4,2) CHECK (nota BETWEEN 0 AND 10),
  FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

ALTER TABLE estudiantes ADD telefono VARCHAR(15);
ALTER TABLE estudiantes DROP COLUMN telefono;
DROP TABLE IF EXISTS tabla_vieja;
CREATE INDEX idx_nombre ON estudiantes(nombre);
```

Tipos comunes: `INT`, `DECIMAL(10,2)` (dinero), `VARCHAR(n)`, `TEXT`, `DATE`, `DATETIME`, `BOOLEAN`.

## 2. CRUD (DML)

```sql
INSERT INTO carreras (nombre) VALUES ('Software'), ('Enfermería'), ('Marketing');

INSERT INTO estudiantes (cedula, nombre, email, carrera_id)
VALUES ('1804567890', 'Ana Pérez', 'ana@mail.com', 1);

SELECT * FROM estudiantes;
SELECT nombre, email FROM estudiantes WHERE carrera_id = 1;

UPDATE estudiantes SET email = 'nuevo@mail.com' WHERE id = 1;   -- ¡SIEMPRE con WHERE!
DELETE FROM estudiantes WHERE id = 1;                           -- ¡SIEMPRE con WHERE!
```

## 3. Filtros

```sql
WHERE nota >= 7 AND materia = 'Programación'
WHERE carrera_id IN (1, 2)
WHERE nota BETWEEN 7 AND 10
WHERE nombre LIKE 'A%'        -- empieza con A
WHERE nombre LIKE '%ez'       -- termina en ez
WHERE nombre LIKE '%an%'      -- contiene "an"
WHERE email IS NULL / IS NOT NULL
ORDER BY nota DESC, nombre ASC
LIMIT 5                        -- SQL Server: SELECT TOP 5 ...
LIMIT 10 OFFSET 20             -- paginación (página 3 de 10)
SELECT DISTINCT materia FROM notas;
```

## 4. Funciones de agregación + GROUP BY + HAVING

```sql
SELECT COUNT(*) FROM estudiantes;
SELECT AVG(nota), MAX(nota), MIN(nota), SUM(nota) FROM notas;

-- Promedio por estudiante
SELECT estudiante_id, ROUND(AVG(nota), 2) AS promedio
FROM notas
GROUP BY estudiante_id;

-- Solo los que tienen promedio >= 8  (HAVING filtra grupos, WHERE filtra filas)
SELECT estudiante_id, AVG(nota) AS promedio
FROM notas
GROUP BY estudiante_id
HAVING AVG(nota) >= 8
ORDER BY promedio DESC;
```

Orden de ejecución: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

## 5. JOINs (seguro preguntan)

```sql
-- INNER JOIN: solo filas que coinciden en ambas tablas
SELECT e.nombre, c.nombre AS carrera
FROM estudiantes e
INNER JOIN carreras c ON e.carrera_id = c.id;

-- LEFT JOIN: todos los de la izquierda, aunque no tengan match (salen NULL)
SELECT c.nombre, COUNT(e.id) AS total_estudiantes
FROM carreras c
LEFT JOIN estudiantes e ON e.carrera_id = c.id
GROUP BY c.id, c.nombre;

-- Estudiantes SIN notas
SELECT e.nombre
FROM estudiantes e
LEFT JOIN notas n ON n.estudiante_id = e.id
WHERE n.id IS NULL;

-- 3 tablas: promedio por carrera
SELECT c.nombre AS carrera, ROUND(AVG(n.nota), 2) AS promedio
FROM carreras c
JOIN estudiantes e ON e.carrera_id = c.id
JOIN notas n ON n.estudiante_id = e.id
GROUP BY c.nombre
ORDER BY promedio DESC;
```

| JOIN | Devuelve |
|---|---|
| INNER | Solo coincidencias |
| LEFT | Todo de la izquierda + coincidencias |
| RIGHT | Todo de la derecha + coincidencias |
| FULL OUTER | Todo de ambas (MySQL no lo tiene: usar UNION de LEFT y RIGHT) |

## 6. Subconsultas

```sql
-- Estudiantes con nota mayor al promedio general
SELECT DISTINCT e.nombre
FROM estudiantes e JOIN notas n ON n.estudiante_id = e.id
WHERE n.nota > (SELECT AVG(nota) FROM notas);

-- Carreras que tienen al menos un estudiante
SELECT nombre FROM carreras
WHERE id IN (SELECT DISTINCT carrera_id FROM estudiantes);

-- El estudiante con la nota más alta
SELECT e.nombre, n.nota FROM notas n JOIN estudiantes e ON e.id = n.estudiante_id
WHERE n.nota = (SELECT MAX(nota) FROM notas);
```

## 7. Otras cosas útiles

```sql
-- CASE (if dentro de SQL)
SELECT nombre, nota,
  CASE WHEN nota >= 9 THEN 'Excelente'
       WHEN nota >= 7 THEN 'Aprobado'
       ELSE 'Reprobado' END AS estado
FROM notas n JOIN estudiantes e ON e.id = n.estudiante_id;

-- Texto y fechas (MySQL)
CONCAT(nombre, ' - ', email), UPPER(nombre), LENGTH(nombre), SUBSTRING(cedula, 1, 2)
NOW(), CURDATE(), YEAR(fecha_nacimiento), TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS edad
COALESCE(email, 'sin email')          -- reemplaza NULL

-- Vista
CREATE VIEW v_promedios AS
SELECT e.nombre, AVG(n.nota) promedio FROM estudiantes e JOIN notas n ON n.estudiante_id = e.id GROUP BY e.nombre;

-- Transacción
START TRANSACTION;
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;      -- o ROLLBACK;

-- Procedimiento almacenado (MySQL)
DELIMITER //
CREATE PROCEDURE notas_de(IN p_id INT)
BEGIN
  SELECT materia, nota FROM notas WHERE estudiante_id = p_id;
END //
DELIMITER ;
CALL notas_de(1);
```

## 8. Teoría rápida

- **PK (Primary Key)**: identifica cada fila, única y no nula. **FK (Foreign Key)**: referencia la PK de otra tabla.
- **Normalización**: 1FN = valores atómicos, sin grupos repetidos; 2FN = 1FN + todo depende de la PK completa; 3FN = 2FN + sin dependencias transitivas (un campo no clave no depende de otro no clave).
- **Relaciones**: 1:1, 1:N (FK en la tabla "muchos"), N:M (tabla intermedia, ej. `estudiante_materia`).
- **ACID**: Atomicidad, Consistencia, Aislamiento, Durabilidad.
- **SQL Injection**: nunca concatenar input del usuario en SQL; usar consultas parametrizadas (`?` o `%s`).
- **DDL** (CREATE, ALTER, DROP) vs **DML** (INSERT, UPDATE, DELETE, SELECT) vs **DCL** (GRANT, REVOKE).
- **DELETE vs TRUNCATE vs DROP**: borra filas (con WHERE) / vacía la tabla / elimina la tabla.

---

# PARTE 2 — AMPLIACIÓN

> Practica todo con `03-logica/sql/`: `practica.sql` (15 ejercicios), `ejercicios_extra.sql` (25 más) y `ejecutar_sql.py` para correrlos sin instalar nada.

## 9. Cómo ejecutar SQL (entornos)

| Herramienta | Cómo |
|---|---|
| **SQLite + Python** | `python ejecutar_sql.py archivo.sql` (incluido en el kit) |
| **sqlite3 CLI** | `sqlite3 base.db` → `.tables`, `.schema tabla`, `.headers on`, `.mode column`, `.read archivo.sql`, `.quit` |
| **phpMyAdmin (XAMPP)** | http://localhost/phpmyadmin → base → pestaña SQL |
| **MySQL CLI** | `C:\xampp\mysql\bin\mysql -u root` → `SHOW DATABASES; USE tienda; SHOW TABLES; DESCRIBE productos;` |
| **MySQL Workbench / DBeaver / HeidiSQL** | Conexión a localhost:3306, usuario root |
| **SQL Server** | SSMS o Azure Data Studio; `sqlcmd -S localhost -E` |
| **VS Code** | Extensión SQLite Viewer (ver .db) o "SQLTools" |
| **Online** | sqliteonline.com, db-fiddle.com (MySQL/PostgreSQL) |

## 10. Diferencias entre motores (lo que cambia)

| Concepto | MySQL | SQLite | SQL Server | PostgreSQL |
|---|---|---|---|---|
| Autoincremento | `INT AUTO_INCREMENT` | `INTEGER PRIMARY KEY AUTOINCREMENT` | `INT IDENTITY(1,1)` | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` |
| Limitar | `LIMIT 10 OFFSET 20` | igual | `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` / `TOP 10` | `LIMIT 10 OFFSET 20` |
| Concatenar | `CONCAT(a, b)` | `a \|\| b` | `a + b` / `CONCAT` | `a \|\| b` |
| Fecha actual | `NOW()`, `CURDATE()` | `datetime('now')`, `date('now')` | `GETDATE()` | `NOW()` |
| Booleano | `BOOLEAN` (= TINYINT) | INTEGER 0/1 | `BIT` | `BOOLEAN` |
| Texto | `VARCHAR(n)`, `TEXT` | `TEXT` | `NVARCHAR(n)` | `VARCHAR`, `TEXT` |
| Parámetro en código | `%s` (Python), `?` (Node) | `?` | `?` / `@p` | `%s` / `$1` |
| Si nulo | `IFNULL(x, 0)` / `COALESCE` | `IFNULL` / `COALESCE` | `ISNULL(x, 0)` / `COALESCE` | `COALESCE` |

## 11. Funciones de ventana (window functions): nivel pro

```sql
-- Ranking de estudiantes por promedio dentro de cada carrera
SELECT carrera, nombre, promedio,
       RANK()       OVER (PARTITION BY carrera ORDER BY promedio DESC) AS puesto,
       ROW_NUMBER() OVER (ORDER BY promedio DESC)                      AS fila_global,
       AVG(promedio) OVER (PARTITION BY carrera)                       AS prom_carrera
FROM v_promedios;

-- Total acumulado de ventas por fecha
SELECT fecha, monto, SUM(monto) OVER (ORDER BY fecha) AS acumulado FROM ventas;

-- Diferencia con la fila anterior
SELECT fecha, monto, monto - LAG(monto) OVER (ORDER BY fecha) AS variacion FROM ventas;
```
Soportado en MySQL 8+, SQLite 3.25+, SQL Server, PostgreSQL. **RANK** deja huecos tras empates (1,1,3), **DENSE_RANK** no (1,1,2), **ROW_NUMBER** nunca repite.

## 12. CTE (WITH): consultas legibles por pasos

```sql
WITH promedios AS (
  SELECT estudiante_id, AVG(nota) AS promedio FROM notas GROUP BY estudiante_id
),
mejores AS (
  SELECT * FROM promedios WHERE promedio >= 8
)
SELECT e.nombre, m.promedio
FROM mejores m JOIN estudiantes e ON e.id = m.estudiante_id
ORDER BY m.promedio DESC;
```

## 13. Más JOINs y operaciones de conjuntos

```sql
-- Self join: empleados con su jefe (la tabla se une consigo misma)
SELECT e.nombre AS empleado, j.nombre AS jefe
FROM empleados e LEFT JOIN empleados j ON j.id = e.jefe_id;

-- CROSS JOIN: todas las combinaciones (ej. todos los estudiantes × todas las materias)
SELECT e.nombre, m.nombre FROM estudiantes e CROSS JOIN materias m;

-- Tabla intermedia N:M
SELECT e.nombre, m.nombre
FROM matriculas mt
JOIN estudiantes e ON e.id = mt.estudiante_id
JOIN materias m ON m.id = mt.materia_id;

-- UNION (sin repetidos) / UNION ALL (con repetidos) / INTERSECT / EXCEPT
SELECT ciudad FROM estudiantes UNION SELECT ciudad FROM docentes;
SELECT id FROM estudiantes EXCEPT SELECT estudiante_id FROM notas;     -- sin notas (MySQL 8.0.31+)

-- EXISTS (suele ser más eficiente que IN con subconsultas grandes)
SELECT c.nombre FROM carreras c
WHERE EXISTS (SELECT 1 FROM estudiantes e WHERE e.carrera_id = c.id);
```

## 14. Índices, restricciones y rendimiento

```sql
CREATE INDEX idx_reservas_lab_fecha ON reservas (laboratorio_id, fecha);   -- acelera WHERE lab = ? AND fecha = ?
CREATE UNIQUE INDEX idx_email ON usuarios (email);
EXPLAIN SELECT ...;                         -- MySQL: ver si usa índice.  SQLite: EXPLAIN QUERY PLAN SELECT ...
ALTER TABLE productos ADD CONSTRAINT chk_precio CHECK (precio > 0);
ALTER TABLE notas ADD CONSTRAINT fk_est FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE;
```
- Un índice acelera búsquedas y JOIN, pero hace más lentos los INSERT/UPDATE y ocupa espacio.
- Indexa las columnas que usas en WHERE, JOIN y ORDER BY. Las PK ya tienen índice.
- `ON DELETE CASCADE` borra los hijos. `ON DELETE SET NULL` los deja huérfanos con NULL. `RESTRICT` (por defecto) impide borrar el padre.
- Evita `SELECT *` en producción, y evita `LIKE '%texto'` (no usa índice).

## 15. Triggers y procedimientos (MySQL)

```sql
-- Trigger: descontar stock automáticamente al registrar una venta
DELIMITER //
CREATE TRIGGER tr_descontar_stock AFTER INSERT ON detalle_ventas
FOR EACH ROW
BEGIN
  UPDATE productos SET stock = stock - NEW.cantidad WHERE id = NEW.producto_id;
END //

-- Procedimiento con parámetro de salida
CREATE PROCEDURE total_ventas(IN p_desde DATE, IN p_hasta DATE, OUT p_total DECIMAL(10,2))
BEGIN
  SELECT COALESCE(SUM(total), 0) INTO p_total FROM ventas WHERE fecha BETWEEN p_desde AND p_hasta;
END //

-- Función
CREATE FUNCTION con_iva(p DECIMAL(10,2)) RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
  RETURN ROUND(p * 1.15, 2);
END //
DELIMITER ;

CALL total_ventas('2026-01-01', '2026-12-31', @t); SELECT @t;
SELECT nombre, con_iva(precio) FROM productos;
```

## 16. Usuarios y permisos (DCL)

```sql
CREATE USER 'app'@'localhost' IDENTIFIED BY 'Clave_Segura1';
GRANT SELECT, INSERT, UPDATE, DELETE ON tienda.* TO 'app'@'localhost';
REVOKE DELETE ON tienda.* FROM 'app'@'localhost';
SHOW GRANTS FOR 'app'@'localhost';
```
La aplicación **no** debería conectarse como root: se crea un usuario con los permisos mínimos.

## 17. Normalización con ejemplo

Tabla sin normalizar:

| venta | cliente | tel_cliente | productos |
|---|---|---|---|
| 1 | Ana | 099... | Mouse, Teclado |

- **1FN** (valores atómicos): separar "Mouse, Teclado" en filas distintas.
- **2FN** (sin dependencias parciales): si la clave es (venta, producto), el cliente depende solo de venta, así que va a otra tabla `ventas`.
- **3FN** (sin dependencias transitivas): `tel_cliente` depende de cliente y no de venta, así que va a la tabla `clientes`.

Resultado: `clientes(id, nombre, telefono)`, `ventas(id, cliente_id, fecha)`, `productos(id, nombre, precio)`, `detalle_ventas(venta_id, producto_id, cantidad, precio_unitario)`.

> ¿Por qué guardar `precio_unitario` en el detalle si ya está en productos? Porque el precio puede cambiar después, y la venta debe conservar el precio histórico. Es una **desnormalización intencional**.

## 18. Modelos típicos que te pueden pedir (dibújalos)

**Biblioteca:** `autores`, `libros(autor_id)`, `socios`, `prestamos(libro_id, socio_id, fecha_prestamo, fecha_devolucion)`.
**Matrículas:** `estudiantes`, `materias(creditos)`, `periodos`, `matriculas(estudiante_id, materia_id, periodo_id, nota_final)`, con UNIQUE(estudiante_id, materia_id, periodo_id).
**Facturación:** `clientes`, `productos`, `facturas(cliente_id, fecha, subtotal, iva, total)`, `detalle_factura(factura_id, producto_id, cantidad, precio_unitario)`.
**Mesa de ayuda:** `usuarios(rol)`, `tickets(solicitante_id, tecnico_id, estado, prioridad, creado_en, cerrado_en)`, `comentarios(ticket_id, usuario_id, texto, fecha)`.
**Inventario de equipos:** `equipos(codigo, tipo, marca, estado, laboratorio_id)`, `laboratorios`, `mantenimientos(equipo_id, fecha, descripcion, costo)`.

## 19. Consultas típicas de entrevista (con solución)

```sql
-- Segundo salario más alto
SELECT MAX(salario) FROM empleados WHERE salario < (SELECT MAX(salario) FROM empleados);
-- o: SELECT DISTINCT salario FROM empleados ORDER BY salario DESC LIMIT 1 OFFSET 1;

-- Duplicados
SELECT email, COUNT(*) FROM usuarios GROUP BY email HAVING COUNT(*) > 1;

-- Eliminar duplicados conservando el de menor id
DELETE FROM usuarios WHERE id NOT IN (SELECT MIN(id) FROM usuarios GROUP BY email);

-- Top 3 por grupo (con ventana)
SELECT * FROM (
  SELECT carrera, nombre, promedio, ROW_NUMBER() OVER (PARTITION BY carrera ORDER BY promedio DESC) AS rn
  FROM v_promedios) t
WHERE rn <= 3;

-- Ventas por mes
SELECT strftime('%Y-%m', fecha) AS mes, SUM(total) FROM ventas GROUP BY mes;      -- SQLite
SELECT DATE_FORMAT(fecha, '%Y-%m') AS mes, SUM(total) FROM ventas GROUP BY mes;   -- MySQL

-- Clientes que nunca compraron
SELECT c.* FROM clientes c LEFT JOIN ventas v ON v.cliente_id = c.id WHERE v.id IS NULL;

-- Pivot simple (conteo por estado en columnas)
SELECT tecnico_id,
  SUM(CASE WHEN estado = 'abierto' THEN 1 ELSE 0 END) AS abiertos,
  SUM(CASE WHEN estado = 'cerrado' THEN 1 ELSE 0 END) AS cerrados
FROM tickets GROUP BY tecnico_id;
```
