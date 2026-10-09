# Genera códigos Gecko que escriben el equipo actual en memoria de Dolphin.
# Port de CheatCode.cs y Form1.cs de obluda3/strikers2013-teambuilder, con validaciones.
# No modifica ningún archivo: el resultado se pega en el gestor de códigos Gecko de Dolphin
# y solo afecta al equipo que se está usando mientras corre el juego.
#
# Uso:
#   python team_gecko.py --name "Mi equipo" --emblem 3 --uniform 2 --players 1,2,3
#   python team_gecko.py --players 1,2 --out codigos.txt
import argparse
import sys

NAME_ADDR = "06526312"     # escritura de cadena en 0x80526312
NAME_MAX = 16              # bytes Shift-JIS
EMBLEM_ADDR = "0258d868"   # 0x8058D868
WEAR_ADDR = "0258a05e"     # 0x8058A05E (uniforme)
PLAYER_BASE = 0x58A06E     # id del jugador 1 (0x8058A05C + 0x10 + 2)
PLAYER_STRIDE = 0x14       # _SV_PLAYER_TEAM_INFO
PLAYER_SLOTS = 16          # _SV_TEAM_INFO.players[16]
PLAYER_MAX_ID = 411        # ids de jugador de serie (ver docs/estado.md)
BYTE_MAX = 0xFF

def name_lines(name):
    raw = name.encode("shift_jis")
    if len(raw) > NAME_MAX:
        sys.exit("nombre demasiado largo: %d bytes en Shift-JIS (máximo %d)" % (len(raw), NAME_MAX))
    raw = raw.ljust(NAME_MAX, b"\0")
    # Cabecera y dos líneas de 8 bytes, como en CheatCode.TeamNameCode
    def chunk(b):
        return b[0:4].hex().upper() + " " + b[4:8].hex().upper()
    return [NAME_ADDR + " 00000010", chunk(raw[0:8]), chunk(raw[8:16])]

def emblem_line(emblem_id):
    if not 0 <= emblem_id <= BYTE_MAX:
        sys.exit("emblema fuera de rango: %d" % emblem_id)
    return EMBLEM_ADDR + " 000000" + "%02X" % emblem_id

def wear_line(wear_id):
    if not 0 <= wear_id <= BYTE_MAX:
        sys.exit("uniforme fuera de rango: %d" % wear_id)
    return WEAR_ADDR + " 000000" + "%02X" % wear_id

def player_line(player_id, slot):
    # slot empieza en 1, como en playerCheatCode(playerid, playerIndex)
    if not 1 <= player_id <= PLAYER_MAX_ID:
        sys.exit("id de jugador fuera de rango: %d (1-%d)" % (player_id, PLAYER_MAX_ID))
    addr = PLAYER_BASE + (slot - 1) * PLAYER_STRIDE
    return "02%06X 0000%04X" % (addr, player_id)

def build_codes(name=None, emblem=None, uniform=None, players=()):
    if len(players) > PLAYER_SLOTS:
        sys.exit("un equipo tiene como máximo %d jugadores (hay %d)" % (PLAYER_SLOTS, len(players)))
    if len(set(players)) != len(players):
        sys.exit("hay jugadores repetidos en el equipo")
    codes = []
    if name:
        codes += name_lines(name)
    if emblem:
        codes.append(emblem_line(emblem))
    if uniform:
        codes.append(wear_line(uniform))
    for slot, pid in enumerate(players, start=1):
        codes.append(player_line(pid, slot))
    return codes

def main(argv=None):
    ap = argparse.ArgumentParser(description="Códigos Gecko para escribir el equipo actual (Dolphin).")
    ap.add_argument("--name", help="nombre del equipo (máx. 16 bytes Shift-JIS)")
    ap.add_argument("--emblem", type=int, help="id de emblema (1-255)")
    ap.add_argument("--uniform", type=int, help="id de uniforme (1-255)")
    ap.add_argument("--players", default="", help="ids de jugador separados por comas, hasta 16")
    ap.add_argument("--out", help="archivo de salida (si no, se imprime)")
    args = ap.parse_args(argv)

    players = [int(x) for x in args.players.split(",") if x.strip()]
    codes = build_codes(args.name, args.emblem, args.uniform, players)
    text = "\n".join(codes) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print("escritos %d renglones en %s" % (len(codes), args.out))
    else:
        sys.stdout.write(text)
    return 0

if __name__ == "__main__":
    sys.exit(main())
