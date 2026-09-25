import express from "express";
import { fileURLToPath } from "url";
import laboratoriosRouter from "./routes/laboratorios.js";
import reservasRouter from "./routes/reservas.js";
import reporteRouter from "./routes/reporte.js";
import apiRouter from "./routes/api.js";

// Recibe la BD por parámetro: así las pruebas pueden usar una BD en memoria.
export function crearApp(db) {
  const app = express();

  // Configuración de vistas EJS (carpeta /views en la raíz del proyecto)
  app.set("view engine", "ejs");
  app.set("views", fileURLToPath(new URL("../views", import.meta.url)));

  // Middlewares
  app.use(express.urlencoded({ extended: false }));   // lee formularios HTML (req.body)
  app.use(express.json());                            // lee JSON (para la API)
  app.use(express.static(fileURLToPath(new URL("../public", import.meta.url))));

  // Mensajes después de redirigir: /laboratorios?ok=Guardado  o  ?error=...
  app.use((req, res, next) => {
    res.locals.ok = req.query.ok || "";
    res.locals.error = req.query.error || "";
    res.locals.errores = [];
    next();
  });

  app.get("/", (req, res) => {
    const contar = (sql) => db.prepare(sql).get().total;
    res.render("inicio", {
      totales: {
        laboratorios: contar("SELECT COUNT(*) AS total FROM laboratorios"),
        disponibles: contar("SELECT COUNT(*) AS total FROM laboratorios WHERE estado = 'disponible'"),
        reservas: contar("SELECT COUNT(*) AS total FROM reservas"),
      },
    });
  });

  app.use("/laboratorios", laboratoriosRouter(db));
  app.use("/reservas", reservasRouter(db));
  app.use("/reporte", reporteRouter(db));
  app.use("/api", apiRouter(db));

  // 404 y errores (siempre al final)
  app.use((req, res) => res.status(404).send("Página no encontrada"));
  app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send("Error interno del servidor");
  });

  return app;
}
