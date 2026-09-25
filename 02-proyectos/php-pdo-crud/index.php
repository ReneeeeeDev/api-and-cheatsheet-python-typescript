<?php
// Controlador principal: un solo archivo con "acciones" según ?accion=...
//   index.php                      → listado (con búsqueda ?q= y filtro ?cat=)
//   index.php?accion=nuevo         → formulario vacío
//   index.php?accion=editar&id=2   → formulario con datos
//   POST accion=guardar            → crear o actualizar
//   POST accion=eliminar           → eliminar
require __DIR__ . "/config.php";
require __DIR__ . "/validaciones.php";

$pdo = conectar();
$accion = $_POST["accion"] ?? $_GET["accion"] ?? "listar";
$errores = [];
$form = [];

// ------------------------------------------------------------------ ACCIONES POST
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if ($accion === "guardar") {
        $id = (int)($_POST["id"] ?? 0);
        $errores = validar_producto($pdo, $_POST, $id);
        if (!$errores) {
            if ($id > 0) {
                $st = $pdo->prepare("UPDATE productos SET codigo=?, nombre=?, precio=?, stock=?, categoria_id=? WHERE id=?");
                $st->execute([...datos_producto($_POST), $id]);
                flash("ok", "Producto actualizado.");
            } else {
                $st = $pdo->prepare("INSERT INTO productos (codigo, nombre, precio, stock, categoria_id) VALUES (?, ?, ?, ?, ?)");
                $st->execute(datos_producto($_POST));
                flash("ok", "Producto creado con id " . $pdo->lastInsertId() . ".");
            }
            redirigir("index.php");               // POST → Redirect → GET
        }
        $form = $_POST;                            // volver a mostrar con los datos escritos
        $accion = $id > 0 ? "editar" : "nuevo";
    } elseif ($accion === "eliminar") {
        $st = $pdo->prepare("DELETE FROM productos WHERE id = ?");
        $st->execute([(int)$_POST["id"]]);
        flash($st->rowCount() ? "ok" : "error", $st->rowCount() ? "Producto eliminado." : "No existe.");
        redirigir("index.php");
    }
}

// ------------------------------------------------------------------ DATOS PARA LA VISTA
if ($accion === "editar" && !$form) {
    $st = $pdo->prepare("SELECT * FROM productos WHERE id = ?");
    $st->execute([(int)($_GET["id"] ?? 0)]);
    $form = $st->fetch() ?: [];
    if (!$form) { flash("error", "Producto no encontrado."); redirigir("index.php"); }
}

$categorias = $pdo->query("SELECT * FROM categorias ORDER BY nombre")->fetchAll();

$q = trim($_GET["q"] ?? "");
$cat = (int)($_GET["cat"] ?? 0);
$sql = "SELECT p.*, c.nombre AS categoria FROM productos p JOIN categorias c ON c.id = p.categoria_id WHERE (p.nombre LIKE ? OR p.codigo LIKE ?)";
$params = ["%$q%", "%$q%"];
if ($cat) { $sql .= " AND p.categoria_id = ?"; $params[] = $cat; }
$st = $pdo->prepare($sql . " ORDER BY p.nombre");
$st->execute($params);
$productos = $st->fetchAll();

$resumen = $pdo->query("SELECT COUNT(*) AS total, COALESCE(SUM(stock), 0) AS unidades,
    COALESCE(SUM(precio * stock), 0) AS valor, SUM(CASE WHEN stock < 5 THEN 1 ELSE 0 END) AS bajo FROM productos")->fetch();

$flash = tomar_flash();
$mostrar_form = in_array($accion, ["nuevo", "editar"], true);
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inventario PHP</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="barra">
  <a href="index.php" class="logo">Inventario (PHP + PDO)</a>
  <a href="index.php?accion=nuevo" class="btn blanco">+ Nuevo producto</a>
</header>
<main class="contenedor">

  <?php if ($flash): ?>
    <div class="alerta <?= e($flash["tipo"]) ?>"><?= e($flash["mensaje"]) ?></div>
  <?php endif; ?>

  <?php if ($errores): ?>
    <div class="alerta error"><strong>Revise los datos:</strong>
      <ul><?php foreach ($errores as $err): ?><li><?= e($err) ?></li><?php endforeach; ?></ul>
    </div>
  <?php endif; ?>

  <section class="tarjetas">
    <div class="tarjeta"><span>Productos</span><strong><?= e($resumen["total"]) ?></strong></div>
    <div class="tarjeta"><span>Unidades</span><strong><?= e($resumen["unidades"]) ?></strong></div>
    <div class="tarjeta"><span>Valor inventario</span><strong>$<?= number_format((float)$resumen["valor"], 2) ?></strong></div>
    <div class="tarjeta"><span>Stock bajo (&lt;5)</span><strong><?= e((int)$resumen["bajo"]) ?></strong></div>
  </section>

  <?php if ($mostrar_form): ?>
  <section class="panel">
    <h2><?= !empty($form["id"]) ? "Editar " . e($form["codigo"] ?? "") : "Nuevo producto" ?></h2>
    <form method="post" action="index.php">
      <input type="hidden" name="accion" value="guardar">
      <input type="hidden" name="id" value="<?= e($form["id"] ?? 0) ?>">
      <div class="grid">
        <label>Código <input name="codigo" value="<?= e($form["codigo"] ?? "") ?>" required></label>
        <label>Nombre <input name="nombre" value="<?= e($form["nombre"] ?? "") ?>" required></label>
        <label>Precio <input name="precio" type="number" step="0.01" min="0.01" value="<?= e($form["precio"] ?? "") ?>" required></label>
        <label>Stock <input name="stock" type="number" min="0" value="<?= e($form["stock"] ?? 0) ?>" required></label>
        <label>Categoría
          <select name="categoria_id" required>
            <option value="">-- Seleccione --</option>
            <?php foreach ($categorias as $c): ?>
              <option value="<?= $c["id"] ?>" <?= (string)($form["categoria_id"] ?? "") === (string)$c["id"] ? "selected" : "" ?>><?= e($c["nombre"]) ?></option>
            <?php endforeach; ?>
          </select>
        </label>
      </div>
      <div class="acciones">
        <button type="submit">Guardar</button>
        <a class="btn sec" href="index.php">Cancelar</a>
      </div>
    </form>
  </section>
  <?php endif; ?>

  <section class="panel">
    <form method="get" class="filtros">
      <input name="q" value="<?= e($q) ?>" placeholder="Buscar por nombre o código">
      <select name="cat">
        <option value="0">Todas las categorías</option>
        <?php foreach ($categorias as $c): ?>
          <option value="<?= $c["id"] ?>" <?= $cat === (int)$c["id"] ? "selected" : "" ?>><?= e($c["nombre"]) ?></option>
        <?php endforeach; ?>
      </select>
      <button>Filtrar</button>
      <a class="btn sec" href="index.php">Limpiar</a>
    </form>
    <table>
      <thead><tr><th>Código</th><th>Nombre</th><th>Categoría</th><th>Precio</th><th>Stock</th><th></th></tr></thead>
      <tbody>
      <?php if (!$productos): ?>
        <tr><td colspan="6">Sin resultados.</td></tr>
      <?php endif; ?>
      <?php foreach ($productos as $p): ?>
        <tr>
          <td><?= e($p["codigo"]) ?></td>
          <td><?= e($p["nombre"]) ?></td>
          <td><?= e($p["categoria"]) ?></td>
          <td>$<?= number_format((float)$p["precio"], 2) ?></td>
          <td class="<?= $p["stock"] < 5 ? "bajo" : "" ?>"><?= e($p["stock"]) ?></td>
          <td class="acciones">
            <a class="btn sec" href="index.php?accion=editar&id=<?= $p["id"] ?>">Editar</a>
            <form method="post" action="index.php" onsubmit="return confirm('¿Eliminar <?= e($p["codigo"]) ?>?')">
              <input type="hidden" name="accion" value="eliminar">
              <input type="hidden" name="id" value="<?= $p["id"] ?>">
              <button class="peligro">Eliminar</button>
            </form>
          </td>
        </tr>
      <?php endforeach; ?>
      </tbody>
    </table>
  </section>

  <p><a href="api.php">Ver API JSON</a></p>
</main>
</body>
</html>
