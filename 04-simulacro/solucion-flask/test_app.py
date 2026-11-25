import os
import tempfile
import unittest

import app as m


class TestReservas(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".db")
        m.app.config.update(TESTING=True, DATABASE=self.path)
        with m.app.app_context():
            m.init_db()
        self.c = m.app.test_client()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.path)

    def reservar(self, ini, fin, lab=2, fecha="2026-09-25"):
        return self.c.post("/reservas", data={"docente": "Prof. Ruiz", "laboratorio_id": lab,
                                              "fecha": fecha, "hora_inicio": ini, "hora_fin": fin})

    # Pruebas unitarias de la regla de choque
    def test_se_cruzan(self):
        self.assertTrue(m.se_cruzan("08:00", "10:00", "09:00", "11:00"))
        self.assertTrue(m.se_cruzan("08:00", "12:00", "09:00", "10:00"))    # contenida
        self.assertFalse(m.se_cruzan("08:00", "10:00", "10:00", "12:00"))   # contiguas

    # Integración
    def test_reserva_valida(self):
        self.assertEqual(self.reservar("08:00", "10:00").status_code, 302)

    def test_choque(self):
        self.reservar("08:00", "10:00")
        r = self.reservar("09:00", "11:00")
        self.assertEqual(r.status_code, 400)
        self.assertIn("Horario ocupado", r.get_data(as_text=True))

    def test_contiguas_y_otro_dia(self):
        self.reservar("08:00", "10:00")
        self.assertEqual(self.reservar("10:00", "12:00").status_code, 302)
        self.assertEqual(self.reservar("08:00", "10:00", fecha="2026-09-26").status_code, 302)

    def test_fin_menor_inicio(self):
        self.assertEqual(self.reservar("10:00", "09:00").status_code, 400)

    def test_mantenimiento(self):
        self.assertEqual(self.reservar("08:00", "09:00", lab=3).status_code, 400)

    def test_no_elimina_lab_con_reservas(self):
        self.reservar("08:00", "10:00")
        self.c.post("/laboratorios/2/eliminar")
        self.assertEqual(len(self.c.get("/api/laboratorios").get_json()), 3)

    def test_reporte_horas(self):
        self.reservar("08:00", "10:30")
        self.assertIn("2.5", self.c.get("/reporte").get_data(as_text=True))

    def test_api_crear_y_duplicado(self):
        body = {"codigo": "lab-010", "nombre": "Lab IA", "piso": 3, "capacidad": 15}
        self.assertEqual(self.c.post("/api/laboratorios", json=body).status_code, 201)
        self.assertEqual(self.c.post("/api/laboratorios", json=body).status_code, 400)


if __name__ == "__main__":
    unittest.main()
