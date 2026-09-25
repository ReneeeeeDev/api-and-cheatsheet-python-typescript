// Rutas de reservas. Montadas en /reservas (ver app.js).
import { Router } from "express";
import { validarReserva } from "../validaciones.js";

export default function reservasRouter(db) {
  const router = Router();

  const mostrar = (req, res, form = {}, errores = [], status = 200) => {
    const filtro = { fecha: req.query.fecha || "", lab: req.query.lab || "" };

    let sql = `SELECT r.*, l.codigo, l.nombre AS laboratorio
               FROM reservas r
               JOIN laboratorios l ON l.id = r.laboratorio_id
               WHERE 1 = 1`;
    const params = [];
    if (filtro.fecha) { sql += " AND r.fecha = ?"; params.push(filtro.fecha); }
    if (filtro.lab) { sql += " AND r.laboratorio_id = ?"; params.push(Number(filtro.lab)); }
    sql += " ORDER BY r.fecha, r.hora_inicio";

    res.status(status).render("reservas", {
      reservas: db.prepare(sql).all(...params),
      labs: db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all(),
      form, errores, filtro,
    });
  };

  router.get("/", (req, res) => mostrar(req, res));

  router.post("/", (req, res) => {
    const b = req.body;
    const errores = validarReserva(db, b);
    if (errores.length) return mostrar(req, res, b, errores, 400);
    db.prepare(`INSERT INTO reservas (laboratorio_id, docente, fecha, hora_inicio, hora_fin, motivo)
                VALUES (?, ?, ?, ?, ?, ?)`)
      .run(Number(b.laboratorio_id), b.docente.trim(), b.fecha, b.hora_inicio, b.hora_fin, (b.motivo || "").trim());
    res.redirect("/reservas?ok=" + encodeURIComponent("Reserva registrada."));
  });

  router.post("/:id/eliminar", (req, res) => {
    db.prepare("DELETE FROM reservas WHERE id = ?").run(Number(req.params.id));
    res.redirect("/reservas?ok=" + encodeURIComponent("Reserva cancelada."));
  });

  return router;
}
