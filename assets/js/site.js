/* Shared site behavior: mobile drawer, modal plumbing, footer year.
   No dependencies. Progressive: every page works without it. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- drawer */
  var drawer = document.getElementById('drawer');
  var openBtn = document.getElementById('drawer-open');
  var lastFocus = null;

  function setDrawer(open) {
    if (!drawer) return;
    drawer.setAttribute('data-open', open ? 'true' : 'false');
    if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) {
      lastFocus = document.activeElement;
      var first = drawer.querySelector('.drawer__close');
      if (first) first.focus();
    } else if (lastFocus) {
      lastFocus.focus();
    }
  }

  if (openBtn) openBtn.addEventListener('click', function () { setDrawer(true); });
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('[data-drawer-close]') || e.target.classList.contains('drawer__scrim')) {
        setDrawer(false);
      }
    });
  }

  /* ----------------------------------------------------------------- modals */
  var openModal = null;

  function trap(e) {
    if (!openModal || e.key !== 'Tab') return;
    var f = openModal.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  window.NGRC = window.NGRC || {};

  window.NGRC.openModal = function (id) {
    var m = document.getElementById(id);
    if (!m) return;
    lastFocus = document.activeElement;
    m.setAttribute('data-open', 'true');
    document.documentElement.style.overflow = 'hidden';
    openModal = m;
    var target = m.querySelector('input, select, textarea, button');
    if (target) target.focus();
  };

  window.NGRC.closeModal = function () {
    if (!openModal) return;
    openModal.setAttribute('data-open', 'false');
    openModal = null;
    document.documentElement.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  };

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-modal-close]') || e.target.classList.contains('modal__scrim')) {
      window.NGRC.closeModal();
    }
    var opener = e.target.closest('[data-modal-open]');
    if (opener) {
      e.preventDefault();
      window.NGRC.openModal(opener.getAttribute('data-modal-open'));
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (openModal) window.NGRC.closeModal();
      else if (drawer && drawer.getAttribute('data-open') === 'true') setDrawer(false);
    }
    trap(e);
  });

  /* ------------------------------------------------------------- footer year */
  var y = document.querySelectorAll('[data-year]');
  for (var i = 0; i < y.length; i++) y[i].textContent = String(new Date().getFullYear());
})();
