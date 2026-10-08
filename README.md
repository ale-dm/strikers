# Strikers 2013 — herramientas y notas de modding

Herramientas y documentación para modificar **Inazuma Eleven GO Strikers 2013 (Wii)** sobre el mod
Xtreme 2.0 y la traducción al castellano. Este repositorio **no contiene el juego, ISOs, ni archivos de mods o traducciones**:
hace falta tu propia copia legal del juego y los parches se obtienen de sus autores.

## Contenido

- `scripts/shadelz.py`: descompresor/compresor ShadeLz (formato de `dat.bin`), port en Python de Strikers2013-Tools.
- `scripts/build_dat15_overlay.py`: cambia la altura (Scale) de un jugador en `Modified/dat/15.bin` (archivo 40015 de jugadores) y lo escribe como bloques sin comprimir, listo para Riivolution.
- `scripts/dol_peek.py`: muestra los bytes de un `main.dol` en direcciones concretas, para comparar ejecutables de distintas revisiones.
- `docs/estado.md`: estado del proyecto y pruebas realizadas.

## Cómo usarlo

1. Tener tu copia legal de Inazuma Eleven GO Strikers 2013 (Wii).
2. Descomprimir `Modified/dat/15.bin` del mod (en la carpeta de Riivolution del mod).
3. `python scripts/build_dat15_overlay.py <15.bin_original> <15.bin_salida> 1500`
4. Poner `<15.bin_salida>` en una carpeta de prueba de Riivolution (`<carpeta>/xtreme2_dev/files/Modified/dat/15.bin`) y superponerla sobre el mod con un descriptor propio.

Requisitos: Python 3.7 o superior. No hace falta CodeWarrior ni Kamek para los cambios de datos.

## Qué no está aquí y por qué

Ver `docs/NO_INCLUIDO.md`.
