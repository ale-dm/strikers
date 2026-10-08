# Registro de pruebas (Dolphin, sobre copias locales del juego)

Todas las pruebas usan la misma base: Xtreme 2.0 de obluda3 (Riivolution) sobre una copia traducida del juego.

## Arranque del mod y la traducción
| Prueba | Base | Resultado |
|---|---|---|
| Xtreme 2.0 sobre la copia HI traducida | HI | Arranca |
| Xtreme 2.0 sobre la copia HF parcheada con el parcheador ISO | HF → ID S5SJHI | Arranca, en castellano |
| Parche de Riivolution de la traducción sobre HF | HF | Arranca, pero en japonés: el parche de Riivolution es para la revisión HI |
| Paquete completo de Infinity | HI y HF | No arranca (negro) |

## Piezas de Infinity sobre Xtreme (cada una por separado)
| Pieza | Resultado |
|---|---|
| `Code/CustomCode.bin` | Arranca |
| `Modified/dat` (97 archivos, incluido `15.bin`) | Arranca |
| `Modified/grp` (1.313 archivos) | Arranca |
| `Modified/scn`, `scn_sh`, `ui` | Arranca |
| `InazmaWii.brsar` + `save.sav` | Arranca |
| `stream` nuevos (2 archivos) | Arranca |
| Todas las piezas a la vez | Arranca |

## Hallazgos sobre el código y las partidas
- Cada `CustomCode.bin` fija el nombre del archivo de partida: Infinity usa `xtreme3.sav` y Xtreme 2.0 usa `xtreme2.sav`.
- En la prueba con todas las piezas, el juego mostró las partidas de `xtreme2.sav` (título "XTREME2"). Eso indica que el código de Infinity **no** estaba activo: las piezas de datos sí se aplicaban, pero el código de la base de Xtreme prevalecía.
- Por tanto, arrancar con las piezas no demuestra que el código de Infinity funcione. El paquete completo, que sí activa su código, no arranca.

## Pendiente
- Entender por qué el código de Infinity no arranca sobre la copia traducida.
- Comprobar en el juego que aparecen los equipos y personajes nuevos de Infinity.
- Destin y Harper no aparecen en el título.
