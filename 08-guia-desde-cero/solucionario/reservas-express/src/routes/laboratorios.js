// Rutas del CRUD de laboratorios. Montadas en /laboratorios (ver app.js).
import { Router } from "express";
import { validarLaboratorio } from "../validaciones.js";

// Limpia y convierte los datos del formulario al orden de las columnas.
export const datosLaboratorio = (b) => [
  String(b.codigo).trim().toUpperCase(),
  String(b.nombre).trim(),
  Number(b.piso),
  Number(b.capacidad),
  b.estado || "disponible",
];

export default function laboratoriosRouter(db) {
  const router = Router();

  const mostrar = (res, form = {}, errores = [], status = 200) => {
    const labs = db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all();
    res.status(status).render("laboratorios", { labs, form, errores });
  };

  // GET /laboratorios            → listado + formulario vacío
  // GET /laboratorios?editar=2   → listado + formulario con el laboratorio 2
  router.get("/", (req, res) => {
    const editarId = Number(req.query.editar);
    if (editarId) {
      const lab = db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(editarId);
      if (!lab) return res.redirect("/laboratorios?error=" + encodeURIComponent("Laboratorio no encontrado."));
      return mostrar(res, lab);
    }
    mostrar(res);
  });

  // POST /laboratorios → crear
  router.post("/", (req, res) => {
    const errores = validarLaboratorio(db, req.body);
    if (errores.length) return mostrar(res, req.body, errores, 400);
    db.prepare("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)")
      .run(...datosLaboratorio(req.body));
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio creado correctamente."));
  });

  // POST /laboratorios/:id → actualizar
  router.post("/:id", (req, res) => {
    const id = Number(req.params.id);
    const errores = validarLaboratorio(db, req.body, id);
    if (errores.length) return mostrar(res, { ...req.body, id }, errores, 400);
    db.prepare("UPDATE laboratorios SET codigo = ?, nombre = ?, piso = ?, capacidad = ?, estado = ? WHERE id = ?")
      .run(...datosLaboratorio(req.body), id);
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio actualizado."));
  });

  // POST /laboratorios/:id/eliminar → eliminar (si no tiene reservas)
  router.post("/:id/eliminar", (req, res) => {
    const id = Number(req.params.id);
    if (db.prepare("SELECT 1 FROM reservas WHERE laboratorio_id = ?").get(id)) {
      return res.redirect("/laboratorios?error=" +
        encodeURIComponent("No se puede eliminar: el laboratorio tiene reservas registradas."));
    }
    db.prepare("DELETE FROM laboratorios WHERE id = ?").run(id);
    res.redirect("/laboratorios?ok=" + encodeURIComponent("Laboratorio eliminado."));
  });

  return router;
}
