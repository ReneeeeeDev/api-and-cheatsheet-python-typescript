-- =====================================================================
-- PRÁCTICA SQL: crea las tablas, carga datos y resuelve los 15 ejercicios.
-- Compatible con SQLite y MySQL (en MySQL cambia INTEGER PRIMARY KEY
-- AUTOINCREMENT por INT AUTO_INCREMENT PRIMARY KEY).
--
-- SQLite:  sqlite3 practica.db < practica.sql
-- MySQL:   pégalo en phpMyAdmin (crea antes una BD y selecciónala)
-- Online:  https://sqliteonline.com
-- Intenta cada ejercicio ANTES de leer la solución de abajo.
-- =====================================================================

DROP TABLE IF EXISTS notas;
DROP TABLE IF EXISTS matriculas;
DROP TABLE IF EXISTS estudiantes;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS carreras;

CREATE TABLE carreras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE estudiantes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cedula CHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  ciudad VARCHAR(50),
  email VARCHAR(120),
  carrera_id INTEGER REFERENCES carreras(id)
);

CREATE TABLE materias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(80) NOT NULL,
  creditos INTEGER NOT NULL
);

CREATE TABLE notas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
  materia_id INTEGER NOT NULL REFERENCES materias(id),
  nota DECIMAL(4,2) NOT NULL
);

INSERT INTO carreras (nombre) VALUES ('Desarrollo de Software'), ('Enfermería'), ('Marketing Digital'), ('Gastronomía');

INSERT INTO estudiantes (cedula, nombre, ciudad, email, carrera_id) VALUES
('1710034065', 'Ana Pérez',     'Ambato', 'ana@mail.com',   1),
('0926687856', 'Luis Mora',     'Quito',  NULL,             1),
('1804432126', 'María Díaz',    'Ambato', 'maria@mail.com', 2),
('1803456789', 'Carlos Vega',   'Latacunga', 'carlos@mail.com', 3),
('1805555555', 'Andrea Ruiz',   'Ambato', 'andrea@mail.com', 1),
('1801111111', 'Pedro Lema',    'Riobamba', NULL,           NULL);

INSERT INTO materias (nombre, creditos) VALUES
('Programación I', 4), ('Base de Datos', 4), ('Anatomía', 3), ('Marketing', 3), ('Inglés', 2);

INSERT INTO notas (estudiante_id, materia_id, nota) VALUES
(1, 1, 9.5), (1, 2, 8.7), (1, 5, 9.0),
(2, 1, 6.0), (2, 2, 7.2), (2, 5, 5.5),
(3, 3, 8.0), (3, 5, 7.5),
(4, 4, 9.8), (4, 5, 6.8),
(5, 1, 7.9), (5, 2, 9.1);

-- =====================================================================
-- EJERCICIOS
--  1. Listar nombre y ciudad de los estudiantes de Ambato, ordenados por nombre.
--  2. Estudiantes que no tienen email.
--  3. Estudiantes cuyo nombre empieza con "A".
--  4. Cuántos estudiantes hay por ciudad (mayor a menor).
--  5. Nombre del estudiante con el nombre de su carrera (INNER JOIN).
--  6. Todas las carreras con su número de estudiantes, incluidas las que tienen 0 (LEFT JOIN).
--  7. Estudiantes que no están en ninguna carrera.
--  8. Promedio de notas de cada estudiante (nombre + promedio con 2 decimales), mayor a menor.
--  9. Estudiantes con promedio mayor o igual a 8 (HAVING).
-- 10. Nota máxima, mínima y promedio de cada materia.
-- 11. El estudiante con la nota más alta y en qué materia (subconsulta).
-- 12. Mostrar cada nota con su estado: >= 9 "Excelente", >= 7 "Aprobado", si no "Reprobado" (CASE).
-- 13. Promedio por carrera (3 tablas).
-- 14. Materias en las que nadie tiene nota.
-- 15. Subir 0.5 puntos (sin pasar de 10) a todas las notas de Inglés y luego eliminar
--     las notas menores a 6. (Hazlo con UPDATE y DELETE. Revisa el antes y el después.)
-- =====================================================================

-- ============================== SOLUCIONES ==============================

-- 1
SELECT nombre, ciudad FROM estudiantes WHERE ciudad = 'Ambato' ORDER BY nombre;

-- 2
SELECT nombre FROM estudiantes WHERE email IS NULL;

-- 3
SELECT nombre FROM estudiantes WHERE nombre LIKE 'A%';

-- 4
SELECT ciudad, COUNT(*) AS total FROM estudiantes GROUP BY ciudad ORDER BY total DESC;

-- 5
SELECT e.nombre, c.nombre AS carrera
FROM estudiantes e
INNER JOIN carreras c ON c.id = e.carrera_id;

-- 6
SELECT c.nombre, COUNT(e.id) AS estudiantes
FROM carreras c
LEFT JOIN estudiantes e ON e.carrera_id = c.id
GROUP BY c.id, c.nombre
ORDER BY estudiantes DESC;

-- 7
SELECT nombre FROM estudiantes WHERE carrera_id IS NULL;

-- 8
SELECT e.nombre, ROUND(AVG(n.nota), 2) AS promedio
FROM estudiantes e
JOIN notas n ON n.estudiante_id = e.id
GROUP BY e.id, e.nombre
ORDER BY promedio DESC;

-- 9
SELECT e.nombre, ROUND(AVG(n.nota), 2) AS promedio
FROM estudiantes e
JOIN notas n ON n.estudiante_id = e.id
GROUP BY e.id, e.nombre
HAVING AVG(n.nota) >= 8;

-- 10
SELECT m.nombre, MAX(n.nota) AS maxima, MIN(n.nota) AS minima, ROUND(AVG(n.nota), 2) AS promedio
FROM materias m
JOIN notas n ON n.materia_id = m.id
GROUP BY m.id, m.nombre;

-- 11
SELECT e.nombre, m.nombre AS materia, n.nota
FROM notas n
JOIN estudiantes e ON e.id = n.estudiante_id
JOIN materias m ON m.id = n.materia_id
WHERE n.nota = (SELECT MAX(nota) FROM notas);

-- 12
SELECT e.nombre, m.nombre AS materia, n.nota,
  CASE WHEN n.nota >= 9 THEN 'Excelente'
       WHEN n.nota >= 7 THEN 'Aprobado'
       ELSE 'Reprobado' END AS estado
FROM notas n
JOIN estudiantes e ON e.id = n.estudiante_id
JOIN materias m ON m.id = n.materia_id
ORDER BY e.nombre;

-- 13
SELECT c.nombre AS carrera, ROUND(AVG(n.nota), 2) AS promedio
FROM carreras c
JOIN estudiantes e ON e.carrera_id = c.id
JOIN notas n ON n.estudiante_id = e.id
GROUP BY c.id, c.nombre
ORDER BY promedio DESC;

-- 14
SELECT m.nombre
FROM materias m
LEFT JOIN notas n ON n.materia_id = m.id
WHERE n.id IS NULL;
-- (con los datos actuales todas tienen notas. Agrega una materia nueva para probarla)

-- 15
UPDATE notas
SET nota = CASE WHEN nota + 0.5 > 10 THEN 10 ELSE nota + 0.5 END
WHERE materia_id = (SELECT id FROM materias WHERE nombre = 'Inglés');

DELETE FROM notas WHERE nota < 6;

SELECT * FROM notas;
