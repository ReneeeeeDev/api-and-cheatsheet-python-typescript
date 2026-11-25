import express from "express";
import cors from "cors";
import { randomUUID } from "crypto";
import { validarProducto } from "./validacion.js";

// RETO 3: credenciales fijas (en un sistema real vendrían de la BD con contraseña hasheada)
const USUARIO = process.env.APP_USER || "admin";
const CLAVE = process.env.APP_PASS || "admin123";

export function crearApp(repo) {
  const app = express();
  app.use(cors());
  app.use(express.json());
  app.use(express.static("public"));

  // ------------------------------------------------------------ RETO 3: LOGIN + MIDDLEWARE
  const tokens = new Set();                       // tokens válidos en memoria

  app.post("/api/login", (req, res) => {
    const { usuario, clave } = req.body ?? {};
    if (usuario !== USUARIO || clave !== CLAVE) return res.status(401).json({ error: "Credenciales incorrectas" });
    const token = randomUUID();
    tokens.add(token);
    res.json({ token, usuario });
  });

  app.post("/api/logout", (req, res) => {
    tokens.delete(extraerToken(req));
    res.status(204).end();
  });

  function extraerToken(req) {
    const [tipo, token] = (req.headers.authorization || "").split(" ");
    return tipo === "Bearer" ? token : null;
  }

  // Middleware: exige "Authorization: Bearer <token>" válido
  function requiereAuth(req, res, next) {
    if (!tokens.has(extraerToken(req))) return res.status(401).json({ error: "No autorizado: inicie sesión" });
    next();
  }

  // ------------------------------------------------------------ PRODUCTOS
  const router = express.Router();

  router.param("id", (req, res, next, valor) => {
    const id = Number(valor);
    if (!Number.isInteger(id) || id <= 0) return res.status(400).json({ error: "ID inválido" });
    req.idNum = id;
    next();
  });

  router.get("/resumen", (req, res) => res.json(repo.resumen()));

  // GET /api/productos?q=&orden=&categoria=&activo=true|false
  // RETO 2: si viene ?pagina=N (y opcional &limite=M) responde { datos, pagina, limite, total, paginas }
  router.get("/", (req, res) => {
    const lista = repo.listar(req.query);
    if (req.query.pagina === undefined) return res.json(lista);           // compatibilidad: arreglo simple

    const limite = Math.min(50, Math.max(1, Number(req.query.limite) || 5));
    const total = lista.length;
    const paginas = Math.max(1, Math.ceil(total / limite));
    const pagina = Math.min(paginas, Math.max(1, Number(req.query.pagina) || 1));
    const inicio = (pagina - 1) * limite;
    res.json({ datos: lista.slice(inicio, inicio + limite), pagina, limite, total, paginas });
  });

  router.get("/:id", (req, res) => {
    const p = repo.obtener(req.idNum);
    if (!p) return res.status(404).json({ error: "Producto no encontrado" });
    res.json(p);
  });

  // Las rutas que MODIFICAN datos requieren sesión (requiereAuth va antes del manejador)
  router.post("/", requiereAuth, (req, res) => {
    const { errores, datos } = validarProducto(req.body ?? {});
    if (errores.length) return res.status(400).json({ errores });
    res.status(201).json(repo.crear({ ...datos, activo: true }));
  });

  router.put("/:id", requiereAuth, (req, res) => {
    const { errores, datos } = validarProducto(req.body ?? {}, { parcial: true });
    if (errores.length) return res.status(400).json({ errores });
    const p = repo.actualizar(req.idNum, datos);
    if (!p) return res.status(404).json({ error: "Producto no encontrado" });
    res.json(p);
  });

  // RETO 1: PATCH /api/productos/:id/estado  body { "activo": true | false }
  router.patch("/:id/estado", requiereAuth, (req, res) => {
    const { activo } = req.body ?? {};
    if (typeof activo !== "boolean") return res.status(400).json({ error: "'activo' debe ser true o false" });
    const p = repo.actualizar(req.idNum, { activo });
    if (!p) return res.status(404).json({ error: "Producto no encontrado" });
    res.json(p);
  });

  router.delete("/:id", requiereAuth, (req, res) => {
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
