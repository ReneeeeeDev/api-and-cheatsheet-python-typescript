import { useState } from "react";

const VACIO = { nombre: "", categoria: "", precio: "", stock: 0 };

export default function ProductoForm({ inicial, onGuardar, onCancelar }) {
  const [form, setForm] = useState(inicial ?? VACIO);   // formulario controlado
  const [errores, setErrores] = useState([]);
  const [enviando, setEnviando] = useState(false);

  const cambiar = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  function validar() {
    const errs = [];
    if (form.nombre.trim().length < 3) errs.push("Nombre mínimo 3 caracteres");
    if (!form.categoria.trim()) errs.push("Categoría obligatoria");
    if (!(Number(form.precio) > 0)) errs.push("Precio debe ser mayor a 0");
    if (!Number.isInteger(Number(form.stock)) || Number(form.stock) < 0) errs.push("Stock entero >= 0");
    return errs;
  }

  async function enviar(e) {
    e.preventDefault();
    const errs = validar();
    setErrores(errs);
    if (errs.length) return;
    try {
      setEnviando(true);
      await onGuardar({ ...form, precio: Number(form.precio), stock: Number(form.stock) });
      setForm(VACIO);
    } catch (err) {
      setErrores([err.message]);          // errores que devuelve el backend
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      <div className="grid">
        <label>Nombre <input name="nombre" value={form.nombre} onChange={cambiar} /></label>
        <label>Categoría <input name="categoria" value={form.categoria} onChange={cambiar} /></label>
        <label>Precio <input name="precio" type="number" step="0.01" value={form.precio} onChange={cambiar} /></label>
        <label>Stock <input name="stock" type="number" value={form.stock} onChange={cambiar} /></label>
      </div>
      {errores.length > 0 && (
        <ul className="errores">{errores.map((e) => <li key={e}>{e}</li>)}</ul>
      )}
      <div className="acciones">
        <button type="submit" disabled={enviando}>{enviando ? "Guardando..." : "Guardar"}</button>
        {inicial && <button type="button" className="sec" onClick={onCancelar}>Cancelar</button>}
      </div>
    </form>
  );
}
