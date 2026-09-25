# Inventario — PHP 8 + PDO (SQLite o MySQL)

CRUD de productos con categorías (JOIN), búsqueda y filtro, validaciones en el servidor, mensajes flash con sesión, protección XSS/SQL Injection y una API REST en JSON.

## Ejecutar: opción A, servidor integrado de PHP (sin XAMPP)
```bash
cd 02-proyectos/php-pdo-crud
php -S localhost:8080            # con XAMPP: C:\xampp\php\php.exe -S localhost:8080
```
Abre http://localhost:8080. Usa SQLite: se crea `inventario.db` con datos de ejemplo.

## Ejecutar: opción B, XAMPP + Apache
1. Copia la carpeta `php-pdo-crud` a `C:\xampp\htdocs\`.
2. Start Apache en el XAMPP Control Panel.
3. Abre http://localhost/php-pdo-crud/

## Usar MySQL en vez de SQLite
1. Start MySQL en XAMPP → http://localhost/phpmyadmin → pestaña **SQL** → pega `mysql.sql` → Continuar.
2. En `config.php` cambia `const USAR_MYSQL = false;` por `true`.

> Si da *"could not find driver"* con SQLite: en `C:\xampp\php\php.ini` quita el `;` de `extension=pdo_sqlite` (y de `extension=sqlite3`) y reinicia Apache.
> Requiere PHP 8.1 o superior (`php -v`).

## Probar la API
```bash
curl http://localhost:8080/api.php
curl http://localhost:8080/api.php?id=1
curl -X POST http://localhost:8080/api.php -d "{\"codigo\":\"P010\",\"nombre\":\"Cable HDMI\",\"precio\":5,\"stock\":10,\"categoria_id\":2}"
curl -X PUT "http://localhost:8080/api.php?id=1" -d "{\"stock\":99}"
curl -X DELETE "http://localhost:8080/api.php?id=2"
```

## Estructura
```
config.php        conexión PDO, creación de tablas, helpers (e(), flash, redirigir)
validaciones.php  reglas de negocio
index.php         controlador + vista: listar, crear, editar, eliminar, buscar
api.php           API REST JSON (GET/POST/PUT/DELETE)
styles.css
mysql.sql         script para MySQL
```

## Qué estudiar
- `PDO::prepare` + `execute([...])`: consultas preparadas contra SQL Injection.
- `htmlspecialchars` (función `e()`): contra XSS.
- Patrón POST → redirect → GET con `header("Location: ...")` + `exit`.
- `$_GET`, `$_POST`, `$_SESSION`, `$_SERVER["REQUEST_METHOD"]`, `php://input` para leer JSON.
- `http_response_code()` para los códigos HTTP de la API.
- Separar configuración, validaciones y vistas, aunque sea en un proyecto pequeño.

## Retos
1. Agregar el CRUD de categorías, sin permitir eliminar una categoría que tenga productos.
2. Paginación con `LIMIT ? OFFSET ?`.
3. Login con `password_hash()` / `password_verify()` y `$_SESSION`.
