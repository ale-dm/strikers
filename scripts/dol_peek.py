import struct, sys
def addr_to_off(dol, addr):
    for i in range(18):
        off = struct.unpack(">I", dol[i*4:i*4+4])[0]
        sa  = struct.unpack(">I", dol[0x48+i*4:0x48+i*4+4])[0]
        sz  = struct.unpack(">I", dol[0x90+i*4:0x90+i*4+4])[0]
        if sz and sa <= addr < sa+sz:
            return off + (addr - sa), i
    return None, None
for path in sys.argv[1:]:
    d = open(path, "rb").read()
    out = []
    for a in (0x804EACD0, 0x803313D0, 0x805060DC):
        o, sec = addr_to_off(d, a)
        out.append("%08X:%s" % (a, d[o:o+8].hex() if o is not None else "unmapped"))
    print(path.split("\\")[-3] if "\\" in path else path, " | ".join(out))
