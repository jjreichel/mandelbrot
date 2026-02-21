#!/usr/bin/env python3
"""Mandelbrot Explorer – App-Icon Generator (pure stdlib)"""
import struct, zlib, math, os

SIZE     = 512
MAX_ITER = 256
CX       = -0.75
CY       =  0.0
SCALE    =  1.35
RADIUS   = int(SIZE * 0.175)
BG       = (0x1a, 0x1a, 0x2e, 255)

def mandelbrot(cx, cy):
    zx = zy = 0.0
    for i in range(MAX_ITER):
        zx2, zy2 = zx*zx, zy*zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) * 0.5
            nu     = math.log(log_zn / math.log(2)) / math.log(2)
            return (i + 1 - nu) / MAX_ITER
        zy = 2*zx*zy + cy
        zx = zx2 - zy2 + cx
    return -1.0

def hsv2rgb(h, s, v):
    h = h % 1.0
    i = int(h * 6)
    f = h * 6 - i
    p, q, t = v*(1-s), v*(1-f*s), v*(1-(1-f)*s)
    r, g, b = [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)][i % 6]
    return int(r*255), int(g*255), int(b*255)

def colorize(t):
    return hsv2rgb((t * 3.0 + 0.6) % 1.0, 0.85, math.sqrt(t))

def in_rounded_rect(px, py):
    cx2, cy2 = SIZE / 2.0, SIZE / 2.0
    dx = max(abs(px - cx2) - (cx2 - RADIUS), 0)
    dy = max(abs(py - cy2) - (cy2 - RADIUS), 0)
    return dx*dx + dy*dy <= RADIUS*RADIUS

def write_png(path, rows):
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', SIZE, SIZE, 8, 6, 0, 0, 0)
    raw  = bytearray()
    for row in rows:
        raw.append(0)
        raw.extend(row)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', zlib.compress(bytes(raw), 6)))
        f.write(chunk(b'IEND', b''))

def main():
    print(f'Rendere {SIZE}x{SIZE} Mandelbrot-Icon ...')
    rows = []
    for py in range(SIZE):
        row = bytearray()
        cy_val = CY - (py / SIZE - 0.5) * 2.0 * SCALE
        for px in range(SIZE):
            cx_val = CX + (px / SIZE - 0.5) * 2.0 * SCALE
            if not in_rounded_rect(px + 0.5, py + 0.5):
                row.extend([0, 0, 0, 0])
                continue
            t = mandelbrot(cx_val, cy_val)
            if t < 0:
                row.extend(BG)
            else:
                r, g, b = colorize(t)
                row.extend([r, g, b, 255])
        rows.append(row)
        if py % 64 == 0:
            print(f'  {py}/{SIZE}')
    write_png('icon_base.png', rows)
    print('icon_base.png geschrieben')

if __name__ == '__main__':
    main()
