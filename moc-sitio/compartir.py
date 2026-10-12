#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imágenes para compartir (1200x630) e íconos del sitio. Necesita Pillow.
    python3 compartir.py <ruta a Marcellus-Regular.ttf>
Las fotos salen de assets/fotos, así que primero va fotos.py.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from build import SUITES

AQUI = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(AQUI, 'assets')
FUENTE = sys.argv[1]
MARFIL, TINTA = (253, 253, 253), (28, 28, 26)
W, H = 1200, 630

def mayor(nombre):
    """La versión más grande de una foto procesada."""
    ws = sorted(int(f[len(nombre) + 1:-4]) for f in os.listdir(os.path.join(A, 'fotos'))
                if f.startswith(nombre + '-') and f.endswith('.jpg') and f[len(nombre) + 1:-4].isdigit())
    return Image.open(os.path.join(A, 'fotos', f'{nombre}-{ws[-1]}.jpg')).convert('RGB')

def encuadre(im, alto=0.5):
    """Recorta a 1200x630; alto = dónde cae el centro vertical (0 arriba, 1 abajo)."""
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = min(max(round(im.height * alto - H / 2), 0), im.height - H)
    return im.crop((x, y, x + W, y + H))

def velo(im, arriba=0.15, abajo=0.7):
    """Degradado tinta de arriba a abajo para que el texto blanco se lea."""
    capa = Image.new('L', (1, H))
    for y in range(H):
        t = y / (H - 1)
        capa.putpixel((0, y), round(255 * (arriba + (abajo - arriba) * t ** 1.6)))
    capa = capa.resize((W, H))
    return Image.composite(Image.new('RGB', (W, H), TINTA), im, capa)

def blanco(png, ancho):
    """Un logo con transparencia, en blanco y al ancho pedido."""
    lg = Image.open(os.path.join(A, png)).convert('RGBA')
    lg = lg.resize((ancho, round(lg.height * ancho / lg.width)), Image.LANCZOS)
    b = Image.new('RGBA', lg.size, MARFIL + (0,))
    b.putalpha(lg.split()[3])
    return b

def espaciado(d, xy, texto, fuente, tracking, color):
    x, y = xy
    for c in texto:
        d.text((x, y), c, font=fuente, fill=color)
        x += d.textlength(c, font=fuente) + tracking
    return x

os.makedirs(os.path.join(A, 'compartir'), exist_ok=True)

# portada y páginas generales: el atardecer con el logotipo completo al centro
im = velo(encuadre(mayor('portada-atardecer'), 0.5), 0.45, 0.6)
lg = blanco('logo-lockup.png', 520)
im.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2), lg)
im.save(os.path.join(A, 'compartir', 'inicio.jpg'), quality=86, optimize=True, progressive=True)

# una por suite: su foto principal, su nombre y la marca
nombre_f = ImageFont.truetype(FUENTE, 66)
rot_f = ImageFont.truetype(FUENTE, 17)
for s in SUITES:
    im = velo(encuadre(mayor(s['fotos'][0]), 0.55), 0.05, 0.72)
    d = ImageDraw.Draw(im)
    espaciado(d, (72, H - 172), 'MI OTRA CASA  ·  SAYULITA', rot_f, 5, MARFIL)
    d.text((70, H - 140), s['nombre'], font=nombre_f, fill=MARFIL)
    im.save(os.path.join(A, 'compartir', f"{s['slug']}.jpg"), quality=86, optimize=True, progressive=True)

# íconos: monograma sobre marfil; en los chicos llena casi todo el ancho para que se lea
mono = Image.open(os.path.join(A, 'monograma-moc.png')).convert('RGBA')
def icono(lado, llenado):
    base = Image.new('RGBA', (lado * 4, lado * 4), MARFIL + (255,))
    w = round(lado * 4 * llenado)
    m = mono.resize((w, round(mono.height * w / mono.width)), Image.LANCZOS)
    base.paste(m, ((base.width - m.width) // 2, (base.height - m.height) // 2), m)
    return base.resize((lado, lado), Image.LANCZOS).convert('RGB')

icono(32, .9).save(os.path.join(A, 'favicon-32.png'), optimize=True)
icono(180, .66).save(os.path.join(A, 'apple-touch-icon.png'), optimize=True)
icono(192, .62).save(os.path.join(A, 'icono-192.png'), optimize=True)
icono(512, .62).save(os.path.join(A, 'icono-512.png'), optimize=True)
icono(48, .9).save(os.path.join(A, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
print('listo:', sorted(os.listdir(os.path.join(A, 'compartir'))))
