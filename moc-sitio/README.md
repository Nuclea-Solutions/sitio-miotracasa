# Mi Otra Casa — sitio

Sitio estático bilingüe de Mi Otra Casa, hotel boutique en Sayulita, Nayarit.
Sin dependencias ni empaquetadores: se publica tal cual con GitHub Pages.

## Estructura
    index.html            portada            en/index.html
    suites.html           las siete suites   en/suites.html
    suites/<slug>.html    página por suite   en/suites/<slug>.html
    casa.html             la casa            en/house.html
    reservar.html         solicitud          en/booking.html
    contacto.html         contacto y mapa    en/contact.html
    politicas.html        políticas          en/policies.html
    privacidad.html       aviso legal        en/privacy.html
    404.html  robots.txt  sitemap.xml
    assets/   site.css, site.js, imágenes, video, logos

El español vive en la raíz y el inglés bajo `/en/`. Cada página declara
`hreflang` y su canónica, así que Google indexa las dos versiones por separado.

## Regenerar
Las páginas se generan con `pages.py` (contenido y plantillas) y `build.py`
(datos, rutas y chrome compartido). Para cambiar un precio o un texto se edita
el dato en `build.py` y se corre:

    python3 pages.py

## Publicar con GitHub Pages
1. Subir el contenido de esta carpeta a la raíz del repositorio.
2. Settings → Pages → Source: *Deploy from a branch* → `main`, carpeta `/ (root)`.
3. Dominio propio: Settings → Pages → Custom domain → `miotracasa.mx`,
   y apuntar en el DNS los registros A de GitHub Pages.

## Antes de publicar — pendientes reales

### Decisiones que necesita MOC
- **Formulario**: `reservar.html` apunta a `https://formspree.io/f/REEMPLAZAR`.
  Crear la cuenta y poner el endpoint, o conectar el motor de reservas.
- **Reseñas**: los puntajes ya son reales (Expedia 9.6, Hotels.com 9.4, 4.8/5 de 107
  reseñas). Faltan los tres textos: deben ser reseñas reales con permiso del huésped.
- **Ofertas**: las tres de la portada son de ejemplo. Confirmar o quitarlas.
- **Imágenes**: en pausa, se están editando. Las de las suites se cargan todavía
  desde `miotracasa.mx/images/...`; al tenerlas, copiarlas a `assets/`, generar WebP
  y varios tamaños con `srcset`.
- **Video**: el de portada salió de un archivo de WhatsApp (832×464). Reemplazar con
  el original del dron y generar una versión vertical para móvil.

### Contradicciones detectadas entre el sitio y las plataformas
- **Desayuno**: el sitio dice incluido; Expedia lo lista con cargo. Hay que unificarlo
  en todos los canales, porque genera reclamaciones en recepción.
- **WiFi**: el sitio dice en toda la casa; Expedia registra WiFi gratis solo en áreas
  comunes e internet por cable con cargo.
- **Estacionamiento**: el sitio dice dos cajones techados; las plataformas dicen
  estacionamiento descubierto, limitado y bajo petición.
- **Número de habitaciones**: en todos lados son 7, pero el listado de tipos incluye
  un octavo, "08 MOC Ocean View". Definir si existe y si debe aparecer en el sitio.
- **Depósito en garantía**: las plataformas publican 2,100 USD por estancia. En el
  sitio quedó sin monto hasta confirmarlo; si la cifra es correcta conviene explicarla
  bien, porque a ese nivel asusta a quien reserva directo.
- **Metros de cada suite**: el listado viejo y las páginas individuales no coinciden.

### Legal y medición
- **Aviso de privacidad**: borrador base. Debe revisarlo un abogado antes de publicar.
- **Analítica**: falta instalar medición y dar de alta el sitio en Search Console.
- **Licencias**: verificar derechos de las fotos de Sayulita (surf, tortugas, plaza, calles).

### Datos ya corregidos con la información de las plataformas
Llegada de 16:00 a 19:00 y salida a las 11:00; edad mínima 21 años; alberca de 8:00 a
medianoche; bar junto a la alberca, spa, sala de juegos, guarda equipaje, microondas y
refrigerador compartidos; tres niveles sin elevador; pago con Diners Club además de
Amex, Visa y Mastercard; coordenadas reales en el mapa y en los datos estructurados.
