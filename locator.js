/* ==========================================================================
   Kappa League Program Locator
   Dependencies: Leaflet 1.9.x (map only). Everything else is vanilla.
   Data source: assets/data/chapters.json  (SAMPLE DATA — replace before launch)

   Swap points for production:
     CONFIG.dataUrl      -> live chapter feed (same JSON shape)
     CONFIG.geocode      -> your geocoding provider
     CONFIG.tileUrl      -> Mapbox/Google/Esri tiles if you move off OSM
     submitApplication() -> POST to your application endpoint
     submitInquiry()     -> POST to your chapter-routing endpoint
   ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('locator');
  if (!root) return;

  var CONFIG = {
    dataUrl: root.getAttribute('data-source') || 'assets/data/chapters.json',
    tileUrl: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    tileAttribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    defaultRadius: 25,
    defaultCenter: [39.5, -98.35],
    defaultZoom: 4
  };

  /* Offline-safe centroids: every sample chapter ZIP plus common metros.
     Anything not listed falls through to the network geocoder below. */
  var PLACES = {
    '76201': [33.2148, -97.1331], '75215': [32.7767, -96.7970], '76104': [32.7555, -97.3308],
    '77004': [29.7604, -95.3698], '78702': [30.2672, -97.7431], '30303': [33.7490, -84.3880],
    '35203': [33.5186, -86.8104], '38104': [35.1495, -90.0490], '70112': [29.9511, -90.0715],
    '60653': [41.8781, -87.6298], '63103': [38.6270, -90.1994], '64108': [39.0997, -94.5786],
    '48202': [42.3314, -83.0458], '46202': [39.7684, -86.1581], '43215': [39.9612, -82.9988],
    '20001': [38.9072, -77.0369], '19107': [39.9526, -75.1652], '28202': [35.2271, -80.8431],
    '90008': [34.0522, -118.2437], '94612': [37.8044, -122.2711], '80205': [39.7392, -104.9903],
    'denton tx': [33.2148, -97.1331], 'dallas tx': [32.7767, -96.7970],
    'fort worth tx': [32.7555, -97.3308], 'houston tx': [29.7604, -95.3698],
    'austin tx': [30.2672, -97.7431], 'san antonio tx': [29.4241, -98.4936],
    'atlanta ga': [33.7490, -84.3880], 'birmingham al': [33.5186, -86.8104],
    'memphis tn': [35.1495, -90.0490], 'nashville tn': [36.1627, -86.7816],
    'new orleans la': [29.9511, -90.0715], 'jackson ms': [32.2988, -90.1848],
    'chicago il': [41.8781, -87.6298], 'st louis mo': [38.6270, -90.1994],
    'kansas city mo': [39.0997, -94.5786], 'minneapolis mn': [44.9778, -93.2650],
    'detroit mi': [42.3314, -83.0458], 'cleveland oh': [41.4993, -81.6944],
    'indianapolis in': [39.7684, -86.1581], 'columbus oh': [39.9612, -82.9988],
    'cincinnati oh': [39.1031, -84.5120], 'louisville ky': [38.2527, -85.7585],
    'washington dc': [38.9072, -77.0369], 'baltimore md': [39.2904, -76.6122],
    'philadelphia pa': [39.9526, -75.1652], 'pittsburgh pa': [40.4406, -79.9959],
    'new york ny': [40.7128, -74.0060], 'newark nj': [40.7357, -74.1724],
    'boston ma': [42.3601, -71.0589], 'charlotte nc': [35.2271, -80.8431],
    'raleigh nc': [35.7796, -78.6382], 'richmond va': [37.5407, -77.4360],
    'columbia sc': [34.0007, -81.0348], 'jacksonville fl': [30.3322, -81.6557],
    'orlando fl': [28.5383, -81.3792], 'miami fl': [25.7617, -80.1918],
    'tampa fl': [27.9506, -82.4572], 'los angeles ca': [34.0522, -118.2437],
    'oakland ca': [37.8044, -122.2711], 'san francisco ca': [37.7749, -122.4194],
    'san diego ca': [32.7157, -117.1611], 'sacramento ca': [38.5816, -121.4944],
    'denver co': [39.7392, -104.9903], 'phoenix az': [33.4484, -112.0740],
    'las vegas nv': [36.1699, -115.1398], 'seattle wa': [47.6062, -122.3321],
    'portland or': [45.5152, -122.6784], 'oklahoma city ok': [35.4676, -97.5164],
    'little rock ar': [34.7465, -92.2896], 'omaha ne': [41.2565, -95.9345],
    'milwaukee wi': [43.0389, -87.9065], 'tulsa ok': [36.1540, -95.9928]
  };

  /* ------------------------------------------------------------ dom handles */
  var el = {
    form:       document.getElementById('loc-form'),
    query:      document.getElementById('loc-query'),
    radius:     document.getElementById('loc-radius'),
    geo:        document.getElementById('loc-geo'),
    filters:    root.querySelectorAll('.pill'),
    results:    document.getElementById('loc-results'),
    list:       document.getElementById('loc-list'),
    count:      document.getElementById('loc-count'),
    map:        document.getElementById('loc-map'),
    viewBtns:   root.querySelectorAll('[data-view-btn]'),
    status:     document.getElementById('loc-status')
  };

  var state = {
    chapters: [],
    origin: null,
    originLabel: '',
    radius: CONFIG.defaultRadius,
    filters: { has_league: true, accepting: false, junior: false, senior: false },
    activeId: null,
    view: 'list'
  };

  var map = null;
  var markers = {};
  var originMarker = null;

  /* ----------------------------------------------------------------- utils */
  function announce(msg) { if (el.status) el.status.textContent = msg; }

  function miles(a, b) {
    var R = 3958.8, toRad = Math.PI / 180;
    var dLat = (b[0] - a[0]) * toRad;
    var dLng = (b[1] - a[1]) * toRad;
    var s = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(a[0] * toRad) * Math.cos(b[0] * toRad) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return R * 2 * Math.atan2(Math.sqrt(s), Math.sqrt(1 - s));
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function normalize(q) {
    return q.toLowerCase().trim().replace(/[.,]/g, '').replace(/\s+/g, ' ');
  }

  /* ------------------------------------------------------------- geocoding */
  function geocode(query) {
    var key = normalize(query);
    if (PLACES[key]) return Promise.resolve({ coords: PLACES[key], label: query.trim() });

    var zip = key.match(/^\d{5}$/);
    if (!zip && !/[a-z]/.test(key)) {
      return Promise.reject(new Error('Enter a 5-digit ZIP code or a city and state.'));
    }

    // Network fallback. Replace with your provider (Mapbox, Google, Smarty) in production.
    var url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q=' +
              encodeURIComponent(query);
    return fetch(url, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (json) {
        if (!json || !json.length) throw new Error('We could not find that location. Try a 5-digit ZIP code.');
        return {
          coords: [parseFloat(json[0].lat), parseFloat(json[0].lon)],
          label: query.trim()
        };
      });
  }

  /* ------------------------------------------------------------------- map */
  function initMap() {
    if (typeof L === 'undefined' || !el.map) return;
    map = L.map(el.map, { scrollWheelZoom: false, zoomControl: true })
           .setView(CONFIG.defaultCenter, CONFIG.defaultZoom);
    L.tileLayer(CONFIG.tileUrl, { attribution: CONFIG.tileAttribution, maxZoom: 18 }).addTo(map);
    map.on('click', function () { setActive(null); });
  }

  function pinIcon(active) {
    return L.divIcon({
      className: '',
      html: '<div class="pin' + (active ? ' pin--active' : '') + '"></div>',
      iconSize: [26, 26],
      iconAnchor: [13, 24],
      popupAnchor: [0, -22]
    });
  }

  function drawMarkers(list) {
    if (!map) return;
    Object.keys(markers).forEach(function (id) { map.removeLayer(markers[id]); });
    markers = {};

    list.forEach(function (c) {
      var m = L.marker([c.lat, c.lng], { icon: pinIcon(false), title: c.name, riseOnHover: true }).addTo(map);
      m.bindPopup(
        '<h4>' + esc(c.name) + '</h4>' +
        '<p>' + esc(c.city) + ', ' + esc(c.state) + (c.distance != null ? ' &middot; ' + c.distance.toFixed(1) + ' mi' : '') + '<br>' +
        esc(c.meets) + '</p>' +
        '<button type="button" class="btn btn--primary btn--sm" data-popup-apply="' + esc(c.id) + '">Apply to this Kappa League</button>'
      );
      m.on('click', function () { setActive(c.id, false); });
      markers[c.id] = m;
    });

    if (originMarker) { map.removeLayer(originMarker); originMarker = null; }
    if (state.origin) {
      originMarker = L.marker(state.origin, {
        icon: L.divIcon({ className: '', html: '<div class="pin pin--origin"></div>', iconSize: [18, 18], iconAnchor: [9, 9] }),
        title: 'Your search location',
        keyboard: false
      }).addTo(map);
    }

    var pts = list.map(function (c) { return [c.lat, c.lng]; });
    if (state.origin) pts.push(state.origin);
    if (pts.length > 1) map.fitBounds(L.latLngBounds(pts).pad(0.18));
    else if (pts.length === 1) map.setView(pts[0], 10);
    else map.setView(CONFIG.defaultCenter, CONFIG.defaultZoom);
  }

  /* -------------------------------------------------------------- filtering */
  function matches(c) {
    if (state.filters.has_league && !c.has_league) return false;
    if (state.filters.accepting && !c.accepting) return false;
    if (state.filters.junior && !c.junior) return false;
    if (state.filters.senior && !c.senior) return false;
    return true;
  }

  function compute() {
    var list = state.chapters.filter(matches).map(function (c) {
      var copy = Object.assign({}, c);
      copy.distance = state.origin ? miles(state.origin, [c.lat, c.lng]) : null;
      return copy;
    });

    if (state.origin) {
      list = list.filter(function (c) { return c.distance <= state.radius; });
      list.sort(function (a, b) { return a.distance - b.distance; });
    } else {
      list.sort(function (a, b) { return a.name.localeCompare(b.name); });
    }
    return list;
  }

  /* -------------------------------------------------------------- rendering */
  function cardHtml(c) {
    var badges = [];
    if (c.accepting) badges.push('<span class="tag tag--open">Accepting applications</span>');
    else if (c.has_league) badges.push('<span class="tag">Applications closed</span>');
    if (c.junior) badges.push('<span class="tag tag--gold">Junior &middot; Grades 6&ndash;8</span>');
    if (c.senior) badges.push('<span class="tag tag--gold">Senior &middot; Grades 9&ndash;12</span>');
    if (!c.has_league) badges.push('<span class="tag tag--crimson">Program in formation</span>');

    return '' +
      '<article class="chapter-card" data-id="' + esc(c.id) + '" tabindex="0" aria-label="' + esc(c.name) + '">' +
        '<div class="chapter-card__top">' +
          '<h3 class="chapter-card__name">' + esc(c.name) + '</h3>' +
          (c.distance != null ? '<span class="chapter-card__dist">' + c.distance.toFixed(1) + ' mi</span>' : '') +
        '</div>' +
        '<div class="chapter-card__meta">' +
          '<div>' + esc(c.city) + ', ' + esc(c.state) + ' ' + esc(c.zip) + ' &middot; ' + esc(c.province) + ' Province</div>' +
          '<div><strong>Meets:</strong> ' + esc(c.meets) + '</div>' +
          '<div><strong>Location:</strong> ' + esc(c.venue) + '</div>' +
        '</div>' +
        '<div class="tags">' + badges.join('') + '</div>' +
        '<div class="chapter-card__actions">' +
          (c.has_league && c.accepting
            ? '<button type="button" class="btn btn--primary btn--sm" data-apply="' + esc(c.id) + '">Apply to this Kappa League</button>'
            : '<button type="button" class="btn btn--ghost btn--sm" data-apply="' + esc(c.id) + '">Join the interest list</button>') +
          '<button type="button" class="btn btn--outline btn--sm" data-contact="' + esc(c.id) + '">Contact program director</button>' +
        '</div>' +
      '</article>';
  }

  function emptyHtml() {
    var where = state.originLabel ? ' of ' + esc(state.originLabel) : ' of your location';
    return '' +
      '<div class="empty-state">' +
        '<h3>No active Kappa League program found within ' + state.radius + ' miles' + where + '.</h3>' +
        '<p class="muted">Widen your search radius, or use one of the options below. The Commission tracks every request as a signal for where the next charter should go.</p>' +
        '<div class="btn-row">' +
          '<button type="button" class="btn btn--primary" data-modal-open="modal-start">Request a Kappa League in your district</button>' +
          '<button type="button" class="btn btn--outline" data-modal-open="modal-province">Contact your Province Guide Right Director</button>' +
        '</div>' +
      '</div>';
  }

  var PREVIEW = 6;  // programs shown before a location search narrows the list

  function render() {
    var list = compute();
    var shown = list;
    var capped = false;
    if (!state.origin && list.length > PREVIEW) { shown = list.slice(0, PREVIEW); capped = true; }

    if (el.count) {
      el.count.textContent = state.origin
        ? list.length + (list.length === 1 ? ' program' : ' programs') + ' within ' + state.radius + ' miles' +
          (state.originLabel ? ' of ' + state.originLabel : '')
        : list.length + (list.length === 1 ? ' program' : ' programs') + ' listed nationwide';
    }

    el.list.innerHTML = list.length
      ? shown.map(cardHtml).join('') +
        (capped
          ? '<p class="list-hint"><strong>Showing ' + PREVIEW + ' of ' + list.length + ' programs.</strong> ' +
            'Enter a ZIP code or city above to see the programs closest to you.</p>'
          : '')
      : emptyHtml();

    drawMarkers(shown);
    announce(el.count ? el.count.textContent : '');
    if (state.activeId && !shown.some(function (c) { return c.id === state.activeId; })) state.activeId = null;
    paintActive();
  }

  function paintActive() {
    var cards = el.list.querySelectorAll('.chapter-card');
    for (var i = 0; i < cards.length; i++) {
      cards[i].setAttribute('data-active', cards[i].getAttribute('data-id') === state.activeId ? 'true' : 'false');
    }
    Object.keys(markers).forEach(function (id) {
      markers[id].setIcon(pinIcon(id === state.activeId));
    });
  }

  function setActive(id, scrollCard) {
    state.activeId = id;
    paintActive();
    if (!id) return;
    if (map && markers[id]) {
      map.panTo(markers[id].getLatLng(), { animate: true });
      markers[id].openPopup();
    }
    if (scrollCard !== false) {
      var card = el.list.querySelector('.chapter-card[data-id="' + id + '"]');
      if (card) card.scrollIntoView({ block: 'nearest' });
    }
  }

  /* ---------------------------------------------------------------- modals */
  function findChapter(id) {
    for (var i = 0; i < state.chapters.length; i++) if (state.chapters[i].id === id) return state.chapters[i];
    return null;
  }

  function fillModal(prefix, c) {
    var box = document.getElementById(prefix + '-chapter');
    if (box) {
      box.innerHTML = '<strong>' + esc(c.name) + '</strong>' +
        esc(c.city) + ', ' + esc(c.state) + ' &middot; ' + esc(c.province) + ' Province' +
        '<br>Meets: ' + esc(c.meets);
    }
    var idField = document.getElementById(prefix + '-chapter-id');
    if (idField) idField.value = c.id;
    var nameField = document.getElementById(prefix + '-chapter-name');
    if (nameField) nameField.value = c.name;
    var status = document.getElementById(prefix + '-status');
    if (status) status.hidden = true;
    var form = document.getElementById(prefix + '-form');
    if (form) form.hidden = false;
  }

  root.addEventListener('click', function (e) {
    var applyBtn = e.target.closest('[data-apply], [data-popup-apply]');
    if (applyBtn) {
      var aid = applyBtn.getAttribute('data-apply') || applyBtn.getAttribute('data-popup-apply');
      var ac = findChapter(aid);
      if (ac) { fillModal('apply', ac); window.NGRC.openModal('modal-apply'); }
      return;
    }
    var contactBtn = e.target.closest('[data-contact]');
    if (contactBtn) {
      var cc = findChapter(contactBtn.getAttribute('data-contact'));
      if (cc) { fillModal('contact', cc); window.NGRC.openModal('modal-contact'); }
      return;
    }
    var card = e.target.closest('.chapter-card');
    if (card) setActive(card.getAttribute('data-id'), false);
  });

  // Popup buttons render outside #locator in Leaflet's pane on some setups.
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-popup-apply]');
    if (!b || root.contains(b)) return;
    var c = findChapter(b.getAttribute('data-popup-apply'));
    if (c) { fillModal('apply', c); window.NGRC.openModal('modal-apply'); }
  });

  el.list.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var card = e.target.closest('.chapter-card');
    if (card) { e.preventDefault(); setActive(card.getAttribute('data-id'), false); }
  });

  /* ----------------------------------------------------------- form wiring */
  function wireForm(prefix, successMsg) {
    var form = document.getElementById(prefix + '-form');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // PRODUCTION: POST new FormData(form) to your endpoint, then show the status panel.
      var status = document.getElementById(prefix + '-status');
      if (status) { status.hidden = false; status.textContent = successMsg; }
      form.hidden = true;
    });
  }
  wireForm('apply', 'Application started. The chapter Guide Right Chairman receives this request and will follow up with orientation details. (Demo build: no data was transmitted.)');
  wireForm('contact', 'Your message is queued for the chapter Guide Right Chairman. (Demo build: no data was transmitted.)');
  wireForm('start', 'Request logged for the National Guide Right Commission. (Demo build: no data was transmitted.)');
  wireForm('province', 'Your message is queued for the Province Guide Right Director. (Demo build: no data was transmitted.)');

  /* ------------------------------------------------------------- listeners */
  if (el.form) {
    el.form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = el.query.value.trim();
      if (!q) { announce('Enter a ZIP code or city and state to search.'); el.query.focus(); return; }
      announce('Searching…');
      geocode(q).then(function (res) {
        state.origin = res.coords;
        state.originLabel = res.label;
        render();
      }).catch(function (err) {
        announce(err.message || 'Search failed. Try a 5-digit ZIP code.');
        el.list.innerHTML = '<div class="empty-state"><h3>We could not locate that place.</h3>' +
          '<p class="muted">' + esc(err.message || 'Try a 5-digit ZIP code, or a city and state.') + '</p></div>';
      });
    });
  }

  if (el.geo) {
    el.geo.addEventListener('click', function () {
      if (!navigator.geolocation) { announce('Location services are unavailable in this browser.'); return; }
      el.geo.disabled = true;
      announce('Finding your location…');
      navigator.geolocation.getCurrentPosition(function (pos) {
        state.origin = [pos.coords.latitude, pos.coords.longitude];
        state.originLabel = 'your location';
        el.query.value = '';
        el.geo.disabled = false;
        render();
      }, function () {
        el.geo.disabled = false;
        announce('Location permission was declined. Enter a ZIP code instead.');
        el.query.focus();
      }, { timeout: 10000, maximumAge: 300000 });
    });
  }

  if (el.radius) {
    el.radius.addEventListener('change', function () {
      state.radius = parseInt(el.radius.value, 10) || CONFIG.defaultRadius;
      render();
    });
  }

  for (var i = 0; i < el.filters.length; i++) {
    el.filters[i].addEventListener('click', function () {
      var key = this.getAttribute('data-filter');
      var on = this.getAttribute('aria-pressed') !== 'true';
      this.setAttribute('aria-pressed', on ? 'true' : 'false');
      state.filters[key] = on;
      render();
    });
  }

  for (var j = 0; j < el.viewBtns.length; j++) {
    el.viewBtns[j].addEventListener('click', function () {
      var v = this.getAttribute('data-view-btn');
      state.view = v;
      root.setAttribute('data-view', v);
      for (var k = 0; k < el.viewBtns.length; k++) {
        el.viewBtns[k].setAttribute('aria-pressed', el.viewBtns[k].getAttribute('data-view-btn') === v ? 'true' : 'false');
      }
      if (v === 'map' && map) setTimeout(function () { map.invalidateSize(); }, 60);
    });
  }

  /* ------------------------------------------------------------------ boot */
  initMap();
  el.list.innerHTML = '<div class="empty-state"><p class="muted">Loading chapter programs…</p></div>';

  fetch(CONFIG.dataUrl)
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (json) {
      state.chapters = json.chapters || [];
      render();
    })
    .catch(function () {
      el.list.innerHTML = '<div class="empty-state"><h3>Chapter directory unavailable.</h3>' +
        '<p class="muted">The program list could not be loaded. Reload the page, or contact the National Guide Right Commission for help finding a program.</p></div>';
      announce('Chapter directory unavailable.');
    });
})();
