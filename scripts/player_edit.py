# Edita campos de un jugador en el archivo de jugadores 40015 (Modified/dat/15.bin)
# y lo escribe como bloques sin comprimir (formato que acepta ShadeLz).
#
# Uso:
#   python player_edit.py <15.bin_original> --id 1 --show
#   python player_edit.py <15.bin_original> <15.bin_salida> --id 1 scale=1500 price=300
#
# Valores: enteros (decimal o 0x...) o nombres de la lista de ENUMS (p. ej. element=fire).
# <15.bin_original> no se modifica. Offsets y tipos: Strikers2013Editor/Logic/PlayerDef.cs
# (obluda3/strikers2013editor). Todos los enteros son big endian.
import argparse
import struct
import sys
from shadelz import decompress, compress_literal

HEADER = 0x10      # contador de registros (valor = registros + 1)
REC = 0xFA4        # inicio de los registros de jugadores
SIZE = 0x148       # tamaño de cada registro PLAYER_DEF
NAME_LEN = 24

# campo: (offset dentro del registro, formato struct, descripción)
FIELDS = {
    "name":           (0x14,  None, "nombre interno, ASCII de hasta 24 caracteres"),
    "gender":         (0x2C,  ">i", "sexo (ver ENUMS)"),
    "bodytype":       (0x3C,  ">i", "tipo de cuerpo (ver ENUMS)"),
    "scale":          (0x40,  ">i", "altura, 1000 = 100 %"),
    "shadow":         (0x44,  ">i", "tamaño de la sombra"),
    "team":           (0x50,  ">i", "equipo"),
    "position":       (0x5C,  ">i", "posición (ver ENUMS)"),
    "voice":          (0x104, ">i", "voz"),
    "voice_alias":    (0x108, ">i", "alias de voz"),
    "element":        (0xF4,  ">i", "elemento (ver ENUMS)"),
    "charge":         (0xF8,  ">i", "perfil de carga"),
    "price":          (0x110, ">h", "precio"),
    "list_pos":       (0x112, ">h", "posición en la lista"),
    "team_list_pos":  (0x114, ">i", "posición en la lista del equipo"),
}

ENUMS = {
    "gender":   {"male": 0, "female": 1, "other": 2},
    "bodytype": {"man": 0, "large": 1, "chibi": 2, "muscle": 3, "girl1": 4, "girl2": 5},
    "position": {"gk": 0, "df": 0x23, "mf": 0x24, "fw": 0x25},
    "element":  {"wind": 0, "wood": 1, "fire": 2, "earth": 3, "void": 4},
}

def find_player(d, pid):
    # Igual que el editor: hay (contador - 1) registros desde REC.
    count = struct.unpack(">I", d[HEADER:HEADER+4])[0]
    for k in range(count - 1):
        off = REC + k * SIZE
        if off + SIZE > len(d):
            break
        if struct.unpack(">i", d[off:off+4])[0] == pid:
            return off
    sys.exit("no hay ningun jugador con id %d" % pid)

def read_field(d, off, name):
    foff, fmt, _ = FIELDS[name]
    start = off + foff
    if name == "name":
        return bytes(d[start:start+NAME_LEN]).rstrip(b"\0").decode("ascii", "replace")
    return struct.unpack(fmt, d[start:start+struct.calcsize(fmt)])[0]

def parse_value(name, text, parser):
    if name == "name":
        if not text.isascii() or len(text) > NAME_LEN:
            parser.error("name: ASCII de maximo %d caracteres" % NAME_LEN)
        return text.encode("ascii")
    if text.lower() in ENUMS.get(name, {}):
        return ENUMS[name][text.lower()]
    try:
        return int(text, 0)
    except ValueError:
        parser.error("%s: valor no valido '%s'" % (name, text))

def write_field(d, off, name, value, parser):
    foff, fmt, _ = FIELDS[name]
    start = off + foff
    if name == "name":
        d[start:start+NAME_LEN] = value.ljust(NAME_LEN, b"\0")
        return
    try:
        packed = struct.pack(fmt, value)
    except struct.error:
        parser.error("%s: valor %d fuera de rango" % (name, value))
    d[start:start+len(packed)] = packed

def main(argv=None):
    parser = argparse.ArgumentParser(description="Edita campos de un jugador en 40015 (15.bin).")
    parser.add_argument("src", help="15.bin original (descomprimido o ShadeLz)")
    parser.add_argument("dst", nargs="?", help="archivo de salida")
    parser.add_argument("--id", type=int, required=True, help="id del jugador (p. ej. 1 = Endo)")
    parser.add_argument("--show", action="store_true", help="muestra los campos y no escribe nada")
    parser.add_argument("cambios", nargs="*", metavar="campo=valor")
    args = parser.parse_args(argv)

    d = bytearray(decompress(open(args.src, "rb").read()))
    off = find_player(d, args.id)

    if args.show:
        for name, (foff, _, desc) in FIELDS.items():
            print("%-14s 0x%03X  %-24s %s" % (name, foff, read_field(d, off, name), desc))
        return 0

    if not args.dst or not args.cambios:
        parser.error("hacen falta <salida> y al menos un campo=valor (o usa --show)")

    for item in args.cambios:
        name, sep, text = item.partition("=")
        if not sep or name not in FIELDS:
            parser.error("campo desconocido o formato incorrecto: '%s' (campos: %s)" % (item, ", ".join(FIELDS)))
        old = read_field(d, off, name)
        write_field(d, off, name, parse_value(name, text, parser), parser)
        print("%s: %s -> %s" % (name, old, read_field(d, off, name)))

    enc = compress_literal(bytes(d))
    assert decompress(enc) == bytes(d), "fallo al comprobar la recompresion"
    open(args.dst, "wb").write(enc)
    print("escrito %s (tamano descomprimido %d)" % (args.dst, len(d)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
