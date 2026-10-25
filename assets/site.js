// Header shadow on scroll, mobile menu, lead form.
(function () {
  var top = document.querySelector('.top');
  var onScroll = function () { if (top) top.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.textContent = open ? 'Close' : 'Menu';
  });

  // Tag where the visitor came from (?ref=blueflame from blue-flame.co.ke) so leads show their route in Zoho CRM.
  var ref = new URLSearchParams(location.search).get('ref');
  try { if (ref) sessionStorage.setItem('rema_ref', ref); ref = ref || sessionStorage.getItem('rema_ref'); } catch (e) {}
  document.querySelectorAll('input[name="Lead Source"]').forEach(function (i) {
    i.value = ref === 'blueflame' ? 'ReMA via Blueflame' : 'ReMA website';
  });

  // Until the Zoho CRM web-to-lead form is connected, the form confirms on the page and opens an e-mail with the details.
  document.querySelectorAll('form.lead').forEach(function (f) {
    if (f.getAttribute('action')) return; // connected to Zoho: let it post normally
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var d = new FormData(f), lines = [];
      d.forEach(function (v, k) { if (v) lines.push(k + ': ' + v); });
      location.href = 'mailto:office@blue-flame.co.ke?subject=' + encodeURIComponent('ReMA demo request') + '&body=' + encodeURIComponent(lines.join('\n'));
      var done = f.querySelector('.form-done'); if (done) done.style.display = 'block';
    });
  });
})();
