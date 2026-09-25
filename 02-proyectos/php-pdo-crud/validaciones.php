<?php
// Reglas de negocio: devuelven un array de errores (vacío = válido).

function validar_producto(PDO $pdo, array $d, int $id_actual = 0): array
{
    $errores = [];
    $codigo = strtoupper(trim($d["codigo"] ?? ""));
    if ($codigo === "" || !preg_match('/^[A-Z0-9-]{3,10}$/', $codigo)) {
        $errores[] = "El código debe tener entre 3 y 10 letras, números o guiones.";
    } else {
        $st = $pdo->prepare("SELECT 1 FROM productos WHERE codigo = ? AND id <> ?");
        $st->execute([$codigo, $id_actual]);
        if ($st->fetch()) $errores[] = "Ya existe un producto con el código $codigo.";
    }
    if (mb_strlen(trim($d["nombre"] ?? "")) < 3) $errores[] = "El nombre debe tener al menos 3 caracteres.";
    if (!is_numeric($d["precio"] ?? "") || (float)$d["precio"] <= 0) $errores[] = "El precio debe ser un número mayor a 0.";
    if (!ctype_digit((string)($d["stock"] ?? ""))) $errores[] = "El stock debe ser un entero mayor o igual a 0.";
    $st = $pdo->prepare("SELECT 1 FROM categorias WHERE id = ?");
    $st->execute([(int)($d["categoria_id"] ?? 0)]);
    if (!$st->fetch()) $errores[] = "Seleccione una categoría válida.";
    return $errores;
}

function datos_producto(array $d): array
{
    return [
        strtoupper(trim($d["codigo"])),
        trim($d["nombre"]),
        round((float)$d["precio"], 2),
        (int)$d["stock"],
        (int)$d["categoria_id"],
    ];
}
