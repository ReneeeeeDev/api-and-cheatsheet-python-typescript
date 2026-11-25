-- =====================================================================
-- 25 EJERCICIOS SQL EXTRA (16 a 40) — Facturación + Mesa de ayuda (tickets TI)
-- Ejecutar:  python ejecutar_sql.py ejercicios_extra.sql
-- Compatible con SQLite. Diferencias para MySQL anotadas con "MySQL:".
-- Intenta cada ejercicio antes de leer su solución (están justo debajo).
-- =====================================================================

DROP TABLE IF EXISTS comentarios;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS detalle_factura;
DROP TABLE IF EXISTS facturas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

-- ------------------------------------------------------- FACTURACIÓN
CREATE TABLE clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,         -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
  identificacion VARCHAR(13) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  ciudad VARCHAR(50),
  email VARCHAR(120)
);
CREATE TABLE productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
  stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
CREATE TABLE facturas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  numero VARCHAR(17) NOT NULL UNIQUE,
  cliente_id INTEGER NOT NULL REFERENCES clientes(id),
  fecha DATE NOT NULL,
  estado VARCHAR(10) NOT NULL DEFAULT 'emitida' CHECK (estado IN ('emitida', 'anulada'))
);
CREATE TABLE detalle_factura (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  factura_id INTEGER NOT NULL REFERENCES facturas(id) ON DELETE CASCADE,
  producto_id INTEGER NOT NULL REFERENCES productos(id),
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  precio_unitario DECIMAL(10,2) NOT NULL          -- precio histórico al momento de la venta
);

INSERT INTO clientes (identificacion, nombre, ciudad, email) VALUES
('1710034065', 'Ana Pérez', 'Ambato', 'ana@mail.com'),
('0926687856', 'Luis Mora', 'Quito', NULL),
('1804432126001', 'Comercial Díaz', 'Ambato', 'ventas@diaz.ec'),
('1803456789', 'Carlos Vega', 'Latacunga', 'carlos@mail.com'),
('1805555555', 'Sin Compras', 'Riobamba', NULL);

INSERT INTO productos (codigo, nombre, categoria, precio, stock) VALUES
('P001', 'Mouse inalámbrico', 'Periféricos', 15.50, 40),
('P002', 'Teclado mecánico', 'Periféricos', 45.00, 12),
('P003', 'Monitor 24"', 'Pantallas', 139.99, 5),
('P004', 'Router WiFi 6', 'Redes', 79.90, 0),
('P005', 'Cable HDMI', 'Accesorios', 6.50, 100),
('P006', 'Webcam HD', 'Periféricos', 35.00, 7);

INSERT INTO facturas (numero, cliente_id, fecha, estado) VALUES
('001-001-000000001', 1, '2026-07-05', 'emitida'),
('001-001-000000002', 2, '2026-07-18', 'emitida'),
('001-001-000000003', 3, '2026-08-02', 'emitida'),
('001-001-000000004', 1, '2026-08-20', 'emitida'),
('001-001-000000005', 4, '2026-09-10', 'anulada'),
('001-001-000000006', 3, '2026-09-15', 'emitida');

INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 2, 15.50), (1, 5, 3, 6.50),
(2, 2, 1, 45.00),
(3, 3, 2, 139.99), (3, 1, 5, 15.00), (3, 6, 2, 35.00),
(4, 2, 1, 42.00), (4, 5, 1, 6.50),
(5, 3, 1, 139.99),
(6, 1, 10, 14.50), (6, 2, 2, 45.00);

-- ------------------------------------------------------- MESA DE AYUDA (TI)
CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(100) NOT NULL,
  rol VARCHAR(10) NOT NULL CHECK (rol IN ('docente', 'tecnico', 'admin')),
  jefe_id INTEGER REFERENCES usuarios(id)            -- auto-referencia (para self join)
);
CREATE TABLE tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo VARCHAR(150) NOT NULL,
  solicitante_id INTEGER NOT NULL REFERENCES usuarios(id),
  tecnico_id INTEGER REFERENCES usuarios(id),
  prioridad VARCHAR(5) NOT NULL CHECK (prioridad IN ('alta', 'media', 'baja')),
  estado VARCHAR(12) NOT NULL DEFAULT 'abierto' CHECK (estado IN ('abierto', 'en_proceso', 'cerrado')),
  creado_en DATETIME NOT NULL,
  cerrado_en DATETIME
);
CREATE TABLE comentarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
  texto TEXT NOT NULL,
  fecha DATETIME NOT NULL
);

INSERT INTO usuarios (nombre, rol, jefe_id) VALUES
('Marta Jefa TI', 'admin', NULL),
('Pablo Técnico', 'tecnico', 1),
('Sofía Técnica', 'tecnico', 1),
('Ing. Ruiz', 'docente', NULL),
('Lic. Andrade', 'docente', NULL);

INSERT INTO tickets (titulo, solicitante_id, tecnico_id, prioridad, estado, creado_en, cerrado_en) VALUES
('Proyector del Lab 002 no enciende', 4, 2, 'alta', 'cerrado', '2026-09-01 08:10', '2026-09-01 10:40'),
('Sin internet en Lab 001', 5, 3, 'alta', 'cerrado', '2026-09-02 09:00', '2026-09-02 09:45'),
('Instalar Visual Studio Code', 4, 2, 'media', 'cerrado', '2026-09-03 14:00', '2026-09-04 11:00'),
('Impresora sin tóner', 5, NULL, 'baja', 'abierto', '2026-09-20 16:00', NULL),
('Cuenta de correo bloqueada', 4, 3, 'alta', 'en_proceso', '2026-09-24 07:30', NULL),
('Actualizar Windows en 20 PCs', 5, 2, 'media', 'en_proceso', '2026-09-22 10:00', NULL);

INSERT INTO comentarios (ticket_id, usuario_id, texto, fecha) VALUES
(1, 2, 'Se cambió el cable de poder', '2026-09-01 10:30'),
(1, 4, 'Gracias, funciona', '2026-09-01 10:45'),
(2, 3, 'Switch reiniciado', '2026-09-02 09:40'),
(5, 3, 'Se solicitó desbloqueo a proveedor', '2026-09-24 08:00');

-- =====================================================================
-- EJERCICIOS Y SOLUCIONES
-- =====================================================================

-- 16. Total de cada factura (subtotal, IVA 15 % y total), solo las emitidas.
SELECT f.numero,
       ROUND(SUM(d.cantidad * d.precio_unitario), 2)        AS subtotal,
       ROUND(SUM(d.cantidad * d.precio_unitario) * 0.15, 2) AS iva,
       ROUND(SUM(d.cantidad * d.precio_unitario) * 1.15, 2) AS total
FROM facturas f
JOIN detalle_factura d ON d.factura_id = f.id
WHERE f.estado = 'emitida'
GROUP BY f.id, f.numero
ORDER BY f.numero;

-- 17. Total comprado por cliente (incluye clientes sin compras con 0), mayor a menor.
SELECT c.nombre, COALESCE(ROUND(SUM(d.cantidad * d.precio_unitario), 2), 0) AS total_comprado
FROM clientes c
LEFT JOIN facturas f ON f.cliente_id = c.id AND f.estado = 'emitida'   -- el filtro va en el ON para no perder clientes
LEFT JOIN detalle_factura d ON d.factura_id = f.id
GROUP BY c.id, c.nombre
ORDER BY total_comprado DESC;

-- 18. Clientes que nunca han comprado.
SELECT c.nombre FROM clientes c
WHERE NOT EXISTS (SELECT 1 FROM facturas f WHERE f.cliente_id = c.id);

-- 19. Productos más vendidos (unidades) en facturas emitidas, top 3.
SELECT p.nombre, SUM(d.cantidad) AS unidades
FROM detalle_factura d
JOIN productos p ON p.id = d.producto_id
JOIN facturas f ON f.id = d.factura_id AND f.estado = 'emitida'
GROUP BY p.id, p.nombre
ORDER BY unidades DESC
LIMIT 3;

-- 20. Productos que nunca se han vendido.
SELECT p.codigo, p.nombre FROM productos p
LEFT JOIN detalle_factura d ON d.producto_id = p.id
WHERE d.id IS NULL;

-- 21. Ventas por mes (solo emitidas).  MySQL: DATE_FORMAT(f.fecha, '%Y-%m')
SELECT strftime('%Y-%m', f.fecha) AS mes, COUNT(DISTINCT f.id) AS facturas,
       ROUND(SUM(d.cantidad * d.precio_unitario), 2) AS vendido
FROM facturas f JOIN detalle_factura d ON d.factura_id = f.id
WHERE f.estado = 'emitida'
GROUP BY mes ORDER BY mes;

-- 22. Ventas por categoría con porcentaje sobre el total.
SELECT p.categoria,
       ROUND(SUM(d.cantidad * d.precio_unitario), 2) AS vendido,
       ROUND(100.0 * SUM(d.cantidad * d.precio_unitario) /
             (SELECT SUM(d2.cantidad * d2.precio_unitario) FROM detalle_factura d2
              JOIN facturas f2 ON f2.id = d2.factura_id WHERE f2.estado = 'emitida'), 1) AS porcentaje
FROM detalle_factura d
JOIN productos p ON p.id = d.producto_id
JOIN facturas f ON f.id = d.factura_id AND f.estado = 'emitida'
GROUP BY p.categoria ORDER BY vendido DESC;

-- 23. Ventas con descuento: líneas donde se vendió por debajo del precio actual de lista.
SELECT f.numero, p.nombre, d.precio_unitario, p.precio AS precio_lista,
       ROUND(p.precio - d.precio_unitario, 2) AS descuento_unitario
FROM detalle_factura d
JOIN productos p ON p.id = d.producto_id
JOIN facturas f ON f.id = d.factura_id
WHERE d.precio_unitario < p.precio;

-- 24. Productos con stock crítico (< 10) y su valor inmovilizado, con CASE para el nivel.
SELECT codigo, nombre, stock,
       CASE WHEN stock = 0 THEN 'AGOTADO' WHEN stock < 6 THEN 'CRÍTICO' ELSE 'BAJO' END AS nivel,
       ROUND(precio * stock, 2) AS valor_en_bodega
FROM productos WHERE stock < 10 ORDER BY stock;

-- 25. Clientes cuya compra total supera el promedio de compra por cliente (subconsulta + HAVING).
SELECT c.nombre, ROUND(SUM(d.cantidad * d.precio_unitario), 2) AS total
FROM clientes c
JOIN facturas f ON f.cliente_id = c.id AND f.estado = 'emitida'
JOIN detalle_factura d ON d.factura_id = f.id
GROUP BY c.id, c.nombre
HAVING SUM(d.cantidad * d.precio_unitario) > (
  SELECT AVG(total_cliente) FROM (
    SELECT SUM(d3.cantidad * d3.precio_unitario) AS total_cliente
    FROM facturas f3 JOIN detalle_factura d3 ON d3.factura_id = f3.id
    WHERE f3.estado = 'emitida' GROUP BY f3.cliente_id) t);

-- 26. Ranking de clientes con función de ventana (RANK).
SELECT nombre, total, RANK() OVER (ORDER BY total DESC) AS puesto
FROM (SELECT c.nombre, ROUND(SUM(d.cantidad * d.precio_unitario), 2) AS total
      FROM clientes c JOIN facturas f ON f.cliente_id = c.id AND f.estado = 'emitida'
      JOIN detalle_factura d ON d.factura_id = f.id GROUP BY c.id, c.nombre) t;

-- 27. Venta acumulada en el tiempo (running total) con CTE + ventana.
WITH por_factura AS (
  SELECT f.fecha, f.numero, SUM(d.cantidad * d.precio_unitario) AS monto
  FROM facturas f JOIN detalle_factura d ON d.factura_id = f.id
  WHERE f.estado = 'emitida' GROUP BY f.id
)
SELECT fecha, numero, ROUND(monto, 2) AS monto,
       ROUND(SUM(monto) OVER (ORDER BY fecha), 2) AS acumulado
FROM por_factura ORDER BY fecha;

-- 28. Clientes de Ambato que compraron productos de la categoría Periféricos (sin repetir).
SELECT DISTINCT c.nombre
FROM clientes c
JOIN facturas f ON f.cliente_id = c.id
JOIN detalle_factura d ON d.factura_id = f.id
JOIN productos p ON p.id = d.producto_id
WHERE c.ciudad = 'Ambato' AND p.categoria = 'Periféricos';

-- 29. Tipo de cliente según su identificación: 10 dígitos = persona, 13 = RUC.
SELECT nombre, identificacion,
       CASE LENGTH(identificacion) WHEN 10 THEN 'Persona natural' WHEN 13 THEN 'RUC' ELSE 'Inválido' END AS tipo,
       COALESCE(email, 'sin email') AS email
FROM clientes;

-- 30. Descontar del stock lo vendido en la factura 6 (UPDATE con subconsulta correlacionada).
UPDATE productos
SET stock = stock - (SELECT SUM(d.cantidad) FROM detalle_factura d WHERE d.factura_id = 6 AND d.producto_id = productos.id)
WHERE id IN (SELECT producto_id FROM detalle_factura WHERE factura_id = 6);
SELECT codigo, stock FROM productos WHERE id IN (1, 2);

-- ------------------------------------------------------- TICKETS

-- 31. Tickets abiertos o en proceso, con nombre del solicitante y del técnico ("Sin asignar" si no hay).
SELECT t.id, t.titulo, s.nombre AS solicitante, COALESCE(tec.nombre, 'Sin asignar') AS tecnico, t.prioridad, t.estado
FROM tickets t
JOIN usuarios s ON s.id = t.solicitante_id
LEFT JOIN usuarios tec ON tec.id = t.tecnico_id              -- misma tabla usada dos veces con alias distintos
WHERE t.estado <> 'cerrado'
ORDER BY CASE t.prioridad WHEN 'alta' THEN 1 WHEN 'media' THEN 2 ELSE 3 END, t.creado_en;

-- 32. Carga de trabajo por técnico: tickets por estado en columnas (pivot con SUM(CASE)).
SELECT u.nombre,
       SUM(CASE WHEN t.estado = 'abierto' THEN 1 ELSE 0 END)    AS abiertos,
       SUM(CASE WHEN t.estado = 'en_proceso' THEN 1 ELSE 0 END) AS en_proceso,
       SUM(CASE WHEN t.estado = 'cerrado' THEN 1 ELSE 0 END)    AS cerrados
FROM usuarios u LEFT JOIN tickets t ON t.tecnico_id = u.id
WHERE u.rol = 'tecnico'
GROUP BY u.id, u.nombre;

-- 33. Tiempo promedio de resolución en horas por técnico.  MySQL: TIMESTAMPDIFF(MINUTE, creado_en, cerrado_en) / 60
SELECT u.nombre,
       ROUND(AVG((julianday(t.cerrado_en) - julianday(t.creado_en)) * 24), 2) AS horas_promedio
FROM tickets t JOIN usuarios u ON u.id = t.tecnico_id
WHERE t.estado = 'cerrado'
GROUP BY u.id, u.nombre;

-- 34. Tickets de prioridad alta resueltos en menos de 2 horas (cumplimiento de SLA).
SELECT id, titulo, ROUND((julianday(cerrado_en) - julianday(creado_en)) * 24, 2) AS horas,
       CASE WHEN (julianday(cerrado_en) - julianday(creado_en)) * 24 <= 2 THEN 'Cumple' ELSE 'No cumple' END AS sla
FROM tickets WHERE prioridad = 'alta' AND estado = 'cerrado';

-- 35. Empleados con su jefe (self join).
SELECT e.nombre AS empleado, e.rol, COALESCE(j.nombre, '—') AS jefe
FROM usuarios e LEFT JOIN usuarios j ON j.id = e.jefe_id;

-- 36. Tickets sin ningún comentario.
SELECT t.id, t.titulo FROM tickets t
WHERE t.id NOT IN (SELECT DISTINCT ticket_id FROM comentarios);

-- 37. Último comentario de cada ticket (subconsulta correlacionada con MAX).
SELECT t.id, t.titulo, c.texto, c.fecha
FROM tickets t
JOIN comentarios c ON c.ticket_id = t.id
WHERE c.fecha = (SELECT MAX(c2.fecha) FROM comentarios c2 WHERE c2.ticket_id = t.id);

-- 38. Asignar el ticket sin técnico al técnico con menos tickets activos.
UPDATE tickets
SET tecnico_id = (
  SELECT u.id FROM usuarios u
  LEFT JOIN tickets t2 ON t2.tecnico_id = u.id AND t2.estado <> 'cerrado'
  WHERE u.rol = 'tecnico'
  GROUP BY u.id ORDER BY COUNT(t2.id), u.id LIMIT 1),
    estado = 'en_proceso'
WHERE tecnico_id IS NULL;
SELECT id, titulo, tecnico_id, estado FROM tickets WHERE id = 4;

-- 39. Cerrar un ticket registrando la fecha y un comentario (dos sentencias en una transacción).
BEGIN;
UPDATE tickets SET estado = 'cerrado', cerrado_en = '2026-09-25 12:00' WHERE id = 5;
INSERT INTO comentarios (ticket_id, usuario_id, texto, fecha) VALUES (5, 3, 'Cuenta desbloqueada', '2026-09-25 12:00');
COMMIT;
SELECT id, estado, cerrado_en FROM tickets WHERE id = 5;

-- 40. Vista de reporte y consulta sobre la vista.
DROP VIEW IF EXISTS v_resumen_tickets;
CREATE VIEW v_resumen_tickets AS
SELECT t.id, t.titulo, t.prioridad, t.estado, s.nombre AS solicitante, COALESCE(tec.nombre, 'Sin asignar') AS tecnico,
       (SELECT COUNT(*) FROM comentarios c WHERE c.ticket_id = t.id) AS comentarios
FROM tickets t JOIN usuarios s ON s.id = t.solicitante_id LEFT JOIN usuarios tec ON tec.id = t.tecnico_id;
SELECT tecnico, COUNT(*) AS tickets, SUM(comentarios) AS comentarios FROM v_resumen_tickets GROUP BY tecnico;
