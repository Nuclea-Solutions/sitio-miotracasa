#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye todas las páginas. Uso:  python3 pages.py"""
import os, json
from build import (RAIZ, DOMINIO, RAIZ_WEB, SUITES, INCLUYE, T, RUTAS, foto, foto_url,
                   base, url, alterno, cabeza, barra, pie, escribir)

L = ('es', 'en')
i = lambda lang: 0 if lang == 'es' else 1          # índice de idioma en las tuplas

# ---------------------------------------------------------------- portada

EXPERIENCIAS = [
 ('el-atardecer-todos-los-dias', ('El atardecer, todos los días','Sunset, every single day'),
  ('A las seis el pueblo entero camina hacia la playa principal. Es el plan que nadie organiza y todos cumplen.',
   'At six the whole town walks down to the main beach. It is the plan nobody organises and everybody keeps.')),
 ('calles-que-dan-al-mar', ('Calles que dan al mar','Streets that end at the sea'),
  ('Fachadas de colores, palmeras y el Pacífico al final de la cuadra. Todo el centro se recorre a pie.',
   'Painted façades, palm trees and the Pacific at the end of the block. The whole centre is walkable.')),
 ('playa-de-los-muertos', ('Playa de los Muertos','Playa de los Muertos'),
  ('La playa tranquila de Sayulita, a poco más de setecientos metros. Agua clara y menos gente que en la principal.',
   'Sayulita’s quiet beach, just over seven hundred metres away. Clear water and fewer people than the main one.')),
 ('campamento-tortuguero', ('Campamento tortuguero','Turtle camp'),
  ('A siete cuadras. En temporada se liberan crías al atardecer y se puede participar.',
   'Seven blocks away. In season, hatchlings are released at dusk and guests can take part.')),
 ('clases-de-surf', ('Clases de surf','Surf lessons'),
  ('La ola de Sayulita es de las más nobles del Pacífico para aprender a surfear. Te conectamos con instructores del pueblo.',
   'Sayulita’s wave is one of the friendliest on the Pacific for learning. We put you in touch with local instructors.')),
 ('la-plaza-a-media-cuadra', ('La plaza, a media cuadra','The plaza, half a block away'),
  ('Papel picado, puestos y las mejores paletas del pueblo. Se cruza en dos minutos desde la puerta.',
   'Papel picado, market stalls and the best paletas in town. Two minutes from the door.')),
]

TEXTOS = {
 'index': dict(
  titulo=('Mi Otra Casa — Hotel boutique en Sayulita, Nayarit',
          'Mi Otra Casa — Boutique hotel in Sayulita, Mexico'),
  desc=('Hotel boutique de siete suites en el corazón de Sayulita, a media cuadra de la plaza y a tres del mar. Solo adultos, desayuno incluido. Desde 240 USD la noche.',
        'A seven-suite boutique hotel in the heart of Sayulita, half a block from the plaza and three from the sand. Adults only, breakfast included. From 240 USD a night.'),
  h1=('Una casa de siete suites, a tres cuadras del mar',
      'A house of seven suites, three blocks from the sea'),
  lugar=('Sayulita, Nayarit','Sayulita, Nayarit, Mexico'),
  suites_t=('Siete formas de quedarse','Seven ways to stay'),
  suites_p=('Cada suite es distinta a la anterior, y ahí está el encanto de quedarse en una casa y no en un hotel. Todas llevan el nombre de lo que las define — el sol de la mañana, el agua del jacuzzi, la palma del techo. De 240 a 420 dólares por noche, siempre con desayuno.',
            'Every suite is different from the last, and that is the charm of staying in a house rather than a hotel. Each is named after what defines it — the morning sun, the jacuzzi water, the palm roof. From 240 to 420 dollars a night, always with breakfast.'),
  vistazo_t=('La casa, de un vistazo','The house at a glance'),
  vistazo_p=('Todo lo de abajo va incluido en cualquier suite, sin costo adicional y sin tener que pedirlo.',
             'Everything below comes with any suite, at no extra cost and without having to ask.'),
  say_t=('Todo pasa caminando','Everything happens on foot'),
  say_p=('Estamos a media cuadra de la plaza y a tres del mar. No hace falta coche, ni taxi, ni salir a buscar nada: el pueblo entero está a pie, con todo lo que eso trae.',
         'We are half a block from the plaza and three from the sea. No car, no taxi, nothing to go looking for: the whole town is walkable, with everything that brings.'),
  des_t=('Servido donde te acomodes','Served wherever you settle in'),
  des_p=('De ocho a once, en la terraza, en el jardín o en tu suite. Va incluido en todas las tarifas, siempre, sin letra chica.',
         'From eight to eleven, on the terrace, in the garden or in your suite. Included in every rate, always, no small print.'),
  comp_t=('Para cuando vienen todos','For when everyone comes'),
  comp_p=('Siete suites, terrazas compartidas, jardín y cocina, para hasta catorce personas. Se renta entera para bodas, cumpleaños y viajes de amigos.',
          'Seven suites, shared terraces, a garden and a kitchen, for up to fourteen people. The house can be booked whole for weddings, birthdays and trips with friends.'),
  cita=('Del desayuno al mar, descalzo','From breakfast to the sea, barefoot'),
  cita_pie=('Solo adultos · Siete suites · Sayulita','Adults only · Seven suites · Sayulita'),
 ),
}

def portada_video(lang, t):
    a = 'assets/' if lang == 'es' else '../assets/'
    x = TEXTOS['index']; k = i(lang)
    return f'''
  <section class="portada portada--video">
    <video class="fondo" id="video" autoplay muted loop playsinline preload="metadata"
           poster="{a}portada-poster.jpg" aria-label="{'Vista aérea de Sayulita' if lang=='es' else 'Aerial view of Sayulita'}">
      <source src="{a}portada.mp4" type="video/mp4">
    </video>
    <button class="control" id="control" aria-label="{'Pausar video' if lang=='es' else 'Pause video'}">&#10073;&#10073;</button>
    <div class="txt">
      <h1 class="display">{x['h1'][k]}</h1>
      <p class="rotulo">{x['lugar'][k]}</p>
    </div>
    <p class="baja" aria-hidden="true"><span></span>{'Desliza' if lang=='es' else 'Scroll'}</p>
  </section>
'''

def pagina_index(lang):
    t = T[lang]; k = i(lang); x = TEXTOS['index']
    prof = 0
    a = 'assets/' if lang == 'es' else '../assets/'
    jsonld = {
      "@context":"https://schema.org","@type":"Hotel","name":"Mi Otra Casa","alternateName":"MOC",
      "url": DOMINIO + ('/' if lang=='es' else '/en/'),
      "image": DOMINIO + "/assets/compartir.jpg",
      "description": x['desc'][k],
      "address":{"@type":"PostalAddress","streetAddress":"Marlin 18","addressLocality":"Sayulita",
                 "addressRegion":"Nayarit","postalCode":"63734","addressCountry":"MX"},
      "email":"contact@miotracasa.mx","priceRange":"$$$","petsAllowed":False,"smokingAllowed":False,
      "numberOfRooms":7,"checkinTime":"16:00","checkoutTime":"11:00",
      "starRating":{"@type":"Rating","ratingValue":4},
      "geo":{"@type":"GeoCoordinates","latitude":20.86830,"longitude":-105.44066},
      "amenityFeature":[{"@type":"LocationFeatureSpecification","name":n,"value":True} for n in
                        (["Desayuno incluido","WiFi sin costo","Alberca","Bar junto a la alberca","Servicios de spa","Estacionamiento sin costo","Aire acondicionado","Asador","Jardín","Terraza","Sala de juegos"]
                         if lang=='es' else
                         ["Breakfast included","Free WiFi","Outdoor pool","Poolside bar","Spa services","Free parking","Air conditioning","Barbecue grill","Garden","Terrace","Game room"])],
      "sameAs":["https://www.instagram.com/miotracasa/","https://www.facebook.com/MOCSayulita"]
    }
    extra = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'

    vistazo = '\n'.join(f'''      <article class="servicio">
        <svg viewBox="0 0 24 24" aria-hidden="true">{ICONOS[ic]}</svg>
        <div><h3>{tit[k]}</h3><p>{txt[k]}</p></div>
      </article>''' for ic, tit, txt in sorted((x for x in SERVICIOS if x[0] in VISTAZO), key=lambda x: VISTAZO.index(x[0])))

    exps = '\n'.join(f'''      <article class="tarjeta-exp">
        <div class="foto"><img src="{a}{img}.jpg" width="620" height="827" alt="{tit[k]}" loading="lazy" decoding="async"></div>
        <h3>{tit[k]}</h3>
        <p>{txt[k]}</p>
      </article>''' for img, tit, txt in EXPERIENCIAS)

    return (cabeza(lang, x['titulo'][k], x['desc'][k], 'index', prof, extra=extra)
      + barra(lang, 'index', prof)
      + '\n<main id="contenido">\n'
      + portada_video(lang, t)
      + f'''
  <section class="bloque rev" id="suites" aria-labelledby="t-suites">
    <div class="foto">{foto(a, 'suite-sayulita-recamara', lang, 'bloque')}</div>
    <div class="texto">
      <p class="rotulo">{t['nav_suites']}</p>
      <h2 class="display" id="t-suites">{x['suites_t'][k]}</h2>
      <p>{x['suites_p'][k]}</p>
      <a class="liga" href="{url(lang,'suites',prof)}">{t['volver']}</a>
    </div>
  </section>

  <section class="ofertas rev" id="la-casa" aria-labelledby="t-casa">
    <div class="centro">
      <p class="rotulo">{t['nav_servicios']}</p>
      <h2 class="display" id="t-casa">{x['vistazo_t'][k]}</h2>
      <p>{x['vistazo_p'][k]}</p>
    </div>
    <div class="vistazo">
{vistazo}
    </div>
    <p class="centro" style="margin-top:var(--seccion-corta)"><a class="liga" href="{url(lang,'casa',prof)}#servicios">{('Ver todos los servicios','See all services')[k]}</a></p>
  </section>

  <section class="rev seccion-sayulita" id="experiencias" aria-labelledby="t-say">
    <div class="centro limite">
      <p class="rotulo">Sayulita</p>
      <h2 class="display" id="t-say">{x['say_t'][k]}</h2>
      <p>{x['say_p'][k]}</p>
    </div>
    <div class="carril" tabindex="0" role="group" aria-label="{x['say_t'][k]}">
{exps}
    </div>
  </section>

  <section class="bloque rev" aria-labelledby="t-des">
    <div class="foto">{foto(a, 'casa-comedor-palapa', lang, 'bloque')}</div>
    <div class="texto">
      <p class="rotulo">{'Desayuno' if lang=='es' else 'Breakfast'}</p>
      <h2 class="display" id="t-des">{x['des_t'][k]}</h2>
      <p>{x['des_p'][k]}</p>
      <a class="liga" href="{url(lang,'casa',prof)}">{'Conocer la casa' if lang=='es' else 'See the house'}</a>
    </div>
  </section>

  {resenas(lang, prof)}

  <section class="bloque rev" id="casa-completa" aria-labelledby="t-comp">
    <div class="foto">{foto(a, 'casa-alberca-atardecer', lang, 'bloque')}</div>
    <div class="texto">
      <p class="rotulo">{t['nav_completa']}</p>
      <h2 class="display" id="t-comp">{x['comp_t'][k]}</h2>
      <p>{x['comp_p'][k]}</p>
      <a class="liga" href="{url(lang,'contacto',prof)}">{'Consultar disponibilidad' if lang=='es' else 'Check availability'}</a>
    </div>
  </section>

  <section class="cita rev">
    <img src="{a}monograma-moc.png" width="272" height="130" alt="" loading="lazy">
    <blockquote class="display">{x['cita'][k]}</blockquote>
    <cite>{x['cita_pie'][k]}</cite>
  </section>

</main>
''' + pie(lang, prof))

# ---------------------------------------------------------------- reseñas

RESENAS = [
 ('“This place has a great friendly staff. Clean. Beautiful shared areas and rooftop.”', 'TripAdvisor',
  ('febrero 2023','February 2023'),
  'https://www.tripadvisor.com/Hotel_Review-g445056-d17532206-Reviews-Mi_Otra_Casa-Sayulita_Pacific_Coast.html'),
 ('“The room was beautiful as well as the common areas.”', 'Hotels.com',
  ('mayo 2026','May 2026'),
  'https://www.hotels.com/ho738695264/mi-otra-casa-adults-only-sayulita-mexico/'),
 ('“We just stayed at Mi Otra Casa and it was fabulous.”', 'Trip.com', None,
  'https://www.trip.com/hotels/sayulita-hotel-detail-21860524/mi-otra-casa/'),
]

PUNTAJES = [
 ('9.6', 'Expedia', 'https://www.expedia.mx/Puerto-Vallarta-Hoteles-Mi-Otra-Casa-Adults-Only.h23052977.Informacion-Hotel'),
 ('9.6', 'Hotels.com', 'https://www.hotels.com/ho738695264/mi-otra-casa-adults-only-sayulita-mexico/'),
 ('10', 'Booking.com', 'https://www.booking.com/hotel/mx/mi-otra-casa.html'),
]

def resenas(lang, prof):
    k = i(lang)
    tit = ('Lo que dicen quienes se quedaron','What past guests say')[k]
    sub = ('Reseñas publicadas por huéspedes verificados en las plataformas. Las dejamos sin nombre; quien quiera leerlas completas puede ir a la fuente.',
           'Reviews published by verified guests on the platforms. We leave them unsigned; anyone who wants to read them in full can go to the source.')[k]
    verif = ('Huésped verificado','Verified guest')[k]
    ver = ('Ver la reseña','See the review')[k]
    pts = '\n'.join(f'        <a class="puntaje" href="{u}" rel="noopener"><b>{n}</b><span>{f}</span></a>' for n, f, u in PUNTAJES)
    tarjetas = '\n'.join(f"""      <article class="resena">
        <blockquote>{txt}</blockquote>
        <footer><b>{fuente}</b>{verif}{' · ' + fecha[k] if fecha else ''}<br><a class="liga" href="{u}" rel="noopener">{ver}</a></footer>
      </article>""" for txt, fuente, fecha, u in RESENAS)
    return f"""<section class="resenas rev" aria-labelledby="t-res">
    <header>
      <p class="rotulo">{('Reseñas','Reviews')[k]}</p>
      <h2 class="display" id="t-res">{tit}</h2>
      <p>{sub}</p>
    </header>
    <div class="lista">
{tarjetas}
    </div>
    <div class="puntajes">
{pts}
    </div>
  </section>"""

# ---------------------------------------------------------------- suites

def pagina_suites(lang):
    t = T[lang]; k = i(lang); prof = 0
    a = 'assets/' if lang == 'es' else '../assets/'
    titulo = ('Suites — Mi Otra Casa, Sayulita','Suites — Mi Otra Casa, Sayulita')[k]
    desc = ('Las siete suites de Mi Otra Casa: master suites con vista al mar, suites con jacuzzi o techo de palapa y junior suites al jardín. Desde 240 USD con desayuno.',
            'The seven suites at Mi Otra Casa: master suites with ocean views, suites with a jacuzzi or a palapa roof, and junior suites onto the garden. From 240 USD with breakfast.')[k]
    intro = ('Cada suite es distinta a la anterior, y ahí está el encanto de quedarse en una casa y no en un hotel. Todas llevan el nombre de lo que las define — el sol de la mañana, el agua del jacuzzi, la palma del techo — y todas incluyen desayuno.',
             'Every suite is different from the last, and that is the charm of staying in a house rather than a hotel. Each is named after what defines it — the morning sun, the jacuzzi water, the palm roof — and every one includes breakfast.')[k]
    filtros = [('todas',('Todas','All')),('master',('Master suites','Master suites')),
               ('suite',('Suites','Suites')),('jr',('Jr. suites','Jr. suites'))]
    fbtn = '\n'.join(f'''    <button type="button" data-tipo="{v}" aria-pressed="{str(v=='todas').lower()}">{n[k]}</button>''' for v, n in filtros)

    tarjetas = []
    for s in SUITES:
        tarjetas.append(f'''    <article class="suite" data-tipo="{s['tipo']}">
      <a class="foto" href="{url(lang,'suite',prof,s['slug'])}" aria-label="{t['ver']}: {s['nombre']}">
        {foto(a, s['fotos'][0], lang, 'tarjeta', alt=s['nombre'])}
        {foto(a, s['fotos'][1], lang, 'tarjeta', clase='alt', alt='')}
      </a>
      <h2>{s['nombre']}</h2>
      <p>{s['corta'][k]}</p>
      <p class="datos"><span>{s['m2']} m²</span><span>{s['huespedes']} {'adultos' if lang=='es' else 'adults'}</span><span>{s['cama'][k]}</span></p>
      <p class="desde"><b>${s['precio']}</b>{t['noche']}</p>
      <div class="acciones">
        <a class="boton" href="{url(lang,'suite',prof,s['slug'])}">{t['ver']}</a>
        <a class="liga" href="{url(lang,'reservar',prof)}">{t['reservar']}</a>
      </div>
    </article>''')

    jsonld = {"@context":"https://schema.org","@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":n+1,"name":s['nombre'],
         "url": f"{DOMINIO}/{'en/' if lang=='en' else ''}{RUTAS[lang]['suite'](s['slug'])}"}
        for n, s in enumerate(SUITES)]}
    extra = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'

    return (cabeza(lang, titulo, desc, 'suites', prof, extra=extra)
      + barra(lang, 'suites', prof)
      + f'''
<main id="contenido">

  <section class="portada portada--interior">
    {foto(a, 'casa-terraza-mar', lang, 'portada', clase='fondo', alt='', perezosa=False, extra=' fetchpriority="high"')}
    <div class="txt">
      <p class="rotulo">{('Nuestras suites','Our suites')[k]}</p>
      <h1 class="display">{('Siete formas de quedarse','Seven ways to stay')[k]}</h1>
    </div>
  </section>

  <p class="centro limite" style="padding-block:var(--seccion) var(--seccion-corta);color:var(--texto)">{intro}</p>

  <div class="filtros" id="filtros" role="group" aria-label="{('Filtrar suites','Filter suites')[k]}">
{fbtn}
  </div>

  <div class="rejilla" id="lista-suites">
''' + '\n'.join(tarjetas) + f'''
    <p class="vacio" id="sin-resultados" hidden>{('No hay suites de ese tipo.','No suites of that type.')[k]}</p>
  </div>

  <section class="cierre" id="casa-completa">
    <img class="mono" src="{a}monograma-moc.png" width="272" height="130" alt="" loading="lazy">
    <h2 class="display">{('¿Vienen todos?','Bringing everyone?')[k]}</h2>
    <p>{TEXTOS['index']['comp_p'][k]}</p>
    <a class="boton" href="{url(lang,'contacto',prof)}">{('Consultar la casa completa','Ask about the whole house')[k]}</a>
  </section>

</main>
''' + pie(lang, prof))

# ---------------------------------------------------------------- página de suite

def pagina_suite(lang, s):
    t = T[lang]; k = i(lang); prof = 1
    a = base(lang, prof) + ('../assets/' if lang == 'en' else 'assets/')
    titulo = f"{s['nombre']} — Mi Otra Casa, Sayulita"
    desc = s['corta'][k][:155]
    otras = [o for o in SUITES if o['slug'] != s['slug']][:3]
    otras_html = '\n'.join(f'''      <a href="{url(lang,'suite',prof,o['slug'])}">
        <div class="foto">{foto(a, o['fotos'][0], lang, 'otras', alt=o['nombre'])}</div>
        <h3>{o['nombre']}</h3>
        <p>{o['rasgo'][k]} · {t['desde'].lower()} ${o['precio']} USD</p>
      </a>''' for o in otras)
    fotos_suite = '\n'.join(
        f'    <a href="{foto_url(a, n)}">{foto(a, n, lang, "suite1" if j == 0 else "suite2", perezosa=j > 0, extra=' fetchpriority="high"' if j == 0 else '')}</a>'
        for j, n in enumerate(s['fotos']))
    incluye = '\n'.join(f'        <li>{x}</li>' for x in (list(s['extras'][k]) + list(INCLUYE[k])))
    parrafos = '\n'.join(f'      <p>{p}</p>' for p in s['larga'][k])

    jsonld = {"@context":"https://schema.org","@type":"HotelRoom","name":s['nombre'],
      "description": s['corta'][k],
      "url": f"{DOMINIO}/{'en/' if lang=='en' else ''}{RUTAS[lang]['suite'](s['slug'])}",
      "image": DOMINIO + '/' + foto_url('assets/', s['fotos'][0]),
      "occupancy":{"@type":"QuantitativeValue","maxValue":s['huespedes']},
      "floorSize":{"@type":"QuantitativeValue","value":s['m2'],"unitCode":"MTK"},
      "containedInPlace":{"@type":"Hotel","name":"Mi Otra Casa","url":DOMINIO+"/"}}
    extra = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'

    return (cabeza(lang, titulo, desc, 'suite', prof, slug=s['slug'], extra=extra)
      + barra(lang, 'suites', prof, slug=s['slug'])
      + f'''
<main id="contenido">

  <div class="suite-fotos" id="galeria">
{fotos_suite}
  </div>

  <div class="suite-cuerpo">
    <div>
      <p class="rotulo">{s['rasgo'][k]}</p>
      <h1 class="display">{s['nombre']}</h1>
      <p class="ficha"><span>{s['m2']} m²</span><span>{s['huespedes']} {'adultos' if lang=='es' else 'adults'}</span><span>{s['cama'][k]}</span><span>{s['orienta'][k]}</span></p>
      <div class="suite-texto">
{parrafos}
      </div>
      <div class="incluye">
        <h2>{t['incluye']}</h2>
        <ul>
{incluye}
        </ul>
      </div>
      <p><a class="liga" href="{url(lang,'politicas',prof)}">{('Ver políticas de la casa','See house policies')[k]}</a></p>
    </div>

    <aside class="tarjeta-reserva">
      <p class="rotulo">{t['desde']}</p>
      <p class="desde"><b>${s['precio']}</b>{t['noche']}</p>
      <a class="boton" href="{url(lang,'reservar',prof)}?suite={s['slug']}">{t['reservar']}</a>
      <div class="detalle">
        <p>{('Llegada 16:00–19:00 · Salida 11:00','Check-in 4–7 pm · Check-out 11 am')[k]}</p>
        <p>{('Mínimo dos noches, tres en temporada alta','Two-night minimum, three in high season')[k]}</p>
        <p>{('Cancelación sin costo hasta 7 días antes','Free cancellation up to 7 days before')[k]}</p>
        <p>{('Solo adultos, a partir de 21 años','Adults only, 21 and over')[k]}</p>
      </div>
    </aside>
  </div>

  <section class="otras">
    <h2>{('Otras suites','Other suites')[k]}</h2>
    <div class="lista">
{otras_html}
    </div>
    <p style="margin-top:2.5rem"><a class="liga" href="{url(lang,'suites',prof)}">{t['volver']}</a></p>
  </section>

</main>

<div class="visor" id="visor" aria-hidden="true">
  <button class="cerrar-visor" aria-label="{('Cerrar imagen','Close image')[k]}">&#10005;</button>
  <img src="" alt="">
</div>
''' + pie(lang, prof))


# ---------------------------------------------------------------- la casa

ICONOS = {
 'desayuno':'<path d="M4 9h12v5a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V9Z"/><path d="M16 10h2.5a2.5 2.5 0 0 1 0 5H16"/><path d="M7 5.5c0-1 1-1 1-2M11 5.5c0-1 1-1 1-2"/>',
 'wifi':'<path d="M2.5 9a15 15 0 0 1 19 0"/><path d="M5.5 12.5a10.5 10.5 0 0 1 13 0"/><path d="M8.5 16a6 6 0 0 1 7 0"/><circle cx="12" cy="19.5" r=".6" fill="currentColor" stroke="none"/>',
 'amenidades':'<path d="M12 3c2.5 2.5 3.5 4.5 3.5 6.5a3.5 3.5 0 0 1-7 0C8.5 7.5 9.5 5.5 12 3Z"/><path d="M5 13c2 3.5 4.5 5.5 7 8 2.5-2.5 5-4.5 7-8"/>',
 'tv':'<rect x="2.5" y="4.5" width="19" height="13" rx="1.5"/><path d="M8 21h8"/><path d="M12 17.5V21"/>',
 'codigo':'<rect x="5" y="2.5" width="14" height="19" rx="2"/><circle cx="9.5" cy="8" r=".9" fill="currentColor" stroke="none"/><circle cx="14.5" cy="8" r=".9" fill="currentColor" stroke="none"/><circle cx="9.5" cy="12.5" r=".9" fill="currentColor" stroke="none"/><circle cx="14.5" cy="12.5" r=".9" fill="currentColor" stroke="none"/><circle cx="9.5" cy="17" r=".9" fill="currentColor" stroke="none"/><circle cx="14.5" cy="17" r=".9" fill="currentColor" stroke="none"/>',
 'concierge':'<path d="M3 17h18"/><path d="M4.5 17a7.5 7.5 0 0 1 15 0"/><path d="M12 6.5v3"/><circle cx="12" cy="5" r="1.3"/>',
 'asador':'<path d="M4 10h16l-1.6 5.5a3 3 0 0 1-2.9 2.1H8.5a3 3 0 0 1-2.9-2.1L4 10Z"/><path d="M8 21l1-3M16 21l-1-3"/><path d="M9.5 6.5c0-1 1-1.2 1-2.2M14 6.5c0-1 1-1.2 1-2.2"/>',
 'tarjeta':'<rect x="2.5" y="5.5" width="19" height="13" rx="2"/><path d="M2.5 10h19"/><path d="M6 14.5h4"/>',
 'caja':'<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.4"/>',
 'humo':'<rect x="2.5" y="13" width="15" height="5" rx="1"/><path d="M20 13h1.5v5H20"/><path d="M9 13v5M13.5 13v5"/><path d="M12 10c0-2 2-2 2-3.5S12.5 4 12.5 4"/><path d="M3 3l18 18"/>',
 'mascotas':'<ellipse cx="12" cy="16" rx="4" ry="3.2"/><ellipse cx="6.5" cy="11" rx="2" ry="2.4"/><ellipse cx="17.5" cy="11" rx="2" ry="2.4"/><ellipse cx="9.5" cy="6.5" rx="1.8" ry="2.2"/><ellipse cx="14.5" cy="6.5" rx="1.8" ry="2.2"/>',
 'parking':'<rect x="3.5" y="3.5" width="17" height="17" rx="2"/><path d="M9.5 17V7.5h3a3 3 0 0 1 0 6h-3"/>',
 'alberca':'<path d="M3 16c1.6 0 1.6 1.4 3.2 1.4S7.8 16 9.4 16s1.6 1.4 3.2 1.4S14.2 16 15.8 16s1.6 1.4 3.2 1.4S20.6 16 22 16"/><path d="M3 20c1.6 0 1.6 1.4 3.2 1.4S7.8 20 9.4 20s1.6 1.4 3.2 1.4S14.2 20 15.8 20s1.6 1.4 3.2 1.4S20.6 20 22 20"/><path d="M8 17V5a2 2 0 0 1 4 0M16 17V5a2 2 0 0 0-4 0"/><path d="M8 9h8"/>',
 'bar':'<path d="M4 4h16l-8 8Z"/><path d="M12 12v7"/><path d="M8.5 19h7"/><path d="M15 7.5c2-2 4-1 4-1"/>',
 'spa':'<path d="M12 21c0-4.5 3.5-8 8-8 0 4.5-3.5 8-8 8Z"/><path d="M12 21c0-4.5-3.5-8-8-8 0 4.5 3.5 8 8 8Z"/><path d="M12 21c-1.5-4 0-8.5 2.5-11-2.5 1-4.5 3-5 5.5"/>',
 'juegos':'<rect x="2.5" y="7" width="19" height="11" rx="3.5"/><path d="M7 11v3M5.5 12.5h3"/><circle cx="16" cy="12" r=".9" fill="currentColor" stroke="none"/><circle cx="18.5" cy="14" r=".9" fill="currentColor" stroke="none"/>',
 'cocina':'<rect x="3" y="5" width="18" height="9" rx="1.5"/><path d="M3 18h18"/><path d="M7 8.5h4M7 11h2"/><circle cx="17" cy="9.5" r="1.6"/>',
 'equipaje':'<rect x="4" y="7.5" width="16" height="12" rx="2"/><path d="M9 7.5V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2.5"/><path d="M9 19.5V21M15 19.5V21"/>',
 'escaleras':'<path d="M3 20h4v-4h4v-4h4V8h4V4"/><path d="M3 20v-1"/>',
}

# los seis que se muestran en «La casa, de un vistazo» de la portada
VISTAZO = ('desayuno','alberca','bar','spa','asador','wifi')

SERVICIOS = [
 ('desayuno', ('Desayuno incluido','Breakfast included'),
  ('Todas las reservas incluyen desayuno diario para dos personas, servido donde te acomodes.',
   'Every booking includes daily breakfast for two, served wherever you settle in.')),
 ('wifi', ('WiFi sin costo','Free WiFi'),
  ('Red disponible en toda la casa, incluidas las terrazas y el jardín.',
   'Available throughout the house, terraces and garden included.')),
 ('amenidades', ('Amenidades de baño','Bath amenities'),
  ('Productos de regadera y varios tipos de toalla en cada suite.',
   'Shower products and several kinds of towel in every suite.')),
 ('tv', ('Smart TV','Smart TV'),
  ('Pantalla inteligente de última generación en varias de las suites.',
   'Latest-generation smart screens in several of the suites.')),
 ('codigo', ('Entrada con código','Keypad entry'),
  ('La puerta principal se abre con clave: puedes llegar e irte a la hora que quieras.',
   'The main door opens with a code: arrive and leave whenever you like.')),
 ('concierge', ('Concierge','Concierge'),
  ('Reservas de mesa, clases, tours y traslados: pregunta y te lo resolvemos.',
   'Restaurant tables, lessons, tours and transfers: ask and we sort it out.')),
 ('asador', ('Asador','Barbecue grill'),
  ('Asador Weber para uso de los huéspedes, junto a la alberca o en la terraza grande.',
   'A Weber grill for guests to use, by the pool or on the large terrace.')),
 ('tarjeta', ('Pago con tarjeta','Card payment'),
  ('Aceptamos American Express, Visa y Mastercard, además de otras formas de pago.',
   'We take American Express, Visa and Mastercard, as well as other payment methods.')),
 ('caja', ('Caja fuerte','Safe box'),
  ('Cada suite tiene caja de seguridad con espacio para una laptop de hasta 14 pulgadas.',
   'Every suite has a safe that fits a laptop of up to 14 inches.')),
 ('humo', ('Espacio sin humo','Smoke-free'),
  ('No se fuma dentro de las suites, por respeto a los demás huéspedes.',
   'No smoking inside the suites, out of respect for other guests.')),
 ('mascotas', ('Sin mascotas','No pets'),
  ('Por higiene y por el descanso de todos, no recibimos mascotas.',
   'For hygiene and for everyone’s rest, we do not accept pets.')),
 ('parking', ('Estacionamiento sin costo','Free parking'),
  ('Estacionamiento propio sin costo, limitado y bajo petición, más lugar en la calle.',
   'Free self parking on site, limited and on request, plus street parking nearby.')),
 ('alberca', ('Alberca y camastros','Pool and loungers'),
  ('Abierta de 8:00 a medianoche, con cabañas, sombrillas y camastros sin costo.',
   'Open from 8 am to midnight, with cabanas, umbrellas and loungers at no charge.')),
 ('bar', ('Bar junto a la alberca','Poolside bar'),
  ('Barra a pie de alberca para la tarde, sin tener que salir de la casa.',
   'A bar at the edge of the pool for the afternoon, without leaving the house.')),
 ('spa', ('Masaje y spa','Spa and massage'),
  ('Servicios de spa y masaje que se agendan desde la casa, con terapeutas del pueblo.',
   'Spa and massage services booked from the house, with local therapists.')),
 ('juegos', ('Sala de juegos','Game room'),
  ('Sala común con juegos para las tardes de calor o los días de lluvia.',
   'A shared room with games for hot afternoons and rainy days.')),
 ('cocina', ('Microondas y refrigerador','Microwave and fridge'),
  ('De uso compartido, además del frigobar de cada suite.',
   'Shared, in addition to the minibar in every suite.')),
 ('equipaje', ('Guarda equipaje','Luggage storage'),
  ('Puedes dejar las maletas antes de la llegada o después de la salida.',
   'Leave your bags before check-in or after check-out.')),
 ('escaleras', ('Tres niveles, sin elevador','Three floors, no lift'),
  ('La casa se recorre por escaleras. Luna es la única suite que no las tiene de por medio.',
   'The house is laid out over stairs. Luna is the only suite reached without them.')),
]

# espacios comunes; la 1.ª y la 8.ª ocupan doble en la retícula, así que van horizontales
GALERIA = ['casa-fachada', 'casa-alberca', 'casa-reposeras', 'casa-alberca-sala', 'casa-bar-palapa',
           'casa-terraza-atardecer', 'casa-corredor', 'casa-palapa-rooftop', 'casa-masaje', 'casa-hora-azul']

def pagina_casa(lang):
    t = T[lang]; k = i(lang); prof = 0
    a = 'assets/' if lang == 'es' else '../assets/'
    titulo = ('La casa — Mi Otra Casa, Sayulita','The house — Mi Otra Casa, Sayulita')[k]
    desc = ('Mi Otra Casa por dentro: jardín, alberca, terrazas y siete suites a media cuadra de la plaza de Sayulita.',
            'Inside Mi Otra Casa: garden, pool, terraces and seven suites half a block from the plaza in Sayulita.')[k]
    intro = ([ 'Mi Otra Casa está en Marlin 18, a media cuadra de la plaza y a tres del mar. Son tres niveles alrededor de un jardín, con alberca, terrazas que se comparten y siete suites que no se parecen entre sí.',
               'No hay recepción con mostrador ni pasillos largos. La puerta principal abre con código, el desayuno se sirve donde te acomodes y si necesitas algo del pueblo — una mesa, una tabla, un taxi al aeropuerto — se resuelve preguntando.',
               'Es una casa para adultos que vienen a descansar. Afuera, Sayulita es un pueblo de fiesta y en temporada alta se escucha hasta la madrugada; adentro, las suites interiores dan al jardín y en todas hay tapones y ruido blanco. Lo decimos antes de que reserves, no después.'],
             [ 'Mi Otra Casa sits at Marlin 18, half a block from the plaza and three from the sea. Three floors around a garden, with a pool, shared terraces and seven suites that look nothing alike.',
               'There is no front desk and there are no long corridors. The main door opens with a code, breakfast is served wherever you settle in, and anything you need from town — a table, a surfboard, a ride to the airport — gets sorted by asking.',
               'It is a house for adults who came to rest. Outside, Sayulita is a party town and in high season it is heard into the early hours; inside, the interior suites face the garden and every room has earplugs and a white-noise machine. We say so before you book, not after.'])[k]
    galeria = '\n'.join(f'    <figure>{foto(a, n, lang, "gal2" if j in (0, 7) else "gal", extra=f" data-grande=\"{foto_url(a, n)}\"")}</figure>'
                         for j, n in enumerate(GALERIA))
    servicios = '\n'.join(f"""      <article class="item">
        <svg viewBox="0 0 24 24" aria-hidden="true">{ICONOS[ic]}</svg>
        <div><h3>{tit[k]}</h3><p>{txt[k]}</p></div>
      </article>""" for ic, tit, txt in SERVICIOS)
    dist = ([('Plaza de Sayulita','A un lado'),('Playa de Sayulita','3 minutos a pie'),
             ('Playa de los Muertos','750 metros'),('Mercado de San Pancho','10 minutos en coche'),
             ('Aeropuerto de Puerto Vallarta','45 minutos')],
            [('Sayulita square','Next door'),('Sayulita beach','3-minute walk'),
             ('Playa de los Muertos','750 metres'),('San Pancho market','10 minutes by car'),
             ('Puerto Vallarta airport','45 minutes')])[k]
    distancias = '\n'.join(f'        <div><span>{x}</span><b>{y}</b></div>' for x, y in dist)

    return (cabeza(lang, titulo, desc, 'casa', prof)
      + barra(lang, 'casa', prof)
      + f"""
<main id="contenido">

  <section class="portada portada--interior">
    <img class="fondo" src="{a}sayulita-aerea.jpg" width="1800" height="1012" alt="" aria-hidden="true">
    <div class="txt">
      <p class="rotulo">{t['nav_casa']}</p>
      <h1 class="display">{('Siete suites alrededor de un jardín','Seven suites around a garden')[k]}</h1>
    </div>
  </section>

  <section class="intro" aria-labelledby="t-intro">
    <h2 class="display" id="t-intro">{('Una casa que se abrió al pueblo','A house that opened up to the town')[k]}</h2>
    <div>
      <p>{intro[0]}</p>
      <p>{intro[1]}</p>
      <p>{intro[2]}</p>
    </div>
  </section>

  <section class="galeria" id="galeria" aria-label="{('Galería de la casa','House gallery')[k]}">
{galeria}
  </section>

  <section class="servicios" id="servicios" aria-labelledby="t-serv">
    <header>
      <p class="rotulo">{t['pie_servicios']}</p>
      <h2 class="display" id="t-serv">{('Lo que incluye quedarse aquí','What staying here includes')[k]}</h2>
      <p>{('Todo lo de abajo aplica para cualquier suite, sin costo adicional y sin tener que pedirlo.','Everything below applies to any suite, at no extra cost and without having to ask.')[k]}</p>
    </header>
    <div class="lista">
{servicios}
    </div>
  </section>

  <section class="ubica" aria-labelledby="t-ubica">
    <div class="foto">{foto(a, 'casa-balcon-pueblo', lang, 'ubica')}</div>
    <div>
      <p class="rotulo">{('Cómo llegar','Getting here')[k]}</p>
      <h2 class="display" id="t-ubica">Marlin 18, Sayulita</h2>
      <p>{('En pleno centro, pero en una calle tranquila. Todo lo que hay que ver del pueblo está a pie desde la puerta.','Right in the centre, but on a quiet street. Everything worth seeing in town is walkable from the door.')[k]}</p>
      <div class="distancias">
{distancias}
      </div>
      <a class="liga" href="{url(lang,'contacto',prof)}">{('Ver indicaciones','See directions')[k]}</a>
    </div>
  </section>

  <section class="cierre" id="casa-completa">
    <img class="mono" src="{a}monograma-moc.png" width="272" height="130" alt="" loading="lazy">
    <h2 class="display">{('¿Vienen todos?','Bringing everyone?')[k]}</h2>
    <p>{TEXTOS['index']['comp_p'][k]}</p>
    <a class="boton" href="{url(lang,'contacto',prof)}">{('Consultar la casa completa','Ask about the whole house')[k]}</a>
  </section>

</main>

<div class="visor" id="visor" aria-hidden="true">
  <button class="cerrar-visor" aria-label="{('Cerrar imagen','Close image')[k]}">&#10005;</button>
  <img src="" alt="">
</div>
""" + pie(lang, prof))

# ---------------------------------------------------------------- reservar

def pagina_reservar(lang):
    t = T[lang]; k = i(lang); prof = 0
    titulo = ('Reservar — Mi Otra Casa, Sayulita','Book — Mi Otra Casa, Sayulita')[k]
    desc = ('Consulta disponibilidad y reserva directo en Mi Otra Casa, Sayulita. Tarifas directas con desayuno incluido.',
            'Check availability and book direct at Mi Otra Casa, Sayulita. Direct rates with breakfast included.')[k]
    opciones = '\n'.join(f'            <option value="{s["slug"]}">{s["nombre"]} — ${s["precio"]} USD</option>' for s in SUITES)
    return (cabeza(lang, titulo, desc, 'reservar', prof)
      + barra(lang, 'reservar', prof)
      + f'''
<main id="contenido">

  <section class="limite" style="padding-block:var(--seccion) 0;max-width:720px;text-align:center">
    <p class="rotulo">{t['destacado_ch']}</p>
    <h1 class="display" style="font-size:clamp(2rem,4.4vw,3.2rem);line-height:1.08;margin:1rem 0">{('Reserva directo con la casa','Book direct with the house')[k]}</h1>
    <p style="color:var(--texto)">{('Tarifa directa, desayuno incluido y sin comisión de plataformas. Te confirmamos disponibilidad el mismo día.','Direct rate, breakfast included and no platform commission. We confirm availability the same day.')[k]}</p>
  </section>

  <div class="form-envoltura">
    <form class="formulario" id="form-reserva" method="post" action="https://formspree.io/f/REEMPLAZAR">
      <div class="fila">
        <p class="campo"><label for="llegada">{('Llegada','Check-in')[k]}</label>
          <input type="date" id="llegada" name="llegada" required></p>
        <p class="campo"><label for="salida">{('Salida','Check-out')[k]}</label>
          <input type="date" id="salida" name="salida" required></p>
      </div>
      <div class="fila">
        <p class="campo"><label for="adultos">{('Adultos','Adults')[k]}</label>
          <select id="adultos" name="adultos">
            <option>1</option><option selected>2</option><option>3</option><option>4</option>
          </select></p>
        <p class="campo"><label for="suite">{('Suite','Suite')[k]}</label>
          <select id="suite" name="suite">
            <option value="">{('Sin preferencia','No preference')[k]}</option>
{opciones}
          </select></p>
      </div>
      <div class="fila">
        <p class="campo"><label for="nombre">{('Nombre completo','Full name')[k]}</label>
          <input type="text" id="nombre" name="nombre" required autocomplete="name" placeholder=" "></p>
        <p class="campo"><label for="correo">{('Correo','Email')[k]}</label>
          <input type="email" id="correo" name="correo" required autocomplete="email" placeholder=" "></p>
      </div>
      <p class="campo"><label for="telefono">{('Teléfono o WhatsApp','Phone or WhatsApp')[k]}</label>
        <input type="tel" id="telefono" name="telefono" autocomplete="tel" placeholder=" "></p>
      <p class="campo"><label for="mensaje">{('Algo que debamos saber','Anything we should know')[k]}</label>
        <textarea id="mensaje" name="mensaje" rows="4" placeholder=" "></textarea></p>
      <p class="casilla"><input type="checkbox" id="acepto" name="acepto" required>
        <label for="acepto">{('He leído el','I have read the')[k]} <a href="{url(lang,'privacidad',prof)}" style="border-bottom:1px solid var(--filete)">{t['nav_privacidad'].lower()}</a> {('y las','and the')[k]} <a href="{url(lang,'politicas',prof)}" style="border-bottom:1px solid var(--filete)">{t['nav_politicas'].lower()}</a>.</label></p>
      <button class="boton" type="submit">{('Enviar solicitud','Send request')[k]}</button>
      <p class="ayuda">{('Esto es una solicitud, no un cargo: no se pide tarjeta en este paso.','This is a request, not a charge: no card details at this stage.')[k]}</p>
    </form>

    <aside class="resumen">
      <h2>{('Tu estancia','Your stay')[k]}</h2>
      <dl>
        <div><dt>{('Llegada','Check-in')[k]}</dt><dd id="r-llegada">—</dd></div>
        <div><dt>{('Salida','Check-out')[k]}</dt><dd id="r-salida">—</dd></div>
        <div><dt>{('Noches','Nights')[k]}</dt><dd id="r-noches">—</dd></div>
        <div><dt>{('Suite','Suite')[k]}</dt><dd id="r-suite">—</dd></div>
      </dl>
      <p class="nota" id="r-aviso">{('Mínimo dos noches, tres en temporada alta y puentes.','Two-night minimum, three in high season and holiday weekends.')[k]}</p>
      <p class="nota">{('¿Prefieres escribirnos? ','Rather write to us? ')[k]}<a href="mailto:contact@miotracasa.mx" style="border-bottom:1px solid var(--filete)">contact@miotracasa.mx</a></p>
    </aside>
  </div>

  <section class="cierre">
    <h2 class="display">{('La casa completa','The whole house')[k]}</h2>
    <p>{('Para catorce personas, con jardín, alberca y cocina. Las fechas de casa completa se cotizan aparte.','For fourteen people, with a garden, a pool and a kitchen. Whole-house dates are quoted separately.')[k]}</p>
    <a class="boton" href="{url(lang,'contacto',prof)}">{('Escribir a la casa','Write to the house')[k]}</a>
  </section>

</main>
''' + pie(lang, prof))

# ---------------------------------------------------------------- contacto

def pagina_contacto(lang):
    t = T[lang]; k = i(lang); prof = 0
    titulo = ('Contacto y cómo llegar — Mi Otra Casa, Sayulita','Contact and directions — Mi Otra Casa, Sayulita')[k]
    desc = ('Marlin 18, Sayulita, Nayarit. Cómo llegar desde el aeropuerto de Puerto Vallarta, dónde estacionarse y cómo escribirnos.',
            'Marlin 18, Sayulita, Nayarit. How to get here from Puerto Vallarta airport, where to park and how to reach us.')[k]
    mapa = 'https://www.google.com/maps?q=20.86830,-105.44066&z=16&hl=' + lang + '&output=embed'
    llegar = ([('Desde el aeropuerto de Puerto Vallarta','Unos 45 minutos en coche. Hay taxis autorizados en la terminal y servicios de traslado privado que podemos reservar por ti.'),
               ('En coche','Por la carretera federal 200 hacia el norte. Sayulita tiene una sola entrada; al llegar al centro, Marlin cruza a media cuadra de la plaza.'),
               ('Estacionamiento','La casa tiene dos cajones techados y dos sobre la calle. El centro de Sayulita es angosto, así que conviene avisarnos tu hora de llegada.'),
               ('Dentro del pueblo','Todo está a pie. Para San Pancho o Punta Mita hay camionetas que salen de la entrada del pueblo.')],
              [('From Puerto Vallarta airport','About 45 minutes by car. There are authorised taxis at the terminal, and private transfers we can arrange for you.'),
               ('By car','Take federal highway 200 north. Sayulita has a single entrance; once in the centre, Marlin crosses half a block from the plaza.'),
               ('Parking','The house has two covered spaces and two on the street. Sayulita’s streets are narrow, so let us know your arrival time.'),
               ('Around town','Everything is walkable. For San Pancho or Punta Mita, shared vans leave from the entrance of town.')])[k]
    llegar_html = '\n'.join(f'''      <div><dt>{a}</dt><dd>{b}</dd></div>''' for a, b in llegar)
    return (cabeza(lang, titulo, desc, 'contacto', prof)
      + barra(lang, 'contacto', prof)
      + f'''
<main id="contenido">

  <section class="limite" style="padding-block:var(--seccion) var(--seccion-corta);max-width:720px;text-align:center">
    <p class="rotulo">{t['nav_contacto']}</p>
    <h1 class="display" style="font-size:clamp(2rem,4.4vw,3.2rem);line-height:1.08;margin:1rem 0">{('Marlin 18, Sayulita','Marlin 18, Sayulita')[k]}</h1>
    <p style="color:var(--texto)">{('A media cuadra de la plaza y a tres del mar, en una calle tranquila del centro.','Half a block from the plaza and three from the sea, on a quiet street in the centre.')[k]}</p>
  </section>

  <div class="limite">
    <div class="mapa-caja" id="mapa-caja">
      <iframe class="mapa" src="{mapa}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{('Mapa de Mi Otra Casa','Map of Mi Otra Casa')[k]}"></iframe>
      <button class="mapa-activar" type="button">{('Activar el mapa','Activate map')[k]}</button>
    </div>
    <p class="mapa-pie"><a class="liga" href="https://www.google.com/maps/search/?api=1&query=20.86830%2C-105.44066" rel="noopener">{('Abrir en Google Maps','Open in Google Maps')[k]}</a></p>
  </div>

  <div class="form-envoltura">
    <div>
      <h2 class="display" style="font-size:clamp(1.6rem,3vw,2.3rem);margin-bottom:1.5rem">{('Cómo llegar','Getting here')[k]}</h2>
      <dl class="tabla-politicas" style="padding:0">
{llegar_html}
      </dl>
    </div>
    <aside class="resumen">
      <h2>{('Escríbenos','Write to us')[k]}</h2>
      <div class="contacto-datos">
        <div><h3>{('Correo','Email')[k]}</h3><p><a href="mailto:contact@miotracasa.mx">contact@miotracasa.mx</a></p></div>
        <div><h3>{('Reservas','Reservations')[k]}</h3><p><a href="{url(lang,'reservar',prof)}">{t['destacado_t']}</a></p></div>
        <div><h3>{('Dirección','Address')[k]}</h3><p>Calle Marlin 18<br>63734 Sayulita, Nayarit<br>México</p></div>
        <div><h3>{('Recepción','Front desk')[k]}</h3><p>{('Llegada de 16:00 a 19:00. La puerta abre con código, que te enviamos el día anterior; si llegas fuera de ese horario, escríbenos y lo coordinamos.','Check-in from 4 to 7 pm. The door opens with a code we send the day before; if you arrive outside those hours, write to us and we will coordinate.')[k]}</p></div>
      </div>
    </aside>
  </div>

</main>
''' + pie(lang, prof))

# ---------------------------------------------------------------- políticas y privacidad

def pagina_politicas(lang):
    t = T[lang]; k = i(lang); prof = 0
    filas = ([('Llegada y salida','Llegada de 16:00 a 19:00. Salida antes de las 11:00. La llegada anticipada o tardía está sujeta a disponibilidad; avísanos con tiempo y la acomodamos.'),
              ('Solo adultos','La casa recibe únicamente a mayores de 21 años. No es un hotel para niños ni adolescentes, y preferimos decirlo antes de que reserves.'),
              ('Entrada con código','La puerta principal abre con clave, que enviamos el día anterior. Si tu vuelo llega tarde, escríbenos y coordinamos la llegada.'),
              ('Mínimo de noches','Dos noches en temporada regular. Tres noches en temporada alta, puentes y fin de año.'),
              ('Cancelación','Sin costo hasta 7 días antes de la llegada. Después de ese plazo se retiene el importe de la primera noche.'),
              ('Formas de pago','American Express, Visa, Mastercard y Diners Club, además de transferencia. Las tarifas están en dólares y se cobran al tipo de cambio del día.'),
              ('Depósito en garantía','Se solicita un depósito reembolsable antes de la llegada, que se libera al salir si no hubo daños. (Monto por confirmar con la casa.)'),
              ('Desayuno','Incluido en la tarifa, para dos personas por suite, de 8:00 a 11:00.'),
              ('Alberca','Abierta de 8:00 a medianoche, con camastros, sombrillas y cabañas sin costo.'),
              ('Mascotas','No recibimos mascotas ni animales de servicio, por higiene y por el descanso de los demás huéspedes.'),
              ('Sin humo','La casa entera es libre de humo. No se fuma dentro de las suites ni en las áreas comunes.'),
              ('Accesibilidad','La casa tiene tres niveles y no cuenta con elevador. Luna es la única suite sin escaleras de por medio.'),
              ('Silencio','A partir de las 22:00 se cuida el ruido en las áreas comunes. Es una casa, no un salón de fiestas.'),
              ('El pueblo de noche','Sayulita tiene vida nocturna y en temporada alta la música se escucha hasta la madrugada. Las suites interiores dan al jardín y son las más resguardadas; en todas dejamos tapones y ruido blanco. Si viajas con el sueño ligero, dínoslo al reservar y te acomodamos en la más tranquila disponible.'),
              ('Casa completa','Las reservas de la casa entera se cotizan aparte y tienen condiciones propias de anticipo y cancelación.')],
             [('Check-in and check-out','Check-in from 4 to 7 pm. Check-out before 11 am. Early and late check-in are subject to availability; let us know ahead and we will arrange it.'),
              ('Adults only','The house welcomes guests aged 21 and over only. It is not a hotel for children or teenagers, and we would rather say so before you book.'),
              ('Keypad entry','The main door opens with a code we send the day before. If your flight lands late, write to us and we will coordinate your arrival.'),
              ('Minimum stay','Two nights in regular season. Three nights in high season, holiday weekends and over New Year.'),
              ('Cancellation','Free until 7 days before arrival. After that, the first night is retained.'),
              ('Payment','American Express, Visa, Mastercard and Diners Club, as well as bank transfer. Rates are in US dollars and charged at the day\u2019s exchange rate.'),
              ('Security deposit','A refundable deposit is requested before arrival and released on check-out if there is no damage. (Amount to be confirmed with the house.)'),
              ('Breakfast','Included in the rate, for two people per suite, from 8 to 11 am.'),
              ('Pool','Open from 8 am to midnight, with loungers, umbrellas and cabanas at no charge.'),
              ('Pets','We do not accept pets or service animals, for hygiene and for the rest of our other guests.'),
              ('Smoking','The whole property is smoke-free, inside the suites and in the shared areas.'),
              ('Accessibility','The house has three floors and no lift. Luna is the only suite reached without stairs.'),
              ('Quiet hours','From 10 pm we keep noise down in the shared areas. This is a house, not a party venue.'),
              ('The town at night','Sayulita has nightlife, and in high season the music carries into the early hours. The interior suites face the garden and are the most sheltered; every room has earplugs and a white-noise machine. If you are a light sleeper, tell us when booking and we will put you in the quietest room available.'),
              ('Whole house','Whole-house bookings are quoted separately and have their own deposit and cancellation terms.')])[k]
    html_filas = '\n'.join(f'''    <div><dt>{a}</dt><dd>{b}</dd></div>''' for a, b in filas)
    return (cabeza(lang, ('Políticas — Mi Otra Casa','Policies — Mi Otra Casa')[k],
                   ('Horarios de llegada y salida, mínimo de noches, cancelación, formas de pago y políticas de la casa.',
                    'Check-in and check-out times, minimum stay, cancellation, payment methods and house policies.')[k],
                   'politicas', prof)
      + barra(lang, 'politicas', prof)
      + f'''
<main id="contenido">
  <section class="limite" style="padding-block:var(--seccion) var(--seccion-corta);max-width:720px;text-align:center">
    <p class="rotulo">{t['nav_politicas']}</p>
    <h1 class="display" style="font-size:clamp(2rem,4.4vw,3.2rem);line-height:1.08;margin:1rem 0">{('Lo que conviene saber antes de reservar','What to know before you book')[k]}</h1>
    <p style="color:var(--texto)">{('Sin letra chica: esto es todo lo que aplica a cualquier reserva.','No small print: this is everything that applies to any booking.')[k]}</p>
  </section>
  <dl class="tabla-politicas">
{html_filas}
  </dl>
  <section class="cierre">
    <h2 class="display">{('¿Alguna duda?','Any questions?')[k]}</h2>
    <p>{('Escríbenos antes de reservar. Contestamos el mismo día.','Write to us before booking. We answer the same day.')[k]}</p>
    <a class="boton" href="{url(lang,'contacto',prof)}">{t['nav_contacto']}</a>
  </section>
</main>
''' + pie(lang, prof))

def pagina_privacidad(lang):
    t = T[lang]; k = i(lang); prof = 0
    cuerpo = ([
      ('Responsable','Mi Otra Casa, con domicilio en Calle Marlin 18, Sayulita, Nayarit, México, es responsable del tratamiento de tus datos personales.'),
      ('Qué datos recabamos','Nombre, correo electrónico, teléfono, fechas de estancia y los datos que nos compartas en el mensaje del formulario.'),
      ('Para qué los usamos','Para responder tu solicitud de reserva, confirmar disponibilidad, prestarte el servicio de hospedaje y, si lo autorizas, enviarte promociones de la casa.'),
      ('Con quién los compartimos','No vendemos ni compartimos tus datos con terceros, salvo con los proveedores necesarios para operar la reserva, que están obligados a protegerlos.'),
      ('Tus derechos','Puedes acceder, rectificar, cancelar u oponerte al tratamiento de tus datos, así como revocar tu consentimiento, escribiendo a contact@miotracasa.mx.'),
      ('Cambios','Cualquier modificación a este aviso se publicará en esta misma página.'),
      ('Pendiente de revisión legal','Este texto es un borrador base. Antes de publicarlo debe revisarlo un abogado para cumplir con la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.'),
    ], [
      ('Data controller','Mi Otra Casa, at Calle Marlin 18, Sayulita, Nayarit, Mexico, is responsible for the processing of your personal data.'),
      ('What we collect','Name, email address, phone number, stay dates and whatever you choose to tell us in the form message.'),
      ('Why we use it','To answer your booking request, confirm availability, provide the accommodation and, if you agree to it, send you offers from the house.'),
      ('Who we share it with','We do not sell or share your data with third parties, except the providers needed to run the booking, who are bound to protect it.'),
      ('Your rights','You may access, correct, delete or object to the processing of your data, and withdraw consent, by writing to contact@miotracasa.mx.'),
      ('Changes','Any change to this notice will be published on this page.'),
      ('Pending legal review','This is a working draft. Before publication it must be reviewed by a lawyer to comply with Mexican data protection law.'),
    ])[k]
    filas = '\n'.join(f'''    <div><dt>{a}</dt><dd>{b}</dd></div>''' for a, b in cuerpo)
    return (cabeza(lang, (t['nav_privacidad'] + ' — Mi Otra Casa'),
                   ('Cómo tratamos los datos personales de quienes escriben o reservan en Mi Otra Casa.',
                    'How we handle the personal data of anyone who writes to or books at Mi Otra Casa.')[k],
                   'privacidad', prof)
      + barra(lang, 'privacidad', prof)
      + f'''
<main id="contenido">
  <section class="limite" style="padding-block:var(--seccion) var(--seccion-corta);max-width:720px;text-align:center">
    <p class="rotulo">{('Legal','Legal')[k]}</p>
    <h1 class="display" style="font-size:clamp(2rem,4.4vw,3.2rem);line-height:1.08;margin:1rem 0">{t['nav_privacidad']}</h1>
  </section>
  <dl class="tabla-politicas">
{filas}
  </dl>
</main>
''' + pie(lang, prof))

# ---------------------------------------------------------------- 404 y sitemap

def pagina_404():
    r = RAIZ_WEB
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada — Mi Otra Casa</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{r}assets/favicon-32.png" sizes="32x32">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body>
<main id="contenido" class="cierre" style="min-height:100svh;display:grid;align-content:center;border:none">
  <img class="mono" src="{r}assets/monograma-moc.png" width="272" height="130" alt="Mi Otra Casa">
  <h1 class="display" style="font-size:clamp(1.85rem,3.6vw,2.8rem);margin-bottom:1rem">Esta página no existe<br><span style="font-size:.6em">This page does not exist</span></h1>
  <p>Desde el inicio llegas a todo lo demás. / Everything else is one click from the home page.</p>
  <a class="boton" href="{r}">Inicio / Home</a>
</main>
</body>
</html>
'''

def sitemap():
    urls = []
    for lang in L:
        p = '' if lang == 'es' else 'en/'
        for clave in ('index','suites','casa','reservar','contacto','politicas','privacidad'):
            ruta = RUTAS[lang][clave].replace('index.html','')
            urls.append(f'{DOMINIO}/{p}{ruta}')
        for s in SUITES:
            urls.append(f'{DOMINIO}/{p}{RUTAS[lang]["suite"](s["slug"])}')
    cuerpo = '\n'.join(f'  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>' for u in urls)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{cuerpo}
</urlset>
'''

# ---------------------------------------------------------------- main

def main():
    hechas = []
    for lang in L:
        pre = '' if lang == 'es' else 'en/'
        hechas.append(escribir(pre + RUTAS[lang]['index'], pagina_index(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['suites'], pagina_suites(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['casa'], pagina_casa(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['reservar'], pagina_reservar(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['contacto'], pagina_contacto(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['politicas'], pagina_politicas(lang)))
        hechas.append(escribir(pre + RUTAS[lang]['privacidad'], pagina_privacidad(lang)))
        for s in SUITES:
            hechas.append(escribir(pre + RUTAS[lang]['suite'](s['slug']), pagina_suite(lang, s)))
    hechas.append(escribir('404.html', pagina_404()))
    hechas.append(escribir('sitemap.xml', sitemap()))
    hechas.append(escribir('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n'))
    print(f'{len(hechas)} archivos')
    for h in hechas: print('  ', h)

if __name__ == '__main__':
    main()
