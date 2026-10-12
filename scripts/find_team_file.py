# Busca en una carpeta de archivos dat (0.bin, 1.bin, ...) cuál es el archivo de equipos.
# Cabecera según TeamFile.Write del editor (Strikers2013Editor/Logic/TeamDef.cs):
#   0x00 = 3 secciones, 0x04 = offset de la lista de punteros, 0x08 = 0x24,
#   0x0C = offset de TEAM_DEFS, 0x10 = número de equipos + 1 (el último puntero es 0),
#   0x14 = 0x24 (stats), 0x18 = nº de stats, 0x1C = offset de Kizuna, 0x20 = nº de entradas Kizuna.
# Los archivos de dat están comprimidos con ShadeLz sin cabecera; si no descomprimen, se prueban tal cual.
#
# Uso:
#   python find_team_file.py <carpeta_con_los_dat>
import os
import re
import struct
import sys
from shadelz import decompress

HEADER = 0x24
STAT_SIZE = 0x14
KIZUNA_SIZE = 0x10

def u32(d, off):
    # El editor usa BeBinaryReader: big endian
    return struct.unpack(">I", d[off:off + 4])[0]

def check_team_file(d):
    """Devuelve un dict con los datos si la cabecera encaja con el formato de equipos, o None."""
    if len(d) < HEADER:
        return None
    if u32(d, 0) != 3 or u32(d, 8) != HEADER or u32(d, 0x14) != HEADER:
        return None
    team_off, team_count = u32(d, 0x0C), u32(d, 0x10)
    stat_count, kiz_off, kiz_count = u32(d, 0x18), u32(d, 0x1C), u32(d, 0x20)
    if not 2 <= team_count <= 512:
        return None
    if team_off + 4 * team_count > len(d):
        return None
    ptrs = [u32(d, team_off + 4 * i) for i in range(team_count)]
    if ptrs[-1] != 0:
        return None
    if any(not HEADER <= p < len(d) for p in ptrs[:-1]):
        return None
    if HEADER + stat_count * STAT_SIZE > kiz_off:
        return None
    if kiz_off + kiz_count * KIZUNA_SIZE > len(d):
        return None
    return {"equipos": team_count - 1, "stats": stat_count, "kizuna": kiz_count}

def inspect(path):
    raw = open(path, "rb").read()
    found = check_team_file(raw)
    if found:
        return "sin comprimir", found
    try:
        dec = decompress(raw)
    except Exception:
        return None, None
    found = check_team_file(dec)
    if found:
        return "ShadeLz", found
    return None, None

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        sys.exit(__doc__)
    folder = argv[0]
    hits = []
    for name in sorted(os.listdir(folder)):
        m = re.fullmatch(r"(\d+)\.bin", name)
        if not m:
            continue
        mode, info = inspect(os.path.join(folder, name))
        if info:
            hits.append((name, mode, info))
    if not hits:
        print("ningún archivo parece el archivo de equipos")
        return 1
    for name, mode, info in hits:
        idx = int(name[:-4])
        print("%s  (dat %d -> archivo 400%02d)  %s: %d equipos, %d stats, %d entradas kizuna"
              % (name, idx, idx, mode, info["equipos"], info["stats"], info["kizuna"]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
