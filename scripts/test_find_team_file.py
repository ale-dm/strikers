# Pruebas de find_team_file.py con cabeceras construidas según TeamFile.Write (big endian).
import struct
import unittest
import find_team_file as ftf

def make_team_file(team_count=3, stat_count=2, kiz_count=1):
    d = bytearray(0x200)
    def be(off, v):
        struct.pack_into(">I", d, off, v)
    be(0, 3); be(4, 0x180); be(8, 0x24); be(0xC, 0x100)
    be(0x10, team_count); be(0x14, 0x24); be(0x18, stat_count); be(0x1C, 0x24 + stat_count * 0x14); be(0x20, kiz_count)
    for i, p in enumerate([0x60, 0x78]):
        be(0x100 + 4 * i, p)
        be(p, 0x90); be(p + 0x10, 0xA0); be(p + 0x14, 0xB0)  # nombre, jugadores, metadatos
    be(0x100 + 4 * (team_count - 1), 0)
    return d

class FindTeamFileTests(unittest.TestCase):
    def test_archivo_valido(self):
        self.assertEqual(ftf.check_team_file(bytes(make_team_file())),
                         {"equipos": 2, "stats": 2, "kizuna": 1})

    def test_cabecera_incorrecta(self):
        d = make_team_file(); struct.pack_into(">I", d, 0, 4)
        self.assertIsNone(ftf.check_team_file(bytes(d)))

    def test_puntero_fuera_de_rango(self):
        d = make_team_file(); struct.pack_into(">I", d, 0x100, 0x1000)
        self.assertIsNone(ftf.check_team_file(bytes(d)))

    def test_sentinel_no_es_cero(self):
        d = make_team_file(); struct.pack_into(">I", d, 0x108, 5)
        self.assertIsNone(ftf.check_team_file(bytes(d)))

    def test_archivo_corto(self):
        self.assertIsNone(ftf.check_team_file(b"\x00" * 10))

if __name__ == "__main__":
    unittest.main()
