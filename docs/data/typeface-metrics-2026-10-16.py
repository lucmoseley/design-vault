"""The #282 instrument, for docs/research/typeface-traits.md R5: read x-height, cap height, weight, lowercase average advance and fvar axes from TTF files.
Usage: python3 -I docs/data/typeface-metrics-2026-10-16.py FONT...   (no dependencies)
Lowercase advance = mean hmtx advance of a-z at the default instance, in em.
"""

import struct
import sys


def tables(b):
    n = struct.unpack(">H", b[4:6])[0]
    t = {}
    for i in range(n):
        tag, _, off, ln = struct.unpack(">4sIII", b[12 + 16 * i : 28 + 16 * i])
        t[tag.decode("latin1")] = (off, ln)
    return t


def cmap4(b, t):
    off = t["cmap"][0]
    n = struct.unpack(">H", b[off + 2 : off + 4])[0]
    best = None
    for i in range(n):
        pid, eid, so = struct.unpack(">HHI", b[off + 4 + 8 * i : off + 12 + 8 * i])
        fmt = struct.unpack(">H", b[off + so : off + so + 2])[0]
        if fmt == 4 and pid in (0, 3):
            best = off + so
    if best is None:
        return {}
    s = best
    segx2 = struct.unpack(">H", b[s + 6 : s + 8])[0]
    seg = segx2 // 2
    ends = struct.unpack(">%dH" % seg, b[s + 14 : s + 14 + segx2])
    starts = struct.unpack(">%dH" % seg, b[s + 16 + segx2 : s + 16 + 2 * segx2])
    deltas = struct.unpack(">%dh" % seg, b[s + 16 + 2 * segx2 : s + 16 + 3 * segx2])
    roff_pos = s + 16 + 3 * segx2
    roffs = struct.unpack(">%dH" % seg, b[roff_pos : roff_pos + segx2])
    m = {}
    for c in range(ord("a"), ord("z") + 1):
        for k in range(seg):
            if starts[k] <= c <= ends[k]:
                if roffs[k] == 0:
                    g = (c + deltas[k]) & 0xFFFF
                else:
                    p = roff_pos + 2 * k + roffs[k] + 2 * (c - starts[k])
                    g = struct.unpack(">H", b[p : p + 2])[0]
                    if g:
                        g = (g + deltas[k]) & 0xFFFF
                m[chr(c)] = g
                break
    return m


def main(path):
    b = open(path, "rb").read()
    t = tables(b)
    upm = struct.unpack(">H", b[t["head"][0] + 18 : t["head"][0] + 20])[0]
    o = t["OS/2"][0]
    ver = struct.unpack(">H", b[o : o + 2])[0]
    wt = struct.unpack(">H", b[o + 4 : o + 6])[0]
    xh = cap = None
    if ver >= 2:
        xh, cap = struct.unpack(">hh", b[o + 86 : o + 90])
    nh = struct.unpack(">H", b[t["hhea"][0] + 34 : t["hhea"][0] + 36])[0]
    h = t["hmtx"][0]

    def adv(g):
        g = min(g, nh - 1)
        return struct.unpack(">H", b[h + 4 * g : h + 4 * g + 2])[0]

    cm = cmap4(b, t)
    lc = sum(adv(g) for g in cm.values()) / len(cm) / upm if cm else None
    axes = []
    if "fvar" in t:
        f = t["fvar"][0]
        aoff, _, cnt, size = struct.unpack(">HHHH", b[f + 4 : f + 12])
        for i in range(cnt):
            p = f + aoff + i * size
            tag = b[p : p + 4].decode()
            mn, df, mx = [v / 65536 for v in struct.unpack(">iii", b[p + 4 : p + 16])]
            axes.append("%s %g-%g (def %g)" % (tag, mn, mx, df))
    name = path.rsplit("/", 1)[-1]
    print(
        "%-26s upm %5d  x-height %s  cap %s  x/cap %s  lc-adv %s  wt %d  %s"
        % (
            name,
            upm,
            "%.3f" % (xh / upm) if xh else "-",
            "%.3f" % (cap / upm) if cap else "-",
            "%.2f" % (xh / cap) if xh and cap else "-",
            "%.3f" % lc if lc else "-",
            wt,
            "; ".join(axes),
        )
    )


for p in sys.argv[1:]:
    try:
        main(p)
    except (OSError, KeyError, IndexError, struct.error) as e:
        print(p, "ERROR", e)
