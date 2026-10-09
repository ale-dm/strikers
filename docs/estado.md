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
- Los mods no crean ids nuevos: reutilizan registros que ya existen. La documentación dice que hay jugadores "no usados" (cita a Shinoyama y a la forma miximax de Saru) y otros "presentes pero no jugables" (managers y entrenadores).
- El editor marca 14 jugadores como "Unused", pero la etiqueta no es fiable. Comparada con el código de Xtreme (`source/`), solo 3 no aparecen referenciados: 267 Hikita Goushirou, 349 Shinoyama Mitsuru (confirmado por la doc) y 406 Afuro Terumi (Unused). Los demás aparecen en listas de Xtreme (premixed, armed, miximax, banlist), así que no son candidatos seguros.
- El id 411 no es "Fran MM": el enum de Xtreme lo llama `P_12502YOBI` y el código lo usa como personaje activo (premixed, armed, miximax). Se descarta como candidato.
- Nada de esto está comprobado en el juego: referenciado en el código no significa jugable.
- `player_edit.py` avisa cuando una copia (`--add-from`) o una edición deja a dos jugadores con el mismo equipo y posición en la lista.

## Equipos (sin comprobar en el juego)
- Un equipo de juego se identifica por su **emblema**: `PLAYER_DEF` tiene `emblem` (0x54), y Xtreme usa `GetTeamIDToEmblemLL` para pasar de equipo a emblema. El enum `Emblem` tiene 101 entradas (`includes/enums.h`).
- Las definiciones de equipo (`TEAM_DEF`: nombre, índice, formación, entrenador, mánager, fuerza y lista de `TEAM_PLAYER`) están en un archivo de equipos aparte, distinto de 40015. El editor lo lee con `TeamFile` y `TeamDef` (`Logic/TeamDef.cs`, `Forms/TeamEditor.cs`). Su escritura rehace los punteros del archivo.
- No sé en qué índice de `dat` está ese archivo: la documentación de Xtreme deja vacías las secciones "Teams" y "Team Definition", y no aparece en el código que tenemos.
- Por tanto, añadir un equipo implica: un emblema existente (o nuevo, con sus modelos y texturas en `grp`), una entrada en el archivo de equipos, y que los jugadores tengan ese `team` y `emblem`. No he probado nada de esto.

## Qué se puede modificar (investigado sin archivos del juego)
Fuentes: `Strikers2013Editor` (obluda3), documentación de Xtreme y `xtreme`. Nada de esto está probado en el juego.

| Área | Archivo | Formato conocido | Herramienta | Notas |
|---|---|---|---|---|
| Jugadores | 40015 (2ª sección) | Sí (`PlayerDef.cs`) | `player_edit.py` | Precio, elemento, perfil de carga, altura, equipo, emblema, posición en la lista |
| Perfiles de carga | 40015 (1ª sección) | Solo por la doc | No | Incrementos del medidor por acción; algunos perfiles marcados UNUSED |
| Movimientos | 40081 (`Modified\dat\81.bin`) | Sí (`Move.cs`) | No (solo `MoveEditor`) | Tier, poder base y máximo, TP, elemento, estado, alcance, quién lo usa (`Users`, `Partners`); muchos campos sin nombre |
| Info de animación de movimientos | Ver `MoveInfo.cs` | Sí (`MoveInfo.cs`) | No (solo `MoveInfoEditor`) | Efectos, uniformes, estadio, rivales |
| Guardado (partida) | `xtreme2.sav` / `xtreme3.sav` (local) | Sí (`Save.cs`) | `SaveEditor` | Estadísticas, movimientos aprendidos, puntos Inazuma, nombre de perfil, emblema del equipo. Útil para probar desbloqueos sin jugar |
| Equipos | Archivo de equipos (índice desconocido) | Sí (`TeamDef.cs`) | `TeamEditor` | Ver la sección de equipos |
| Claves de control | 40011 | Parcial (solo las 2 últimas secciones) | No | Perfiles de control por jugador |
| Copias de jugador | 40017 | Parcial | No | Versiones de un mismo jugador (grupo ListID) |
| Reglas de movimientos (código) | `source/moveset_banlist.cpp` | Sí | Kamek + CodeWarrior | Listas de prohibición y de permitidos por jugador/movimiento. Solo en código |
| Ajustes del mod | `source/xtremeSettings.h` | Sí | Kamek + CodeWarrior | Opciones como mostrar poder, aperturas, teclado, modo mixi. Son ajustes en el menú, no datos |
| Miximax | Código (dirección 0x804c8b90) | Parcial | Kamek + CodeWarrior | No está en ningún archivo |
| Audio | Archivos `stream` | — | Brawlcrate (externo) | Según la doc de Xtreme |

Lo más directo sin el juego: documentar y preparar un editor de movimientos similar a `player_edit.py`. Hay que verificar antes el tamaño exacto del registro en `Move.cs`, porque tiene muchos campos sin nombre.

## Repos de obluda3 revisados (lectura, sin archivos del juego)
- **strikers2013-re-notes** (notas de ingeniería inversa): formato de `TEAM_DEF` y `TEAM_PLAYER`, tabla de `PlayerDef` (con inicio 0xE5C, distinto del 0xFA4 que usa el editor; el editor lee archivos reales, así que confiamos en 0xFA4), desbloqueo de movimientos por kizuna (`main.dol` @0x804C8C50), tabla de miximax (`main.dol` @0x804c8b90), tabla de uniformes (`main.dol` @0x804D08B8), `wazainfo` (tamaño 0x8c), claves, SHTX/TEXCUT/SSAD, archivos y códigos Gecko.
- **strikers2013-teambuilder**: genera **códigos Gecko** que escriben el equipo actual en memoria: nombre (0x80526312), emblema (0x8058D868), uniforme (0x8058A05E) y los ids de los 16 jugadores (base 0x8058A05C, paso 0x14). Coincide con `_SV_TEAM_INFO` de Xtreme. Permite usar jugadores no publicados (p. ej. Aum Nirvana, SARU Miximax). Solo afecta al equipo que se está usando, y necesita Dolphin con el juego.
- **Strikers2013-Tools**: extrae e importa archivos de los `.bin` (con sufijo `.dec` para comprimir al importar) y exporta/importa textos. Textos útiles: `1.bin` (texto principal), `5.bin` (descripciones de movimientos), `113.bin` (tutorial), todos en `dat`.
- **obluda3.github.io**: fuente de la documentación de Xtreme. No aporta nada nuevo sobre el archivo de equipos.

Lo que cambia respecto a lo anterior:
- Para **equipos** hay una vía sin tocar archivos (Gecko, solo equipo actual). La vía por archivo sigue bloqueada por el índice de dat del archivo de equipos.
- Las **listas de nombres no coinciden** entre fuentes para los ids no usados: teambuilder llama 349 a "Aum Nirvana" y 411 a "Flora Miximax"; el editor llama 349 a Shinoyama y 411 a Fran MM; el enum de Xtreme llama 411 a Yobi. Hay que comprobarlo antes de activar nada.

## Próximos pasos
1. Investigar por qué el código de Infinity no arranca sobre la base traducida.
2. Probar cambios de datos sencillos (perfil de carga, precio) con el script de superposición.
3. Si hace falta código nuevo: instalar CodeWarrior SE y Kamek (Windows), siguiendo el README de obluda3/strikers2013-xtreme.
