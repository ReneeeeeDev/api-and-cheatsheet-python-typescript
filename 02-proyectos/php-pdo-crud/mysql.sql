-- Script para MySQL (XAMPP). Ejecutar en phpMyAdmin → pestaña SQL.
CREATE DATABASE IF NOT EXISTS inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE inventario;

CREATE TABLE IF NOT EXISTS categorias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
  categoria_id INT NOT NULL,
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

INSERT INTO categorias (nombre) VALUES ('Periféricos'), ('Pantallas'), ('Redes');
INSERT INTO productos (codigo, nombre, precio, stock, categoria_id) VALUES
('P001', 'Mouse inalámbrico', 15.50, 20, 1),
('P002', 'Teclado mecánico', 45.00, 8, 1),
('P003', 'Monitor 24 pulgadas', 139.99, 3, 2);
