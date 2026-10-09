# Pruebas de team_gecko.py. Los valores esperados se calculan a mano desde
# CheatCode.cs de obluda3/strikers2013-teambuilder (no se ejecuta el código C#).
import unittest
from unittest import mock
import team_gecko as tg

class TeamGeckoTests(unittest.TestCase):
    def test_nombre_corto_rellena_con_ceros(self):
        # "AB" = 41 42; los 16 bytes se completan con ceros
        self.assertEqual(tg.name_lines("AB"), [
            "06526312 00000010",
            "41420000 00000000",
            "00000000 00000000",
        ])

    def test_nombre_de_16_bytes(self):
        lines = tg.name_lines("ABCDEFGHIJKLMNOP")
        self.assertEqual(lines[1], "41424344 45464748")
        self.assertEqual(lines[2], "494A4B4C 4D4E4F50")

    def test_nombre_demasiado_largo_se_rechaza(self):
        with self.assertRaises(SystemExit):
            tg.name_lines("A" * 17)

    def test_emblema_y_uniforme(self):
        self.assertEqual(tg.emblem_line(3), "0258d868 00000003")
        self.assertEqual(tg.wear_line(2), "0258a05e 00000002")

    def test_jugadores_con_paso_de_0x14(self):
        self.assertEqual(tg.player_line(1, 1), "0258A06E 00000001")
        self.assertEqual(tg.player_line(411, 2), "0258A082 0000019B")

    def test_equipo_completo_orden(self):
        codes = tg.build_codes("AB", 3, 2, [1, 411])
        self.assertEqual(len(codes), 3 + 1 + 1 + 2)
        self.assertEqual(codes[-2], "0258A06E 00000001")
        self.assertEqual(codes[-1], "0258A082 0000019B")

    def test_mas_de_16_jugadores(self):
        with self.assertRaises(SystemExit):
            tg.build_codes(players=list(range(1, 18)))

    def test_jugador_repetido(self):
        with self.assertRaises(SystemExit):
            tg.build_codes(players=[5, 5])

    def test_id_de_jugador_fuera_de_rango(self):
        with self.assertRaises(SystemExit):
            tg.player_line(0, 1)
        with self.assertRaises(SystemExit):
            tg.player_line(412, 1)

    def test_emblema_fuera_de_rango(self):
        with self.assertRaises(SystemExit):
            tg.emblem_line(256)

if __name__ == "__main__":
    unittest.main()
