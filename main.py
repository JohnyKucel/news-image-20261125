"""Entri make.fun news-image-20261125: halaman depan koran broadsheet.

"Wednesday 25 November 2026 \u2014 35 dated stories, 8 regions: Huang is
back at Nvidia and says sorry, Asia sinks, Shenzhou-24 carries the first
Pakistani to Tiangong, Bitcoin back below $60,000".

Konsep: satu hari, satu halaman, satu gambar. Grid 6 kolom, hairline
1px, radius 0, newsprint #F1ECE0 + tinta #111111 + SATU warna spot
merah (kicker, stempel BACK IN 11 DAYS, band CRYPTO NEWS) + panel navy
gelap sebagai lapisan kedua. Masthead serif display THE WORLD + ears +
double rule. Lead Nvidia headline satu baris, deck satu baris, body 2
baris; hero-nya panel before/after selebar halaman penuh (Senin 12 Nov
"he quits": kursi CEO kosong di kantor gelap, vs Senin 23 Nov "he
returns" + Selasa 24 Nov "he apologises": figur dewasa gaya modern
flat 2D \u2014 kepala kecil relatif badan, bahu lebar, jas formal \u2014
berdiri di balik meja + panah saham naik +31.5%) + stempel merah di
jahitan panel. Setiap cerita membawa tanggalnya (Minggu\u2013Rabu 22\u201325
Nov 2026): 1 feature + 12 berita kecil berilustrasi + 5 sel CRYPTO
NEWS + 17 brief = 35 cerita bertanggal, 8 region, peta + legenda,
tabel timeline UTC, DATE CHECK.

Semua angka dari riset 25 Nov 2026 (snapshot 07:20 UTC: BTC $59,100,
ETH $1,660, SOL $68,70; Fear & Greed 13). Semua gambar kartun orisinal
hasil code (bentuk vektor bersih, warna solid, detail minimal).
Tanpa nomor cerita, tanpa sebut testnet.

File ini stdlib-only (os, struct, zlib) dan hanya merakit aset yang
sudah di-render sebelumnya di assets/ menjadi satu PNG deterministik
1024x1024. Urutan lapisan: kertas, grain, ilustrasi, garis pemisah,
lalu teks. Tidak ada timestamp dan tidak ada random, jadi setiap run
menghasilkan byte yang sama persis.
"""

import os
import struct
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"
WIDTH = 1024
HEIGHT = 1024
BG = (241, 236, 224)
INK = (17, 17, 17)
DIVIDER = (180, 170, 145)


def _paeth(left, up, up_left):
    p = left + up - up_left
    pa = abs(p - left)
    pb = abs(p - up)
    pc = abs(p - up_left)
    if pa <= pb and pa <= pc:
        return left
    if pb <= pc:
        return up
    return up_left


def _unfilter(raw, width, height, bpp):
    stride = width * bpp
    out = bytearray(height * stride)
    prev = bytearray(stride)
    pos = 0
    for y in range(height):
        f = raw[pos]
        pos += 1
        row = raw[pos:pos + stride]
        pos += stride
        cur = bytearray(stride)
        if f == 0:
            cur[:] = row
        elif f == 1:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + left) & 0xFF
        elif f == 2:
            for i in range(stride):
                cur[i] = (row[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + (left + prev[i]) // 2) & 0xFF
        elif f == 4:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                up_left = prev[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + _paeth(left, prev[i], up_left)) & 0xFF
        else:
            raise ValueError("filter tidak dikenal: %d" % f)
        out[y * stride:(y + 1) * stride] = cur
        prev = cur
    return bytes(out)


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != SIGNATURE:
        raise ValueError("bukan PNG: %s" % path)
    offset = 8
    width = height = None
    bit_depth = None
    color_type = None
    idat = []
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        name = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if name == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB", payload[:10])
            interlace = payload[12]
            if bit_depth != 8:
                raise ValueError("bit depth harus 8: %s" % path)
            if interlace != 0:
                raise ValueError("interlace harus 0: %s" % path)
            if color_type not in (0, 2, 6):
                raise ValueError("color type tidak didukung: %d" % color_type)
        elif name == b"IDAT":
            idat.append(payload)
        elif name == b"IEND":
            break
    if width is None:
        raise ValueError("IHDR tidak ditemukan: %s" % path)
    if color_type == 0:
        bpp = 1
    elif color_type == 2:
        bpp = 3
    else:
        bpp = 4
    raw = zlib.decompress(b"".join(idat))
    plain = _unfilter(raw, width, height, bpp)
    if color_type == 0:
        pixels = bytearray(width * height * 3)
        for i, v in enumerate(plain):
            pixels[i * 3] = v
            pixels[i * 3 + 1] = v
            pixels[i * 3 + 2] = v
        return width, height, bytes(pixels), False
    if color_type == 2:
        return width, height, plain, False
    return width, height, plain, True


def _chunk(name, payload):
    out = struct.pack(">I", len(payload))
    out += name
    out += payload
    out += struct.pack(">I", zlib.crc32(name + payload) & 0xFFFFFFFF)
    return out


def write_png(path, width, height, rgb):
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    stride = width * 3
    raw0 = bytearray()
    raw2 = bytearray()
    for y in range(height):
        row = rgb[y * stride:(y + 1) * stride]
        raw0.append(0)
        raw0 += row
        raw2.append(2)
        if y == 0:
            raw2 += row
        else:
            prev = rgb[(y - 1) * stride:y * stride]
            raw2 += bytes((row[i] - prev[i]) & 0xFF for i in range(stride))
    comp0 = zlib.compress(bytes(raw0), 9)
    comp2 = zlib.compress(bytes(raw2), 9)
    if len(comp2) < len(comp0):
        idat = comp2
    else:
        idat = comp0
    with open(path, "wb") as fh:
        fh.write(SIGNATURE)
        fh.write(_chunk(b"IHDR", ihdr))
        fh.write(_chunk(b"IDAT", idat))
        fh.write(_chunk(b"IEND", b""))


def paste(canvas, sw, sh, pixels, has_alpha, dx, dy):
    if has_alpha:
        step = 4
    else:
        step = 3
    for sy in range(sh):
        ty = dy + sy
        if ty < 0 or ty >= HEIGHT:
            continue
        for sx in range(sw):
            tx = dx + sx
            if tx < 0 or tx >= WIDTH:
                continue
            so = (sy * sw + sx) * step
            do = (ty * WIDTH + tx) * 3
            if has_alpha:
                a = pixels[so + 3]
                if a == 0:
                    continue
                if a == 255:
                    canvas[do] = pixels[so]
                    canvas[do + 1] = pixels[so + 1]
                    canvas[do + 2] = pixels[so + 2]
                else:
                    inv = 255 - a
                    canvas[do] = (pixels[so] * a + canvas[do] * inv + 127) // 255
                    canvas[do + 1] = (pixels[so + 1] * a + canvas[do + 1] * inv + 127) // 255
                    canvas[do + 2] = (pixels[so + 2] * a + canvas[do + 2] * inv + 127) // 255
            else:
                canvas[do] = pixels[so]
                canvas[do + 1] = pixels[so + 1]
                canvas[do + 2] = pixels[so + 2]


def hbar(canvas, y, thickness):
    top = y - (thickness - 1) // 2
    r, g, b = DIVIDER
    for yy in range(top, top + thickness):
        if yy < 0 or yy >= HEIGHT:
            continue
        base = yy * WIDTH * 3
        for x in range(24, 1000 + 1):
            o = base + x * 3
            canvas[o] = r
            canvas[o + 1] = g
            canvas[o + 2] = b


def vbar(canvas, x, y0, y1):
    r, g, b = DIVIDER
    for yy in range(y0, y1 + 1):
        if yy < 0 or yy >= HEIGHT:
            continue
        o = (yy * WIDTH + x) * 3
        canvas[o] = r
        canvas[o + 1] = g
        canvas[o + 2] = b


# Koordinat layout (1024x1024). Kolom kecil: 6 x 160px, step 164 dari x=24.
COL_X = [24, 188, 352, 516, 680, 844]

TEXT = [
    ("t_topband.png", 24, 8),
    ("t_masthead.png", 24, 30),
    ("t_ticker.png", 24, 124),
    ("t_stats.png", 24, 148),
    ("t_regions.png", 24, 188),
    ("t_feat0.png", 24, 208),
    ("t_crypto.png", 24, 722),
    ("t_map.png", 24, 790),
    ("t_timeline.png", 24, 924),
    ("t_briefs.png", 374, 790),
    ("t_datecheck.png", 804, 790),
    ("t_footband.png", 0, 1000),
]
for _i in range(6):
    TEXT.append(("t_small%d.png" % _i, COL_X[_i], 486))
for _i in range(6, 12):
    TEXT.append(("t_small%d.png" % _i, COL_X[_i - 6], 604))

ART = [("illo_hero.png", 24, 316)]
for _i in range(6):
    ART.append(("illo_s%d.png" % _i, COL_X[_i] + 3, 556))
for _i in range(6, 12):
    ART.append(("illo_s%d.png" % _i, COL_X[_i - 6] + 3, 674))

BARS_H = [121, 144, 186, 480, 598, 716, 784]

BARS_V = []
for _x in (184, 348, 512, 676, 840):
    BARS_V.append((_x, 482, 592))
    BARS_V.append((_x, 600, 710))
BARS_V.append((366, 790, 996))
BARS_V.append((796, 790, 996))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "assets")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)

    canvas = bytearray(WIDTH * HEIGHT * 3)
    r, g, b = BG
    for i in range(0, len(canvas), 3):
        canvas[i] = r
        canvas[i + 1] = g
        canvas[i + 2] = b

    gw, gh, grain, galpha = read_png(os.path.join(assets, "grain_256.png"))
    for gy in range(0, HEIGHT, gh):
        for gx in range(0, WIDTH, gw):
            paste(canvas, gw, gh, grain, galpha, gx, gy)

    for name, x, y in ART:
        w, h, pixels, alpha = read_png(os.path.join(assets, name))
        paste(canvas, w, h, pixels, alpha, x, y)

    for y in BARS_H:
        hbar(canvas, y, 1)

    for x, y0, y1 in BARS_V:
        vbar(canvas, x, y0, y1)

    for name, x, y in TEXT:
        w, h, pixels, alpha = read_png(os.path.join(assets, name))
        paste(canvas, w, h, pixels, alpha, x, y)

    out_path = os.path.join(out_dir, "entry.png")
    write_png(out_path, WIDTH, HEIGHT, bytes(canvas))
    print(out_path)


if __name__ == "__main__":
    main()
