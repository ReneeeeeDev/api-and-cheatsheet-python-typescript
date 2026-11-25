import { crearApp } from "./src/app.js";
import { crearRepositorio } from "./src/repositorio.js";

const PORT = process.env.PORT || 3000;
const app = crearApp(crearRepositorio("db.json"));

app.listen(PORT, () => {
  console.log(`Servidor en http://localhost:${PORT}`);
  console.log(`API en      http://localhost:${PORT}/api/productos`);
});
