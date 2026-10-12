#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del sitio de Mi Otra Casa.
Escribe el sitio en español en la raíz y en inglés bajo /en/.
    python3 build.py
"""
import os, shutil, html

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
DOMINIO = 'https://miotracasa.mx'
IMG = 'https://miotracasa.mx/images'          # fotos que todavía viven en el sitio actual

# ---------------------------------------------------------------- datos

SUITES = [
 dict(slug='sayulita', tipo='master', nombre='Master Suite Sayulita', precio=420,
      m2=90, huespedes=2, foto='06_sayulita',
      rasgo=('Vista al pueblo y al mar','Town and ocean view'),
      cama=('Cama king','King bed'),
      corta=('En el segundo piso, con la mejor luz de la casa: por la mañana entra limpia desde el oriente y por la noche se ven las luces del pueblo.',
             'On the second floor, with the best light in the house: clean morning sun from the east and the town lights at night.'),
      larga=(['Es la suite más alta de la casa y la que mejor resume por qué MOC está donde está: desde la terraza se ve el pueblo por un lado y el mar por el otro.',
              'Adentro, noventa metros cuadrados con cama king, baño amplio y una sala donde cabe el equipaje de un viaje largo sin que estorbe.'],
             ['The highest suite in the house, and the one that best explains why MOC sits where it does: from the terrace you see the town on one side and the ocean on the other.',
              'Inside, ninety square metres with a king bed, a generous bathroom and a sitting area where the luggage of a long trip fits without getting in the way.']),
      extras=(['Terraza con palapa','Vista al mar','Sala independiente'],
              ['Palapa-covered terrace','Ocean view','Separate sitting area'])),

 dict(slug='flores', tipo='master', nombre='Master Suite Flores', precio=420,
      m2=80, huespedes=4, foto='05_flores',
      rasgo=('Terraza con vista al océano','Ocean view terrace'),
      cama=('Terraza privada','Private terrace'),
      corta=('El corazón de la casa. Más de 70 m² de interior más una terraza con mesa y camastros que da al mar, la alberca y el jardín.',
             'The heart of the house. Over 70 m² inside plus a terrace with a table and loungers facing the ocean, the pool and the garden.'),
      larga=(['La terraza es lo que la vuelve distinta: mesa para desayunar, camastros para la tarde y una vista que abarca el mar, la alberca y el jardín de la casa.',
              'Adentro caben cuatro adultos sin que nadie duerma de prestado, así que funciona igual para dos parejas que para una familia de adultos.'],
             ['The terrace is what sets it apart: a breakfast table, loungers for the afternoon and a view that takes in the ocean, the pool and the garden.',
              'Inside it sleeps four adults properly, so it works as well for two couples as for a family of grown-ups.']),
      extras=(['Terraza con camastros','Vista a la alberca','Para cuatro adultos'],
              ['Terrace with loungers','Pool view','Sleeps four adults'])),

 dict(slug='agua', tipo='suite', nombre='Suite Agua', precio=360,
      m2=60, huespedes=2, foto='04_agua',
      rasgo=('Jacuzzi para dos','Jacuzzi for two'),
      cama=('Jacuzzi','Jacuzzi'),
      corta=('Planta baja con entrada independiente por una terraza grande y vista parcial al mar. El jacuzzi la vuelve la favorita de las lunas de miel.',
             'Ground floor with its own entrance through a large terrace and a partial ocean view. The jacuzzi makes it the honeymoon favourite.'),
      larga=(['Se entra por su propia terraza, sin pasar por las áreas comunes, lo que la hace la más privada de la casa.',
              'El jacuzzi está en la terraza, con vista parcial al mar. Es la suite que más se reserva para aniversarios y lunas de miel.'],
             ['You enter through its own terrace, without crossing the shared areas, which makes it the most private suite in the house.',
              'The jacuzzi sits on the terrace, with a partial ocean view. It is the suite most often booked for anniversaries and honeymoons.']),
      extras=(['Entrada independiente','Terraza grande','Vista parcial al mar'],
              ['Private entrance','Large terrace','Partial ocean view'])),

 dict(slug='palapa', tipo='suite', nombre='Suite Palapa', precio=360,
      m2=60, huespedes=2, foto='07_palapa',
      rasgo=('Vista al mar bajo techo de palma','Ocean view under a palapa roof'),
      cama=('Techo de palma','Palapa roof'),
      corta=('Duermes bajo la palma y con el aire del mar; no lleva aire acondicionado y ese es justo el punto. La más fresca entre noviembre y abril.',
             'You sleep under the palm roof with sea air; there is no air conditioning and that is precisely the point. The coolest room from November to April.'),
      larga=(['El techo de palapa y la ventilación cruzada mantienen la suite fresca sin aire acondicionado, que es como se ha dormido en esta costa desde siempre.',
              'Conviene saberlo antes de reservar: de mayo a octubre el calor de Sayulita es húmedo, y esta suite es para quien prefiere el ventilador y el aire del mar.'],
             ['The palapa roof and the cross ventilation keep the room cool without air conditioning, which is how people have slept on this coast for a long time.',
              'Worth knowing before you book: from May to October Sayulita is humid, and this suite is for guests who prefer a fan and sea air.']),
      extras=(['Vista al mar','Ventilación natural','Techo de palapa'],
              ['Ocean view','Natural ventilation','Palapa roof'])),

 dict(slug='sol', tipo='suite', nombre='Suite Sol', precio=360,
      m2=80, huespedes=2, foto='03_sol',
      rasgo=('Vista al jardín','Garden view'),
      cama=('Planta baja','Ground floor'),
      corta=('Calma, privacidad y silencio en planta baja. Dos ventanales, uno al jardín y otro a un traspatio de plantas que abre a un cubo de luz natural.',
             'Calm, privacy and quiet on the ground floor. Two large windows, one onto the garden and one onto a planted courtyard open to the sky.'),
      larga=(['Se entra por una salita con dos sofás convertibles, útiles para la siesta de la tarde o para una noche extra.',
              'Tiene dos ventanales: uno da al jardín y el otro a un traspatio lleno de plantas, al que se puede salir desde la suite. El piso de cerámica vidriada y la artesanía son lo que la vuelven distinta.'],
             ['You enter through a small sitting room with two convertible sofas, useful for an afternoon nap or an extra night.',
              'It has two large windows: one onto the garden, the other onto a planted courtyard you can step into from the room. The glazed ceramic floor and the crafts are what set it apart.']),
      extras=(['Sala independiente','Traspatio privado','Planta baja'],
              ['Separate sitting room','Private courtyard','Ground floor'])),

 dict(slug='luna', tipo='jr', nombre='Jr. Suite Luna', precio=240,
      m2=30, huespedes=2, foto='01_luna',
      rasgo=('Vista al jardín, sin escaleras','Garden view, step-free'),
      cama=('Cama queen','Queen bed'),
      corta=('Pequeña y bien resuelta, con cama queen. Ideal para una pareja joven o para quien prefiere no subir escaleras.',
             'Small and well resolved, with a queen bed. Ideal for a young couple or anyone who would rather skip the stairs.'),
      larga=(['Treinta metros cuadrados aprovechados al máximo: cama queen, baño completo y vista al jardín.',
              'Está en planta baja y no tiene escaleras de por medio, así que es la más cómoda para quien llega con equipaje pesado o prefiere no subir.'],
             ['Thirty square metres used well: a queen bed, a full bathroom and a garden view.',
              'It sits on the ground floor with no stairs along the way, so it is the easiest room for anyone arriving with heavy luggage.']),
      extras=(['Sin escaleras','Vista al jardín','Cama queen'],
              ['Step-free','Garden view','Queen bed'])),

 dict(slug='arena', tipo='jr', nombre='Jr. Suite Arena', precio=240,
      m2=30, huespedes=2, foto='02_arena',
      rasgo=('Dos camas individuales','Two single beds'),
      cama=('Dos camas','Two beds'),
      corta=('Pensada para compartir con una amiga o con la familia: dos camas individuales, escritorio y una decoración ecléctica.',
             'Made for sharing with a friend or a relative: two single beds, a desk and an eclectic mix of pieces.'),
      larga=(['Es la única suite con dos camas individuales, así que resuelve el viaje de dos amigas o de madre e hija adulta.',
              'Tiene escritorio, lo que la hace la mejor opción para quien viene a trabajar unos días desde Sayulita.'],
             ['The only suite with two single beds, which solves a trip for two friends or a mother and her grown daughter.',
              'It has a desk, which makes it the best choice for anyone coming to work from Sayulita for a few days.']),
      extras=(['Dos camas individuales','Escritorio','Vista al jardín'],
              ['Two single beds','Desk','Garden view'])),
]

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
   nav_completa='Casa completa', nav_ofertas='Ofertas', nav_contacto='Contacto',
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
   nav_completa='Whole house', nav_ofertas='Offers', nav_contacto='Contact',
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

def barra(lang, clave, prof=0, slug=None):
    t = T[lang]; a = base(lang, prof) + ('../assets/' if lang == 'en' else 'assets/')
    def act(c): return ' aria-current="page"' if c == clave else ''
    return f'''
<header class="barra">
  <button class="menu-btn" id="abrir" aria-expanded="false" aria-controls="cortina">
    <span class="hamb" aria-hidden="true"><i></i><i></i><i></i></span><span>{t['menu']}</span>
  </button>
  <a class="logo" href="{url(lang,'index',prof)}" aria-label="Mi Otra Casa">
    <img src="{a}logo-mi-otra-casa.png" width="900" height="125" alt="Mi Otra Casa">
  </a>
  <a class="reservar" href="{url(lang,'reservar',prof)}">{t['reservar']}</a>
</header>

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
      <a href="{url(lang,'index',prof)}#ofertas">{t['nav_ofertas']}</a>
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
