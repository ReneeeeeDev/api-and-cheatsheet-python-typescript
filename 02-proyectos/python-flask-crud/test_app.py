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


if __name__ == "__main__":
    unittest.main()
