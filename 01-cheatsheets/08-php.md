# Cheatsheet PHP completo (PHP 8)

> Ejemplo ejecutable: `05-ejemplos/php/basicos.php`. Proyecto CRUD completo: `02-proyectos/php-pdo-crud/`.

## 1. Cómo se ejecuta PHP

| Forma | Comando / lugar | Uso |
|---|---|---|
| Consola | `php archivo.php` | scripts, pruebas de lógica |
| Servidor integrado | `php -S localhost:8080` (en la carpeta del proyecto) | desarrollo rápido sin XAMPP |
| XAMPP (Apache) | archivos en `C:\xampp\htdocs\proyecto\` → http://localhost/proyecto/ | lo típico en Ecuador / institutos |
| Interactivo | `php -a` | probar líneas |
| Ver configuración | `php -v`, `php -m` (módulos), `php --ini` | diagnosticar |

En Windows con XAMPP, si `php` "no se reconoce": usa `C:\xampp\php\php.exe`, o agrega `C:\xampp\php` al PATH.

Errores visibles en desarrollo (al inicio del archivo):
```php
ini_set('display_errors', '1');
error_reporting(E_ALL);
```

## 2. Sintaxis esencial

```php
<?php
declare(strict_types=1);                 // tipos estrictos (recomendado)

$nombre = "Ana";                          // variables con $
const IVA = 0.15;                         // constante
echo "Hola $nombre\n";                    // comillas dobles interpolan
echo 'Literal $nombre';                   // simples no
echo "Total: " . ($precio * (1 + IVA));   // concatenar con .
$x ??= 10;                                // asigna si es null
$edad = (int)"25"; $p = (float)"3.5"; $s = (string)10;
var_dump($x); print_r($array);            // depurar
isset($x); empty($x); is_null($x); is_numeric("12.5"); is_array($a);
```

Comparación: `==` compara valor con conversión, `===` compara valor y tipo. `<=>` devuelve -1, 0 o 1 (útil en usort).

## 3. Strings

```php
strlen($s); mb_strlen($s);              // mb_ para tildes/ñ
strtoupper($s); strtolower($s); ucfirst($s); ucwords($s); trim($s);
str_contains($s, "x"); str_starts_with($s, "a"); str_ends_with($s, "z");   // PHP 8
strpos($s, "o"); substr($s, 0, 4); str_replace("a", "b", $s); strrev($s);
explode(",", "a,b,c"); implode("-", $arr); str_pad("7", 3, "0", STR_PAD_LEFT);
sprintf("%05.2f", 3.14159); number_format(1234.5, 2, ",", ".");   // 1.234,50
htmlspecialchars($texto, ENT_QUOTES, "UTF-8");                     // ¡contra XSS!
preg_match('/^\d{10}$/', $cedula); preg_replace('/\s+/', ' ', $s);
```

## 4. Arrays

```php
$nums = [5, 3, 8];
$nums[] = 10;                                    // push
array_push($nums, 1); array_pop($nums); array_shift($nums); array_unshift($nums, 0);
count($nums); in_array(8, $nums); array_search(8, $nums); array_sum($nums); max($nums);
sort($nums); rsort($nums);                       // ordena valores (reindexa)
$persona = ["nombre" => "Ana", "edad" => 25];    // asociativo
asort($a); arsort($a); ksort($a); krsort($a);    // ordenar asociativos por valor/clave
usort($lista, fn($a, $b) => $a["nota"] <=> $b["nota"]);
array_map(fn($x) => $x * 2, $nums);
array_filter($nums, fn($x) => $x > 3);           // conserva claves → array_values() para reindexar
array_reduce($nums, fn($acc, $x) => $acc + $x, 0);
array_column($filas, "nombre");                  // extrae una columna de un array de filas
array_keys($a); array_values($a); array_merge($a, $b); array_unique($a); array_slice($a, 1, 2);
array_key_exists("edad", $persona); unset($persona["edad"]);
[$a, $b] = [1, 2];                               // destructuring
['nombre' => $n] = $persona;
foreach ($persona as $clave => $valor) { ... }
```

## 5. Control de flujo y funciones

```php
if ($x > 0) { } elseif ($x < 0) { } else { }
$estado = $nota >= 7 ? "Aprobado" : "Reprobado";
$texto = match ($dia) { 1, 7 => "Fin de semana", default => "Laborable" };   // PHP 8, comparación estricta
switch ($op) { case 1: ...; break; default: ...; }
for ($i = 0; $i < 10; $i++) { }
while ($cond) { }  do { } while ($cond);
foreach ($lista as $i => $item) { if (...) continue; if (...) break; }

function sumar(int $a, int $b = 0): int { return $a + $b; }
function total(float ...$precios): float { return array_sum($precios); }
function buscar(?int $id): ?array { ... }            // ? = puede ser null
function nada(): void { }
$doble = fn($x) => $x * 2;                           // arrow function (captura variables automáticamente)
$sumarN = function ($x) use ($n) { return $x + $n; };   // closure clásica: use para capturar
sumar(b: 5, a: 1);                                   // argumentos con nombre (PHP 8)
```

## 6. Formularios y superglobales

```php
$_GET["q"]           // parámetros de la URL
$_POST["nombre"]     // formulario method="post"
$_REQUEST            // ambos (evítalo)
$_FILES["foto"]      // archivos subidos (form enctype="multipart/form-data")
$_SESSION            // sesión (requiere session_start())
$_COOKIE
$_SERVER["REQUEST_METHOD"], $_SERVER["REQUEST_URI"], $_SERVER["HTTP_HOST"]

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $nombre = trim($_POST["nombre"] ?? "");
    $edad = filter_input(INPUT_POST, "edad", FILTER_VALIDATE_INT);         // false si inválido
    $email = filter_var($_POST["email"] ?? "", FILTER_VALIDATE_EMAIL);
    $errores = [];
    if ($nombre === "") $errores[] = "Nombre obligatorio";
    if ($edad === false || $edad < 0) $errores[] = "Edad inválida";
    if (!$errores) {
        // guardar...
        header("Location: index.php?ok=1");   // redirigir tras POST
        exit;
    }
}
```
```html
<input name="nombre" value="<?= htmlspecialchars($nombre ?? '') ?>">
<?php foreach ($errores as $e): ?><p class="error"><?= htmlspecialchars($e) ?></p><?php endforeach; ?>
```
`<?= $x ?>` es un atajo de `<?php echo $x; ?>`. La sintaxis alternativa `if: ... endif;` y `foreach: ... endforeach;` resulta más legible dentro del HTML.

### Subir archivos
```php
if (($_FILES["foto"]["error"] ?? 1) === UPLOAD_ERR_OK) {
    $ext = strtolower(pathinfo($_FILES["foto"]["name"], PATHINFO_EXTENSION));
    if (in_array($ext, ["jpg", "png"]) && $_FILES["foto"]["size"] < 2_000_000) {
        $destino = __DIR__ . "/uploads/" . uniqid() . ".$ext";
        move_uploaded_file($_FILES["foto"]["tmp_name"], $destino);
    }
}
```

## 7. PDO: base de datos (MySQL / SQLite / SQL Server)

```php
$pdo = new PDO("mysql:host=localhost;dbname=tienda;charset=utf8mb4", "root", "", [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
// SQLite:      new PDO("sqlite:" . __DIR__ . "/datos.db")
// SQL Server:  new PDO("sqlsrv:Server=localhost;Database=tienda", "sa", "clave")

// SELECT varios
$st = $pdo->prepare("SELECT * FROM productos WHERE precio > ? ORDER BY nombre");
$st->execute([10]);
$filas = $st->fetchAll();

// Parámetros con nombre
$st = $pdo->prepare("SELECT * FROM productos WHERE id = :id");
$st->execute([":id" => $id]);
$producto = $st->fetch();                 // false si no existe

// Un solo valor
$total = $pdo->query("SELECT COUNT(*) FROM productos")->fetchColumn();

// INSERT / UPDATE / DELETE
$st = $pdo->prepare("INSERT INTO productos (nombre, precio) VALUES (?, ?)");
$st->execute([$nombre, $precio]);
$nuevoId = $pdo->lastInsertId();
$st = $pdo->prepare("UPDATE productos SET precio = ? WHERE id = ?");
$st->execute([$precio, $id]);
$filasAfectadas = $st->rowCount();

// Transacción
try {
    $pdo->beginTransaction();
    $pdo->prepare("UPDATE cuentas SET saldo = saldo - ? WHERE id = ?")->execute([100, 1]);
    $pdo->prepare("UPDATE cuentas SET saldo = saldo + ? WHERE id = ?")->execute([100, 2]);
    $pdo->commit();
} catch (Throwable $e) {
    $pdo->rollBack();
    throw $e;
}
```
**Nunca:** `"SELECT * FROM usuarios WHERE email = '$email'"` (eso es SQL Injection). La extensión `mysqli` también existe, pero PDO es más portable.

## 8. Sesiones y login seguro

```php
session_start();                                        // al inicio de CADA página que use sesión

// Registro
$hash = password_hash($_POST["clave"], PASSWORD_DEFAULT);          // bcrypt
$pdo->prepare("INSERT INTO usuarios (email, clave_hash) VALUES (?, ?)")->execute([$email, $hash]);

// Login
$st = $pdo->prepare("SELECT * FROM usuarios WHERE email = ?");
$st->execute([$_POST["email"]]);
$u = $st->fetch();
if ($u && password_verify($_POST["clave"], $u["clave_hash"])) {
    session_regenerate_id(true);                         // evita fijación de sesión
    $_SESSION["usuario_id"] = $u["id"];
    $_SESSION["rol"] = $u["rol"];
    header("Location: panel.php"); exit;
}
$error = "Credenciales incorrectas";

// Proteger una página (poner arriba de todo)
if (empty($_SESSION["usuario_id"])) { header("Location: login.php"); exit; }
if ($_SESSION["rol"] !== "admin") { http_response_code(403); exit("Acceso denegado"); }

// Logout
session_start(); session_destroy(); header("Location: login.php"); exit;
```

### Token CSRF (protección de formularios)
```php
$_SESSION["csrf"] ??= bin2hex(random_bytes(32));
// en el form:  <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
if (!hash_equals($_SESSION["csrf"], $_POST["csrf"] ?? "")) { http_response_code(403); exit("CSRF"); }
```

## 9. POO en PHP

```php
interface Pagable { public function calcularPago(): float; }

abstract class Empleado implements Pagable {
    protected static int $contador = 0;
    public function __construct(
        protected string $nombre,                  // promoción de propiedades (PHP 8)
        private readonly string $cedula,           // readonly (PHP 8.1)
    ) { static::$contador++; }
    abstract public function calcularPago(): float;
    public function getNombre(): string { return $this->nombre; }
    public static function total(): int { return static::$contador; }
    public function __toString(): string { return "{$this->nombre}: {$this->calcularPago()}"; }
}

class Docente extends Empleado {
    public function __construct(string $n, string $c, private float $sueldo) { parent::__construct($n, $c); }
    public function calcularPago(): float { return $this->sueldo; }
}

trait Timestamps {                                 // reutilizar código entre clases
    public function ahora(): string { return date("Y-m-d H:i:s"); }
}
class Producto { use Timestamps; }

enum Estado: string { case Activo = "activo"; case Inactivo = "inactivo"; }   // PHP 8.1
$e = Estado::from("activo");  $e->value;

$d = new Docente("Ana", "1710034065", 1100);
echo $d, " ", Empleado::total();
$d instanceof Pagable;                            // true
```
Visibilidad: `public` (todos), `protected` (clase e hijas), `private` (solo la clase). `self::` apunta a la clase donde está escrito el código; `static::` a la clase real (late static binding). `$this->` es la instancia.

### Autoload y namespaces (proyectos más grandes)
```php
namespace App\Modelos;          // en src/Modelos/Producto.php
use App\Modelos\Producto;       // en otro archivo

// composer.json:  "autoload": { "psr-4": { "App\\": "src/" } }   →  composer dump-autoload
require __DIR__ . "/vendor/autoload.php";
```

## 10. Estructura MVC simple en PHP puro

```
proyecto/
├── public/index.php          ← único punto de entrada (front controller)
├── app/
│   ├── Controladores/ProductoControlador.php
│   ├── Modelos/Producto.php  ← consultas PDO
│   └── Vistas/productos/lista.php
├── config/database.php
└── composer.json
```
Mini enrutador:
```php
// public/index.php
$ruta = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
$metodo = $_SERVER["REQUEST_METHOD"];
match (true) {
    $ruta === "/" && $metodo === "GET"             => (new ProductoControlador)->index(),
    $ruta === "/productos" && $metodo === "POST"   => (new ProductoControlador)->guardar(),
    preg_match('#^/productos/(\d+)$#', $ruta, $m) === 1 => (new ProductoControlador)->ver((int)$m[1]),
    default => http_response_code(404),
};
```

## 11. API JSON en PHP

```php
header("Content-Type: application/json; charset=utf-8");
header("Access-Control-Allow-Origin: *");              // CORS si la consume otro dominio
$body = json_decode(file_get_contents("php://input"), true) ?? [];
http_response_code(201);
echo json_encode($datos, JSON_UNESCAPED_UNICODE);
```

## 12. Laravel en 1 minuto (el framework PHP más usado)

```bash
composer create-project laravel/laravel tienda
cd tienda
php artisan serve                          # http://127.0.0.1:8000
php artisan make:model Producto -mcr       # modelo + migración + controlador resource
php artisan migrate
php artisan route:list
```
```php
// routes/web.php
Route::resource('productos', ProductoController::class);
// app/Http/Controllers/ProductoController.php
public function store(Request $r) {
    $datos = $r->validate(['nombre' => 'required|min:3', 'precio' => 'required|numeric|gt:0']);
    Producto::create($datos);
    return redirect()->route('productos.index')->with('ok', 'Creado');
}
// Eloquent ORM
Producto::all(); Producto::find(1); Producto::where('precio', '>', 10)->orderBy('nombre')->get();
```
Vistas Blade: `{{ $variable }}` (escapado), `@foreach ($productos as $p) ... @endforeach`, `@if`, `@csrf`, `@extends('layout')`, `@section('contenido')`.

## 13. Errores frecuentes

| Error | Causa |
|---|---|
| `Parse error: syntax error, unexpected ...` | Falta `;` o `}` en la línea anterior |
| `Undefined variable $x` / `Undefined array key "x"` | Variable o clave inexistente: usa `?? ""` |
| `Cannot modify header information - headers already sent` | Hubo salida (echo, espacio o HTML) antes de `header()`. Nada antes de `<?php` |
| `could not find driver` | Falta la extensión: activa `extension=pdo_mysql` / `pdo_sqlite` en php.ini |
| `SQLSTATE[HY000] [1045] Access denied` | Usuario/clave de MySQL incorrectos |
| `SQLSTATE[HY000] [2002] No connection` | MySQL no está iniciado en XAMPP |
| `SQLSTATE[23000] Integrity constraint violation` | UNIQUE o FK violada |
| Página en blanco | Error oculto: activa `display_errors` o revisa `C:\xampp\apache\logs\error.log` |
