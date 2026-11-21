"""font-file.py — reads the tables of a font file a page loads, for
check-load.py's --files mode (#313), with no font library: TrueType and
OpenType (sfnt), WOFF and WOFF2.

    font = fontfile.read(data, unbrotli)   # Font, or FontError
    font.features      # {'smcp', 'kern', …}: GSUB's and GPOS's feature tags
    font.chars         # {0x41, …}: every code point the cmap maps
    font.axes          # {'wght': (100, 400, 900), …}: fvar's axes
    font.postscript    # the name table's PostScript name (ID 6)
    font.family        # its typographic family (ID 16), else family (ID 1)
    font.italic        # OS/2 fsSelection's italic bit, else head macStyle's

WOFF2 compresses every table in one Brotli stream, which the standard library
cannot open: `unbrotli(bytes) -> bytes` decodes it. The tables read here are
never transformed (WOFF2 §5.1, only glyf, loca and hmtx are), and lie back to
back in the stream in directory order. A font collection (ttcf) is refused.
"""

import collections
import struct
import zlib

# WOFF2 §5.2's known table tags, by the index a directory entry's flags give.
WOFF2_TAGS = (
    "cmap head hhea hmtx maxp name OS/2 post cvt  fpgm glyf loca prep CFF  VORG "
    "EBDT EBLC gasp hdmx kern LTSH PCLT VDMX vhea vmtx BASE GDEF GPOS GSUB EBSC "
    "JSTF MATH CBDT CBLC COLR CPAL SVG  sbix acnt avar bdat bloc bsln cvar fdsc "
    "feat fmtx fvar gvar hsty just lcar mort morx opbd prop trak Zapf Silf Glat "
    "Gloc Feat Sill"
)
WOFF2_TAGS = [WOFF2_TAGS[i : i + 4] for i in range(0, len(WOFF2_TAGS), 5)]
SFNT = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1")
WANTED = ("cmap", "GSUB", "GPOS", "fvar", "name", "OS/2", "head")

Font = collections.namedtuple("Font", "features chars axes postscript family italic")


class FontError(Exception):
    pass


def read(data, unbrotli=None):
    """The Font in `data`, a whole font file's bytes."""
    try:
        tables = _tables(bytes(data), unbrotli)
        return Font(
            features=_features(tables.get("GSUB")) | _features(tables.get("GPOS")),
            chars=_chars(tables.get("cmap")),
            axes=_axes(tables.get("fvar")),
            postscript=_name(tables.get("name"), (6,)),
            family=_name(tables.get("name"), (16, 1)),
            italic=_italic(tables),
        )
    except (struct.error, IndexError, zlib.error) as exc:
        raise FontError(f"a table is cut short or malformed ({exc})") from exc


def kind(data):
    """The file format `data` begins with: sfnt, woff, woff2, ttc, or None."""
    head = bytes(data[:4])
    if head in SFNT:
        return "sfnt"
    return {b"wOFF": "woff", b"wOF2": "woff2", b"ttcf": "ttc"}.get(head)


def _tables(data, unbrotli):
    form = kind(data)
    if form == "sfnt":
        (count,) = struct.unpack_from(">H", data, 4)
        out = {}
        for i in range(count):
            tag, _, offset, length = struct.unpack_from(">4sIII", data, 12 + 16 * i)
            out[tag.decode("latin-1")] = data[offset : offset + length]
        return out
    if form == "woff":
        (count,) = struct.unpack_from(">H", data, 12)
        out = {}
        for i in range(count):
            tag, offset, comp, orig, _ = struct.unpack_from(
                ">4sIIII", data, 44 + 20 * i
            )
            raw = data[offset : offset + comp]
            out[tag.decode("latin-1")] = zlib.decompress(raw) if comp < orig else raw
        return out
    if form == "woff2":
        return _woff2(data, unbrotli)
    if form == "ttc":
        raise FontError("a font collection (ttcf), which this reader does not open")
    raise FontError(f"no font signature: begins {bytes(data[:4])!r}")


def _woff2(data, unbrotli):
    if unbrotli is None:
        raise FontError("a WOFF2 file, and no Brotli decoder was given")
    flavor, _, count = struct.unpack_from(">4sIH", data, 4)
    if flavor == b"ttcf":
        raise FontError("a WOFF2 font collection, which this reader does not open")
    (compressed,) = struct.unpack_from(">I", data, 20)
    at = 48
    entries = []
    for _ in range(count):
        flags = data[at]
        at += 1
        if flags & 0x3F == 0x3F:
            tag = data[at : at + 4].decode("latin-1")
            at += 4
        else:
            tag = WOFF2_TAGS[flags & 0x3F]
        orig, at = _base128(data, at)
        version = flags >> 6
        transformed = (tag in ("glyf", "loca") and version != 3) or (
            tag == "hmtx" and version != 0
        )
        length = orig
        if transformed:
            length, at = _base128(data, at)
        entries.append((tag, length))
    stream = unbrotli(data[at : at + compressed])
    out, offset = {}, 0
    for tag, length in entries:
        if tag in WANTED:
            out[tag] = stream[offset : offset + length]
        offset += length
    if offset != len(stream):
        raise FontError("the WOFF2 tables do not fill the decompressed stream")
    return out


def _base128(data, at):
    value = 0
    for i in range(5):
        byte = data[at + i]
        if i == 0 and byte == 0x80:
            raise FontError("a WOFF2 UIntBase128 with a leading zero")
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            return value, at + i + 1
    raise FontError("a WOFF2 UIntBase128 longer than 5 bytes")


def _features(table):
    """The feature tags of a GSUB or GPOS table's FeatureList."""
    if not table:
        return set()
    (offset,) = struct.unpack_from(">H", table, 6)
    (count,) = struct.unpack_from(">H", table, offset)
    return {
        table[offset + 2 + 6 * i : offset + 6 + 6 * i].decode("latin-1")
        for i in range(count)
    }


def _chars(table):
    if not table:
        return set()
    (count,) = struct.unpack_from(">H", table, 2)
    out = set()
    for i in range(count):
        platform, encoding, offset = struct.unpack_from(">HHI", table, 4 + 8 * i)
        if not (platform == 0 or (platform == 3 and encoding in (1, 10))):
            continue
        (form,) = struct.unpack_from(">H", table, offset)
        if form == 4:
            out |= _cmap4(table, offset)
        elif form == 12:
            (groups,) = struct.unpack_from(">I", table, offset + 12)
            for g in range(groups):
                start, end, glyph = struct.unpack_from(
                    ">III", table, offset + 16 + 12 * g
                )
                out.update(c for c in range(start, end + 1) if glyph + c - start)
    return out


def _cmap4(table, offset):
    (doubled,) = struct.unpack_from(">H", table, offset + 6)
    n = doubled // 2
    ends = struct.unpack_from(f">{n}H", table, offset + 14)
    starts = struct.unpack_from(f">{n}H", table, offset + 16 + doubled)
    deltas = struct.unpack_from(f">{n}h", table, offset + 16 + 2 * doubled)
    ranges_at = offset + 16 + 3 * doubled
    ranges = struct.unpack_from(f">{n}H", table, ranges_at)
    out = set()
    for i in range(n):
        for c in range(starts[i], ends[i] + 1):
            if c == 0xFFFF:
                continue
            if ranges[i] == 0:
                glyph = (c + deltas[i]) & 0xFFFF
            else:
                at = ranges_at + 2 * i + ranges[i] + 2 * (c - starts[i])
                (glyph,) = struct.unpack_from(">H", table, at)
                glyph = (glyph + deltas[i]) & 0xFFFF if glyph else 0
            if glyph:
                out.add(c)
    return out


def _axes(table):
    if not table:
        return {}
    offset, _, count, size = struct.unpack_from(">HHHH", table, 4)
    out = {}
    for i in range(count):
        tag, lo, default, hi = struct.unpack_from(">4siii", table, offset + size * i)
        out[tag.decode("latin-1")] = tuple(v / 65536 for v in (lo, default, hi))
    return out


def _name(table, ids):
    """The first of `ids` the name table holds, Windows Unicode English or
    Mac Roman, decoded."""
    if not table:
        return None
    count, strings = struct.unpack_from(">HH", table, 2)
    found = {}
    for i in range(count):
        platform, encoding, lang, nid, length, offset = struct.unpack_from(
            ">HHHHHH", table, 6 + 12 * i
        )
        raw = table[strings + offset : strings + offset + length]
        if platform == 3 and encoding in (0, 1) and lang == 0x409:
            found.setdefault(nid, raw.decode("utf-16-be"))
        elif platform == 1 and encoding == 0:
            found.setdefault(nid, raw.decode("mac-roman"))
    return next((found[n] for n in ids if n in found), None)


def _italic(tables):
    if tables.get("OS/2"):
        (selection,) = struct.unpack_from(">H", tables["OS/2"], 62)
        return bool(selection & 1)
    if tables.get("head"):
        (style,) = struct.unpack_from(">H", tables["head"], 44)
        return bool(style & 2)
    return False
