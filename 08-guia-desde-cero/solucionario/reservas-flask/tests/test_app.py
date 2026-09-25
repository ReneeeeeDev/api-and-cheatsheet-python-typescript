"""Pruebas. Ejecutar desde la carpeta del proyecto:  python -m unittest discover tests -v"""
import os
import tempfile
import unittest

from app import app
from db import init_db
from validaciones import se_cruzan


class TestReglas(unittest.TestCase):
    """Pruebas unitarias: la función pura, sin base de datos."""

    def test_horarios_que_se_cruzan(self):
        self.assertTrue(se_cruzan("08:00", "10:00", "09:00", "11:00"))
        self.assertTrue(se_cruzan("08:00", "12:00", "09:00", "10:00"))   # uno dentro del otro

    def test_horarios_contiguos_no_se_cruzan(self):
        self.assertFalse(se_cruzan("08:00", "10:00", "10:00", "12:00"))


class TestApp(unittest.TestCase):
    """Pruebas de integración: peticiones HTTP reales contra una BD temporal."""

    def setUp(self):
        self.fd, self.ruta = tempfile.mkstemp(suffix=".db")
        app.config.update(TESTING=True, DATABASE=self.ruta)
        with app.app_context():
            init_db()
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.ruta)

    def reservar(self, inicio, fin, lab=2, fecha="2026-09-25"):
        return self.client.post("/reservas", data={
            "docente": "Ing. Ruiz", "laboratorio_id": lab, "fecha": fecha,
            "hora_inicio": inicio, "hora_fin": fin, "motivo": "Clase"})

    def test_paginas_cargan(self):
        for ruta in ["/", "/laboratorios", "/reservas", "/reporte", "/laboratorios?editar=1"]:
            self.assertEqual(self.client.get(ruta).status_code, 200, ruta)

    def test_crear_laboratorio(self):
        r = self.client.post("/laboratorios", data={
            "codigo": "lab-010", "nombre": "Lab IA", "piso": "3", "capacidad": "15", "estado": "disponible"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("LAB-010", self.client.get("/laboratorios").get_data(as_text=True))

    def test_laboratorio_invalido_y_duplicado(self):
        r = self.client.post("/laboratorios", data={"codigo": "LAB-001", "nombre": "X", "piso": "-1",
                                                    "capacidad": "0", "estado": "otro"})
        self.assertEqual(r.status_code, 400)
        html = r.get_data(as_text=True)
        self.assertIn("Ya existe", html)
        self.assertIn("capacidad", html)

    def test_editar_laboratorio(self):
        r = self.client.post("/laboratorios/1", data={
            "codigo": "LAB-001", "nombre": "Redes Renovado", "piso": "1", "capacidad": "40",
            "estado": "disponible"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("Redes Renovado", self.client.get("/laboratorios").get_data(as_text=True))

    def test_reserva_valida(self):
        self.assertEqual(self.reservar("08:00", "10:00").status_code, 302)

    def test_reserva_que_choca(self):
        self.reservar("08:00", "10:00")
        r = self.reservar("09:00", "11:00")
        self.assertEqual(r.status_code, 400)
        self.assertIn("Horario ocupado", r.get_data(as_text=True))

    def test_reservas_contiguas_y_otro_dia(self):
        self.reservar("08:00", "10:00")
        self.assertEqual(self.reservar("10:00", "12:00").status_code, 302)
        self.assertEqual(self.reservar("08:00", "10:00", fecha="2026-09-26").status_code, 302)

    def test_hora_fin_menor(self):
        self.assertEqual(self.reservar("10:00", "09:00").status_code, 400)

    def test_laboratorio_en_mantenimiento(self):
        self.assertEqual(self.reservar("08:00", "09:00", lab=3).status_code, 400)

    def test_no_elimina_laboratorio_con_reservas(self):
        self.reservar("08:00", "10:00")
        self.client.post("/laboratorios/2/eliminar")
        self.assertEqual(len(self.client.get("/api/laboratorios").get_json()), 3)
        self.client.post("/laboratorios/1/eliminar")                 # este no tiene reservas
        self.assertEqual(len(self.client.get("/api/laboratorios").get_json()), 2)

    def test_filtro_y_reporte(self):
        self.reservar("08:00", "10:30")
        self.reservar("08:00", "09:00", fecha="2026-09-26")
        self.assertEqual(len(self.client.get("/api/reservas?fecha=2026-09-26").get_json()), 1)
        self.assertIn("3.5", self.client.get("/reporte").get_data(as_text=True))

    def test_api_crear(self):
        r = self.client.post("/api/laboratorios", json={"codigo": "LAB-020", "nombre": "Lab Móvil",
                                                         "piso": 1, "capacidad": 10})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["codigo"], "LAB-020")
        self.assertEqual(self.client.post("/api/laboratorios", json={}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
