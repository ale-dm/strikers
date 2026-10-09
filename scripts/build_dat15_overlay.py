# Edita la altura de Endo (id 1) en el archivo de jugadores 40015 (Modified/dat/15.bin)
# y lo escribe como bloques sin comprimir (formato que acepta ShadeLz).
# Es un atajo de player_edit.py con el id 1 y el campo scale.
#
# Uso:
#   python build_dat15_overlay.py <15.bin_original> <15.bin_salida> [valor_scale]
#
# <15.bin_original>: archivo Modified/dat/15.bin de tu copia del mod (NO se modifica).
# <15.bin_salida>:   donde se escribe el archivo modificado (p. ej. una carpeta de prueba de Riivolution).
import sys
from player_edit import main as edit_player

ENDO_ID = 1

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    new_scale = sys.argv[3] if len(sys.argv) > 3 else "1500"
    return edit_player([src, dst, "--id", str(ENDO_ID), "scale=" + new_scale])

if __name__ == "__main__":
    sys.exit(main())
