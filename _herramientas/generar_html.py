"""Genera versiones .html de todos los .md del kit y un índice LEEME-PRIMERO.html."""
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

RAIZ = Path(__file__).resolve().parent.parent
CSS = HtmlFormatter(style="github-dark").get_style_defs(".codehilite")

PLANTILLA = """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{titulo}</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui,Segoe UI,sans-serif;line-height:1.6;color:#1f2937;background:#f8fafc}}
.layout{{display:grid;grid-template-columns:270px 1fr;max-width:1400px;margin:auto}}
nav{{position:sticky;top:0;height:100vh;overflow:auto;padding:18px;border-right:1px solid #e5e7eb;background:#fff;font-size:13.5px}}
nav ul{{list-style:none;padding-left:10px;margin:3px 0}} nav>div>ul{{padding-left:0}} nav a{{color:#334155;text-decoration:none}} nav a:hover{{color:#0a5bd6}}
.volver{{display:inline-block;margin-bottom:10px;font-weight:600;color:#0a5bd6!important}}
main{{padding:24px 40px;min-width:0}} h1{{color:#0a5bd6}} h2{{border-top:2px solid #e5e7eb;padding-top:22px;margin-top:36px}}
table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;display:block;overflow-x:auto}}
th,td{{border:1px solid #e5e7eb;padding:6px 10px;text-align:left;vertical-align:top}} th{{background:#f1f5f9}}
code{{background:#eef2f7;padding:1px 5px;border-radius:4px;font-size:.9em}}
.codehilite{{border-radius:8px;margin:12px 0;overflow:auto;position:relative}} .codehilite pre{{padding:14px;margin:0;font-size:13px;line-height:1.5}}
.codehilite code{{background:none;padding:0;color:inherit}}
blockquote{{margin:12px 0;padding:8px 16px;background:#fff7ed;border-left:4px solid #f59e0b;border-radius:4px}}
.copiar{{position:absolute;right:6px;top:6px;padding:3px 10px;font-size:12px;border:0;border-radius:4px;cursor:pointer;background:#334155;color:#fff}}
@media (max-width:900px){{.layout{{grid-template-columns:1fr}} nav{{position:static;height:auto;border-right:0}} main{{padding:16px}}}}
{css}
</style></head><body><div class="layout">
<nav><a class="volver" href="{volver}">← Índice del kit</a><br><strong>En esta página</strong>{toc}</nav>
<main>{cuerpo}</main></div>
<script>
document.querySelectorAll('.codehilite').forEach(b => {{
  const btn = document.createElement('button'); btn.className = 'copiar'; btn.textContent = 'Copiar';
  btn.onclick = () => {{ const t = b.querySelector('pre').innerText;
    navigator.clipboard.writeText(t).then(() => {{ btn.textContent = '¡Copiado!'; setTimeout(() => btn.textContent = 'Copiar', 1500); }}); }};
  b.prepend(btn);
}});
</script></body></html>"""

IGNORAR = ("node_modules", "_herramientas")
generados = []
for md in sorted(RAIZ.rglob("*.md")):
    if any(p in md.parts for p in IGNORAR):
        continue
    conv = markdown.Markdown(extensions=["fenced_code", "tables", "codehilite", "toc", "sane_lists"],
                             extension_configs={"codehilite": {"guess_lang": False}, "toc": {"toc_depth": "2-3"}})
    texto = md.read_text(encoding="utf-8")
    cuerpo = conv.convert(texto)
    # enlaces a otros .md → .html
    cuerpo = cuerpo.replace('.md"', '.html"')
    titulo = next((l.lstrip("# ").strip() for l in texto.splitlines() if l.startswith("#")), md.stem)
    profundidad = len(md.relative_to(RAIZ).parts) - 1
    volver = "../" * profundidad + "LEEME-PRIMERO.html"
    destino = md.with_suffix(".html")
    destino.write_text(PLANTILLA.format(titulo=titulo, toc=conv.toc, cuerpo=cuerpo, css=CSS, volver=volver), encoding="utf-8")
    generados.append((md.relative_to(RAIZ), titulo))

# Índice
grupos = {}
for ruta, titulo in generados:
    carpeta = ruta.parts[0] if len(ruta.parts) > 1 else "Inicio"
    grupos.setdefault(carpeta, []).append((ruta, titulo))
DESCR = {
    "Inicio": "Resumen del kit y plan de estudio",
    "00-entorno": "Instalar, configurar y ejecutar todo",
    "01-cheatsheets": "Cheatsheets por tecnología",
    "02-proyectos": "Proyectos completos (README de cada uno)",
    "03-logica": "Ejercicios de lógica y SQL",
    "04-simulacro": "Simulacro de la prueba",
    "05-ejemplos": "Programas ejecutables por tema",
    "06-retos-resueltos": "Soluciones de los retos",
    "07-entrevista": "Preguntas de entrevista",
    "08-guia-desde-cero": "Construir el simulacro paso a paso",
}
filas = []
for carpeta in sorted(grupos, key=lambda c: (c != "Inicio", c)):
    enlaces = "".join(f'<li><a href="{r.with_suffix(".html").as_posix()}">{t}</a> <small>{r.as_posix()}</small></li>'
                      for r, t in grupos[carpeta])
    filas.append(f"<section><h2>{carpeta}</h2><p>{DESCR.get(carpeta, '')}</p><ul>{enlaces}</ul></section>")
indice = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kit de preparación ISTE</title><style>
body{{margin:0;font-family:system-ui,Segoe UI,sans-serif;background:#f1f5f9;color:#1f2937}}
header{{background:#0a5bd6;color:#fff;padding:24px}} header h1{{margin:0}} header p{{color:#dbeafe;font-size:15px}} main{{align-items:start}} main{{max-width:1100px;margin:20px auto;padding:0 16px;
display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
section{{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.06)}} h2{{margin:0;font-size:18px;color:#0a5bd6}}
p{{margin:4px 0 8px;color:#64748b;font-size:14px}} ul{{padding-left:18px;margin:0}} li{{margin:4px 0}} a{{color:#1f2937}} small{{color:#94a3b8;display:block;font-size:11px}}
</style></head><body><header><h1>Kit de preparación — Técnico en Desarrollo de Software</h1>
<p>Prueba: viernes 25/09/2026 · 16h00 · Laboratorio 002 · llegar 15h45 con cédula</p></header>
<main>{''.join(filas)}</main></body></html>"""
(RAIZ / "LEEME-PRIMERO.html").write_text(indice, encoding="utf-8")
print(len(generados), "documentos HTML generados + índice")
