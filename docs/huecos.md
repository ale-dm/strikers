# Huecos para equipos nuevos (sin comprobar en el juego)

Un equipo nuevo necesita: un emblema (id, textura en `grp`), una entrada en el archivo de equipos
(índice de `dat` desconocido) y, si el equipo tiene uniforme propio, una fila en `uniformDataTbl`
(`main.dol` @0x804D08B8). Esta página solo cubre los ids libres.

## Emblemas libres

Contrastado entre el enum `Emblem` de Xtreme (`includes/enums.h`) y `Common/emblemNames.txt` del editor.
Solo cuentan los ids que aparecen libres en las dos fuentes:

| Ids | Motivo |
|---|---|
| 69–80 | Sin entrada en el enum y marcados UNUSED en el editor (12 ids) |
| 87–89 | Sin entrada en el enum y UNUSED en el editor (3 ids) |
| 95 | Sin entrada en el enum y UNUSED en el editor (1 id) |

Ids que NO son libres aunque el editor diga UNUSED: 81–84 (E_AKI_B, E_HARUNA_B, E_NATSUMI_B, E_HUYUKA_B)
y 86 (E_TSURUGI_SCHOOL), porque el enum les da nombre. Id 38 (Mary Times) tampoco es libre: el editor tiene nombre.

## Uniformes libres

`teambuilder/data/Database.cs` marca UNUSED los uniformes 36–40 y 45–51 (12 ids). No hay enum de
uniformes en el código que tenemos, así que esto solo viene de la lista del teambuilder.

## Prueba en Dolphin (con el juego)

Cada emblema libre se prueba con un código Gecko del equipo actual. Si el emblema no se ve, el
hueco no sirve sin textura nueva. Probar uno por uno:

```
python scripts/team_gecko.py --emblem 69
python scripts/team_gecko.py --emblem 70
# ... hasta 80, luego 87, 88, 89 y 95
```

Qué mirar en el juego: el emblema del equipo en el menú de equipo, y si aparece en blanco, con
otro escudo o si el juego se cierra.
