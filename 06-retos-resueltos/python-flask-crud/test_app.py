"""
Pruebas del CRUD. Ejecutar:  python -m unittest -v
Usa una BD temporal para no tocar instituto.db.
"""
import os
import tempfile
import unittest

import app as modulo


class TestEstudiantes(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".db")
        modulo.app.config.update(TESTING=True, DATABASE=self.path)
        with modulo.app.app_context():
            modulo.init_db()
        self.client = modulo.app.test_client()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    # --- validador de cédula (prueba unitaria pura)
    def test_cedula_valida(self):
        self.assertTrue(modulo.cedula_valida("1710034065"))

    def test_cedula_invalida(self):
        self.assertFalse(modulo.cedula_valida("1710034066"))   # dígito verificador mal
        self.assertFalse(modulo.cedula_valida("123"))
        self.assertFalse(modulo.cedula_valida("9910034065"))   # provincia inexistente

    # --- API (pruebas de integración)
    def test_listar(self):
        r = self.client.get("/api/estudiantes")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 2)

    def test_crear_valido(self):
        r = self.client.post("/api/estudiantes", json={
            "cedula": "1804432126", "nombre": "María Díaz", "email": "maria@mail.com",
            "carrera_id": 1, "promedio": 8.4})
        self.assertEqual(r.status_code, 201, r.get_json())
        self.assertEqual(r.get_json()["nombre"], "María Díaz")

    def test_crear_invalido(self):
        r = self.client.post("/api/estudiantes", json={"cedula": "1", "nombre": "A", "email": "x"})
        self.assertEqual(r.status_code, 400)
        self.assertGreaterEqual(len(r.get_json()["errores"]), 3)

    def test_cedula_duplicada(self):
        r = self.client.post("/api/estudiantes", json={
            "cedula": "1710034065", "nombre": "Otra Ana", "email": "o@mail.com", "carrera_id": 1})
        self.assertEqual(r.status_code, 400)

    def test_actualizar_y_eliminar(self):
        r = self.client.put("/api/estudiantes/1", json={
            "cedula": "1710034065", "nombre": "Ana Actualizada", "email": "ana@mail.com",
            "carrera_id": 1, "promedio": 10})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["nombre"], "Ana Actualizada")
        self.assertEqual(self.client.delete("/api/estudiantes/1").status_code, 204)
        self.assertEqual(self.client.get("/api/estudiantes/1").status_code, 404)

    def test_buscar(self):
        r = self.client.get("/api/estudiantes?q=luis")
        self.assertEqual([e["nombre"] for e in r.get_json()], ["Luis Mora"])

    # --- vistas HTML
    def test_pagina_inicio(self):
        r = self.client.get("/")
        self.assertIn("Ana Pérez", r.get_data(as_text=True))


    # ------------------------------------------------ RETOS
    def test_reto1_notas_y_promedio(self):
        r = self.client.get("/estudiantes/1/notas")
        html = r.get_data(as_text=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Programación I", html)
        self.assertIn("9.1", html)                      # promedio simple (9.5 + 8.7) / 2
        # registrar Inglés = 10 y actualizar Programación I = 7 (UPSERT)
        self.client.post("/estudiantes/1/notas", data={"materia_id": 3, "nota": "10"})
        self.client.post("/estudiantes/1/notas", data={"materia_id": 1, "nota": "7"})
        est = self.client.get("/api/estudiantes/1").get_json()
        self.assertEqual(est["promedio"], 8.57)         # (7 + 8.7 + 10) / 3
        self.assertEqual(self.client.post("/estudiantes/1/notas", data={"materia_id": 1, "nota": "11"}).status_code, 302)
        self.assertEqual(self.client.get("/api/estudiantes/1").get_json()["promedio"], 8.57)   # no cambió

    def test_reto2_paginacion(self):
        from app import cedula_valida
        # crear 6 estudiantes más (8 en total) generando cédulas válidas
        n = 0
        for pre in range(1000000, 1000100):
            c9 = f"17{pre:07d}"
            for d in range(10):
                if cedula_valida(c9 + str(d)):
                    self.client.post("/api/estudiantes", json={"cedula": c9 + str(d), "nombre": f"Est {n:02d}",
                                                             "email": f"e{n}@m.com", "carrera_id": 1, "promedio": 7})
                    n += 1
                    break
            if n == 6:
                break
        html1 = self.client.get("/?pagina=1").get_data(as_text=True)
        html2 = self.client.get("/?pagina=2").get_data(as_text=True)
        self.assertIn("Página 1 de 2", html1)
        self.assertIn("Página 2 de 2", html2)
        self.assertEqual(html1.count('href="/editar/'), 5)
        self.assertEqual(html2.count('href="/editar/'), 3)
        self.assertIn("Página 2 de 2", self.client.get("/?pagina=99").get_data(as_text=True))   # se ajusta al máximo

    def test_reto3_exportar_csv(self):
        r = self.client.get("/exportar")
        texto = r.get_data(as_text=True)
        self.assertEqual(r.mimetype, "text/csv")
        self.assertIn("attachment", r.headers["Content-Disposition"])
        self.assertIn("cedula,nombre,email,carrera,promedio", texto)
        self.assertEqual(len(texto.strip().splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
