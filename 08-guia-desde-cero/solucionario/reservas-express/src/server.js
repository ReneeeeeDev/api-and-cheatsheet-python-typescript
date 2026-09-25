// Punto de entrada: crea la BD, crea la app y levanta el servidor.
import { crearDb } from "./db/conexion.js";
import { crearApp } from "./app.js";

const PUERTO = process.env.PORT || 3000;
const db = crearDb("reservas.db");
const app = crearApp(db);

app.listen(PUERTO, () => {
  console.log(`Servidor listo en http://localhost:${PUERTO}`);
});
