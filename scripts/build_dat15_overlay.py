# Edita la altura de Endo (registro 1, id 1) en el archivo de jugadores 40015 (Modified/dat/15.bin)
# y lo escribe como bloques sin comprimir (formato que acepta ShadeLz).
#
# Uso:
#   python build_dat15_overlay.py <15.bin_original> <15.bin_salida> [valor_scale]
#
# <15.bin_original>: archivo Modified/dat/15.bin de tu copia del mod (NO se modifica).
# <15.bin_salida>:   donde se escribe el archivo modificado (p. ej. una carpeta de prueba de Riivolution).
import struct, sys
from shadelz import decompress

REC = 0xFA4        # inicio de los registros de jugadores
SIZE = 0x148       # tamaño de cada registro PLAYER_DEF
SCALE_OFF = 0x40   # campo Scale (altura) dentro del registro

def legacy_compress(data):
    out = bytearray(); pos = 0
    while pos < len(data):
        count = min(0x1FFF, len(data) - pos)
        out += bytes([((count & 0x1F00) >> 8) | 0x20, count & 0xFF])
        out += data[pos:pos+count]; pos += count
    return bytes(out)

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    new_scale = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    d = bytearray(decompress(open(src, "rb").read()))
    assert struct.unpack(">I", d[REC:REC+4])[0] == 1, "el primer registro no es el id 1"
    off = REC + SCALE_OFF
    old = struct.unpack(">I", d[off:off+4])[0]
    d[off:off+4] = struct.pack(">I", new_scale)
    enc = legacy_compress(bytes(d))
    assert decompress(enc) == bytes(d), "fallo al comprobar la recompresion"
    open(dst, "wb").write(enc)
    print("Endo scale: %d -> %d (tamano descomprimido %d)" % (old, new_scale, len(d)))

if __name__ == "__main__":
    main()
