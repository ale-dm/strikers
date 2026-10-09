# Estado del proyecto

## Objetivo
Modificar el mod Xtreme 2.0 (y la versión con textos en castellano) de Strikers 2013 para Wii: más personajes, equipos y gameplay.

## Lo verificado (en Dolphin)
- El mod Xtreme 2.0 arranca sobre la copia traducida (ID S5SJHI).
- Traducción al castellano: se aplica con el parche de Riivolution de la traducción sobre la revisión HI, y con el parcheador ISO sobre la revisión HF. Las dos versiones muestran texto en castellano.
- Cambio de altura de Endo (jugador id 1) con `build_dat15_overlay.py`: se ve en el campo.
- Partidas: el mod lee `xtreme2.sav` (Xtreme 2.0) o `xtreme3.sav` (Infinity), según el código de cada versión (`CustomCode.bin` fija el nombre del archivo).

## Lo que no funciona todavía (ver docs/pruebas.md)
- Infinity (paquete de Riivolution completo) no arranca sobre la base traducida: se queda en negro. Las piezas por separado (datos, gráficos, audio) sí arrancan, pero no contienen el código de Infinity activo.
- En la pantalla de título no aparecen Destin y Harper (la guía del paquete dice que sustituyen a Arion y JP).

## Formato del archivo de jugadores (`dat.bin` entrada 40015)
- Comprimido con ShadeLz sin cabecera (ver `scripts/shadelz.py`).
- Tras descomprimir: contador de jugadores (+1) en `0x10` (big endian); registros desde `0xFA4`, de `0x148` bytes cada uno.
- Dentro de un registro: `0x40` = Scale (altura, 1000 = 100 %), `0x14` = nombre interno (ASCII, 24 bytes), `0xF4` = elemento, `0xF8` = perfil de carga, `0x110` = precio (int16).
- Campos que edita `scripts/player_edit.py`: name, gender (0x2C), bodytype (0x3C), scale (0x40), shadow (0x44), team (0x50), emblem (0x54), position (0x5C), voice (0x104), voice_alias (0x108), element (0xF4), charge (0xF8), price (0x110, int16), list_pos (0x112, int16), team_list_pos (0x114).
- Fuente: [Strikers2013Editor](https://github.com/obluda3/Strikers2013Editor), archivo `Strikers2013Editor/Logic/PlayerDef.cs`. Los offsets se revisaron contra esa clase: suman 0x148 bytes por registro.
- Los registros se buscan por id (no por posición). Cómo se leen: `Forms/PlayerEditor.cs`, con `count - 1` registros desde `0xFA4`.

## Verificado sin el juego
- `player_edit.py` con un `15.bin` sintético: cada edición cambia solo los bytes del campo; el resto de jugadores queda igual; los valores fuera de rango o mal escritos dan error. `build_dat15_overlay.py` produce la misma salida byte a byte que la versión anterior.
- `--add-from`: añade un registro copiado con id = máximo + 1 y actualiza el contador. Probado con un `15.bin` sintético; se rechaza si hay bytes tras los registros.
- Pendiente: comprobar en Dolphin los valores de `element`, `charge` y `price`, y que el juego acepta el archivo con varios cambios a la vez.

## Añadir jugadores: límites conocidos (sin comprobar en el juego)
- Los ids de serie son 1–411 (`includes/enums.h` de obluda3/strikers2013-xtreme). Un jugador nuevo tendría id 412 o superior.
- `source/randomMode.cpp` elige con `shdRndi(1, 0x19C)` (0x19C = 412; según si `shdRndi` incluye el límite superior, llega hasta 411 o 412) y cuenta reclutados con `i < P_12502YOBI` (411). Un jugador nuevo no entraría en el aleatorio ni en esos contadores sin cambiar ese código. No he comprobado la semántica de `shdRndi`.
- Las banderas de jugador (reclutado, desbloqueado) están indexadas por id en la partida; no está claro el tamaño de esa tabla.
- Hace falta que el jugador esté en una plantilla de equipo, con modelos, rostro y textos. Eso está en otros archivos, no en 40015.

## Cómo se activan jugadores (docs de Xtreme, sin comprobar en el juego)
- Según la documentación de Xtreme (obluda3.github.io/strikers, sección Players): un jugador aparece si tiene equipo y emblema válidos y una posición en la lista válida. Si dos comparten equipo y posición en la lista, solo sale el de id menor.
- `price` > 0 habilita al jugador; `-1` lo desbloquea por defecto.
- Los mods no crean ids nuevos: reutilizan los registros que ya existen. El editor de nombres marca 14 jugadores como no usados (`Common/playernames.txt` del editor): ids 267, 268, 269, 271, 349, 361, 392, 397, 398, 404, 405, 406, 410 y 411.
- Discrepancia por revisar: el id 411 es `P_12502YOBI` en el enum de Xtreme, pero "Fran MM (Unused)" en la lista del editor.
- `player_edit.py` avisa cuando una copia (`--add-from`) o una edición deja a dos jugadores con el mismo equipo y posición en la lista.

## Próximos pasos
1. Investigar por qué el código de Infinity no arranca sobre la base traducida.
2. Probar cambios de datos sencillos (perfil de carga, precio) con el script de superposición.
3. Si hace falta código nuevo: instalar CodeWarrior SE y Kamek (Windows), siguiendo el README de obluda3/strikers2013-xtreme.
