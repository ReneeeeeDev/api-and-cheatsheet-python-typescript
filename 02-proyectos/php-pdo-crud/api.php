<?php
// API REST en JSON para productos.
//   GET    api.php            → lista
//   GET    api.php?id=1       → uno
//   POST   api.php            → crear   (body JSON)
//   PUT    api.php?id=1       → actualizar
//   DELETE api.php?id=1       → eliminar
require __DIR__ . "/config.php";
require __DIR__ . "/validaciones.php";

header("Content-Type: application/json; charset=utf-8");
$pdo = conectar();
$metodo = $_SERVER["REQUEST_METHOD"];
$id = isset($_GET["id"]) ? (int)$_GET["id"] : null;

function responder(int $codigo, $datos = null): never
{
    http_response_code($codigo);
    if ($datos !== null) echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION);
    exit;
}

function buscar(PDO $pdo, int $id): ?array
{
    $st = $pdo->prepare("SELECT * FROM productos WHERE id = ?");
    $st->execute([$id]);
    return $st->fetch() ?: null;
}

$body = json_decode(file_get_contents("php://input") ?: "{}", true) ?? [];

switch ($metodo) {
    case "GET":
        if ($id) {
            $p = buscar($pdo, $id);
            $p ? responder(200, $p) : responder(404, ["error" => "No encontrado"]);
        }
        responder(200, $pdo->query("SELECT * FROM productos ORDER BY id")->fetchAll());
    case "POST":
        $errores = validar_producto($pdo, $body);
        if ($errores) responder(400, ["errores" => $errores]);
        $pdo->prepare("INSERT INTO productos (codigo, nombre, precio, stock, categoria_id) VALUES (?, ?, ?, ?, ?)")
            ->execute(datos_producto($body));
        responder(201, buscar($pdo, (int)$pdo->lastInsertId()));
    case "PUT":
        if (!$id || !($actual = buscar($pdo, $id))) responder(404, ["error" => "No encontrado"]);
        $datos = array_merge($actual, $body);       // actualización parcial
        $errores = validar_producto($pdo, $datos, $id);
        if ($errores) responder(400, ["errores" => $errores]);
        $pdo->prepare("UPDATE productos SET codigo=?, nombre=?, precio=?, stock=?, categoria_id=? WHERE id=?")
            ->execute([...datos_producto($datos), $id]);
        responder(200, buscar($pdo, $id));
    case "DELETE":
        $st = $pdo->prepare("DELETE FROM productos WHERE id = ?");
        $st->execute([$id ?? 0]);
        $st->rowCount() ? responder(204) : responder(404, ["error" => "No encontrado"]);
    default:
        responder(405, ["error" => "Método no permitido"]);
}
