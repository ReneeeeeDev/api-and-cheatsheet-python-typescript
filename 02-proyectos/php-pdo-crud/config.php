<?php
// Configuración y conexión a la base de datos (PDO).
// Por defecto usa SQLite (archivo inventario.db, sin instalar nada).
// Para usar MySQL de XAMPP: cambia USAR_MYSQL a true y crea la base "inventario" en phpMyAdmin
// (el archivo mysql.sql tiene el script).

const USAR_MYSQL = false;

function conectar(): PDO
{
    $opciones = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,        // lanza excepciones ante errores SQL
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,   // filas como arrays asociativos
        PDO::ATTR_EMULATE_PREPARES => false,
    ];
    if (USAR_MYSQL) {
        return new PDO("mysql:host=localhost;dbname=inventario;charset=utf8mb4", "root", "", $opciones);
    }
    $pdo = new PDO("sqlite:" . __DIR__ . "/inventario.db", null, null, $opciones);
    $pdo->exec("PRAGMA foreign_keys = ON");
    $pdo->exec("CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE)");
    $pdo->exec("CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL CHECK (precio > 0),
        stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
        categoria_id INTEGER NOT NULL REFERENCES categorias(id))");
    if ((int)$pdo->query("SELECT COUNT(*) FROM categorias")->fetchColumn() === 0) {
        $pdo->exec("INSERT INTO categorias (nombre) VALUES ('Periféricos'), ('Pantallas'), ('Redes')");
        $pdo->exec("INSERT INTO productos (codigo, nombre, precio, stock, categoria_id) VALUES
            ('P001', 'Mouse inalámbrico', 15.50, 20, 1),
            ('P002', 'Teclado mecánico', 45.00, 8, 1),
            ('P003', 'Monitor 24 pulgadas', 139.99, 3, 2)");
    }
    return $pdo;
}

// Escapa texto para imprimirlo en HTML (evita XSS). Úsalo SIEMPRE con datos.
function e($valor): string
{
    return htmlspecialchars((string)$valor, ENT_QUOTES, "UTF-8");
}

// Mensajes flash con sesión (sobreviven a una redirección)
session_start();
function flash(string $tipo, string $mensaje): void
{
    $_SESSION["flash"] = ["tipo" => $tipo, "mensaje" => $mensaje];
}
function tomar_flash(): ?array
{
    $f = $_SESSION["flash"] ?? null;
    unset($_SESSION["flash"]);
    return $f;
}
function redirigir(string $url): never
{
    header("Location: $url");
    exit;
}
