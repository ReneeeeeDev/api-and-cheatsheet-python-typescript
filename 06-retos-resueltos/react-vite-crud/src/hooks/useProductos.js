// RETO 2: custom hook. Toda la lógica de datos (cargar, filtrar, guardar, eliminar)
// sale del componente y se puede reutilizar en cualquier página.
import { useCallback, useEffect, useState } from "react";
import { api } from "../api.js";

export function useProductos() {
  const [productos, setProductos] = useState([]);
  const [resumen, setResumen] = useState(null);
  const [categorias, setCategorias] = useState([]);
  const [filtros, setFiltros] = useState({ q: "", orden: "id", categoria: "" });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  const cargar = useCallback(async () => {
    try {
      setError("");
      const [lista, res, todos] = await Promise.all([api.listar(filtros), api.resumen(), api.listar()]);
      setProductos(lista);
      setResumen(res);
      // categorías únicas y ordenadas, calculadas de TODOS los productos (no de los filtrados)
      setCategorias([...new Set(todos.map((p) => p.categoria))].sort((a, b) => a.localeCompare(b, "es")));
    } catch {
      setError("No se pudo conectar con la API. ¿Está corriendo el backend en el puerto 3000?");
    } finally {
      setCargando(false);
    }
  }, [filtros]);

  // Debounce de 300 ms al cambiar filtros
  useEffect(() => {
    const t = setTimeout(cargar, 300);
    return () => clearTimeout(t);
  }, [cargar]);

  const cambiarFiltro = (campo, valor) => setFiltros((f) => ({ ...f, [campo]: valor }));

  const guardar = async (datos, id) => {
    if (id) await api.actualizar(id, datos);
    else await api.crear(datos);
    await cargar();
  };

  const eliminar = async (id) => {
    await api.eliminar(id);
    await cargar();
  };

  return { productos, resumen, categorias, filtros, cambiarFiltro, cargando, error, guardar, eliminar, recargar: cargar };
}
