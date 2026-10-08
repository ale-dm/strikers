# Estado del proyecto

## Objetivo
Modificar el mod Xtreme 2.0 (y la versión con textos en castellano) de Strikers 2013 para Wii: más personajes, equipos y gameplay.

## Lo verificado (en Dolphin)
- El mod Xtreme 2.0 arranca sobre la copia traducida (ID S5SJHI).
- Traducción al castellano: se aplica con el parche de Riivolution de la traducción sobre la revisión HI, y con el parcheador ISO sobre la revisión HF. Las dos versiones muestran texto en castellano.
- Cambio de altura de Endo (jugador id 1) con `build_dat15_overlay.py`: se ve en el campo.
- Partidas: el mod lee `xtreme2.sav` (Xtreme 2.0) o `xtreme3.sav` (Infinity), según el código de cada versión (`CustomCode.bin` fija el nombre del archivo).

## Lo que no funciona todavía
- Infinity (paquete de Riivolution completo) no arranca sobre la base traducida: se queda en negro. Las piezas por separado (datos, gráficos, audio) sí arrancan, pero no contienen el código de Infinity activo.
- En la pantalla de título no aparecen Destin y Harper (la guía del paquete dice que sustituyen a Arion y JP).

## Formato del archivo de jugadores (`dat.bin` entrada 40015)
- Comprimido con ShadeLz sin cabecera (ver `scripts/shadelz.py`).
- Tras descomprimir: contador de jugadores (+1) en `0x10` (big endian); registros desde `0xFA4`, de `0x148` bytes cada uno.
- Dentro de un registro: `0x40` = Scale (altura, 1000 = 100 %), `0x14` = nombre interno, `0xF4` = elemento, `0xF8` = perfil de carga, `0x110` = precio.
- Fuente: [Strikers2013Editor](https://github.com/obluda3/Strikers2013Editor), archivo `PlayerDef.cs`.

## Próximos pasos
1. Investigar por qué el código de Infinity no arranca sobre la base traducida.
2. Probar cambios de datos sencillos (perfil de carga, precio) con el script de superposición.
3. Si hace falta código nuevo: instalar CodeWarrior SE y Kamek (Windows), siguiendo el README de obluda3/strikers2013-xtreme.
