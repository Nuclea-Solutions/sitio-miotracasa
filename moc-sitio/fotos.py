# Optimiza las fotos editadas de MOC: JPEG progresivo y WebP en dos o tres anchos.
# Uso: python3 fotos.py "<carpeta de originales>" assets/fotos [nombre ...]   (necesita Pillow)
import sys, os, io
from PIL import Image, ImageCms
SRC, DST = sys.argv[1], sys.argv[2]
# rol: c = tarjeta (600, 1200) · h = portada (1200, 1800) · hc = ambos
# un cuarto dato opcional recorta el original antes: (izquierda, arriba, derecha, abajo) en px
CAT = [
 ('Master Suite Sayulita/27b184ea-40da-4d4f-a90c-0cd69a2504f4.png','suite-sayulita-recamara','hc'),
 ('Master Suite Sayulita/Persiana romana crema perfectamente alisada.png','suite-sayulita-sala','c'),
 ('Master Suite Sayulita/Cocina boutique cálida y serena.png','suite-sayulita-cocina','c'),
 ('Master Suite Flores/Dormitorio twin con vista al mar.png','suite-flores-recamara','hc'),
 ('Master Suite Flores/Desayuno elegante en terraza tropical.png','suite-flores-desayuno','hc'),
 ('Master Suite Flores/Interior de hotel mexicano con artesanías.png','suite-flores-interior','c'),
 ('Suite Agua/Elegancia cálida en dormitorio boutique.png','suite-agua-recamara','hc'),
 ('Suite Agua/Terraza tropical frente al océano.png','suite-agua-terraza','c'),
 ('Suite Agua/Jacuzzi en terraza bajo cielo pálido.png','suite-agua-jacuzzi','c'),
 ('Suite Palapa/Suite serena bajo techo de palapa.png','suite-palapa-recamara','hc'),
 ('Suite Palapa/Terraza serena con vista al mar.png','suite-palapa-terraza','c'),
 ('Suite Palapa/Dormitorio de lujo con techo de paja.png','suite-palapa-dosel','c'),
 ('ROOFTOP/Terraza tropical con cojines oliva.png','suite-palapa-sala','c'),  # venía en ROOFTOP, es de la suite
 ('Suite Sol/Dormitorio elegante con luz cálida y terracota.png','suite-sol-recamara','hc'),
 ('Suite Sol/dc2dbf66-fd61-47f5-a35c-7180ccbe22ae.png','suite-luna-sala','c'),  # venía en Suite Sol, es la sala de Luna
 ('Jr. Suite Luna/Dormitorio boutique cálido y sereno.png','suite-luna-recamara','hc'),
 ('Jr. Suite Luna/Entrada serena de hotel boutique.png','suite-luna-entrada','c'),
 ('Jr. Suite Arena/Dormitorio twin con edredones blancos y cojines.png','suite-arena-recamara','hc'),
 ('Jr. Suite Arena/Baño boutique sereno en crema y verde.png','suite-arena-bano','c'),
 ('Jr. Suite Arena/Dormitorio cálido con textiles neutros.png','suite-arena-escritorio','c'),
 ('EXTRAS/Patio boutique con arcos y vegetación.png','casa-patio-arcos','c'),
 ('COMEDOR/Comedor tropical con mesa de cristal.png','casa-comedor-palapa','h', (0, 0, 1383, 1086)),  # corta a media columna
 ('ALBERCA/Salón junto a la piscina al atardecer.png','casa-alberca-atardecer','h'),
 ('ROOFTOP/Terraza de lujo frente al mar.png','casa-terraza-mar','h'),
 ('EXTRAS/Balcón de palapa con luz cálida.png','casa-balcon-pueblo','h'),
 ('EXTRAS/Hotel boutique tropical con palapa y balcones.png','casa-fachada','h'),
 ('ALBERCA/Piscina tropical en hotel boutique de lujo.png','casa-alberca','c'),
 ('ALBERCA/Reposeras beige bajo palapa tropical.png','casa-reposeras','c'),
 ('ALBERCA/Refugio tropical junto a la piscina.png','casa-alberca-sala','c'),
 ('ROOFTOP/Interior hotelero cálido bajo techo de palapa.png','casa-bar-palapa','c'),
 ('ROOFTOP/Terraza de lujo al atardecer.png','casa-terraza-atardecer','c'),
 ('EXTRAS/Corredor boutique de piedra y luz cálida.png','casa-corredor','c'),
 ('ROOFTOP/Palapa boutique con luz natural serena.png','casa-palapa-rooftop','h'),
 ('ROOFTOP/Masaje tropical, sin telas ni botellas.png','casa-masaje','hc'),
 ('EXTRAS/Hotel de lujo en hora azul.png','casa-hora-azul','c'),
 ('ROOFTOP/Elegancia serena bajo la palapa.png','casa-sala-palapa','hc'),
 ('ROOFTOP/Terraza de lujo al atardecer.png','portada-atardecer','h'),
 ('ROOFTOP/Terraza de lujo al atardecer.png','portada-atardecer-vertical','c', (563, 0, 1331, 1024)),  # 3:4 sobre palmas y farol
]
ANCHOS = {'c': (600, 1200), 'h': (1200, 1800), 'hc': (600, 1200, 1800)}
SRGB = ImageCms.createProfile('sRGB')
os.makedirs(DST, exist_ok=True)
tot_in = tot_out = 0
solo = sys.argv[3:]  # nombres a procesar; sin ellos, todos
for rel, nombre, rol, *recorte in CAT:
    if solo and nombre not in solo: continue
    ruta = os.path.join(SRC, rel)
    im = Image.open(ruta)
    icc = im.info.get('icc_profile')
    if icc:  # todo a sRGB para que el navegador no adivine
        im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode='RGB')
    im = im.convert('RGB')
    if recorte: im = im.crop(recorte[0])
    W, H = im.size
    tot_in += os.path.getsize(ruta)
    for w in sorted({min(a, W) for a in ANCHOS[rol]}):
        r = im if w == W else im.resize((w, round(H * w / W)), Image.LANCZOS)
        base = os.path.join(DST, f'{nombre}-{w}')
        r.save(base + '.jpg', 'JPEG', quality=75, progressive=True, optimize=True)
        r.save(base + '.webp', 'WEBP', quality=75, method=6)
        tot_out += os.path.getsize(base + '.jpg') + os.path.getsize(base + '.webp')
    print(f'{nombre:28s} {W}x{H} {"icc" if icc else "   "} -> {sorted({min(a, W) for a in ANCHOS[rol]})}')
print(f'PNG {tot_in/1e6:.1f} MB -> JPEG+WebP {tot_out/1e6:.1f} MB')
