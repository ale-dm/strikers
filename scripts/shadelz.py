# Port of ShadeLz.Decompress (Strikers2013-Tools, Utils/ShadeLz.cs), headerless path.
import struct, sys

MAGIC = b"\xFC\xAA\x55\xA7"

def calc_size(inp):
    size, i = 0, 0
    while i < len(inp):
        flag = inp[i]; i += 1
        if flag & 0x80:
            size += ((flag >> 5) & 0x3) + 4; i += 1
        elif flag & 0x60 == 0x60:
            size += flag & 0x1F
        elif flag & 0x40:
            if flag & 0x10 == 0:
                length = (flag & 0xF) + 4
            else:
                length = ((flag & 0xF) << 8) + inp[i] + 4; i += 1
            i += 1; size += length
        else:
            if flag & 0x20 == 0:
                length = flag
            else:
                length = ((flag & 0x1F) << 8) + inp[i]; i += 1
            i += length; size += length
    return size

def decompress(c):
    if c[:4] == MAGIC:
        dsize = struct.unpack("<i", c[4:8])[0]; pos = 12
    else:
        dsize = calc_size(c); pos = 0
    out = bytearray(dsize)
    ip, op, win, prev = pos, 0, 0, 0
    while op < dsize:
        flags = c[ip]; ip += 1
        if flags & 0x80:
            count = ((flags >> 5) & 0x3) + 4
            win = ((flags & 0x1F) << 8) + c[ip]; ip += 1
            prev = win
            for i in range(count): out[op + i] = out[op - win + i]
            op += count
        elif flags & 0x60 == 0x60:
            count = flags & 0x1F; win = prev
            for i in range(count): out[op + i] = out[op - win + i]
            op += count
        elif flags & 0x40:
            if flags & 0x10 == 0:
                count = (flags & 0x0F) + 4
            else:
                count = (((flags & 0x0F) << 8) + c[ip]) + 4; ip += 1
            data = c[ip]; ip += 1
            for i in range(count): out[op] = data; op += 1
        elif flags & 0xC0 == 0:
            if flags & 0x20 == 0:
                count = flags
            else:
                count = ((flags & 0x1F) << 8) + c[ip]; ip += 1
            for i in range(count): out[op] = c[ip]; op += 1; ip += 1
    return bytes(out)

def compress_literal(data):
    # Solo bloques literales (sin back-references): el archivo crece, pero lo acepta el juego.
    out = bytearray(); pos = 0
    while pos < len(data):
        count = min(0x1FFF, len(data) - pos)
        out += bytes([((count & 0x1F00) >> 8) | 0x20, count & 0xFF])
        out += data[pos:pos+count]; pos += count
    return bytes(out)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    data = decompress(open(src, "rb").read())
    open(dst, "wb").write(data)
    print("decompressed", len(data), hex(len(data)))
