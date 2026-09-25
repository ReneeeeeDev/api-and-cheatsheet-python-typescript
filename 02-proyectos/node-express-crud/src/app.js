import express from "express";
import cors from "cors";
import { validarProducto } from "./validacion.js";

// Recibe el repositorio por parámetro (inyección de dependencias): así las pruebas usan otro archivo.
export function crearApp(repo) {
  const app = express();
  app.use(cors());                       // permite que React (otro puerto) consuma la API
  app.use(express.json());
  app.use(express.static("public"));     // frontend HTML/JS

  const router = express.Router();

  // Middleware para validar el :id una sola vez
  router.param("id", (req, res, next, valor) => {
    const id = Number(valor);
    if (!Number.isInteger(id) || id <= 0) return res.status(400).json({ error: "ID inválido" });
    req.idNum = id;
    next();
  });

  router.get("/resumen", (req, res) => res.json(repo.resumen()));

  router.get("/", (req, res) => res.json(repo.listar(req.query)));

  router.get("/:id", (req, res) => {
    const p = repo.obtener(req.idNum);
    if (!p) return res.status(404).json({ error: "Producto no encontrado" });
    res.json(p);
  });

  router.post("/", (req, res) => {
    const { errores, datos } = validarProducto(req.body);
    if (errores.length) return res.status(400).json({ errores });
    res.status(201).json(repo.crear(datos));
  });

  router.put("/:id", (req, res) => {
    const { errores, datos } = validarProducto(req.body, { parcial: true });
    if (errores.length) return res.status(400).json({ errores });
    const p = repo.actualizar(req.idNum, datos);
    if (!p) return res.status(404).json({ error: "Producto no encontrado" });
    res.json(p);
  });

  router.delete("/:id", (req, res) => {
    if (!repo.eliminar(req.idNum)) return res.status(404).json({ error: "Producto no encontrado" });
    res.status(204).end();
  });

  app.use("/api/productos", router);

  app.use((req, res) => res.status(404).json({ error: "Ruta no encontrada" }));
  app.use((err, req, res, _next) => {
    console.error(err);
    res.status(500).json({ error: "Error interno del servidor" });
  });

  return app;
}
