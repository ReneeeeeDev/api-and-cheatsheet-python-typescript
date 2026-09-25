<?php
/**
 * Repaso de PHP en consola: tipos, strings, arrays, funciones, POO, excepciones, JSON, fechas y PDO con SQLite.
 * Ejecutar:  php basicos.php
 * Con XAMPP en Windows:  C:\xampp\php\php.exe basicos.php
 */
declare(strict_types=1);

echo "===== VARIABLES Y TIPOS\n";
$nombre = "Ana";
$edad = 25;
$precio = 12.5;
$activo = true;
$nada = null;
var_dump($edad, $activo);                         // muestra tipo y valor
echo gettype($precio), " ", intdiv(7, 2), " ", 7 % 2, " ", 2 ** 10, " ", round(3.14159, 2), "\n";
echo "Interpolación: $nombre tiene {$edad} años\n";
echo 'Comillas simples NO interpolan: $nombre', "\n";
echo "Concatenación: " . $nombre . " - " . number_format(1234.5, 2, ',', '.') . "\n";   // 1.234,50
echo ("5" == 5 ? "==: true" : "false"), " | ", ("5" === 5 ? "true" : "===: false"), "\n";
echo $nada ?? "valor por defecto", "\n";          // null coalescing

echo "\n===== STRINGS\n";
$s = "  Hola Mundo PHP  ";
echo trim($s), "|", strtoupper($s), "|", strtolower($s), "|", strlen(trim($s)), "\n";
echo str_contains($s, "Mundo") ? "contiene" : "no", " ", strpos($s, "o"), " ", substr(trim($s), 0, 4), " ", strrev("hola"), "\n";
echo str_replace("o", "0", $s), "|", ucfirst("hola"), "|", ucwords("hola mundo"), "|", str_pad("7", 3, "0", STR_PAD_LEFT), "\n";
print_r(explode(",", "a,b,c")); echo implode("-", ["2026", "09", "25"]), "\n";
echo htmlspecialchars("<script>alert(1)</script>"), "\n";   // SIEMPRE al imprimir datos del usuario en HTML (evita XSS)
printf("%-10s|%8.2f|%05d\n", "Ana", 9.456, 42);

echo "\n===== ARRAYS\n";
$nums = [5, 3, 8, 1];
$nums[] = 10;                                     // agregar al final
array_unshift($nums, 0);
array_pop($nums);
sort($nums);
echo implode(",", $nums), " | count=", count($nums), " sum=", array_sum($nums), " max=", max($nums), " in=", in_array(8, $nums) ? "sí" : "no", "\n";
$pares = array_filter($nums, fn($n) => $n % 2 === 0);
$dobles = array_map(fn($n) => $n * 2, $nums);
$total = array_reduce($nums, fn($acc, $n) => $acc + $n, 0);
echo implode(",", $pares), " | ", implode(",", $dobles), " | ", $total, "\n";
echo implode(",", array_slice($nums, 1, 2)), " | unique: ", implode(",", array_unique([1, 1, 2])), " | ", implode(",", array_reverse($nums)), "\n";

// Arrays asociativos (como diccionarios)
$persona = ["nombre" => "Ana", "edad" => 25];
$persona["email"] = "ana@mail.com";
unset($persona["edad"]);
foreach ($persona as $clave => $valor) echo "  $clave: $valor\n";
echo array_key_exists("email", $persona) ? "tiene email" : "", " | keys: ", implode(",", array_keys($persona)), "\n";

$estudiantes = [
    ["nombre" => "Ana", "nota" => 9.0],
    ["nombre" => "Luis", "nota" => 6.5],
    ["nombre" => "María", "nota" => 8.0],
];
usort($estudiantes, fn($a, $b) => $b["nota"] <=> $a["nota"]);    // <=> operador nave espacial
$aprobados = array_column(array_filter($estudiantes, fn($e) => $e["nota"] >= 7), "nombre");
$promedio = array_sum(array_column($estudiantes, "nota")) / count($estudiantes);
echo "Orden: ", implode(", ", array_column($estudiantes, "nombre")), " | aprobados: ", implode(", ", $aprobados), " | promedio: ", round($promedio, 2), "\n";

echo "\n===== CONTROL DE FLUJO\n";
$nota = 8.4;
if ($nota >= 9) echo "Excelente\n"; elseif ($nota >= 7) echo "Aprobado\n"; else echo "Reprobado\n";
echo match (true) { $edad < 12 => "Niño", $edad < 18 => "Adolescente", default => "Adulto" }, "\n";   // PHP 8
for ($i = 0; $i < 3; $i++) echo $i, " ";
$n = 3; while ($n-- > 0) echo "w", $n, " ";
echo "\n";

echo "\n===== FUNCIONES\n";
function saludar(string $nombre, string $saludo = "Hola"): string { return "$saludo, $nombre"; }
function sumarTodo(int ...$numeros): int { return array_sum($numeros); }
$multiplicar = fn(int $a, int $b): int => $a * $b;          // arrow function
echo saludar("Ana"), " | ", saludar(saludo: "Buenas", nombre: "Luis"), " | ", sumarTodo(1, 2, 3), " | ", $multiplicar(3, 4), "\n";

echo "\n===== POO\n";
interface Pagable { public function calcularPago(): float; }

abstract class Empleado implements Pagable {
    private static int $contador = 0;
    public readonly int $id;
    public function __construct(protected string $nombre) {       // promoción de propiedades (PHP 8)
        if (trim($nombre) === "") throw new InvalidArgumentException("Nombre obligatorio");
        $this->id = ++self::$contador;
    }
    public function getNombre(): string { return $this->nombre; }
    public function aporteIess(): float { return round($this->calcularPago() * 0.0945, 2); }
    public function __toString(): string { return sprintf("#%d %-15s %-6s $%8.2f", $this->id, static::class, $this->nombre, $this->calcularPago()); }
}
class TiempoCompleto extends Empleado {
    public function __construct(string $nombre, private float $sueldo) { parent::__construct($nombre); }
    public function calcularPago(): float { return $this->sueldo; }
}
class PorHoras extends Empleado {
    public function __construct(string $nombre, private int $horas, private float $tarifa) { parent::__construct($nombre); }
    public function calcularPago(): float { return $this->horas * $this->tarifa; }
}
$nomina = [new TiempoCompleto("Ana", 900), new PorHoras("Luis", 160, 5)];
foreach ($nomina as $e) echo $e, " IESS: ", $e->aporteIess(), "\n";
echo "Total: ", array_sum(array_map(fn(Pagable $e) => $e->calcularPago(), $nomina)), "\n";

echo "\n===== EXCEPCIONES\n";
class StockException extends Exception {}
function vender(int $stock, int $cantidad): int {
    if ($cantidad <= 0) throw new InvalidArgumentException("Cantidad inválida");
    if ($cantidad > $stock) throw new StockException("Stock insuficiente ($stock)");
    return $stock - $cantidad;
}
foreach ([2, 50, -1] as $c) {
    try { echo "Quedan: ", vender(10, $c), "\n"; }
    catch (StockException | InvalidArgumentException $ex) { echo get_class($ex), ": ", $ex->getMessage(), "\n"; }
    finally { /* siempre */ }
}

echo "\n===== JSON Y FECHAS\n";
$json = json_encode(["nombre" => "Ana", "notas" => [9, 10]], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
echo $json, "\n";
$datos = json_decode('{"a":1,"b":[1,2]}', true);        // true → array asociativo
echo $datos["b"][1], "\n";
$fecha = new DateTime("2026-09-25 16:00");
echo $fecha->format("d/m/Y H:i"), " | +30 días: ", (clone $fecha)->modify("+30 days")->format("Y-m-d"), "\n";
echo "Edad: ", (new DateTime("2001-03-15"))->diff(new DateTime("2026-09-25"))->y, "\n";

echo "\n===== PDO (SQLite en memoria; con MySQL solo cambia el DSN)\n";
// MySQL:  new PDO("mysql:host=localhost;dbname=tienda;charset=utf8mb4", "root", "")
if (!in_array("sqlite", PDO::getAvailableDrivers())) { echo "Driver SQLite no disponible en este PHP\n"; exit; }
$pdo = new PDO("sqlite::memory:", null, null, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
$pdo->exec("CREATE TABLE productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, precio REAL NOT NULL, stock INTEGER DEFAULT 0)");
$ins = $pdo->prepare("INSERT INTO productos (nombre, precio, stock) VALUES (:nombre, :precio, :stock)");
foreach ([["Mouse", 15.5, 20], ["Teclado", 45, 8], ["Monitor", 139.99, 3]] as [$n, $p, $s]) {
    $ins->execute([":nombre" => $n, ":precio" => $p, ":stock" => $s]);
}
echo "Último id: ", $pdo->lastInsertId(), "\n";
$st = $pdo->prepare("SELECT * FROM productos WHERE precio > ? ORDER BY precio");
$st->execute([20]);
foreach ($st->fetchAll() as $fila) echo "  {$fila['id']} {$fila['nombre']} {$fila['precio']}\n";
$st = $pdo->prepare("UPDATE productos SET stock = ? WHERE id = ?");
$st->execute([50, 1]);
echo "Filas actualizadas: ", $st->rowCount(), "\n";
$uno = $pdo->prepare("SELECT * FROM productos WHERE id = ?");
$uno->execute([1]);
print_r($uno->fetch());
$pdo->prepare("DELETE FROM productos WHERE id = ?")->execute([2]);
echo "Quedan: ", $pdo->query("SELECT COUNT(*) FROM productos")->fetchColumn(), "\n";
