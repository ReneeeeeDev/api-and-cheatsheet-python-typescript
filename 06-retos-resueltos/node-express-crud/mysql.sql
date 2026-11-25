CREATE DATABASE IF NOT EXISTS inventario CHARACTER SET utf8mb4;
USE inventario;

CREATE TABLE IF NOT EXISTS productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  categoria VARCHAR(60) NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Mouse inalámbrico', 'Periféricos', 15.50, 20),
('Teclado mecánico', 'Periféricos', 45.00, 8),
('Monitor 24"', 'Pantallas', 139.99, 3);
