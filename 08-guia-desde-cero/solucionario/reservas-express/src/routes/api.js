// API REST en JSON. Montada en /api (ver app.js).
import { Router } from "express";
import { validarLaboratorio } from "../validaciones.js";
import { datosLaboratorio } from "./laboratorios.js";

export default function apiRouter(db) {
  const router = Router();

  // GET /api/laboratorios
  router.get("/laboratorios", (req, res) => {
    res.json(db.prepare("SELECT * FROM laboratorios ORDER BY codigo").all());
  });

  // POST /api/laboratorios   body: {"codigo":"LAB-010","nombre":"...","piso":1,"capacidad":20}
  router.post("/laboratorios", (req, res) => {
    const datos = { estado: "disponible", ...(req.body || {}) };
    const errores = validarLaboratorio(db, datos);
    if (errores.length) return res.status(400).json({ errores });
    const r = db.prepare("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)")
      .run(...datosLaboratorio(datos));
    res.status(201).json(db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(r.lastInsertRowid));
  });

  // GET /api/reservas?fecha=2026-09-25
  router.get("/reservas", (req, res) => {
    let sql = "SELECT r.*, l.codigo FROM reservas r JOIN laboratorios l ON l.id = r.laboratorio_id";
    const params = [];
    if (req.query.fecha) { sql += " WHERE r.fecha = ?"; params.push(req.query.fecha); }
    res.json(db.prepare(sql + " ORDER BY r.fecha, r.hora_inicio").all(...params));
  });

  return router;
}
