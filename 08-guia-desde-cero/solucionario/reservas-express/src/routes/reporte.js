// Reporte de uso. Montado en /reporte (ver app.js).
import { Router } from "express";

const SQL_REPORTE = `
SELECT l.codigo, l.nombre,
       COUNT(r.id) AS total_reservas,
       ROUND(COALESCE(SUM(
           (strftime('%s', r.hora_fin) - strftime('%s', r.hora_inicio)) / 3600.0
       ), 0), 1) AS horas
FROM laboratorios l
LEFT JOIN reservas r ON r.laboratorio_id = l.id
GROUP BY l.id
ORDER BY horas DESC, l.codigo`;

export default function reporteRouter(db) {
  const router = Router();
  router.get("/", (req, res) => res.render("reporte", { filas: db.prepare(SQL_REPORTE).all() }));
  return router;
}
