/* =========================================================
   Mi Otra Casa — comportamiento del sitio
   Todo es progresivo: sin JS la página sigue siendo legible.
   ========================================================= */
(function () {
  'use strict';

  var menosMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- menú lateral ---------- */
  var cortina = document.getElementById('cortina');
  if (cortina) {
    var abrir = document.getElementById('abrir');
    var cerrar = document.getElementById('cerrar');
    var velo = cortina.querySelector('.velo');
    var panel = cortina.querySelector('.panel');
    var ultimoFoco = null;

    var enfocables = function () {
      return panel.querySelectorAll('a[href], button:not([disabled])');
    };

    var abrirMenu = function () {
      ultimoFoco = document.activeElement;
      cortina.classList.add('abierta');
      cortina.removeAttribute('aria-hidden');
      abrir.setAttribute('aria-expanded', 'true');
      document.body.classList.add('sin-scroll');
      window.setTimeout(function () { cerrar.focus(); }, menosMovimiento ? 0 : 380);
    };

    var cerrarMenu = function () {
      cortina.classList.remove('abierta');
      cortina.setAttribute('aria-hidden', 'true');
      abrir.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('sin-scroll');
      if (ultimoFoco) { ultimoFoco.focus(); }
    };

    abrir.addEventListener('click', abrirMenu);
    cerrar.addEventListener('click', cerrarMenu);
    velo.addEventListener('click', cerrarMenu);
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', cerrarMenu);
    });

    // el foco no se sale del panel mientras está abierto
    cortina.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { cerrarMenu(); return; }
      if (e.key !== 'Tab') { return; }
      var lista = enfocables();
      if (!lista.length) { return; }
      var primero = lista[0], ultimo = lista[lista.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    });
  }

  /* ---------- video de portada ---------- */
  var video = document.getElementById('video');
  var control = document.getElementById('control');
  if (video && control) {
    var PAUSA = '&#10073;&#10073;', PLAY = '&#9654;';

    var pintar = function () {
      var pausado = video.paused;
      control.innerHTML = pausado ? PLAY : PAUSA;
      control.setAttribute('aria-label', pausado ? 'Reproducir video' : 'Pausar video');
    };

    control.addEventListener('click', function () {
      if (video.paused) { video.play(); } else { video.pause(); }
      pintar();
    });

    if (menosMovimiento) { video.pause(); }

    // no gastar batería ni datos con el video fuera de pantalla
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (e.isIntersecting) {
            if (!video.dataset.pausadoAMano && !menosMovimiento) { video.play().catch(function () {}); }
          } else if (!video.paused) {
            video.pause();
          }
          pintar();
        });
      }, { threshold: 0.15 }).observe(video);
    }

    control.addEventListener('click', function () {
      video.dataset.pausadoAMano = video.paused ? '1' : '';
    });

    video.addEventListener('play', pintar);
    video.addEventListener('pause', pintar);
    pintar();
  }

  /* ---------- filtros de suites ---------- */
  var filtros = document.getElementById('filtros');
  if (filtros) {
    var botones = filtros.querySelectorAll('button');
    var suites = document.querySelectorAll('.suite');
    var aviso = document.getElementById('sin-resultados');

    botones.forEach(function (b) {
      b.addEventListener('click', function () {
        var tipo = b.dataset.tipo;
        botones.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        var visibles = 0;
        suites.forEach(function (c) {
          var mostrar = (tipo === 'todas' || c.dataset.tipo === tipo);
          c.hidden = !mostrar;
          if (mostrar) { visibles++; }
        });
        if (aviso) { aviso.hidden = visibles > 0; }
      });
    });
  }

  /* ---------- visor de galería ---------- */
  var visor = document.getElementById('visor');
  if (visor) {
    var visorImg = visor.querySelector('img');
    var cerrarVisor = visor.querySelector('.cerrar-visor');
    var focoPrevio = null;

    document.querySelectorAll('#galeria figure').forEach(function (fig) {
      fig.setAttribute('role', 'button');
      fig.setAttribute('tabindex', '0');
      var abrirVisor = function () {
        var im = fig.querySelector('img');
        focoPrevio = document.activeElement;
        visorImg.src = im.dataset.grande || im.currentSrc || im.src;
        visorImg.alt = im.alt;
        visor.classList.add('abierto');
        visor.removeAttribute('aria-hidden');
        document.body.classList.add('sin-scroll');
        cerrarVisor.focus();
      };
      fig.addEventListener('click', abrirVisor);
      fig.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrirVisor(); }
      });
    });

    var ocultarVisor = function () {
      visor.classList.remove('abierto');
      visor.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('sin-scroll');
      if (focoPrevio) { focoPrevio.focus(); }
    };
    cerrarVisor.addEventListener('click', ocultarVisor);
    visor.addEventListener('click', function (e) { if (e.target !== visorImg) { ocultarVisor(); } });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && visor.classList.contains('abierto')) { ocultarVisor(); }
    });
  }

  /* ---------- apariciones al entrar en pantalla ---------- */
  var reveladas = document.querySelectorAll('.rev');
  if (reveladas.length) {
    if (!('IntersectionObserver' in window) || menosMovimiento) {
      reveladas.forEach(function (el) { el.classList.add('vista'); });
    } else {
      var obs = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('vista'); obs.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -10% 0px' });
      reveladas.forEach(function (el) { obs.observe(el); });
    }
  }
})();

/* ---------- resumen del formulario de reserva ---------- */
(function () {
  'use strict';
  var form = document.getElementById('form-reserva');
  if (!form) { return; }

  var llegada = form.llegada, salida = form.salida, suite = form.suite;
  var rL = document.getElementById('r-llegada'), rS = document.getElementById('r-salida');
  var rN = document.getElementById('r-noches'), rSu = document.getElementById('r-suite');
  var idioma = document.documentElement.lang === 'en' ? 'en' : 'es';
  var hoy = new Date().toISOString().slice(0, 10);
  llegada.min = hoy;
  salida.min = hoy;

  // suite preseleccionada desde ?suite=slug
  var q = new URLSearchParams(location.search).get('suite');
  if (q) {
    Array.prototype.forEach.call(suite.options, function (o) {
      if (o.value === q) { suite.value = q; }
    });
  }

  var fmt = function (v) {
    if (!v) { return '—'; }
    var d = new Date(v + 'T12:00:00');
    return d.toLocaleDateString(idioma === 'en' ? 'en-GB' : 'es-MX',
      { day: 'numeric', month: 'short', year: 'numeric' });
  };

  var pintar = function () {
    rL.textContent = fmt(llegada.value);
    rS.textContent = fmt(salida.value);
    rSu.textContent = suite.selectedIndex > 0 ? suite.options[suite.selectedIndex].text.split(' — ')[0]
                                              : (idioma === 'en' ? 'No preference' : 'Sin preferencia');
    if (llegada.value && salida.value) {
      var n = Math.round((new Date(salida.value) - new Date(llegada.value)) / 86400000);
      rN.textContent = n > 0 ? n + (idioma === 'en' ? (n === 1 ? ' night' : ' nights')
                                                     : (n === 1 ? ' noche' : ' noches')) : '—';
      salida.setCustomValidity(n > 0 ? '' :
        (idioma === 'en' ? 'Check-out must be after check-in' : 'La salida debe ser posterior a la llegada'));
    } else {
      rN.textContent = '—';
    }
  };

  llegada.addEventListener('change', function () {
    var d = new Date(llegada.value + 'T12:00:00');
    d.setDate(d.getDate() + 1);
    salida.min = d.toISOString().slice(0, 10);
    if (salida.value && salida.value <= llegada.value) { salida.value = ''; }
    pintar();
  });
  salida.addEventListener('change', pintar);
  suite.addEventListener('change', pintar);
  pintar();
})();

/* ---------- el mapa no captura el scroll hasta que se activa ---------- */
(function () {
  'use strict';
  var caja = document.getElementById('mapa-caja');
  if (!caja) { return; }
  caja.querySelector('.mapa-activar').addEventListener('click', function () {
    caja.classList.add('activo');
  });
})();
