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
    i.value = ref === 'blueflame' ? 'Blueflame website' : 'Website';
  });

  // Notes and the page the form was sent from go into the lead's Description.
  document.querySelectorAll('form.lead').forEach(function (f) {
    f.addEventListener('submit', function () {
      var lines = [];
      f.querySelectorAll('[data-desc]').forEach(function (el) {
        if ((el.type === 'radio' && !el.checked) || !el.value) return;
        lines.push(el.getAttribute('data-desc') + ': ' + el.value.trim());
      });
      lines.push('Page: ' + location.pathname);
      f.querySelector('input[name="Description"]').value = lines.join('\n');
      var btn = f.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    });
  });
})();
