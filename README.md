# Strikers 2013 — herramientas y notas de modding

Herramientas y documentación para modificar **Inazuma Eleven GO Strikers 2013 (Wii)** sobre el mod
Xtreme 2.0 y la traducción al castellano. Este repositorio **no contiene el juego, ISOs, ni archivos de mods o traducciones**:
hace falta tu propia copia legal del juego y los parches se obtienen de sus autores.

## Contenido

- `scripts/shadelz.py`: descompresor/compresor ShadeLz (formato de `dat.bin`), port en Python de Strikers2013-Tools.
- `scripts/player_edit.py`: lee y cambia campos de un jugador (por id) en `Modified/dat/15.bin` (archivo 40015 de jugadores) y lo escribe como bloques sin comprimir, listo para Riivolution.
- `scripts/build_dat15_overlay.py`: atajo de `player_edit.py` que cambia solo la altura (Scale) de Endo (id 1).
- `scripts/dol_peek.py`: muestra los bytes de un `main.dol` en direcciones concretas, para comparar ejecutables de distintas revisiones.
- `docs/estado.md`: estado del proyecto y pruebas realizadas.
- `docs/referencia_jugadores.md`: valores de `element`, `bodytype`, `gender`, `position` y nombres de los perfiles de carga (`charge`).

## Cómo usarlo

1. Tener tu copia legal de Inazuma Eleven GO Strikers 2013 (Wii).
2. Descomprimir `Modified/dat/15.bin` del mod (en la carpeta de Riivolution del mod).
3. Ver los campos de un jugador, sin modificar nada:
   `python scripts/player_edit.py <15.bin_original> --id 1 --show`
4. Editar uno o varios campos y escribir el resultado:
   `python scripts/player_edit.py <15.bin_original> <15.bin_salida> --id 1 scale=1500 element=fire price=300`
   Los valores son enteros (decimal o `0x...`) o nombres de `ENUMS` en `player_edit.py` (`element`, `position`, `bodytype`, `gender`). `name` admite hasta 24 caracteres ASCII.
   Solo cambia el campo indicado: el resto de bytes y de jugadores queda igual.
   Para añadir un jugador nuevo, copia el registro de otro y le asigna el siguiente id libre:
   `python scripts/player_edit.py <15.bin_original> <15.bin_salida> --add-from 1 name=NuevoJugador`
   El juego puede no mostrar un jugador con id nuevo: ver `docs/estado.md`.
6. Poner `<15.bin_salida>` en una carpeta de prueba de Riivolution (`<carpeta>/xtreme2_dev/files/Modified/dat/15.bin`) y superponerla sobre el mod con un descriptor propio.

Requisitos: Python 3.7 o superior. No hace falta CodeWarrior ni Kamek para los cambios de datos.

## Qué no está aquí y por qué

Ver `docs/NO_INCLUIDO.md`.
