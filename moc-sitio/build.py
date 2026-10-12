#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del sitio de Mi Otra Casa.
Escribe el sitio en español en la raíz y en inglés bajo /en/.
    python3 build.py
"""
import os, re, shutil, html

RAIZ = os.path.dirname(os.path.abspath(__file__))   # el sitio vive junto a los generadores
DOMINIO = 'https://miotracasa.mx'
# ruta del sitio en el servidor; el 404 la necesita porque se sirve a cualquier profundidad.
# En GitHub Pages es /sitio-miotracasa/; al conectar miotracasa.mx pasa a ser /
RAIZ_WEB = '/sitio-miotracasa/'

# ---------------------------------------------------------------- datos

# Smart TV: la de Sayulita es de 42"; en Flores, Agua, Sol y Luna falta confirmar la medida.
# fotos: la principal, la que aparece al pasar el cursor y las demás de su página (tres o cuatro)
SUITES = [
 dict(slug='sayulita', tipo='master', nombre='Master Suite Sayulita', precio=420,
      m2=90, huespedes=2,
      fotos=('suite-sayulita-recamara', 'suite-sayulita-sala', 'suite-sayulita-cocina'),
      rasgo=('Vista al pueblo y al mar','Town and ocean view'),
      cama=('Cama king','King bed'),
      orienta=('Segundo piso, da al pueblo','Second floor, faces the town'),
      corta=('En el segundo piso, con la mejor luz de la casa y vista al pueblo y al mar. Da al centro, así que de noche se escucha Sayulita.',
             'On the second floor, with the best light in the house and views of the town and the sea. It faces the centre, so you hear Sayulita at night.'),
      larga=(['Es la suite más alta de la casa y la que mejor resume por qué MOC está donde está: desde la terraza se ve el pueblo por un lado y el mar por el otro.',
              'Adentro, noventa metros cuadrados con cama king, baño amplio y una sala donde cabe el equipaje de un viaje largo sin que estorbe.',
              'Conviene saberlo antes de reservar: es la suite que más mira al centro del pueblo, y en temporada alta la música se escucha hasta la madrugada. Hay tapones y ruido blanco en la habitación.'],
             ['The highest suite in the house, and the one that best explains why MOC sits where it does: from the terrace you see the town on one side and the ocean on the other.',
              'Inside, ninety square metres with a king bed, a generous bathroom and a sitting area where the luggage of a long trip fits without getting in the way.',
              'Worth knowing before you book: it is the suite that looks most directly onto the centre of town, and in high season the music carries into the early hours. Earplugs and a white-noise machine are in the room.']),
      extras=(['Terraza con palapa','Vista al mar','Sala independiente','Smart TV de 42 pulgadas'],
              ['Palapa-covered terrace','Ocean view','Separate sitting area','42-inch smart TV'])),

 dict(slug='flores', tipo='master', nombre='Master Suite Flores', precio=420,
      m2=80, huespedes=4,
      fotos=('suite-flores-recamara', 'suite-flores-desayuno', 'suite-flores-interior'),
      rasgo=('Terraza con vista al océano','Ocean view terrace'),
      cama=('Terraza privada','Private terrace'),
      orienta=('Terraza al mar y a la alberca','Terrace facing the ocean and pool'),
      corta=('El corazón de la casa. Más de 70 m² de interior más una terraza con mesa y camastros que da al mar, la alberca y el jardín.',
             'The heart of the house. Over 70 m² inside plus a terrace with a table and loungers facing the ocean, the pool and the garden.'),
      larga=(['La terraza es lo que la vuelve distinta: mesa para desayunar, camastros para la tarde y una vista que abarca el mar, la alberca y el jardín de la casa.',
              'Adentro caben cuatro adultos sin que nadie duerma de prestado, así que funciona igual para dos parejas que para una familia de adultos.'],
             ['The terrace is what sets it apart: a breakfast table, loungers for the afternoon and a view that takes in the ocean, the pool and the garden.',
              'Inside it sleeps four adults properly, so it works as well for two couples as for a family of grown-ups.']),
      extras=(['Terraza con camastros','Vista a la alberca','Para cuatro adultos','Smart TV'],
              ['Terrace with loungers','Pool view','Sleeps four adults','Smart TV'])),

 dict(slug='agua', tipo='suite', nombre='Suite Agua', precio=360,
      m2=60, huespedes=2,
      fotos=('suite-agua-recamara', 'suite-agua-jacuzzi', 'suite-agua-terraza'),
      rasgo=('Jacuzzi para dos','Jacuzzi for two'),
      cama=('Jacuzzi','Jacuzzi'),
      orienta=('Planta baja, terraza propia','Ground floor, its own terrace'),
      corta=('Planta baja con entrada independiente por una terraza grande y vista parcial al mar. El jacuzzi la vuelve la favorita de las lunas de miel.',
             'Ground floor with its own entrance through a large terrace and a partial ocean view. The jacuzzi makes it the honeymoon favourite.'),
      larga=(['Se entra por su propia terraza, sin pasar por las áreas comunes, lo que la hace la más privada de la casa.',
              'El jacuzzi está en la terraza, con vista parcial al mar. Es la suite que más se reserva para aniversarios y lunas de miel.'],
             ['You enter through its own terrace, without crossing the shared areas, which makes it the most private suite in the house.',
              'The jacuzzi sits on the terrace, with a partial ocean view. It is the suite most often booked for anniversaries and honeymoons.']),
      extras=(['Entrada independiente','Terraza grande','Vista parcial al mar','Smart TV'],
              ['Private entrance','Large terrace','Partial ocean view','Smart TV'])),

 dict(slug='palapa', tipo='suite', nombre='Suite Palapa', precio=360,
      m2=60, huespedes=2,
      fotos=('suite-palapa-recamara', 'suite-palapa-sala', 'suite-palapa-dosel', 'suite-palapa-terraza'),
      rasgo=('Vista al mar bajo techo de palma','Ocean view under a palapa roof'),
      cama=('Techo de palma','Palapa roof'),
      orienta=('Abierta al aire','Open to the air'),
      corta=('Duermes bajo la palma y con el aire del mar; no lleva aire acondicionado y ese es justo el punto. La más fresca entre noviembre y abril.',
             'You sleep under the palm roof with sea air; there is no air conditioning and that is precisely the point. The coolest room from November to April.'),
      larga=(['El techo de palapa y la ventilación cruzada mantienen la suite fresca sin aire acondicionado, que es como se ha dormido en esta costa desde siempre.',
              'Conviene saberlo antes de reservar: de mayo a octubre el calor de Sayulita es húmedo, y esta suite es para quien prefiere el ventilador y el aire del mar. Y como el techo es abierto, también entra el sonido del pueblo: no es la suite para quien tiene el sueño ligero.'],
             ['The palapa roof and the cross ventilation keep the room cool without air conditioning, which is how people have slept on this coast for a long time.',
              'Worth knowing before you book: from May to October Sayulita is humid, and this suite is for guests who prefer a fan and sea air. And because the roof is open, the sound of the town comes in too: this is not the room for a light sleeper.']),
      extras=(['Vista al mar','Ventilación natural','Techo de palapa'],
              ['Ocean view','Natural ventilation','Palapa roof'])),

 dict(slug='sol', tipo='suite', nombre='Suite Sol', precio=360,
      m2=80, huespedes=2,
      fotos=('suite-sol-recamara', 'casa-patio-arcos', 'casa-corredor'),
      rasgo=('Vista al jardín','Garden view'),
      cama=('Planta baja','Ground floor'),
      orienta=('Interior, al jardín','Interior, onto the garden'),
      corta=('Planta baja, interior y al jardín: es de las más resguardadas del ruido del pueblo. Dos ventanales, uno al jardín y otro a un traspatio de plantas.',
             'Ground floor, interior and facing the garden: one of the most sheltered rooms from the noise of the town. Two large windows, one onto the garden and one onto a planted courtyard.'),
      larga=(['Se entra por una salita con dos sofás convertibles, útiles para la siesta de la tarde o para una noche extra.',
              'Tiene dos ventanales: uno da al jardín y el otro a un traspatio lleno de plantas, al que se puede salir desde la suite. El piso de cerámica vidriada y la artesanía son lo que la vuelven distinta.'],
             ['You enter through a small sitting room with two convertible sofas, useful for an afternoon nap or an extra night.',
              'It has two large windows: one onto the garden, the other onto a planted courtyard you can step into from the room. The glazed ceramic floor and the crafts are what set it apart.']),
      extras=(['Sala independiente','Traspatio privado','Planta baja','Smart TV'],
              ['Separate sitting room','Private courtyard','Ground floor','Smart TV'])),

 dict(slug='luna', tipo='jr', nombre='Jr. Suite Luna', precio=240,
      m2=30, huespedes=2,
      fotos=('suite-luna-recamara', 'suite-luna-sala', 'suite-luna-entrada', 'casa-patio-arcos'),
      rasgo=('Vista al jardín, sin escaleras','Garden view, step-free'),
      cama=('Cama queen','Queen bed'),
      orienta=('Interior, al jardín','Interior, onto the garden'),
      corta=('Pequeña y bien resuelta, con cama queen. Interior y al jardín, sin escaleras de por medio: de las más tranquilas de la casa.',
             'Small and well resolved, with a queen bed. Interior and facing the garden, with no stairs along the way: one of the quietest rooms in the house.'),
      larga=(['Treinta metros cuadrados aprovechados al máximo: cama queen, baño completo y vista al jardín.',
              'Está en planta baja y no tiene escaleras de por medio, así que es la más cómoda para quien llega con equipaje pesado o prefiere no subir.'],
             ['Thirty square metres used well: a queen bed, a full bathroom and a garden view.',
              'It sits on the ground floor with no stairs along the way, so it is the easiest room for anyone arriving with heavy luggage.']),
      extras=(['Sin escaleras','Vista al jardín','Cama queen','Smart TV'],
              ['Step-free','Garden view','Queen bed','Smart TV'])),

 dict(slug='arena', tipo='jr', nombre='Jr. Suite Arena', precio=240,
      m2=30, huespedes=2,
      fotos=('suite-arena-recamara', 'suite-arena-escritorio', 'suite-arena-bano', 'casa-patio-arcos'),
      rasgo=('Dos camas individuales','Two single beds'),
      cama=('Dos camas','Two beds'),
      orienta=('Interior, al jardín','Interior, onto the garden'),
      corta=('Pensada para compartir con una amiga o con la familia: dos camas individuales, escritorio y una decoración ecléctica. Interior, al jardín.',
             'Made for sharing with a friend or a relative: two single beds, a desk and an eclectic mix of pieces. Interior, facing the garden.'),
      larga=(['Es la única suite con dos camas individuales, así que resuelve el viaje de dos amigas o de madre e hija adulta.',
              'Tiene escritorio, lo que la hace la mejor opción para quien viene a trabajar unos días desde Sayulita.'],
             ['The only suite with two single beds, which solves a trip for two friends or a mother and her grown daughter.',
              'It has a desk, which makes it the best choice for anyone coming to work from Sayulita for a few days.']),
      extras=(['Dos camas individuales','Escritorio','Vista al jardín'],
              ['Two single beds','Desk','Garden view'])),
]

# ---------------------------------------------------------------- fotos
# Viven en assets/fotos/<nombre>-<ancho>.jpg|webp. Los anchos se leen del disco,
# así que basta con procesar una foto nueva y darla de alta aquí con su texto alternativo.

FOTOS = {
 'suite-sayulita-recamara': ('Recámara de la Master Suite Sayulita con vista al mar','Master Suite Sayulita bedroom with an ocean view'),
 'suite-sayulita-sala':     ('Sala de la Master Suite Sayulita con vista al pueblo','Master Suite Sayulita sitting area looking over the town'),
 'suite-sayulita-cocina':   ('Cocineta de la Master Suite Sayulita','Kitchenette in Master Suite Sayulita'),
 'suite-flores-recamara':   ('Master Suite Flores, dos camas y vista al mar','Master Suite Flores, two beds and an ocean view'),
 'suite-flores-desayuno':   ('Desayuno servido en la Master Suite Flores','Breakfast served in Master Suite Flores'),
 'suite-flores-interior':   ('Interior de la Master Suite Flores con artesanía mexicana','Inside Master Suite Flores, with Mexican crafts'),
 'suite-agua-recamara':     ('Recámara de la Suite Agua','Suite Agua bedroom'),
 'suite-agua-terraza':      ('Terraza de la Suite Agua con vista parcial al mar','Suite Agua terrace with a partial ocean view'),
 'suite-agua-jacuzzi':      ('Jacuzzi en la terraza de la Suite Agua','Jacuzzi on the Suite Agua terrace'),
 'suite-palapa-recamara':   ('Suite Palapa bajo su techo de palma','Suite Palapa under its palm roof'),
 'suite-palapa-terraza':    ('Terraza de la Suite Palapa con vista al mar','Suite Palapa terrace with an ocean view'),
 'suite-palapa-dosel':      ('Cama con mosquitero bajo la palapa','Canopy bed under the palapa'),
 'suite-palapa-sala':       ('Sala en la terraza de la Suite Palapa','Lounge on the Suite Palapa terrace'),
 'suite-sol-recamara':      ('Recámara de la Suite Sol','Suite Sol bedroom'),
 'suite-luna-recamara':     ('Recámara de la Jr. Suite Luna','Jr. Suite Luna bedroom'),
 'suite-luna-entrada':      ('Entrada de la Jr. Suite Luna','Entrance to Jr. Suite Luna'),
 'suite-luna-sala':         ('Sala de la Jr. Suite Luna','Jr. Suite Luna sitting room'),
 'suite-arena-recamara':    ('Jr. Suite Arena, dos camas individuales','Jr. Suite Arena, two single beds'),
 'suite-arena-bano':        ('Baño de la Jr. Suite Arena','Jr. Suite Arena bathroom'),
 'suite-arena-escritorio':  ('Escritorio de la Jr. Suite Arena, junto a la ventana al patio','Jr. Suite Arena desk, by the window onto the courtyard'),
 'casa-patio-arcos':        ('Jardín de la casa, bajo los arcos','The garden of the house, under the arches'),
 'casa-comedor-palapa':     ('Comedor bajo la palapa','Dining table under the palapa'),
 'casa-alberca-atardecer':  ('Sala junto a la alberca al atardecer','Lounge by the pool at dusk'),
 'casa-terraza-mar':        ('Terraza de la azotea con vista al mar','Rooftop terrace with an ocean view'),
 'casa-balcon-pueblo':      ('Vista al pueblo y al mar desde el balcón','View over the town and the sea from the balcony'),
 'casa-fachada':            ('La casa entre palmeras, con su palapa en lo alto','The house among palms, its palapa on top'),
 'casa-alberca':            ('Alberca entre plantas tropicales','Pool among tropical plants'),
 'casa-reposeras':          ('Camastros bajo una palapa junto a la alberca','Loungers under a palapa by the pool'),
 'casa-alberca-sala':       ('Sala al aire libre frente a la alberca','Open-air lounge facing the pool'),
 'casa-bar-palapa':         ('Barra bajo la palapa de la azotea','Bar under the rooftop palapa'),
 'casa-terraza-atardecer':  ('Atardecer sobre Sayulita desde la terraza','Sunset over Sayulita from the terrace'),
 'casa-corredor':           ('Corredor de piedra hacia el jardín','Stone walkway to the garden'),
 'casa-palapa-rooftop':     ('Sala bajo la palapa de la azotea','Lounge under the rooftop palapa'),
 'casa-masaje':             ('Masaje en la terraza','Massage on the terrace'),
 'casa-hora-azul':          ('La casa en la hora azul','The house at blue hour'),
 'casa-sala-palapa':        ('Sala bajo la palapa de la azotea, con uvas sobre la mesa','Lounge under the rooftop palapa, with grapes on the table'),
 'portada-atardecer':       ('Atardecer sobre Sayulita y el mar desde la terraza de la casa','Sunset over Sayulita and the sea from the terrace of the house'),
}

# encuadre de las verticales cuando la retícula las recorta a 3:2 o cuadrado
FOCO = {
 'suite-agua-jacuzzi': '50% 80%',
 'casa-reposeras':     '50% 75%',
 'casa-bar-palapa':    '50% 75%',
}

# sizes según la retícula de site.css (cortes en 640, 1000 y 1100 px)
TAM = {
 'portada':  '100vw',
 'bloque':   '(max-width: 1000px) 100vw, 60vw',
 'tarjeta':  '(max-width: 640px) 100vw, (max-width: 1100px) 50vw, 33vw',
 'otras':    '(max-width: 640px) 100vw, (max-width: 1000px) 50vw, 33vw',
 'suite1':   '(max-width: 1000px) 100vw, 62vw',
 'suite2':   '(max-width: 1000px) 100vw, 38vw',
 'gal':      '(max-width: 640px) 100vw, (max-width: 1000px) 50vw, 25vw',
 'gal2':     '(max-width: 640px) 100vw, 50vw',
 'ubica':    '(max-width: 1000px) 100vw, 58vw',
 'carrusel': '(max-width: 640px) 100vw, 62vw',
}

DIR_FOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fotos')
_anchos = {}

def anchos(nombre):
    """Anchos disponibles de una foto, de menor a mayor, leídos de assets/fotos."""
    if nombre not in _anchos:
        _anchos[nombre] = sorted(int(m.group(1)) for f in os.listdir(DIR_FOTOS)
                                 if (m := re.fullmatch(re.escape(nombre) + r'-(\d+)\.jpg', f)))
        assert _anchos[nombre], f'falta la foto {nombre} en assets/fotos'
    return _anchos[nombre]

def alto(nombre, w):
    """Alto de la versión de ancho w, leído de la cabecera JPEG."""
    with open(os.path.join(DIR_FOTOS, f'{nombre}-{w}.jpg'), 'rb') as f:
        d = f.read()
    j = 2
    while j < len(d):
        marca, largo = d[j+1], int.from_bytes(d[j+2:j+4], 'big')
        if marca in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(d[j+5:j+7], 'big')
        j += 2 + largo
    raise ValueError(nombre)

def foto_url(a, nombre, w=None):
    """Ruta a una versión JPEG; sin ancho, la más grande."""
    return f'{a}fotos/{nombre}-{w or anchos(nombre)[-1]}.jpg'

def foto(a, nombre, lang, tam, clase='', alt=None, perezosa=True, extra='', vertical=None):
    """<picture> con WebP y JPEG en todos los anchos que existan.
    a: prefijo hasta assets/ · alt=None usa el texto del catálogo · alt='' la marca decorativa.
    vertical: otro recorte de la misma foto para pantallas en vertical (teléfono, tableta parada)."""
    ws = anchos(nombre)
    w0 = ws[-1] if len(ws) == 1 else ws[-2]
    texto = FOTOS[nombre]['en' == lang] if alt is None else alt
    srcset = lambda ext, n=nombre: ', '.join(f'{a}fotos/{n}-{w}.{ext} {w}w' for w in anchos(n))
    attrs = f' class="{clase}"' if clase else ''
    attrs += f' alt="{texto}"' + ('' if texto else ' aria-hidden="true"')
    attrs += ' loading="lazy"' if perezosa else ''
    attrs += f' style="object-position:{FOCO[nombre]}"' if nombre in FOCO else ''
    vert = ''.join(f'<source media="(orientation: portrait)"{t} srcset="{srcset(ext, vertical)}" sizes="{TAM[tam]}">'
                   for ext, t in (('webp', ' type="image/webp"'), ('jpg', ''))) if vertical else ''
    return (f'<picture>{vert}<source type="image/webp" srcset="{srcset("webp")}" sizes="{TAM[tam]}">'
            f'<img src="{a}fotos/{nombre}-{w0}.jpg" srcset="{srcset("jpg")}" sizes="{TAM[tam]}" '
            f'width="{ws[-1]}" height="{alto(nombre, ws[-1])}"{attrs} decoding="async"{extra}></picture>')

INCLUYE = (
 ['Desayuno diario para dos','WiFi sin costo','Aire acondicionado','Frigobar','Agua embotellada sin costo',
  'Sábanas de algodón egipcio','Edredón de pluma','Regadera tipo lluvia','Caja fuerte','Mosquitero',
  'Cafetera y té','Amenidades de baño','Secadora (bajo petición)','Limpieza diaria'],
 ['Daily breakfast for two','Free WiFi','Air conditioning','Mini fridge','Free bottled water',
  'Egyptian cotton sheets','Down comforter','Rainfall shower','Safe box','Mosquito net',
  'Coffee and tea','Bath amenities','Hair dryer (on request)','Daily housekeeping'])

T = {
 'es': dict(
   lang='es', otro='en', otro_nombre='English', pre='', raiz='index.html',
   menu='Menú', cerrar_menu='Cerrar menú', reservar='Reservar', saltar='Saltar al contenido',
   nav_suites='Suites', nav_casa='La casa', nav_sayulita='Sayulita',
   nav_completa='Casa completa', nav_servicios='Servicios', nav_contacto='Contacto',
   nav_politicas='Políticas', nav_privacidad='Aviso de privacidad',
   destacado_ch='Reservas', destacado_t='Consultar disponibilidad',
   pie_casa='La casa', pie_reservas='Reservas', pie_social='Síguenos',
   pie_sobre='Sobre MOC', pie_servicios='Servicios', pie_legal='© 2026 Mi Otra Casa, Sayulita',
   pie_precios='Precios en dólares, por noche, sujetos a temporada',
   pie_dir='Marlin 18, Sayulita, Nayarit. A media cuadra de la plaza, a tres del mar.',
   ver='Ver la suite', noche='USD por noche', desde='Desde',
   solo_adultos='Solo adultos', incluye='Lo que incluye', volver='Ver todas las suites',
 ),
 'en': dict(
   lang='en', otro='es', otro_nombre='Español', pre='../', raiz='../index.html',
   menu='Menu', cerrar_menu='Close menu', reservar='Book', saltar='Skip to content',
   nav_suites='Suites', nav_casa='The house', nav_sayulita='Sayulita',
   nav_completa='Whole house', nav_servicios='Services', nav_contacto='Contact',
   nav_politicas='Policies', nav_privacidad='Privacy notice',
   destacado_ch='Reservations', destacado_t='Check availability',
   pie_casa='The house', pie_reservas='Reservations', pie_social='Follow us',
   pie_sobre='About MOC', pie_servicios='Services', pie_legal='© 2026 Mi Otra Casa, Sayulita',
   pie_precios='Rates in USD per night, subject to season',
   pie_dir='Marlin 18, Sayulita, Nayarit. Half a block from the plaza, three from the sand.',
   ver='View suite', noche='USD per night', desde='From',
   solo_adultos='Adults only', incluye='What is included', volver='See all suites',
 ),
}

RUTAS = {
 'es': dict(index='index.html', suites='suites.html', casa='casa.html', reservar='reservar.html',
            contacto='contacto.html', politicas='politicas.html', privacidad='privacidad.html',
            suite=lambda s: f'suites/{s}.html'),
 'en': dict(index='index.html', suites='suites.html', casa='house.html', reservar='booking.html',
            contacto='contact.html', politicas='policies.html', privacidad='privacy.html',
            suite=lambda s: f'suites/{s}.html'),
}

def base(lang, prof=0):
    """prefijo para llegar a la raíz del idioma desde una página a 'prof' niveles."""
    return '../' * prof

def url(lang, clave, prof=0, slug=None):
    r = RUTAS[lang]
    destino = r['suite'](slug) if clave == 'suite' else r[clave]
    return base(lang, prof) + destino

def alterno(lang, clave, prof=0, slug=None):
    """misma página en el otro idioma"""
    otro = T[lang]['otro']
    destino = RUTAS[otro]['suite'](slug) if clave == 'suite' else RUTAS[otro][clave]
    salto = base(lang, prof) + ('../' if lang == 'en' else 'en/')
    return salto + destino

# ---------------------------------------------------------------- plantillas

def cabeza(lang, titulo, desc, clave, prof=0, slug=None, extra=''):
    t = T[lang]; a = base(lang, prof) + ('../assets/' if lang == 'en' else 'assets/')
    canon = f"{DOMINIO}/{'en/' if lang=='en' else ''}" + (RUTAS[lang]['suite'](slug) if clave=='suite' else RUTAS[lang][clave])
    canon = canon.replace('/index.html', '/')
    otro_url = f"{DOMINIO}/{'' if lang=='en' else 'en/'}" + (RUTAS[t['otro']]['suite'](slug) if clave=='suite' else RUTAS[t['otro']][clave])
    otro_url = otro_url.replace('/index.html', '/')
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#FDFDFD">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="{lang}" href="{canon}">
<link rel="alternate" hreflang="{t['otro']}" href="{otro_url}">
<link rel="alternate" hreflang="x-default" href="{canon if lang=='es' else otro_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mi Otra Casa">
<meta property="og:locale" content="{'es_MX' if lang=='es' else 'en_US'}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMINIO}/assets/compartir.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{a}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a}site.css">
<script src="{a}site.js" defer></script>
{extra}</head>
<body>

<a class="salto" href="#contenido">{t['saltar']}</a>
'''

# Por ahora el botón Reservar de la barra lleva a la lista de suites. Cuando el formulario de
# reservar.html tenga destino (Formspree o motor de reservas), volver a ('reservar', '').
BOTON_RESERVAR = ('suites', '#filtros')

def barra(lang, clave, prof=0, slug=None):
    t = T[lang]; a = base(lang, prof) + ('../assets/' if lang == 'en' else 'assets/')
    def act(c): return ' aria-current="page"' if c == clave else ''
    destino = url(lang, BOTON_RESERVAR[0], prof) + BOTON_RESERVAR[1]
    return f'''
<header class="barra">
  <button class="menu-btn" id="abrir" aria-expanded="false" aria-controls="cortina">
    <span class="hamb" aria-hidden="true"><i></i><i></i><i></i></span><span>{t['menu']}</span>
  </button>
  <a class="logo" href="{url(lang,'index',prof)}" aria-label="Mi Otra Casa">
    <img src="{a}logo-mi-otra-casa.png" width="900" height="125" alt="Mi Otra Casa">
  </a>
  <a class="reservar" href="{destino}">{t['reservar']}</a>
</header>
{'' if clave == BOTON_RESERVAR[0] == 'reservar' else f'<a class="reservar-movil" href="{destino}">{t["reservar"]}</a>'}

<div class="cortina" id="cortina" aria-hidden="true">
  <div class="velo"></div>
  <div class="panel">
    <button class="cerrar" id="cerrar" aria-label="{t['cerrar_menu']}">&#10005;</button>
    <a class="destacado" href="{url(lang,'reservar',prof)}">
      <span><small>{t['destacado_ch']}</small><b>{t['destacado_t']}</b></span>
      <i aria-hidden="true">&rsaquo;</i>
    </a>
    <nav aria-label="{t['menu']}">
      <a href="{url(lang,'suites',prof)}"{act('suites')}>{t['nav_suites']} <i aria-hidden="true">&rsaquo;</i></a>
      <a href="{url(lang,'casa',prof)}"{act('casa')}>{t['nav_casa']}</a>
      <a href="{url(lang,'index',prof)}#experiencias">{t['nav_sayulita']}</a>
      <a href="{url(lang,'index',prof)}#casa-completa">{t['nav_completa']}</a>
      <a href="{url(lang,'casa',prof)}#servicios">{t['nav_servicios']}</a>
    </nav>
    <div class="secundario">
      <a href="{url(lang,'contacto',prof)}"{act('contacto')}>{t['nav_contacto']}</a>
      <a href="{url(lang,'politicas',prof)}"{act('politicas')}>{t['nav_politicas']}</a>
      <a href="https://www.instagram.com/miotracasa/" rel="noopener">Instagram</a>
    </div>
    <p class="idiomas">
      <a href="#" aria-current="true">{'ES' if lang=='es' else 'EN'}</a>
      <span aria-hidden="true">·</span>
      <a href="{alterno(lang, clave, prof, slug)}" hreflang="{t['otro']}">{'EN' if lang=='es' else 'ES'}</a>
    </p>
    <p class="datos">Marlin 18, Sayulita, Nayarit<br><a href="mailto:contact@miotracasa.mx">contact@miotracasa.mx</a></p>
  </div>
</div>
'''

def pie(lang, prof=0):
    t = T[lang]; a = base(lang, prof) + ('../assets/' if lang == 'en' else 'assets/')
    return f'''
<footer class="pie-sitio">
  <div class="pie">
    <div class="pie-marca">
      <img src="{a}logo-lockup.png" width="780" height="244" alt="Mi Otra Casa, hotel boutique, Sayulita" loading="lazy">
      <p>{t['pie_dir']}</p>
    </div>
    <nav aria-labelledby="pie-casa">
      <h2 id="pie-casa">{t['pie_casa']}</h2>
      <ul>
        <li><a href="{url(lang,'casa',prof)}">{t['pie_sobre']}</a></li>
        <li><a href="{url(lang,'suites',prof)}">{t['nav_suites']}</a></li>
        <li><a href="{url(lang,'casa',prof)}#servicios">{t['pie_servicios']}</a></li>
      </ul>
    </nav>
    <nav aria-labelledby="pie-reservas">
      <h2 id="pie-reservas">{t['pie_reservas']}</h2>
      <ul>
        <li><a href="{url(lang,'reservar',prof)}">{t['destacado_t']}</a></li>
        <li><a href="{url(lang,'politicas',prof)}">{t['nav_politicas']}</a></li>
        <li><a href="{url(lang,'privacidad',prof)}">{t['nav_privacidad']}</a></li>
      </ul>
    </nav>
    <nav aria-labelledby="pie-social">
      <h2 id="pie-social">{t['pie_social']}</h2>
      <ul>
        <li><a href="https://www.instagram.com/miotracasa/" rel="noopener">Instagram</a></li>
        <li><a href="https://www.facebook.com/MOCSayulita" rel="noopener">Facebook</a></li>
        <li><a href="mailto:contact@miotracasa.mx">contact@miotracasa.mx</a></li>
      </ul>
    </nav>
  </div>
  <div class="legal">
    <span>{t['pie_legal']}</span>
    <span>{t['pie_precios']}</span>
  </div>
</footer>

</body>
</html>
'''

def escribir(ruta, contenido):
    destino = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    open(destino, 'w', encoding='utf-8').write(contenido)
    return ruta
