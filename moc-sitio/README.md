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

Escribe las páginas en esta misma carpeta. No se editan los HTML a mano: cualquier
cambio hecho directo en un HTML se pierde en la siguiente regeneración.

## Fotos
Viven en `assets/fotos/<nombre>-<ancho>.jpg` y `.webp` (JPEG progresivo y WebP,
calidad 75). Las de tarjeta van en 600 y 1200 px; las de portada en 1200 y su ancho
original, hasta 1800. Las páginas las sirven con `<picture>` y `srcset`, y los anchos
disponibles se leen del disco al regenerar.

Para agregar o cambiar una foto:
1. Darla de alta en la lista `CAT` de `fotos.py` con su nombre y su uso
   (`c` tarjeta, `h` portada, `hc` ambos) y correr
   `python3 fotos.py "<carpeta de originales>" assets/fotos` (necesita Pillow).
2. Agregar su texto alternativo en `FOTOS` de `build.py` y usarla en `pages.py`
   o en `fotos=` de la suite. Si es vertical y la retícula la recorta, su encuadre
   va en `FOCO`.
3. `python3 pages.py`.

## Publicar con GitHub Pages
1. Subir el contenido de esta carpeta a la raíz del repositorio.
2. Settings → Pages → Source: *Deploy from a branch* → `main`, carpeta `/ (root)`.
3. Dominio propio: Settings → Pages → Custom domain → `miotracasa.mx`,
   y apuntar en el DNS los registros A de GitHub Pages.

## Antes de publicar — pendientes reales

### Decisiones que necesita MOC
- **Formulario**: `reservar.html` apunta a `https://formspree.io/f/REEMPLAZAR`.
  Crear la cuenta y poner el endpoint, o conectar el motor de reservas.
- **Reseñas**: las tres publicadas son reales (TripAdvisor, Hotels.com, Trip.com),
  sin nombre y con enlace a la fuente. No escribir reseñas nuevas.
- **Ofertas**: se quitaron a propósito; las promociones no están autorizadas. En su
  lugar va «La casa, de un vistazo».
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
